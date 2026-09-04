"""What are perpetual futures? ~45s crypto short.

Source: crypto-wiki/content/posts/what-are-perpetual-futures.mdx, the same
post as the `perpetual-futures-long` explainer.

**Second pass, after review.** The first cut opened straight on the funding-
rate mechanism and the user's note was that it read as confusing - a Short
still has to explain what the thing *is* before it can explain how it
behaves, the same way the long form does, just in fewer words. So this cut
now spends two sentences saying plainly what a perpetual future is (leverage,
no expiry) before it gets to the reframe (a normal contract has a date; this
one does not) and only then the funding rate. Leverage's *danger* is still
left to the long form - only its existence is named here, in one clause, so
the viewer knows why a contract with no expiry needs anything to hold its
price down at all.

**It opens by asking its own title question.** A Short has no title card, no
thumbnail on screen and no chapter list, so the first line has to be the
question the whole thing answers - "Why doesn't a contract with no
expiration date just float away from the real price?" - not the first line
of the argument.

**One drawn beat: `grid`, not `checklist`.** The two funding-direction facts
("above spot, longs pay shorts" / "below spot, shorts pay longs") are not a
judged list - neither is right or wrong, they are just the two halves of one
rule - so `grid` is the correct silhouette, not `checklist`.

**No financial advice line, and that is now the standing rule for every
Short on this channel, not just this one.** The user's note: shorts don't
carry the disclaimer, only the long-form videos do - a Short has no room to
earn the line's own weight, and the long form it is paired with already
carries it. The script still names no price level, no platform, no
direction and recommends nothing; the disclaimer was never load-bearing
here, only the compliance *line* is dropped.

**A capitalised "IT" is read as the initialism, not the word.** The
statement card's on-screen text is `NO EXPIRY. JUST A FEE THAT KEEPS IT
HONEST.`, and `espeak-ng --ipa` confirms Kokoro reads capital `IT` as
`aɪtˈiː` - "I.T." - which is exactly what shipped in the first cut, audible
at 0:34. The card stays capitals; the spoken half of the sentence is now the
lower-case sentence, exactly as `Binance`/`Bynanse` already does for a
different reason. Check every all-caps beat title against this before it
ships - `narration.md` already warned ALL CAPS was untested, and this is the
untested case landing.

**Assets are shared with the long form's roster where the reuse budget
allows, and fresh where it does not.** `laptop-closing-screen-dark-night`,
`night-sky-stars-twinkling-slow-dark`, `tightrope-walker-balance-dark` and
`man-looking-at-phone-worried-dark` were each used once in the long form, so
this short uses each exactly once more to stay inside the two-use cap the
pair shares. `infinity-loop-abstract-gold-dark` (a slow gold tunnel with no
visible end - the picture of "no date at all") and
`hands-shaking-silhouette-dark-deal` (two sides settling something directly,
not through a company) are new and used only by this pair; the handshake is
the only clip repeated within this cut itself, five slots apart. The closing
line was shortened rather than left on `night-sky-stars-twinkling-slow-dark`
at length - that clip is only 7.4s, and the first cut's longer closing
question needed more than its 1.33x stretch ceiling allows.

**Phonemes.** Same finding as the long form: `Binance` is not named in this
cut, so no respell is needed here; every other word read is already checked
by the long form's docstring.

Run from the repo root:

    PYTHONPATH=. .venv/bin/python projects/crypto-short/perpetual-futures.py
"""

from pathlib import Path

from video_automation.core import music
from video_automation.core.brand import CRYPTO
from video_automation.core.stock import CACHE as STOCK
from video_automation.crypto.build import render_crypto_short
from video_automation.crypto.shots import Shot
from video_automation.longform.thumb import render_short_thumb

V = STOCK / "videos"
# Shared with the long form, one use left each under the pair's reuse cap.
LAPTOPCLOSE = V / "laptop-closing-screen-dark-night/7272375.mp4"       # 19.6s L14-18 S8-10
STARS = V / "night-sky-stars-twinkling-slow-dark/11533575.mp4"         # 7.4s L30-39 S12-22
RISK = V / "tightrope-walker-balance-dark/10013469.mp4"                # 16.2s L18 S14, single use in the long form - one left
WORRIED1 = V / "man-looking-at-phone-worried-dark/7280528.mp4"         # 18.1s L42 S24, single use in the long form - one left
# New, and shared only with this post's long form.
INF = V / "infinity-loop-abstract-gold-dark/33830922.mp4"              # 8.0s L24-30 S49-59, a tunnel with no visible end
SHAKE = V / "hands-shaking-silhouette-dark-deal/6101696.mp4"           # 17.4s L28-36 S3-7, two hands settling a deal directly

