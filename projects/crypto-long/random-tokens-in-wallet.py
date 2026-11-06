"""Random tokens in your crypto wallet - long-form 16:9 for YouTube.

Source: crypto-wiki/content/posts/understanding-crypto-airdrops.mdx (its
"Beware of fake tokens" and "Revoke permissions" lines), with address
poisoning from `send-and-receive-crypto-safely` and the recovery-scam
warning from `what-is-a-rug-pull` - all three on the site.

**The angle.** A re-angle of the airdrops article onto the moment the
viewer is in. Cyber Scrilla's "If you find random Crypto in your wallet...
DO THIS" is 11.7x its channel (235k), and every "how to spot a fake airdrop"
title beside it sits at 0-2x (`demand/teardowns/random-crypto-in-your-
wallet.md`). The standout names the moment, not the category, and its first
real payoff is the reassurance - receiving is harmless, interacting is the
danger - so that is our hook. Its most replayed stretch is the address-
poisoning fix; its open comments are "can I just delete it?", "how do they
make a look-alike address?", "a cold wallet protects you" (it does not) and
"how do I get it back?" (the recovery scam). This answers each, in that
order, with two scams instead of their three.

**A mechanism, so the default arc** (`longform.md`); the turn is the
hardware-wallet chapter ("Actually, no"), and the climax is the look-alike
address, drawn.

**Every figure is sourced or arithmetic.** 1,155 wrapped bitcoin, about $68M,
sent to a look-alike on 3 May 2024, nearly all returned by 10 May (CoinDesk,
Cointelegraph). 270M poisoning attempts on Ethereum and BNB Chain, July 2022
to June 2024 (Tsuchiya et al., "Blockchain Address Poisoning", USENIX
Security 2025). Four hex characters at each end is 16^8, about 4.3 billion
tries. The addresses in the `lookalike` beat are made up for the picture
and say so in the description; the `blindsign` rows are an illustration of
a claim screen, not a quoted one.

## The beats

Last three crypto long forms: crypto-billionaires (reel / compare / stake /
bars / stat), gta-6-crypto (timeline / quote / checklist / diagram / chart),
what-are-memecoins (compare / stat / steps / pool / grid).

* `diagram` - how the token reached you: the public chain, a script, a
  thousand wallets, one bite. Icons that all animate (🌍 🤖 🎁 🎣).
* `blindsign` - the claim screen, one signature, and the approval under it.
* `pile` - the tokens in the wallet, then the floor opening: the approval
  being used.
* `behind` - OFFLINE between the site's Ledger photograph and its room:
  what a hardware wallet does protect, before the turn says what it cannot.
* `lookalike` - **new, built for this video.** Two addresses with the same
  ends and a different middle. The library could not set two strings
  against each other.
* `post` - CoinDesk's real headline on the $68M case.
* `stat` - 270M attempts.
* `checklist`, flow - the 2026-11-06 note card: two crosses, two ticks.

**Opener: `Stamp`** on the fear the viewer arrives with ("My wallet got
hacked"), stamped WRONG on "hacked" - it judges the viewer's claim about
what happened, never an asset. Last three long forms opened Search / Stamp
/ Counter.

**Footage: the act, in the subject's world** - a phone lighting up on a
nightstand, hands on a phone in the dark, a trading app, a laptop of code,
a laptop carrying our drawn claim page (`screenfill`), a graphics card, a
Trezor asking to sign (Commons), keycaps spelling SCAM, and captured pages -
Blockscout's transfers and Revoke.cash. Verdicts in `footage.md`.

    PYTHONPATH=. .venv/bin/python projects/crypto-long/random-tokens-in-wallet.py
"""

import sys
from pathlib import Path
from pathlib import Path as _P

from video_automation.core import music, screenfill, stillclip
from video_automation.core.brand import CRYPTO
from video_automation.core.stock import CACHE as STOCK
from video_automation.crypto.shots import Shot

from video_automation.longform import Meta, Section, render_long
from video_automation.longform.openers import Stamp

SOURCE_POST = "understanding-crypto-airdrops"
DEMAND = ("Cyber Scrilla 'If you find random Crypto in your wallet... DO THIS' "
          "11.7x (235k); Adam Venture '3 Crypto Scams YOU WILL Fall For' "
          "26.5x - re-angle of the airdrops article")

