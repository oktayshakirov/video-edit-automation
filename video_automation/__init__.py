"""Video automation — one engine, three projects.

    core/       voices, TTS, caption alignment, type, crop, vertical render
    drone/      footage index, music-driven edits, FCPXML, narrated shorts
    crypto/     thecrypto.wiki article shorts            (stub)
    tinnitus/   tinnitushelp.me shorts and sound therapy (stub)
"""

__version__ = "0.2.0"

# No em or en dash is ever drawn in a video, only a single hyphen - the
# editor's standing rule. Installed here so every render inherits it without
# any script or beat having to remember (`core/dashes.py`).
from .core import dashes as _dashes  # noqa: E402

_dashes.install()
