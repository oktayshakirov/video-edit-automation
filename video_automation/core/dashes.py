"""No long dashes on screen, ever: a single hyphen in their place.

**The editor's standing rule (2026-11-07): no video made here shows an em or
en dash anywhere, only a plain `-`.** It already held for published metadata
(titles, descriptions, tags); this widens it to every glyph in the picture.
The second Love Swipe batch is what prompted it: the app's card text carries
em dashes ("Who texts first after an argument — you or your partner?") and
`Round.from_app` put them on screen unchanged.

**Why at the drawing call and not in every script.** On-screen text reaches
Pillow from about 130 call sites - beats, captions, karaoke, cards, openers,
thumbnails - and from article text, app decks and hand-written scripts. A rule
each of those has to remember is a rule one of them forgets. Every one of them
ends in `ImageDraw.text` (or a measure of the same string), so `install()`
wraps those few methods once and the whole engine inherits it.

**Measure and draw are patched together.** A layout that measured "a — b"
and then drew "a - b" would centre a string of the wrong width, so
`textbbox`, `textlength` and `multiline_textbbox` see the same text `text`
draws.

The narration is untouched: a spoken line may keep its dash for pacing,
since only the picture is under the rule. Final Cut titles (drone FCPXML)
are not drawn by Pillow and go through `plain()` directly.
"""

from __future__ import annotations

import re

from PIL import ImageDraw

# Em dash, en dash, figure dash, horizontal bar. Not the minus sign (U+2212),
# which is a different character doing a different job ("-3 dB").
LONG = "—–‒―"
_SPACED = re.compile(rf"\s*[{LONG}]\s*")
_RANGE = re.compile(rf"(\d)[{LONG}](\d)")


def plain(text):
    """`text` with every long dash as a spaced single hyphen.

    "a — b" and "house—you" both become "a - b" / "house - you": an unspaced
    em dash turned into a bare hyphen would read as a compound word. A dash
    that opens or closes the string loses the space on that side. Anything
    that is not a `str` is returned as it is.
    """
    if not isinstance(text, str) or not any(c in text for c in LONG):
        return text
    # A range between numbers stays tight: "2010–2020" is "2010-2020".
    out = _RANGE.sub(r"\1-\2", text)
    out = _SPACED.sub(" - ", out)
    if text[:1] in LONG:
        out = out.lstrip()
    if text[-1:] in LONG:
        out = out.rstrip()
    return out


_METHODS = ("text", "multiline_text", "textbbox", "textlength",
            "multiline_textbbox")
_installed = False


def install() -> None:
    """Route every Pillow draw and measure through `plain`. Idempotent."""
    global _installed
    if _installed:
        return
    for name in _METHODS:
        orig = getattr(ImageDraw.ImageDraw, name, None)
        if orig is None:
            continue

        if name == "textlength":
            # `textlength(text, font=None, ...)`: the text comes first.
            def wrapped(self, *a, _orig=orig, **kw):
                if a:
                    a = (plain(a[0]),) + a[1:]
                if "text" in kw:
                    kw["text"] = plain(kw["text"])
                return _orig(self, *a, **kw)
        else:
            # `text(xy, text, ...)` and the bbox measures: xy, then text.
            def wrapped(self, *a, _orig=orig, **kw):
                if len(a) >= 2:
                    a = (a[0], plain(a[1])) + a[2:]
                if "text" in kw:
                    kw["text"] = plain(kw["text"])
                return _orig(self, *a, **kw)

        wrapped.__name__ = name
        wrapped.__doc__ = orig.__doc__
        setattr(ImageDraw.ImageDraw, name, wrapped)
    _installed = True