V = STOCK / "videos"
ROOT = _P(__file__).resolve().parents[2]
BRAND = ROOT / "assets/brand"

# Fetched fresh for this pair, contact-sheeted at 15/50/85%. Luma sampled at
# 0.5/3/6/9s. **No clip whose phone screen shows a social feed** - the first
# cut ran four of them (a TikTok scroll, an Instagram grid by a candle, a feed
# in bed) and the editor called each one irrelevant (2026-11-06).
NIGHTSTAND = V / "phone-vibrating-on-table-dark/35999376.mp4"            # 10s, L34, a phone lights up on a nightstand - the token arriving
PHONEDARK = V / "holding-smartphone-dark-background-close-up/13358555.mp4"  # 14s, L14, two hands on a glowing phone in black - opens
HOLD = V / "holding-smartphone-dark-background-close-up/7534329.mp4"     # 15s, L33-37, hands turning a phone over, dark, no screen
TRADE = V / "cryptocurrency-app-on-phone/8480231.mp4"                    # 11s, L48-54, a trading app on a phone over a laptop - trying to sell
DESK = V / "thumb-scrolling-phone-close-up/17586687.mp4"                 # 12s, L35, a hand at a phone on a dark desk
CODE = V / "laptop-screen-glow-dark-room-hands/13522186.mp4"             # 13s, L36, a laptop of code, hands at the keys
# Its screen is blank white; the editor: "either replace the clip or add
# something on top" (2026-11-06). It carries our drawn claim page instead
# (`screenfill`), so the clip is named here and made in `main()`.
LAPTOP = V / "laptop-screen-glow-dark-room-hands/6611947.mp4"            # 11s, L50, hands on a laptop with a blank lit screen - the claim site
GPU = V / "graphics-card-fan-spinning/3147349.mp4"                       # 20s, L41-48, a graphics card's fan, purple-lit
LAMPLAPTOP = V / "using-laptop-at-night-dark-room/7272375.mp4"           # 20s, L14-18, hands at a laptop under a lamp; it closes at the end
ETHCOIN = V / "crypto-wallet-qr-code/10243081.mp4"                       # an Ether coin on black, green code falling behind it - the public chain
SCAMKEYS = V / "hacker-hands-keyboard-dark-hoodie/6964023.mp4"           # 14s, a hooded figure holding out keycaps that spell SCAM - the recovery offer
# Cut on review (2026-11-06): CHIP circuit-board-macro-dark/6755158 (a chip
# is not a wallet), SETTINGS settings-toggle-on-phone/7326142 (a calendar on
# the screen), CHAT woman-hands-phone-dark-room/5617952 (its chat reads "im
# lonely" from about 4.5s).

# The real thing: a public Ethereum address (the burn address, which nobody
# owns) receiving token transfers from strangers, captured on Blockscout
# 2026-11-06 (`screencap`, record in `captures/blockscout-dead.json`; prices
# and ads hidden). The spoof token "vitalek buteren" is on it.
CAPS = STOCK / "captures/blockscout-dead"
ADDRESS = CAPS / "address.mp4"     # 11s: the address, then its token transfers
SPOOF = CAPS / "spoof.mp4"         # 9s: the list, then the spoof token's name ringed
HISTORY = CAPS / "history.mp4"     # 9s: the transfers, the top row ringed
# Revoke.cash, which the airdrops article names for revoking, on the same
# address: Revoke Selected ringed, then APPROVALS 0 / VALUE AT RISK $0 -
# the state the viewer is after (`captures/revoke-dead/revoke-dead.json`).
REVOKE = STOCK / "captures/revoke-dead/revoke.mp4"

