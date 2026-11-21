"""The tinnitus sound samples: synthesis, placement and the bed dip."""

import numpy as np
import soundfile as sf

from video_automation.core import samples, sfx
from video_automation.crypto.shots import Shot
from video_automation.longform import audio


def test_every_sample_is_soft_edged_and_sized():
    for name, dur in samples.DUR.items():
        x = sfx._MAKERS_EXTRA[f"sample_{name}"](samples.SR)
        assert len(x) == int(dur * samples.SR)
        # Nothing starts or ends as a transient.
        assert abs(x[0]) < 1e-3 and abs(x[-1]) < 1e-3


def test_a_sample_ends_before_the_next_caption():
    sh = Shot(graphic="spectrum", samples=(None, "ringing", "hissing"))
    sh.reveals = [10.0, 12.0, 15.0]
    out = samples.cues([sh], [10.0, 12.0, 15.0, 19.0], 30.0)
    # The floor plays nothing; each sound is cued on its end.
    assert out == [(15.0 - samples.LEAD, "sample_ringing"),
                   (19.0 - samples.LEAD, "sample_hissing")]
    assert sfx.ANCHOR["sample_ringing"] == samples.DUR["ringing"]


def test_the_bed_dips_under_a_sample(tmp_path):
    sr = 48000
    src = tmp_path / "bed.wav"
    sf.write(str(src), np.ones((sr * 4, 2), np.float32), sr)
    out = audio.dip(src, tmp_path / "dip.wav", [(1.5, 2.5)], gain=0.2)
    y, _ = sf.read(str(out))
    assert abs(y[int(2.0 * sr), 0] - 0.2) < 1e-3
    assert abs(y[int(0.5 * sr), 0] - 1.0) < 1e-3


def test_a_recorded_clip_plays_as_loud_as_the_voice(tmp_path):
    import numpy as np
    import soundfile as sf
    from video_automation.core import samples, sfx
    sr = 24000
    t = np.arange(int(1.5 * sr)) / sr
    sf.write(tmp_path / "v.wav", 0.3 * np.sin(2 * np.pi * 220 * t), sr)
    name = samples.register(tmp_path / "v.wav", "test-voice")
    key = f"sample_{name}"
    assert samples.DUR[name] == 1.5
    clip = samples.MAKERS[key](samples.SR)
    assert abs(np.max(np.abs(clip)) - 1.0) < 0.02          # peak-normalised
    assert abs(sfx.LEVELS[key] * sfx.DEFAULT_GAIN - 0.9) < 1e-9
    assert sfx.ANCHOR[key] == 1.5                           # cued on its end


def test_the_voice_beat_plays_its_row_while_its_clip_does(tmp_path):
    import numpy as np
    import soundfile as sf
    from video_automation.core import samples
    from video_automation.core.brand import OKTAI
    from video_automation.longform.beats import BEATS
    sf.write(tmp_path / "c.wav", np.sin(np.arange(48000) / 9), 48000)   # 1s
    name = samples.register(tmp_path / "c.wav", "test-row")
    beat = BEATS["voice"]([("AI", "a clip", name), ("Me", "the voice", None)],
                          brand=OKTAI, reveals=[0.0, 3.0], start=0.0, hold=6.0)
    a, b = beat._window(0)
    assert b == 3.0 - samples.LEAD and abs((b - a) - 1.0) < 1e-6
    assert beat._window(1) is None and beat._speaking(1, 4.0)
    beat.draw(0.4)                                           # renders
