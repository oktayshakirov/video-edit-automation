"""Which articles still have no video?

Coverage is *derived*, never tracked: an article counts as done when a project
script in `projects/` names it, or when the site's own `videos.json` carries an
entry pointing at it. There is no list to keep up to date, so there is no list
to forget to update.

    python3 tools/topics.py crypto
    python3 tools/topics.py tinnitus --covered
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

CODING = Path.home() / "Coding"
REPO = Path(__file__).resolve().parent.parent

SITES = {
    "crypto": {
        "posts": CODING / "crypto-wiki/content/posts",
        "videos": CODING / "crypto-wiki/json/videos.json",
        "projects": ("crypto-long", "crypto-short"),
    },
    "tinnitus": {
        "posts": CODING / "tinnitus-blog/content/posts",
        "videos": CODING / "tinnitus-blog/src/data/videos.json",
        "projects": ("tinnitus-long", "tinnitus-short"),
    },
}

# A project script names its article one of three ways. Oldest first; new
# scripts should set SOURCE_POST and nothing else.
PATTERNS = (
    re.compile(r'^SOURCE_POST\s*=\s*["\']([a-z0-9-]+)["\']', re.M),
    re.compile(r'https?://[^"\'\s]*/posts/([a-z0-9-]+)'),
    re.compile(r'content/posts/([a-z0-9-]+)\.mdx'),
)


def slug_of(script: Path) -> str | None:
    text = script.read_text(errors="replace")
    # A wrapped URL is two adjacent string literals; join them before matching
    # or the slug sits on a line the pattern never sees.
    text = re.sub(r'["\']\s*\n\s*["\']', "", text)
    for pat in PATTERNS:
        m = pat.search(text)
        if m:
            return m.group(1)
    return None


def title_of(post: Path) -> str:
    for line in post.read_text(errors="replace").splitlines()[:15]:
        m = re.match(r'''title:\s*["']?(.+?)["']?\s*$''', line)
        if m:
            return m.group(1)
    return post.stem


def built(site: dict) -> dict[str, set[str]]:
    """slug -> {"long", "short"} already built in this repo."""
    out: dict[str, set[str]] = {}
    for proj in site["projects"]:
        kind = "long" if proj.endswith("-long") else "short"
        d = REPO / "projects" / proj
        for script in sorted(d.glob("*.py")):
            slug = slug_of(script)
            if slug:
                out.setdefault(slug, set()).add(kind)
    return out


def published(site: dict) -> set[str]:
    """Article slugs the site's registry already points a video at."""
    p = site["videos"]
    if not p.exists():
        return set()
    data = json.loads(p.read_text())
    out = set()
    for v in data.get("videos", []):
        target = v.get("target") or {}
        if target.get("type") in (None, "posts") and target.get("slug"):
            out.add(target["slug"])
        for extra in v.get("alsoOn") or []:
            if isinstance(extra, dict) and extra.get("slug"):
                out.add(extra["slug"])
    return out


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("site", choices=sorted(SITES))
    ap.add_argument("--covered", action="store_true",
                    help="list what is already done instead of what is left")
    ap.add_argument("--limit", type=int, default=0)
    args = ap.parse_args()

    site = SITES[args.site]
    if not site["posts"].is_dir():
        print(f"no posts dir: {site['posts']}", file=sys.stderr)
        return 1

    have, live = built(site), published(site)
    posts = [p for p in sorted(site["posts"].glob("*.mdx"))
             if not p.stem.startswith("_")]

    done, todo = [], []
    for p in posts:
        formats = have.get(p.stem, set())
        if p.stem in live:
            formats = formats | {"published"}
        (done if formats else todo).append((p.stem, title_of(p), formats))

    rows = done if args.covered else todo
    if args.limit:
        rows = rows[: args.limit]

    label = "already has a video" if args.covered else "no video yet"
    print(f"{args.site}: {len(done)} of {len(posts)} covered - showing "
          f"{len(rows)} {label}\n")
    for slug, title, formats in rows:
        mark = f"  [{', '.join(sorted(formats))}]" if formats else ""
        print(f"  {slug}\n      {title}{mark}")

    if not args.covered:
        print(f"\nAn off-site topic - one with no article - is fine when asked "
              f"for, but it is never suggested from this list.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