# The site's own hardware-wallet pictures (the editor's ask, 2026-11-06).
POSTS = _P.home() / "Coding/crypto-wiki/public/images/posts"
LEDGER = POSTS / "ledger.jpeg"                      # 1500px, hands holding a Ledger on its cable
WALLETS = POSTS / "what-is-a-hardware-wallet.jpg"   # 800px, a Trezor and a Ledger on slats
# Pexels has no hardware wallet; Wikimedia Commons does. A Trezor's own
# confirm screen, "Hold to sign", in two hands (CC0, `CREDITS.md`).
TREZOR = ROOT / "assets/crypto/random-tokens/trezor-hold-to-sign.jpg"
# Our drawn claim page, on the laptop's blank screen.
SITE = ROOT / "assets/crypto/random-tokens/claim-site.png"
SITE_SEARCH = (0.15, 0.0, 0.85, 0.6)     # the panel, not the lit palm rest

# The cover's picture, also the disclaimer's: a stranger holding out coins.
# AI-generated, supplied by the editor, no credit owed.
STRANGER = ROOT / "assets/crypto/random-tokens/stranger.jpg"

BEATGROUND = BRAND / "beat-ground-crypto.jpg"
ENDCARD = V / "subscribe/4928934.mp4"

VOICE = "mia"
MUSIC = music.track("night-drift")
URL = "https://thecrypto.wiki/posts/understanding-crypto-airdrops"

# Made up for the picture: the same first four and last four characters
# after 0x, every middle character different.
REAL = "0x7a3fC09e5d21b84F6c3A9e07d14B2f58c6E1d4b9"
FAKE = "0x7a3f8b1E06cD94a7F2e5B13c09A8d6E4f27Bd4b9"


def _usd(s: str) -> tuple:
    """The caption keeps the figure; the voice reads it."""
    return (s, s.replace("$68M", "sixty-eight million dollars"))


# The stranger as a slow push the notice card can sit on. The shot list
# names the clip; `main()` makes it, so importing this file draws nothing.
DISCLAIMER_BG = stillclip.path(STRANGER, focus=(0.5, 0.2))
CLAIM = screenfill.path(LAPTOP, SITE, search=SITE_SEARCH)


