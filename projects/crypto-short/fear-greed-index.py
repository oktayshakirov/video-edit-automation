"""Is there really a number for crypto's mood? ~48s crypto short.

Source: crypto-wiki/content/posts/crypto-fear-and-greed-index-for-beginners.mdx
- the same post as the `fear-greed-index` long-form, written in the same pass.

**The single move.** The long form walks the six weighted inputs, the fear and
greed feedback loop and the Buffett line. The Short does the one thing every
chapter of that video is building toward: the score measures the crowd's
*mood*, never a signal to buy or sell - so a hundred does not mean buy and
zero does not mean sell. Then it stops.

**It opens by asking its own title question**, over thumbs moving on a phone,
with nothing else on screen for a viewer to go on.

## Re-cut, same diagnosis as the long form

The first cut leaned on mood footage - a celebration under string lights, a
hands-in-hair portrait, a studio portrait - under lines about *a number*.
Every clip passed screening and none of them showed the noun. The rule this
pair settled is in `footage.md`: **an abstract topic has to be drawn, and the
clips around it should be screens, hands and people in numbers rather than
portraits** - which also takes the casting question out of most slots instead
of trying to steer a brightness filter that does not steer.

So this cut leads on the new `dial` beat - the index's own 0-100 scale, in the
index's own five band colours - and every clip in it is a phone, a hand or a
carriage full of people.

**Three graphics, no shared silhouette.** `dial` (the scale, drawn with no
needle, because the line describes the instrument rather than a reading on
it), `grid` (the five zones, each carrying the exact emoji the site's own live
widget uses - `😱 😢 😐 🙂 😁`), and a `chapter` statement card to close.

**The site's own legend, over moving footage.** `ImageOverlay` lays the
`fear-greed-legend.png` crop - the site's five band names in its own colours -
as a thin panel over the panic/euphoria line. That is the portrait answer to a
graphic a landscape frame would give a whole shot to; see `shorts.md`.

**No financial-advice line** - the standing rule for every Short on this
channel; the paired long form carries the disclaimer, and this Short closes on
the instruction instead. No token, platform, price or direction is named.

**Assets.** Every clip is shared with the long form and used **once here**,
which is the "once there, once here" convention `footage.md` sets for a pair
built from one post.

Run from the repo root:

    PYTHONPATH=. .venv/bin/python projects/crypto-short/fear-greed-index.py
"""

from pathlib import Path
from pathlib import Path as _P

from video_automation.core import music
from video_automation.core.brand import CRYPTO
from video_automation.core.frame import VERTICAL
from video_automation.core.stock import CACHE as STOCK
from video_automation.crypto.build import render_crypto_short
from video_automation.crypto.shots import Shot
from video_automation.longform.overlay import ImageOverlay
from video_automation.longform.thumb import render_short_thumb

V = STOCK / "videos"
BRAND = _P(__file__).resolve().parents[2] / "assets/brand"

# Shared with the long form, once each - screens, hands, people in numbers.
DESK = V / "man-looking-at-laptop-screen-glow-dark/33874628.mp4"     # 17.8s L9-12 S10-14, someone at a desk with a phone, night
FACE2 = V / "man-checking-phone-anxious-dark-room/7280528.mp4"       # 18.1s L42 S24, a reaction to something on a phone
TYPING = V / "hands-typing-phone-dark-close-up-night/33942937.mp4"   # 15.4s L11-14 S4-5, thumbs on a phone, close
SCROLL = V / "man-scrolling-social-media-phone-dark/13358555.mp4"    # 14.5s L14 S5, a hand scrolling a feed
PHONE1 = V / "woman-looking-at-phone-reaction-dark/7986753.mp4"      # 20.6s L7-9 S1-2, two people reading one phone
TRAIN = V / "subway-train-passengers-phones-dark/36111567.mp4"       # 15.3s L18-21, a night train, lit windows, passengers

LEGEND = BRAND / "graphics/fear-greed-legend.png"                    # the site's own scale, cropped + 2x
BEATGROUND = BRAND / "beat-ground-crypto.jpg"
THUMB = BRAND / "graphics/fear-greed-dial-v.png"                     # the dial beat, rendered as a still

E_EXFEAR, E_FEAR, E_NEUTRAL, E_GREED, E_EXGREED = (
    "\U0001F631", "\U0001F622", "\U0001F610", "\U0001F642", "\U0001F601")

BANDS = [("Extreme fear", 0.25, "#f85032"), ("Fear", 0.50, "#ff7e5f"),
         ("Neutral", 0.55, "#f2c94c"), ("Greed", 0.75, "#a8ff78"),
         ("Extreme greed", 1.00, "#56ab2f")]

VOICE = "mia"
MUSIC = music.track("night-drift")

