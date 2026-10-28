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