def sections() -> list:
    bg = DISCLAIMER_BG
    return [
    # --- hook. No card. The Stamp lands on "hacked". -------------------------
    Section(
        title="Random tokens in your wallet",
        card=False,
        sentences=[
            ("A token you never bought just showed up in your crypto wallet.",),
            ("Nobody hacked you.",),
            ("Anyone can send crypto to any address, and receiving it is harmless.",),
            ("The danger starts the moment you try to do something with it.",),
            ("So where did it come from, and what is it waiting for you to do?",),
            # "copy and paste" read with a hole after "copy", and "copy-paste"
            # still left a 0.17s gap there (2026-11-06): no compound at all.
            ("Stay to the end for the pasted address that cost one person sixty-eight million dollars.",),
        ],
        shots=[
            Shot(clip=PHONEDARK, clip_at=1.0),
            Shot(clip=NIGHTSTAND, clip_at=0.5),
            Shot(clip=HOLD, clip_at=1.0),
            Shot(clip=TRADE, clip_at=0.5),
            None,
            Shot(clip=DESK, clip_at=1.0),
        ],
        gaps=[0.70, 0.85, 0.60, 0.80, 0.70, 0.90],
    ),

    # --- how it got there ------------------------------------------------------
    Section(
        title="How did it get into your wallet?",
        spoken_title="So how did it get into your wallet?",
        kicker="THE OPEN ADDRESS",
        sentences=[
            ("Your wallet address works like an email address.",),
            ("Anyone who has it can send you something, and there is no button to refuse a transfer.",),
            # the diagram's own sentence: one chunk per box.
            ("Every address you have used sits on a public blockchain.",
             "A script reads it,",
             "sends the same token to thousands of active wallets,",
             "and waits for one person to bite."),
            ("So getting one says nothing about your security. It only says your address is in use.",),
        ],
        shots=[
            # A real address taking transfers from strangers, held across
            # both sentences - the ring moves to its token transfers.
            Shot(clip=ADDRESS, clip_at=0.0),
            None,
            Shot(graphic="diagram", backdrop=BEATGROUND,
                 payload=([("Public blockchain", "every address readable", "\U0001F30D"),
                           ("A script", "reads it for active wallets", "\U0001F916"),
                           ("Thousands of wallets", "the same free token", "\U0001F381"),
                           ("One bite", "is all it needs", "\U0001F3A3")],
                          "HOW IT REACHED YOU", False)),
            Shot(clip=ETHCOIN, clip_at=1.0),
        ],
        gaps=[0.55, 0.80, 1.30, 0.90],
    ),

    # --- the bait ---------------------------------------------------------------
    Section(
        title="What does the token want?",
        spoken_title="So what does the token actually want from you?",
        kicker="THE BAIT",
        sentences=[
            ("Look at its name. Often it is a website, a reward to claim, or a famous name, misspelled.",),
            ("Try to sell it, and you are told to claim it, or enable trading, first.",),
            ("That sends you to a site, which asks you to connect your wallet and approve one small transaction.",),
            # the blindsign's own sentence: card, approval, truth.
            ("Your screen shows a claim, with a fee of a few cents.",
             "You approve it.",
             "But what you signed lets their contract move your tokens, with no limit."),
            # the pile's own sentence: the tokens in, then the floor opening.
            ("Your tokens sit in the wallet.",
             "Their contract drains it, and the approval stays open until you revoke it."),
        ],
        shots=[
            Shot(clip=SPOOF, clip_at=0.0),
            Shot(clip=HOLD, clip_at=6.5),
            Shot(clip=CLAIM, clip_at=1.0),
            Shot(graphic="blindsign", backdrop=BEATGROUND,
                 payload=([("Action", "Claim reward"),
                           ("Amount", "5,000 tokens"),
                           ("Network fee", "A few cents")],
                          [("Action", "Approve spending"),
                           ("Spender", "Their contract"),
                           ("Limit", "Unlimited")],
                          ["YOU"], "ONE SIGNATURE")),
            Shot(graphic="pile", backdrop=BEATGROUND,
                 payload=([(40, "YOUR TOKENS")], "ONE APPROVAL", "THEIR CONTRACT")),
        ],
        gaps=[0.60, 0.70, 0.70, 1.90, 1.40],
    ),

    # --- the turn: the hardware wallet ------------------------------------------
    Section(
        title="Doesn't a hardware wallet stop this?",
        spoken_title="So doesn't a hardware wallet stop this?",
        kicker="THE SIGNATURE",
        card_gap=1.30,
        sentences=[
            ("Actually, no.",),
            # the behind's own sentence: the word, then its line.
            ("A hardware wallet keeps your private keys on a chip,",
             "off the internet, and that matters."),
            ("But it signs whatever you approve.",),
            ("Press the button on a drainer's request, and the device has done its job perfectly.",),
            ("It protects your private keys. It cannot protect the decision.",),
        ],
        shots=[
            # Not a chip (2026-11-06): the site's two wallets, the room
            # dimming round them on the turn.
            Shot(image=WALLETS, isolate=1.0),
            # The photo whole, OFFLINE on top - the cutout frayed round the
            # fingers, the editor's call (2026-11-06).
            Shot(graphic="behind",
                 payload=(LEDGER, "OFFLINE", "Your keys never touch the internet",
                          "fly", None, False)),
            # "It signs whatever you approve" on a wallet asking to sign,
            # held through the button press.
            Shot(image=TREZOR, aspect=16 / 9),
            None,
            Shot(clip=PHONEDARK, clip_at=6.0),
        ],
        gaps=[0.90, 0.70, 0.85, 0.70, 0.90],
    ),

    # --- address poisoning --------------------------------------------------------
    Section(
        title="What is address poisoning?",
        spoken_title="So what is address poisoning?",
        kicker="THE LOOK-ALIKE",
        sentences=[
            ("Sometimes the strange transfer is not a new token at all.",),
            ("It is a tiny amount, from an address that looks almost exactly like one you use.",),
            ("A computer generates addresses until the first and last characters match yours.",),
            ("Four at each end takes about four billion tries, which a graphics card gets through in minutes.",),
            # the lookalike's own sentence: one chunk per reveal.
            ("Your real address.",
             "Their look-alike.",
             "The same start, and the same end.",
             "And a different middle, where nobody looks."),
            ("Now it sits at the top of your history, and the next time you copy from there, you pay them.",),
            # the post's own sentence: the lead-in, then the headline read.
            ("In May 2024, one person did exactly that.",
             _usd("Exploiter steals $68M worth of crypto through address poisoning.")),
            ("A week later the thief sent almost all of it back, which almost never happens.",),
            ("A 2025 study counted two hundred and seventy million poisoning attempts, on just two blockchains, in two years.",),
        ],
        shots=[
            Shot(clip=LAMPLAPTOP, clip_at=1.0),
            None,
            Shot(clip=CODE, clip_at=5.0),
            Shot(clip=GPU, clip_at=1.0,
                 note=("4.3 BILLION", "tries to match four characters at each end")),
            Shot(graphic="lookalike", backdrop=BEATGROUND, shader="bloom",
                 payload=(REAL, FAKE, "THE LOOK-ALIKE", (4, 4))),
            Shot(clip=HISTORY, clip_at=0.0),
            Shot(graphic="post", backdrop=BEATGROUND,
                 payload=("headline",
                          {"source": "CoinDesk", "date": "3 May 2024",
                           "headline": "Exploiter Steals [$68M] Worth of Crypto "
                                       "Through Address Poisoning"},
                          "")),
            # The headline holds through what happened next.
            None,
            Shot(graphic="stat", backdrop=BEATGROUND,
                 payload=("270M", "poisoning attempts",
                          "Ethereum and BNB Chain, 2022 to 2024")),
        ],
        gaps=[0.55, 0.70, 0.60, 0.80, 1.40, 0.85, 1.20, 0.70, 0.90],
    ),

    # --- what to do -----------------------------------------------------------------
    Section(
        title="What should you do with it?",
        spoken_title="So what should you actually do when one shows up?",
        kicker="THE RULES",
        sentences=[
            # the checklist's own sentence: one chunk per item, verdicts as said.
            ("Don't sell it, swap it, or visit the site in its name.",
             "Don't copy an address from your history.",
             "Copy it from the receive screen of whoever you are paying.",
             "And hide the token. Leave it alone."),
            ("Then check every character, not just the ends.",),
            ("If you already signed something, revoke the approval from a clean wallet, and move what is left to a new one.",),
            ("And ignore anyone who offers to recover it for a fee.",
             "That is the second scam."),
        ],
        shots=[
            Shot(graphic="checklist", backdrop=BEATGROUND,
                 payload=([("Sell it, swap it, visit its site", False),
                           ("Copy from your history", False),
                           ("Copy from the receive screen", True),
                           ("Hide it, leave it alone", True)],
                          "WHEN ONE SHOWS UP", True)),
            # The note holds while the last rule is said.
            None,
            Shot(clip=REVOKE, clip_at=0.0),
            Shot(clip=SCAMKEYS, clip_at=1.0),
        ],
        gaps=[2.40, 0.80, 0.70, 0.90],
    ),

    # --- close: the echo ----------------------------------------------------------
    Section(
        title="So is a random token dangerous?",
        spoken_title="So, is a random token dangerous?",
        kicker="THE ANSWER",
        sentences=[
            ("On its own, it cannot take a thing.",),
            ("It needs your signature, or a pasted address.",),
            ("Nothing in this video is financial advice.",),
            ("So, the last address you pasted: did you check the middle?",),
        ],
        shots=[
            Shot(clip=LAMPLAPTOP, clip_at=10.0),
            None,
            # The video's own stranger, not weather (2026-11-06).
            Shot(clip=bg, clip_at=0.5,
                 payload=("", "This is not financial advice.")),
            Shot(clip=DESK, clip_at=4.0),
        ],
        gaps=[0.80, 1.00, 1.10, 2.30],
    ),
    ]


