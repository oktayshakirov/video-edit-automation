"""Crypto exchanges explained — long-form 16:9 for YouTube.

Source: crypto-wiki/content/posts/understanding-crypto-exchanges.mdx.
**Second on the demand ranking in `docs/long-form-strategy.md` — 1,038 views**,
behind the mining rig, which already shipped. Like that one it is a query typed
into YouTube more or less verbatim ("crypto exchanges explained", "CEX vs DEX"),
and like that one there is no short from this post to inherit an angle from —
so the short built alongside this one takes its angle from here, not the
reverse.

**The article is a taxonomy plus a buyer's guide, and the video cannot be
either.** Read aloud, "here are the pros, here are the cons, here are five
factors to consider" is a comparison table with a voice over it. So the script
takes the thing the article states plainly in a Cons bullet and again under Best
Practices — **on a centralized exchange you hold none of the keys** — and puts
it in the first thirty seconds as a question the viewer has a stake in. The
taxonomy then arrives as the *answer* to that question rather than as an agenda.

The arc:

* **Hook** — you can see your balance. Who is actually holding it? Zero keys.
* **Reframe** — an exchange is a marketplace; the middle is where they split.
  One is a company, one is a piece of code.
* **Deep dive** — what each actually gives you, then trading pairs, which is
  the one piece of jargon on every screen and the thing beginners ask about.
* **Twist** — the friendlier platform is the one where you own nothing. The
  support line and the password reset are what make it custodial.
* **Mirror** — so the checks, and the habits, are about the same question.
* **Echo** — back to the balance on the screen, reframed.

**No financial advice, and the line here is about *custody*, not about price.**
The script never suggests an exchange, never rates one, and never implies a
holding will gain. Everything it recommends is a security practice the article
already states: app-based two-factor, cold storage, limit orders, and moving
what you are not trading off the platform. The named exchanges are named as
examples of the category, exactly as the article names them, with no ranking.

**Beat silhouettes, checked before building** — the skill's rule is to list them
and confirm you are not drawing the same two shapes four times. Six beats, six
different shapes, and no shape repeats: `stat` (hook), `compare` (the split),
`grid` (three pair types), `quote` (the twist), `checklist` (five checks, two
phase), `steps` (four habits, a sequence). Item counts vary too — 3+3, 3, 5, 4.

**Pictures.** The post owns four images and two of them are out on brightness:
`crypto-exchange.jpg` measures L144 and `cryptocurrency.jpg` L179/S83, both far
over the ~L82 working ceiling for a site photograph. Its other two —
`laptop-trading.jpg` (L55/S25) and `law.jpg` (L42/S11) — are in, and both are
used on the lines they were drawn for. The rest of the site photography comes
from the wider library, screened: `futuristic-crypto-exchange.jpg` (L52/S28) is
the pick of it and is gold-lit, which is rarer than it sounds.

**Stock screening rejected two whole queries.** Every `bank vault safe door`
result is a lit chrome door (L59-184) and every `passport identity document
desk` result is a bright overhead flat-lay (L47-155) — the two most obvious
illustrations for custody and for identity checks, and neither has a usable
frame. Both are cached and manifested as rejects. The custody line is carried by
`security-combination-lock.jpg` instead, which is a gold lock on black and is
the closest thing in either library to on-palette, and the identity line by the
article's own `law.jpg`.

**Phonemes.** No initialism is spoken. "CEX" and "DEX" never appear in the
narration — they are "centralized" and "decentralized" throughout, which is also
what a beginner searching this actually types. "Crypto.com" is written "Crypto
dot com" in the spoken form or the synthesiser reads the full stop as a sentence
end. "BTC/USD" is spoken as "bitcoin slash dollar" and the slash is shown, not
said as punctuation. "2FA" is "two-factor authentication" and then "two-factor".

Run from the repo root:

    PYTHONPATH=. .venv/bin/python projects/crypto-long/crypto-exchanges.py
"""

from pathlib import Path

from video_automation.core import music
from video_automation.core.brand import CRYPTO
from video_automation.core.stock import CACHE as STOCK
from video_automation.crypto.shots import SITE_IMAGES, Shot
from video_automation.longform import Meta, Section, render_long

POSTS = SITE_IMAGES / "posts"

