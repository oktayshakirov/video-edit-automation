"""What are perpetual futures? — long-form 16:9 for YouTube.

Source: crypto-wiki/content/posts/what-are-perpetual-futures.mdx.

**The angle.** The article covers a lot: funding, mark price, leverage,
margin modes, hedging, tax notes. The video does not try to carry all of it —
it picks the one mechanism that makes a perpetual contract different from an
ordinary futures contract (no expiry, so something else has to pin the price
to reality) and walks it through to the practical danger that actually hurts
traders (leverage, not the funding fee itself). Hedging, tax and the step-by-
step trade blueprint are left to the article.

The arc:

* **Hook** — you can open a Bitcoin trade and never have to close it. No
  expiration date, ever. So what stops the price from drifting away from the
  real one? 2016, BitMEX, the first contract like this.
* **Reframe** — an ordinary futures contract settles on a date, and that date
  is what pulls the price back. Perpetuals removed it, so one thing does that
  job instead: the funding rate, paid trader to trader.
* **Deep dive** — how big the fee actually is (tiny on a quiet day, ten times
  higher when the market is hot), and the mark-price safeguard that keeps a
  brief wick from liquidating people on a fluke.
* **Twist** — the funding fee is not what wipes people out. Leverage is. The
  arithmetic of how much room a price has to move against you shrinks fast as
  leverage climbs — walked with a `bars` beat, never a level or a call.
* **Second twist** — the two margin modes as the practical mitigation, then
  the honest list of what can still go wrong beyond leverage (funding cost,
  wick risk, an outage, ADL) — all real, none hypothetical.
* **Mirror/echo** — no company and no court sets this price, a recalculated
  number does; where perpetuals actually trade, centralized and on-chain
  alike; back to the opening claim, reframed; the disclaimer stands alone.

**No financial advice, anywhere.** No price level, no direction, no platform
rated, no leverage recommended. The `bars` beat draws pure arithmetic (how
much a price has to move against a position at a given leverage), never a
prediction. The risks are named as mechanisms, with the article's own
disclaimer language behind them.

**First video built for this post**, so the asset roster is entirely fresh —
nothing here is shared with any other crypto video. Ten stock clips and one
stock photograph, screened dark before use exactly as the skill requires;
`stock-market-chart-screen-dark`, `trading-candlestick-chart-monitor` and
`wall-street-trading-floor-screens` all sat in the cache from earlier fetches
and all three were rejected on sight — every one is a real, legible price
chart or ticker, which this format bans outright for a leverage-and-derivatives
topic. Two more candidates were pulled and rejected once the actual footage
was looked at rather than the folder name: a "tightrope walker" query's
pendulum clip turned out to be jewellery, and a "scale balance" macro turned
out to be a camera lens ring — the site's own "a folder name is a search
query, not a description" warning, twice in one afternoon.

**Phonemes, checked with espeak.** `Binance` phonemizes to `baɪnˈæns` — bye-
NANCE, stress on the wrong syllable — and `Bynanse` returns the brand's own
`bˈaɪnæns`. The respell rides in the spoken half of the pair, same as every
other crypto script. `Bybit`, `Kraken`, `Hyperliquid`, `perpetual`, `leverage`,
`liquidation` and `collateral` all phonemize correctly as written and needed
no respell.

**Beat silhouettes, chosen before writing, no two alike:** `stat` (2016),
`bars` (how far the price can move against you, by leverage), `compare`
(isolated vs. cross margin, name_columns=True), `checklist` (four real risks,
flow=True since the narration states each one as a fact), `logos` (Binance,
Bybit, Kraken, Hyperliquid, grouped centralized vs. decentralized, no
per-tile marks — this is not a verdict, just where the contract actually
trades).

Run from the repo root:

    PYTHONPATH=. .venv/bin/python projects/crypto-long/perpetual-futures.py
"""

from pathlib import Path

from video_automation.core import music
from video_automation.core.brand import CRYPTO
from video_automation.core.stock import CACHE as STOCK
from video_automation.crypto.shots import SITE_IMAGES, Shot
from video_automation.longform import Meta, Section, render_long

