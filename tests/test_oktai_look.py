"""The OktAI look from the editor's review of the third draft (2026-11-23):
footage in every card, a polished headline, yellow subtitles, marks with a
sound, our videos on a watch page, Claude Code at work, falling stars."""

import numpy as np
from PIL import Image

from video_automation.core.brand import OKTAI
from video_automation.core.frame import LANDSCAPE
from video_automation.crypto.shots import Shot


def test_a_headline_has_no_dust_and_no_chapter_sounds():
    from video_automation.core.filmfx import kind
    head = Shot(graphic="chapter", payload=("AI slop.", None, "headline", None, None))
    card = Shot(graphic="chapter", payload=("The music",))
    assert kind(head) == "beat" and kind(card) == "chapter"


def test_a_headline_keeps_its_style_and_takes_no_number():
    from video_automation.longform.plan import style_chapters
    head = Shot(graphic="chapter", payload=("AI slop.", None, "headline", None, None))
    card = Shot(graphic="chapter", payload=("The music",))
    style_chapters([head, card], "grid")
    assert head.payload[2] == "headline" and card.payload[3] == 1


def test_every_verdict_gets_its_sound():
    from video_automation.core import sfx
    wrong, right = sfx.verdict_wrong(), sfx.verdict_right()
    assert 0.3 < len(wrong) / sfx.SR < 1.2 and 0.5 < len(right) / sfx.SR < 1.5
    assert abs(np.max(np.abs(wrong)) - 1.0) < 1e-3
    assert "verdict_wrong" in sfx.LEVELS and "verdict_right" in sfx.LEVELS


def test_a_count_is_shown_as_pips():
    from video_automation.longform.beats import BEATS
    plain = BEATS["stat"]("3", "times", "I stopped one cut", brand=OKTAI,
                          frame=LANDSCAPE, start=0.0, hold=3.0, reveals=[0.2])
    pips = BEATS["stat"]("3", "times", "I stopped one cut", True, True, brand=OKTAI,
                         frame=LANDSCAPE, start=0.0, hold=3.0, reveals=[0.2])
    a = np.asarray(plain.draw(0.9).convert("RGB")).astype(int)
    b = np.asarray(pips.draw(0.9).convert("RGB")).astype(int)
    assert np.abs(a - b).sum() > 0


def test_one_logo_is_not_blown_up_to_fill_the_frame():
    from video_automation.core import logos
    from video_automation.longform.beats import BEATS
    im = BEATS["logos"]([(str(logos.path("claude")), "Claude Code")], "", brand=OKTAI,
                        frame=LANDSCAPE, start=0.0, hold=3.0, reveals=[0.0]).draw(0.9)
    a = np.asarray(im.convert("RGB")).astype(int)
    orange = (a[..., 0] > 180) & (a[..., 1] > 90) & (a[..., 1] < 150) & (a[..., 2] < 120)
    rows = np.where(orange.any(axis=1))[0]
    assert rows.size and rows.max() - rows.min() < 340


def test_our_video_sits_on_a_watch_page():
    from video_automation.core.window import WindowShot

    class Inner:
        def draw(self, f):
            return Image.new("RGB", (1920, 1080), (40, 80, 120))
    w = WindowShot(Inner(), ("youtube", "Why Was Ethereum Created?",
                             "Crypto Wiki  ·  22 views"), 0.0, 3.0, LANDSCAPE, OKTAI)
    im = np.asarray(w.draw(0.5).convert("RGB"))
    red = (im[..., 0] > 230) & (im[..., 1] < 40) & (im[..., 2] < 80)
    assert red.sum() > 200                       # the progress line


def test_a_claude_chat_is_terminal_steps():
    from video_automation.core import screenplay as sp
    steps = sp.claude_chat("make it feel alive", "I'll add a beat.",
                           [("Update(core/music.py)", "bpm=100")], done="Done.")
    kinds = [s["do"] for s in steps]
    # The welcome box is already up; the prompt is the one thing typed.
    assert kinds[:3] == ["out", "cmd", "think"] and kinds.count("out") == 4
    assert steps[1]["prompt"] == "> "


def test_a_falling_star_crosses_the_sky_and_is_gone():
    from video_automation.core.painted import OKTAI_NIGHT, Painted
    p = Painted("oktai-night", OKTAI_NIGHT)
    at = OKTAI_NIGHT.shooting[0][2]
    quiet = p.at(at - 0.5, 1920, 1080).astype(int)
    streak = p.at(at + 0.4, 1920, 1080).astype(int)
    # The stars twinkle and the grain flickers; only the streak adds a
    # bright run of pixels.
    later = p.at(at + 3.0, 1920, 1080).astype(int)
    box = (slice(0, 420), slice(1100, 1640))     # where its path runs
    lit = ((streak - quiet)[box].max(axis=2) > 25).sum()
    assert lit > 200 and lit > 4 * ((later - quiet)[box].max(axis=2) > 25).sum()


def test_long_form_subtitles_are_on_for_oktai():
    from video_automation.oktai.build import SUBTITLES
    assert SUBTITLES[0] > 240 and SUBTITLES[2] < 60      # yellow


