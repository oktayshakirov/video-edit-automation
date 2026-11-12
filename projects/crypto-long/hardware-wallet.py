"""Do you need a hardware wallet? - long-form 16:9 for YouTube.

Source: crypto-wiki/content/posts/what-is-a-hardware-wallet.mdx - its
signing walkthrough, the threat-model section (what it blocks and what it
does not), the Coldcard case, and the hot / hardware / custodial split.

**The angle.** The yes/no question a buyer already has: Cyber Scrilla "Do
You NEED a Cold Wallet? (Watch This First)" 330k, 16.3x
(`demand/teardowns/do-you-need-a-cold-wallet.md`). Viewers rewound for the
rule and the verdict, thanked it for the signing flow shown step by step,
and skipped the plan preview. What it left open is what this one answers:
what the device does *not* protect, the device itself failing (Coldcard,
2026), and that the backup becomes your job. No product is picked or rated;
the verdict is two questions the viewer answers about themselves.

**A mechanism, so the default arc** (`longform.md`); the turn is "Actually,
more than people think", and the climax is the Coldcard case on TRM Labs'
own page. Three chapters (E18).

**Every figure is sourced.** Coldcard: TRM Labs, 5 Aug 2026 ("Firmware
version 4.0.1, released in March 2021"; "Starting July 30, 2026, attackers
drained roughly 1,816 BTC ... from over 5,200 addresses across four
waves"; "without ever touching the physical device"), matching the
article. Bybit, 21 Feb 2025, about $1.46 billion in one transaction: the
site's `how-does-north-korea-steal-crypto`.

## The picture (re-cut 2026-11-12 after the editor's review)

The first cut had 6 of 25 shots drawn and was rejected as boring: full-frame
photographs and stock one after another, the coin `pile` again, a title
slate, a drawer clip with an unrelated note in it. This cut was planned
picture first (`workflow.md`, "Write the picture first"): 19 of 27 shots are
drawn or framed, and no two full-frame pictures follow each other.

* `grid` (2) - where things are: the blockchain holds the coins, the device
  holds one key.
* `spotlight` - a real Trezor, then its screen: "Confirm sending".
* `callout` - a real Coldcard with its parts labelled: the chip, the
  screen, the buttons.
* `airgap` (new) - the signing flow as two places and what crosses between
  them; the key gets its ring and NEVER LEAVES. Held under the next line.
* `blindsign` - "it signs whatever you approve".
* `steps` - recovery words, typed into another wallet, your key rebuilt.
* `compare` - what it blocks against what it cannot stop, 3 + 3.
* `bars` - key strength, 128 bits against 40 (TRM Labs' figures).
* `breach` (new) - 5,200 addresses emptied in four waves, the figure
  counting up. Not `pile`: it was in the last pair, and this money was
  spread over thousands of addresses, not in one pot.
* `grid` (3), `stat`, `diagram` - where your key sits, Bybit, the two
  questions and what they add up to.
* `checklist` - what it guards and what it does not, as the close.
* Windows: TRM Labs' report in a browser tab (twice), the laptop clip in a
  player. **No title slate** (`longform.md`, "No title slate").

**Opener: `Stamp`**, "My crypto is on the device", stamped NEVER WAS on
"never". It judges a claim, never a product. Last three long forms opened
Search / Split / Stamp. The Short shares it.

**Real pictures:** Wikimedia Commons photographs of real devices (Ledger,
Trezor, Coldcard - Pexels has none), `assets/crypto/hardware-wallet/
CREDITS.md`; TRM Labs' report captured (`screencap`, the headline, then the
firmware line and the drained line ringed), shown in a browser window so
the white page sits on the dark ground.

    PYTHONPATH=. .venv/bin/python projects/crypto-long/hardware-wallet.py
"""

import sys
from pathlib import Path
from pathlib import Path as _P

from video_automation.core import music, stillclip
from video_automation.core.brand import CRYPTO
from video_automation.core.stock import CACHE as STOCK
from video_automation.crypto.shots import Shot

from video_automation.longform import Meta, Section, render_long
from video_automation.longform.openers import Stamp

SOURCE_POST = "what-is-a-hardware-wallet"
DEMAND = ("Cyber Scrilla 'Do You NEED a Cold Wallet? (Watch This First)' "
          "16.3x (330k); VirtualBacon 'Do you need a Crypto Hardware "
          "Wallet?' Short 220k")
# The cover's style, for the review to compare views and clicks by
# (`thumbnails.md`, "Cover styles are a choice, and every video says which").
COVER_STYLE = "arrow"