# Pexels, cached under assets/stock/ and screened across the clip rather than at
# one second — the trailing comment is the luma/saturation range over the whole
# length. The chart footage is the one category this topic has in abundance and
# it is also the one that risks looking like a single clip reused: four distinct
# desks, deliberately, plus the phone.
CHART = STOCK / "videos/stock-market-chart-screen-dark"      # see per-file below
CANDLE = STOCK / "videos/trading-candlestick-chart-monitor"  # 38471109 L15-16 S18
FLOOR = STOCK / "videos/wall-street-trading-floor-screens"   # see per-file below
PHONE = STOCK / "videos/smartphone-finance-app-dark"         # 35518150 L34-45 S24-29
TICKER = STOCK / "videos/cryptography-code-screen"           # 14003933 L17-19 S14
STREAM = STOCK / "videos/digital-code-stream-dark"           # 34127877 L13-15 S5
SERVER = STOCK / "videos/server-room-data-center"            # 7140928  L22-31 S24-43
KEYS = STOCK / "videos/typing-keyboard-night"                # 8212370  L20-25 S10-12
VAULTISH = STOCK / "videos/warehouse-industrial-dark-interior"  # 19217894 L23-34 S3
PARTICLES = STOCK / "videos/dark-abstract-digital-particles"  # 36703282 L9 S0
WAVES = STOCK / "videos/abstract-dark-waves-motion"          # 15690300 L9-10 S0

COINS = STOCK / "photos/hardware-wallet-crypto-dark/20534456.jpg"  # L28 S2

ENDCARD = STOCK / "videos/subscribe/4928934.mp4"

VOICE = "mia"                   # female, af_heart. Candidate, not approved.

# **A real track, shared with tinnitushelp.me.** `night-drift` was picked by
# ear for `tinnitus-and-sleep` and the user's call is that the small library in
# `assets/brand/music/` serves both channels rather than one — which is the
# right shape for it: the tracks are brand-neutral, they are stored trimmed so
# they loop without a hole, and a bed a human chose beats a generated one that
# only measures correctly. The generated presets stay as the licence-safe
# fallback; see that directory's README before adding another.
MUSIC = music.track("night-drift")

URL = "https://thecrypto.wiki/posts/understanding-crypto-exchanges"

A = 16 / 9                      # crop toward the frame, not the shorts' 1.15


