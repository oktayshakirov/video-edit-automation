"""Was Ledger hacked? The Optimizely hack - long-form 16:9 for YouTube.

Source: crypto-wiki/content/posts/send-and-receive-crypto-safely.mdx - its
"collect the address from the source", "verify on the device" and "send a
small test first" steps, which are the checks this video sorts into the
ones that would have caught the swap and the one that would not.

**The news, as sourced (checked 2026-11-20).** On 16 November 2026 an
attacker used a flaw in Optimizely Web Experimentation's account signup to
insert JavaScript into customers' projects (Optimizely's own status page,
captured). The script ran on 178 organisations' sites, Ledger among them
(Decrypt, StepSecurity, Newsweek), for about 16-19 hours, and rewrote
wallet addresses "in page text, form inputs ... copy events, the clipboard
API ... and the URL and body of fetch and XHR requests", only where the
address passed its chain's checksum and sat near a word like "wallet",
"deposit" or "send" (StepSecurity). One fixed replacement address per
chain (StepSecurity's IOC table, captured). About $7,000 reached them
(Report URI via Decrypt $7,150; StepSecurity $7,040), said as "about".
How the attacker got in is disputed past "a flaw in the signup", so the
video says no more than that.

**The angle.** The CryptoDad "Ledger Website Hacked! Is Your Crypto Safe?"
51k in two days (`demand/teardowns/optimizely-hack-ledger.md`): the
reassurance, plus a claim this video corrects - that matching the device
screen to the computer screen "would thwart" the swap. The page itself was
rewritten, so the page, the paste and the device all showed the attacker's
address. A commenter there asked exactly this. Plain "Optimizely hack
explained" titles sit at 4-252 views; the viewer's stake is Ledger.

**Picture first** (`workflow.md`). Per sentence:

* Search opener types "was ledger hacked" over Decrypt's real headline in a
  browser window; the camera rings "wallet addresses with the attacker's".
* `spotlight` - a real hardware wallet's own "Confirm sending" screen:
  IT WOULD HAVE AGREED.
* `grid` - the plan, three cards.
* code on a screen, in a player window - code from other companies.
* `diagram` - Optimizely, two versions, every visit.
* Optimizely's status page, in a tab, "an unauthorized third party
  exploited" ringed.
* `grid` - 178 organisations, five named (no logos - names only).
* a hand over a trackpad, not clicking, in a player window.
* StepSecurity's OPTIMJACK headline, in a tab.
* `grid` - three places it swapped.
* `spotlight` - StepSecurity's table of the attacker's addresses.
* the turn: the Trezor's screen torn (`aberration`).
* `relay` (new) - the page, the wallet app, the hardware wallet: SWAPPED,
  MATCHES, MATCHES, EVERY SCREEN MATCHES.
* a Ledger in a hand, isolated.
* `compare` - what reading the device catches, and what it cannot.
* keyboard copy, in a player window.
* `steps` - a second source.
* `stat` - about $7,000.
* Optimizely's status page again, "within three hours" ringed.
* a screen in someone's glasses, in a player window - check where it went.
* `checklist` close, the disclaimer on a Ledger, the Ledger on its laptop.

`relay` is new: no beat drew every screen agreeing on the wrong thing.
Rotation: no `pile`, `behind`, `honeypot`, `pool`, `reserve`, `post` (the
last two crypto long forms). Opener `Search` (last three: Search, Search,
Counter - not three running).

    PYTHONPATH=. .venv/bin/python projects/crypto-long/optimizely-hack.py
"""

import sys
from pathlib import Path
from pathlib import Path as _P

from video_automation.core import music, stillclip
from video_automation.core.brand import CRYPTO
from video_automation.core.stock import CACHE as STOCK
from video_automation.crypto.shots import Shot

from video_automation.longform import Meta, Section, render_long
from video_automation.longform.openers import Search

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
BRAND = ROOT / "assets/brand"
HW = ROOT / "assets/crypto/hardware-wallet"