# **Every asset below is fresh** — this is the first video built from this
# post, so nothing here is shared with any other crypto video.
V = STOCK / "videos"
BIZ = V / "businessman-working-late-night-office-moody-dark/5281602.mp4"          # 11.69s L30-31 S7-8, man on phone at laptop, night
TYPE1 = V / "man-hands-typing-keyboard-fast-dark-close-up/8212370.mp4"            # 12.16s L20-25 S10-12
TYPE2 = V / "businessman-working-late-night-office-moody-dark/34771078.mp4"       # 13.68s L21-24 S4-5, hands on laptop close up
TYPE3 = V / "man-hands-typing-keyboard-fast-dark-close-up/6963750.mp4"            # 11.60s L42 S22-23, hand reaching to keyboard
TIMER = V / "vintage-pocket-watch-ticking-macro-dark/30084890.mp4"                # 20.16s L18-32 S9-13, small alarm clock on black
GLOBE = V / "network-globe-connections-world-dark-gold/3129902.mp4"               # 30.00s L4-5 S5-6, gold-lit rotating world network
RISK = V / "tightrope-walker-balance-dark/10013469.mp4"                           # 16.20s L18 S14, performer balancing on a high wire
LEVER = V / "weight-lifting-barbell-gym-dark-dramatic/5320001.mp4"                # 24.44s L39-43 S4-5, barbell close-up, dark gym
WORRIED1 = V / "man-looking-at-phone-worried-dark/7280528.mp4"                    # 18.08s L42 S24, man head-in-hand looking at phone
WORRIED2 = V / "man-looking-at-phone-worried-dark/7699007.mp4"                    # 13.48s L36-39 S13, woman looking at phone at night
WATER = V / "calm-dark-water-ripple-slow-night/16392053.mp4"                      # 22.00s L29-37 S12, slow water droplet, quiet
LAPTOPCLOSE = V / "laptop-closing-screen-dark-night/7272375.mp4"                  # 19.60s L14-18 S8-10, hand at laptop, lamp-lit room
STARS = V / "night-sky-stars-twinkling-slow-dark/11533575.mp4"                    # 7.42s L30-39 S12-22, treeline against a starry sky
ALONE1 = V / "man-alone-dark-room-night-silhouette/6944065.mp4"                   # 20.72s L26-27 S22-24, man alone on the phone, dim bedroom
ALONE2 = V / "man-alone-dark-room-night-silhouette/34535504.mp4"                  # 8.38s L26-29 S18, silhouette at a window, arms crossed

PH = STOCK / "photos"
COINS = PH / "gold-coins-stack-dark-moody-macro/38724872.jpg"                     # L30 S18, a gold bitcoin standing on a pile of coins

ENDCARD = STOCK / "videos/subscribe/4928934.mp4"

VOICE = "mia"

MUSIC = music.track("night-drift")

URL = "https://thecrypto.wiki/posts/what-are-perpetual-futures"

A = 16 / 9


