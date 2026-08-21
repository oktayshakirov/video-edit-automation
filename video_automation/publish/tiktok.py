"""TikTok Content Posting API — direct post, private, one account per project.

Three sandbox apps, one per TikTok account. Each app has its own client key and
secret, and each authorisation produces a token bound to one TikTok user by
`open_id`. That binding is the whole safety story here: the apps all live under
one developer account, so nothing about the app itself says which profile a post
lands on, and three authorisations done in one browser session will happily all
point at whichever account happened to be logged in.

So `open_id` is recorded at authorisation time and checked again before every
post. A mismatch refuses the post rather than publishing a crypto short to the
drone account.

Uploads go to the account's **inbox as a draft**, not as a direct post. That is
not a preference, it is the only route open to us. Direct post was tried first
and TikTok refused with `unaudited_client_can_only_post_to_private_accounts`:
an unaudited client may direct-post only to an account whose *profile* is
private, and all three of these are public brand accounts. The post's own
privacy level is irrelevant — `creator_info` cheerfully lists SELF_ONLY as an
option and `init` refuses anyway.

Applying for the audit would lift this, and this pipeline deliberately does not:
the audit's UX requirements describe a consumer publishing app — creator
nickname on screen, manual privacy selection with no default, Duet/Stitch
toggles, a preview, explicit consent — which an automation posting the owner's
own videos structurally cannot satisfy.

The cost of the inbox route is real and worth stating plainly: **TikTok accepts
no caption and no cover for an inbox upload.** The video lands in the account's
inbox and the user writes the caption and picks the cover in the app. So the
caption this pipeline generates is printed for the user to paste, not sent.
"""
from __future__ import annotations

import json
import mimetypes
import time
import urllib.parse
import urllib.request
from dataclasses import dataclass
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
SECRETS = REPO / ".secrets"
APPS_FILE = SECRETS / "tiktok.json"
TOKENS_FILE = SECRETS / "tiktok-tokens.json"

# The redirect URI is PER APP and lives in tiktok.json, because the three apps
# are registered against three different domains. TikTok compares it byte for
# byte against what the app has registered and rejects the whole authorisation
# with a bare `redirect_uri` error on any difference, including a missing `www.`
# or a trailing slash.
#
# TikTok requires a web redirect URI to be absolute https, static and
# parameter-free, which rules out n8n's own callback on http://localhost. The
# page does not have to render anything - all three currently 404 - because the
# browser is redirected there with ?code=... and the address bar is all we need.

AUTH_URL = "https://www.tiktok.com/v2/auth/authorize/"
TOKEN_URL = "https://open.tiktokapis.com/v2/oauth/token/"
USER_INFO_URL = "https://open.tiktokapis.com/v2/user/info/"
CREATOR_INFO_URL = "https://open.tiktokapis.com/v2/post/publish/creator_info/query/"
INIT_URL = "https://open.tiktokapis.com/v2/post/publish/video/init/"
INBOX_INIT_URL = "https://open.tiktokapis.com/v2/post/publish/inbox/video/init/"

# TikTok's upload chunking rules. A chunk must be at least 5 MB and at most
# 64 MB, so a whole file can only go up in one piece if it is under the ceiling.
# Everything this repo had tested against was a 5-second clip, which is why a
# hardcoded single chunk survived until the first real render: a 145 MB short
# came back "The chunk size is invalid".
#
# The remainder does NOT become an extra chunk. total_chunk_count is
# floor(size / chunk_size) and the final chunk carries whatever is left over,
# so it can be up to just under 2x chunk_size. Sending an extra short chunk
# instead is the other way to get "chunk size is invalid".
CHUNK_MIN = 5 * 1024 * 1024
CHUNK_MAX = 64 * 1024 * 1024
CHUNK_TARGET = 16 * 1024 * 1024
CHUNK_COUNT_MAX = 1000
STATUS_URL = "https://open.tiktokapis.com/v2/post/publish/status/fetch/"