SECTIONS = sections()

META = Meta(
    title="Random Tokens in Your Crypto Wallet? Don't Touch Them",
    hook="A token you never bought showed up in your crypto wallet. Nobody "
         "hacked you - anyone can send crypto to any address. Here is where "
         "it came from, what it wants you to sign, why a hardware wallet "
         "will not stop it, how address poisoning works, and what to do.",
    url=URL,
    summary="Random tokens in your crypto wallet, explained: why anyone can "
            "send crypto to your address and why receiving it is harmless; "
            "how scam tokens point you to a site that asks for one approval, "
            "and how that approval lets a drainer contract move your tokens "
            "with no limit; why a hardware wallet signs whatever you approve; "
            "how address poisoning works - a look-alike address with the same "
            "first and last characters, a tiny transfer into your history, "
            "and the May 2024 case where 1,155 wrapped bitcoin (about $68M) "
            "went to one; a 2025 study's 270 million poisoning attempts; and "
            "the rules - don't sell it or visit its site, copy addresses from "
            "the source, check the whole address, revoke approvals, and "
            "ignore recovery offers. The addresses shown are made up for the "
            "picture. Nothing here is financial advice.",
    tags=["random tokens in crypto wallet", "random crypto in my wallet",
          "unknown tokens in wallet", "someone sent me crypto",
          "airdrop scam", "fake airdrop", "scam tokens", "address poisoning",
          "address poisoning scam", "wallet drainer", "token approval",
          "revoke token approval", "hardware wallet", "crypto scams"],
    cta=f"Real airdrops versus fake ones, and the full safety checklist: {URL}",
    credits=["Nothing in this video is financial advice.",
             "Headline: CoinDesk, 3 May 2024. Study: Tsuchiya et al., "
             "\"Blockchain Address Poisoning\", USENIX Security 2025.",
             "The wallet addresses shown are made up for illustration, and "
             "so is the claim page.",
             "Trezor photo: FlippyFlink, Wikimedia Commons, CC0."],
)

