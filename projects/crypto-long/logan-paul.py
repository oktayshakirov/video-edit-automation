"""What happened to Logan Paul's CryptoZoo - long-form 16:9 for YouTube.

Source: crypto-wiki/content/crypto-ogs/logan-paul.mdx - the CryptoZoo,
buyback and lawsuit sections.

**The angle.** The search ("logan paul cryptozoo") is proven and the
recent standouts are all drama-register commentary on the Coffeezilla feud
(`demand/teardowns/logan-paul-cryptozoo.md`). None explains what the court
actually decided his pitch *was* - puffery - or what the buyback covered.
This does: what CryptoZoo was meant to be, who the refund paid and what it
cost to take it, and why the first round in court went his way while the
case is not over. The video judges claims, never the man: the allegations
are attributed (Coffeezilla, the buyers' suit), the outcomes are the
court's, and nothing is called a scam in our voice.

**A named person and a named scheme**, so the investigative devices from
`projects/crypto.md`: a planted fact (the exact words of the pitch, read
off Wikipedia in the hook) pays off as the thing the judge ruled on; the
buyback's terms are a list, each judged.

**E18: three chapters, ~2:45.**

## The beats

Last three crypto long forms: tokenized-stocks (diagram / compare / quote
/ checklist / post / chart / timeline), random-tokens-in-wallet (diagram /
blindsign / pile / behind / lookalike / post / stat / checklist),
crypto-billionaires (reel / compare / stake / bars / stat).

* `diagram` - how CryptoZoo was meant to work: ZOO, egg, animal, hybrid.
* `pile` with `drain` - eggs and ZOO bought in, the value draining out.
* `checklist` - what the buyback covered, and what taking it cost.
* `behind` - PUFFERY behind Logan Paul: the word the ruling turns on.
* `timeline` - Feb 2023 to Jul 2026, spaced by real time.

**Opener: `Search`** - the title is the search. The last three long forms
opened Split / Stamp / Stamp.

**Real pictures and pages:** Wikipedia's CryptoZoo page captured dark
(`screencap`), the camera ringing "really fun game that makes you money";
CryptoZoo's own egg art (its 2021 site, via the Wayback Machine,
`assets/stock/press/logan-paul/SOURCES.md`); Logan Paul from Wikimedia
Commons (CC BY 2.0, `assets/crypto/logan-paul/CREDITS.md`) with `isolate`
and `behind`.

    PYTHONPATH=. .venv/bin/python projects/crypto-long/logan-paul.py
"""

import sys
from pathlib import Path
from pathlib import Path as _P

from video_automation.core import music, stillclip
from video_automation.core.brand import CRYPTO
from video_automation.core.stock import CACHE as STOCK
from video_automation.crypto.shots import Shot
from video_automation.longform import Meta, Section, render_long
from video_automation.longform.openers import Search

SOURCE_POST = "logan-paul"
DEMAND = ("'logan paul cryptozoo': Coffeezilla 'Investigating Logan Paul's "
          "Biggest Scam' 2.4x (11.5M); Fesify 'Logan Paul Finally Humiliated "
          "Himself In Court' 5.6x (531k, 80 days); Cloutishh 10.2x")
# The cover's style, for the review to compare views and clicks by
# (`thumbnails.md`, "Cover styles are a choice, and every video says which").
COVER_STYLE = "arrow"

V = STOCK / "videos"
ROOT = _P(__file__).resolve().parents[2]
BRAND = ROOT / "assets/brand"
PEOPLE = ROOT / "assets/crypto/logan-paul"
PRESS = STOCK / "press/logan-paul"

# Wikimedia Commons, CC BY 2.0 - see CREDITS.md there.
LOGAN = PEOPLE / "lp-48086760546.jpg"        # 3840x2556, a half smile, looking off frame, a ballpark behind
LOGAN_CAP = PEOPLE / "lp-48086619418.jpg"    # 2948x4024 portrait, cap, looking past the camera
# CryptoZoo's own egg, from its 2021 site (Wayback), padded on its own black.
EGG = PRESS / "cz-egg-wide.jpg"
HERO = PRESS / "cz-hero-wide.jpg"            # the egg beside the CRYPTOZOO wordmark
# Wikipedia's CryptoZoo page, dark, captured 2026-11-11: the camera glides
# from the title to the ringed pitch.
WIKI = STOCK / "captures/wikipedia-cryptozoo/wikipedia-cryptozoo-l.mp4"

