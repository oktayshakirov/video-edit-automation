"""Who controls Bitcoin's price? ~50s crypto short.

Source: crypto-wiki/content/posts/who-controls-bitcoins-price.mdx, the same post
as the `bitcoin-price-long` explainer.

**It narrows the long form's angle rather than repeating it.** That video walks
the whole mechanism - the fixed supply, the halving schedule, the whales, the
developers, the regulators, and what to watch instead - and needs four minutes
to earn its conclusion. Fifty seconds cannot walk a mechanism at all, so this
one does the single move the long form spends three chapters setting up: **a
whale can move the market and still cannot choose where it lands**, because
almost none of the supply is for sale and the book they are pushing into is
thin.

**It opens by asking its own title question**, which is the standing rule: a
Short arrives with no title card, no thumbnail on screen and no chapter list,
so a piece that opens on the first line of its argument reads as random. "Who
controls Bitcoin's price?" costs two seconds and turns the next fifty into an
answer somebody is waiting for.

**Three beats, three silhouettes, and none of them the pair the last crypto
short used.** That one ran `logos` then `steps`; this one runs `checklist`
(four options, two-phase, the verdicts landing in the pause), `grid` (two
cards, exchange flows) and `chapter` (the closing line full screen). The
channel-level rule is that a fourth video whose lists look like the first
three's is the templated sameness the strategy doc says gets a channel
suppressed, so the check is on the shape across videos, not within one.

**No financial advice.** The script describes a mechanism and never a
direction: it names no level, predicts nothing, rates no platform, and the one
thing it points the viewer at - how much bitcoin is sitting on exchanges - is
explained as what the flow means rather than as a signal to act on.

**The figures are structural, so the video cannot date.** "A thousand bitcoin
or more" is the article's own definition of a whale and "a hundred thousand
coins" is a hypothetical, not a claim about anybody's holdings. Nothing here is
a current on-chain number, which an evergreen Short has no way to correct.

**Vertical crop.** Every clip in the cut is either a screen filling the frame
or an unbroken surface - a chart, a phone, dark water, an abstract wave - so
none of them has an off-centre subject to lose in the ~32% of source width a
9:16 crop keeps. `clip_ax`/`clip_ay` are left at the default 0.5 deliberately
rather than by omission; this is the rare shot list where the contact-sheet
check finds nothing to move.

Run from the repo root:

    PYTHONPATH=. .venv/bin/python projects/crypto-short/bitcoin-price.py
"""

from pathlib import Path

from video_automation.core import music
from video_automation.core.brand import CRYPTO
from video_automation.core.stock import CACHE as STOCK
from video_automation.crypto.build import render_crypto_short
from video_automation.crypto.shots import SITE_IMAGES, Shot
from video_automation.longform.thumb import render_short_thumb, render_thumb

POSTS = SITE_IMAGES / "posts"

# Screened across their length, not at one second - the trailing comment is the
# luma/saturation range over the whole clip. OCEAN is this pair's own addition,
# fetched for the long form and the closest thing in the whole cache to the
# brand's near-black ground.
CHART = STOCK / "videos/stock-market-chart-screen-dark/38133087.mp4"   # L20 S19
BOOK = STOCK / "videos/stock-market-chart-screen-dark/38055931.mp4"    # L19 S21
PHONE = STOCK / "videos/smartphone-finance-app-dark/35518150.mp4"      # L34-45 S24-29
CANDLE = STOCK / "videos/trading-candlestick-chart-monitor/38471109.mp4"  # L15-16 S18
OCEAN = STOCK / "videos/deep-ocean-underwater-dark/5678004.mp4"        # L29-31 S1.5-2.0
WAVES = STOCK / "videos/abstract-dark-waves-motion/27980029.mp4"       # L2-4 S2-6

VOICE = "mia"                   # female, af_heart. Matches the long form from
                                # the same post. Still a candidate, not approved.

# Every short gets a bed from here on - the user's call. The same track the
# long form uses, which is the point of a channel having a small library.
MUSIC = music.track("night-drift")

