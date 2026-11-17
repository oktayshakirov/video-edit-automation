"""Is the US using stablecoins to reset its debt? - long-form 16:9 for YouTube.

Source: crypto-wiki/content/posts/what-is-the-genius-act.mdx - its interest
ban ("The Ban on Paying Interest"), who may issue, and the timeline - with
the reserve mechanism from `what-are-stablecoins`.

**The angle (2026-11-16, the editor's call: "cover the rumours ... the
conspiracy side of it to gain viewers interest ... we need to
experiment").** The title is the rumour, as people type it: the stablecoin
"debt reset", proven on three channels - Clearly Finance 39.2x, Swan
Bitcoin 31.5x, Noel Lorenzana's debunk 10.5x
(`demand/teardowns/stablecoin-debt-reset.md`). The mechanism under a plain
title found nobody ("Your Stablecoin Earns Interest. Just Not for You", 1
view). So the rumour is the search and the mechanism is the answer: follow
one dollar, and the true part (stablecoins fund the debt, the issuer keeps
the interest, the coins can be frozen) is checked against the false one (it
erases the debt). Verdicts judge claims, never an asset; no direction, no
"what to buy" - the standouts' hard-asset sections are closed to us.

**A list of claims checked, so the arc ends on a `checklist`** (Lorenzana's
shape, `projects/crypto.md`, "Evidence in a list"). Three chapters (E18).

**Every figure is sourced.** Debt $40.62T: US Treasury, Debt to the Penny,
13 Nov 2026. All stablecoins $287.1B: DefiLlama, 16 Nov 2026. Tether's
Treasury bills $122.8B: its Q3 2026 attestation (BDO, 30 Sep 2026). Circle:
FY2025 results, reserve income $2,637M of $2,747M revenue (96%). The ban:
GENIUS Act (Public Law 119-27) Sec. 4(a)(11), "any form of interest or
yield"; effective the earlier of 18 months after enactment (18 Jan 2027) or
120 days after final rules (Sec. 20); OCC final rule 21 Oct 2026 keeps it.
Freeze: Sec. 4(a)(6)(B) and Sec. 2(16)(A) ("seize, freeze, burn, or
prevent the transfer"); Tether 9,597 addresses, $5.69B frozen by 26 Jul
2026 (BlockSec). Wyoming FRNT: public sale 7 Jan 2026; "interest income
beyond the 102% reserve is transferred to the school foundation program"
(the Commission's factbook). Kyrgyzstan KGST: Dec 2025. The adviser:
Anton Kobyakov, Eastern Economic Forum press briefing, 8 Sep 2025, as
reported by Cointelegraph (via RussiaDirect). Bessent: has said
stablecoins could drive trillions in Treasury demand.

## The picture (planned per sentence before any footage, `workflow.md`)

* `reserve` (new) - the dollar in, a token back, the dollar lent to a
  Treasury bill, the interest streaming to the issuer, the line to you
  blocked at $0. The one mechanism the pair is about.
* `post` - the adviser's own words, "crypto cloud" highlighted.
* `grid` - the three things to check, set as the promise.
* `stat` - Circle's 96%.
* `bars` - the debt against every stablecoin there is.
* the Treasury Secretary's official portrait, whole and named, in a window.
* `timeline` - July 2025 to January 2027.
* `checklist` - the claims, judged.
* Pages: the law's own text captured (govinfo), the interest line and the
  freeze line ringed, in browser windows; Wyoming's stable-token page.
* Clips: the Capitol, the Treasury building, dollars into a counter, hands
  paying on a phone. No `pile` (Logan Paul's pair), no `breach` /
  `blindsign` (the hardware wallet's).

**Opener: `Search`**, the title as typed. Last two long forms opened
`Stamp`; the editor prefers `Search` when the title is a search.

    PYTHONPATH=. .venv/bin/python projects/crypto-long/stablecoin-interest.py
"""

import sys
from pathlib import Path
from pathlib import Path as _P

from video_automation.core import music
from video_automation.core.brand import CRYPTO
from video_automation.core.stock import CACHE as STOCK
from video_automation.crypto.shots import Shot