HEADLINE = "Free crypto\nfrom a\n[stranger?]"


def thumbs(out: Path) -> Path:
    """The editor's stranger holding out coins, whole on the right, and the
    Short's question - the editor's pick, "more catchy" than the long's own
    (2026-11-06) - in three rows on the black to his left. The picture slides
    right and feathers into its own near-black ground; he is never faded or
    crossed (`thumbnails.md`, rule 1)."""
    import numpy as np
    from PIL import Image, ImageEnhance
    from video_automation.longform import thumb as T
    src = Image.open(STRANGER).convert("RGB")
    h = 720
    pic = src.resize((int(src.width * h / src.height), h), Image.LANCZOS)
    edge = tuple(int(c) for c in
                 np.asarray(pic)[:, :30].reshape(-1, 3).mean(0))
    im = Image.new("RGB", (1280, 720), edge)
    x = 1280 - pic.width + 170          # his centre at ~x 900
    feather = 200
    mask = np.ones((h, pic.width), np.float32)
    mask[:, :feather] = np.linspace(0.0, 1.0, feather)
    im.paste(pic, (x, 0), Image.fromarray((mask * 255).astype("uint8")))
    im = ImageEnhance.Brightness(im).enhance(1.04)
    fill, ink = T.ACCENTS["yellow"]
    T._headline(im, HEADLINE, 190, int(560 / 1.38), 40, fill, ink,
                max_lines=3, leading=1.0, band="middle", margin=34,
                shadow=12, drop=(5, 6))
    im.save(out, quality=92)
    return out


def main() -> None:
    stillclip.make(STRANGER, focus=(0.5, 0.2))
    screenfill.make(LAPTOP, SITE, search=SITE_SEARCH)
    out = Path.home() / "Desktop/random-tokens-long.mp4"
    work = Path.home() / "Desktop/.random-tokens-long-work"
    made = render_long(
        SECTIONS, out, work, brand=CRYPTO, meta=META, voice=VOICE,
        music=MUSIC,
        callouts=None,
        # The fear the viewer arrives with. Last three long forms opened
        # Search / Stamp / Counter.
        opener=Stamp("My wallet got hacked", "WRONG", at_word="hacked"),
        emphasis=["harmless", "whatever you approve", "you pay them",
                  "every character"],
        thumb_headline=HEADLINE,
        thumb_accent="yellow",
        endcard=ENDCARD, endcard_lead=7.0,
        title_at=10.5, title_hold=5.4,
    )
    made["thumb"] = thumbs(Path(made["thumb"]))
    for k, v in made.items():
        print(f"{k}: {v}")


if __name__ == "__main__":
    if "--thumb" in sys.argv:
        print(thumbs(Path.home() / "Desktop/random-tokens-long-thumb.jpg"))
    else:
        main()
