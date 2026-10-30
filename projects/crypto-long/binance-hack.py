"""Binance hack explained - long-form 16:9 for YouTube.

Source: crypto-wiki/content/posts/how-does-north-korea-steal-crypto.mdx,
updated 2026-10-30 with the Binance theft. The second pair from this post;
the first (`north-korea-crypto`) told the Bybit heist.

**The angle.** A brand-new search term ("binance hack", E8) on a subject the
demand map already proves: the teardown found the standouts tell **one
heist as a sequence of moments**, and the failures summarise totals
(`demand/teardowns/how-does-north-korea-steal-crypto.md`). So this is the
29 October 2026 theft told start to finish: the size against the heists
before it, the way in, the evening itself, the freeze race, and what it
means for coins on an exchange. The close echoes the open: no key was
stolen; the wallet signed the door open.

**A named scheme, so the profile arc** (`projects/crypto.md`): "no private
key was stolen" is planted in the hook and paid off by the `sweep` beat,
which shows what was stolen instead - a signature.

**News, so every claim is someone's.** Same-day figures, and Binance has
not published a root cause. Attribution is TRM's and Chainalysis's, "with
high confidence" (TRM); the laptop is Binance's *preliminary* finding; the
signing-system break-in is TRM's *most likely* explanation, said as such.
No exchange is rated. "Binance says it will cover every loss" is its
statement; the next line is about reserves in general, not a judgement.

**Figures** (TRM Labs blog, 30 October 2026, onchain data as of 00:30 UTC;
Binance statements via CBS / Yahoo Finance, 30 October): ~$6.36B across ten
chains; drain from 20:05 UTC, most of it in ~20 minutes; on Ethereum at
20:20 UTC one transaction carrying 50 pre-signed authorizations delegated a
Binance hot wallet to a sweeper contract, emptied in ~3 min 24 s, then new
deposits swept at 20:41, 20:59, 21:04, 21:44, 22:39, 23:56; operator wallet
funded via Tornado Cash from 28 October, preparation 36+ hours. Frozen
~$2.7B by TRM's count (Tether ~1.77B USDT, Circle ~825M USDC, Ripple 40.5M
RLUSD, World Liberty 27.8M USD1, Arbitrum ~$30M); Binance says ~$3B. With
the attacker: 420,000+ ETH and 18,270 BTC; ~325M USDT sold for ETH at a
10%+ discount; the BTC split by a peel chain. Ronin $625M (2022), Bybit
$1.46B (Feb 2025), Bitget $387M (Sep 2026). Binance: no evidence of a
private-key leak; withdrawals suspended; losses covered by SAFU plus
company funds.

**Spoken around:** `Binance` phonemizes bye-NANCE, so the voice says
"Bynanse" (`projects/crypto.md`); `Bitget` reads BIT-git, so "Bit get".

## The beats

Last three crypto long forms: prediction-markets (shares / diagram / post /
checklist), north-korea-crypto (blindsign / timeline / post / grid / reel),
crypto-when-you-die (bars / reel / checklist / quorum / post). `post` has
run three times, so it sits this one out.

* `sweep` - **new, built for this video.** The hot wallet, the fifty
  authorizations handing it to the attackers' contract, the balance running
  out, then every new deposit swept straight through. The library could not
  draw a wallet whose own code works for someone else.
* `bars` - the four heists against each other: Binance is the proportion.
* `compare` - what could be frozen against what could not.

**Opener: `Counter`** on $6.36B. The last three long forms opened Counter /
Search / Search.

**Footage: the act, in the subject's world** - trading screens and order
books, phones with exchange apps, an engineer's laptop, a network switch
for the signing systems, a globe of connections for ten chains. All fetched
fresh (the first North Korea pair's roster is unavailable); verdicts in
`footage.md`. Binance's own card from the site is the real picture, as an
inset.

    PYTHONPATH=. .venv/bin/python projects/crypto-long/binance-hack.py
"""

