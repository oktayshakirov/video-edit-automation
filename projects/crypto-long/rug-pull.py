"""How to spot a crypto rug pull - long-form 16:9 for YouTube.

Source: crypto-wiki/content/posts/what-is-a-rug-pull.mdx.

**The angle.** The article is a full playbook - five rug-pull patterns, an
on-chain checklist, two case studies, a regulation section, a triage list for
victims. The video does not carry all of it. It walks the one idea a beginner
is missing: a brand-new token only has a price because the creators paired it
with real money in a pool, so whoever controls that pool controls whether the
price is real. Everything after that - the five shapes it takes, the decoy of a
locked pool, the four-question check - hangs off that one mechanism. Regulation,
recourse and the victim triage are left to the article.

The arc:

* **Hook** - you buy a new token, it jumps, then it is worth nothing and the
  team is gone. That is a rug pull, and most of them work the same way. Stay
  and you will be able to check any new token for it in about two minutes.
  2020, the summer anyone could launch a token - and so could any scammer.
* **Reframe** - a new token is not on a big exchange. It trades on a
  decentralized exchange against a pool of real money the creators put up. That
  pool *is* the price, and it is the only thing a holder can sell back into.
* **Deep dive** - the mechanism, from the scammer's side, as a `diagram`: seed
  a pool, market it hard, let buyers pour real money in, then pull the pool.
* **The shapes it takes** - a `grid` of the five patterns: liquidity pull, team
  dump, hidden backdoor, honeypot, slow bleed. Different speeds, same ending.
* **Twist** - a locked pool is not proof of safety. If the team kept most of
  the supply they never needed the pool; they just sell into every buyer. A
  `gauge` on supply concentration against a healthy spread.
* **Mirror / echo** - the four-question check as a `steps` routine, the rule
  restated (a rug pull is a design, and a design leaves fingerprints), the
  disclaimer on its own, and the closing question.

**No financial advice, anywhere.** No token is named, no price or direction is
given, no platform is rated, nothing is recommended to buy or sell. The
`diagram` draws the scam's own mechanism; the `gauge` draws a distribution, not
a prediction; the `steps` beat is a safety checklist that routes to the article
and to a block explorer, which is where the checks actually happen.

**Beat silhouettes, chosen before writing, no two alike, and deliberately off
the recipe the last three crypto long-forms all ran** (vitalik: compare / grid /
quote / stat / steps; perpetual: bars / checklist / compare / logos / stat;
quantum: checklist / compare / quote / stat / steps). This one drops `compare`,
`quote` and `checklist` entirely and leads on the two beats the channel has
barely touched: `diagram` (0 uses in the last six scripts) for the mechanism and
`gauge` (0 uses ever on this channel) for the supply distribution. Full set:
`stat` (2020), `diagram` (the four moves), `grid` (the five patterns), `gauge`
(supply concentration), `steps` (the four-question check).

**Grid carries no icons.** Five small emoji on five wide cards render as smudges
on the near-black ground; the label plus the note line is clear on its own. The
`diagram` and `steps` beats keep the handful of glyphs that read as icons at
node size - money bag, flame, rocket, warning triangle, padlock, bar chart,
crown - checked on a rendered frame, not in the editor.

**Assets are all fresh** - nothing here is shared with another crypto video. A
proper inventory of all nine crypto scripts was run first; every clip was
screened dark, contact-sheeted, and is unused on the channel. Anything
price-shaped is banned outright for this niche, so `rugpull.jpg` (a real
PancakeSwap screenshot) is out; `CHART` is a hand-drawn abstraction of the same
shape - a line steps up, then plunges to a flat zero - naming nothing tradeable.

**Two generated brand assets, both new here.** `assets/brand/graphics/
rug-pull-chart.png` is the chart above. `assets/brand/beat-ground-crypto.jpg`
is a warm near-black bloom passed as `Shot(backdrop=...)` to every drawn beat -
the user's note was that `crypto-blackwater` (the brand default) was the ground
under *every* graphic, so now the water is reserved for the chapter cards and
the beats sit on the gradient. `Beat.__init__` covers + blurs + dims a supplied
backdrop to 0.42, so the source is generated bright (~L45) to land ~L19 behind
type.

**Re-cut after the first review.** Replaced: a phone-over-rubble clip that read
as a war zone (-> `CHART`), two foreign-banknote clips (-> a US-dollar photo and
`CHART`), an Instagram-reels clip (-> `CHART` on the buy/sell line), the
over-used black water, and the thumbnail (a portrait that did not fit the topic
-> the site's own `hacker.jpg`).

**Phonemes, checked with espeak-ng.** "rug pull", "liquidity", "decentralized",
"blockchain", "honeypot", "explorer" all phonemize correctly as written. "DeFi"
returns "duh-FY" and "APY" returns "a-PY" - both are avoided; the script says
"the summer of twenty twenty" and "triple-digit yields" instead.

Run from the repo root:

    PYTHONPATH=. .venv/bin/python projects/crypto-long/rug-pull.py
"""

