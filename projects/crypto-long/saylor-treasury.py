"""Michael Saylor — where the money came from. Long-form 16:9 for YouTube.

Source: crypto-wiki/content/crypto-ogs/michael-saylor.mdx (1,379 words). The
62-second short `crypto-saylor-treasury` came from the same article and this
keeps its angle deliberately — a boring software company emptied its bank
account is the strongest line the article has, and inventing a weaker one just
to be different would be a worse video.

**What three minutes buys is depth on the same story.** Three things the short
had to drop and this one is built around:

* **The financing mechanics.** Convertible notes and at-the-market share sales,
  which is the actual answer to the question the short leaves hanging — a
  company that size did not have thirty-five billion dollars in a drawer. This
  is the deep-dive section and it is why the video exists.
* **The rename to Strategy**, and the step down from chief executive in 2022.
* **The honest bear case.** Leverage cuts both ways, the interest is due either
  way, and the shares track one asset now. Reported, not argued.

**No financial advice, and this topic invites it.** A piece about a man who bet
a company on one asset is one sentence away from sounding like a
recommendation. The script reports what the company did and what it cost, and
the close is a question about governance rather than a verdict about Bitcoin —
the same shape the Satoshi script ends on, for the same reason.

**Attribution is mandatory.** Two of the four portraits are CC BY-SA, which
makes this video a derivative work; `assets/crypto/michael-saylor/CREDITS.md`
has the block and `Meta.credits` carries it into the description. The site's own
two Saylor images are 700x348 and 500x472, far under the floor, so the
Wikimedia Commons set is the only usable picture of the man.

**Numbers are as the article states them** — over 531,000 BTC for more than $35
billion, as of mid-April 2025 — so the script says "by twenty twenty-five"
rather than implying a current figure. Holdings move; a dated claim does not go
stale the way an undated one does.

Run from the repo root:

    PYTHONPATH=. .venv/bin/python projects/crypto-long/saylor-treasury.py
"""

from pathlib import Path

from video_automation.core.brand import CRYPTO
from video_automation.core.stock import CACHE as STOCK
from video_automation.crypto.shots import SITE_IMAGES, Shot
from video_automation.longform import Meta, Section, render_long

POSTS = SITE_IMAGES / "posts"
SAYLOR = Path(__file__).resolve().parents[2] / "assets/crypto/michael-saylor"

# Pexels, cached under assets/stock/ and already screened for this palette —
# the trailing comment on each is its luma/saturation from `stock.screen`.
# Supporting layer only: the portraits and the drawn beats carry the argument.
WAVES = STOCK / "videos/abstract-dark-waves-motion"
PARTICLES = STOCK / "videos/dark-abstract-digital-particles"
STREAM = STOCK / "videos/digital-code-stream-dark"
SERVER = STOCK / "videos/server-room-data-center"
CIRCUIT = STOCK / "videos/circuit-board-macro-dark"

ENDCARD = STOCK / "videos/subscribe/4928934.mp4"

VOICE = "mia"                   # female, af_heart. Candidate, not approved.
MUSIC = "pulse"                 # 112 BPM, plucked, no air layer.

URL = "https://thecrypto.wiki/crypto-ogs/michael-saylor"

A = 16 / 9                      # crop toward the frame, not the shorts' 1.15


