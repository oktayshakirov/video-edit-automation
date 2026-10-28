"""What happens to your crypto when you die? - long-form 16:9 for YouTube.

Source: crypto-wiki/content/posts/what-happens-to-crypto-when-you-die.mdx.

**The angle.** Everyone assumes crypto passes on like everything else: a will,
a court, some paperwork. The video's job is the mechanism that breaks that
assumption. A bank resets access because it knows who you are; a blockchain
checks one thing, a signature from the right private key, and no court can
make one. From there the two routes: coins on a custodial exchange go through
an estate process like any other account, and coins you hold yourself pass on
only if someone can find the keys. The twist is where people would put them
first - the will - which in many places becomes a public record in probate.
The mirror is what works (a sealed letter that says where, never what; a
two-of-three wallet), with Hal Finney's own 2013 plan as the human case. The
close echoes the open: a court decides who should get it, only the keys
decide whether anyone can.

**No financial or legal advice.** No coin, platform or price is named as a
choice. The setups are the article's own, described as mechanisms, and the
closing compliance line covers legal advice as well, because the article does.

**Figures, each said as an estimate.** 21 million bitcoin, ever. An estimated
3.0-3.7 million likely irretrievable (the article's "independent analyses").
Probate commonly 3-12 months by jurisdiction (the article). Hal Finney received
the first bitcoin transaction from Satoshi (block 170, January 2009); his post
"Bitcoin and me (Hal Finney)", bitcointalk, 19 March 2013: "My bitcoins are
stored in our safe deposit box, and my son and daughter are tech savvy." He
wrote it paralysed by ALS, diagnosed 2009 ("a fatal disease", his words).

**Spoken around:** "ALS" phonemizes as one syllable (`ælz`), so the voice says
"a fatal illness", which is Finney's own phrase.

## The beats

Last three crypto long forms: vitalik-ethereum (compare / grid / quote / stat /
steps), what-are-memecoins (compare / stat / steps / pool / grid), gta-6-crypto
(chart / checklist / diagram / quote / timeline). None of those five is here
except `checklist`, last used three videos back.

* `bars` - 21 million against the 3-3.7 million thought lost: a proportion,
  the one thing narration cannot say.
* `reel` - the exchange's estate process, one card per step, the camera
  travelling along them. First use in a shipped cut.
* `checklist` (flow) - where the seed phrase goes, each place judged as it is
  said, titled as the question the crosses answer.
* `quorum` - **new, built for this video.** A lock that needs two of three
  keys; the keys arrive as their holders are named, one is struck, the other
  two open it. The library could not draw a multisig wallet.
* `post` - Hal Finney's 2013 line about his own coins, the real wording.

**Opener: `Search`.** The title is the phrase people type, and last three long
forms opened hook / Counter / Stamp.

**Footage: the act, in the subject's world** - a face scan, a judge's hands,
papers being signed, a phone call to an office, a safe, an envelope being
sealed, drawers of records. Every clip fetched fresh for this pair and checked
on a labelled contact sheet; clips used by any other video were dropped even
where they were the better picture. Verdicts in `footage.md`.

    PYTHONPATH=. .venv/bin/python projects/crypto-long/crypto-when-you-die.py
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

SOURCE_POST = "what-happens-to-crypto-when-you-die"

V = STOCK / "videos"
P = STOCK / "photos"
ROOT = _P(__file__).resolve().parents[2]
BRAND = ROOT / "assets/brand"
SITE = ROOT.parent / "crypto-wiki/public/images/posts"

# Fetched fresh for this pair, looked at on a labelled three-frame contact
# sheet (15/50/85%). Luma sampled at 0.5/3/6/9s.
JUDGE = V / "judge-gavel-courtroom/6101367.mp4"            # 11s, L33, a judge's hands folded by a gavel, face out of frame
HANDS = V / "elderly-hands-holding/8057825.mp4"            # 7s,  L76, two people holding hands
USB = V / "usb-device-plugged-laptop-dark/40304895.mp4"    # 10s, L49, a device plugged into a laptop in the dark
WINDOW = V / "man-thinking-dark-window/33972359.mp4"       # 24s, L94, a man standing still by a curtain
WRITE = V / "writing-on-paper-notebook-night/39425741.mp4"  # 14s, L62, a hand writing in a notebook under a lamp
SCAN = V / "face-id-unlock-phone-dark/8090419.mp4"         # 35s, L27, a face scanned by a red line
SUPPORT = V / "customer-support-headset-night/5452679.mp4"  # 15s, L77, a support agent on a headset
ETCH = V / "metal-plate-engraving/30455960.mp4"            # 17s, L62, a machine engraving metal
DRIVE = V / "old-hard-drive-computer/7841655.mp4"          # 31s, L109, an opened hard drive, platter spinning
CALL = V / "phone-call-desk-night/8061371.mp4"             # 21s, L60, a woman on the phone in an office
NOTARY = V / "notary-stamping-document/8731441.mp4"        # 14s, L80, a hand signing papers by a law book
SIGN = V / "signing-documents-desk-lamp/8061370.mp4"       # 9s,  L81, hands signing a stack of papers
LAWBOOK = V / "lawyer-office-documents-night/8731589.mp4"  # 11s, L59, a "THE LAW" book against a leather bag
LETTER = V / "reading-letter-by-window/8171550.mp4"        # 9s,  L48, a woman reading a letter
ARCHIVE = V / "archive-files-shelves/6550428.mp4"          # 20s, L113, rows of record drawers - bright, but the noun
ENVELOPE = V / "sealed-envelope-wax-seal/5916730.mp4"      # 18s, L80, hands sealing an envelope
VAULT = V / "safe-deposit-box-bank-vault/31750573.mp4"     # 10s, L66, coins poured into a deposit box
RAIN = V / "rain-on-window-night/4458918.mp4"              # 10s, L20, rain on a window, a street lamp - the one abstract

LEDGER = SITE / "ledger.jpeg"                     # 1500x997, a hand holding a hardware wallet - the site's own
BOXES = P / "safe-deposit-box/5332291.jpg"        # 6000x4000, L75, a wall of deposit boxes, monochrome
DIAL = P / "safe-deposit-box/32334240.jpg"        # 9504x6336, L51, a safe's dial in the dark
KEYPAD = P / "wall-safe/1990764.jpg"              # 6048x4024, L73, a keypad safe
# Both covers, the editor's pick: a man in a trench coat at a grave, a stone
# cross dark in the left foreground. Pexels 10499499, cottonbro studio.
GRAVE = P / "man-at-grave/10499499.jpg"           # 6073x4049, L49, the man at ~0.55-0.83 of the width

BEATGROUND = BRAND / "beat-ground-crypto.jpg"
ENDCARD = V / "subscribe/4928934.mp4"

VOICE = "noah"
MUSIC = music.track("night-drift")
URL = "https://thecrypto.wiki/posts/what-happens-to-crypto-when-you-die"

FINNEY = {"name": "Hal Finney", "handle": "bitcointalk.org",
          "date": "19 Mar 2013",
          "text": "Those discussions about inheriting your bitcoins are of "
                  "more than academic interest. [My bitcoins are stored in "
                  "our safe deposit box, and my son and daughter are tech "
                  "savvy.]"}


SECTIONS = [
    # --- hook. No card. The Search types the title over sentence 1. --------
    Section(
        title="What happens to your crypto when you die?",
        card=False,
        sentences=[
            ("No court can unlock a crypto wallet you hold yourself.",),
            ("Not even for your family, after you die.",),
            ("If the keys are gone, the coins never move again.",),
            ("So what actually happens to your crypto when you die?",),
            ("Stay to the end, and you will know the one place",
             "you should never write your seed phrase.",
             "It is the place most people would pick first."),
        ],
        shots=[
            Shot(clip=JUDGE, clip_at=1.0),
            Shot(clip=HANDS, clip_at=2.0),
            Shot(clip=USB, clip_at=1.0),
            Shot(clip=WINDOW, clip_at=2.0),
            Shot(clip=WRITE, clip_at=1.0),
        ],
        gaps=[0.80, 0.85, 0.85, 0.90, 0.90],
    ),

    # --- the keys ------------------------------------------------------------
    Section(
        title="Who actually controls your crypto?",
        spoken_title="So who actually controls your crypto?",
        kicker="THE KEYS",
        sentences=[
            ("A bank knows who you are.",),
            ("Lose your password, and it lets you back in,",
             "because your identity is the lock."),
            ("Crypto flips that around.",),
            ("The blockchain has no idea who you are.",
             "It checks one thing: a signature made with the right private key."),
            ("Whoever can make that signature controls the coins.",),
            ("Nobody else can. Not a judge, and not a support team.",),
            ("Most wallets keep that private key as a seed phrase,",
             "twelve or twenty-four plain words that can rebuild the whole wallet."),
            ("No key, no coins.",),
            # the bars' own sentence: one chunk per row.
            ("Bitcoin will only ever have twenty-one million coins.",
             "An estimated three to three point seven million of them are probably gone for good."),
        ],
        shots=[
            Shot(clip=SCAN, clip_at=1.0),
            None,
            Shot(image=LEDGER, zoom=1.08, pan=(0.02, 0.0)),
            None,
            Shot(clip=SUPPORT, clip_at=1.0),
            None,
            Shot(clip=ETCH, clip_at=2.0,
                 note=("12-24 words", "a seed phrase: the whole wallet")),
            None,
            Shot(graphic="bars", backdrop=BEATGROUND,
                 payload=([("All bitcoin, ever", 1.0, "21M"),
                           ("Likely lost for good", 0.176, "3-3.7M")],
                          "LOCKED AWAY FOR GOOD")),
        ],
        gaps=[0.45, 0.80, 0.55, 0.60, 0.45, 0.70, 0.55, 0.90, 1.30],
    ),

    # --- the exchange route --------------------------------------------------
    Section(
        title="What if your crypto is on an exchange?",
        spoken_title="So what happens if your crypto sits on an exchange?",
        kicker="THE EXCHANGE",
        sentences=[
            ("Then the exchange holds the keys for you, and that is the easier case.",),
            # the reel: one sentence per card, held across with None.
            ("Your family contacts the exchange and opens an estate case.",),
            ("They send a death certificate, and court papers naming an executor.",),
            ("The account is frozen while every document is checked.",),
            ("Then the coins move to the estate, or are sold, as the papers say.",),
            ("Probate alone often takes three to twelve months.",),
            ("But none of it starts if nobody knows which exchanges you used.",),
        ],
        shots=[
            Shot(image=BOXES, zoom=1.08, pan=(0.0, 0.02)),
            Shot(graphic="reel",
                 payload=([(CALL, "The case"),
                           (NOTARY, "The papers"),
                           (None, "Frozen"),
                           (SIGN, "The transfer")],
                          "THE ESTATE PROCESS")),
            None,
            None,
            None,
            Shot(clip=LAWBOOK, clip_at=1.0,
                 note=("3-12 months", "a typical probate, by country")),
            Shot(clip=WINDOW, clip_at=12.0),
        ],
        gaps=[0.70, 0.45, 0.45, 0.45, 0.80, 0.80, 0.90],
    ),

    # --- self-custody ---------------------------------------------------------
    Section(
        title="What if you hold the keys yourself?",
        spoken_title="And what if you hold the keys yourself?",
        kicker="THE WALLET",
        sentences=[
            ("Then there is no estate department.",
             "No form, no support line, no reset."),
            ("Your family gets the coins only if they can find the wallet,",
             "and the seed phrase that opens it."),
            ("That phrase has to be easy for them to find, and hard for anyone else.",
             "So where do you keep it?"),
            # the checklist's own sentence (flow): each chunk says its verdict.
            ("Only in your head? Then your family never finds it.",
             "In a desk drawer? So does anyone who breaks in.",
             "Written into your will? That one is the worst of all."),
        ],
        shots=[
            Shot(clip=VAULT, clip_at=1.0),
            Shot(image=DIAL, zoom=1.08, pan=(-0.02, 0.0)),
            None,
            Shot(graphic="checklist", backdrop=BEATGROUND,
                 payload=([("Only in your head", False),
                           ("In a desk drawer", False),
                           ("Written into your will", False)],
                          "FINDABLE, AND SAFE?", True)),
        ],
        gaps=[0.60, 0.70, 0.90, 1.20],
    ),

    # --- the twist: the will --------------------------------------------------
    # The turning point, so the card gets the longer silence.
    Section(
        title="Why is a will the worst place?",
        spoken_title="So why is a will the worst place of all?",
        kicker="THE CATCH",
        card_gap=1.30,
        sentences=[
            ("A will feels safe.",
             "It is the one document your family is sure to read."),
            ("But in many countries, a will becomes a public record",
             "once it goes through probate."),
            ("Write your seed phrase into it,",
             "and you may have published the key to your coins."),
            ("So let the will name your crypto, and say where the instructions are kept.",
             "Never the words themselves."),
        ],
        shots=[
            Shot(clip=LETTER, clip_at=0.5),
            Shot(clip=ARCHIVE, clip_at=2.0),
            Shot(clip=WRITE, clip_at=7.0),
            Shot(clip=NOTARY, clip_at=7.0),
        ],
        gaps=[0.85, 0.70, 0.85, 0.90],
    ),

    # --- the mirror: what works -----------------------------------------------
    Section(
        title="So what actually works?",
        spoken_title="So what actually works?",
        kicker="THE PLAN",
        sentences=[
            ("Every setup that works does two things at once.",
             "Your family can find the keys, and no single person can take them early."),
            ("The simple version: a hardware wallet in a safe,",
             "its seed phrase split across two places."),
            ("A sealed letter with your will says where each piece is.",
             "Never what it says."),
            ("The stronger version spreads the keys out,",
             "so no one key can move anything alone."),
            # the quorum's own sentence: one chunk per key, then the opening.
            ("One key stays with you, at home.",
             "One sits on a second device, in another safe.",
             "And one is held by a lawyer.",
             "Any two can move the coins, so your executor and the lawyer still can."),
            # the post: the lead-in, then the quoted line.
            ("In 2013, Hal Finney, the first person Satoshi ever sent a bitcoin to, wrote this about his own.",
             "My bitcoins are stored in our safe deposit box, and my son and daughter are tech savvy."),
            ("He was already paralysed by a fatal illness.",
             "One box, and two people who knew what to do with it."),
        ],
        shots=[
            Shot(clip=HANDS, clip_at=0.0),
            Shot(image=KEYPAD, zoom=1.08, pan=(0.02, 0.0)),
            Shot(clip=ENVELOPE, clip_at=1.0),
            Shot(clip=ETCH, clip_at=10.0),
            Shot(graphic="quorum", backdrop=BEATGROUND,
                 payload=([("YOU", "at home"),
                           ("SECOND DEVICE", "in another safe"),
                           ("A LAWYER", "in escrow")],
                          2, "COINS MOVE", "TWO OF THREE", 0)),
            Shot(graphic="post", backdrop=BEATGROUND,
                 payload=("post", FINNEY, "")),
            Shot(clip=VAULT, clip_at=3.0),
        ],
        gaps=[0.70, 0.60, 0.85, 0.60, 2.00, 1.10, 0.90],
    ),

    # --- close: the echo ------------------------------------------------------
    Section(
        title="So what happens to your crypto?",
        spoken_title="So, what happens to your crypto when you die?",
        kicker="THE ANSWER",
        sentences=[
            ("Whatever your keys allow.",),
            ("A court can decide who should get it.",
             "Only the keys decide whether anyone can."),
            ("Nothing in this video is financial or legal advice.",),
            ("So, if you died tomorrow,",
             "could anyone you trust actually find your keys?"),
        ],
        shots=[
            Shot(clip=DRIVE, clip_at=14.0),
            Shot(clip=JUDGE, clip_at=5.0),
            Shot(clip=RAIN, clip_at=1.0,
                 payload=("", "This is not financial or legal advice.")),
            Shot(clip=LETTER, clip_at=1.5),
        ],
        gaps=[0.85, 0.90, 1.10, 2.30],
    ),
]

META = Meta(
    title="What Happens to Your Crypto When You Die?",
    hook="No court can unlock a crypto wallet you hold yourself - not even for "
         "your family. Here is who actually controls your coins, what happens "
         "on an exchange, why a will is the worst place for a seed phrase, "
         "and the setups that let your family inherit without anyone taking "
         "the coins early.",
    url=URL,
    summary="What happens to crypto when you die: why a bank can reset access "
            "and a blockchain cannot, because it only checks a signature from "
            "the right private key; the estimated 3 to 3.7 million bitcoin "
            "thought lost for good out of 21 million; how a custodial "
            "exchange's estate process works (an estate case, a death "
            "certificate and court papers, a frozen account, then a transfer "
            "or sale) and why probate often takes 3 to 12 months; why "
            "self-custodied coins pass on only if someone can find the wallet "
            "and its seed phrase; why a will is the worst place for a seed "
            "phrase, since in many countries it becomes a public record in "
            "probate; and two setups that work - a hardware wallet with a "
            "split seed phrase and a sealed letter that says where, and a "
            "two-of-three multisignature wallet - with Hal Finney's own 2013 "
            "plan. Nothing here is financial or legal advice.",
    tags=["what happens to crypto when you die", "crypto inheritance",
          "bitcoin inheritance", "what happens to bitcoin when you die",
          "crypto estate planning", "seed phrase in will",
          "how to pass on crypto", "multisig inheritance",
          "crypto after death", "hal finney", "self custody inheritance",
          "crypto for beginners"],
    cta=f"The full guide to crypto inheritance: {URL}",
    credits=["Quote: Hal Finney, \"Bitcoin and me (Hal Finney)\", "
             "bitcointalk.org, 19 March 2013.",
             "Nothing in this video is financial or legal advice."],
)

HEADLINE = "Who gets\nyour\n[Bitcoin?]"


def thumbs(out: Path) -> Path:
    """The man at the grave set against the right edge, the cross going dark
    into the black at the left, and the Short's question in three rows over
    it. The plate stays clear of his face (~0.72 of the frame's width)."""
    import numpy as np
    from PIL import Image
    from video_automation.longform import thumb as T
    src = Image.open(GRAVE).convert("RGB")
    crop = src.crop((int(src.width * 0.22), 0, src.width, src.height))
    pw = int(720 * crop.width / crop.height)
    crop = crop.resize((pw, 720), Image.LANCZOS)
    im = Image.new("RGB", (1280, 720), (0, 0, 0))
    x = 1280 - pw
    im.paste(crop, (x, 0))
    a = np.zeros((1, 1280), np.float32)
    a[0, :x] = 1.0
    a[0, x:x + 260] = np.linspace(1.0, 0.0, 260)
    mask = Image.fromarray((np.repeat(a, 720, 0) * 255).astype("uint8"))
    im = Image.composite(Image.new("RGB", im.size, (0, 0, 0)), im, mask)
    fill, ink = T.ACCENTS["yellow"]
    T._headline(im, HEADLINE, 130, 560, 50, fill, ink, max_lines=3,
                leading=1.02, band="middle", margin=40, shadow=11, drop=(5, 6))
    im.save(out, quality=92)
    return out


def main() -> None:
    out = Path.home() / "Desktop/crypto-when-you-die-long.mp4"
    work = Path.home() / "Desktop/.crypto-when-you-die-long-work"
    made = render_long(
        SECTIONS, out, work, brand=CRYPTO, meta=META, voice=VOICE,
        music=MUSIC,
        callouts=None,
        # The title is the search. Last three long forms opened
        # hook / Counter / Stamp. Question only - no answer on screen.
        opener=Search("what happens to crypto when you die"),
        emphasis=["Nobody", "public record"],
        thumb_headline=HEADLINE,
        thumb_image=GRAVE,
        thumb_accent="yellow",
        endcard=ENDCARD, endcard_lead=7.0,
        title_at=10.5, title_hold=5.4,
    )
    # `render_long`'s own thumbnail is replaced by the hand-built one.
    made["thumb"] = thumbs(Path(made["thumb"]))
    for k, v in made.items():
        print(f"{k}: {v}")


if __name__ == "__main__":
    if "--thumb" in sys.argv:
        print(thumbs(Path.home() / "Desktop/crypto-when-you-die-long-thumb.jpg"))
    else:
        main()