import sys
from pathlib import Path
from pathlib import Path as _P

from video_automation.core import music
from video_automation.core.brand import CRYPTO
from video_automation.core.stock import CACHE as STOCK
from video_automation.crypto.shots import Shot

from video_automation.longform import Meta, Section, render_long
from video_automation.longform.openers import Counter

SOURCE_POST = "how-does-north-korea-steal-crypto"
DEMAND = ("New search term 'binance hack' (29 Oct 2026, E8); subject proven: "
          "Johnny Harris 'How North Korea Pulled off a Billion $$$ Heist' 2.9M, "
          "18.0x; Lume 'The Hacker Who Stole $1.5 Billion In 2 Minutes' 3.0x")

V = STOCK / "videos"
ROOT = _P(__file__).resolve().parents[2]
BRAND = ROOT / "assets/brand"
SITE = ROOT.parent / "crypto-wiki/public/images"

# Fetched fresh for this pair, contact-sheeted at 15/50/85%. Luma sampled at
# 0.5/3/6/9s.
TRADE = V / "trading-screens-dark-night/38736270.mp4"            # 25s, L11, line charts on a dark trading monitor - opens the cut
CANDLES = V / "trading-screens-dark-night/38440688.mp4"          # 25s, L29, candlesticks over an RGB keyboard
BOOK = V / "stock-ticker-screen-night/9421909.mp4"               # 27s, L28, an order book scrolling
TICKER = V / "stock-ticker-screen-night/7578632.mp4"             # 10s, L22, prices ticking red and green, close
BARS = V / "stock-ticker-screen-night/38222819.mp4"              # 18s, L18, red and green candle bars on a wall screen
CHARTROOM = V / "crypto-chart-monitor-dark-room/38440686.mp4"    # 11s, L37, chart monitors in a dark room
PHONEAPP = V / "cryptocurrency-app-phone-dark/39494572.mp4"      # 24s, L31, a hand holding a phone with a trading chart
HANDSAPP = V / "cryptocurrency-app-phone-dark/8480231.mp4"       # 11s, L48-54, two hands on a phone trading app over a laptop
PHONEMAN = V / "man-phone-night-city-dark/19538764.mp4"          # 18s, L25, a man in a beanie checking his phone at night
PHONEHANDS = V / "man-phone-night-city-dark/34796502.mp4"        # 28s, L34, a man at home with his phone, from the side
LAPTOP = V / "office-night-empty-monitors/34492303.mp4"          # 11s, L49, a man working at a laptop at home at night
TYPING = V / "computer-screen-code-dark-close-up/18382358.mp4"   # 16s, L38, hands on a laptop keyboard, code on the screen
KEYS = V / "keyboard-backlit-typing-close-up/9972272.mp4"        # 13s, L1-4, a backlit keyboard in the dark
GREEN = V / "cyber-security-analyst-screens/7534243.mp4"         # 14s, L31-35, a hand at a keyboard under green screens
GLOBE = V / "earth-from-space-night-lights/3125448.mp4"          # 20s, L35, a globe with network arcs - ten chains at once
EARTH = V / "earth-from-space-night-lights/20481076.mp4"         # 30s, L16-20, the Earth turning in space
SWITCH = V / "server-rack-blinking-lights-close-up/1085656.mp4"  # 24s, L52, a network switch's lights - the signing systems
ETH = V / "hardware-wallet-usb-crypto/10243082.mp4"              # 10s, L14-21, an Ether coin on black - "On Ethereum"
CANDLE = V / "candle-flame-dark/19726028.mp4"                    # 15s, L3, a candle on black - the disclaimer

BINANCE = SITE / "exchanges/binance.png"   # 900x506, the site's own Binance card, unused until now