from pathlib import Path

from pathlib import Path as _P

from video_automation.core import music
from video_automation.core.brand import CRYPTO
from video_automation.core.stock import CACHE as STOCK
from video_automation.crypto.shots import SITE_IMAGES, Shot
from video_automation.longform import Meta, Section, render_long

POSTS = SITE_IMAGES / "posts"
V = STOCK / "videos"
PH = STOCK / "photos"
BRAND = _P(__file__).resolve().parents[2] / "assets/brand"

# --- fresh, screened dark, contact-sheeted, unused elsewhere on the channel -
FACE = V / "close-up-worried-man-face-dark-room/8458651.mp4"            # 19.2s L38-46 S9-11, man's face, low key
VANISH_CITY = V / "man-walking-city-night-alone/19223893.mp4"          # 12.8s L4-9 S5-10, lone figure walking away, night street
VANISH_HALL = V / "man-walking-dark-corridor-night-moody/35130880.mp4" # 21.5s L11-22 S11-18, figure down a dark corridor
CONTEMPLATE = V / "man-contemplating-window-night-city-dark/4538212.mp4"  # 16.3s L51-52 S9, man at a window, city lights, still
HOODED = V / "hooded-figure-computer-screen-dark/32829777.mp4"         # 21.5s L36-37 S11, hooded figure at a screen
DESK = V / "man-working-laptop-dark-office-night-alone/8311535.mp4"    # 23.7s L10-28 S5-12, man at a laptop alone, night office
COUNTDOWN = V / "digital-clock-countdown-timer-dark/35516561.mp4"      # 22.0s L0-1 S1, a digital countdown ticking
LOCK = V / "hands-locking-padlock-dark/10241357.mp4"                   # 20.7s L0-7 S0-3, a padlock closing, near black
LINKS = V / "metal-chain-links-macro-dark/3999356.mp4"               # 8.2s L31-33 S13-20, heavy chain links, macro
GEARS = V / "mechanical-gears-turning-macro-dark/3826844.mp4"         # 41.1s L9-42 S6-29, dark gears meshing (skip past the bright open)
RECORDS = V / "old-hard-drive-data-storage-dark/19285752.mp4"         # 24.9s L35-36 S14-15, a hard-drive platter, macro
THINK = V / "person-thinking-dark-room-serious/7698440.mp4"           # 28.1s L41-46 S11-15, person thinking, dark room
ROAD = V / "forked-road-aerial-night/31070839.mp4"                    # 18.0s L33 S8, a road forking, aerial, night
DUST = V / "golden-dust-particles-black-background/10296171.mp4"       # 27.6s L15-19 S9-10, slow gold specks on black - contemplative

