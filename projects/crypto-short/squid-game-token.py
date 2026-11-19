"""Why could nobody sell the Squid Game token? ~38s crypto short.

Source: crypto-wiki/content/posts/the-squid-game-crypto-scam.mdx - the same
article as the `squid-game-token` long form, written in the same pass.

**Not a trailer for the long form.** The long form tells the whole story:
the pitch, the climb, the warning signs, the pull, the money trail. This
does one move, the trap, in the order a stranger needs it (`shorts.md`,
"It happened again, on a story Short"): what SQUID was and its stake in
sentence 1, the rule (marbles) in sentence 2, the `honeypot` drawing who
could and could not sell, then the pull and the crash, and the show's own
rule as the close.

**Opener: `Stamp`** - WHAT YOU BUY, YOU CAN SELL, stamped NOT SQUID as
sentence 2 says "marbles". The first build used the redacted hook
[MARBLES], but the 13-word title question puts the word at ~6.8s and the
hook reveals by 4.2s at the latest, so it showed before it was said. A
verdict on a claim, never on the asset. The last three crypto Shorts
opened Stamp / Counter / Stamp.

**E17: 30-40s.** **Close: a plain last sentence, no `outro=` card**,
recontextualising the opening (one winner), on the clip the Short opened
on. **No disclaimer** (the long form carries it).

    PYTHONPATH=. .venv/bin/python projects/crypto-short/squid-game-token.py
"""

import sys
from pathlib import Path
from pathlib import Path as _P

from video_automation.core import music
from video_automation.core.stock import CACHE as STOCK
from video_automation.crypto.build import render_crypto_short
from video_automation.crypto.shots import Shot
from video_automation.longform.openers import Stamp

SOURCE_POST = "the-squid-game-crypto-scam"
DEMAND = ("'squid game crypto scam': TheClipZone 'Live RUG PULL of $SQUID' "
          "Short 978.8x (1.8M); Anant Ladha 'Squid Game Scam' Short 15.5x "
          "(1.5M); CoinGecko honeypot explainer ~15x (85k)")
# The cover's style, for the review to compare views and clicks by
# (`thumbnails.md`, "Cover styles are a choice, and every video says which").
COVER_STYLE = "cutout"

V = STOCK / "videos"
ROOT = _P(__file__).resolve().parents[2]
SITE = Path.home() / "Coding/crypto-wiki/public/images/posts"
SHOW = SITE / "squid-game.jpg"         # the show's art the post carries
BEATGROUND = ROOT / "assets/brand/beat-ground-crypto.jpg"

# The long form's roster - screened there, see its header.
CHART = SITE / "rugpull.jpg"            # the real SQUID/WBNB chart, 1 Nov 2021
# No trading-app phone: its ticker read "Apple Inc" (first render, 2026-11-19).
TAPDARK = V / "finger-tapping-phone-screen-dark/33942937.mp4"
MARBLES = V / "glass-marbles-close-up-dark/7233704.mp4"
HOOD = V / "person-laptop-anonymous-dark-room/36036810.mp4"

VOICE = "mia"
MUSIC = music.track("night-drift")

SENTENCES = [
    # The title question, 13 words carrying the name and the stake, so
    # sentence 2 starts at about 4s (`shorts.md`, "The first eight seconds").
    ("Why could nobody sell the Squid Game token, even at two thousand dollars?",),

    # Keeps the answer back: a rule, and a thing nobody has heard of. The
    # hook reveals MARBLES on it.
    ("To sell it, its rules said you first needed marbles.",),

    ("And marbles only came from a game that never launched.",),

    # The honeypot's own sentence: one chunk per reveal.
    ("Anyone could buy SQUID.",
     "But a holder's sell was refused.",
     "No marbles, no sale.",
     "The creators' wallet needed nothing."),

    ("So the price could only climb.",),

    ("On November first, 2021, the creators sold into the pool and took about three point four million dollars.",),

    # The real chart, the camera on the cliff.
    ("Five minutes later, SQUID was worth less than a tenth of a cent.",),

    # The close, said and captioned - no outro card - on the opening clip,
    # so the loop's last frame matches its first.
    ("In the show, one player walks out with the money. Here, it was the creators.",),
]

SHOTS = [
    Shot(clip=TAPDARK, clip_at=1.0, clip_ax=0.50),
    Shot(clip=MARBLES, clip_at=1.0, window=("player", "Marbles: the second token you needed")),
    Shot(image=SHOW, window=("player", "Squid Game, Netflix, 2021")),
    Shot(graphic="honeypot", ground="grid",
         payload=(("YOU", "a SQUID holder"), ("THE CREATORS", "anonymous"),
                  ("THE POOL", "BNB, on PancakeSwap"), "NEEDS MARBLES",
                  "THE GAME NEVER LAUNCHED", "NO RULE FOR THEM",
                  "WHO COULD SELL SQUID")),
    # The real chart (06:30-10:30 UTC, 1 Nov, priced in WBNB): its last climb, then (two shots on) the cliff.
    Shot(graphic="spotlight",
         payload=(CHART, [((0.02, 0.10, 0.66, 0.90), "1 NOV, THE LAST MORNING")],
                  "SQUID / BNB", False)),
    Shot(clip=HOOD, clip_at=2.0, clip_ax=0.60, note=("~$3.38M", "taken, 1 Nov 2021")),
    Shot(graphic="spotlight",
         payload=(CHART, [((0.50, 0.06, 0.92, 0.96), "09:35 UTC, 1 NOV 2021")],
                  "SQUID / BNB", False)),
    Shot(clip=TAPDARK, clip_at=1.5, clip_ax=0.50),
]

GAPS = [0.80, 0.70, 0.70, 1.60, 0.60, 0.80, 0.80, 1.20]

HEADLINE = "Only one\n[winner]"


def thumbs(out: Path, variants: bool = False) -> list[Path]:
    """The 9:16 cover - a pair shares a thumbnail, so the long form's
    `cover()` draws it (`thumbnails.md`)."""
    import importlib.util
    spec = importlib.util.spec_from_file_location(
        "squid_long", ROOT / "projects/crypto-long/squid-game-token.py")
    long_ = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(long_)
    return long_.thumbs(out, portrait=True, variants=variants)


def main() -> None:
    out = Path.home() / "Desktop/squid-game-token-short.mp4"
    work = Path.home() / "Desktop/.squid-game-token-short-work"
    out, total = render_crypto_short(
        SENTENCES, SHOTS, out, work,
        voice=VOICE, gap=GAPS,
        music=MUSIC, music_gain=0.85,
        # The redacted hook cannot wait past 4.2s, and the 13-word title
        # question puts "marbles" at ~6.8s; a Stamp lands on its word up to
        # 7s. A verdict on a claim, never on an asset (`projects/crypto.md`).
        opener=Stamp("What you buy, you can sell", "NOT SQUID",
                     at_word="marbles", enter_word="rules", tone="negative",
                     centre_y=0.40),
        opener_holds=True)
    vert = thumbs(out.with_name(out.stem + "-thumb.jpg"))[0]
    print(f"{out}  {total:.2f}s")
    print(f"{vert}")


if __name__ == "__main__":
    if "--thumb" in sys.argv or "--thumb-variants" in sys.argv:
        for q in thumbs(Path.home() / "Desktop/squid-game-token-short-thumb.jpg",
                        variants="--thumb-variants" in sys.argv):
            print(q)
    else:
        main()
