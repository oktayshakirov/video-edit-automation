"""Who actually holds your keys? ~50s crypto short.

Source: crypto-wiki/content/posts/understanding-crypto-exchanges.mdx, the same
post as the `crypto-exchanges-long` explainer.

**It narrows the long form's angle rather than repeating it.** That video walks
the whole taxonomy — what an exchange is, centralized against decentralized,
trading pairs, the checks before you deposit — and deliberately never names a
platform as one thing or another, because a three-minute explainer that starts
ranking exchanges stops being an explainer. Forty seconds cannot walk a taxonomy
at all, so this one does the single thing the long form leaves out: it puts four
real platforms on screen and answers the custody question for each.

**The beat is `facts.py`, not a script.** `F.compare(..., "custody", ...)` reads
the `quickFacts` block the site already publishes and maintains across all 27
exchange files, so the four verdicts on screen are the site's own data rather
than this repo's opinion — which is exactly the case the crypto skill makes for
that module. Coinbase, Binance and Crypto.com come back custodial; Uniswap comes
back non-custodial. The article names all four in its own examples.

**A cross here means custodial, not bad**, and the beat's title says so —
`WHO HOLDS YOUR KEYS?`, where the tick is "you do". That distinction is the
whole reason this is not a platform rating and not financial advice: it is a
factual answer to a question about custody, and the fix at the end is a security
practice the article states in its own Best Practices section.

**Two-phase, and the beat is `logos` rather than `checklist`.** The narration
reads four names and no verdicts, so the badges *are* the answer and holding
them for the pause is the point. What changed after the first cut is the
graphic: a list of four names with three crosses and one tick did not say why
the tick was a tick, and the user found it confusing. Brand cards in a 2x2 —
two labelled "they hold", two "you hold" — make the split the subject, and the
custody verdict still lands into each tile's corner in the pause.

Run from the repo root:

    PYTHONPATH=. .venv/bin/python projects/crypto-short/crypto-exchanges.py
"""

from pathlib import Path

from video_automation.core.brand import CRYPTO
from video_automation.core.stock import CACHE as STOCK
from video_automation.crypto import facts as F
from video_automation.crypto.build import render_crypto_short
from video_automation.crypto.shots import SITE_IMAGES, Shot
from video_automation.longform.thumb import render_short_thumb

POSTS = SITE_IMAGES / "posts"

# Screened across their length, not at one second — the trailing comment is the
# luma/saturation range over the whole clip. Cached by the long-form build from
# the same post. All three are centre-weighted, which a 9:16 crop requires: it
# keeps roughly the middle third and a wide establishing shot loses its subject.
PHONE = STOCK / "videos/smartphone-finance-app-dark/35518150.mp4"   # L34-45 S24-29
CHART = STOCK / "videos/stock-market-chart-screen-dark/38133087.mp4"  # L20 S19
CANDLE = STOCK / "videos/trading-candlestick-chart-monitor/38471109.mp4"  # L15-16 S18
WAVES = STOCK / "videos/abstract-dark-waves-motion/15690300.mp4"    # L9-10 S0

VOICE = "mia"                   # female, af_heart. Matches the long form from
                                # the same post. Still a candidate, not approved.

# The site's own frontmatter answers the beat. `contains("non-custodial")` is
# the right predicate rather than a negated "Custodial": Coinbase's value is
# "Custodial; self-custody available via the separate Coinbase Wallet", and the
# honest reading of that is still custodial — the wallet is a different product.
# The site's own frontmatter answers the beat. `contains("non-custodial")` is
# the right predicate rather than a negated "Custodial": Coinbase's value is
# "Custodial; self-custody available via the separate Coinbase Wallet", and the
# honest reading of that is still custodial — the wallet is a different product.
#
# **Two and two, not three and one.** The first cut listed Coinbase, Binance,
# Crypto.com and Uniswap, and the user found the beat confusing — rightly: with
# a single tick at the end there is nothing to tell you the tick means
# *decentralized* rather than "best one". A balanced pair of pairs makes the
# split the subject.
#
# **PancakeSwap, driven by `facts.py` like the other three.** The site gained
# `content/exchanges/pancakeswap.mdx` between the first draft of this script and
# the rebuild — its own `quickFacts.custody` reads "Non-custodial; users trade
# directly from their own wallet" — so the row is the site's maintained data
# again rather than a literal written here. All four rows now come from the
# same source, which is the property this beat is supposed to have.
PICKS = ("coinbase", "binance", "uniswap", "pancakeswap")
CUSTODY = F.compare([F.load("exchanges", s) for s in PICKS],
                    "custody", F.contains("non-custodial"))