# The site's `rugpull.jpg` is a real TradingView screenshot (PancakeSwap
# ticker, price axis) - banned outright for this niche. `CHART` is a
# hand-drawn abstraction of the same shape: a line steps up, then plunges
# straight to a flat zero. No ticker, no numbers, no broker; it names
# nothing tradeable, it just *is* the picture of a rug pull. Full frame.
CHART = BRAND / "graphics/rug-pull-chart.png"                         # 1920x1080, generated
# Behind the drawn beats only. The chapter cards keep `crypto-blackwater`
# (the brand default); the beats get this warm near-black bloom so the water
# is not the ground under every single graphic - the user's note.
BEATGROUND = BRAND / "beat-ground-crypto.jpg"                          # 2200x1400, generated, ~L45 -> x0.42 -> ~L19 behind type

DOLLARS = PH / "stack-of-cash-money-dark-moody/18921474.jpg"          # 6000x4000 L78 S8, three $100 bills on dark - US dollars

THUMB = POSTS / "hacker.jpg"                                          # 996x664 L38 S3, hooded figure with a laptop, grey studio

ENDCARD = V / "subscribe/4928934.mp4"

VOICE = "mia"
MUSIC = music.track("night-drift")
URL = "https://thecrypto.wiki/posts/what-is-a-rug-pull"
A = 16 / 9

# emoji as \U escapes so the source file stays ASCII-clean. Kept to the ones
# that read as icons on a near-black card at node size - bright, saturated,
# no ambiguous silhouette (the `grid` cards carry no icon at all: five small
# glyphs on wide cards read as smudges, and the label plus note is clear).
E_MONEY, E_FIRE, E_ROCKET, E_WARN = "\U0001F4B0", "\U0001F525", "\U0001F680", "\U000026A0"
E_LOCK, E_CHART, E_CROWN = "\U0001F512", "\U0001F4CA", "\U0001F451"