# Fetched for this pair 2026-11-11, contact-sheeted, B = the set's luma at
# 0.5/3/6/9s - see the footage.md verdicts.
GAVEL = V / "judge-gavel-courtroom-dark/6699964.mp4"          # 12s, B29-37, a hand lifts a gavel off its block
GAVELDOC = V / "judge-gavel-courtroom-dark/6101337.mp4"       # 8s, B34-35, a gavel beside a document on a desk
COURTHOUSE = V / "courthouse-exterior-night/14994537.mp4"     # 10s, B68-88 (over, used once), a domed courthouse lit at dusk
SIGNING = V / "signing-contract-pen-close-up-dark/8061370.mp4"  # 9s, B78-85 (over, used once), a hand signing papers - the waiver
MIC = V / "podcast-microphone-studio-dark/12315775.mp4"       # 7s, B40-42, a lit podcast studio - a YouTuber's set
REDCHART = V / "red-stock-chart-falling-screen-dark/38698441.mp4"   # 28s, B13, a red chart falling on a monitor
CONTROLLER = V / "video-game-controller-hands-dark/8128022.mp4"     # 8s, B14-16, two hands on a controller in the dark

BEATGROUND = BRAND / "beat-ground-crypto.jpg"
ENDCARD = V / "subscribe/4928934.mp4"

VOICE = "mia"
MUSIC = music.track("night-drift")
URL = "https://thecrypto.wiki/crypto-ogs/logan-paul"

DISCLAIMER_BG = stillclip.path(EGG, focus=(0.5, 0.5))


def _eth(caption: str) -> tuple:
    """The caption keeps ETH; the voice says ether."""
    return (caption, caption.replace("0.1 ETH", "zero point one ether"))


