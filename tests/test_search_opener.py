"""The Search opener types on the shared rhythm (`core/typewriter.py`)."""

from PIL import Image

from video_automation.core import typewriter
from video_automation.core.brand import CRYPTO
from video_automation.core.frame import VERTICAL
from video_automation.longform.openers import Search


def test_search_types_on_the_shared_schedule():
    q = "can tmj cause tinnitus"
    op = Search(q).build(VERTICAL, CRYPTO, [])
    assert op.times == typewriter.schedule(q, Search.TYPE_AT)
    keys = [c for c in op.cues() if c[1].startswith("key")]
    assert len(keys) == len(q.replace(" ", ""))
    assert op.land == op.times[-1]
    blank = Image.new("RGB", VERTICAL.size)
    for t in (0.0, 0.5, op.land, op.land + 0.6):
        assert op.draw(blank.copy(), t).size == VERTICAL.size
