"""Place-sound under footage (`core/ambience.py`), as an A/B. **Not a
publishable video.**

Six short shots: four places (city, rain, office, servers), a drawn beat that
must stay in clean air, and a room over the city. Renders the same cut twice:

* `ambience-A.mp4` - `ambience=False`
* `ambience-B.mp4` - the default

The shots here are short (~2.5s); `ambience.MIN_RUN` is 3s, so only the
places that hold long enough get a bed - which is the restraint working.

    PYTHONPATH=. .venv/bin/python projects/demo/ambience.py
"""

from pathlib import Path

from video_automation.core import music
from video_automation.core.brand import CRYPTO
from video_automation.core.stock import CACHE as STOCK
from video_automation.crypto.shots import Shot
from video_automation.longform import Section, render_long

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "projects/demo/out"
V = STOCK / "videos"


# --- the cut ----------------------------------------------------------------

SECTIONS = [
    Section(
        title="After dark", card=False,
        sentences=[
            ("At night the city never really goes quiet.",),
            ("Rain on the window turns it into a hiss.",),
            ("Somewhere, someone is still at their desk.",),
            ("And in a building nobody visits, the machines keep running.",),
            ("One point one million coins have never moved.",),
            ("Back home, the room finally settles.",),
        ],
        shots=[Shot(clip=V / "city-traffic-night-bus-street/16657010.mp4"),
               Shot(clip=V / "rain-on-window-at-night-dark/15161525.mp4"),
               Shot(clip=V / "businessman-working-late-night-office-moody-dark/5281602.mp4"),
               Shot(clip=V / "data-center-servers-rack-dark/3130182.mp4"),
               Shot(graphic="stat", payload=("1.1M", "coins", "never moved")),
               Shot(clip=V / "city-window-night-quiet-room/8591726.mp4", clip_at=4.0)],
    ),
]

def main():
    for name, amb in (("A", False), ("B", True)):
        made = render_long(SECTIONS, OUT / f"ambience-{name}.mp4",
                           OUT / f"ambience-{name}-work", brand=CRYPTO,
                           voice="mia", music=music.track("night-drift"),
                           callouts=None, special_cuts=False, ambience=amb)
        print(made["video"])


if __name__ == "__main__":
    main()