def sections() -> list:
    return [
    # --- hook. No card. ---------------------------------------------------------
    Section(
        title="Logan Paul's CryptoZoo",
        card=False,
        sentences=[
            ("In 2021, Logan Paul sold thousands of people a digital egg.",),
            ("He called the game it belonged to a really fun game that makes you money.",),
            ("The eggs sold out in minutes. The game never arrived.",),
            ("So what happened to CryptoZoo, and to the people who paid for it?",),
            ("Stay to the end for what a court decided those exact words were worth.",),
        ],
        shots=[
            Shot(image=LOGAN, isolate=1.0),
            Shot(clip=WIKI, clip_at=0.0),
            Shot(image=EGG, parallax=0.5),
            Shot(clip=REDCHART, clip_at=12.0),
            None,
        ],
        gaps=[0.70, 0.85, 0.80, 0.70, 0.90],
    ),

    # --- what it was ----------------------------------------------------------------
    Section(
        title="What was CryptoZoo?",
        spoken_title="So what was CryptoZoo, exactly?",
        kicker="THE PITCH",
        sentences=[
            ("A game about collecting animals, where every egg and every animal was an NFT.",),
            ("Here is how it was meant to work.",),
            # the diagram's own sentence: one chunk per box.
            ("You buy the project's own token, called ZOO,",
             "spend it on an egg,",
             "hatch the egg into an animal,",
             "and breed animals into rarer hybrids you can sell."),
            ("On launch day, the third of September 2021, the first ten thousand eggs sold out within minutes.",),
            # the pile's own sentence: two batches in, then the drain.
            ("Buyers paid for eggs,",
             "they bought the ZOO token,",
             "and then the value drained away."),
            ("But the game never became playable, and buyers were left holding eggs with nothing to hatch them into.",),
        ],
        shots=[
            Shot(image=HERO, parallax=0.4),
            None,
            Shot(graphic="diagram", backdrop=BEATGROUND,
                 payload=([("ZOO token", "the project's own coin", "\U0001FA99"),
                           ("An egg", "bought with ZOO", "\U0001F95A"),
                           ("An animal", "hatched from the egg", "\U0001F423"),
                           ("A hybrid", "bred, then sold", "\U0001F984")],
                          "HOW IT WAS MEANT TO WORK", False)),
            Shot(clip=CONTROLLER, clip_at=0.5, note=("10,000", "eggs, sold out in minutes")),
            Shot(graphic="pile", backdrop=BEATGROUND,
                 payload=([(26, "EGGS BOUGHT"), (26, "ZOO BOUGHT")],
                          "WHERE THE MONEY WENT", "THE VALUE DRAINS")),
            Shot(clip=REDCHART, clip_at=1.0),
        ],
        gaps=[0.60, 0.55, 1.40, 0.80, 1.60, 0.90],
    ),

    # --- the buyback ----------------------------------------------------------------
    Section(
        title="Did Logan Paul refund the buyers?",
        spoken_title="So did Logan Paul pay anyone back?",
        kicker="THE BUYBACK",
        sentences=[
            ("Not for more than a year.",),
            ("In December 2022, the YouTuber Coffeezilla published an investigation into the project.",),
            ("Paul first threatened to sue him. Days later he apologised, and said he had hired conmen to build it.",),
            _eth("In January 2024 the buyback finally came: 0.1 ETH for each base egg or base animal."),
            ("So here is who it actually paid.",),
            # the checklist's own sentence: one chunk per row, verdicts as said.
            ("Base eggs, yes.",
             "Base animals, yes.",
             "Hybrid animals, no.",
             "The ZOO token, no.",
             "And the price of taking it: you gave up any claim against him."),
        ],
        shots=[
            Shot(clip=GAVELDOC, clip_at=0.5),
            Shot(clip=MIC, clip_at=0.0),
            Shot(image=LOGAN_CAP, name="Logan Paul"),
            Shot(image=EGG, parallax=0.4),
            Shot(clip=SIGNING, clip_at=1.0),
            Shot(graphic="checklist", backdrop=BEATGROUND,
                 payload=([("Base eggs", True),
                           ("Base animals", True),
                           ("Hybrid animals", False),
                           ("The ZOO token", False),
                           ("Your right to sue him", False)],
                          "WHAT THE BUYBACK PAID FOR", True)),
        ],
        gaps=[0.90, 0.70, 0.85, 0.80, 0.55, 2.40],
    ),

    # --- the ruling and the echo ----------------------------------------------------------
    Section(
        title="Can you sue an influencer over a crypto pitch?",
        spoken_title="So can you sue an influencer over a crypto pitch?",
        kicker="THE RULING",
        card_gap=1.30,
        sentences=[
            ("In October 2025, a federal judge in Texas threw out all twenty-seven claims against him.",),
            # the behind's own sentence: the word, then its line.
            ("The court called the pitch puffery:",
             "sales talk too vague to be a promise."),
            ("Actually, that was round one.",),
            ("Here is the whole fight so far.",),
            # the timeline's own sentence: one chunk per date.
            ("February 2023, the buyers sue Paul and five others.",
             "June 2024, Paul sues Coffeezilla for defamation.",
             "October 2025, the first complaint is dismissed, most of it with leave to try again.",
             "February 2026, a new complaint, and Paul moves to dismiss it too.",
             "July 2026, the Coffeezilla case settles, its terms private."),
            ("A really fun game that makes you money promised nothing, so far, in court.",),
            ("Nothing in this video is financial advice.",),
            ("So the next famous person who pitches you a game that pays: what is that sentence actually promising?",),
        ],
        shots=[
            Shot(clip=GAVEL, clip_at=1.0),
            Shot(graphic="behind",
                 payload=(LOGAN, "PUFFERY", "Too vague to be a promise",
                          "fly", None, False)),
            Shot(clip=COURTHOUSE, clip_at=1.0, shader="aberration"),
            None,
            Shot(graphic="timeline", backdrop=BEATGROUND,
                 payload=([("Feb 2023", "Buyers sue"),
                           ("Jun 2024", "Paul sues Coffeezilla"),
                           ("Oct 2025", "All 27 claims dismissed"),
                           ("Feb 2026", "A new complaint"),
                           ("Jul 2026", "Coffeezilla case settles")],
                          "ROUND ONE, NOT THE END")),
            Shot(clip=WIKI, clip_at=2.0),
            # The video's own subject, not weather (2026-11-06).
            Shot(clip=DISCLAIMER_BG, clip_at=0.5,
                 payload=("", "This is not financial advice.")),
            Shot(image=LOGAN, parallax=0.5),
        ],
        gaps=[0.70, 1.20, 0.85, 0.45, 1.60, 0.90, 1.10, 2.30],
    ),
    ]


SECTIONS = sections()

