"""Why do you never see the interest on your stablecoin? ~36s crypto short.

Source: crypto-wiki/content/posts/what-is-the-genius-act.mdx - the same
article as the `stablecoin-interest` long form, written in the same pass.

**Not a trailer for the long form.** The long form is the debt-reset
rumour, checked. This does one move, in the order a stranger would ask it:
your stablecoin earns interest, you never see it, because your dollar was
lent to the US government and the issuer keeps the interest - and a law
keeps it that way. Then the rumour as the twist ("some call it a secret
plan to erase America's debt") and the sum that answers it. The close
loops to the opening: nobody erases the debt, they keep the interest.

**Opener: `Counter`**, $0 - YOUR SHARE OF THE INTEREST, entering on
"lent" and landing on "else" in sentence 2. Sentence 1 is the title
question at 13 words, so sentence 2 starts near 4s. The last two crypto
Shorts opened `Stamp`.

**Pictures:** hands paying on a phone (a clip, to open and to close); the
real Treasury building under "lent to the US government"; `reserve` (new)
for the mechanism; a full-screen `chapter` for Circle's figure; the law's
own text in a browser window; the Capitol under the rumour; `bars` for the
debt against every stablecoin. No `pile`, `breach` or `blindsign`.

**E17: 30-40s.** A plain last sentence, no `outro=` card. No disclaimer
(the long form carries it).

    PYTHONPATH=. .venv/bin/python projects/crypto-short/stablecoin-interest.py
"""

import sys
from pathlib import Path
from pathlib import Path as _P

from video_automation.core import music
from video_automation.core.stock import CACHE as STOCK
from video_automation.crypto.build import render_crypto_short
from video_automation.crypto.shots import Shot
from video_automation.longform.openers import Counter

SOURCE_POST = "what-is-the-genius-act"
DEMAND = ("Clearly Finance 'Is the US Planning a $37 Trillion Crypto Debt "
          "Reset?' 39.2x (216k); The Part Time Economist 'How Stablecoin "
          "Issuers Make Money' 47.7k")
COVER_STYLE = "cutout"

V = STOCK / "videos"
CAP = STOCK / "captures"
ROOT = _P(__file__).resolve().parents[2]

# The long form's roster - screened there, see its header.
PHONE_CARD = V / "man-using-phone-banking-app-at-night/7535099.mp4"   # hands, a phone and a card
TREASURY = V / "us-treasury-department-building/29188210.mp4"         # the Treasury building's columns
CAPITOL_MOODY = V / "washington-dc-capitol-dome-aerial/29188237.mp4"  # the dome behind bare trees
LAW_YIELD_V = CAP / "genius-act/yield-v.mp4"                          # Sec. 4(a)(11), ringed, cut tall
LAW_ADDR = "govinfo.gov - GENIUS Act"

VOICE = "mia"
MUSIC = music.track("night-drift")

SENTENCES = [
    # The title question, 13 words, the stake in it.
    ("If your stablecoin earns interest every day, why do you never see any?",),

    # Not the verdict: who, and why it is legal, are still open. The
    # Counter enters on "lent" and lands $0 on "else".
    ("Your dollar was lent to the US government, and someone else collects.",),

    # The reserve's own sentence: deposit, loan, interest, yours.
    ("You hand over a dollar, and get a token.",
     "The issuer buys a US Treasury bill with it.",
     "The bill pays interest. The issuer keeps it.",
     "You get zero."),

    (("$2.6 BILLION IN INTEREST. CIRCLE, 2025.",
      "Circle made two point six billion dollars that way in 2025."),),

    ("And a new US law bans paying you any of it.",),

    # The rumour, as the turn.
    ("Some call it a secret plan to erase America's debt.",),

    # The bars' own sentence: one chunk per row.
    ("But the debt is over forty trillion dollars.",
     "Every stablecoin together, under three hundred billion."),

    # The close loops to the opening question.
    ("Nobody's erasing the debt. They're just keeping the interest.",),
]

SHOTS = [
    Shot(clip=PHONE_CARD, clip_at=0.5),
    # Framed, so it is not a second full-frame clip after the opening one.
    Shot(clip=TREASURY, clip_at=1.0,
         window=("player", "The US Treasury, Washington")),
    Shot(graphic="reserve", ground="grid",
         payload=(("YOU", "hand over a dollar"),
                  ("THE ISSUER", "Tether, Circle"),
                  ("US TREASURY BILL", "93 days or less"),
                  "KEEPS THE INTEREST", "$0", "BANNED BY LAW",
                  "WHERE THE INTEREST GOES")),
    Shot(graphic="chapter", ground="grid",
         payload=("$2.6 BILLION IN INTEREST. CIRCLE, 2025.",)),
    Shot(clip=LAW_YIELD_V, clip_at=0.0, window=("browser", LAW_ADDR)),
    Shot(clip=CAPITOL_MOODY, clip_at=2.0),
    Shot(graphic="bars", ground="grid",
         payload=([("US debt", 1.0, "$40.6T"),
                   ("Every stablecoin", 287.1 / 40617, "$287B")],
                  "THE DEBT AGAINST EVERY STABLECOIN")),
    # The opening clip again, so the last frame meets the first.
    Shot(clip=PHONE_CARD, clip_at=3.5),
]

GAPS = [0.85, 0.70, 1.40, 0.60, 0.60, 0.60, 1.20, 1.00]

def thumbs(out: Path) -> list[Path]:
    """The 9:16 cover, from the long form's `cover()` (a pair shares one):
    the cutout at `out`, written once."""
    import importlib.util
    spec = importlib.util.spec_from_file_location(
        "stablecoin_interest_long",
        _P(__file__).resolve().parents[1] / "crypto-long/stablecoin-interest.py")
    long = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(long)
    return long.thumbs(out, portrait=True)


def main() -> None:
    out = Path.home() / "Desktop/stablecoin-interest-short.mp4"
    work = Path.home() / "Desktop/.stablecoin-interest-short-work"
    out, total = render_crypto_short(
        SENTENCES, SHOTS, out, work,
        voice=VOICE, gap=GAPS,
        music=MUSIC, music_gain=0.85,
        opener=Counter("$0", "YOUR SHARE OF THE INTEREST", at_word="else",
                       enter_word="lent", centre_y=0.36),
        opener_holds=True)
    covers = thumbs(out.with_name(out.stem + "-thumb.jpg"))
    print(f"{out}  {total:.2f}s")
    print(covers[0])


if __name__ == "__main__":
    if "--thumb" in sys.argv:
        for p in thumbs(Path.home() / "Desktop/stablecoin-interest-short-thumb.jpg"):
            print(p)
    else:
        main()