V = STOCK / "videos"
ROOT = _P(__file__).resolve().parents[2]
BRAND = ROOT / "assets/brand"
HW = ROOT / "assets/crypto/hardware-wallet"

# Fetched fresh for this pair (2026-11-12), contact-sheeted at 15/50/85%,
# luma at 0.5/3/6/9s, and checked by Pexels id against every other script
# (300 either side - the same shoot). Three batches; almost nothing else
# survived (verdicts in `footage.md`, "The hardware-wallet fetch").
BURGLAR = V / "burglar-flashlight-dark-room/18449083.mp4"        # 17s, B2-37, a flashlight searching a dark room - hacked tonight
GLOW = V / "laptop-glow-dark-room-close-up/15356658.mp4"         # 8s, L6-9, a backlit keyboard in the dark, light trails above - online all day

# The real devices (Commons, credits in CREDITS.md). Pexels has none.
LEDGER_LAPTOP = HW / "ledger-laptop.jpg"    # a Ledger on its cable beside a laptop - opens, plugs in, closes
LEDGER_HAND = HW / "ledger-hand.jpg"        # a hand holding a Ledger - COLD goes behind it
TREZOR = HW / "trezor-confirm.jpg"          # a Trezor's own screen: "Confirm sending ... to addr..."
TREZOR_ASPECT = 953 / 1270
COLDCARD_READY = HW / "coldcard-ready.jpg"  # "Coldcard is ready to sign transactions!" on its screen
COLDCARD_DARK = HW / "coldcard-dark.jpg"    # a Coldcard lit on black - the case begins, and the disclaimer
COLDCARD_HAND = HW / "coldcard-hand.jpg"    # a Coldcard in a hand, "OK TO SEND?" on its screen
COLDCARD_KEYS = HW / "coldcard-keyboard.jpg"  # a Coldcard on a dark keyboard - "software too"
# The cover only (`thumbnails.md`, "The cover's picture stays on the cover"):
# a Ledger on its cable, "Bitcoin" on its screen.
LEDGER_CABLE = HW / "ledger-cable.jpg"

# The real page: TRM Labs' report, captured 2026-11-12 (`screencap`, record
# in `captures/trm-coldcard/`, consent banner hidden). `head` is the
# headline; `drained` rings the March 2021 firmware line, then "attackers
# drained roughly 1,816 BTC".
TRM = STOCK / "captures/trm-coldcard"
TRM_HEAD = TRM / "head.mp4"
TRM_LINES = TRM / "drained.mp4"
# The address shown in the browser window: the page's real host and path.
TRM_ADDR = "trmlabs.com/resources/blog/coldcard-hack"

BEATGROUND = BRAND / "beat-ground-crypto.jpg"
ENDCARD = V / "subscribe/4928934.mp4"

VOICE = "mia"
MUSIC = music.track("night-drift")
URL = "https://thecrypto.wiki/posts/what-is-a-hardware-wallet"

DISCLAIMER_BG = stillclip.path(COLDCARD_DARK, focus=(0.5, 0.45))