BEATGROUND = BRAND / "beat-ground-crypto.jpg"
FLAG = ROOT / "assets/crypto/north-korea/dprk-flag.png"   # drawn in code, see its CREDITS.md
ENDCARD = V / "subscribe/4928934.mp4"

VOICE = "noah"
MUSIC = music.track("night-drift")
URL = "https://thecrypto.wiki/posts/how-does-north-korea-steal-crypto"

SWEEP = (("BINANCE HOT WALLET", "ETHEREUM"), ("ATTACKER CONTRACT", "SWEEPER"),
         "50 SIGNED AUTHORIZATIONS", "EMPTY IN 3 MIN 24 S",
         ["20:41", "20:59", "21:04", "21:44", "22:39", "23:56"],
         "ONE TRANSACTION")


def _b(s: str) -> tuple:
    """A line naming Binance: the caption spells it, the voice says
    "Bynanse" (espeak reads the brand bye-NANCE)."""
    return (s, s.replace("Binance", "Bynanse"))


SECTIONS = [
    # --- hook. No card. The Counter lands on "billion". ------------------------
    Section(
        title="Binance hack explained",
        card=False,
        sentences=[
            (_b("About six point three six billion dollars just left Binance."),),
            ("Most of it was gone in about twenty minutes.",),
            (_b("And Binance says no private key was stolen."),),
            ("So how did North Korea's hackers pull off the biggest crypto theft ever recorded?",),
            ("Stay to the end for the trap that kept running for hours,",
             "and what it means for coins you keep on an exchange."),
        ],
        shots=[
            Shot(clip=TRADE, clip_at=1.0),
            Shot(clip=KEYS, clip_at=1.0),
            Shot(clip=SWITCH, clip_at=1.0),
            Shot(clip=GREEN, clip_at=1.0),
            Shot(clip=PHONEMAN, clip_at=1.0),
        ],
        gaps=[0.70, 0.80, 0.90, 0.90, 0.90],
    ),

    # --- who ------------------------------------------------------------------
    Section(
        title="Who did it?",
        spoken_title="So who actually did it?",
        kicker="THE THIEVES",
        sentences=[
            ("Investigators at TRM Labs and Chainalysis point to one group,",
             "a North Korean hacking unit known as TraderTraitor."),
            ("The FBI named the same unit for the Bybit theft in February 2025.",),
            ("And the size of the thefts has jumped.",),
            # the bars' own sentence: one chunk per bar.
            ("The Ronin bridge in 2022, six hundred and twenty-five million dollars.",
             "Bybit, one point four six billion.",
             ("Bitget last month, three hundred and eighty-seven million.",
              "Bit get last month, three hundred and eighty-seven million."),
             _b("And Binance, about six point three six billion.")),
            ("About four times the record it replaced.",),
        ],
        shots=[
            Shot(clip=GLOBE, clip_at=1.0),
            Shot(clip=CHARTROOM, clip_at=1.0),
            Shot(clip=BOOK, clip_at=2.0),
            Shot(graphic="bars", backdrop=BEATGROUND,
                 payload=([("Ronin bridge, 2022", 0.098, "$625M"),
                           ("Bybit, Feb 2025", 0.230, "$1.46B"),
                           ("Bitget, Sep 2026", 0.061, "$387M"),
                           ("Binance, Oct 2026", 1.0, "$6.36B")],
                          "THE BIGGEST THEFTS")),
            Shot(clip=EARTH, clip_at=2.0),
        ],
        gaps=[0.70, 0.60, 0.45, 1.30, 0.90],
    ),

    # --- the way in -------------------------------------------------------------
    Section(
        title="How did they get in?",
        spoken_title="So how did they get in?",
        kicker="THE WAY IN",
        sentences=[
            (_b("Binance has not published a full account yet."),),
            ("Its first finding points to one engineer's compromised laptop.",),
            ("TRM goes further.",
             _b("Its most likely explanation is a break-in to the systems that sign Binance's hot-wallet transactions.")),
            ("Either way, this was planned.",),
            ("The attackers' wallet was funded through the mixer Tornado Cash the day before,",
             "and the setup ran for at least thirty-six hours."),
        ],
        shots=[
            Shot(clip=BARS, clip_at=1.0),
            Shot(clip=LAPTOP, clip_at=0.5),
            Shot(clip=SWITCH, clip_at=9.0),
            Shot(clip=TYPING, clip_at=1.0),
            Shot(clip=GREEN, clip_at=4.0,
                 note=("36 hours", "of preparation, at least")),
        ],
        gaps=[0.55, 0.70, 0.80, 0.45, 0.90],
    ),

    # --- the heist ------------------------------------------------------------
    # The turning point, so the card gets the longer silence.
    Section(
        title="What happened that evening?",
        spoken_title="So what actually happened that evening?",
        kicker="THE HEIST",
        card_gap=1.30,
        sentences=[
            (_b("At five past eight in the evening, universal time, money started leaving Binance on ten blockchains at once."),),
            ("On Ethereum, it took a single transaction.",),
            ("A recent Ethereum upgrade lets an ordinary wallet run a smart contract's code,",
             "as long as the wallet has signed for it."),
            # the sweep's own sentence: the wallet, the hand-over, the drain,
            # the deposits.
            (_b("At twenty past eight, one transaction reached Binance's hot wallet."),
             "It carried fifty signed authorizations, and pointed the wallet at the attackers' contract.",
             "About three and a half minutes later, the wallet was empty.",
             "And for hours after, every new deposit was swept straight out."),
            ("Why fifty?",
             "Each was signed for a different place in the wallet's queue, so one was bound to fit."),
            (_b("Binance suspended withdrawals across the exchange."),),
        ],
        shots=[
            Shot(clip=GLOBE, clip_at=9.0,
                 note=("20:05 UTC", "29 October 2026, the drain begins")),
            Shot(clip=ETH, clip_at=1.0),
            Shot(clip=CANDLES, clip_at=2.0),
            Shot(graphic="sweep", backdrop=BEATGROUND, payload=SWEEP),
            Shot(clip=TICKER, clip_at=1.0),
            Shot(clip=PHONEMAN, clip_at=9.0, inset=(BINANCE, "tr", 0.14)),
        ],
        gaps=[0.70, 0.55, 0.70, 2.00, 0.80, 0.90],
    ),

    # --- the freeze -------------------------------------------------------------
    Section(
        title="Can stolen crypto be frozen?",
        spoken_title="So can any of it be frozen?",
        kicker="THE FREEZE",
        sentences=[
            ("Some of it.",
             "Stablecoins can be frozen by the companies that issue them. Ether and Bitcoin cannot."),
            # the compare's own sentence: a heading chunk, three items, twice.
            ("Here is what could be frozen.",
             "Tether, about one point seven seven billion.",
             "Circle, about eight hundred and twenty-five million.",
             "Ripple, World Liberty and Arbitrum, about a hundred million more.",
             "And here is what could not.",
             "More than four hundred and twenty thousand Ether.",
             "Eighteen thousand two hundred and seventy Bitcoin.",
             "And three hundred and twenty-five million in Tether, dumped for Ether at a ten percent loss before it could be frozen."),
            ("By TRM's count, about two point seven billion dollars was frozen within hours,",
             _b("and Binance puts it nearer three.")),
            ("The rest is still moving.",
             "The Bitcoin is being split into smaller and smaller pieces."),
        ],
        shots=[
            Shot(clip=BOOK, clip_at=14.0),
            Shot(graphic="compare", backdrop=BEATGROUND,
                 payload=("COULD BE FROZEN",
                          ["Tether: $1.77B", "Circle: $825M", "Others: ~$100M"],
                          "COULD NOT",
                          ["420,000+ ETH", "18,270 BTC", "$325M swapped out"],
                          True)),
            Shot(clip=CHARTROOM, clip_at=2.5,
                 note=("$2.7B", "frozen within hours, by TRM's count")),
            Shot(clip=EARTH, clip_at=14.0),
        ],
        gaps=[0.70, 1.30, 0.80, 0.90],
    ),

    # --- you --------------------------------------------------------------------
    Section(
        title="What does it mean for you?",
        spoken_title="So what does this mean for you?",
        kicker="YOUR COINS",
        sentences=[
            (_b("Binance says it will cover every loss, from its emergency user fund and its own money."),),
            ("That promise is only as good as the reserves behind it.",),
            ("Coins on a centralized exchange sit in wallets that the exchange signs for.",),
            ("Coins in a wallet you hold yourself are signed for by you,",
             "and no exchange breach can reach them."),
            ("Neither is free of risk.",
             "One trusts a company's systems. The other trusts your own care."),
        ],
        shots=[
            Shot(clip=PHONEAPP, clip_at=2.0),
            Shot(clip=BARS, clip_at=10.0),
            Shot(clip=HANDSAPP, clip_at=1.0),
            Shot(clip=PHONEHANDS, clip_at=4.0),
            Shot(clip=KEYS, clip_at=7.0),
        ],
        gaps=[0.60, 0.70, 0.55, 0.70, 0.90],
    ),

    # --- close: the echo ------------------------------------------------------
    Section(
        title="So how did North Korea rob Binance?",
        spoken_title="So, how did North Korea rob Bynanse?",
        kicker="THE ANSWER",
        sentences=[
            ("Not by stealing a key.",
             _b("By getting Binance's own wallet to sign the door open, and leaving it open.")),
            ("Nothing in this video is financial advice.",),
            ("So, do you know everything your own wallet has already signed?",),
        ],
        shots=[
            Shot(clip=TRADE, clip_at=14.0),
            Shot(clip=CANDLE, clip_at=2.0,
                 payload=("", "This is not financial advice.")),
            Shot(clip=TYPING, clip_at=9.0),
        ],
        gaps=[0.90, 1.10, 2.30],
    ),
]