from video_automation.longform import Meta, Section, render_long
from video_automation.longform.openers import Search

SOURCE_POST = "what-is-the-genius-act"
DEMAND = ("Clearly Finance 'Is the US Planning a $37 Trillion Crypto Debt "
          "Reset?' 39.2x (216k); Swan Bitcoin 'Is the U.S. Using Stablecoins "
          "to Reset $35T Debt?' 31.5x (305k); Noel Lorenzana debunk 10.5x")
# The cover's style (`thumbnails.md`, "Cover styles are a choice").
COVER_STYLE = "cutout"

V = STOCK / "videos"
CAP = STOCK / "captures"
ROOT = _P(__file__).resolve().parents[2]
BRAND = ROOT / "assets/brand"
SI = ROOT / "assets/crypto/stablecoin-interest"

# Fetched for this pair (2026-11-16), sheeted at 15/50/85% with luma, and
# checked by Pexels id against every script (300 either side).
CAPITOL_MOODY = V / "washington-dc-capitol-dome-aerial/29188237.mp4"    # 20s, the dome behind bare trees, grey sky
CAPITOL_STREET = V / "us-capitol-building-night/6581274.mp4"           # 30s, a street toward the Capitol at dusk (windowed)
CAPITOL_FLAG = V / "us-capitol-building-night/6854091.mp4"             # 30s, the dome and the flag, blue sky
CAPITOL_LAWN = V / "washington-dc-capitol-dome-aerial/4961476.mp4"      # 24s, the Capitol across the lawn
TREASURY = V / "us-treasury-department-building/29188210.mp4"           # 17s, the Treasury building's columns
TREASURY_SIDE = V / "us-treasury-department-building/29188217.mp4"      # 15s, the Treasury from the street
DOLLARS = V / "dollar-bills-money-counter-machine/5909916.mp4"          # 22s, a hand feeds US dollars into a counter
PHONE_CARD = V / "man-using-phone-banking-app-at-night/7535099.mp4"     # 9s, hands, a phone and a card
PHONE_MAN = V / "man-using-phone-banking-app-at-night/7567651.mp4"      # 15s, a man paying on his phone, card in hand

# The real pages (`screencap`, records in `captures/<name>/`).
LAW_YIELD = CAP / "genius-act/yield.mp4"       # Sec. 4(a)(11), "any form of interest or" ringed
LAW_FREEZE = CAP / "genius-act/freeze.mp4"     # Sec. 2(16)(A), "seize, freeze, burn, or" ringed
LAW_ADDR = "govinfo.gov - GENIUS Act, Public Law 119-27"
WYOMING = CAP / "wyoming-frnt/first.mp4"       # "...issued by a U.S. public entity" ringed
WYOMING_ADDR = "stabletoken.wyo.gov"

BESSENT = SI / "bessent.jpg"                   # official portrait, public domain (CREDITS.md)
# cropped to 16:9 with the whole head in it - a window centre-crops a
# portrait and took his forehead off (2026-11-17)
BESSENT_WIDE = SI / "bessent-wide.jpg"

BEATGROUND = BRAND / "beat-ground-crypto.jpg"
ENDCARD = V / "subscribe/4928934.mp4"

VOICE = "mia"
MUSIC = music.track("night-drift")
URL = "https://thecrypto.wiki/posts/what-is-the-genius-act"