def sections() -> list:
    return [
    # --- hook. No card. The Stamp lands NEVER WAS on "never". -----------------
    Section(
        title="Do you need a hardware wallet?",
        card=False,
        sentences=[
            ("Your crypto is not on your hardware wallet. It never was.",),
            # the grid's own sentence: one chunk per card.
            ("Every coin lives on the blockchain.",
             "The device holds one thing: the key that can move them."),
            ("So what does that key need protecting from, and does a small device really do it?",),
            ("Stay for the 2026 case where nobody touched a device, and about eighteen hundred bitcoin were drained anyway.",),
        ],
        shots=[
            Shot(image=LEDGER_LAPTOP, parallax=0.6),
            Shot(graphic="grid", backdrop=BEATGROUND,
                 payload=([("The blockchain", "holds every coin", "\u26D3\uFE0F"),
                           ("Your device", "holds one key", "\U0001F511")],
                          "WHERE THINGS ARE")),
            None,
            # The case, teased with its own headline, as a page in a tab.
            Shot(clip=TRM_HEAD, clip_at=0.0, window=("browser", TRM_ADDR)),
        ],
        gaps=[0.85, 0.90, 0.70, 0.90],
    ),

    # --- what it does ------------------------------------------------------------
    Section(
        title="What does a hardware wallet actually do?",
        spoken_title="So what does a hardware wallet actually do?",
        kicker="THE KEY",
        sentences=[
            # the spotlight's own sentence: the device, then its screen.
            ("Every wallet does one job:",
             "it signs, with your private key, to prove you approved a transaction."),
            ("On a phone or a laptop, that key sits on a device that's online all day.",),
            # the callout's own sentence: one chunk per label.
            ("A hardware wallet keeps the key on a chip inside,",
             "with its own screen,",
             "and its own buttons, all off the internet."),
            ("That is why it is called a cold wallet.",),
            # the airgap's own sentence: one chunk per crossing.
            ("When you send, your computer prepares the transaction,",
             "the device shows it on its own screen,",
             "you check it and press the button,",
             "and only the signature comes back."),
            ("The key never leaves the chip, so malware on your laptop has nothing to read.",),
        ],
        shots=[
            # A real device asking to confirm a send: the camera goes to its
            # screen as the voice says "it signs".
            Shot(graphic="spotlight",
                 payload=(TREZOR, [(None, ""),
                                   ((0.27, 0.36, 0.73, 0.68), "CONFIRM SENDING")],
                          "ONE JOB")),
            Shot(clip=GLOW, clip_at=0.5, window=("player", "A laptop: online all day")),
            Shot(graphic="callout", backdrop=BEATGROUND,
                 payload=(COLDCARD_HAND,
                          [("The key, on a chip inside", 0.44, 0.30),
                           ("Its own screen", 0.56, 0.40),
                           ("Its own buttons", 0.56, 0.68)],
                          "INSIDE A HARDWARE WALLET")),
            Shot(image=LEDGER_HAND, isolate=1.0),
            Shot(graphic="airgap", backdrop=BEATGROUND,
                 payload=([("Send", "0.5 BTC"), ("To", "bc1q7k...9x4f")],
                          "SENDING FROM A HARDWARE WALLET")),
            None,
        ],
        gaps=[0.70, 0.70, 1.00, 0.70, 1.30, 0.80],
    ),

    # --- the turn: what it can't stop ------------------------------------------------
    Section(
        title="What can't a hardware wallet stop?",
        spoken_title="So what can't a hardware wallet stop?",
        kicker="THE LIMITS",
        card_gap=1.30,
        sentences=[
            ("Actually, more than people think.",),
            # the blindsign's own sentence: card, approval, truth.
            ("It signs whatever you approve.",
             "Press the button on a scammer's request,",
             "and it has done its job perfectly."),
            # the steps' own sentence: one chunk per node.
            ("And your recovery words are the key, written down.",
             "Anyone who reads them can type them into another wallet,",
             "and rebuild your key, without your device."),
            # the compare's own sentence: a heading chunk per column, one per item.
            ("It blocks",
             "malware reading your key,",
             "a thief without your PIN,",
             "and a swapped address, if you read the screen.",
             "It can't stop",
             "a request you approve,",
             "your words typed into a fake site,",
             "or your words lost with the device."),
            ("And in 2026, the device itself failed.",),
            ("A Coldcard firmware release from March 2021 made some wallets create their keys from weak randomness.",),
            # the bars' own sentence: one chunk per row.
            ("Key strength fell from a hundred and twenty-eight bits",
             "to as little as forty: weak enough to guess, without touching the device."),
            # the breach's own sentence: the field, then the waves.
            ("Coins sat in more than five thousand two hundred addresses.",
             "Starting July thirtieth, about eighteen hundred bitcoin were drained, in four waves."),
            ("So a hardware wallet is software too, and its updates matter.",),
        ],
        shots=[
            # "Ready to sign" on its own screen - torn on the turn.
            Shot(image=COLDCARD_READY, zoom=1.08, shader="aberration"),
            Shot(graphic="blindsign", backdrop=BEATGROUND,
                 payload=([("Action", "Send"),
                           ("To", "Your saved address"),
                           ("Fee", "A few cents")],
                          [("Action", "Approve spending"),
                           ("Spender", "Their contract"),
                           ("Limit", "Unlimited")],
                          ["YOU"], "ONE BUTTON")),
            Shot(graphic="steps", backdrop=BEATGROUND,
                 payload=(["Recovery words, written down",
                           "Typed into another wallet",
                           "Your key, without your device"],
                          "THE BACKUP IS THE KEY")),
            Shot(graphic="compare", backdrop=BEATGROUND,
                 payload=("IT BLOCKS",
                          ["Malware reading your key", "A thief without your PIN",
                           "A swapped address, if you read it"],
                          "IT CAN'T STOP",
                          ["A request you approve", "Words typed into a fake site",
                           "Words lost with the device"],
                          True)),
            Shot(image=COLDCARD_DARK, isolate=1.0),
            # TRM Labs' own report, in a tab: the firmware line ringed.
            Shot(clip=TRM_LINES, clip_at=0.0, window=("browser", TRM_ADDR)),
            Shot(graphic="bars", backdrop=BEATGROUND,
                 payload=([("As designed", 1.0, "128 bits"),
                           ("Some wallets", 40 / 128, "40 bits")],
                          "KEY STRENGTH")),
            Shot(graphic="breach", backdrop=BEATGROUND,
                 payload=("5,200+ ADDRESSES", 1816, "BTC", 4, "COLDCARD, 2026",
                          "DRAINED", "1 square = 25 addresses")),
            Shot(image=COLDCARD_KEYS, zoom=1.08),
        ],
        gaps=[1.00, 1.10, 0.90, 1.30, 0.60, 0.80, 1.00, 1.50, 0.80],
    ),

    # --- do you need one -------------------------------------------------------------
    Section(
        title="So do you need one?",
        spoken_title="So, do you need one?",
        kicker="THE TEST",
        sentences=[
            # the grid's own sentence: one chunk per card.
            ("On an exchange, the company holds it.",
             "In a phone app, you hold it, on a device that's always online.",
             "On a hardware wallet, you hold it offline, and the backup is yours alone."),
            ("Exchanges get hacked too: in 2025, Bybit lost about one and a half billion dollars in one transaction.",),
            # the diagram's own sentence: one chunk per node.
            ("If the place your key sits was hacked tonight, would you be fine?",
             "And can you keep your recovery words safe, and secret, for years?",
             "If it is no, then yes, that is the problem a hardware wallet was built for."),
        ],
        shots=[
            Shot(graphic="grid", backdrop=BEATGROUND,
                 payload=([("An exchange", "the company holds your key", "\U0001F3E6"),
                           ("A phone app", "your key, always online", "\U0001F4F1"),
                           ("A hardware wallet", "your key, offline - your backup", "\U0001F512")],
                          "WHERE YOUR KEY SITS")),
            Shot(graphic="stat", backdrop=BEATGROUND,
                 payload=("$1.46B", "taken from Bybit in one transaction",
                          "21 February 2025")),
            Shot(graphic="diagram", backdrop=BEATGROUND,
                 payload=([("Hacked tonight", "would you be fine?"),
                           ("Your recovery words", "safe and secret, for years?"),
                           ("No, then yes", "the problem it was built for")],
                          "TWO QUESTIONS", False)),
        ],
        gaps=[1.30, 0.90, 1.30],
    ),

    # --- close: the echo ------------------------------------------------------------
    Section(
        title="So who can reach your key?",
        spoken_title="So, who can reach your key?",
        kicker="THE ANSWER",
        sentences=[
            # the checklist's own sentence: one chunk per item.
            ("A hardware wallet guards the key.",
             "It can't guard your recovery words,",
             "or the button you press."),
            ("Nothing in this video is financial advice.",),
            ("So, your coins were never on the device. Who else could reach the key right now?",),
        ],
        shots=[
            Shot(graphic="checklist", backdrop=BEATGROUND,
                 payload=([("The key", True),
                           ("Your recovery words", False),
                           ("The button you press", False)],
                          "WHAT IT GUARDS", True)),
            # The video's own device, not weather (2026-11-06).
            Shot(clip=DISCLAIMER_BG, clip_at=0.5,
                 payload=("", "This is not financial advice.")),
            Shot(image=LEDGER_LAPTOP, parallax=0.5),
        ],
        gaps=[1.40, 1.10, 2.30],
    ),
    ]