PH = STOCK / "photos"
COINS = PH / "gold-coins-stack-dark-moody-macro/38724872.jpg"          # thumbnail only, matches the long form

VOICE = "mia"

MUSIC = music.track("night-drift")

SENTENCES = [
    # The title question, over motion - a Short viewer has nothing else on
    # screen but this sentence.
    ("Why doesn't a contract with no expiration date",
     "just float away from the real price?"),

    # Say what it plainly IS before saying how it behaves - the note from
    # review was that the first cut skipped straight to the mechanism.
    ("A perpetual future lets you trade something like Bitcoin with leverage,",
     "and the contract itself never expires."),

    ("A normal futures contract settles on a date,",
     "and that date is what pulls its price back to reality."),

    ("This one has no date at all.",),

    # Hinge, its own sentence - a beat times its reveals off the caption
    # starts of its own sentence, so the lead-in cannot live inside it.
    ("So one thing has to do that job instead -",
     "a fee, paid directly between traders, every few hours."),

    # The beat: two facts, no verdict - neither side is "wrong", so `grid`
    # rather than `checklist`.
    ("If the contract trades above the real price, longs pay shorts.",
     "If it trades below, shorts pay longs."),

    ("It's a small fee,",
     "and it's not the exchange getting rich -",
     "just two traders settling up, automatically."),

    # A full-screen statement. `build` suppresses captions on any shot with a
    # graphic, so the on-screen card can stay capitals while the voice reads
    # a normal sentence - which also fixes the capital "IT" reading as the
    # initialism (`espeak-ng --ipa "keeps IT honest"` -> "I.T.").
    (("NO EXPIRY. JUST A FEE THAT KEEPS IT HONEST.",
      "No expiry. Just a fee that keeps it honest."),),

    # No compliance line here - shorts on this channel carry the question
    # only, and the paired long form is where the disclaimer lives.
    ("So what's actually keeping a price like that honest?",),
]

SHOTS = [
    Shot(clip=SHAKE, clip_at=1.0),
    Shot(clip=LAPTOPCLOSE, clip_at=1.0),
    Shot(clip=WORRIED1, clip_at=1.0),
    Shot(clip=INF, clip_at=0.5),
    Shot(clip=RISK, clip_at=1.0),
    Shot(graphic="grid",
         payload=([("Above the real price", "Longs pay shorts", "\U0001F4C8"),
                   ("Below the real price", "Shorts pay longs", "\U0001F4C9")],
                  "WHICH SIDE PAYS?")),
    Shot(clip=SHAKE, clip_at=8.0),           # second use, five slots on
    Shot(graphic="chapter",
         payload=("NO EXPIRY. JUST A FEE THAT KEEPS IT HONEST.",)),
    Shot(clip=STARS, clip_at=0.3),           # short closing line, well
                                              # inside the 7.4s clip's budget
]

EMOJI = {
    "a fee, paid directly between traders, every few hours.": "⏱️",   # stopwatch
}

# 0.34 inside a thought, 0.55-0.90 at the end of one. The grid (index 5) is a
# flat pair with no marks to land, so 1.10 rather than a checklist's 2.10 -
# there is no verdict pause to buy. The statement card (index 7) takes 1.30
# before the closing question is allowed to land on its own.
GAPS = [0.75, 0.85, 0.85, 0.90, 0.60, 1.10, 0.85, 1.30, 0.34]


def main() -> None:
    out = Path.home() / "Desktop/perpetual-futures-short.mp4"
    work = Path.home() / "Desktop/.perpetual-futures-short-work"
    out, total = render_crypto_short(SENTENCES, SHOTS, out, work,
                                     voice=VOICE, emoji=EMOJI, gap=GAPS,
                                     music=MUSIC, music_gain=0.85)

    # Same source and headline as the long form - a viewer who sees both
    # should recognise the second one. Simplified from the bracket-accent
    # phrasing after review: "Never expires. Still [risky.]" clipped its own
    # last word at the frame edge, and a plain search-style question is
    # clearer at feed size anyway.
    head = "What Are Perpetual [Futures]?"
    vert = render_short_thumb(
        out.with_name(out.stem + "-thumb.jpg"), CRYPTO, head,
        image=COINS, accent="yellow", band="top")
    print(f"{out}  {total:.2f}s")
    print(f"{vert}")


if __name__ == "__main__":
    main()
