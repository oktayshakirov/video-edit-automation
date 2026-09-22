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

from pathlib import Path
from pathlib import Path as _P

from video_automation.core import music
from video_automation.core.brand import CRYPTO
from video_automation.core.stock import CACHE as STOCK
from video_automation.crypto.build import render_crypto_short
from video_automation.crypto.shots import Shot
from video_automation.longform.thumb import render_short_thumb

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


def main() -> None:
    out = Path.home() / "Desktop/crypto-scams-short.mp4"
    work = Path.home() / "Desktop/.crypto-scams-short-work"
    out, total = render_crypto_short(SENTENCES, SHOTS, out, work,
                                     voice=VOICE, gap=GAPS,
                                     music=MUSIC, music_gain=0.85,
                                     hook="Every crypto scam asks for [two things]")
    # Same headline as the long form - a pair shares its thumbnail.
    vert = render_short_thumb(
        out.with_name(out.stem + "-thumb.jpg"), CRYPTO,
        "How to spot a [crypto scam]",
        image=THUMB, accent="yellow", band="top")
    print(f"{out}  {total:.2f}s")
    print(f"{vert}")


if __name__ == "__main__":
    main()
