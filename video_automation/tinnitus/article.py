"""Article shorts for tinnitushelp.me — the crypto short, with this brand.

**This is the format `video-tinnitus-short` recorded as "not built".** It is
built now, and it is deliberately not a second copy of anything: the two sites'
article shorts are structurally identical, so what was missing was never a
pipeline, it was the two values `render_crypto_short` had hard-coded — the
`Brand` its beats and clips are drawn with, and the watermark.

Both are arguments now, defaulted to crypto, so **the shipped crypto shorts are
byte-identical**: same brand, and `mark=None` still falls through to
`logo_mark()`, which is what they always used.

What this wrapper adds on top is the one thing that genuinely differs:

* **A watermark.** The crypto shorts carry the site logo `render_shots` builds
  by default. This site's mark is a lockup assembled at render time — the app's
  mascot with the domain under it — so it has to be passed in. It is the same
  `Brand.mark()` the long-form videos use, at the vertical frame's `logo_w`
  scaled by `mark_scale`, which exists precisely because a tall
  mascot-over-domain lockup at a wide wordmark's width dominates the frame.
* **`mia` as the default voice**, the reader the tinnitus long-form uses. A
  short and a long video on the same channel reading in two different voices is
  two channels. `luna-calm` is the sound-therapy voice and belongs to
  `asmr.py`; do not use it here. Both remain candidates.

**Use `grid`, `steps` or `bars` for a drawn beat, not `checklist`.**
`ChecklistShot` is the vertical-native beat and it is the one drawn object in
the stack that still carries thecrypto.wiki's gold as a module constant — it
would render an off-brand beat here and nothing would raise. The three beats
above all take the brand as an argument.

The medical rule from the skill applies unchanged and applies hardest in
short form, where there is no room to qualify anything: describe what a thing
*is*, never what it will do for the viewer, and never imply a cure.
"""

from __future__ import annotations

from pathlib import Path

from ..core.brand import TINNITUS, Brand
from ..core.frame import VERTICAL, Frame
from ..crypto.build import render_crypto_short
from ..crypto.shots import Shot


def render_tinnitus_short(sentences: list, shots: list[Shot], out: Path,
                          workdir: Path, voice: str = "mia",
                          brand: Brand = TINNITUS,
                          frame: Frame = VERTICAL,
                          **kw) -> tuple[Path, float]:
    """One tinnitus article short, end to end.

    Every other keyword — `gap`, `tail`, `font_size`, `y_frac`, `emoji`,
    `sound`, `fps`, `keep_work` — goes straight through to
    `render_crypto_short` and means exactly what it means there.
    """
    return render_crypto_short(
        sentences, shots, out, workdir, voice=voice, frame=frame,
        brand=brand,
        mark=brand.mark(int(frame.logo_w * brand.mark_scale)),
        **kw)