# Screened 2026-11-20 at 1/4/8s (contact sheet), already in other scripts.
CODE = V / "code-scrolling-screen-terminal-dark/34268861.mp4"            # 18s, code scrolling on a dark screen
TRACKPAD = V / "hand-on-laptop-trackpad-night-dark-close/39425747.mp4"   # 19s, a hand hovering over a trackpad
KEYBOARD = V / "copy-paste-laptop-keyboard-shortcut-dark/36036748.mp4"   # 11s, a lit keyboard, fingers by the shortcut keys from 3s
GLASSES = V / "computer-screen-reflected-in-glasses/8311536.mp4"         # 14s, a screen reflected in someone's glasses

# The real devices (Commons, credits in assets/crypto/hardware-wallet/CREDITS.md).
TREZOR = HW / "trezor-confirm.jpg"          # a Trezor's own screen: "Confirm sending ... to addr..."
COLDCARD_HAND = HW / "coldcard-hand.jpg"    # a Coldcard in a hand, "OK TO SEND?" on its screen
LEDGER_LAPTOP = HW / "ledger-laptop.jpg"    # a Ledger on its cable beside a laptop
COLDCARD_DARK = HW / "coldcard-dark.jpg"    # the disclaimer's ground

# The real pages, captured 2026-11-20 (`screencap`, records in captures/).
CAP = STOCK / "captures"
DECRYPT = CAP / "decrypt-optimizely/decrypt-optimizely-l.mp4"     # headline, then "wallet addresses with the attacker's" ringed
DECRYPT_ADDR = "decrypt.co/383414/optimizely-hack-hijacked-ledger"
STATUS_FLAW = CAP / "optimizely-status/optimizely-status-flaw.mp4"    # "an unauthorized third party exploited" ringed
STATUS_FIXED = CAP / "optimizely-status/optimizely-status-fixed.mp4"  # "within three hours of detection" ringed
STATUS_ADDR = "status.optimizely.com/incidents/ftw0fh9wx43z"
STEPSEC = CAP / "stepsecurity-optimjack/stepsecurity-optimjack-l.mp4"  # the OPTIMJACK headline
STEPSEC_ADDR = "stepsecurity.io/blog/optimjack"
IOC = CAP / "stepsecurity-optimjack/ioc.jpg"   # the Wallets row of its IOC table, cut from the capture

# The made-up address the page should have shown, and the attacker's real
# Bitcoin replacement (StepSecurity's IOC table).
MEANT = "1Kp7vQ2mXz9LrT4wBn6cHd8yFs3aJe5gUq"
ATTACKER = "19g9rZcPeiz8rUvyWpTRyXXhPnjsWrc3kW"

BEATGROUND = BRAND / "beat-ground-crypto.jpg"
ENDCARD = V / "subscribe/4928934.mp4"

VOICE = "mia"
MUSIC = music.track("night-drift")
URL = "https://thecrypto.wiki/posts/send-and-receive-crypto-safely"

DISCLAIMER_BG = stillclip.path(COLDCARD_DARK, focus=(0.5, 0.45))