def sections() -> list:
    return [
    # --- hook. No card. The Search types the title. ----------------------------
    Section(
        title="Is the US using stablecoins to reset its debt?",
        card=False,
        sentences=[
            ("The rumour says America will hide its forty trillion dollar debt inside stablecoins, and quietly wipe it out.",),
            ("Stablecoins really do hold that debt.",),
            ("But they don't erase a cent of it. They earn interest on it, and you get none.",),
            # the post's own sentence: the lead-in, then the quoted words.
            ("In September 2025, a Putin adviser said America would solve its debt",
             "by pushing everyone into the crypto cloud."),
            # the grid's own sentence: one chunk per card.
            ("So follow one stablecoin dollar, and check three things: does it erase the debt,",
             "who keeps the interest,",
             "and who can freeze it?"),
        ],
        shots=[
            Shot(clip=CAPITOL_MOODY, clip_at=2.0),
            # the figure seen as it is said, on the building that borrows it
            Shot(clip=TREASURY_SIDE, clip_at=1.0,
                 note=("$122.8B", "US Treasury bills held by Tether, Sep 2026")),
            Shot(clip=PHONE_CARD, clip_at=0.5),
            Shot(graphic="post", backdrop=BEATGROUND,
                 payload=("post",
                          {"name": "Anton Kobyakov", "handle": "adviser to Vladimir Putin",
                           "date": "8 Sep 2025, Eastern Economic Forum",
                           "text": "As in the 1930s and the 1970s, the US plans to "
                                   "solve its financial problems at the world's "
                                   "expense - this time by [pushing everyone into "
                                   "the 'crypto cloud.']"},
                          "THE RUMOUR")),
            Shot(graphic="grid", ground="grid",
                 payload=([("Erase the debt?", "the rumour", "\U0001F4B8"),
                           ("Who keeps the interest?", "the business", "\U0001F4B0"),
                           ("Who can freeze it?", "the fear", "\U0001F512")],
                          "THREE THINGS TO CHECK")),
        ],
        gaps=[0.70, 0.55, 0.90, 1.00, 0.90],
    ),

    # --- where the dollar goes -------------------------------------------------
    Section(
        title="Where does a stablecoin dollar go?",
        spoken_title="So where does a stablecoin dollar actually go?",
        kicker="THE RESERVE",
        sentences=[
            # the reserve's own sentence: deposit, loan, interest, yours.
            ("You hand an issuer like Tether or Circle a dollar, and get one token back.",
             "They lend that dollar to the US government, by buying a Treasury bill.",
             "The bill pays interest, and the issuer keeps it.",
             "Your share is zero."),
            ("That's not a side effect. It's the business.",),
            ("In 2025, ninety-six percent of Circle's revenue was interest on its reserves, about two point six billion dollars.",),
            ("And a law now makes sure you never get a share.",),
            ("The GENIUS Act bans issuers from paying holders any form of interest or yield, from January 2027.",),
        ],
        shots=[
            Shot(graphic="reserve", ground="grid",
                 payload=(("YOU", "hand over a dollar"),
                          ("THE ISSUER", "Tether, Circle"),
                          ("US TREASURY BILL", "93 days or less"),
                          "KEEPS THE INTEREST", "$0", "BANNED BY LAW",
                          "WHERE THE INTEREST GOES")),
            None,
            Shot(graphic="stat", backdrop=BEATGROUND,
                 payload=("96%", "of Circle's 2025 revenue was interest on reserves",
                          "$2.64B - Circle, FY2025 results")),
            Shot(clip=DOLLARS, clip_at=2.0),
            Shot(clip=LAW_YIELD, clip_at=0.0, window=("browser", LAW_ADDR)),
        ],
        gaps=[1.40, 0.70, 0.80, 0.50, 0.90],
    ),

    # --- the rumour, checked -----------------------------------------------------
    Section(
        title="Can stablecoins erase the debt?",
        spoken_title="So can stablecoins really erase America's debt?",
        kicker="THE RUMOUR",
        card_gap=1.30,
        sentences=[
            ("Actually, buying a Treasury bill is lending, not erasing.",),
            ("Within ninety-three days, the government pays the dollar back, with interest.",),
            # the bars' own sentence: one chunk per row.
            ("The debt is over forty trillion dollars.",
             "Every stablecoin in existence adds up to about two hundred and eighty-seven billion."),
            ("Less than one percent, even if every token sat in Treasury bills.",),
            ("What is true: the US Treasury Secretary wants stablecoins as big new buyers of those bills.",),
            ("So stablecoins don't shrink the debt. They help the government keep borrowing.",),
            ("And if the dollar ever lost value, a dollar token would lose exactly the same.",),
        ],
        shots=[
            Shot(clip=TREASURY, clip_at=1.0, shader="aberration"),
            None,
            Shot(graphic="bars", ground="grid",
                 payload=([("US debt", 1.0, "$40.6T"),
                           ("Every stablecoin", 287.1 / 40617, "$287B")],
                          "THE DEBT AGAINST EVERY STABLECOIN")),
            None,
            # Shown whole, with his name (`footage.md`, 2026-11-04); a
            # spotlight ring on a portrait left no room for its label.
            Shot(image=BESSENT_WIDE, zoom=1.03,
                 window=("player", "Scott Bessent, US Treasury Secretary")),
            Shot(clip=CAPITOL_FLAG, clip_at=4.0),
            None,
        ],
        gaps=[0.60, 0.80, 1.20, 0.80, 0.70, 0.60, 0.90],
    ),

    # --- governments, and the switch ---------------------------------------------
    Section(
        title="Are governments taking stablecoins over?",
        spoken_title="So are governments taking stablecoins over?",
        kicker="THE SWITCH",
        sentences=[
            # the timeline's own sentence: one chunk per date.
            ("In July 2025, the US passed the GENIUS Act.",
             "In December, Kyrgyzstan launched a national stablecoin.",
             "In January 2026, Wyoming put its own stable token on sale.",
             "And in January 2027, the US rules take effect."),
            ("Wyoming keeps the interest too. It goes to the state's schools, not to holders.",),
            ("But one fear is real: every licensed stablecoin can be frozen.",),
            ("The law requires issuers to be able to seize, freeze or burn tokens on a lawful order.",),
            ("By July 2026, Tether had frozen about five point seven billion dollars, across nine thousand six hundred addresses.",),
            ("So a stablecoin isn't a government currency. It's a dollar with an off switch.",),
            # the checklist's own sentence: one chunk per claim.
            ("Does it erase the debt?",
             "Does it fund it?",
             "Is the interest yours?",
             "Can it be frozen?"),
            ("Nothing in this video is financial advice.",),
            ("So the debt isn't going anywhere. Who do you think should get the interest on your dollar?",),
        ],
        shots=[
            Shot(graphic="timeline", ground="grid",
                 payload=([("Jul 2025", "GENIUS Act signed"),
                           ("Dec 2025", "Kyrgyzstan's KGST"),
                           ("Jan 2026", "Wyoming's FRNT on sale"),
                           ("Jan 2027", "US rules take effect")],
                          "WHO ISSUES THEM")),
            Shot(clip=WYOMING, clip_at=0.0, window=("browser", WYOMING_ADDR)),
            Shot(clip=PHONE_MAN, clip_at=2.0),
            Shot(clip=LAW_FREEZE, clip_at=0.0, window=("browser", LAW_ADDR)),
            Shot(clip=CAPITOL_LAWN, clip_at=3.0,
                 note=("$5.69B", "frozen by Tether, 9,597 addresses, by Jul 2026")),
            Shot(clip=CAPITOL_STREET, clip_at=6.0,
                 window=("player", "The US Capitol, Washington")),
            Shot(graphic="checklist", backdrop=BEATGROUND,
                 payload=([("Erases the debt", False),
                           ("Funds the debt", True),
                           ("Pays you the interest", False),
                           ("Can be frozen", True)],
                          "THE RUMOUR, CHECKED")),
            # The video's own subject, not weather (2026-11-06).
            Shot(clip=TREASURY_SIDE, clip_at=8.0,
                 payload=("", "This is not financial advice.")),
            Shot(clip=CAPITOL_MOODY, clip_at=10.0),
        ],
        gaps=[1.20, 0.80, 0.60, 0.60, 0.80, 0.90, 2.40, 1.10, 2.30],
    ),
    ]