# One tuple per sentence; each string is one caption. The logos beat must have
# exactly one caption per tile — that is what times its reveals.
SENTENCES = [
    ("Your crypto is sitting on an exchange.",
     "So who is actually holding it?"),

    ("Not you.",
     "You hold zero of the private keys."),

    ("Your balance is a row",
     "in that company's database."),

    # The question goes here, not inside the beat: a beat times its reveals off
    # the caption starts of its own sentence, so a lead-in line inside that
    # span eats reveal zero and shunts every item one line late.
    ("It is not the same everywhere.",
     "So who holds the keys?"),

    # The beat. Four names, no verdicts in the voice — the badges are the
    # answer, which is why this is two-phase and takes the long gap below.
    # **"Binance" is spelled for espeak**: the real spelling phonemizes to
    # `baɪnˈæns`, bye-NANCE, which is what the user heard and called wrong.
    # **The fourth name is PancakeSwap, not Hyperliquid.** The beat's own
    # payload switched to PancakeSwap when the site gained a real page for it
    # (`content/exchanges/pancakeswap.mdx`), but this line was left reading
    # the old name — voice and visual disagreed on which tile was on screen,
    # which the user caught. "PancakeSwap" phonemizes cleanly on its own
    # (`pˈæŋkeɪk swˈɑːp`) and needs no respelling.
    (("Coinbase.", "Coinbase."),
     ("Binance.", "Bynanse."),
     ("Uniswap.", "Uniswap."),
     ("PancakeSwap.", "PancakeSwap.")),

    ("The first two hold your keys for you.",
     "The other two cannot.",
     "That is the whole split."),

    # **The tip needs a reason before it is a tip.** The user's note was that
    # the three habits arrived with no introduction — a list of instructions
    # with nothing saying why you are being given them. One sentence fixes it,
    # and it also ties the fix back to the beat above rather than leaving it
    # as generic advice.
    ("You cannot change who holds the keys.",
     "You can change how much they are holding.",
     "Three things, today."),

    # A vertical `steps` track — a completely different silhouette from the
    # logo grid, which is the point: two beats of the same shape in one short
    # read as the same graphic twice.
    ("Turn on app-based two-factor.",
     "Keep only what you are trading on there.",
     "Move the rest to a wallet you control."),

    # **The card needs a line handing off to it.** A full-screen statement that
    # arrives with nothing in front of it reads as a title card dropped into
    # the middle of the video; one sentence turns it into the thing the video
    # has been building toward. Same note the three habits got.
    ("Always remember the golden rule.",),

    # **A full-screen statement, not a caption over footage.** The line is the
    # whole argument and the user asked for it big. A `chapter` beat in 9:16
    # wraps to three lines at 148px and burns no caption over itself, because
    # `build` suppresses captions on any shot carrying a graphic.
    (("NOT YOUR KEYS, NOT YOUR COINS.",
      "Not your keys, not your coins."),),

    # **A hyphen, never an em or en dash.** The user's rule, for every video:
    # a dash set as "—" reads as a typographic flourish in a burned caption and
    # at caption size the long rule is easy to mistake for a stray mark. Only
    # "-" goes on screen.
    ("So - who is holding yours?",),
]