SECTIONS = [
    # --- the hook, first thirty seconds ---------------------------------
    # No card. Pattern interrupt, hard number, then the promise — in that
    # order, because the steepest drop is between ten and twenty seconds.
    Section(
        title="The purchase",
        card=False,
        sentences=[
            ("In two thousand twenty,",
             "a software company",
             "emptied its bank account."),
            ("Not a startup.",
             "A thirty-one-year-old business",
             "that sold reporting tools to banks."),
            ("It put two hundred and fifty million dollars",
             "into Bitcoin.",
             "Then it never stopped buying."),
            ("Five years later",
             "it had spent more than",
             "thirty-five billion dollars."),
            ("Here is the question",
             "almost nobody asks about it."),
            ("Where did the money come from?",),
            ("Because a company that size",
             "does not have thirty-five billion dollars",
             "sitting in a drawer."),
        ],
        shots=[
            Shot(image=SAYLOR / "saylor-keynote.jpg", zoom=1.09,
                 pan=(0.02, -0.01), aspect=A, bias=0.35),
            None,                                    # ride through the setup
            Shot(graphic="stat",
                 payload=("$250M", "THE FIRST PURCHASE",
                          "August 2020. It was not the last."),
                 backdrop=POSTS / "bitcoin-neon.jpg"),
            None,
            Shot(image=POSTS / "regulators.jpg", zoom=1.11, pan=(-0.02, 0.01),
                 aspect=A, bias=0.45),
            # The title stamp, at about fifteen seconds, on the line that
            # promises the payoff — so it costs none of the opening five.
            Shot(clip=STREAM / "34127877.mp4",       # L14 S6
                 payload=("", "WHERE DID THE MONEY COME FROM?")),
            Shot(image=POSTS / "security-combination-lock.jpg", zoom=1.10,
                 pan=(0.02, 0.01), aspect=A, bias=0.5),
        ],
    ),

    # --- reframe: why a software company does this at all ----------------
    Section(
        title="Why would a software company do this?",
        sentences=[
            ("Michael Saylor co-founded MicroStrategy",
             "in nineteen eighty-nine."),
            ("Business intelligence software.",
             "Dashboards and reports.",
             "It went public in ninety-eight",
             "and nothing about it was exciting."),
            ("Then he looked at the cash",
             "sitting on the balance sheet",
             "and asked a simple question:",
             "what will this buy in ten years?"),
            ("His answer was: less.",),
            ("Every company with idle cash",
             "has roughly the same four options,",
             "and every treasurer knows them."),
            # One caption per item — that is what times the reveals. Two-phase
            # (no `flow`), because the narration only lists; the verdict lands
            # into the 2.4s pause after it.
            ("Leave it in the bank.",
             "Buy back your own stock.",
             "Park it in government bonds.",
             "Or buy Bitcoin with it."),
            ("He picked the last one,",
             "out loud, in public,",
             "with the shareholders watching."),
        ],
        shots=[
            Shot(image=SAYLOR / "saylor-portrait.jpg", zoom=1.10,
                 pan=(0.02, -0.01), aspect=A, bias=0.3),
            Shot(image=POSTS / "man-and-laptop.jpg", zoom=1.11,
                 pan=(-0.02, 0.01), aspect=A, bias=0.45),
            Shot(image=POSTS / "bitcoin-vs-fiat.jpg", zoom=1.12,
                 pan=(0.02, 0.01), aspect=A, bias=0.45),
            None,
            Shot(clip=SERVER / "7140928.mp4",        # L29 S43
                 payload=("", "Idle cash has four homes")),
            Shot(graphic="checklist",
                 payload=([("Leave it in the bank", False),
                           ("Buy back stock", False),
                           ("Park it in bonds", False),
                           ("Buy Bitcoin", True)],
                          "CORPORATE CASH, 2020"),
                 picture=POSTS / "gold.jpg"),
            Shot(image=SAYLOR / "saylor-speaking.jpg", zoom=1.11,
                 pan=(0.02, -0.01), aspect=A, bias=0.35),
        ],
        # The checklist needs its pause: the four options sit on screen
        # unmarked, the voice stops, and the verdicts land into the silence.
        gaps=[0.34, 0.34, 0.34, 0.34, 0.34, 2.40, 0.34],
    ),

    # --- the deep dive: the financing. This is the video. ----------------
    Section(
        title="So where did the money come from?",
        sentences=[
            ("The software business",
             "was profitable, and small.",
             "Its profits went in too,",
             "but they were never the engine."),
            ("The engine was the capital markets.",),
            ("There are two ways",
             "a public company raises money",
             "it does not have,",
             "and Strategy used both, repeatedly."),
            # One caption per item, in column order, no lead-in sentence inside
            # the beat's span — a spare sentence in front eats reveal zero.
            ("Bonds that can convert into shares.",
             "Cash today, dilution later.",
             "Interest due whatever Bitcoin does.",
             "New shares sold straight into the market.",
             "Every existing holder owns a little less.",
             "Nothing to repay, and no way back."),
            ("Borrow, buy coins.",
             "Issue shares, buy coins.",
             "Repeat that for five years."),
            ("By twenty twenty-five",
             "the company held over",
             "five hundred and thirty thousand coins."),
            ("That is the largest corporate stack on earth,",
             "and about one coin in forty",
             "that will ever exist."),
        ],
        shots=[
            Shot(image=POSTS / "digital-technology.jpg", zoom=1.10, pan=(0.02, 0.01),
                 aspect=A, bias=0.45),
            Shot(image=POSTS / "htx-dashboard.jpg", zoom=1.11,
                 pan=(-0.02, -0.01), aspect=A, bias=0.4),
            None,
            Shot(graphic="compare",
                 payload=("Convertible debt",
                          ["Bonds that turn into shares",
                           "Cash now, dilution later",
                           "Interest due either way"],
                          "New share sales",
                          ["Sold into the market at will",
                           "Every holder owns less",
                           "Nothing to repay, no way back"]),
                 backdrop=POSTS / "futuristic-crypto-exchange.jpg"),
            Shot(clip=CIRCUIT / "6755170.mp4",       # L41 S20
                 payload=("", "Borrow. Buy. Repeat.")),
            Shot(image=POSTS / "bitcoin.jpg", zoom=1.11, pan=(0.02, -0.01),
                 aspect=A, bias=0.5),
            # A proportion is the one thing a spoken number cannot convey.
            # "531,000 coins" means nothing until it is drawn against 21M.
            Shot(graphic="bars",
                 payload=([("Held by Strategy, 2025", 0.025, "531K"),
                           ("Bitcoin that will ever exist", 1.0, "21M")],
                          "THE SIZE OF THE STACK"),
                 backdrop=POSTS / "proof-of-work.jpg"),
        ],
    ),

    # --- the twist: what the company became ------------------------------
    # `flow=True`. The narration says each verdict itself, so the mark lands on
    # the word rather than four seconds behind it.
    Section(
        title="What is the company now?",
        sentences=[
            ("In twenty twenty-two",
             "he stepped down as chief executive",
             "to work on the Bitcoin strategy full time."),
            ("In twenty twenty-five",
             "the company dropped the MicroStrategy name",
             "and simply called itself Strategy."),
            ("Which is honest, in a way.",
             "Look at what it actually is now."),
            ("It is barely a software business.",
             "It is not a safe cash cushion.",
             "It is a leveraged bet on one asset."),
            ("And the stock became something else too —",
             "a way to hold Bitcoin",
             "inside an ordinary brokerage account,",
             "years before the spot funds existed."),
        ],
        shots=[
            Shot(image=SAYLOR / "saylor-stage.jpg", zoom=1.10, pan=(0.02, 0.01),
                 aspect=A, bias=0.5),
            Shot(image=POSTS / "futuristic-ui.jpg", zoom=1.12, pan=(-0.02, -0.01),
                 aspect=A, bias=0.4),
            None,
            Shot(graphic="checklist",
                 payload=([("A software business", False),
                           ("A cash cushion", False),
                           ("A leveraged Bitcoin bet", True)],
                          "WHAT IT IS NOW",
                          True),                     # flow
                 picture=POSTS / "analysis.jpg"),
            Shot(image=POSTS / "laptop-trading.jpg", zoom=1.11,
                 pan=(0.02, -0.01), aspect=A, bias=0.45),
        ],
    ),

    # --- the honest part. A statement card: it resolves, it does not ask. --
    Section(
        title="Leverage cuts both ways",
        spoken_title="But leverage cuts both ways.",
        sentences=[
            ("That is not a criticism.",
             "It is arithmetic."),
            ("A bet funded with borrowed money",
             "gains faster on the way up",
             "and loses faster on the way down."),
            ("The interest is due",
             "whether the price cooperates or not."),
            ("So the shares moved",
             "almost exactly with Bitcoin,",
             "only harder in both directions."),
            ("Analysts stopped calling it",
             "a software company years ago.",
             "Some call it a Bitcoin fund",
             "with a reporting tool attached."),
        ],
        shots=[
            Shot(clip=WAVES / "27980029.mp4",        # L4 S5
                 payload=("", "Not a criticism. Arithmetic.")),
            Shot(image=POSTS / "portfolio.jpg", zoom=1.11, pan=(-0.02, 0.01),
                 aspect=A, bias=0.45),
            None,
            Shot(graphic="quote",
                 payload=("The debt does not care about the price.",
                          "how leverage actually works"),
                 # Not `one-coin.jpg`, which is OneCoin — Ruja Ignatova's fraud,
                 # nothing to do with Saylor, and putting it beside him is an
                 # accusation the script never makes. A price screen instead:
                 # the quote is about a debt that ignores the price.
                 picture=POSTS / "htx-dashboard.jpg"),
            Shot(image=POSTS / "analysis.jpg", zoom=1.10, pan=(0.02, -0.01),
                 aspect=A, bias=0.5),
        ],
    ),

    # --- mirror: the viewer in the room ----------------------------------
    Section(
        title="Would you have signed it off?",
        sentences=[
            ("Put yourself in that boardroom",
             "in twenty twenty."),
            ("You hold cash",
             "that is quietly losing value.",
             "You have a board to answer to.",
             "And one option on the list",
             "has no corporate track record at all."),
            ("That is the part",
             "Saylor's influence actually rests on."),
            ("Not the purchase itself.",
             "Making the purchase",
             "something another executive",
             "could point at and survive."),
            ("Tesla did it.",
             "Block did it.",
             "Dozens of smaller companies followed the blueprint."),
        ],
        shots=[
            Shot(image=POSTS / "regulators.jpg", zoom=1.11, pan=(0.02, 0.01),
                 aspect=A, bias=0.35),
            Shot(image=POSTS / "law.jpg", zoom=1.12,
                 pan=(-0.02, 0.01), aspect=A, bias=0.45),
            None,
            Shot(image=SAYLOR / "saylor-speaking.jpg", zoom=1.12,
                 pan=(0.02, -0.01), aspect=A, bias=0.4),
            Shot(image=POSTS / "tesla.jpg", zoom=1.11, pan=(-0.02, -0.01),
                 aspect=A, bias=0.45),
        ],
    ),

    # --- echo, and the ask ------------------------------------------------
    Section(
        title="A blueprint, or a warning?",
        spoken_title="So is it a blueprint, or a warning?",
        sentences=[
            ("Back to that software company",
             "emptying its bank account."),
            ("The interesting question",
             "was never whether he was right.",
             "Bitcoin's price will answer that",
             "without any help from you."),
            ("The question is whether a public company",
             "should be able to borrow billions",
             "to make one concentrated bet",
             "with other people's money."),
            ("What would you have voted?",),
            ("Nothing here is advice —",
             "the full breakdown and the sources",
             "are linked below."),
            ("If that was useful,",
             "subscribe for more videos like this one."),
        ],
        shots=[
            Shot(image=SAYLOR / "saylor-keynote.jpg", zoom=1.12,
                 pan=(-0.02, 0.01), aspect=A, bias=0.3),
            Shot(clip=PARTICLES / "36703282.mp4"),   # L9 S0
            Shot(image=SAYLOR / "saylor-portrait.jpg", zoom=1.13,
                 pan=(0.02, 0.01), aspect=A, bias=0.25),
            Shot(graphic="stat",
                 payload=("531,000", "COINS, ONE COMPANY",
                          "Bought with borrowed money."),
                 backdrop=POSTS / "bitcoin-neon.jpg"),
            Shot(image=POSTS / "global-map.jpg", zoom=1.10,
                 pan=(-0.02, -0.01), aspect=A, bias=0.5),
            # Held on the abstract, so YouTube's end-screen cards have
            # somewhere uncluttered to sit when they go on at upload.
            Shot(clip=WAVES / "15690300.mp4"),       # L9 S0
        ],
        # 2.40 after the question the whole video builds to — the beat that
        # carries it would otherwise be gone in under two seconds.
        gaps=[0.34, 0.34, 0.34, 2.40, 0.34, 3.20],
    ),
]

