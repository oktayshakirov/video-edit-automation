"""Draws `claim-site.png`: a made-up airdrop claim page, our own drawing, for
the laptop screen in `random-tokens-in-wallet` (`core/screenfill.py`). No real
site, brand or token. 1600x1000, a laptop panel's 16:10.

    PYTHONPATH=. .venv/bin/python assets/crypto/random-tokens/make_claim_site.py
"""
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw

from video_automation.longform.beats.base import _display, _font

W, H = 1600, 1000
OUT = Path(__file__).with_name("claim-site.png")


def main() -> Path:
    # A violet night gradient - the look these pages wear, not our gold.
    y = np.linspace(0, 1, H)[:, None]
    x = np.linspace(0, 1, W)[None, :]
    top, bot = np.array([46, 16, 92]), np.array([12, 6, 30])
    g = top * (1 - y)[..., None] + bot * y[..., None]
    glow = np.exp(-(((x - 0.5) / 0.35) ** 2 + ((y - 0.45) / 0.35) ** 2))
    g = g + glow[..., None] * np.array([70, 30, 110])
    im = Image.fromarray(np.clip(g, 0, 255).astype("uint8"))
    d = ImageDraw.Draw(im)
    green, ink = (60, 230, 140), (255, 255, 255)

    # Top bar: a made-up name and its own connect button.
    d.rectangle([0, 0, W, 110], fill=(14, 8, 34))
    d.ellipse([48, 30, 98, 80], fill=green)
    d.text((118, 55), "TOKEN DROP", font=_display(44), fill=ink, anchor="lm")
    d.rounded_rectangle([1250, 26, 1560, 86], radius=30, outline=green, width=4)
    d.text((1405, 56), "Connect wallet", font=_font(32), fill=green, anchor="mm")

    cx = W // 2
    d.text((cx, 230), "YOU ARE ELIGIBLE", font=_display(56), fill=green, anchor="mm")
    d.text((cx, 400), "5,000 TOKENS", font=_display(170), fill=ink, anchor="mm")
    d.text((cx, 545), "waiting in your wallet - claim them now",
           font=_font(48), fill=(205, 195, 235), anchor="mm")
    # The button the narration names.
    d.rounded_rectangle([cx - 520, 640, cx + 520, 790], radius=75, fill=green)
    d.text((cx, 715), "CONNECT WALLET TO CLAIM", font=_display(50),
           fill=(10, 30, 20), anchor="mm")
    d.text((cx, 880), "Offer ends in 14:59", font=_font(40),
           fill=(255, 120, 140), anchor="mm")
    im.save(OUT)
    return OUT


if __name__ == "__main__":
    print(main())