SECTIONS = [
    # --- the hook. No card: an opening chapter card spends the one second
    # that decides whether anybody stays. Frame one is a clip, not a still. ---
    Section(
        title="Who is actually holding it?",
        card=False,
        sentences=[
            ("You bought your first crypto.",
             "You can see the balance on the screen."),
            # **Not "here is the question almost nobody asks about it".** That
            # construction went into three scripts before the user called it
            # out, and they are right that it is bad English — "about it" has
            # nothing to attach to, and the whole clause is a windup that
            # announces a question instead of asking one. Ask the question.
            ("But who is actually holding it?",),
            ("Because on most platforms,",
             "the answer is not you."),
            # The retention call, out loud, in the first fifteen seconds — and
            # the outro answers this exact question rather than a near one.
            ("Stay to the end",
             "and you will know which of the two kinds",
             "you are using,",
             "and the one thing to do",
             "the moment a trade settles."),
            ("Start with the number",
             "that surprises people most."),
            ("Zero.",),
            ("That is how many private keys you hold",
             "when your coins sit",
             "on a centralized exchange."),
            ("The company holds every one of them.",),
        ],
        shots=[
            Shot(clip=PHONE / "35518150.mp4", clip_at=0.5),
            None,                                    # ride the motion
            # The title stamp, on the line that makes the promise. The darkest
            # and least busy of the chart clips, because it carries type.
            Shot(clip=FLOOR / "38797295.mp4",
                 payload=("", "CRYPTO EXCHANGES, EXPLAINED")),
            Shot(clip=CHART / "38133087.mp4", clip_at=2.0,
                 payload=("", "Which kind are you using?")),
            Shot(image=POSTS / "portfolio.jpg", zoom=1.11, pan=(-0.02, 0.01),
                 aspect=A, bias=0.45),
            # Said, then shown. "Zero" is exact, it is the video's thesis, and
            # unlike a bare count of unseen things the note says what it counts.
            Shot(graphic="stat",
                 payload=("0", "PRIVATE KEYS YOU HOLD",
                          "On a centralized exchange. The company holds them all."),
                 backdrop=POSTS / "digital-technology.jpg"),
            None,
            Shot(image=POSTS / "security-combination-lock.jpg", zoom=1.10,
                 pan=(0.02, 0.01), aspect=A, bias=0.5),
        ],
        # **Silence is punctuation, and this script had none.** Every sentence
        # ran at the same 0.34 and the user's note was that the whole thing is
        # monotone — correctly, because pace is the only prosody an AI voice
        # has. The convention now: 0.34 inside a thought, 0.55-0.70 at the end
        # of one, 0.90-1.20 before a line that has to land, and 2.10-2.40 for a
        # two-phase beat. That is the whole of it; longer than 1.2 outside a
        # beat is a hole, not a pause.
        gaps=[0.60, 0.90, 0.70, 0.60, 0.55, 1.10, 0.45, 0.80],
    ),

    # --- reframe: it is a marketplace, and the middle is where they split ----
    Section(
        title="So what is an exchange, actually?",
        sentences=[
            ("An exchange is a marketplace.",
             "Nothing more mysterious than that."),
            ("It matches somebody who wants to buy",
             "with somebody who wants to sell,",
             "and takes a small cut",
             "for standing in the middle."),
            ("It is also where the price comes from,",
             "and where liquidity lives."),
            # No jargon without an immediate plain-English decode.
            ("Liquidity just means",
             "there are enough buyers and sellers",
             "that your order fills",
             "at roughly the price you expected."),
            ("But how that middle is built",
             "is where the two families split."),
            ("One of them is a company.",
             "The other is a piece of code."),
            ("And that single difference",
             "decides everything else about them."),
        ],
        shots=[
            Shot(clip=FLOOR / "38055932.mp4", clip_at=1.0),
            Shot(image=POSTS / "futuristic-crypto-exchange.jpg", zoom=1.11,
                 pan=(0.02, 0.01), aspect=A, bias=0.45),
            None,
            Shot(image=POSTS / "laptop-trading.jpg", zoom=1.12,
                 pan=(-0.02, -0.01), aspect=A, bias=0.45),
            Shot(image=POSTS / "analysis.jpg", zoom=1.11, pan=(0.02, -0.01),
                 aspect=A, bias=0.45),
            Shot(clip=SERVER / "7140928.mp4",
                 payload=("", "A company, or a piece of code")),
            Shot(clip=STREAM / "34127877.mp4"),
        ],
        gaps=[0.55, 0.60, 0.45, 0.75, 0.90, 0.90, 0.70],
    ),

    # --- the deep dive: what each one actually gives you ---------------------
    Section(
        title="A company, or a smart contract?",
        sentences=[
            ("A centralized exchange is a business.",),
            # **The names get the logos.** A script that reads three brand
            # names over a stock photograph of a trading desk is asking the
            # viewer to hold them in their head for no reason; the site owns
            # 27 exchange brand cards and the `logos` beat exists now to use
            # them. One caption per tile, which is what times the reveals.
            #
            # **"Binance" is spelled for espeak, not for the reader.** Kokoro
            # phonemizes through espeak-ng, which reads the real spelling as
            # `baɪnˈæns` — bye-NANCE, stress on the second syllable, which is
            # what the user heard and called wrong. "Bynanse" comes back
            # `bˈaɪnæns`, which is the brand's own BY-nance.
            (("Coinbase.", "Coinbase."),
             ("Binance.", "Bynanse."),
             ("Crypto.com.", "Crypto dot com.")),
            ("It runs an order book,",
             "it checks who you are,",
             "and it keeps your coins",
             "in wallets that it controls."),
            ("A decentralized exchange",
             "has no company in it at all."),
            ("You connect your own wallet,",
             "a smart contract does the swap,",
             "and your keys never leave your hands."),
            ("Most of them do not even run an order book.",
             "You trade against a pool of coins",
             "that other users put there,",
             "and those users take the fees."),
            # Say the point, then show the graphic.
            ("So look at what each one",
             "actually hands you."),
            # **The column headings are spoken and revealed.** They used to be
            # painted at f=0, so both lists were labelled before either had
            # anything in it and the viewer had to work out which one the voice
            # was on. `name_columns=True` makes each heading its own revealed
            # item, so the order on screen is exactly the order in the mouth:
            # "Centralized", three items, "Decentralized", three items.
            ("Centralized.",
             "Deep liquidity and fast fills.",
             "Cash in, and cash out.",
             "It holds your keys.",
             "Decentralized.",
             "You keep your keys.",
             "No identity check.",
             "Thinner markets, and network fees."),
            ("Neither column is the winner.",
             "They are answers",
             "to two different questions."),
        ],
        shots=[
            Shot(clip=CHART / "38783511.mp4", clip_at=1.0,
                 payload=("", "A business, with an order book")),
            Shot(graphic="logos",
                 payload=(["coinbase", "binance", "crypto"],
                          "THE ONES YOU HAVE HEARD OF")),
            Shot(clip=VAULTISH / "19217894.mp4",
                 payload=("", "Your coins, in their wallets")),
            Shot(image=POSTS / "global-map.jpg", zoom=1.10, pan=(0.02, 0.01),
                 aspect=A, bias=0.5),
            Shot(clip=TICKER / "14003933.mp4", clip_at=2.0,
                 payload=("", "A smart contract does the swap")),
            Shot(image=POSTS / "futuristic-ui.jpg", zoom=1.11,
                 pan=(-0.02, 0.01), aspect=A, bias=0.45),
            None,
            Shot(graphic="compare",
                 payload=("Centralized",
                          ["Deep liquidity, fast fills",
                           "Cash in and cash out",
                           "It holds your keys"],
                          "Decentralized",
                          ["You keep your keys",
                           "No identity check",
                           "Thinner markets, network fees"],
                          True),),
            Shot(image=COINS, zoom=1.11, pan=(0.02, -0.01), aspect=A, bias=0.5),
        ],
        gaps=[0.55, 0.80, 0.60, 0.55, 0.60, 0.70, 0.90, 0.70, 0.80],
    ),

    # --- the one piece of jargon on every screen ----------------------------
    Section(
        title="What is a trading pair?",
        sentences=[
            ("One thing confuses every beginner,",
             "and it is written on every screen."),
            # Spoken "U S D", not "dollar" — the pair on screen reads USD and
            # the voice should read what the screen says. espeak gives
            # `jˌuːˌɛsdˈiː`, which is the three letters.
            (("You will see it written as BTC / USD.",
              "You will see it written as bitcoin slash USD."),),
            ("The first one is what you are buying.",
             "The second is what you are paying with."),
            ("That is the whole idea.",
             "A price only means something",
             "measured against something else."),
            ("And they come in three kinds.",),
            ("Crypto against real money.",
             "Crypto against other crypto.",
             "Crypto against a stablecoin."),
            ("Which pairs a platform offers",
             "decides what you can buy directly,",
             "and what costs you three trades",
             "and three sets of fees."),
        ],
        shots=[
            Shot(clip=STREAM / "19808379.mp4", clip_at=1.0),
            Shot(clip=FLOOR / "38569995.mp4", clip_at=2.0,
                 payload=("", "BTC / USD")),
            None,
            Shot(image=POSTS / "analysis.jpg", zoom=1.10, pan=(-0.02, 0.01),
                 aspect=A, bias=0.5),
            Shot(clip=STREAM / "34127877.mp4", clip_at=8.0),
            # A `grid`, not a checklist: three kinds of pair is a *set*, there
            # is no verdict column to fill, and the second line on each card is
            # room a list row does not have. Three cards now stack in one
            # column — a 2x2 with an empty cell reads as a layout that failed
            # rather than as a set of three.
            Shot(graphic="grid",
                 payload=([("Crypto to cash",
                            "Getting into the market, and back out"),
                           ("Crypto to crypto",
                            "Swapping without touching a bank"),
                           ("Crypto to stablecoin",
                            "Parking value without leaving the platform")],
                          "THREE KINDS OF PAIR"),),
            Shot(image=POSTS / "laptop-trading.jpg", zoom=1.12,
                 pan=(0.02, -0.01), aspect=A, bias=0.4),
        ],
        gaps=[0.60, 0.90, 0.70, 0.60, 0.90, 0.80, 0.70],
    ),

    # --- the twist. A statement card: it resolves, it does not ask. ---------
    Section(
        title="Not your keys, not your coins",
        spoken_title="Not your keys, not your coins.",
        sentences=[
            ("Now the part that catches people out.",),
            ("The friendlier platform",
             "is the one where you own nothing."),
            ("A centralized exchange feels safe.",
             "There is a support line.",
             "There is a password reset.",
             "It looks like online banking."),
            ("But those are exactly the features",
             "that require somebody else",
             "to be holding the keys."),
            ("Your balance is a row",
             "in that company's database.",
             "The coins behind it sit in their wallets,",
             "pooled with everybody else's."),
            ("There is an old line about this",
             "and it has outlasted every exchange",
             "that ignored it."),
            ("Not your keys, not your coins.",),
            ("So do not treat an exchange",
             "like a bank account.",
             "It is a place you pass through."),
        ],
        shots=[
            Shot(clip=PHONE / "35518150.mp4", clip_at=3.0),
            Shot(image=POSTS / "futuristic-ui.jpg", zoom=1.11, pan=(0.02, 0.01),
                 aspect=A, bias=0.4),
            # **An exchange interface — but the app, not the website.** The
            # user asked to show one and the site owns both kinds. The website
            # screenshots are the wrong kind and it took a render to see why:
            # `bitfinex-ui.png` measures L46 and `gemini-exchange-trading.jpg`
            # L67, both inside the box, and on the frame they are a bright
            # teal marketing page with a green promo bar and two hundred words
            # of unreadable small type. **The luma box does not screen a
            # screenshot** — a UI is dark chrome carrying small bright text, so
            # the mean reads dark while the eye reads bright, and the legible
            # content is the same objection the no-infographics rule already
            # makes. A branded homepage under a line about custody risk is also
            # closer to naming a platform than this script ever wants to be.
            #
            # `portfolio.jpg` is the app: a phone showing a coin list and
            # balances, dark, unbranded, and the exact thing the sentence is
            # describing.
            Shot(image=POSTS / "portfolio.jpg", zoom=1.10, pan=(-0.02, 0.01),
                 aspect=A, bias=0.5),
            Shot(clip=TICKER / "14003933.mp4", clip_at=6.0,
                 payload=("", "Somebody else has to hold the keys")),
            Shot(clip=SERVER / "7140928.mp4", clip_at=3.0,
                 payload=("", "Pooled, in wallets they control")),
            Shot(image=POSTS / "digital-technology.jpg", zoom=1.11,
                 pan=(0.02, -0.01), aspect=A, bias=0.45),
            Shot(graphic="quote",
                 payload=("Not your keys, not your coins.",
                          "the oldest rule in crypto"),
                 picture=POSTS / "security-combination-lock.jpg"),
            Shot(clip=VAULTISH / "19217894.mp4", clip_at=3.0,
                 payload=("", "A place you pass through")),
        ],
        # The quote is the line the section is built toward; buy it a pause.
        gaps=[0.90, 0.70, 0.60, 0.70, 0.60, 0.90, 2.40, 0.80],
    ),

    # --- mirror, echo, and the ask ------------------------------------------
    Section(
        title="So how do you choose one?",
        sentences=[
            ("Before you trust any platform",
             "with a single coin,",
             "run the same five checks."),
            ("Two-factor authentication from an app.",
             "Most coins held offline, in cold storage.",
             "A licence in a country you have heard of.",
             "Fees you can find without hunting.",
             "A history you can look up."),
            ("Miss one of those",
             "and you are not choosing an exchange.",
             "You are hoping."),
            ("And once you are in,",
             "four habits do most of the work."),
            ("Turn the two-factor on first.",
             "Start with an amount you can afford to lose.",
             "Learn limit orders before market orders.",
             "Then move what you are not trading",
             "off the platform."),
            ("A limit order waits for your price.",
             "A market order takes whatever is there.",
             "That difference costs beginners",
             "more than the fees do."),
            ("So — back to the balance on your screen.",),
            ("The question was never",
             "which exchange is the best one.",
             "It is: who is holding it right now?"),
            ("Know that,",
             "and you already know",
             "whether it should still be sitting there."),
            ("The full comparison and the platform reviews",
             "are linked below —",
             "and nothing here is financial advice."),
            ("If that was useful,",
             "subscribe for more videos like this one."),
        ],
        shots=[
            Shot(image=POSTS / "law.jpg", zoom=1.11, pan=(0.02, 0.01),
                 aspect=A, bias=0.45),
            # **`flow=True`: each tick lands on the check that earns it.** The
            # two-phase version held all five verdicts for a pause at the end,
            # which is right when the list is a question — and this list is
            # not. Every item here is already a thing you *should* have, the
            # voice says so as it names them, and the user asked for the check
            # to land after each one. The pause drops from 2.40 to 1.20
            # accordingly: the silence that bought room for the marks is dead
            # air once the marks are landing on the words.
            Shot(graphic="checklist",
                 payload=([("App-based two-factor", True),
                           ("Most coins in cold storage", True),
                           ("Licensed where it operates", True),
                           ("Fees published plainly", True),
                           ("A track record you can check", True)],
                          "BEFORE YOU DEPOSIT", True),
                 picture=POSTS / "security-combination-lock.jpg"),
            Shot(clip=CHART / "38783511.mp4", clip_at=8.0,
                 payload=("", "Otherwise you are hoping")),
            Shot(image=POSTS / "futuristic-crypto-exchange.jpg", zoom=1.11,
                 pan=(-0.02, -0.01), aspect=A, bias=0.45),
            # A `steps`: these are in order, and order is the thing no other
            # beat can show. One caption chunk per node times the reveals.
            Shot(graphic="steps",
                 payload=(["Turn on app-based two-factor",
                           "Start small",
                           "Learn limit orders",
                           "Withdraw what you are not trading"],
                          "ONCE YOU ARE IN"),),
            Shot(clip=FLOOR / "38395150.mp4", clip_at=2.0,
                 payload=("", "Limit waits. Market takes.")),
            # The echo: the picture the video opened on, under the closing line
            # that reframes the opening one.
            Shot(clip=PHONE / "35518150.mp4", clip_at=1.0),
            Shot(clip=PARTICLES / "36703282.mp4",
                 payload=("", "Who is holding it right now?")),
            Shot(image=POSTS / "global-map.jpg", zoom=1.10, pan=(-0.02, 0.01),
                 aspect=A, bias=0.5),
            Shot(image=COINS, zoom=1.11, pan=(0.02, 0.01), aspect=A, bias=0.45),
            # Held on the abstract, so YouTube's end-screen cards have
            # somewhere uncluttered to sit when they go on at upload.
            Shot(clip=WAVES / "15690300.mp4"),
        ],
        gaps=[0.90, 1.20, 0.80, 0.90, 0.70, 0.70, 0.90, 2.40, 0.80, 0.60, 2.80],
    ),
]

