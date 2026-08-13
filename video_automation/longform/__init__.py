"""Long-form 16:9 YouTube videos, shared by both sites.

The short formats live under `crypto/` and `tinnitus/` because each is that
site's own product. This one is deliberately not: the two long-form videos
differ by palette, watermark, voice and script, and by nothing structural. What
varies is passed in — a `Brand` and a `Frame` — rather than forked.

Entry point is `render_long`; see `docs/long-form-strategy.md` for why the
format is shaped the way it is.
"""

from .build import render_long
from .meta import Meta
from .plan import Section

__all__ = ["render_long", "Meta", "Section"]
