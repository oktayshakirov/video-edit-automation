"""Fix a misread word in a finished long form without re-rendering it.

    PYTHONPATH=. .venv/bin/python tools/revoice.py projects/tinnitus-long/x.py \\
        "sentence as written" "sentence as it should be spoken"

Runs the script's own `main()` with `render_long` wrapped to re-speak that
sentence and keep the existing MP4's picture (`longform/revoice.py`). The
script's text must be unchanged since the render, or the narration cache
misses and the timeline moves; put the respelling into the script as a
`(caption, spoken)` pair *after* this has run, for the next full build.
"""

import functools
import importlib.util
import sys
from pathlib import Path


def main() -> None:
    script, said, spoken = sys.argv[1], sys.argv[2], sys.argv[3]
    spec = importlib.util.spec_from_file_location("revoiced", script)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    real = mod.render_long

    @functools.wraps(real)
    def wrapped(sections, out, workdir, *a, **kw):
        return real(sections, out, workdir, *a, revoice={said: spoken},
                    reuse_picture=Path(out), **kw)

    mod.render_long = wrapped
    mod.main()


if __name__ == "__main__":
    main()