META = Meta(
    title="What Happened to Logan Paul's CryptoZoo? The Refund and the Ruling",
    hook="In 2021 Logan Paul sold thousands of people a digital egg for a "
         "game he called a really fun game that makes you money. The game "
         "never arrived. Here is how CryptoZoo was meant to work, what the "
         "2024 buyback did and did not cover, and why a court called his "
         "pitch puffery - and why the case is not over.",
    url=URL,
    summary="Logan Paul's CryptoZoo, explained: an NFT game launched on 3 "
            "September 2021 where players bought eggs with the ZOO token, "
            "hatched them into animals and bred hybrids to sell; the first "
            "10,000 eggs sold out in minutes and the game never became "
            "playable. Coffeezilla's December 2022 investigation, Paul's "
            "apology, and the January 2024 buyback at 0.1 ETH per base egg "
            "or base animal, which excluded hybrids and the ZOO token and "
            "required a waiver of claims. The Holland v. CryptoZoo class "
            "action, Judge Alan Albright's October 2025 dismissal of all 27 "
            "claims as puffery with leave to amend, the February 2026 "
            "amended complaint and motion to dismiss, and Paul's defamation "
            "suit against Coffeezilla, settled in July 2026. Nothing here is "
            "financial advice.",
    tags=["logan paul", "cryptozoo", "logan paul cryptozoo", "what happened to cryptozoo",
          "logan paul coffeezilla", "cryptozoo lawsuit", "cryptozoo refund",
          "logan paul lawsuit", "puffery", "nft game", "celebrity crypto",
          "influencer crypto promotion", "crypto scams"],
    cta=f"The full story - Dink Doink, Liquid Marketplace and every date in "
        f"the lawsuits: {URL}",
    credits=["Nothing in this video is financial advice.",
             "Photos of Logan Paul: Erik Drost, via Wikimedia Commons, "
             "CC BY 2.0 - \"Logan Paul (48086760546)\" and \"Logan Paul "
             "(48086619418)\".",
             "CryptoZoo egg art: cryptozoo.co (2021), via the Internet "
             "Archive. Page: Wikipedia, \"CryptoZoo\" (captured 11 Nov 2026)."],
)

HEADLINE = "What\nhappened to\n[CryptoZoo?]"


def _egg(size: int):
    """CryptoZoo's own egg on its own black, the square's edge feathered
    away so no box shows on the cover's black."""
    import numpy as np
    from PIL import Image
    egg = Image.open(PRESS / "cz-og.jpg").convert("RGB").resize((size, size), Image.LANCZOS)
    yy, xx = np.mgrid[0:size, 0:size] / (size - 1) - 0.5
    r = np.sqrt(xx ** 2 + yy ** 2)
    a = np.clip((0.5 - r) / 0.12, 0, 1)
    return egg, Image.fromarray((a * 255).astype("uint8"))


def thumbs(out: Path) -> Path:
    """Logan Paul on the left, ramped into black; CryptoZoo's egg and the
    video's question on the right."""
    import numpy as np
    from PIL import Image
    from video_automation.longform import thumb as T
    src = Image.open(LOGAN).convert("RGB")
    pic = src.resize((1082, 720), Image.LANCZOS)
    im = Image.new("RGB", (1280, 720), (0, 0, 0))
    dx = int(1082 * 0.12)
    im.paste(pic, (-dx, 0))
    x = 1280 - dx - 430
    a = np.zeros((1, 1280), np.float32)
    a[0, x:] = 1.0
    a[0, x - 300:x] = np.linspace(0.0, 1.0, 300)
    mask = Image.fromarray((np.repeat(a, 720, 0) * 255).astype("uint8"))
    im = Image.composite(Image.new("RGB", im.size, (0, 0, 0)), im, mask)
    egg, alpha = _egg(330)
    im.paste(egg, (830, 25), alpha)
    # A ring round the egg and an arrow pointing at it (the editor,
    # 2026-11-11: "use again arrow pointing to the egg"). Red on black.
    red = (235, 45, 45)
    im = im.convert("RGBA")
    im.alpha_composite(T.ring_layer(im.size, (868, 35, 1122, 345), red, 12))
    im.alpha_composite(T.arrow_layer(im.size, (760, 470), (880, 320), red,
                                     width=16, head=46, bow=-0.30))
    im = im.convert("RGB")
    fill, ink = T.ACCENTS["yellow"]
    T._headline(im, HEADLINE, 200, int(560 / 1.38), 720, fill, ink,
                max_lines=3, leading=1.0, band="bottom", margin=40,
                shadow=12, drop=(5, 6))
    im.save(out, quality=92)
    return out


def main() -> None:
    stillclip.make(EGG, focus=(0.5, 0.5))
    out = Path.home() / "Desktop/logan-paul-long.mp4"
    work = Path.home() / "Desktop/.logan-paul-long-work"
    made = render_long(
        SECTIONS, out, work, brand=CRYPTO, meta=META, voice=VOICE,
        music=MUSIC,
        callouts=None,
        opener=Search("what happened to logan paul's cryptozoo"),
        emphasis=["never arrived", "gave up any claim", "round one"],
        thumb_headline=HEADLINE,
        thumb_accent="yellow",
        endcard=ENDCARD, endcard_lead=7.0,
        title_at=11.0, title_hold=5.4,
    )
    made["thumb"] = thumbs(Path(made["thumb"]))
    for k, v in made.items():
        print(f"{k}: {v}")


if __name__ == "__main__":
    if "--thumb" in sys.argv:
        print(thumbs(Path.home() / "Desktop/logan-paul-long-thumb.jpg"))
    else:
        main()