SECTIONS = [
    # --- hook. No card. Open on a moving face, name the subject line one. ---
    Section(
        title="The vanishing act",
        card=False,
        sentences=[
            ("You buy a new token.",
             "It jumps for a day."),
            ("Then the price falls to almost nothing,",
             "and the people who made it are gone."),
            ("That is a rug pull -",
             "and almost all of them work the exact same way."),
            ("Stay to the end,",
             "and you will be able to check any new token for this yourself,",
             "in about two minutes, before you ever buy."),
            ("By the summer of twenty twenty,",
             "anyone could launch a token in minutes -",
             "including the people setting out to rob you."),
        ],
        shots=[
            Shot(clip=FACE, clip_at=0.5),
            Shot(image=CHART, zoom=1.0, pan=(0.0, 0.0), aspect=A),
            Shot(clip=VANISH_CITY, clip_at=0.5),
            Shot(clip=DUST, clip_at=3.0,
                 payload=("", "How to Spot a Crypto Rug Pull")),
            Shot(graphic="stat", backdrop=BEATGROUND,
                 payload=("2020", "WHEN ANYONE COULD LAUNCH A TOKEN",
                          "Permissionless tokens and instant liquidity go mainstream",
                          False)),
        ],
        gaps=[0.55, 0.85, 0.70, 0.60, 0.85],
    ),

    # --- reframe: the pool is the price -----------------------------------
    Section(
        title="What actually holds the price up?",
        spoken_title="So what is actually holding the price up?",
        sentences=[
            ("A brand new token is not listed on a big exchange.",),
            ("It trades on a decentralized exchange,",
             "against a pool of real money the creators put up themselves."),
            ("That pool is the price.",),
            ("Buy, and you push the price up.",
             "Sell, and you pull it down."),
            ("And that same pool is the only thing you can ever sell back into.",),
            ("So if the people who created the token also control that pool -",
             "they can take the real money out,",
             "and leave you holding a token that no longer trades."),
        ],
        shots=[
            Shot(clip=THINK, clip_at=1.0),
            Shot(image=DOLLARS, zoom=1.12, pan=(0.02, 0.01), aspect=A, bias=0.5),
            None,                                    # hold the dollars
            Shot(image=CHART, zoom=1.06, pan=(0.03, 0.0), aspect=A),
            None,                                    # hold the chart
            Shot(clip=HOODED, clip_at=1.0),
        ],
        gaps=[0.55, 0.60, 0.90, 0.55, 0.70, 0.85],
    ),

    # --- deep dive: the mechanism, from the scammer's side ----------------
    Section(
        title="How the trick actually works",
        spoken_title="So here is the whole trick, in four moves.",
        sentences=[
            ("From the other side of the screen, a rug pull is just four moves.",),
            # the diagram's own sentence - exactly one caption chunk per node.
            ("First, they seed a pool - the token, paired with real money.",
             "Then they market it hard - hype, a countdown, a promise.",
             "Buyers pour their own money in, and the price climbs.",
             "Then they pull the pool, and the price is zero."),
            ("The whole thing can take an afternoon -",
             "and every step was planned before the token existed."),
        ],
        shots=[
            Shot(clip=DESK, clip_at=1.0),
            Shot(graphic="diagram", backdrop=BEATGROUND,
                 payload=([("A liquidity pool", "the token, paired with real money",
                            E_MONEY),
                           ("Marketing", "hype, a countdown, a promise", E_FIRE),
                           ("Buyers pile in", "the pool and the price climb",
                            E_ROCKET),
                           ("The pool is pulled", "the money leaves, the price is zero",
                            E_WARN)],
                          "THE FOUR MOVES", False)),
            Shot(clip=COUNTDOWN, clip_at=2.0),
        ],
        gaps=[0.70, 0.45, 0.85],
    ),

    # --- the shapes it takes: a grid of the five patterns ----------------
    Section(
        title="Is it always the liquidity?",
        spoken_title="So is it always the liquidity pool? Not quite.",
        sentences=[
            ("The liquidity pull is just the fastest version.",
             "There are five shapes worth knowing."),
            # the grid's own sentence - one caption chunk per card.
            ("The liquidity pull, where the pool vanishes within the hour.",
             "The team dump, where they keep most of the supply and sell it into you.",
             "The hidden backdoor, where the contract lets them mint or freeze at will.",
             "The honeypot, where you are allowed to buy, but the code will not let you sell.",
             "And the slow bleed, where a team just quietly cashes out for months."),
            ("Different speeds.",
             "Same ending."),
        ],
        shots=[
            Shot(clip=GEARS, clip_at=8.0),
            Shot(graphic="grid", backdrop=BEATGROUND,
                 payload=([("Liquidity pull", "the pool vanishes within the hour"),
                           ("Team dump", "they hold the supply and sell it into you"),
                           ("Hidden backdoor", "mint or freeze the token at will"),
                           ("Honeypot", "you can buy, but never sell"),
                           ("Slow bleed", "a quiet exit stretched over months")],
                          "FIVE SHAPES OF A RUG PULL")),
            Shot(clip=VANISH_HALL, clip_at=12.0),
        ],
        gaps=[0.60, 0.45, 0.85],
    ),

    # --- twist: a locked pool is not proof of safety --------------------
    Section(
        title="What if the pool is locked?",
        spoken_title="So what if the liquidity really is locked?",
        sentences=[
            ("Some of these scams really do lock the pool -",
             "sometimes for years,",
             "and the lock is completely real."),
            ("The money genuinely cannot be pulled.",),
            ("But then look at who holds the tokens.",),
            ("If the team kept most of the supply for themselves,",
             "they never needed the pool at all."),
            ("They just sell, in stages, into every buyer who shows up,",
             "until the chart is a staircase heading straight down."),
            # the gauge's own sentence - limit chunk first, value chunk second.
            ("A healthy launch keeps any handful of wallets well under a fifth "
             "of the whole supply.",
             "When the top few wallets are holding seventy or eighty percent, "
             "one decision ends it."),
        ],
        shots=[
            Shot(clip=LOCK, clip_at=1.0),
            Shot(clip=LINKS, clip_at=0.5),
            Shot(clip=RECORDS, clip_at=1.0),
            Shot(clip=GEARS, clip_at=20.0),
            None,                                    # hold the gears
            Shot(graphic="gauge", backdrop=BEATGROUND,
                 payload=("70-80%", 0.78, "top wallets hold most of the supply",
                          0.20, "a healthy spread sits about here",
                          "WHO HOLDS THE SUPPLY?")),
        ],
        gaps=[0.60, 0.70, 0.85, 0.60, 0.70, 0.45],
    ),

    # --- mirror, echo, the ask -----------------------------------------
    Section(
        title="So how do you check?",
        spoken_title="So how do you actually check one?",
        sentences=[
            ("You do not need to read code.",
             "You need a block explorer and four questions."),
            # the steps track - one caption chunk per node.
            ("Can the team still move the liquidity, or is it genuinely locked.",
             "Who holds the supply, and is it a few wallets or thousands.",
             "Can the owner still change the rules - mint, pause, or tax.",
             "And does the yield have a real source, or is it just paying you with "
             "new tokens."),
            ("If a token cannot pass those four,",
             "there is always another one that can."),
            ("Because a rug pull is not bad luck.",
             "It is a design -",
             "and a design leaves fingerprints."),
            ("Nothing in this video is financial advice.",),
            ("So the next time a new coin is climbing on your timeline -",
             "who do you think is actually holding the pool?"),
        ],
        shots=[
            Shot(clip=CONTEMPLATE, clip_at=1.0),
            Shot(graphic="steps", backdrop=BEATGROUND,
                 payload=([("Is the liquidity locked?", E_LOCK),
                           ("Who holds the supply?", E_CHART),
                           ("Can the owner rewrite it?", E_CROWN),
                           ("Where does the yield come from?", E_MONEY)],
                          "THE FOUR-QUESTION CHECK")),
            Shot(clip=ROAD, clip_at=1.0),
            Shot(clip=THINK, clip_at=2.0),
            Shot(clip=DUST, clip_at=14.0,
                 payload=("", "This is not financial advice.")),
            Shot(clip=VANISH_CITY, clip_at=1.0),
        ],
        gaps=[0.60, 0.45, 0.70, 0.85, 1.10, 2.30],
    ),
]

