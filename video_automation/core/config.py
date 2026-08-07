"""Constants shared by every project.

Only things that are genuinely common live here — proxy generation and the
clip index are not drone concerns, because crypto and tinnitus shorts also
need cheap proxies of stock footage before `pick_crop` can measure it.

Project-specific tuning stays in that project's own config (see
`video_automation/drone/config.py`), which re-exports these names so drone
code can keep importing everything from one place.
"""

VIDEO_EXTS = {".mp4", ".mov", ".m4v", ".mkv", ".avi"}

# --- proxy ---------------------------------------------------------------
PROXY_WIDTH = 320
PROXY_FPS = 10
PROXY_DIRNAME = ".analysis_cache"
DB_NAME = "clip_index.sqlite"
