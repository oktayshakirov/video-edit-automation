"""Stand-in fonts for machines that are not the Mac the videos are built on.

Every face the engine draws with is a macOS system font, named by its
absolute path (`/System/Library/Fonts/...`). On Linux - a remote session checking
an engine change - none of those files exist, every `ImageFont.truetype` raises
`OSError: cannot open resource`, and 147 of the test suite's checks fail
before they test anything. They were never about the typeface: a beat that
lays out its rows, a reel that fills the frame, an overlay that leaves on
time.

`install()` wraps `ImageFont.truetype` so that **a font path that does not
exist** is answered by the nearest free face on the machine instead
(DejaVu / Liberation / Noto, then Pillow's bundled face). A path that exists
is passed through untouched, so on the Mac this is a no-op even when it is
installed.

**Never install this for a render that ships.** The stand-ins have other
metrics: lines wrap at other widths, DIN Condensed becomes a wider sans, and
the Apple emoji become Noto's. It is for checks that do not depend on the
face - `tests/conftest.py`. Nothing in the render path imports it.
"""

from __future__ import annotations

from pathlib import Path

from PIL import ImageFont

_ROOTS = ("/System/Library/Fonts/", "/Library/Fonts/")

_D = "/usr/share/fonts/truetype/dejavu/"
_L = "/usr/share/fonts/truetype/liberation/"

# Each macOS face -> free faces of the same weight and width class, nearest
# first. Matched on the file name, so `Supplemental/` and the bare directory
# both resolve.
STAND_INS: dict[str, tuple[str, ...]] = {
    "DIN Condensed Bold.ttf": (_L + "LiberationSansNarrow-Bold.ttf",
                               _D + "DejaVuSansCondensed-Bold.ttf",
                               _D + "DejaVuSans-Bold.ttf"),
    "Arial Black.ttf": (_L + "LiberationSans-Bold.ttf",
                        _D + "DejaVuSans-Bold.ttf"),
    "Futura.ttc": (_D + "DejaVuSans.ttf", _L + "LiberationSans-Regular.ttf"),
    "Avenir Next.ttc": (_D + "DejaVuSans-Bold.ttf",
                        _L + "LiberationSans-Bold.ttf"),
    "SFNS.ttf": (_D + "DejaVuSans.ttf", _L + "LiberationSans-Regular.ttf"),
    "SFNSRounded.ttf": (_D + "DejaVuSans.ttf",
                        _L + "LiberationSans-Regular.ttf"),
    "SFNSItalic.ttf": (_D + "DejaVuSans-Oblique.ttf",
                       _L + "LiberationSans-Italic.ttf",
                       _D + "DejaVuSans.ttf"),
    "SFNSMono.ttf": (_D + "DejaVuSansMono.ttf", _L + "LiberationMono-Regular.ttf"),
    "NewYork.ttf": (_D + "DejaVuSerif.ttf", _L + "LiberationSerif-Regular.ttf"),
    "Georgia.ttf": (_D + "DejaVuSerif.ttf", _L + "LiberationSerif-Regular.ttf"),
    "Iowan Old Style.ttc": (_L + "LiberationSerif-Italic.ttf",
                            _D + "DejaVuSerif.ttf"),
}
SANS = (_D + "DejaVuSans.ttf", _L + "LiberationSans-Regular.ttf")

# Apple Color Emoji is a bitmap font loaded at its 160px strike; Noto Color
# Emoji is too, but its only strike is 109. Asking it for 160 raises "invalid
# pixel size", so the size is replaced, not passed through. Callers render the
# glyph, crop to its ink and scale, so a smaller strike only costs sharpness.
EMOJI = "Apple Color Emoji.ttc"
EMOJI_STAND_IN = "/usr/share/fonts/truetype/noto/NotoColorEmoji.ttf"
EMOJI_STRIKE = 109

_real_truetype = ImageFont.truetype
_used: dict[str, str] = {}


def stand_in(path: str) -> str | None:
    """The free face that answers for a missing macOS `path`, or None."""
    name = Path(path).name
    if name == EMOJI:
        return EMOJI_STAND_IN if Path(EMOJI_STAND_IN).exists() else None
    for cand in STAND_INS.get(name, SANS):
        if Path(cand).exists():
            return cand
    return None


def _truetype(font=None, size=10.0, index=0, encoding="", *args, **kwargs):
    path = str(font) if isinstance(font, (str, Path)) else None
    if path is None or Path(path).exists() or not path.startswith(_ROOTS):
        return _real_truetype(font, size, index, encoding, *args, **kwargs)
    sub = stand_in(path)
    _used[path] = sub or "<pillow default>"
    if sub is None:
        return ImageFont.load_default(size)
    if Path(path).name == EMOJI:
        return _real_truetype(sub, EMOJI_STRIKE)
    # A .ttc index means nothing in a single-face .ttf.
    return _real_truetype(sub, size, 0, encoding, *args, **kwargs)


def install() -> None:
    """Answer missing macOS font paths with free stand-ins. Idempotent."""
    ImageFont.truetype = _truetype


def uninstall() -> None:
    ImageFont.truetype = _real_truetype


def substitutions() -> dict[str, str]:
    """Every missing path asked for since `install()`, and what answered it."""
    return dict(_used)