def sections() -> list:
    return [
    # --- hook. No card. Search types the query over Decrypt's headline. -----
    Section(
        title="Was Ledger hacked?",
        card=False,
        sentences=[
            ("Was Ledger hacked? On November sixteenth, its website was hijacked, along with a hundred and seventy-seven others.",),
            ("For most of a day, one script on all of them swapped crypto wallet addresses for the attacker's own.",),
            # the spotlight's own sentence: the device, then its screen.
            ("The devices were never touched.",
             "But the usual advice, check your hardware wallet's screen, would not have caught it."),
            # the grid's own sentence: one chunk per card.
            ("Here is where the address was swapped,",
             "why every screen agreed with it,",
             "and the one check that does work."),
        ],
        shots=[
            Shot(clip=DECRYPT, clip_at=0.0, window=("browser", DECRYPT_ADDR)),
            None,
            Shot(graphic="spotlight",
                 payload=(TREZOR, [(None, ""),
                                   ((0.27, 0.36, 0.73, 0.68), "IT WOULD HAVE AGREED")],
                          "THE USUAL ADVICE")),
            Shot(graphic="grid", backdrop=BEATGROUND, ground="grid",
                 payload=([("Where", "the address was swapped", "\U0001F500"),
                           ("Why", "every screen agreed", "✅"),
                           ("The check", "that does work", "\U0001F50D")],
                          "IN THIS VIDEO")),
        ],
        gaps=[0.80, 0.85, 0.90, 1.00],
    ),

    # --- how it got there ---------------------------------------------------
    Section(
        title="How did one script reach 178 websites?",
        spoken_title="So how did one script reach a hundred and seventy-eight websites?",
        kicker="ONE SCRIPT",
        sentences=[
            ("Big websites run code from other companies on every visit.",),
            # the diagram's own sentence: one chunk per node.
            ("One of them, Optimizely,",
             "lets a site test two versions of a page,",
             "so its script loads on every page it serves."),
            ("On November sixteenth, someone used a flaw in Optimizely's signup to slip their own code into customers' projects.",),
            # the grid's own sentence: one chunk per card.
            ("It reached a hundred and seventy-eight organisations: the BBC,",
             "CNN,",
             "Zoom,",
             "HSBC,",
             "and Ledger."),
            ("Nobody had to click anything. Opening the page was enough.",),
        ],
        shots=[
            Shot(clip=CODE, clip_at=1.0, window=("player", "Code from other companies")),
            Shot(graphic="diagram", backdrop=BEATGROUND, ground="grid",
                 payload=([("Optimizely", "a testing tool"),
                           ("Two versions", "of one page"),
                           ("Every visit", "its script loads")],
                          "ONE TOOL, MANY SITES", False)),
            Shot(clip=STATUS_FLAW, clip_at=0.0, window=("browser", STATUS_ADDR)),
            Shot(graphic="grid", backdrop=BEATGROUND, ground="grid",
                 payload=([("BBC", ""), ("CNN", ""), ("Zoom", ""),
                           ("HSBC", ""), ("Ledger", "")],
                          "178 ORGANISATIONS")),
            Shot(clip=TRACKPAD, clip_at=2.0, window=("player", "No click needed")),
        ],
        gaps=[0.70, 1.10, 0.90, 1.20, 0.90],
    ),

    # --- what it did: the turn ---------------------------------------------
    Section(
        title="What did the script do to crypto addresses?",
        spoken_title="So what did the script do to crypto addresses?",
        kicker="THE SWAP",
        card_gap=1.20,
        sentences=[
            ("It looked for wallet addresses next to words like deposit or send, and swapped them for the attacker's own.",),
            # the grid's own sentence: one chunk per card.
            ("It swapped them in the text on the page,",
             "in whatever you copied,",
             "and in whatever the page sent."),
            # the spotlight's own sentence: the table, then the address.
            ("Each was a real, valid address for its chain,",
             "so a format check passes."),
            ("Actually, this is where the usual advice breaks.",),
            # the relay's own sentence: one chunk per screen, then the verdict.
            ("You copy the address from the page,",
             "paste it into your wallet app,",
             "and your hardware wallet shows it on its own screen.",
             "Every screen matches: the attacker's address."),
            ("The device did its job. It showed exactly where the coins would go. It can't know where you meant them to go.",),
            # the compare's own sentence: a heading chunk per column, one per item.
            ("Reading the device screen catches",
             "malware that changes the address after you paste it.",
             "It can't catch",
             "an address that was wrong before you copied it."),
        ],
        shots=[
            Shot(clip=STEPSEC, clip_at=0.0, window=("browser", STEPSEC_ADDR)),
            Shot(graphic="grid", backdrop=BEATGROUND, ground="grid",
                 payload=([("The page", "its text", "\U0001F4C4"),
                           ("Your copy", "the clipboard", "\U0001F4CB"),
                           ("What it sent", "the page's requests", "\U0001F4E4")],
                          "THREE PLACES")),
            Shot(graphic="spotlight",
                 payload=(IOC, [(None, ""),
                                ((0.26, 0.25, 0.56, 0.40), "THE ATTACKER'S BITCOIN ADDRESS")],
                          "ONE PER CHAIN", False)),
            Shot(image=TREZOR, zoom=1.08, shader="aberration"),
            Shot(graphic="relay", backdrop=BEATGROUND, ground="grid",
                 payload=(MEANT, ATTACKER,
                          ["The page", "Your wallet app", "Your hardware wallet"],
                          "ONE ADDRESS, THREE SCREENS",
                          ("EVERY SCREEN MATCHES", "THE ATTACKER'S ADDRESS"))),
            Shot(image=COLDCARD_HAND, isolate=1.0),
            Shot(graphic="compare", backdrop=BEATGROUND, ground="grid",
                 payload=("IT CATCHES",
                          ["A change after you paste"],
                          "IT CAN'T CATCH",
                          ["Wrong before you copied"],
                          True)),
        ],
        gaps=[0.80, 1.00, 0.90, 1.00, 1.60, 0.90, 1.30],
    ),

    # --- the check that works ----------------------------------------------
    Section(
        title="So what check would have caught it?",
        spoken_title="So what check would have caught it?",
        kicker="THE CHECK",
        sentences=[
            ("A check only works against a source the page never touched.",),
            # the steps' own sentence: one chunk per node.
            ("Get the address from the receiver's own app, not a web page,",
             "compare it with your device, character by character,",
             "and send a small test they confirm before the rest."),
            ("Any one of those would have shown two different addresses.",),
            ("The take was small: about seven thousand dollars reached the attacker's wallets.",),
            ("Optimizely says it closed the flaw within three hours of spotting it, and removed the code.",),
            ("If you sent crypto on November sixteenth to an address you copied from a website, check where it went.",),
        ],
        shots=[
            Shot(clip=KEYBOARD, clip_at=3.5, window=("player", "Copied from the page")),
            Shot(graphic="steps", backdrop=BEATGROUND, ground="grid",
                 payload=(["From the receiver's own app",
                           "Compared on your device",
                           "A small test, confirmed"],
                          "A SECOND SOURCE")),
            None,
            Shot(graphic="stat", backdrop=BEATGROUND, ground="grid",
                 payload=("$7,000", "about that much reached the attacker",
                          "Report URI, 17 November 2026")),
            Shot(clip=STATUS_FIXED, clip_at=0.0, window=("browser", STATUS_ADDR)),
            Shot(clip=GLASSES, clip_at=2.0, window=("player", "Where did it go?")),
        ],
        gaps=[0.80, 1.20, 0.90, 1.00, 0.90, 1.10],
    ),

    # --- close: the echo ----------------------------------------------------
    Section(
        title="So what did your device agree with?",
        spoken_title="So, what did your device agree with?",
        kicker="THE ANSWER",
        sentences=[
            # the checklist's own sentence: one chunk per item.
            ("Your hardware wallet shows where the coins will go.",
             "It can't tell you where that address came from."),
            ("Nothing in this video is financial advice.",),
            ("So, every screen agreed with the attacker. What did you check yours against?",),
        ],
        shots=[
            Shot(graphic="checklist", backdrop=BEATGROUND,
                 payload=([("Where the coins will go", True),
                           ("Where the address came from", False)],
                          "WHAT IT CHECKS", True)),
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
    title="Was Ledger Hacked? What the Optimizely Hack Did to Crypto Addresses",
    hook="Was Ledger hacked? On 16 November 2026 its website was one of 178 "
         "running a hijacked Optimizely script that swapped crypto wallet "
         "addresses for the attacker's. Here is where the address was "
         "swapped, why your hardware wallet's screen would have agreed with "
         "it, and the one check that does work.",
    url=URL,
    summary="Was Ledger hacked? What the Optimizely hack (OPTIMJACK) did: on "
            "16 November 2026 an attacker used a flaw in Optimizely Web "
            "Experimentation's signup to insert JavaScript into customers' "
            "projects, and for most of a day 178 organisations' sites, "
            "Ledger's among them, served a script that rewrote crypto wallet "
            "addresses - in the page text, in what visitors copied and in "
            "what the page sent - with one valid attacker address per chain. "
            "Why the usual advice (match your hardware wallet's screen) "
            "would not have caught it: the page itself was rewritten, so the "
            "page, the paste and the device all showed the same wrong "
            "address. What does catch it: an address from a source the page "
            "never touched, compared on your device, and a small test the "
            "receiver confirms. About $7,000 reached the attacker. Ledger's "
            "devices were not part of it. Nothing here is financial advice.",
    tags=["was ledger hacked", "ledger hacked", "ledger website hacked",
          "optimizely hack", "optimjack", "optimizely hack explained",
          "crypto clipper", "address swap", "clipboard hijacker",
          "hardware wallet", "verify crypto address", "ledger",
          "crypto security", "how to send crypto safely"],
    cta=f"The full checklist for sending and receiving crypto - networks, "
        f"memos, test sends and checking an address at its source: {URL}",
    credits=["Nothing in this video is financial advice. No product in it is "
             "a recommendation.",
             "Pages: Decrypt, \"Optimizely Hack Hijacked Ledger, BBC and 176 "
             "Other Sites to Swap Crypto Wallet Addresses\" (17 Nov 2026); "
             "Optimizely status page, \"Web Experimentation Security "
             "Incident\" (18 Nov 2026); StepSecurity, \"OPTIMJACK: "
             "Optimizely-Hosted Scripts Loaded a Crypto Clipper and Card "
             "Skimmer on 178 Organizations\" (rev. 20 Nov 2026) - all "
             "captured 20 Nov 2026. Figure: Report URI, via Decrypt.",
             "The address the page should have shown is made up; the "
             "attacker's Bitcoin address is from StepSecurity's published "
             "indicators.",
             "Photos (Wikimedia Commons): Trezor Model T by FlippyFlink, CC0; "
             "Coldcard by Gareth Halfacree, CC BY-SA 2.0; Coldcard by Tony "
             "Webster, CC BY 2.0; Ledger Nano S by Motokoka, CC BY-SA 4.0 "
             "(adapted)."],
)

# The relay's own two cards, drawn: the editor picked it over the real
# Ledger with a ring and an arrow (2026-11-21), which went to the
# `hardware-wallet` long form instead. The cover adds the stake to the
# title, never repeats it (2026-11-17).
COVERS = ("beat",)
COVER_HEADLINES = {"beat": ["Every Screen", "[Agreed]"]}
HEADLINE = "\n".join(COVER_HEADLINES[COVERS[0]])


def _relay_frame(W: int, H: int, portrait: bool):
    """The relay beat's last state, two places, no kicker or verdict."""
    from video_automation.core.frame import LANDSCAPE, VERTICAL
    from video_automation.longform.beats import Relay
    b = Relay(MEANT, ATTACKER, ["The page", "Your hardware wallet"], "",
              ("", ""), brand=CRYPTO, frame=VERTICAL if portrait else LANDSCAPE,
              backdrop=BEATGROUND, reveals=[0.0, 2.0, 4.0], start=0.0,
              hold=8.0, ground="grid")
    im = b.draw(1.0).convert("RGB")
    return im.resize((W, H)) if im.size != (W, H) else im


def cover(kind: str, portrait: bool = False):
    """One cover, 1280x720 or (`portrait`) 1080x1920, as an RGB image.

    `beat`: the relay's two cards - THE PAGE, SWAPPED; YOUR HARDWARE
    WALLET, MATCHES - with EVERY SCREEN [AGREED] stacked under them."""
    import numpy as np
    from PIL import Image
    from video_automation.longform import thumb as T
    W, H = (1080, 1920) if portrait else (1280, 720)
    head = COVER_HEADLINES[kind]
    if kind == "beat":
        im = _relay_frame(W, H, portrait)
        if portrait:
            # The cards sit in the top two thirds; the type goes under them.
            box = (60, 1330, W - 120, 420)
        else:
            # Cut to the cards and lift them: the frame's lower half is the
            # headline's.
            big = _relay_frame(1920, 1080, False)
            crop = big.crop((0, 230, 1920, 230 + 1080 * 0.62))
            im = Image.new("RGB", (W, H), (8, 8, 8))
            cw = W
            ch = int(crop.height * W / crop.width)
            crop = crop.resize((cw, ch), Image.LANCZOS)
            # fade the cut's lower edge into the black, so there is no seam
            fade = np.ones((ch, 1), np.float32)
            fade[-90:, 0] = np.linspace(1.0, 0.0, 90)
            m = Image.fromarray((np.repeat(fade, cw, 1) * 255).astype("uint8"))
            im.paste(crop, (0, 10), m)
            box = (60, ch + 10, W - 120, H - ch - 30)
        T.stack_headline(im, head, box)
        return im
    raise ValueError(f"unknown cover {kind!r} - {COVERS}")


def thumbs(out: Path, portrait: bool = False, variants: bool = False) -> list[Path]:
    """The picked cover (the first of COVERS) at `out`, and nothing else;
    `variants=True` (`--thumb-variants`) writes the other directions as
    `-<style>` beside it, for choosing."""
    cover(COVERS[0], portrait).save(out, quality=92)
    made = [out]
    if variants:
        for k in COVERS[1:]:
            q = out.with_name(f"{out.stem}-{k}{out.suffix}")
            cover(k, portrait).save(q, quality=92)
            made.append(q)
    return made


def cards() -> None:
    """Cut the Wallets row out of StepSecurity's capture for the spotlight.
    Drawn here, never on import (`workflow.md`, step 3)."""
    from PIL import Image
    Image.MAX_IMAGE_PIXELS = None
    src = CAP / "stepsecurity-optimjack/stepsecurity-optimjack.png"
    im = Image.open(src).convert("RGB")
    w, h = im.size
    # A 16:9 cut round the Wallets row: the labels, the addresses and
    # StepSecurity's note beside them.
    x0, x1 = int(0.175 * w), int(0.895 * w)
    y0 = int(0.810 * h)
    im.crop((x0, y0, x1, y0 + (x1 - x0) * 9 // 16)).save(IOC, quality=92)


def main() -> None:
    cards()
    stillclip.make(COLDCARD_DARK, focus=(0.5, 0.45))
    out = Path.home() / "Desktop/optimizely-hack-long.mp4"
    work = Path.home() / "Desktop/.optimizely-hack-long-work"
    made = render_long(
        SECTIONS, out, work, brand=CRYPTO, meta=META, voice=VOICE,
        music=MUSIC,
        callouts=None,
        # The title is the search. Last three long forms opened Search /
        # Search / Counter.
        opener=Search("was ledger hacked"),
        emphasis=["every screen", "never touched"],
        thumb_headline=HEADLINE,
        thumb_accent="yellow",
        endcard=ENDCARD, endcard_lead=7.0,
    )
    made["thumb"] = thumbs(Path(made["thumb"]))[0]
    for k, v in made.items():
        print(f"{k}: {v}")


if __name__ == "__main__":
    if "--cards" in sys.argv:
        cards()
        print(IOC)
    elif "--thumb-variants" in sys.argv or "--thumb" in sys.argv:
        v = "--thumb-variants" in sys.argv
        d = Path.home() / "Desktop"
        for q in thumbs(d / "optimizely-hack-long-thumb.jpg", variants=v):
            print(q)
        for q in thumbs(d / "optimizely-hack-short-thumb.jpg", portrait=True, variants=v):
            print(q)
    else:
        main()