META = Meta(
    title="How One Software Company Bought $35 Billion of Bitcoin",
    hook="In 2020 a boring software company emptied its bank account and bought "
         "Bitcoin. Here is where the money actually came from.",
    url=URL,
    summary="Michael Saylor turned MicroStrategy into the largest corporate "
            "Bitcoin holder on earth. How the purchases were financed, what the "
            "company became, and the risk that comes with it.",
    tags=["michael saylor", "bitcoin", "microstrategy", "strategy",
          "corporate treasury"],
    cta=f"Full profile, quick facts and sources: {URL}",
    credits=["Photographs of Michael Saylor by Gage Skidmore (CC BY-SA 3.0 / "
             "CC BY-SA 2.0) and MicroStrategy (CC BY 2.0), via Wikimedia "
             "Commons. This video is shared under CC BY-SA 4.0.",
             "Additional footage: Pexels (Pexels licence, no attribution "
             "required).",
             "Music: generated for this channel.",
             "Nothing in this video is financial advice."],
)


def main() -> None:
    out = Path.home() / "Desktop/crypto-saylor-treasury-long.mp4"
    work = Path.home() / "Desktop/.crypto-saylor-long-work"
    made = render_long(
        SECTIONS, out, work, brand=CRYPTO, meta=META, voice=VOICE,
        music=MUSIC,
        callouts=None,
        # The title carries the search phrase, so the thumbnail asks what the
        # title does not.
        #
        # **The source is the user's call, against the scorer.** `_layout` puts
        # keynote at -0.02 and stage at -0.01 clean, and this one at +0.91
        # busy — but keynote is Saylor twenty years ago and the thumbnail is a
        # promise about who the video is about. The +0.91 is the CPAC backdrop's
        # star and lettering, which is texture the scorer counts and the eye
        # reads as a flat blue field; at feed size the type sits clean.
        # `side="left"` because the search puts the block top-right, over his
        # head. An override, and recorded as one.
        thumb_headline="[Where] did the money come from?",
        thumb_image=SAYLOR / "saylor-speaking.jpg",
        thumb_accent="yellow",
        thumb_side="left",
        endcard=ENDCARD, endcard_lead=7.0,
    )
    for k, v in made.items():
        print(f"{k}: {v}")


if __name__ == "__main__":
    main()