# `video.upload` is the inbox/draft scope. `video.publish` is direct post, which
# is unusable here (see the module docstring) but is kept because it is what
# `creator_info` needs, and that is the only way to read the account nickname.
SCOPES = "user.info.basic,video.upload,video.publish"
PROJECTS = ("crypto", "tinnitus", "drone")


class TikTokError(RuntimeError):
    pass


# --------------------------------------------------------------------------- io


def _read(path: Path) -> dict:
    if not path.exists():
        return {}
    return json.loads(path.read_text())


def _write(path: Path, data: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2) + "\n")
    path.chmod(0o600)


def app(project: str) -> dict:
    apps = _read(APPS_FILE)
    if project not in apps:
        raise TikTokError(f"No TikTok app for '{project}' in {APPS_FILE}.")
    return apps[project]


def redirect_uri(project: str) -> str:
    uri = app(project).get("redirectUri")
    if not uri:
        raise TikTokError(
            f"No redirectUri for '{project}' in {APPS_FILE}. It must match the app's "
            f"registered Login Kit redirect URI exactly."
        )
    return uri


def _request(url: str, *, data=None, headers=None, method=None) -> dict:
    req = urllib.request.Request(url, data=data, headers=headers or {}, method=method)
    try:
        with urllib.request.urlopen(req) as res:
            body = res.read().decode()
    except urllib.error.HTTPError as err:
        raise TikTokError(f"{method or 'GET'} {url} -> HTTP {err.code}: {err.read().decode()[:600]}") from None
    # The byte upload answers with an empty body, and TikTok occasionally sends a
    # bare `null`. Neither is an error, so normalise both to an empty dict rather
    # than letting `.get` fail on None.
    try:
        payload = json.loads(body) if body.strip() else {}
    except json.JSONDecodeError:
        payload = {}
    if not isinstance(payload, dict):
        payload = {}
    # TikTok reports failures inside a 200 body, so the status code alone is not
    # enough to tell a successful call from a rejected one.
    err = payload.get("error") or {}
    if err and err.get("code") not in (None, "ok"):
        raise TikTokError(f"{url} -> {err.get('code')}: {err.get('message')}")
    return payload


def _post_json(url: str, token: str, body: dict) -> dict:
    return _request(
        url,
        data=json.dumps(body).encode(),
        headers={
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json; charset=UTF-8",
        },
        method="POST",
    )


# ------------------------------------------------------------------------ oauth


def authorize_url(project: str, state: str | None = None) -> str:
    """The URL to open in a browser logged in as *that* project's account."""
    query = urllib.parse.urlencode(
        {
            "client_key": app(project)["clientKey"],
            "scope": SCOPES,
            "response_type": "code",
            "redirect_uri": redirect_uri(project),
            "state": state or project,
        }
    )
    return f"{AUTH_URL}?{query}"


def exchange_code(project: str, code: str) -> dict:
    """Trade the ?code= from the callback URL for a token, and record open_id."""
    cfg = app(project)
    # The code arrives URL-encoded in the address bar and TikTok appends a
    # fragment; both make an otherwise valid code fail with a confusing error.
    code = urllib.parse.unquote(code.strip()).split("#")[0].split("&")[0]
    payload = _request(
        TOKEN_URL,
        data=urllib.parse.urlencode(
            {
                "client_key": cfg["clientKey"],
                "client_secret": cfg["clientSecret"],
                "code": code,
                "grant_type": "authorization_code",
                "redirect_uri": redirect_uri(project),
            }
        ).encode(),
        headers={"Content-Type": "application/x-www-form-urlencoded"},
        method="POST",
    )
    return _store(project, payload)


