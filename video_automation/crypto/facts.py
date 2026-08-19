"""thecrypto.wiki's structured frontmatter, as beat payloads.

**This is the one place in the whole setup where content scales without hitting
the mass-production failure mode**, and the reason is that the *data* is the
script rather than a model's guess at one. Every one of the 27 exchange files
and 33 crypto-og files carries a `quickFacts` map and a `faqs` list that the
site already publishes, already fact-checks and already keeps updated. A
comparison short built from them is a hand-written script over numbers the site
stands behind, which is a different object from an AI-written script over stock
footage — and only the second one is the pattern the platforms suppress.

What is here is deliberately not a script generator. It reads the frontmatter,
says which keys are worth comparing on, and turns a selection into the payload
`ChecklistShot` and `Grid` already take. The angle, the verdict and the wording
stay hand-written, which is the same division the crypto skill records for
scripts generally: the script is the product.

**Four keys are on all 27 exchanges** — `founded`, `type`, `custody` and
`availability` — and those are the only ones a comparison across the whole set
can use. `headquarters` covers 24, `token` 19, `founder` 15, and everything
below that is a handful of files. `coverage()` prints this rather than leaving
it to be discovered by a beat with three blank rows in it.

`custody` is the one worth building the first comparison on. 21 of 27 are
flatly "Custodial", 3 are non-custodial and 3 are custodial with a self-custody
wallet alongside — which is a real answer to a real question ("which of these
actually gives you your keys?"), it is a judged list rather than a table, and
the judgement is the site's own rather than this repo's.
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path

import yaml
from PIL import Image, ImageDraw, ImageFont

from ..core.vertical import FONT_CAPTION, FONT_CAPTION_INDEX

CONTENT = Path.home() / "Coding/crypto-wiki/content"
IMAGES = Path.home() / "Coding/crypto-wiki/public/images"

KINDS = ("exchanges", "crypto-ogs", "posts")

# camelCase keys, as the site writes them, in the words a viewer reads them in.
# Anything not listed falls back to the key with its capitals spaced out, which
# is right for the long tail and wrong often enough to be worth a table.
LABELS = {
    "founded": "Founded",
    "headquarters": "HQ",
    "founder": "Founder",
    "ceo": "CEO",
    "owner": "Owner",
    "type": "Type",
    "custody": "Custody",
    "token": "Token",
    "availability": "Available",
    "regulation": "Regulated",
    "nationality": "Nationality",
    "knownFor": "Known for",
    "status": "Status",
}

# The site's images are landscape and small; the vertical rules about upscaling
# apply to anything pulled from here exactly as they do to a hand-picked file.
# `Entry.image` resolves the frontmatter path and returns None when the asset is
# missing, rather than handing a shot list a path that fails at render time.


def label_of(key: str) -> str:
    """A frontmatter key as a beat reads it."""
    if key in LABELS:
        return LABELS[key]
    spaced = re.sub(r"(?<!^)(?=[A-Z])", " ", key)
    return spaced[0].upper() + spaced[1:]


def head(value: str) -> str:
    """The first clause of a value, which is the part a beat has room for.

    The site writes a fact and then qualifies it in the same string — "Custodial;
    self-custody available via the separate Coinbase Wallet", "Global; US
    residents must use the separate Binance.US". The qualifier is the honest
    part and belongs in the narration; the clause before it is what fits on a
    card. Splitting on the semicolon rather than truncating keeps the short form
    a complete statement instead of a sentence cut off mid-word.
    """
    return value.split(";")[0].strip()


@dataclass(frozen=True)
class Entry:
    """One exchange, og or post, as the site publishes it."""

    kind: str
    slug: str
    title: str
    description: str
    image: Path | None
    quick_facts: dict[str, str]
    faqs: list[tuple[str, str]]

    def fact(self, key: str, short: bool = True) -> str | None:
        v = self.quick_facts.get(key)
        if v is None:
            return None
        return head(v) if short else v


def _frontmatter(path: Path) -> dict:
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---"):
        raise ValueError(f"{path} has no frontmatter")
    # Split on the closing fence only — the body below it is MDX and is not YAML.
    end = text.index("\n---", 3)
    return yaml.safe_load(text[3:end]) or {}


def load(kind: str, slug: str) -> Entry:
    """One entry by kind and slug, e.g. `load("exchanges", "binance")`."""
    if kind not in KINDS:
        raise ValueError(f"unknown kind {kind!r} — one of {KINDS}")
    path = CONTENT / kind / f"{slug}.mdx"
    if not path.exists():
        raise FileNotFoundError(path)
    fm = _frontmatter(path)

    img = fm.get("image")
    # Frontmatter paths are site-absolute ("/images/exchanges/binance.png").
    resolved = None
    if img:
        p = IMAGES / str(img).lstrip("/").removeprefix("images/")
        resolved = p if p.exists() else None

    facts = {str(k): str(v) for k, v in (fm.get("quickFacts") or {}).items()}
    faqs = [(str(f.get("question", "")), str(f.get("answer", "")))
            for f in (fm.get("faqs") or [])]
    return Entry(kind, slug, str(fm.get("title", slug)),
                 str(fm.get("description", "")), resolved, facts, faqs)


def load_all(kind: str) -> list[Entry]:
    """Every entry of a kind, minus the section index, slug-sorted."""
    out = []
    for p in sorted((CONTENT / kind).glob("*.mdx")):
        if p.stem.startswith("_"):
            continue
        out.append(load(kind, p.stem))
    return out


def coverage(entries: list[Entry]) -> list[tuple[str, int, int]]:
    """Every `quickFacts` key, how many entries carry it, out of how many.

    **Check this before choosing what to compare on.** A key that covers 15 of
    27 makes a beat that is missing eight rows, and the missing rows are not
    random — `token` is absent exactly from the exchanges that have no token,
    so a comparison on it silently drops the most interesting cases.
    """
    counts: dict[str, int] = {}
    for e in entries:
        for k in e.quick_facts:
            counts[k] = counts.get(k, 0) + 1
    n = len(entries)
    return sorted(((k, c, n) for k, c in counts.items()),
                  key=lambda r: (-r[1], r[0]))


def having(entries: list[Entry], key: str) -> list[Entry]:
    """Only the entries that actually carry `key`."""
    return [e for e in entries if key in e.quick_facts]


def contains(*needles: str):
    """A verdict predicate: true when the value mentions any of these.

    The default is a substring test rather than anything cleverer because the
    site's values are prose and the judgement is the script's to make. Pass
    something else when it matters — `contains("non-custodial")` is the whole
    of the custody question, but only because the site writes it that way
    every time.
    """
    low = [n.lower() for n in needles]
    return lambda v: any(n in v.lower() for n in low)


# `ChecklistShot` sets its items from x=200 at 54px, so a 1080 frame leaves
# about 860px of line. Measured rather than counted in characters: Futura is
# proportional and "Availability" is not the width of "MMMMMMMMMMMM".
ITEM_MAX_W = 860

# **Not a geometric limit.** Eight rows still fit inside the vertical safe box.
# The constraint is that a checklist reveals one item per caption of its own
# sentence, so every row has to be spoken — six rows is already a long beat in
# a thirty-five-second short, and 27 rows is not a graphic, it is a table.
# Comparing across the whole set is a research step; the beat gets the handful
# the script has an argument about.
MAX_ITEMS = 6


def _too_wide(text: str, size: int = 54, max_w: int = ITEM_MAX_W) -> bool:
    font = ImageFont.truetype(FONT_CAPTION, size, index=FONT_CAPTION_INDEX)
    probe = ImageDraw.Draw(Image.new("RGBA", (8, 8)))
    return probe.textlength(text, font=font) > max_w


def compare(entries: list[Entry], key: str, ok, *,
            with_value: bool = False, strict: bool = True
            ) -> list[tuple[str, bool]]:
    """A judged list across several entries, as a `checklist` payload.

    `ok` takes the raw value and returns the verdict — see `contains`. The item
    text is the entry's title, or `Title — value` with `with_value`.

    **The width check is not decoration.** An item too long for the line is
    drawn straight off the right edge of the frame: nothing clips it, nothing
    raises, and it is invisible until you look at the rendered frame. That is
    the same class of bug as the marks that were once scheduled past the last
    frame, and this is the cheap place to catch it — before a render, not after.
    Pass `strict=False` to get the list anyway while you are still choosing an
    angle.
    """
    rows, wide = [], []
    for e in having(entries, key):
        raw = e.quick_facts[key]
        text = f"{e.title} - {head(raw)}" if with_value else e.title
        if _too_wide(text):
            wide.append(text)
        rows.append((text, bool(ok(raw))))
    if wide and strict:
        raise ValueError(
            f"{len(wide)} item(s) are wider than the {ITEM_MAX_W}px line and "
            f"would draw off the frame: {wide[:3]} — shorten them, drop "
            f"`with_value`, or pass strict=False")
    if len(rows) > MAX_ITEMS and strict:
        raise ValueError(
            f"{len(rows)} rows is more than a beat can carry ({MAX_ITEMS}) — "
            f"every row has to be spoken. Pass the handful the script argues "
            f"about, not the whole set: compare([load('{entries[0].kind}', s) "
            f"for s in (...)], ...). Use strict=False to survey.")
    return rows


def facts_grid(entry: Entry, keys: list[str] | None = None,
               limit: int = 4) -> list[tuple[str, str]]:
    """One entry's quickFacts as a `grid` payload of (label, value) cards.

    `limit` defaults to 4 because that is where the portrait `Grid` drops from
    one column of wide cards to two narrow ones — see `longform/beats.py`. Four
    facts down a 9:16 frame is a beat; eight is a table, and a table is not a
    thing anybody reads on a phone.
    """
    keys = keys or [k for k in LABELS if k in entry.quick_facts]
    keys = [k for k in keys if k in entry.quick_facts][:limit]
    return [(label_of(k), head(entry.quick_facts[k])) for k in keys]