SECTIONS = [
    # --- the hook. No card. Open on motion, not a still. --------------------
    Section(
        title="The trade that never closes",
        card=False,
        sentences=[
            ("You can open a Bitcoin trade,",
             "and never have to close it."),
            ("No expiration date.",
             "Ever."),
            ("So what actually stops the price you are paying",
             "from drifting away from the real one?"),
            ("Stay to the end,",
             "and you will know exactly what pulls it back -",
             "and why the same mechanism",
             "can wipe out your account in seconds."),
            ("Twenty sixteen -",
             "the year the first contract like this went live,",
             "with no settlement date at all."),
        ],
        shots=[
            Shot(clip=BIZ, clip_at=0.5),
            Shot(clip=TYPE1, clip_at=0.5),
            Shot(clip=GLOBE, clip_at=1.0,
                 payload=("", "What Are Perpetual Futures?")),
            Shot(clip=TYPE2, clip_at=0.5),
            Shot(graphic="stat",
                 payload=("2016", "FIRST ONE WENT LIVE",
                          "A contract with no expiration date, ever", False)),
        ],
        gaps=[0.55, 0.90, 0.60, 0.60, 0.85],
    ),

    # --- reframe: what replaced the settlement date -------------------------
    Section(
        title="So what replaced the deadline?",
        sentences=[
            ("A normal futures contract has a deadline,",
             "and that deadline is what pulls the price back to reality."),
            ("Perpetuals removed it completely.",),
            ("So one thing has to do that job instead -",
             "a fee, paid directly between the two sides of the trade."),
            ("It is called the funding rate.",),
            ("Trade above the real price, and the buyers pay the sellers.",
             "Trade below it, and the sellers pay the buyers."),
        ],
        shots=[
            Shot(clip=ALONE1, clip_at=1.0),
            Shot(clip=TYPE3, clip_at=0.5),
            Shot(image=COINS, zoom=1.10, pan=(0.02, 0.01), aspect=A, bias=0.5),
            Shot(clip=TYPE1, clip_at=3.5),
            Shot(clip=GLOBE, clip_at=15.0,
                 payload=("", "Nothing forces it back - except one thing")),
        ],
        gaps=[0.70, 0.85, 0.60, 0.55, 0.85],
    ),

    # --- deep dive: how big the fee is, and the mark-price safeguard --------
    Section(
        title="So how big is that fee, really?",
        sentences=[
            ("On a quiet day it is tiny -",
             "a fraction of a percent, every eight hours."),
            ("In a heated market,",
             "it can spike ten times higher."),
            ("And it is paid trader to trader,",
             "not to the exchange."),
            ("Liquidations are not checked against the last trade though -",
             "they are checked against a mark price,",
             "an index built from several exchanges at once."),
            ("So a single ugly wick",
             "cannot wipe you out by accident."),
        ],
        shots=[
            Shot(clip=TIMER, clip_at=11.0,
                 payload=("", "Every eight hours, on most platforms")),
            Shot(clip=TYPE2, clip_at=5.0),
            Shot(clip=WORRIED2, clip_at=1.0),
            Shot(clip=BIZ, clip_at=3.0),
            Shot(clip=TYPE3, clip_at=3.0),
        ],
        gaps=[0.85, 0.60, 0.55, 0.75, 0.85],
    ),

    # --- the twist: leverage, not the fee, is what wipes people out ---------
    Section(
        title="So where is the actual danger?",
        sentences=[
            ("The funding fee is not what wipes people out.",
             "Leverage is."),
            ("With one thousand dollars of margin at five times leverage,",
             "you control five thousand dollars of exposure."),
            ("A two percent move in the real price",
             "becomes roughly a ten percent swing on your money."),
            ("Push that higher,",
             "and the room to be wrong shrinks fast."),
            # The beat's own sentence - one chunk per bar, nothing else.
            ("Five times leverage, and the price can move twenty percent against you.",
             "Twenty times, and that drops to five percent.",
             "One hundred times, and one percent is enough."),
            ("That is the whole trade-off.",
             "More leverage, less room to be wrong."),
        ],
        shots=[
            Shot(clip=RISK, clip_at=1.0,
                 payload=("", "Leverage multiplies every move, not just the profitable ones")),
            Shot(clip=LEVER, clip_at=1.0),
            Shot(clip=WORRIED1, clip_at=9.0),
            None,                                    # ride the worried shot
            Shot(graphic="bars",
                 payload=([("5x leverage", 1.0, "20%"),
                           ("20x leverage", 0.25, "5%"),
                           ("100x leverage", 0.05, "1%")],
                          "HOW FAR CAN THE PRICE MOVE AGAINST YOU?")),
            Shot(clip=ALONE2, clip_at=0.5),
        ],
        gaps=[0.60, 0.55, 0.60, 0.85, 1.80, 0.85],
    ),

    # --- second twist: the mitigation, and the honest risk list -------------
    Section(
        title="So what actually protects you?",
        sentences=[
            ("Two settings decide how contained the damage is.",),
            ("Isolated margin.",
             "Only that position's margin is at risk.",
             "One bad trade stays contained.",
             "The rest of your account is untouched.",
             "Cross margin.",
             "Draws on your whole balance.",
             "Useful for hedging several positions.",
             "One bad trade can drain everything."),
            ("There is also a backstop, if a position cannot close in time -",
             "but here is the honest list of what can still go wrong."),
            ("Prolonged funding, eating into your profits.",
             "A thin market, with a brief but violent wick.",
             "An exchange outage, at the worst possible moment.",
             "Auto deleveraging, if the insurance fund cannot cover it."),
            ("None of that is rare in theory.",
             "All four have happened, on real exchanges, in real crashes."),
        ],
        shots=[
            Shot(clip=WORRIED2, clip_at=4.5),
            Shot(graphic="compare",
                 payload=("Isolated margin",
                          ["Only that position's margin is at risk",
                           "One bad trade stays contained",
                           "The rest of your account is untouched"],
                          "Cross margin",
                          ["Draws on your whole balance",
                           "Useful for hedging several positions",
                           "One bad trade can drain everything"],
                          True)),
            None,                                    # hold the compare card
            Shot(graphic="checklist",
                 payload=([("Prolonged funding, eating into your profits", True),
                           ("A thin market, with a brief but violent wick", True),
                           ("An exchange outage, at the worst possible moment", True),
                           ("Auto deleveraging, if the insurance fund cannot cover it", True)],
                          "WHAT CAN STILL GO WRONG", True)),
            None,                                    # hold the checklist
        ],
        gaps=[0.60, 0.90, 0.60, 2.10, 0.85],
    ),

    # --- mirror, echo, the ask -----------------------------------------------
    Section(
        title="So who actually decides this price?",
        sentences=[
            ("Neither a company, nor a court decides where this price sits.",),
            ("A number, recalculated every few hours, does that instead.",),
            ("It trades day and night,",
             "on centralized platforms and on-chain ones alike."),
            (("Binance.", "Bynanse."),
             "Bybit.",
             "Kraken.",
             "Or fully on-chain, like Hyperliquid."),
            ("So back to that trade with no expiration date.",),
            ("It never closes on its own.",
             "But every few hours, it still has to prove it is honest."),
            ("Nothing in this video is financial advice.",),
            ("So next time you see a position with no expiration date -",
             "what do you think is quietly deciding when it is actually over?"),
        ],
        shots=[
            Shot(clip=WATER, clip_at=1.0),
            None,                                    # hold the water
            Shot(clip=LAPTOPCLOSE, clip_at=1.0),
            Shot(graphic="logos",
                 payload=(["binance", "bybit", "kraken", "hyperliquid"],
                          "WHERE PERPETUALS ACTUALLY TRADE",
                          [("CENTRALIZED", 3), ("DECENTRALIZED", 1)])),
            Shot(clip=ALONE1, clip_at=12.0),
            Shot(clip=LEVER, clip_at=1.0),
            Shot(clip=STARS, clip_at=0.3),
            Shot(clip=WATER, clip_at=12.0),           # second use, far from
                                                        # the first - STARS is
                                                        # too short to hold
                                                        # across this line too
        ],
        gaps=[0.60, 0.85, 0.60, 0.85, 0.60, 0.85, 1.10, 2.20],
    ),
]