def _store(project: str, payload: dict) -> dict:
    now = int(time.time())
    tokens = _read(TOKENS_FILE)
    record = tokens.get(project, {})
    record.update(
        {
            "access_token": payload["access_token"],
            "refresh_token": payload.get("refresh_token", record.get("refresh_token")),
            "open_id": payload.get("open_id", record.get("open_id")),
            "expires_at": now + int(payload.get("expires_in", 0)),
            "refresh_expires_at": now + int(payload.get("refresh_expires_in", 0)),
        }
    )
    tokens[project] = record
    _write(TOKENS_FILE, tokens)
    return record


def refresh(project: str) -> dict:
    cfg = app(project)
    record = _read(TOKENS_FILE).get(project)
    if not record or not record.get("refresh_token"):
        raise TikTokError(f"No stored TikTok token for '{project}'. Run the authorise step.")
    payload = _request(
        TOKEN_URL,
        data=urllib.parse.urlencode(
            {
                "client_key": cfg["clientKey"],
                "client_secret": cfg["clientSecret"],
                "grant_type": "refresh_token",
                "refresh_token": record["refresh_token"],
            }
        ).encode(),
        headers={"Content-Type": "application/x-www-form-urlencoded"},
        method="POST",
    )
    return _store(project, payload)


def access_token(project: str) -> str:
    """A valid token, refreshed if it is within five minutes of expiring."""
    record = _read(TOKENS_FILE).get(project)
    if not record:
        raise TikTokError(
            f"No stored TikTok token for '{project}'. Open authorize_url('{project}') "
            f"in a browser logged in as that account, then run exchange_code."
        )
    if record.get("expires_at", 0) - time.time() < 300:
        record = refresh(project)
    return record["access_token"]


def whoami(project: str) -> dict:
    """open_id and display name of whichever account this token belongs to."""
    url = f"{USER_INFO_URL}?{urllib.parse.urlencode({'fields': 'open_id,display_name'})}"
    payload = _request(url, headers={"Authorization": f"Bearer {access_token(project)}"})
    return payload.get("data", {}).get("user", {})


def bind_account(project: str) -> dict:
    """Record which TikTok account this project posts to. Run once, after auth."""
    user = whoami(project)
    tokens = _read(TOKENS_FILE)
    tokens[project]["open_id"] = user.get("open_id")
    tokens[project]["display_name"] = user.get("display_name")
    _write(TOKENS_FILE, tokens)
    return user


def assert_right_account(project: str) -> dict:
    """Refuse to post if the token no longer points at the bound account."""
    record = _read(TOKENS_FILE).get(project, {})
    expected = record.get("open_id")
    user = whoami(project)
    if expected and user.get("open_id") != expected:
        raise TikTokError(
            f"Token for '{project}' now belongs to {user.get('display_name')} "
            f"({user.get('open_id')}), not the account it was bound to ({expected}). "
            f"Refusing to post. Re-authorise while logged in as the right account."
        )
    return user


# ------------------------------------------------------------------------- post


@dataclass
class Post:
    publish_id: str
    account: str


def creator_info(project: str) -> dict:
    """Required before a direct post, and the source of the account nickname."""
    return _post_json(CREATOR_INFO_URL, access_token(project), {}).get("data", {})


