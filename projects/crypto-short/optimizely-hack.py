"""Would your hardware wallet catch the Optimizely swap? ~35s crypto short.

Source: crypto-wiki/content/posts/send-and-receive-crypto-safely.mdx - the
same article as the `optimizely-hack` long form, written in the same pass.
Facts and sources in the long form's header.

**Not a trailer for the long form.** The long form walks how one script
reached 178 sites, where it swapped, why every screen agreed and the
checks that work. This does the one move: the hardware wallet would have
shown the attacker's address and it would have matched the page - so the
check has to be against a source the page never touched.

**Opener: `Split`**, PAGE against DEVICE, SAME ADDRESS? - a comparison, and
left open: sentence 2 answers it the way nobody expects (the same, and
both wrong). The last three crypto Shorts opened Counter / Stamp / Stamp.
Sentence 1 is the title question at 13 words, so sentence 2 starts near 4s
(`shorts.md`, "The first eight seconds"), `opener_holds=True`.

**Pictures:** the keyboard (copy) to open and close; a real Trezor's
confirm screen, framed; Decrypt's headline
in a tab; `grid` for the three places; `relay` (new, built for this pair)
for every screen agreeing; the trackpad for the source the page never
touched. Two stock clips of six shots.

**E17: 30-40s.** **Close: a plain last sentence, no `outro=` card**, on the
clip the Short opened on. **No disclaimer** (the long form carries it).

    PYTHONPATH=. .venv/bin/python projects/crypto-short/optimizely-hack.py
"""

import sys
from pathlib import Path
from pathlib import Path as _P

from video_automation.core import music
from video_automation.core.stock import CACHE as STOCK
from video_automation.crypto.build import render_crypto_short
from video_automation.crypto.shots import Shot
from video_automation.longform.openers import Split

SOURCE_POST = "send-and-receive-crypto-safely"
DEMAND = ("The CryptoDad 'Ledger Website Hacked! Is Your Crypto Safe?' 51k in "
          "2 days (ratio ?); Digital Asset News 'Ledger's Site Served "
          "Malware' 35.7k; brand-new term (OPTIMJACK, 16 Nov 2026), plain "
          "explainers 4-252 views")
# The cover's style, for the review to compare views and clicks by
# (`thumbnails.md`, "Cover styles are a choice, and every video says which").
COVER_STYLE = "beat"

V = STOCK / "videos"
ROOT = _P(__file__).resolve().parents[2]
BEATGROUND = ROOT / "assets/brand/beat-ground-crypto.jpg"

# The long form's roster - screened there, see its header.
KEYBOARD = V / "copy-paste-laptop-keyboard-shortcut-dark/36036748.mp4"   # lit from ~3s, fingers by the shortcut keys
TRACKPAD = V / "hand-on-laptop-trackpad-night-dark-close/39425747.mp4"   # a hand hovering over a trackpad
TREZOR = ROOT / "assets/crypto/hardware-wallet/trezor-confirm.jpg"   # its own screen: "Confirm sending"
TREZOR_ASPECT = 953 / 1270
DECRYPT_V = STOCK / "captures/decrypt-optimizely/decrypt-optimizely-v.mp4"
DECRYPT_ADDR = "decrypt.co/383414/optimizely-hack"

MEANT = "1Kp7vQ2mXz9LrT4wBn6cHd8yFs3aJe5gUq"         # made up
ATTACKER = "19g9rZcPeiz8rUvyWpTRyXXhPnjsWrc3kW"      # StepSecurity's IOC table

VOICE = "mia"
MUSIC = music.track("night-drift")

SENTENCES = [
    # The title question, 13 words with the stake in it.
    ("What would your hardware wallet show if a website swapped your copied address?",),

    # Partial answer that overturns what the viewer expects (a warning):
    # it agrees. The next question - then what does catch it? - is open.
    ("The attacker's address, matching the page character for character.",),

    ("On November sixteenth, one script on a hundred and seventy-eight websites, Ledger's among them, did exactly that.",),

    # The grid's own sentence: one chunk per card.
    ("It swapped addresses in the text on the page,",
     "in whatever you copied,",
     "and in whatever the page sent."),

    # The relay's own sentence: one chunk per screen, then the verdict.
    ("Copy it from the page,",
     "paste it into your wallet,",
     "and your hardware wallet shows the same.",
     "Every screen agrees with the attacker."),

    ("The only check that works uses a source the page never touched.",),

    # The close loops to the title question over the keyboard it opened on.
    ("So your device can only agree with what you gave it.",),
]

SHOTS = [
    Shot(clip=KEYBOARD, clip_at=3.0),
    # A real hardware wallet asking to confirm a send - framed and named.
    Shot(image=TREZOR, aspect=TREZOR_ASPECT, zoom=1.05,
         window=("player", "A hardware wallet: confirm sending")),
    Shot(clip=DECRYPT_V, clip_at=0.0, window=("browser", DECRYPT_ADDR)),
    Shot(graphic="grid", backdrop=BEATGROUND, ground="grid",
         payload=([("The page", "its text", "\U0001F4C4"),
                   ("Your copy", "the clipboard", "\U0001F4CB"),
                   ("What it sent", "the page's requests", "\U0001F4E4")],
                  "THREE PLACES")),
    Shot(graphic="relay", backdrop=BEATGROUND, ground="grid",
         payload=(MEANT, ATTACKER,
                  ["The page", "Your wallet app", "Your hardware wallet"],
                  "ONE ADDRESS, THREE SCREENS",
                  ("EVERY SCREEN AGREES", "WITH THE ATTACKER"))),
    Shot(clip=TRACKPAD, clip_at=2.0,
         window=("player", "A source the page never touched")),
    # The opening clip again, so the loop reads.
    Shot(clip=KEYBOARD, clip_at=3.0),
]

GAPS = [0.80, 0.70, 0.80, 0.95, 1.30, 0.80, 1.20]

HEADLINE = "Every Screen\n[Agreed]"


def main() -> None:
    out = Path.home() / "Desktop/optimizely-hack-short.mp4"
    work = Path.home() / "Desktop/.optimizely-hack-short-work"
    out, total = render_crypto_short(
        SENTENCES, SHOTS, out, work,
        voice=VOICE, gap=GAPS,
        music=MUSIC, music_gain=0.85,
        opener=Split("PAGE", "DEVICE", "SAME ADDRESS?"),
        opener_holds=True)
    print(f"{out}  {total:.2f}s")


if __name__ == "__main__":
    main()