SECTIONS = sections()

META = Meta(
    title="Do You Need a Hardware Wallet? What It Protects (and What It Doesn't)",
    hook="Your crypto is not on your hardware wallet - it never was. Here is "
         "what the device actually protects, how it signs a transaction, "
         "what it cannot stop, the 2026 Coldcard case where about 1,816 "
         "bitcoin were drained without anyone touching a device, and the two "
         "questions that tell you whether you need one.",
    url=URL,
    summary="Do you need a hardware wallet? What a hardware wallet (cold "
            "wallet) does: your coins live on the blockchain and the device "
            "holds only the private key that signs for them, on a chip that "
            "never goes online; how sending from one works, step by step; "
            "what it blocks (malware reading your key, a thief without your "
            "PIN, a swapped address if you read the device's screen) and "
            "what it cannot stop (a request you approve, recovery words "
            "typed into a fake site or lost with the device); the 2026 "
            "Coldcard case, where a March 2021 firmware bug left some keys "
            "weak enough to guess and about 1,816 BTC were drained from more "
            "than 5,200 addresses (TRM Labs); exchange, phone app or hardware "
            "wallet - who holds your key; and two questions to answer for "
            "yourself. No product is recommended. Nothing here is financial "
            "advice.",
    tags=["do you need a hardware wallet", "hardware wallet", "cold wallet",
          "what is a hardware wallet", "hardware wallet explained",
          "do i need a cold wallet", "hot wallet vs cold wallet",
          "self custody", "private key", "seed phrase", "coldcard hack",
          "crypto security", "crypto wallet", "how does a hardware wallet work"],
    cta=f"The full setup walkthrough, the common mistakes and the backup "
        f"plan, step by step: {URL}",
    credits=["Nothing in this video is financial advice. No product in it is "
             "a recommendation.",
             "Page: TRM Labs, \"The Largest Hardware Wallet Exploit of 2026: "
             "Inside the USD 116 Million Coldcard Hack\" (5 Aug 2026, "
             "captured 12 Nov 2026).",
             "Photos (Wikimedia Commons): Coldcard by Gareth Halfacree, CC "
             "BY-SA 2.0; Coldcard by Tony Webster, CC BY 2.0; Ledger Nano S "
             "by Motokoka, CC BY-SA 4.0 (adapted); Ledger by Roderart, CC BY-SA 4.0 (adapted); "
             "Trezor Model T by FlippyFlink, CC0."],
)

