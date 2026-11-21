"""The pieces added for a more visual edit (2026-11-21, the editor's notes on
the OktAI opener draft): painted backdrops without rings, the verdict mark,
round logo badges, 3D emblems, the bed stopping under a music example, and
the visual plan check."""

import numpy as np
import pytest
from PIL import Image

from video_automation.core.frame import LANDSCAPE


def test_a_painted_backdrop_has_no_rings_after_8_bit():
    """Across the glow, neighbouring rows differ by grain, never by a
    whole-level step that runs straight across the frame."""
    from video_automation.core.painted import PAINTED, Painted
    p = Painted("oktai-night", PAINTED["oktai-night"])
    a = p.at(1.0, 640, 360).astype(np.float32).mean(axis=2)
    col = a[:, 320]
    # A ringed gradient is flat runs with steps; grain makes it jitter.
    flat_runs = np.sum(np.abs(np.diff(col)) == 0) / len(col)
    assert flat_runs < 0.6
    assert p.at(1.0, 640, 360).shape == (360, 640, 3)


def test_backdrop_get_paints_oktai_and_tinnitus():
    from video_automation.core import backdrop
    from video_automation.core.painted import Painted
    assert isinstance(backdrop.get("oktai-night"), Painted)
    assert isinstance(backdrop.get("tinnitus-plum"), Painted)


def test_a_verdict_drains_a_wrong_picture_and_marks_it():
    from video_automation.core.verdict import VerdictShot
    base = Image.new("RGB", LANDSCAPE.size, (40, 160, 220))

    class Inner:
        def draw(self, f):
            return base.copy()

    v = VerdictShot(Inner(), ("wrong", "Says nothing"), 0, 4.0, LANDSCAPE, at=0.5)
    assert np.asarray(v.draw(0.2)).tolist() == np.asarray(base).tolist()   # clean first
    after = np.asarray(v.draw(0.95)).astype(int)
    assert after[..., 2].mean() < 150                     # the blue has drained
    with pytest.raises(ValueError):
        VerdictShot(Inner(), "maybe", 0, 4.0, LANDSCAPE)


def test_a_round_badge_is_shown_whole(tmp_path):
    from video_automation.longform.beats.wide import Logos
    im = Image.new("RGBA", (200, 200), (0, 0, 0, 0))
    from PIL import ImageDraw
    ImageDraw.Draw(im).ellipse([0, 0, 199, 199], fill=(255, 0, 0, 255))
    assert Logos._is_badge(im)
    assert not Logos._is_badge(Image.new("RGB", (320, 180), (1, 2, 3)))


def test_a_music_example_stops_the_bed(tmp_path):
    import soundfile as sf
    from video_automation.core import samples
    from video_automation.longform.audio import dip
    sf.write(tmp_path / "m.wav", np.sin(np.arange(48000) / 5) * 0.5, 48000)
    name = samples.register(tmp_path / "m.wav", "test-music", level=1.0, bed=0.0)
    w = samples.windows([(5.0, f"sample_{name}")])
    assert w[0][2] == 0.0 and w[0][0] < 4.0 - 0.5       # longer margin
    bed = tmp_path / "bed.wav"
    sf.write(bed, np.ones((48000 * 8, 2), np.float32) * 0.5, 48000)
    out = dip(bed, tmp_path / "out.wav", w)
    a, sr = sf.read(out)
    assert abs(a[int(4.5 * sr), 0]) < 1e-3                # silent under it
    assert abs(a[int(7.5 * sr), 0] - 0.5) < 1e-3          # back after


def test_each_video_gets_its_own_emblem_from_its_brand():
    from video_automation.core import emblem3d
    picks = {emblem3d.pick("crypto", f"video-{i}") for i in range(30)}
    assert picks <= set(emblem3d.SETS["crypto"]) and len(picks) > 1
    assert emblem3d.pick("crypto", "same") == emblem3d.pick("crypto", "same")
    assert emblem3d.use_for("oktai", "x", "microphone") == "microphone"
    assert emblem3d.pick("nobody", "x") is None


def test_a_beat_falls_back_to_arcs_without_blender(monkeypatch):
    from video_automation.core import emblem3d
    from video_automation.core.brand import OKTAI
    from video_automation.longform.beats import BEATS
    monkeypatch.setattr(emblem3d, "available", lambda: False)
    b = BEATS["stat"]("11", "Shorts", "pulled", brand=OKTAI, frame=LANDSCAPE,
                      reveals=[0.1], start=0, hold=3, emblem="chart")
    b.draw(0.5)                                            # draws the arcs


def test_the_visual_check_flags_a_run_of_text(tmp_path):
    import sys
    sys.path.insert(0, "tools")
    import visual_check as vc
    p = tmp_path / "plain.py"
    p.write_text(
        "from video_automation.crypto.shots import Shot\n"
        "from video_automation.longform import Section\n"
        "SECTIONS = [Section('Plain', card=False, sentences=[\n"
        "    ('One two three four five six seven eight nine ten eleven twelve.',),\n"
        "    ('One two three four five six seven eight nine ten eleven twelve.',),\n"
        "    ('One two three four five six seven eight nine ten eleven twelve.',)],\n"
        "    shots=[Shot(graphic='stat', payload=('1', 'a', 'b')),\n"
        "           Shot(graphic='quote', payload=('q', 'w')),\n"
        "           Shot(graphic='stat', payload=('2', 'a', 'b'))])]\n")
    flags = vc.check(p, show=False)
    assert any("text-only" in f for f in flags)
    assert any("no real example" in f for f in flags)
