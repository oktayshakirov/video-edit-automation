"""A camera's recording mark over a shot: a red dot that blinks and "REC"
in the top right (2026-11-24, the editor on the OktAI opener's script page:
"add red dot rec effect on the top right for effect").

    Shot(..., rec=True)

Over everything the shot draws, a window included, so it reads as the
camera recording the screen rather than part of the page.
"""

from __future__ import annotations

import math

from PIL import Image, ImageDraw, ImageFont

RED = (235, 52, 52)
FONT = "/System/Library/Fonts/Supplemental/DIN Condensed Bold.ttf"
BLINK = 1.0            # seconds per on-off cycle


class RecShot:
    def __init__(self, inner, hold: float, frame):
        self.inner, self.hold, self.frame = inner, hold, frame
        W, H = frame.size
        self.size = int(min(W, H) * 0.040)
        self.font = ImageFont.truetype(FONT, int(self.size * 1.25))

    def draw(self, f: float) -> Image.Image:
        pic = self.inner.draw(f)
        t = f * self.hold
        W, H = pic.size
        img = pic.convert("RGBA")
        d = ImageDraw.Draw(img)
        r = self.size / 2
        pad = int(min(W, H) * 0.045)
        tw = d.textlength("REC", font=self.font)
        x1 = W - pad
        cy = pad + r
        # In over the first 0.25 s; the dot pulses, the word stays.
        a = min(1.0, t / 0.25)
        on = 0.35 + 0.65 * (0.5 + 0.5 * math.cos(2 * math.pi * t / BLINK))
        d.text((x1, cy), "REC", font=self.font, anchor="rm",
               fill=(255, 255, 255, int(235 * a)))
        cx = x1 - tw - r * 1.6
        d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(*RED, int(255 * a * on)))
        return img.convert("RGB")
