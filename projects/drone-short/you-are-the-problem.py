"""You Are the Problem — stacked vertical quote, two Berlin sunset clips.

A sarcastic motivational line: it opens like every "everything happens for a
reason" card and then turns on the viewer. Sunset 6 (sun dropping behind
Grunewald, Teufelsberg a silhouette on the left) on top, Teufelsberg 2 (the
radar domes lit against the same sunset, drifting out of frame right) below.

The turn is "STUPID", so it takes the set-piece size on its own caption, in
caps at 80px rather than 88: the lowercase "p" descender at 88 hung past the
100px band, and caps leave room for the shake. The shake is the "triggered"
jolt, matched to the line's vibe (the user's ask for punchline words).
Ink karaoke (Iowan italic, the spoken word tinted), the user's call on this
cut over the box. No "i read a quote" opener and no quote marks: the line is
said straight, by the user's call.

Ungraded on purpose: the user wanted the footage as shot, not corrected.

Crops are hand-set: Sunset 6 is half black ground, so its box is tightened
and pulled up onto the sky with the sun inside; Teufelsberg 2 is a lateral
move to the right, so its box sits right to hold the domes as long as possible.
"""

from pathlib import Path

from video_automation.core.voiceover import render_narrated_stack, profile_args

SOURCE_POST = None                      # off-site: the user's own line, no article

FOOT = Path("~/Desktop/Drone Videos/Footage/Berlin 26 1:4").expanduser()
TOP = FOOT / "Sunset 6.mp4"
BOTTOM = FOOT / "Teufelsberg 2.mp4"
OUT = Path("~/Desktop/you-are-the-problem.mp4").expanduser()
WORK = Path("~/Desktop/.work-you-are-the-problem").expanduser()

# 1080x910 tile aspect, (x, y, w, h) in 4K source pixels
BOX_TOP = (1800, 60, 1768, 1490)        # sun at x~2650-2800; y pulled up off the black ground
BOX_BOTTOM = (1704, 360, 2136, 1800)    # domes at x~2460-3840 through ~8s

START_TOP, START_BOTTOM = 0.0, 0.0

GAP = [0.8, 1.1, 0.65]     # longest beat lands before the kicker
TAIL = 1.2

SENTENCES = [
    [("everything bad in your life", "everything bad in your life"),
     ("happens for a reason.", "happens for a reason.")],
    [("and the reason", "and the reason"),
     ("is that you are", "is that you are"),
     ("STUPID", "stupid,"),
     ("and make bad decisions.", "and make bad decisions.")],
    [("you are the problem.", "you are the problem.")],
]

BIG = "STUPID"


def main() -> None:
    WORK.mkdir(parents=True, exist_ok=True)
    out, total = render_narrated_stack(
        (TOP, START_TOP, BOX_TOP), (BOTTOM, START_BOTTOM, BOX_BOTTOM),
        OUT, SENTENCES, WORK,
        font_size=lambda c: 80 if c == BIG else 44,
        effect=lambda c: "shake" if c == BIG else None,
        gap=GAP, tail=TAIL, **profile_args("leo"))
    print(f"{out}  {total:.2f}s")


if __name__ == "__main__":
    main()