SENTENCES = [
    # The title question, over a hand and a lit phone.
    ("Is there really a number",
     "that measures crypto's mood?"),

    # The payoff lands in sentence two, plainly - no hedge. The dial draws
    # under it, so this line is both the answer and the graphic's own hinge.
    ("Yes - it is called the Fear and Greed Index,",
     "and it runs from zero to a hundred."),

    ("Zero means total panic.",
     "A hundred means pure euphoria - everyone convinced the good times "
     "will never end."),

    # Hinge, its own sentence and its own Shot.
    ("And in between, it breaks down into five zones.",),

    # The grid's own sentence - one caption chunk per card, in order.
    ("Extreme fear, down near zero.",
     "Fear.",
     "Neutral, right in the middle.",
     "Greed.",
     "And extreme greed, up near a hundred."),

    ("But here's the part almost nobody says out loud.",),

    # Full-screen statement - caps on the card, a sentence in the voice.
    (("IT MEASURES THE CROWD'S MOOD. NOT WHAT YOU SHOULD DO.",
      "It measures the crowd's mood. Not what you should do."),),

    ("A hundred does not mean buy.",
     "Zero does not mean sell.",
     "It just means everyone is feeling the same thing, at once."),

    # Cold close - the standing rule for this channel's shorts. No question.
    ("So next time it swings red or green -",
     "remember, it is reading a room, not handing you orders."),
]

SHOTS = [
    # Thumbs on a phone: the hand-and-phone clip is the better composition
    # and its screen is legibly a photo editor, which is the wrong noun under
    # the title question. See `footage.md`.
    Shot(clip=TYPING, clip_at=1.0),
    Shot(graphic="dial", backdrop=BEATGROUND,
         payload=(BANDS, None, "", "ZERO TO A HUNDRED")),
    Shot(clip=FACE2, clip_at=1.0),
    Shot(clip=SCROLL, clip_at=1.0),
    Shot(graphic="grid", backdrop=BEATGROUND,
         payload=([("Extreme fear", "near zero", E_EXFEAR),
                   ("Fear", "leaning fearful", E_FEAR),
                   ("Neutral", "right in the middle", E_NEUTRAL),
                   ("Greed", "leaning greedy", E_GREED),
                   ("Extreme greed", "near a hundred", E_EXGREED)],
                  "FIVE ZONES")),
    Shot(clip=DESK, clip_at=1.0),
    Shot(graphic="chapter",
         payload=("IT MEASURES THE CROWD'S MOOD. NOT WHAT YOU SHOULD DO.",)),
    # **`clip_ax=0.24`, because the subjects are not in the middle.** A 16:9
    # source keeps about 32% of its width in 9:16, and the centred default
    # took the empty wall beside them: the first render of this shot was a
    # black frame with a sliver of a face at the very edge. The pair sits at
    # ~0.23 of the source width, measured off a contact sheet with the crop
    # window drawn on it.
    Shot(clip=PHONE1, clip_at=1.0, clip_ax=0.24),
    Shot(clip=TRAIN, clip_at=1.0),
]

# 0.34 inside a thought, 0.55-0.90 at the end of one. The dial (index 1) and
# the grid (index 4) get room to finish drawing; the statement card takes 1.30.
GAPS = [0.70, 0.90, 0.70, 0.55, 1.10, 0.60, 1.30, 0.70, 0.34]


def main() -> None:
    out = Path.home() / "Desktop/crypto-fear-greed-index-short.mp4"
    work = Path.home() / "Desktop/.crypto-fear-greed-index-short-work"

    # The site's own legend, over the panic/euphoria shot. Absolute seconds,
    # set generously and checked against the render - see `shorts.md`.
    w = int(VERTICAL.w * 0.86)
    overlays = [ImageOverlay(LEGEND, 9.0, 16.5, frame=VERTICAL, scale=0.86,
                             at=((VERTICAL.w - w) // 2, 380))]

    out, total = render_crypto_short(SENTENCES, SHOTS, out, work,
                                     voice=VOICE, gap=GAPS,
                                     music=MUSIC, music_gain=0.85,
                                     overlays=overlays)

    # **The same headline as the long form, word for word.** This shipped
    # once as "your mood" and the user caught it: `thumbnails.md` asks a pair
    # built from one post to share its headline so a viewer who sees the
    # second one recognises it, and "your" against "crypto's" breaks that for
    # no gain - the video is about the market's mood, not the viewer's.
    head = "This number claims to know crypto's [mood]"
    vert = render_short_thumb(
        out.with_name(out.stem + "-thumb.jpg"), CRYPTO, head,
        image=THUMB, accent="yellow", band="bottom")
    print(f"{out}  {total:.2f}s")
    print(f"{vert}")


if __name__ == "__main__":
    main()