META = Meta(
    title="What Are Perpetual Futures?",
    hook="You can open a Bitcoin trade and never have to close it. "
         "So what stops the price from drifting away from the real one?",
    url=URL,
    summary="How a perpetual futures contract stays pinned to the real price "
            "with no expiry date - the funding rate, the mark price safeguard, "
            "and why leverage, not the funding fee, is what actually wipes "
            "traders out.",
    tags=["what are perpetual futures", "perpetual futures explained",
          "funding rate crypto", "crypto leverage explained",
          "perpetual swap", "crypto derivatives", "crypto for beginners",
          "isolated vs cross margin"],
    cta=f"The full breakdown of funding rates, margin modes and liquidation risk: {URL}",
    credits=["Footage: Pexels (Pexels licence, no attribution required).",
             "Music: oosongoo, via Pixabay.",
             "Nothing in this video is financial advice."],
)


def main() -> None:
    out = Path.home() / "Desktop/perpetual-futures-long.mp4"
    work = Path.home() / "Desktop/.perpetual-futures-long-work"
    made = render_long(
        SECTIONS, out, work, brand=CRYPTO, meta=META, voice=VOICE,
        music=MUSIC,
        callouts=None,
        # "Never expires. Still [risky.]" clipped "EXPIRES" at the frame edge
        # on render and was simplified after review - see the regenerated
        # thumbnail note below; the video itself was not re-rendered for this.
        thumb_headline="What Are Perpetual [Futures]?",
        thumb_image=COINS,
        thumb_accent="yellow",
        endcard=ENDCARD, endcard_lead=7.0,
    )
    for k, v in made.items():
        print(f"{k}: {v}")


if __name__ == "__main__":
    main()