# One tuple per sentence; each string is one caption. A drawn beat must have
# exactly one caption per item - that is what times its reveals.
SENTENCES = [
    # The title question, plainly, over motion. Not the first line of the
    # argument - a Short viewer has nothing on screen but this sentence.
    ("Who controls Bitcoin's price?",),

    ("Not who you think.",),

    ("A whale is one wallet",
     "holding a thousand bitcoin or more."),

    ("They can move the market in minutes.",),

    ("Because almost no bitcoin is for sale.",
     "Most of it has not moved in years."),

    ("So the order book is thin,",
     "and a thin book moves easily."),

    # The question goes here, not inside the beat: a beat times its reveals off
    # the caption starts of its own sentence, so a lead-in line inside that
    # span eats reveal zero and shunts every item one line late.
    ("So who actually sets the price?",),

    # The beat. Four options, no verdict in the voice - the marks *are* the
    # answer, which is why this is two-phase and takes the long gap below.
    ("The biggest whale?",
     "The developers?",
     "A regulator?",
     "Or the last person willing to sell?"),

    ("A whale cannot sell a hundred thousand coins",
     "at today's price.",
     "The moment they start,",
     "it stops being today's price."),

    # **The tip needs a reason before it is a tip.** It ties back to the beat
    # above rather than arriving as a new topic - the same note the last
    # short's three habits got.
    ("So stop watching whale wallets.",
     "Watch how much bitcoin sits on exchanges."),

    ("Coins moving on are getting ready to sell.",
     "Coins moving off are going to sleep."),

    # **The card needs a line handing off to it.** A full-screen statement that
    # arrives with nothing in front of it reads as a title card dropped into
    # the middle of the video.
    ("Remember what a price really is.",),

    # A full-screen statement. `build` suppresses captions on any shot with a
    # graphic, so the on-screen wording goes in the caption half of the pair
    # and the spoken wording in the other - the card can be in capitals while
    # the voice reads a sentence.
    (("THE LAST PERSON WILLING TO SELL SETS THE PRICE.",
      "The last person willing to sell sets the price."),),

    # **A hyphen, never an em or en dash.** At caption size a long rule reads
    # as a stray mark.
    ("So - who is selling tonight?",),
]

SHOTS = [
    # 1 - motion on frame one. A Short is judged in its first second.
    Shot(clip=CHART, clip_at=1.0),

    # 2 - a different clip rather than the same one running on, so the opening
    # pair reads as two shots and not six seconds of one.
    Shot(clip=PHONE, clip_at=0.5),

    # 3 - dark water under the whale line. **Not a literal whale**: every clip
    # the `whale swimming underwater` query returned is bright tropical blue
    # (L72-114, S75-177), and a literal whale under "crypto whale" is a pun the
    # script does not need anyway.
    Shot(clip=OCEAN, clip_at=2.0),

    # 4 - the first photograph, framed. The clip/card contrast is what makes
    # the alternation read as rhythm rather than as inconsistency.
    Shot(image=POSTS / "futuristic-crypto-exchange.jpg",
         zoom=1.11, pan=(0.02, 0.01), aspect=1.15, bias=0.40),

    # 5 - the gold lock on black, on the line about coins that never move. It
    # is the closest thing in the site library to on-palette.
    Shot(image=POSTS / "security-combination-lock.jpg",
         zoom=1.10, pan=(-0.02, 0.01), aspect=1.15, bias=0.45),

    Shot(clip=CANDLE, clip_at=1.0),

    Shot(image=POSTS / "analysis.jpg",
         zoom=1.11, pan=(0.02, -0.01), aspect=1.15, bias=0.45),

    # 8 - the beat: four options sitting unmarked while the voice reads them,
    # then three crosses and a tick landing one at a time in the pause.
    Shot(graphic="checklist",
         payload=([("The biggest whale", False),
                   ("The core developers", False),
                   ("A regulator", False),
                   ("The last person willing to sell", True)],
                  "WHO SETS THE PRICE?"),
         backdrop=POSTS / "laptop-trading.jpg"),

    Shot(clip=OCEAN, clip_at=9.0),

    Shot(image=POSTS / "portfolio.jpg",
         zoom=1.12, pan=(-0.02, 0.01), aspect=1.15, bias=0.45),

    # 11 - two cards down the frame. A `grid` rather than a second checklist:
    # these are two facts about a flow, not a judged list, and repeating the
    # checklist's silhouette ten seconds after using it is the sameness rule
    # arriving inside a single video.
    Shot(graphic="grid",
         payload=([("Coins moving on", "Getting ready to sell"),
                   ("Coins moving off", "Going to sleep")],
                  "WATCH THE EXCHANGES"),
         backdrop=POSTS / "global-map.jpg"),

    # 12 - the hand-off into the card.
    Shot(image=POSTS / "gold.jpg",
         zoom=1.11, pan=(0.02, -0.01), aspect=1.15, bias=0.50),

    # 13 - the line, full screen.
    Shot(graphic="chapter",
         payload=("THE LAST PERSON WILLING TO SELL SETS THE PRICE.",)),

    # 14 - the ask, on something uncluttered and moving again.
    Shot(clip=WAVES, clip_at=1.0),
]