SHOTS = [
    # 1 — motion on frame one. A Short is judged in its first second, and the
    # subject is literally the thing the first line names.
    Shot(clip=PHONE, clip_at=0.5),

    # 2 — a different clip rather than the same one running on, so the opening
    # pair reads as two shots.
    Shot(clip=CHART, clip_at=2.0),

    # 3 — the first photograph, framed. The clip/card contrast is what makes
    # the alternation read as rhythm.
    Shot(image=POSTS / "futuristic-crypto-exchange.jpg",
         zoom=1.11, pan=(0.02, 0.01), aspect=1.15, bias=0.40),

    # 4 — the gold lock on black, on the line that asks the question. It is the
    # closest thing in the library to on-palette.
    Shot(image=POSTS / "security-combination-lock.jpg",
         zoom=1.10, pan=(-0.02, 0.01), aspect=1.15, bias=0.45),

    # 5 — the beat: the site's own brand cards in one column, under a heading
    # per group, with the custody verdict landing into each tile's corner in
    # the pause afterwards. **The headings replace the per-tile labels** — with
    # "CENTRALIZED" standing over the pair, "they hold" under each card is the
    # same fact said twice, and the column has less room than the 2x2 did.
    Shot(graphic="logos",
         payload=([(slug, "", ok) for slug, (_, ok) in zip(PICKS, CUSTODY)],
                  "WHO HOLDS THE KEYS?",
                  [("Centralized", 2), ("Decentralized", 2)]),
         backdrop=POSTS / "laptop-trading.jpg"),

    Shot(clip=CANDLE, clip_at=1.0),

    Shot(image=POSTS / "digital-technology.jpg",
         zoom=1.12, pan=(0.02, -0.01), aspect=1.15, bias=0.40),

    # 8 — the fix, as a vertical track.
    Shot(graphic="steps",
         payload=(["App-based two-factor",
                   "Only what you are trading",
                   "The rest in your own wallet"],
                  "DO THIS TODAY"),
         backdrop=POSTS / "global-map.jpg"),

    # 9 — the hand-off into the card, on the gold lock: the picture the beat
    # about custody already used, so the echo is visual as well as verbal.
    Shot(image=POSTS / "security-combination-lock.jpg",
         zoom=1.12, pan=(0.02, -0.01), aspect=1.15, bias=0.45),

    # 10 — the line, full screen.
    Shot(graphic="chapter", payload=("NOT YOUR KEYS, NOT YOUR COINS.",)),

    # 10 — the ask, on something uncluttered and moving again.
    Shot(clip=WAVES, clip_at=1.0),
]


EMOJI = {
    "So - who is holding yours?": "\U0001F447",
}

# **Pauses are punctuation.** The first cut ran 0.34 everywhere except the two
# beats and the user's note was that the whole read is monotone. 0.34 inside a
# thought, 0.55-0.90 at the end of one, and the long gaps only where a beat
# needs room. The logo beat (index 4) is two-phase and keeps the full 2.10: the
# four tiles sit unmarked, the voice stops, and the badges land in the silence.
# `steps` (index 7) takes 0.90 — a beat whose sentence is short is otherwise
# gone in under two seconds — and the statement card (index 8) takes 1.30,
# because a line that fills the screen has to be allowed to sit there.
GAPS = [0.60, 0.80, 0.55, 0.90, 2.10, 0.80, 0.70, 0.90, 0.70, 1.30, 0.34]


def main() -> None:
    out = Path.home() / "Desktop/crypto-exchanges-short.mp4"
    work = Path.home() / "Desktop/.crypto-exchanges-short-work"
    out, total = render_crypto_short(SENTENCES, SHOTS, out, work,
                                     voice=VOICE, emoji=EMOJI, gap=GAPS)

    # **Same source and same headline as the long form from this post** — the
    # pairing rule the tinnitus pairs settled: match a Short to its long form's
    # thumbnail even where the two videos cover different ground, because the
    # thumbnail pairing and the script's angle are independent questions.
    #
    # **`band="bottom"`, not the default top.** The default is right when the
    # Shorts player's chrome is the only consideration, and wrong the moment
    # the subject's face is in the top half of the crop — which it is here,
    # and the first cut printed the headline across it. Text over a face reads
    # as a mistake regardless of how correct the safe-area reasoning is.
    thumb = render_short_thumb(
        out.with_name(out.stem + "-thumb.jpg"), CRYPTO,
        "Your crypto is [not yours]",
        image=POSTS / "futuristic-crypto-exchange.jpg", accent="red",
        band="bottom")
    print(f"{out}  {total:.2f}s")
    print(f"{thumb}")


if __name__ == "__main__":
    main()
