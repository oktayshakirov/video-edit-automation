"""Build the round logo badges - see `video_automation/core/logos.py`.

    PYTHONPATH=. .venv/bin/python tools/oktai_logos.py
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from video_automation.core.logos import build  # noqa: E402

if __name__ == "__main__":
    for p in build():
        print(p)
