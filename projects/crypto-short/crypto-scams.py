"""What does every crypto scam ask you for? ~40s crypto short.

Source: crypto-wiki/content/posts/how-to-avoid-crypto-scams.mdx - the same
post as the `crypto-scams` long form, written in the same pass.

**The single move.** The long form walks why crypto cannot be reversed, the
four stories, phishing, clipper malware and the aftermath. The Short does the
one thing those chapters rest on: whatever the story, a scam ends by asking
for your seed phrase or for coins sent first. A `grid` maps four stories onto
those two asks, and a `chapter` card closes cold on the rule.

**No disclaimer** - the long form carries it. No platform, coin or price.

**Clips** are the long form's roster, each used once here. It opens on the
same keycaps-spelling-SCAM clip the long form opens on.

    PYTHONPATH=. .venv/bin/python projects/crypto-short/crypto-scams.py
"""

import sys
from pathlib import Path
from pathlib import Path as _P

from video_automation.core import music
from video_automation.core.stock import CACHE as STOCK
from video_automation.crypto.build import render_crypto_short
from video_automation.crypto.shots import Shot

SOURCE_POST = "how-to-avoid-crypto-scams"

V = STOCK / "videos"
ROOT = _P(__file__).resolve().parents[2]
BRAND = ROOT / "assets/brand"

SCAMKEYS = V / "hacker-hands-keyboard-dark-hoodie/6964023.mp4"
HACKER = V / "hacker-hands-keyboard-dark-hoodie/5240933.mp4"
WRITING = V / "hand-writing-on-paper-desk-lamp-night/8631662.mp4"
CHAT = V / "hands-typing-smartphone-chat-dark/39494892.mp4"
PHONE = V / "phone-vibrating-on-table-dark/6611950.mp4"
FEED = V / "thumb-scrolling-phone-feed-dark/38410500.mp4"

THUMB = ROOT / "assets/crypto/scams/scam-keycaps.jpg"
BEATGROUND = BRAND / "beat-ground-crypto.jpg"

VOICE = "mia"
MUSIC = music.track("night-drift")

CLOSE = "IF THEY ASK FOR EITHER, IT IS A SCAM."

SENTENCES = [
    # The title question.
    ("What does every crypto scam ask you for?",),
    # Sentence two says the hidden words - the hook reveals on "two things".
    ("Almost always one of two things,",
     "whatever the story in front of it."),
    ("Your seed phrase,",
     "or crypto sent to them first."),
    # Hinge into the grid, its own sentence.
    ("The story is the only part that changes.",),
    # The grid's own sentence - one chunk per card.
    ("Support in your messages wants your seed phrase.",
     "A giveaway wants you to send first.",
     "A daily-profit platform wants a deposit first.",
     "A copied website wants your seed phrase."),
    ("Real support, real giveaways, real platforms -",
     "none of them ever ask for either."),
    ("And once the coins move, nobody can send them back.",
     "So remember one line."),
    # Cold close, recontextualising the opening question.
    ((CLOSE, "If they ask for either one, it is a scam."),),
]

SHOTS = [
    Shot(clip=SCAMKEYS, clip_at=0.5),
    Shot(clip=CHAT, clip_at=1.0),
    Shot(clip=WRITING, clip_at=1.0),
    Shot(clip=FEED, clip_at=1.0),
    Shot(graphic="grid", backdrop=BEATGROUND,
         payload=([("Fake support", "asks for your seed phrase", "🎧"),
                   ("Fake giveaway", "asks you to send first", "🎁"),
                   ("Fake investment", "asks for a deposit first", "📈"),
                   ("Fake website", "asks for your seed phrase", "🪝")],
                  "FOUR STORIES, TWO ASKS")),
    Shot(clip=HACKER, clip_at=1.0),
    Shot(clip=PHONE, clip_at=1.0),
    Shot(graphic="chapter", payload=(CLOSE,)),
]

GAPS = [0.70, 0.85, 0.80, 0.55, 1.20, 0.75, 0.90, 1.30]

# Same words and rows as the long form's cover (2026-10-25).
HEADLINE = "How to\nspot a\ncrypto\n[scam]"


def thumbs(out: Path) -> Path:
    """The keycaps hand cut round and scaled to the width, the hood behind it
    in the top half, the headline in four rows on the dark below it. The
    frame's own background is near black, so the ramps at the picture's edges
    only hide the seam; nothing of the hand is faded."""
    import numpy as np
    from PIL import Image
    from video_automation.longform import thumb as T
    src = Image.open(THUMB).convert("RGB").crop((180, 0, 1380, 1080))
    h = int(src.height * 1080 / src.width)
    src = src.resize((1080, h), Image.LANCZOS)
    im = Image.new("RGB", (1080, 1920), (0, 0, 0))
    y = 120
    im.paste(src, (0, y))
    a = np.zeros((1920, 1), np.float32)
    a[:y, 0] = 1.0
    a[y:y + 120, 0] = np.linspace(1.0, 0.0, 120)
    a[y + h - 240:y + h, 0] = np.linspace(0.0, 1.0, 240)
    a[y + h:, 0] = 1.0
    mask = Image.fromarray((np.repeat(a, 1080, 1) * 255).astype("uint8"))
    im = Image.composite(Image.new("RGB", im.size, (0, 0, 0)), im, mask)
    fill, ink = T.ACCENTS["yellow"]
    T._headline(im, HEADLINE, 240, 1080 - 2 * 52, 52, fill, ink, max_lines=4,
                max_block=1920 * 0.36, leading=1.02, band="bottom",
                margin=int(1920 * 0.16) + 20, shadow=14, drop=(6, 8))
    im.save(out, quality=92)
    return out

def main() -> None:
    out = Path.home() / "Desktop/crypto-scams-short.mp4"
    work = Path.home() / "Desktop/.crypto-scams-short-work"
    out, total = render_crypto_short(SENTENCES, SHOTS, out, work,
                                     voice=VOICE, gap=GAPS,
                                     music=MUSIC, music_gain=0.85,
                                     hook="Every crypto scam asks for [two things]")
    vert = thumbs(out.with_name(out.stem + "-thumb.jpg"))
    print(f"{out}  {total:.2f}s")
    print(f"{vert}")


if __name__ == "__main__":
    if "--thumb" in sys.argv:
        print(thumbs(Path.home() / "Desktop/crypto-scams-short-thumb.jpg"))
    else:
        main()
