"""Palette and watermark, per site.

`crypto/shots.py` has thecrypto.wiki's gold and its logo path as module
constants, which was right while it was the crypto format's own file. The
long-form engine is shared between two sites, so the things that differ between
them have to become a value the caller passes — the same move `Frame` makes for
geometry.

The two marks are genuinely different objects, not one object with two files.
thecrypto.wiki's logo already contains the domain, so it is used as-is.
tinnitushelp.me's is a lockup built at render time: the app's mascot with the
domain set underneath it, because the face alone carries no call to action and
the site prompts for the app install on arrival. `mark()` hides that difference
behind one call.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

from .vertical import FONT_CAPTION, FONT_CAPTION_INDEX

RGB = tuple[int, int, int]


@dataclass(frozen=True)
class Brand:
    """One site's look, and the watermark that says whose it is."""

    name: str
    site: str                     # the domain, as it should be read aloud
    primary: RGB                  # headings, rules, ticks — the site's own accent
    ink: RGB                      # body type
    bg: RGB                       # flat background, when there is no photograph
    panel: RGB
    negative: RGB                 # crosses and struck items
    grid: RGB                     # the drifting backdrop grid on a drawn beat
    logo: Path | None = None      # a mark that already carries the domain
    mascot: Path | None = None    # a face that does not, and needs the wordmark
    mascot_crop: float = 1.0      # fraction of the asset's height to keep
    wordmark: str | None = None
    mark_scale: float = 1.0       # against the frame's `logo_w`. A tall
                                  # mascot-over-domain lockup needs to be
                                  # narrower than a wide wordmark to take
                                  # up the same amount of frame.

    def mark(self, width: int) -> Image.Image | None:
        """The watermark, at `width` px, or None if its asset is missing.

        Full opacity in both cases. A watermark nobody can read is not a
        watermark, and the point of carrying the domain is that it is
        actionable — settled while building the tinnitus shorts.
        """
        if self.logo is not None and self.logo.exists():
            im = Image.open(self.logo).convert("RGBA")
            im = im.crop(im.getbbox())
            return im.resize((width, max(1, int(im.height * width / im.width))),
                             Image.LANCZOS)

        if self.mascot is None or not self.mascot.exists() or not self.wordmark:
            return None

        # The splash asset carries a faint wordmark under the face and the alpha
        # bounding box includes it, so the crop comes off the top of the asset
        # rather than straight from `getbbox`.
        im = Image.open(self.mascot).convert("RGBA")
        im = im.crop((0, 0, im.width, int(im.height * self.mascot_crop)))
        face = im.crop(im.getbbox())

        word_size = max(12, int(width * 0.135))
        font = ImageFont.truetype(FONT_CAPTION, word_size,
                                  index=FONT_CAPTION_INDEX)
        probe = ImageDraw.Draw(Image.new("RGBA", (8, 8)))
        tw = int(probe.textlength(self.wordmark, font=font))

        fh = max(1, int(face.height * width / face.width))
        face = face.resize((width, fh), Image.LANCZOS)
        gap = max(6, width // 20)

        w = max(width, tw) + 8
        out = Image.new("RGBA", (w, fh + gap + int(word_size * 1.3) + 2),
                        (0, 0, 0, 0))
        out.alpha_composite(face, ((w - width) // 2, 0))
        d = ImageDraw.Draw(out)
        y = fh + gap
        # A one-pixel dark offset rather than a stroke: at this size a stroke
        # closes up the counters.
        d.text(((w - tw) // 2 + 1, y + 1), self.wordmark, font=font,
               fill=(0, 0, 0, 140))
        d.text(((w - tw) // 2, y), self.wordmark, font=font,
               fill=(255, 255, 255, 255))
        return out


CRYPTO = Brand(
    name="crypto",
    site="thecrypto.wiki",
    primary=(229, 194, 0),        # #e5c200, from the site's config/theme.json
    ink=(255, 255, 255),
    bg=(23, 23, 23),              # #171717
    panel=(47, 47, 47),           # #2f2f2f
    negative=(196, 84, 84),
    grid=(40, 38, 26),
    logo=Path.home() / "Coding/crypto-wiki/public/images/logo.png",
)

TINNITUS = Brand(
    name="tinnitus",
    site="tinnitushelp.me",
    primary=(255, 218, 185),      # #ffdab9, the app highlight
    ink=(255, 255, 255),
    bg=(18, 10, 26),              # the void behind the nebula
    panel=(91, 57, 100),          # #5B3964, the app background
    negative=(232, 120, 120),     # a red that survives being on purple
    grid=(48, 34, 56),
    mascot=Path.home() / "Coding/tinnitus-app/assets/images/splash-icon.png",
    mascot_crop=0.82,
    wordmark="TinnitusHelp.me",
    mark_scale=0.62,
)

BRANDS = {b.name: b for b in (CRYPTO, TINNITUS)}