SECTIONS = sections()

META = Meta(
    title="Is the US Using Stablecoins to Reset Its Debt?",
    hook="The rumour says America will hide its $40 trillion debt inside "
         "stablecoins and wipe it out. Stablecoins really do hold that debt - "
         "but they don't erase a cent of it. Follow one stablecoin dollar: "
         "where it goes, who keeps the interest, and who can freeze it.",
    url=URL,
    summary="Is the US using stablecoins to reset its debt? The rumour, from a "
            "Putin adviser in September 2025, checked against how a stablecoin "
            "actually works: your dollar is lent to the US government through a "
            "Treasury bill, the bill pays interest, and the issuer keeps it - "
            "96% of Circle's 2025 revenue - while the GENIUS Act bans paying "
            "holders any interest or yield from January 2027. Buying a bill is "
            "lending, not erasing: every stablecoin together ($287B) is under 1% "
            "of the $40.6T debt. What is true: stablecoins fund the debt, "
            "governments have started issuing their own (Wyoming, Kyrgyzstan), "
            "and every licensed stablecoin can be frozen - Tether had frozen "
            "$5.69B by July 2026. Nothing here is financial advice.",
    tags=["stablecoin debt reset", "is the us using stablecoins to reset its debt",
          "us debt stablecoins", "genius act", "genius act explained",
          "stablecoin interest", "how do stablecoin issuers make money",
          "stablecoins explained", "crypto debt reset", "tether treasury bills",
          "stablecoin yield ban", "can stablecoins be frozen", "wyoming stablecoin",
          "crypto cloud"],
    cta=f"The whole law in plain English - who may issue a stablecoin, the "
        f"interest ban, the timeline and what to watch: {URL}",
    credits=["Nothing in this video is financial advice.",
             "Pages: GENIUS Act, Public Law 119-27 (govinfo.gov); Wyoming Stable "
             "Token Commission (stabletoken.wyo.gov), captured 16 Nov 2026.",
             "Quote: Anton Kobyakov, Eastern Economic Forum press briefing, 8 Sep "
             "2025, as reported by Cointelegraph via RussiaDirect.",
             "Figures: US Treasury, Debt to the Penny (13 Nov 2026); DefiLlama "
             "stablecoin supply (16 Nov 2026); Tether Q3 2026 attestation (BDO); "
             "Circle FY2025 results; BlockSec (26 Jul 2026); Wyoming Stable "
             "Token Commission factbook.",
             "Photos: Official portrait of Treasury Secretary Scott Bessent, and "
             "Scott Bessent 2025 Official Portrait (the thumbnail), US Department "
             "of the Treasury, public domain (Wikimedia Commons)."],
)

