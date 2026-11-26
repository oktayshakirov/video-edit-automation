"""If Bitcoin is a Ponzi scheme, who pays the returns? ~38s crypto short.

Source: crypto-wiki/content/posts/what-is-bitcoin.mdx - the same article as
the `bitcoin-ponzi` long form, written in the same pass. Facts and sources
in the long form's header.

**Not a trailer for the long form.** The long form walks the SEC's
definition, three named Ponzis, the check and the sceptics' true part.
This does the one move, as a stranger would ask it: every Ponzi has a
person paying the "returns" out of new money - name one for Bitcoin. The
same three cards, drawn twice: with the operator, and with nobody in the
middle. Then the catch that cuts both ways: nobody pays you anything.
The close loops to the opening question - nobody pays your returns.

**Opener: `Split`**, PONZI against BITCOIN, SAME MACHINE? - a comparison,
left open; sentence 2 names the kind of answer (a person, by name) and
keeps Bitcoin's back. Last three crypto Shorts: Counter, Stamp, Split -
Split again is two running, not three. Sentence 1 is the title question
at 13 words, so sentence 2 starts near 4s; `opener_holds=True`.

**Pictures:** $20 bills on black (open and close);
Charles Ponzi, framed and named; `ponzi` (new) twice - the operator,
then nobody; a full-screen `chapter` for the catch; a fan of $100s in a
player window. The miners line and its mempool.space page were cut
from the first render to bring it from 41.9s under 40s (E17).

**E17: 30-40s.** A plain last sentence, no `outro=` card. No disclaimer
(the long form carries it).

    PYTHONPATH=. .venv/bin/python projects/crypto-short/bitcoin-ponzi.py
"""

import sys
from pathlib import Path
from pathlib import Path as _P

from video_automation.core import music
from video_automation.core.stock import CACHE as STOCK
from video_automation.crypto.build import render_crypto_short
from video_automation.crypto.shots import Shot
from video_automation.longform.openers import Split

SOURCE_POST = "what-is-bitcoin"
DEMAND = ("Austin Talks Money 'Bitcoin: Scam, Ponzi, or Something Bigger?' "
          "4.0x (31.7k); Iced Coffee Hour Clips 'Why Bitcoin is a SCAM! | "
          "Peter Schiff' 14.5x (385k)")
COVER_STYLE = "vector"

V = STOCK / "videos"
CAP = STOCK / "captures"
ROOT = _P(__file__).resolve().parents[2]
BP = ROOT / "assets/crypto/bitcoin-ponzi"

# The long form's roster - screened there, see its header.
# Dollars on black open and close it - the first cut's fanned notes were
# Polish zloty (the editor: "use dollars"), and before that a phone showed a
# FTSE 100 chart under "Bitcoin".
USD20 = V / "dollar-bills-black-background/6590462.mp4"
FAN_ONE = V / "counting-hundred-dollar-bills-hands-dark/5466780.mp4"   # bright - window only
PONZI = BP / "charles-ponzi.jpg"

VOICE = "mia"
MUSIC = music.track("night-drift")

SENTENCES = [
    # The title question, 13 words, the stake in it.
    ("If Bitcoin is a Ponzi scheme, who's the person paying everyone their returns?",),

    # The kind of answer, not the answer: every real one has someone running
    # it. Who, for Bitcoin, stays open. (The first cut's "Every real Ponzi has
    # one, by name: Charles Ponzi, Bernie Madoff, BitConnect" read as a
    # riddle over Ponzi's photo - the editor, at 0:08.)
    ("Every real Ponzi scheme has someone running it, like Charles Ponzi in 1920.",),

    # The beat's own sentence: in, out, the collapse.
    ("They take money from new investors,",
     "pay the earlier ones out of it,",
     "and collapse when the new money stops."),

    # The same cards, nobody in the middle.
    ("When you buy Bitcoin, your dollars go to whoever sold,",
     "nobody holds the pot,",
     "and nobody promises a return."),

    # The catch, as the turn.
    (("BITCOIN PAYS YOU NOTHING.",
      "But that cuts both ways. Bitcoin pays you nothing at all."),),

    ("Selling it for more takes a later buyer who pays more.",),

    # The close loops to the opening question.
    ("So nobody pays your returns. Not an operator, and not Bitcoin.",),
]

SHOTS = [
    Shot(clip=USD20, clip_at=0.5),
    Shot(image=PONZI, zoom=1.04, window=("player", "Charles Ponzi, 1920")),
    Shot(graphic="ponzi", ground="grid",
         payload=("ponzi", ("EARLY INVESTORS", "paid 'returns'"),
                  ("THE OPERATOR", "Ponzi, Madoff, BitConnect"),
                  ("NEW INVESTORS", "pay in"),
                  "'RETURNS'", "COLLAPSES", "HOW A PONZI PAYS")),
    Shot(graphic="ponzi", ground="grid",
         payload=("market", ("THE SELLER", "gets your dollars"),
                  ("NOBODY", "in the middle"), ("YOU", "the buyer"),
                  "HOLDS NO MONEY", "PROMISES NO RETURN",
                  "WHEN YOU BUY BITCOIN", "BTC")),
    Shot(graphic="chapter", ground="grid",
         payload=("BITCOIN PAYS YOU NOTHING.",)),
    Shot(clip=FAN_ONE, clip_at=1.0,
         window=("player", "Sold for more - to a later buyer")),
    # The opening clip again, so the last frame meets the first.
    Shot(clip=USD20, clip_at=0.5),
]

GAPS = [0.85, 0.80, 1.60, 1.60, 0.80, 0.70, 1.00]


def thumbs(out: Path) -> list[Path]:
    """The 9:16 cover, from the long form's `cover()` (a pair shares one)."""
    import importlib.util
    spec = importlib.util.spec_from_file_location(
        "bitcoin_ponzi_long",
        _P(__file__).resolve().parents[1] / "crypto-long/bitcoin-ponzi.py")
    long = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(long)
    return long.thumbs(out, portrait=True)


def main() -> None:
    out = Path.home() / "Desktop/bitcoin-ponzi-short.mp4"
    work = Path.home() / "Desktop/.bitcoin-ponzi-short-work"
    out, total = render_crypto_short(
        SENTENCES, SHOTS, out, work,
        voice=VOICE, gap=GAPS,
        music=MUSIC, music_gain=0.85,
        opener=Split("PONZI", "BITCOIN", "SAME MACHINE?"),
        opener_holds=True)
    covers = thumbs(out.with_name(out.stem + "-thumb.jpg"))
    print(f"{out}  {total:.2f}s")
    print(covers[0])


if __name__ == "__main__":
    if "--thumb" in sys.argv:
        for p in thumbs(Path.home() / "Desktop/bitcoin-ponzi-short-thumb.jpg"):
            print(p)
    else:
        main()
