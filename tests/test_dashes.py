"""No long dash is ever drawn: `core/dashes.py`."""

from PIL import Image, ImageDraw, ImageFont

import video_automation  # noqa: F401  - installs the guard
from video_automation.core.dashes import plain


def test_plain_spaces_every_long_dash():
    assert plain("argument — you or your partner?") == \
        "argument - you or your partner?"
    assert plain("house—you") == "house - you"
    assert plain("2010–2020") == "2010-2020"
    assert plain("— opener") == "- opener"
    assert plain("no dash here") == "no dash here"
    assert plain("minus −3 dB") == "minus −3 dB"
    assert plain(None) is None


def test_draw_and_measure_see_the_same_plain_text():
    font = ImageFont.load_default()
    d = ImageDraw.Draw(Image.new("RGB", (400, 60)))
    assert d.textlength("a — b", font=font) == d.textlength("a - b", font=font)
    assert d.textbbox((0, 0), "a—b", font=font) == \
        d.textbbox((0, 0), "a - b", font=font)
    assert d.textbbox((0, 0), text="a—b", font=font) == \
        d.textbbox((0, 0), "a - b", font=font)


def test_drawn_pixels_match_the_hyphen_version():
    font = ImageFont.load_default()
    a = Image.new("L", (200, 30))
    b = Image.new("L", (200, 30))
    ImageDraw.Draw(a).text((4, 4), "x — y", font=font, fill=255)
    ImageDraw.Draw(b).text((4, 4), "x - y", font=font, fill=255)
    assert a.tobytes() == b.tobytes()