# One or two per script, where they add something. More reads as decoration.
EMOJI = {
    "holding a thousand bitcoin or more.": "\U0001F40B",   # whale
    "So - who is selling tonight?": "\U0001F447",
}

# **Pauses are punctuation.** 0.34 inside a thought, 0.55-0.90 at the end of
# one, and the long gaps only where a beat needs room. The checklist (index 7)
# is two-phase and keeps the full 2.10: the four items sit unmarked, the voice
# stops, and the verdicts land in the silence. The `grid` (index 10) takes 0.90
# - a beat whose sentence is short is otherwise gone in under two seconds - and
# the statement card (index 12) takes 1.30, because a line that fills the
# screen has to be allowed to sit there.
GAPS = [0.75, 0.85, 0.60, 0.80, 0.70, 0.85, 0.90, 2.10, 0.75, 0.70,
        0.90, 0.70, 1.30, 0.34]


def main() -> None:
    out = Path.home() / "Desktop/bitcoin-price-short.mp4"
    work = Path.home() / "Desktop/.bitcoin-price-short-work"
    out, total = render_crypto_short(SENTENCES, SHOTS, out, work,
                                     voice=VOICE, emoji=EMOJI, gap=GAPS,
                                     music=MUSIC, music_gain=0.85)

    # **Two thumbnails, and the vertical one is not for YouTube.** The 1080x1920
    # is what Instagram and Facebook Reels use; YouTube takes the 1280x720 and
    # letterboxes anything else into it with a blurred zoomed copy either side,
    # which shipped once on the tinnitus channel and had to be replaced by hand.
    # Neither the upload nor the audit reports it - only looking does.
    #
    # **Same source and same headline as the long form from this post**, which
    # is the pairing rule: match a Short to its long form's thumbnail even
    # where the two videos cover different ground.
    # **The names are the convention `publish-video` reads, and they are not
    # arbitrary.** `-thumb.jpg` is the vertical Reel cover and `-thumb-yt.jpg`
    # is the 1280x720 YouTube one, matching `can-silence-make-tinnitus-worse`.
    # This script had them the other way round for one render, which is the
    # exact setup for uploading a 9:16 image to YouTube - the failure that
    # shipped on the silence pair, where YouTube letterboxed it between two
    # blurred zoomed copies and neither the upload nor the audit reported it.
    head = "Who controls [Bitcoin's price?]"
    vert = render_short_thumb(
        out.with_name(out.stem + "-thumb.jpg"), CRYPTO, head,
        image=POSTS / "analysis.jpg", accent="orange", band="bottom")
    wide = render_thumb(
        out.with_name(out.stem + "-thumb-yt.jpg"), CRYPTO, head,
        image=POSTS / "analysis.jpg", accent="orange")
    print(f"{out}  {total:.2f}s")
    print(f"{vert}")
    print(f"{wide}")


if __name__ == "__main__":
    main()