def test_a_roadmap_can_number_its_tiles():
    """"#1", "#2"... over the tiles of a lineup that is an order (2026-11-24)."""
    from video_automation.longform.beats import BEATS
    img = Image.new("RGB", (64, 36), (40, 120, 200))
    import tempfile
    from pathlib import Path
    p = Path(tempfile.mkdtemp()) / "tile.png"
    img.save(p)
    kw = dict(brand=OKTAI, frame=LANDSCAPE, reveals=[0.0, 0.1, 0.2], start=0.0, hold=2.0)
    plain = np.asarray(BEATS["logos"]([(str(p), "A")] * 3, "T", **kw).draw(0.95))
    num = np.asarray(BEATS["logos"]([(str(p), "A")] * 3, "T", None, True, **kw).draw(0.95))
    # The numbers are gold, above the tiles: more brand-coloured pixels.
    gold = np.array(OKTAI.primary)
    def golden(a):
        return int((np.abs(a.astype(int) - gold).sum(axis=2) < 60).sum())
    assert golden(num) > golden(plain) + 200


def test_a_voice_footnote_waits_for_both_voices():
    from video_automation.longform.beats import BEATS
    rows = [("A", "a", None), ("B", "b", None)]
    kw = dict(brand=OKTAI, frame=LANDSCAPE, reveals=[0.0, 2.0], start=0.0, hold=4.0)
    one = BEATS["voice"](rows, "*Both are the same.", **kw)
    none = BEATS["voice"](rows, **kw)
    band = slice(int(1080 * 0.78), int(1080 * 0.86))
    a, b = np.asarray(one.draw(0.3))[band], np.asarray(none.draw(0.3))[band]
    assert np.abs(a.astype(int) - b.astype(int)).max() < 40      # not yet
    a, b = np.asarray(one.draw(0.9))[band], np.asarray(none.draw(0.9))[band]
    assert np.abs(a.astype(int) - b.astype(int)).max() > 60      # with the second


def test_a_rec_dot_sits_top_right():
    from video_automation.core.rec import RecShot

    class Flat:
        def draw(self, f):
            return Image.new("RGB", LANDSCAPE.size, (10, 10, 10))
    a = np.asarray(RecShot(Flat(), 2.0, LANDSCAPE).draw(0.5)).astype(int)
    red = (a[:, :, 0] > 180) & (a[:, :, 1] < 90)
    ys, xs = np.nonzero(red)
    assert len(xs) and xs.min() > LANDSCAPE.w * 0.8 and ys.max() < LANDSCAPE.h * 0.15


def test_a_shot_can_name_its_place_sound():
    """Data footage under a server room's name gets bit chirps when the
    script says so, and "" gets none (2026-11-24)."""
    from video_automation.core import ambience
    clip = "/x/data-center-servers-rack-dark/1.mp4"
    assert ambience.bed_for(Shot(clip=clip)) == "servers"
    assert ambience.bed_for(Shot(clip=clip, ambience="digital")) == "digital"
    assert ambience.bed_for(Shot(clip=clip, ambience="")) is None
    x = ambience.digital(48000 * 3)
    assert x.shape == (48000 * 3, 2) and np.abs(x).max() > 0


def test_a_bar_can_name_the_question_beside_its_quote():
    from video_automation.core.frame import VERTICAL
    from video_automation.longform.beats import BEATS
    rows = [(("“It was Hal Finney.”", "Who built digital money?"), 0.5, "7.1s")]
    for frame in (LANDSCAPE, VERTICAL):
        kw = dict(brand=OKTAI, frame=frame, reveals=[0.0], start=0.0, hold=2.0)
        a = np.asarray(BEATS["bars"](rows, "T", **kw).draw(0.9)).astype(int)
        b = np.asarray(BEATS["bars"]([(rows[0][0][0],) + rows[0][1:]], "T", **kw).draw(0.9)).astype(int)
        assert np.abs(a - b).max() > 60                     # the note is drawn


def test_the_coda_is_black_with_a_line_and_an_arrow():
    from video_automation.longform.overlay import Coda
    c = Coda(10.0, 12.5, "Free prompt for all 5 fixes", "in the description",
             frame=LANDSCAPE, brand=OKTAI)
    pic = Image.new("RGB", LANDSCAPE.size, (200, 200, 200))
    assert c.draw(pic, 9.0) is pic
    a = np.asarray(c.draw(pic, 11.0)).astype(int)
    assert (a.sum(axis=2) < 30).mean() > 0.9                  # black
    gold = np.abs(a - np.array(OKTAI.primary)).sum(axis=2) < 60
    assert gold[: LANDSCAPE.h // 2].sum() < gold.sum()        # the arrow is low
    assert c.cues() and c.cues()[0][1] == "reveal"


def test_a_page_mark_names_its_text():
    from video_automation.core import screenplay as sp
    st = sp.mark("content that is repetitive or mass-produced")
    assert st["do"] == "mark" and "repetitive or mass-produced" in st["code"]