META = Meta(
    title="How to Spot a Crypto Rug Pull",
    hook="A new token jumps, then it is worth nothing and the team is gone. "
         "Here is the one mechanism behind almost every rug pull - and the "
         "two-minute check that catches them before you buy.",
    url=URL,
    summary="What a rug pull is, and how almost all of them work: a new token "
            "only has a price because the creators paired it with a pool of "
            "real money, so whoever controls that pool controls the price. The "
            "four moves of the scam, the five patterns it takes, why a locked "
            "pool is not proof of safety, and a four-question check you can run "
            "on a block explorer. Nothing here is financial advice.",
    tags=["rug pull", "what is a rug pull", "crypto rug pull explained",
          "how to spot a rug pull", "crypto scams", "defi scams",
          "liquidity pull", "honeypot token", "crypto for beginners",
          "crypto safety"],
    cta=f"The full breakdown - five rug-pull patterns, the on-chain checklist "
        f"and what to do if it happens to you: {URL}",
    credits=["Footage: Pexels (Pexels licence, no attribution required).",
             "Music: oosongoo, via Pixabay.",
             "Nothing in this video is financial advice."],
)


def main() -> None:
    out = Path.home() / "Desktop/crypto-rug-pull-long.mp4"
    work = Path.home() / "Desktop/.crypto-rug-pull-long-work"
    made = render_long(
        SECTIONS, out, work, brand=CRYPTO, meta=META, voice=VOICE,
        music=MUSIC,
        callouts=None,
        # Asks the video's own question, answers nothing. One-word accent for
        # the narrow landscape column; the Short brackets the two-word phrase.
        thumb_headline="How does a rug pull [work?]",
        thumb_image=THUMB,
        thumb_accent="yellow",
        # `hacker.jpg` is 996px, so the auto-scorer's zoom search would upscale
        # it soft. Pin the crop: the hooded figure sits centre-right, the grey
        # studio falls off dark to the left for the type.
        thumb_crop_at=(0.70, 0.32), thumb_side="left",
        endcard=ENDCARD, endcard_lead=7.0,
    )
    for k, v in made.items():
        print(f"{k}: {v}")


if __name__ == "__main__":
    main()