def post_video(
    project: str,
    video: Path,
    title: str | None = None,
    *,
    cover_ms: int = 1000,
    privacy: str = "SELF_ONLY",
    direct: bool = False,
) -> Post:
    """Upload a video to the account's inbox as a draft. Returns its publish id.

    `direct=True` switches to the direct-post endpoint, which needs an audited
    client or a private account and will otherwise fail with
    `unaudited_client_can_only_post_to_private_accounts`. It is kept so the
    switch is one flag away if the account situation ever changes, not because
    it works today.

    `title` and `cover_ms` are ignored on the inbox route — TikTok accepts
    neither for a draft. They apply only when `direct=True`.
    """
    video = Path(video)
    if not video.exists():
        raise TikTokError(f"No such video: {video}")
    size = video.stat().st_size

    user = assert_right_account(project)
    token = access_token(project)

    # FILE_UPLOAD rather than PULL_FROM_URL in both cases: pulling requires a
    # verified domain or URL prefix on the app, uploading requires nothing.
    chunk_size, chunk_count = _chunk_plan(size)
    source_info = {
        "source": "FILE_UPLOAD",
        "video_size": size,
        "chunk_size": chunk_size,
        "total_chunk_count": chunk_count,
    }
    if direct:
        body = {
            "post_info": {
                "title": title or "",
                "privacy_level": privacy,
                "disable_duet": False,
                "disable_comment": False,
                "disable_stitch": False,
                "video_cover_timestamp_ms": cover_ms,
            },
            "source_info": source_info,
        }
        init = _post_json(INIT_URL, token, body)
    else:
        init = _post_json(INBOX_INIT_URL, token, {"source_info": source_info})
    data = init.get("data", {})
    upload_url = data.get("upload_url")
    publish_id = data.get("publish_id")
    if not upload_url or not publish_id:
        raise TikTokError(f"init returned no upload url: {init}")

    content_type = mimetypes.guess_type(str(video))[0] or "video/mp4"
    with video.open("rb") as fh:
        for i in range(chunk_count):
            start = i * chunk_size
            # Last chunk takes everything that is left, not just chunk_size.
            end = size - 1 if i == chunk_count - 1 else start + chunk_size - 1
            fh.seek(start)
            data = fh.read(end - start + 1)
            _request(
                upload_url,
                data=data,
                headers={
                    "Content-Type": content_type,
                    "Content-Length": str(len(data)),
                    "Content-Range": f"bytes {start}-{end}/{size}",
                },
                method="PUT",
            )
    return Post(publish_id=publish_id, account=user.get("display_name", project))


def _chunk_plan(size: int) -> tuple[int, int]:
    """Chunk size and count for a file of `size` bytes, per TikTok's rules.

    A file that fits inside one chunk goes up whole; that is what the API wants
    and it avoids a pointless second request. Above the ceiling the file is cut
    into equal chunks with the remainder folded into the last one.
    """
    if size <= CHUNK_MAX:
        return size, 1
    chunk = CHUNK_TARGET
    # Very large files would otherwise exceed the 1000-chunk cap.
    if size // chunk > CHUNK_COUNT_MAX:
        chunk = -(-size // CHUNK_COUNT_MAX)
    chunk = max(CHUNK_MIN, min(chunk, CHUNK_MAX))
    count = size // chunk
    if count > CHUNK_COUNT_MAX:
        # 1000 chunks of 64 MB is 64 GB, far past TikTok's own file size limit,
        # so this is a file that was never going to be accepted. Say so here
        # rather than sending a request that cannot be valid.
        raise TikTokError(
            f"{size / 1024**3:.1f} GB is too large for TikTok: it needs "
            f"{count} chunks and the API allows {CHUNK_COUNT_MAX}."
        )
    return chunk, count


def status(project: str, publish_id: str) -> dict:
    return _post_json(
        STATUS_URL, access_token(project), {"publish_id": publish_id}
    ).get("data", {})


def wait_until_published(project: str, publish_id: str, timeout: int = 180) -> dict:
    """Poll until the draft lands, and return the last status either way.

    A timeout is deliberately **not** an error. Once `init` has returned a
    publish id and the bytes are up, the video is on TikTok's side and the draft
    arrives on its own; `PROCESSING_UPLOAD` simply means their processing has not
    caught up. Raising here would report a successful upload as a failure and
    invite a re-run, which double-posts. Only an explicit FAILED is an error.
    """
    deadline = time.time() + timeout
    last: dict = {}
    while time.time() < deadline:
        last = status(project, publish_id)
        state = last.get("status")
        if state in ("PUBLISH_COMPLETE", "SEND_TO_USER_INBOX"):
            return last
        if state == "FAILED":
            raise TikTokError(f"TikTok rejected the upload: {last}")
        time.sleep(5)
    return last