META = Meta(
    title="Binance Hack Explained: How North Korea Stole $6.36 Billion",
    hook="On 29 October 2026 about $6.36 billion left Binance, most of it in "
         "twenty minutes, and Binance says no private key was stolen. Here is "
         "how the biggest crypto theft on record worked, from one transaction "
         "carrying fifty signed authorizations to a wallet that kept sweeping "
         "deposits for hours, how much could be frozen, and what it means for "
         "coins you keep on an exchange.",
    url=URL,
    summary="The Binance hack of 29 October 2026, explained: about $6.36 billion "
            "taken across ten blockchains, most of it within twenty minutes; "
            "TRM Labs and Chainalysis attributing it to North Korea's "
            "TraderTraitor unit, the group the FBI named for the Bybit theft; "
            "how it compares with Ronin, Bybit and Bitget; Binance's "
            "preliminary finding of a compromised engineer's laptop and TRM's "
            "assessment of a break-in to the hot-wallet signing systems; how "
            "one Ethereum transaction carrying fifty pre-signed authorizations "
            "handed a Binance hot wallet to an attacker's contract, emptied it "
            "in about three and a half minutes and kept sweeping new deposits "
            "for hours; why stablecoins could be frozen and Ether and Bitcoin "
            "could not, with about $2.7 billion frozen by TRM's count; and what "
            "it means for coins kept on an exchange. Figures are preliminary, "
            "as of 30 October 2026. Nothing here is financial advice.",
    tags=["binance hack", "binance hack explained", "binance hacked",
          "north korea binance", "north korea crypto hack",
          "how does north korea steal crypto", "tradertraitor",
          "lazarus group", "biggest crypto hack", "crypto hack explained",
          "binance withdrawals suspended", "crypto security"],
    cta=f"Every heist, every source and how the stolen crypto gets laundered: {URL}",
    credits=["Figures: TRM Labs and Binance statements, 30 October 2026 "
             "(preliminary; Binance has not published a root cause).",
             "Nothing in this video is financial advice."],
)

