"""Frame geometry — the shapes this repo renders into, and what covers them.

This was two module constants in `vertical.py`, which was right for as long as
1080x1920 was the only output. Long-form YouTube is 16:9, and the difference is
not just the numbers:

* **The safe area is about a different platform's chrome.** The vertical box
  (`230` / `1440`, clear of `x>860`) is the union of TikTok's, Reels' and
  Shorts' overlays — a right rail of buttons and a caption block along the
  bottom. A 16:9 player has neither. What it has is a control bar and a title
  gradient that appear on hover, top and bottom, and nothing at the sides.

* **The upscale ceiling is a property of the frame, not of the picture.** It is
  tempting to assume a landscape source drops into a landscape frame for free.
  It does not, and the reason is that the binding constraint is *width*, not
  height: the site libraries run to a median of 900px (crypto) and 750px
  (tinnitus), so reaching 1920 wide asks for 2.1x and 2.6x. At `MAX_UPSCALE =
  1.45` the photograph can only ever occupy about 68% of a 1920 frame and it
  floats in blur — the exact failure the vertical skill records for sources
  under 750px.

  What changes is **how big the frame is actually drawn**. A 9:16 short fills a
  phone's height, so its picture is displayed at very near 1:1 and 1.45 is an
  honest ceiling. A 16:9 video is a ~390px-wide card in the feed, or ~844px
  full-screen on the same phone — roughly half the linear resolution for the
  same source. So the ceiling can rise for landscape without the softness
  becoming visible, which is why it lives here per-frame instead of as one
  constant on `PhotoShot`.

**The landscape numbers are guesses** and are marked so. They come from reading
the player, not from measuring frames against a real upload, which is the only
thing that settles them. Check them on the first render that goes to YouTube —
same discipline as `drone/config.py`, where unvalidated values carry `GUESS`.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Frame:
    """One output shape, plus everything that is unsafe to draw into.

    `safe_top` / `safe_bottom` are absolute y in pixels; `safe_right` is the x
    beyond which platform UI sits. `caption_floor` and the logo defaults live
    here too, because both are derived from the safe box and both were
    previously hardcoded to the vertical case at their call sites.
    """

    name: str
    w: int
    h: int
    safe_top: int
    safe_bottom: int
    safe_right: int
    caption_floor: float          # lowest caption centre, as a fraction of h
    logo_at: tuple[int, int]
    logo_w: int
    max_upscale: float            # past this the blur stops covering for it

    @property
    def size(self) -> tuple[int, int]:
        return self.w, self.h

    @property
    def aspect(self) -> float:
        return self.w / self.h

    def check_top(self, y: float, what: str) -> None:
        """Raise rather than ship a mark under the platform's own chrome.

        `render_shots` has always validated the watermark this way. It is worth
        keeping loud: a logo covered by a UI band is invisible in review, where
        the frame is looked at on its own, and obvious in the app.
        """
        if y < self.safe_top:
            raise ValueError(
                f"{what} at y={y:.0f} is above {self.name} safe_top="
                f"{self.safe_top} — it would sit under the platform's UI")


# TikTok, Reels and Shorts, unioned. Measured against the real apps while
# building the tinnitus and crypto shorts; these are settled.
VERTICAL = Frame(
    name="vertical",
    w=1080, h=1920,
    safe_top=230, safe_bottom=1440, safe_right=860,
    caption_floor=0.80,
    logo_at=(58, 268), logo_w=300,
    max_upscale=1.45,             # settled on real frames while building the shorts
)

# YouTube 16:9. GUESS throughout — verify on the first real upload.
#
# The bottom reserve is the control bar and its gradient, which appear on hover
# and on every mobile tap; the top reserve is the title gradient. Neither is
# persistent, which is why they are smaller proportionally than the vertical
# box — but anything drawn there is intermittently covered, which is worse than
# consistently covered because it reads as a glitch.
#
# There is no right rail in a 16:9 player, so `safe_right` is the full width.
# The one exception is the **top-right corner of an embedded player**, which
# carries the YouTube wordmark and a share button: keep the top band clear over
# there, which the upper-left lockup does by construction.
#
# Not encoded here, and it matters for the outro: **end-screen elements live in
# the last 20 seconds** and are placed by hand on upload. Leave the final card
# uncluttered so they have somewhere to go.
LANDSCAPE = Frame(
    name="landscape",
    w=1920, h=1080,
    safe_top=40,                  # The title gradient is transient and the user
                                  # confirms nothing sits over the mark in a
                                  # 16:9 player. 120 was the first guess and it
                                  # pushed the watermark down into the pictures
                                  # and onto the beat kickers, which is a real
                                  # cost paid against a hypothetical one. Note
                                  # this has to clear `logo_at` *minus its
                                  # float* — the mark levitates 8px and the
                                  # guard checks the top of the travel.
    safe_bottom=950,              # GUESS — control bar + gradient
    safe_right=1920,              # no right rail in 16:9
    caption_floor=0.86,           # GUESS — clears safe_bottom by ~20px
    logo_at=(64, 62), logo_w=250,   # up from y=150, which collided with both
                                    # the full-frame photos and the beat kickers
    max_upscale=1.90,             # GUESS — see the module docstring; compared on
                                  # real frames at 1.45 / 1.90 / 2.15
)

FRAMES = {f.name: f for f in (VERTICAL, LANDSCAPE)}