HEADLINE = "Do you\n[need] one?"


def thumbs(out: Path, marks: bool = True) -> Path:
    """The Ledger on its cable at the right, its lit "Bitcoin" screen ringed,
    the video's question in three rows on the black at the left and an arrow
    from it to the screen. The picture is the cover's only (`thumbnails.md`,
    "The cover's picture stays on the cover").

    `marks=False` (`--thumb-plain`) is the same cover with no ring and no
    arrow - a "text" version, kept so either can be picked."""
    import numpy as np
    from PIL import Image
    from video_automation.longform import thumb as T
    src = Image.open(LEDGER_CABLE).convert("RGB")
    pic = src.resize((1100, 825), Image.LANCZOS)
    im = Image.new("RGB", (1280, 720), (0, 0, 0))
    im.paste(pic, (300, -60))
    # fade the picture's left edge into the black the headline sits on
    a = np.ones((720, 1280), np.float32)
    a[:, :300] = 0.0
    a[:, 300:620] = np.linspace(0.0, 1.0, 320)[None, :]
    im = Image.composite(im, Image.new("RGB", im.size, (0, 0, 0)),
                         Image.fromarray((a * 255).astype("uint8")))
    fill, ink = T.ACCENTS["yellow"]
    T._headline(im, HEADLINE, 200, int(560 / 1.38), 48, fill, ink,
                max_lines=3, leading=1.0, band="top", margin=48,
                shadow=12, drop=(5, 6))
    if not marks:
        im.save(out, quality=92)
        return out
    im = im.convert("RGBA")
    im.alpha_composite(T.ring_layer(im.size, RING, width=10))
    im.alpha_composite(T.arrow_layer(im.size, ARROW_FROM, ARROW_TO,
                                     width=18, head=54, bow=-0.25))
    im.convert("RGB").save(out, quality=92)
    return out


# The Ledger's screen in the cover's placement, and the arrow onto it.
RING = (640, 320, 1010, 540)
ARROW_FROM, ARROW_TO = (470, 600), (625, 470)


def main() -> None:
    stillclip.make(COLDCARD_DARK, focus=(0.5, 0.45))
    out = Path.home() / "Desktop/hardware-wallet-long.mp4"
    work = Path.home() / "Desktop/.hardware-wallet-long-work"
    made = render_long(
        SECTIONS, out, work, brand=CRYPTO, meta=META, voice=VOICE,
        music=MUSIC,
        callouts=None,
        # A claim, judged: the coins were never on the device. Last three
        # long forms opened Search / Split / Stamp.
        opener=Stamp("My crypto is on the device", "NEVER WAS",
                     at_word="never", tone="negative"),
        emphasis=["cold wallet", "software too"],
        thumb_headline=HEADLINE,
        thumb_accent="yellow",
        endcard=ENDCARD, endcard_lead=7.0,
    )
    made["thumb"] = thumbs(Path(made["thumb"]))
    for k, v in made.items():
        print(f"{k}: {v}")


if __name__ == "__main__":
    if "--thumb-plain" in sys.argv:
        print(thumbs(Path.home() / "Desktop/hardware-wallet-long-thumb-plain.jpg",
                     marks=False))
    elif "--thumb" in sys.argv:
        print(thumbs(Path.home() / "Desktop/hardware-wallet-long-thumb.jpg"))
    else:
        main()