HEADLINE = "How did\nNorth Korea\nrob\n[Binance?]"


def thumbs(out: Path) -> Path:
    """Binance's own card, large, on the right over the North Korean flag,
    and the video's question in four rows on the flag's darkened left.

    **The feed check's fix.** The first cover put the finished `sweep` card
    there; beside the top three results at 320px (Meet Kevin, Hidden
    Economy, ABC) the card was unreadable noise, while the flag was the one
    thing on that results page saying "North Korea". The real subject's
    own art leads (`thumbnails.md`), so the pairing is the flag and the
    Binance tile - who, and whom - readable before a word is."""
    import numpy as np
    from PIL import Image, ImageDraw, ImageEnhance, ImageFilter
    from video_automation.longform import thumb as T
    card = Image.open(BINANCE).convert("RGB")
    cw = 560
    card = card.resize((cw, int(card.height * cw / card.width)), Image.LANCZOS)
    im = Image.open(FLAG).convert("RGB").resize((1280, 720), Image.LANCZOS)
    im = ImageEnhance.Brightness(im.filter(ImageFilter.GaussianBlur(2))).enhance(0.55)
    a = np.zeros((1, 1280), np.float32)
    a[0, :560] = 0.55
    a[0, 560:740] = np.linspace(0.55, 0.0, 180)
    shade = Image.fromarray((np.repeat(a, 720, 0) * 255).astype("uint8"))
    im = Image.composite(Image.new("RGB", im.size, (0, 0, 0)), im, shade)
    x, y = 1280 - cw - 34, (720 - card.height) // 2
    drop = Image.new("L", im.size, 0)
    drop.paste(255, (x + 10, y + 14, x + cw + 10, y + card.height + 14))
    drop = drop.filter(ImageFilter.GaussianBlur(18)).point(lambda v: int(v * 0.7))
    im = Image.composite(Image.new("RGB", im.size, (0, 0, 0)), im, drop)
    shape = Image.new("L", card.size, 0)
    ImageDraw.Draw(shape).rounded_rectangle([1, 1, card.width - 2, card.height - 2],
                                            radius=18, fill=255)
    im.paste(card, (x, y), shape)
    fill, ink = T.ACCENTS["yellow"]
    T._headline(im, HEADLINE, 180, int((x - 70) / 1.38), 34, fill, ink,
                max_lines=4, leading=1.0, band="middle", margin=34,
                shadow=12, drop=(5, 6))
    im.save(out, quality=92)
    return out


def main() -> None:
    out = Path.home() / "Desktop/binance-hack-long.mp4"
    work = Path.home() / "Desktop/.binance-hack-long-work"
    made = render_long(
        SECTIONS, out, work, brand=CRYPTO, meta=META, voice=VOICE,
        music=MUSIC,
        callouts=None,
        # The payoff is a number. Last three long forms opened
        # Counter / Search / Search.
        opener=Counter("$6.36B", "TAKEN FROM BINANCE, 29 OCT 2026",
                       at_word="billion"),
        emphasis=["thirty-six hours", "still moving"],
        thumb_headline=HEADLINE,
        thumb_accent="yellow",
        endcard=ENDCARD, endcard_lead=7.0,
        title_at=10.0, title_hold=5.4,
    )
    # `render_long`'s own thumbnail is replaced by the hand-built one.
    made["thumb"] = thumbs(Path(made["thumb"]))
    for k, v in made.items():
        print(f"{k}: {v}")


if __name__ == "__main__":
    if "--thumb" in sys.argv:
        print(thumbs(Path.home() / "Desktop/binance-hack-long-thumb.jpg"))
    else:
        main()
