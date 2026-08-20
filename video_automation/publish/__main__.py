"""CLI for the TikTok leg. `python -m video_automation.publish <command>`."""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

from . import tiktok


def _run(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(prog="video_automation.publish")
    sub = ap.add_subparsers(dest="command", required=True)

    p = sub.add_parser("auth-url", help="Print the URL to authorise one account")
    p.add_argument("project", choices=tiktok.PROJECTS)

    p = sub.add_parser("auth", help="Exchange the ?code= from the callback for a token")
    p.add_argument("project", choices=tiktok.PROJECTS)
    p.add_argument("code", help="The code query parameter, or the whole callback URL")

    p = sub.add_parser("whoami", help="Which TikTok account a stored token belongs to")
    p.add_argument("project", choices=tiktok.PROJECTS)

    p = sub.add_parser("post", help="Upload a video to the account's TikTok inbox as a draft")
    p.add_argument("project", choices=tiktok.PROJECTS)
    p.add_argument("video", type=Path)
    p.add_argument("--caption", default="", help="Printed for the user to paste; TikTok takes no caption on a draft")
    p.add_argument("--direct", action="store_true",
                   help="Direct post instead of a draft. Only works on a PRIVATE account.")
    p.add_argument("--apply", action="store_true", help="Without this, only prints the plan")

    args = ap.parse_args(argv)

    if args.command == "auth-url":
        print(tiktok.authorize_url(args.project))
        return 0

    if args.command == "auth":
        raw = args.code
        # Accept the whole pasted callback URL, which is what a browser gives you.
        if "code=" in raw:
            from urllib.parse import parse_qs, urlparse
            raw = parse_qs(urlparse(raw).query).get("code", [raw])[0]
        tiktok.exchange_code(args.project, raw)
        user = tiktok.bind_account(args.project)
        print(f"{args.project} -> bound to {user.get('display_name')} ({user.get('open_id')})")
        print("Check that name is the account you meant. If it is not, re-authorise "
              "in a private window logged in as the right one.")
        return 0

    if args.command == "whoami":
        user = tiktok.whoami(args.project)
        print(f"{args.project} -> {user.get('display_name')} ({user.get('open_id')})")
        return 0

    if args.command == "post":
        if not args.apply:
            print(f"Would upload {args.video} to {args.project}'s TikTok inbox as a draft")
            print("  TikTok accepts no caption and no cover on a draft; both are set in the app.")
            if args.caption:
                print(f"\n  Caption to paste:\n    {args.caption}")
            print("\nNothing was uploaded. Re-run with --apply.")
            return 0
        post = tiktok.post_video(
            args.project, args.video, args.caption or None, direct=args.direct
        )
        print(f"Uploaded to {post.account}'s inbox, publish_id={post.publish_id}")
        result = tiktok.wait_until_published(args.project, post.publish_id)
        state = result.get("status")
        print(f"  {state}")
        if args.direct and state == "PUBLISH_COMPLETE":
            print("  Posted as SELF_ONLY, i.e. private. Flip it to public in the app.")
        elif state not in ("SEND_TO_USER_INBOX", "PUBLISH_COMPLETE"):
            print("  The bytes are uploaded and TikTok has the video; its processing")
            print("  has just not caught up. Do NOT re-run - that uploads a second copy.")
        print("  It is a DRAFT, not a post. Open TikTok, find it in your inbox,")
        print("  add the caption and cover there, and publish.")
        if args.caption:
            print(f"\n  Caption to paste:\n    {args.caption}")
        return 0

    return 1


def main(argv: list[str] | None = None) -> int:
    """Report a TikTok refusal as a message, not a traceback.

    Every failure here is a settings or authorisation problem with a name in it,
    and a stack trace buries the one line that says which.
    """
    try:
        return _run(argv)
    except tiktok.TikTokError as err:
        print(f"\nTikTok refused this: {err}\n", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