HEADLINE = "Debt hidden in\n[stablecoins?]"

# Covers (`thumbnails.md`, 2026-11-13: no style three videos running - the
# arrow ran on the last three). The search's top covers (12, pulled
# 2026-11-16) all cut out a real official - Bessent, Trump, Putin - beside
# a presenter, with a gold coin and the claim in huge caps. We have no
# presenter. Two directions were drawn, both formats; the editor picked the
# cutout (2026-11-17) and the other was deleted:
#
#   "cutout" - the Treasury Secretary's other official portrait, cut out,
#              on a gold-lit ground, $40T as extruded gold type, the
#              question in two rows. True: he does want stablecoins to buy
#              the debt; the question is the rumour's, which the video
#              answers.
#   "beat"   - (deleted) the `reserve` beat's last frame under "Where's
#              your interest?".
#
# The cover's pictures are none of the video's shots (the spotlight uses
# the other portrait).
BESSENT_COVER = SI / "bessent-cover.jpg"
COVERS = ("cutout",)


def _cut(src):
    import numpy as np
    from PIL import Image
    from video_automation.core import vision
    im = Image.open(src).convert("RGB")
    im.thumbnail((1800, 1800))
    a = np.asarray(vision.cutout(im)).copy()
    c = Image.fromarray(a)
    return c.crop(c.getchannel("A").point(lambda v: 255 if v > 24 else 0).getbbox())


def _radial(size, centre, inner, outer, r):
    import numpy as np
    from PIL import Image
    w, h = size
    yy, xx = np.mgrid[0:h, 0:w].astype(np.float32)
    k = np.clip(np.sqrt((xx - centre[0]) ** 2 + (yy - centre[1]) ** 2) / r, 0, 1)[:, :, None]
    arr = np.array(inner, np.float32) * (1 - k) + np.array(outer, np.float32) * k
    return Image.fromarray(arr.astype(np.uint8)).convert("RGBA")