META = Meta(
    title="Crypto Exchanges Explained: Who Actually Holds Your Coins?",
    hook="Centralized or decentralized, what a trading pair is, and the one "
         "thing to do the moment a trade settles.",
    url=URL,
    summary="How cryptocurrency exchanges work, the real difference between "
            "centralized and decentralized platforms, what a trading pair is, "
            "and the security checks worth running before you deposit "
            "anything.",
    tags=["crypto exchanges", "crypto exchanges explained", "cex vs dex",
          "centralized exchange", "decentralized exchange", "trading pairs",
          "crypto for beginners", "not your keys not your coins"],
    cta=f"Full comparison, platform reviews and safety practices: {URL}",
    credits=["Footage: Pexels (Pexels licence, no attribution required).",
             "Music: oosongoo, via Pixabay.",
             "Nothing in this video is financial advice."],
)


def main() -> None:
    out = Path.home() / "Desktop/crypto-exchanges-long.mp4"
    work = Path.home() / "Desktop/.crypto-exchanges-long-work"
    made = render_long(
        SECTIONS, out, work, brand=CRYPTO, meta=META, voice=VOICE,
        music=MUSIC,
        callouts=None,
        # The title already carries the search phrase and already asks the
        # custody question, so the thumbnail asks the thing that decides which
        # answer applies to *you* — and the accent lands on "yours", which is
        # the whole argument in one word.
        #
        # **Hand-placed, and this one is worth the note.** `_layout` cannot
        # win on this source: the cascade returns a box running off the top of
        # the original, so the man is already clipped before any crop, and the
        # searched answer zoomed until only half his face was left against the
        # frame edge. `crop_at=(0.0, 0.0)` takes the top-left of the cover
        # crop, which is the one placement that keeps his whole head — and the
        # right half of the frame is the dashboard's dark falloff, which is
        # where the type wanted to be anyway.
        thumb_headline="Your crypto is [not yours]",
        thumb_image=POSTS / "futuristic-crypto-exchange.jpg",
        thumb_accent="red",
        thumb_side="right",
        thumb_crop_at=(0.0, 0.0),
        # **And slid 16% left, with the vacated band faded to black.** A cover
        # crop of a landscape source into 16:9 has no horizontal slack at all,
        # so `crop_at`'s `ax` cannot move a subject sideways — the only lever
        # was zoom, which is what put half his face off frame to begin with.
        # `shift` translates the picture and fades what it uncovers, which is
        # the user's own suggestion: the man is entirely clear on the left and
        # the type gets a real black ground rather than a scrim over the
        # dashboard. Swept 10 / 16 / 22 and looked; 22 crowds him against the
        # edge and 10 still catches "YOUR" on the hologram.
        thumb_shift=0.16,
        endcard=ENDCARD, endcard_lead=7.0,
    )
    for k, v in made.items():
        print(f"{k}: {v}")


if __name__ == "__main__":
    main()