def cover(kind: str, portrait: bool = False):
    """One cover, 1280x720 or (`portrait`) 1080x1920, as an RGB image."""
    from PIL import Image
    from video_automation.longform import thumb as T
    W, H = (1080, 1920) if portrait else (1280, 720)
    gold, deep = (255, 199, 0), (120, 80, 0)
    fill, ink = T.ACCENTS["yellow"]
    if kind == "cutout":
        man = _cut(BESSENT_COVER)
        if portrait:
            im = _radial((W, H), (560, 1250), (96, 70, 8), (8, 7, 4), 1150)
            im.alpha_composite(T.extrude_text((W, H), "$40T", (90, 560), 300,
                               face=gold, side=deep, depth=24, direction=(0.7, 1.0)))
            h = 1000
            c = man.resize((int(man.width * h / man.height), h), Image.LANCZOS)
            im.alpha_composite(c, ((W - c.width) // 2, H - h))
            im = im.convert("RGB")
            T._headline(im, HEADLINE, 200, W - 120, 60, fill, ink, max_lines=2,
                        max_block=H * 0.22, leading=1.02, band="top",
                        margin=int(H * 0.10), shadow=14, drop=(6, 8))
            return im
        im = _radial((W, H), (900, 300), (96, 70, 8), (8, 7, 4), 900)
        im.alpha_composite(T.extrude_text((W, H), "$40T", (40, 60), 230,
                           face=gold, side=deep, depth=20, direction=(0.7, 1.0)))
        h = 700
        c = man.resize((int(man.width * h / man.height), h), Image.LANCZOS)
        im.alpha_composite(c, (W - c.width + 40, H - h + 20))
        im = im.convert("RGB")
        T._headline(im, HEADLINE, 150, int(600 / 1.38), 48, fill, ink,
                    max_lines=2, leading=1.0, band="bottom", margin=44,
                    shadow=12, drop=(5, 6))
        return im
    raise ValueError(f"unknown cover {kind!r} - {COVERS}")


def thumbs(out: Path, portrait: bool = False, variants: bool = False) -> list[Path]:
    """The picked cover (the first of COVERS) at `out`, and nothing else.

    `variants=True` (`--thumb-variants`) also writes every *other* direction
    as `-<style>` beside it, for choosing. The pick is never written twice:
    a `-cutout` copy of `-thumb` is the duplicate the editor found on the
    Desktop after two runs (`thumbnails.md`, 2026-11-17)."""
    cover(COVERS[0], portrait).save(out, quality=92)
    made = [out]
    if variants:
        for k in COVERS[1:]:
            p = out.with_name(f"{out.stem}-{k}{out.suffix}")
            cover(k, portrait).save(p, quality=92)
            made.append(p)
    return made


def main() -> None:
    out = Path.home() / "Desktop/stablecoin-interest-long.mp4"
    work = Path.home() / "Desktop/.stablecoin-interest-long-work"
    made = render_long(
        SECTIONS, out, work, brand=CRYPTO, meta=META, voice=VOICE,
        music=MUSIC,
        callouts=None,
        # The title as typed; last two long forms opened Stamp.
        opener=Search("is the us using stablecoins to reset its debt",
                      centre_y=0.30),
        emphasis=["none", "off switch"],
        thumb_headline=HEADLINE,
        thumb_accent="yellow",
        endcard=ENDCARD, endcard_lead=7.0,
    )
    made["thumb"] = thumbs(Path(made["thumb"]))[0]
    for k, v in made.items():
        print(f"{k}: {v}")


if __name__ == "__main__":
    if "--thumb" in sys.argv or "--thumb-variants" in sys.argv:
        for p in thumbs(Path.home() / "Desktop/stablecoin-interest-long-thumb.jpg",
                        variants="--thumb-variants" in sys.argv):
            print(p)
    else:
        main()
