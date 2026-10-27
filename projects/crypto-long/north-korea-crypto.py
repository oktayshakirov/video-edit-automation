"""How does North Korea steal crypto? - long-form 16:9 for YouTube.

Source: crypto-wiki/content/posts/how-does-north-korea-steal-crypto.mdx.

**The angle.** The assumption is that a state hacking unit cracks code. The
article's answer is that it almost never does: it gets a person to click a
file or to sign a screen they trusted. The video tells one heist through
(Bybit, 21 February 2025) as the proof, because the teardown showed the
standouts on this subject tell one theft as a sequence and the failures
summarise totals (`demand/teardowns/how-does-north-korea-steal-crypto.md`).
Then the three ways in, the two 2026 heists that show where it is heading
(Drift, Bitget - the E8 lane: few videos answer them yet), the laundering
race, and what it means for an ordinary holder. The close echoes the open:
not breaking code, breaking trust.

**A named scheme, so the profile arc** (`projects/crypto.md`): a fact
planted early pays off late - "signing a screen they trusted" in the hook
is the Bybit mechanism, and the habit the hook promises ("check what it
does, not just what it says") is that same screen turned on the viewer.

**No financial advice.** No exchange is rated. "Bybit covered its loss" is
a sourced fact about reserves, not an endorsement. Attribution is always an
agency's or a firm's finding; Drift is "likely, not confirmed" in the
article, so Drift is "suspected" on the timeline and in the voice. The
weapons figures are UN-panel estimates and are called estimates.

**Figures, all from the article.** More than $7B all-time ($6.75B to the end
of 2025 per Chainalysis, plus more than $1B in 2026 per Elliptic). Ronin
$625M (Mar 2022, began with a fake job offer). Bybit ~$1.46B in Ether, 21 Feb
2025, via a compromised Safe{Wallet} developer machine and an altered
interface; ~72% of the 2025 total. FBI PSA I-022625-PSA, 26 Feb 2025, title
"North Korea Responsible for $1.5 Billion Bybit Hack" (ic3.gov, checked).
Three signatures with the CEO last (NCC Group; Cyfrin's case study). The
signed transaction swapped the wallet's logic for the attackers' contract
(NCC, Ocorian). Drift ~$285M (1 Apr 2026), Bitget ~$387M (24 Sep 2026).
64 US companies (DOJ, Jan 2025). Bitget: 23 transfers, four chains, three
hours. UN panel, March 2024: ~50% of
foreign currency income, ~40% of WMD programs, both member-state estimates.

**Spoken around:** `Bitget` reads BIT-git, so the voice says "Bit get".

## The beats

Last three crypto long forms: crypto-when-you-die (bars / reel / checklist /
quorum / post), what-are-memecoins (compare / stat / steps / pool / grid),
gta-6-crypto (chart / checklist / diagram / quote / timeline).

* `blindsign` - **new, built for this video.** The confirm screen the
  signers saw, the three approvals filling, then a scanline that shows what
  was really signed. The library could not draw a display and its payload
  disagreeing, and it is the heist's whole mechanism.
* `timeline` - the four biggest heists at their real spacing: three years,
  then three in eighteen months.
* `post` - the FBI's own headline, the attribution in its own words.
* `grid` - the three ways in, each with its one-line mechanism.
* `reel` - the laundering, one card per step, the camera travelling: swap,
  hop chains, hide, cash out.

**Opener: `Search`.** The title is the phrase people type. The last three
long forms opened Search / Counter / Stamp; Search twice running is allowed,
three is not.

**Footage: the act, in the subject's world** - a hand on a mouse in red
light, a video-call interview, typing in the dark, a terminal, an Enter key,
a security operations room, remote workers at night, a contract being read,
Phnom Penh for the cash-out, Dubai under the Bybit lines.
Every clip fetched fresh and checked on a labelled contact sheet; verdicts in
`footage.md`. The site's own Bybit and Bitget cards are the real pictures,
as insets.

    PYTHONPATH=. .venv/bin/python projects/crypto-long/north-korea-crypto.py
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

SOURCE_POST = "how-does-north-korea-steal-crypto"
DEMAND = ("Johnny Harris 'How North Korea Pulled off a Billion $$$ Heist' 2.9M, "
          "18.0x (Short); Blackfiles 'The Hacker Who Took Down North Korea' 1.9M, "
          "44.1x; Lume 'The Hacker Who Stole $1.5 Billion In 2 Minutes' 557k, 3.0x")

V = STOCK / "videos"
ROOT = _P(__file__).resolve().parents[2]
BRAND = ROOT / "assets/brand"
SITE = ROOT.parent / "crypto-wiki/public/images"

# Fetched fresh for this pair, contact-sheeted at 15/50/85%. Luma sampled at
# 0.5/3/6/9s.
CLICK = V / "clicking-download-laptop-close-up/36392510.mp4"        # 8s,  L30, a hand on a mouse in red light - opens both cuts
INTERVIEW = V / "video-call-job-interview-laptop-night/8632779.mp4"  # 8s,  L130, a man on a video call with two interviewers - bright, but the noun
TYPING = V / "hands-typing-laptop-dark-room/6611947.mp4"            # 11s, L50, hands on a laptop, a blank lit screen
KEYS = V / "office-workers-computers-night/39425751.mp4"            # 21s, L35, fingers on a backlit keyboard
STYLUS = V / "signing-on-tablet-stylus/6895621.mp4"                 # 17s, L49, hands holding a tablet and a stylus
ENTER = V / "hand-pressing-enter-key/5119219.mp4"                   # 25s, L55-76, a finger pressing Enter
DUBAI = V / "dubai-skyline-night/34529274.mp4"                      # 22s, L80, downtown Dubai at night
OPS = V / "security-camera-monitoring-room/7255101.mp4"             # 10s, L58, analysts in front of a wall of screens
OPS2 = V / "security-camera-monitoring-room/38779103.mp4"           # 13s, L60, an operations floor at night
CONTRACT = V / "person-reading-contract-carefully/7841874.mp4"      # 8s,  L70, a hand with glasses over a contract
REMOTE = V / "remote-worker-home-office-night/8888780.mp4"          # 28s, L56, a man at a desk at home, from behind
ALONE = V / "man-working-laptop-alone-night/4069295.mp4"            # 30s, L40, a figure at a laptop under one lamp
DESKS = V / "man-working-laptop-alone-night/38990451.mp4"           # 20s, L42, monitors glowing in a dark room
NIGHTCALL = V / "laptop-video-call-night-dark-room/6517468.mp4"     # 15s, L33, a silhouette at a desk, blue light
TERMINAL = V / "command-line-terminal-screen-dark/35475345.mp4"     # 14s, L55, a terminal printing an install log
PHNOM = V / "phnom-penh-night/32934306.mp4"                         # 12s, L110, Phnom Penh at dusk from above - bright, but the place
ROCKET = V / "rocket-launch-night/854232.mp4"                       # 16s, L30, a rocket climbing at night
DARKTYPE = V / "laptop-video-call-night-dark-room/39191965.mp4"     # 37s, L16, hands typing on a laptop in near-dark
AERIAL = V / "dubai-skyline-night/35296036.mp4"                     # 22s, L40, Dubai from above at night, traffic moving
LATE = V / "man-working-laptop-alone-night/3585312.mp4"             # 26s, L35-40, a man alone at a laptop at night (smiles by ~20s - use the start)
WATER = V / "dark-water-ripples-night/10577610.mp4"                 # 30s, L34, gold light on dark water - the one abstract

BYBIT = SITE / "exchanges/bybit.png"      # 1193x691, the site's own Bybit card
BITGET = SITE / "exchanges/bitget.png"    # 900x506, the site's own Bitget card
WALLET = SITE / "posts/what-is-a-hardware-wallet.jpg"   # 800x534, unused until now

BEATGROUND = BRAND / "beat-ground-crypto.jpg"
FLAG = ROOT / "assets/crypto/north-korea/dprk-flag.png"   # drawn in code, see its CREDITS.md
ENDCARD = V / "subscribe/4928934.mp4"

VOICE = "noah"
MUSIC = music.track("night-drift")
URL = "https://thecrypto.wiki/posts/how-does-north-korea-steal-crypto"

FBI = {"source": "FBI public service announcement",
       "date": "26 February 2025",
       "headline": "[North Korea Responsible] for $1.5 Billion Bybit Hack"}

SHOWN = [("Action", "Routine transfer"), ("From", "Cold wallet"),
         ("To", "Bybit hot wallet")]
REAL = [("Action", "Replace wallet code"), ("From", "Cold wallet"),
        ("Control", "The attackers")]


SECTIONS = [
    # --- hook. No card. The Search types the title over sentence 1. --------
    Section(
        title="How does North Korea steal crypto?",
        card=False,
        sentences=[
            ("North Korea has stolen more than seven billion dollars in crypto.",),
            ("Almost none of it took breaking the code.",),
            ("It took one person clicking a file,",
             "or signing a screen they trusted."),
            ("So how does a country cut off from the world's banks pull that off?",),
            ("Stay to the end for the three ways they get in,",
             "and the one habit that matters for your own coins."),
        ],
        shots=[
            Shot(clip=CLICK, clip_at=0.5),
            Shot(clip=TERMINAL, clip_at=1.0),
            Shot(clip=STYLUS, clip_at=1.0),
            Shot(clip=DESKS, clip_at=2.0),
            Shot(clip=KEYS, clip_at=1.0),
        ],
        gaps=[0.80, 0.85, 0.85, 0.90, 0.90],
    ),

    # --- who ------------------------------------------------------------------
    Section(
        title="Who is behind the attacks?",
        spoken_title="So who is actually behind the attacks?",
        kicker="THE THIEVES",
        sentences=[
            ("Most of it traces back to one intelligence agency's hackers,",
             "best known as the Lazarus Group."),
            ("And crypto suits them.",
             "Sanctions shut North Korea out of the banks, and a blockchain never asks who you are."),
            ("The heists keep getting bigger.",),
            # the timeline's own sentence: one chunk per event.
            ("In 2022, six hundred and twenty-five million dollars from the Ronin bridge.",
             "In 2025, one point four six billion from Bybit.",
             "In April 2026, a suspected two hundred and eighty-five million from Drift.",
             ("And that September, three hundred and eighty-seven million from Bitget.",
              "And that September, three hundred and eighty-seven million from Bit get.")),
        ],
        shots=[
            Shot(clip=OPS2, clip_at=1.0),
            Shot(clip=NIGHTCALL, clip_at=1.0),
            Shot(clip=TYPING, clip_at=1.0),
            Shot(graphic="timeline", backdrop=BEATGROUND,
                 payload=([("Mar 2022", "Ronin bridge, $625M"),
                           ("Feb 2025", "Bybit, $1.46B"),
                           ("Apr 2026", "Drift, $285M, suspected"),
                           ("Sep 2026", "Bitget, $387M")],
                          "THE BIGGEST HEISTS")),
        ],
        gaps=[0.70, 0.80, 0.45, 1.20],
    ),

    # --- the heist ------------------------------------------------------------
    # The turning point, so the card gets the longer silence.
    Section(
        title="How did they rob Bybit?",
        spoken_title="So how did they rob Bybit?",
        kicker="THE HEIST",
        card_gap=1.30,
        sentences=[
            ("On the twenty-first of February 2025,",
             "Bybit moved Ether out of its cold wallet, as it did routinely."),
            ("Its own systems were never breached.",),
            ("The attackers had hacked one developer's computer at Safe Wallet,",
             "the signing service Bybit used."),
            ("From there, they rewrote what Bybit's signers would see.",),
            # the blindsign's own sentence: the card, the approvals, the truth.
            ("The screen asked for a routine transfer to Bybit's hot wallet.",
             "Three signers approved it, the chief executive last.",
             "But what they signed replaced the wallet's code, and handed it to the attackers."),
            ("Then about one point four six billion dollars in Ether left the wallet.",),
            # the post: the lead-in, then the headline.
            ("Five days later, the FBI said who it was.",
             "North Korea responsible for one point five billion dollar Bybit hack."),
            ("That one theft was about seventy-two percent",
             "of everything North Korea stole that year."),
        ],
        shots=[
            Shot(clip=DUBAI, clip_at=2.0, inset=(BYBIT, "tr", 0.16)),
            Shot(clip=OPS, clip_at=1.0),
            Shot(clip=ALONE, clip_at=3.0),
            Shot(clip=TERMINAL, clip_at=7.0),
            Shot(graphic="blindsign", backdrop=BEATGROUND,
                 payload=(SHOWN, REAL, ["SIGNER", "SIGNER", "CEO"],
                          "WHAT THE SIGNERS SAW")),
            Shot(clip=DESKS, clip_at=10.0,
                 note=("$1.46B", "in Ether, from one wallet")),
            Shot(graphic="post", backdrop=BEATGROUND,
                 payload=("headline", FBI, "")),
            Shot(clip=AERIAL, clip_at=2.0,
                 note=("72%", "of North Korea's 2025 total")),
        ],
        gaps=[0.55, 0.70, 0.55, 0.70, 2.00, 0.80, 1.10, 0.90],
    ),

    # --- the way in -----------------------------------------------------------
    Section(
        title="How do they get in?",
        spoken_title="So how do they get in?",
        kicker="THE WAY IN",
        sentences=[
            ("Almost every big theft starts one of three ways,",
             "and all three go through people."),
            # the grid's own sentence: one chunk per card.
            ("A fake recruiter, whose coding test installs malware.",
             "A trusted supplier, quietly poisoned, the way Safe Wallet was.",
             "Or a fake employee, hired remotely under a stolen identity."),
            ("The Ronin theft began with a fake job offer, sent to one engineer.",),
            ("Actually, this year's two biggest suspected heists skipped malware altogether.",),
            ("At Drift, a security council pre-signed transactions that looked routine.",),
            (("At Bitget, faked data made the theft look like normal withdrawals.",
              "At Bit get, faked data made the theft look like normal withdrawals."),),
            ("Different targets, same gap.",
             "People approving what they could not really see."),
        ],
        shots=[
            Shot(clip=REMOTE, clip_at=2.0),
            Shot(graphic="grid", backdrop=BEATGROUND,
                 payload=([("A fake recruiter", "a coding test that installs malware", "\U0001F4BC"),
                           ("A poisoned supplier", "software the target already trusts", "\U0001F4E6"),
                           ("A fake employee", "hired under a stolen identity", "\U0001FAAA")],
                          "THREE WAYS IN")),
            Shot(clip=INTERVIEW, clip_at=0.5),
            Shot(clip=OPS, clip_at=4.5),
            Shot(clip=STYLUS, clip_at=8.0),
            Shot(clip=NIGHTCALL, clip_at=8.5, inset=(BITGET, "tr", 0.16)),
            Shot(clip=ENTER, clip_at=2.0),
        ],
        gaps=[0.55, 1.10, 0.80, 0.55, 0.45, 0.70, 0.90],
    ),

    # --- the laundering -------------------------------------------------------
    Section(
        title="Where does the stolen crypto go?",
        spoken_title="So where does the stolen crypto actually go?",
        kicker="THE LAUNDERING",
        sentences=[
            ("Once a hack is public, everyone is watching.",
             "So the next part is a race."),
            # the reel: one sentence per card, held across with None.
            ("First, anything that can be frozen gets swapped away, like stablecoins.",),
            ("Then the coins hop chains. Bitget's made twenty-three transfers across four in three hours.",),
            ("Some is moved into Zcash, where transfers are hidden by design.",),
            ("Last, brokers in China and payment platforms in Cambodia turn it into spendable money.",),
            ("And that money goes somewhere.",
             "Estimates given to a UN panel tie cyber theft to about half its foreign currency,",
             "and forty percent of its weapons programs."),
        ],
        shots=[
            Shot(clip=OPS2, clip_at=6.0),
            Shot(graphic="reel",
                 payload=([(None, "Swap"),
                           (KEYS, "Hop chains"),
                           (None, "Hide"),
                           (PHNOM, "Cash out")],
                          "THE FIRST HOURS")),
            None,
            None,
            None,
            Shot(clip=ROCKET, clip_at=2.0),
        ],
        gaps=[0.70, 0.45, 0.45, 0.45, 0.85, 0.90],
    ),

    # --- you --------------------------------------------------------------------
    Section(
        title="What does this mean for you?",
        spoken_title="So what does all this mean for you?",
        kicker="YOUR COINS",
        sentences=[
            ("You are very unlikely to be the target of a state hacking unit.",
             "It goes where the money is concentrated."),
            ("Coins on a centralized exchange are only as safe as its signers.",),
            ("Coins on a hardware wallet cannot be drained by an exchange breach.",),
            ("And a recruiter's coding test is the same trick, aimed at you.",),
            ("So here is the habit that matters most.",),
            ("When a wallet asks you to sign,",
             "check what it does, not just what it says."),
        ],
        shots=[
            Shot(clip=ALONE, clip_at=20.0),
            Shot(clip=DUBAI, clip_at=12.0),
            Shot(clip=DARKTYPE, clip_at=3.0, inset=(WALLET, "right", 0.34)),
            Shot(clip=CLICK, clip_at=3.4),
            Shot(clip=REMOTE, clip_at=14.0),
            Shot(clip=CONTRACT, clip_at=0.2),
        ],
        gaps=[0.70, 0.80, 0.70, 0.70, 0.55, 0.90],
    ),

    # --- close: the echo ------------------------------------------------------
    Section(
        title="So how does North Korea steal crypto?",
        spoken_title="So, how does North Korea steal crypto?",
        kicker="THE ANSWER",
        sentences=[
            ("Rarely by breaking code.",
             "By breaking trust, one approval at a time."),
            ("Nothing in this video is financial advice.",),
            ("So, the next time a wallet asks for your signature,",
             "would you know what you are really signing?"),
        ],
        shots=[
            Shot(clip=ENTER, clip_at=12.0),
            Shot(clip=WATER, clip_at=2.0,
                 payload=("", "This is not financial advice.")),
            Shot(clip=LATE, clip_at=1.0),
        ],
        gaps=[0.90, 1.10, 2.30],
    ),
]

META = Meta(
    title="How Does North Korea Steal Crypto? The $1.5 Billion Bybit Heist, Explained",
    hook="North Korea has stolen more than $7 billion in crypto, and almost none "
         "of it took breaking the code. Here is how the Bybit heist actually "
         "worked, the three ways its hackers get in, what happened at Drift and "
         "Bitget in 2026, where the stolen coins go in the first hours, and the "
         "one habit that matters for your own coins.",
    url=URL,
    summary="How North Korea steals crypto: why its hackers rarely break "
            "cryptography and instead trick the people who control the money; "
            "the Lazarus Group and the state program behind it; the biggest "
            "heists - Ronin ($625M, 2022), Bybit (about $1.46B, February 2025), "
            "Drift (about $285M, April 2026) and Bitget (about $387M, September "
            "2026); how the Bybit theft worked, from a compromised Safe{Wallet} "
            "developer machine to an altered signing screen that three signers "
            "approved; the FBI's attribution five days later; the three ways in "
            "(fake recruiters, poisoned suppliers, fake IT workers); how stolen "
            "crypto is laundered - stablecoins swapped before they can be "
            "frozen, chain-hopping, Bitcoin and Zcash, then brokers and payment "
            "platforms that cash it out; the UN panel's estimates of what the "
            "money funds; and what it means for an ordinary holder. Nothing "
            "here is financial advice.",
    tags=["how does north korea steal crypto", "north korea crypto hack",
          "lazarus group", "bybit hack", "bybit hack explained",
          "drift protocol hack", "bitget hack", "crypto hack explained",
          "how crypto gets laundered", "north korean hackers",
          "crypto security", "blind signing"],
    cta=f"Every heist, every source and the full laundering trail: {URL}",
    credits=["Headline: FBI public service announcement I-022625-PSA, "
             "26 February 2025.",
             "Nothing in this video is financial advice."],
)

HEADLINE = "How does\nNorth Korea\nsteal\n[crypto?]"


def thumbs(out: Path) -> Path:
    """The `blindsign` card in its final state - "WHAT WAS SIGNED", the
    attackers in red, three ticks - on the right, over the North Korean flag,
    and the title's question in four rows on the flag's darkened left. No
    person: the video has none (`thumbnails.md`).

    **The flag is the feed check's fix.** The first cover put the card on the
    beat's dark water; beside the top three results at 320px (BBC, CoinGecko,
    Lume) every one of them said "North Korea" with the flag or a face before
    a word was read, and ours said nothing until it was read. Forced rows
    widen their column by 1.38, so the column passed is the card's edge over
    1.38."""
    import numpy as np
    from PIL import Image, ImageEnhance, ImageFilter
    from video_automation.core.frame import LANDSCAPE
    from video_automation.longform import thumb as T
    from video_automation.longform.beats import BlindSign
    b = BlindSign(SHOWN, REAL, ["SIGNER", "SIGNER", "CEO"], "", brand=CRYPTO,
                  frame=LANDSCAPE, backdrop=BEATGROUND,
                  reveals=[0.0, 3.0, 6.0], start=0.0, hold=9.0)
    card = b.draw(8.9 / 9).crop((b.x0 - 4, b.y0 - 4,
                                 b.x0 + b.cw + 4, b.y0 + b.ch + 4))
    cw = 560
    card = card.resize((cw, int(card.height * cw / card.width)), Image.LANCZOS)
    im = Image.open(FLAG).convert("RGB").resize((1280, 720), Image.LANCZOS)
    im = ImageEnhance.Brightness(im.filter(ImageFilter.GaussianBlur(2))).enhance(0.55)
    a = np.zeros((1, 1280), np.float32)
    a[0, :560] = 0.55
    a[0, 560:760] = np.linspace(0.55, 0.0, 200)
    shade = Image.fromarray((np.repeat(a, 720, 0) * 255).astype("uint8"))
    im = Image.composite(Image.new("RGB", im.size, (0, 0, 0)), im, shade)
    x, y = 1280 - cw - 26, (720 - card.height) // 2
    drop = Image.new("L", im.size, 0)
    drop.paste(255, (x + 10, y + 14, x + cw + 10, y + card.height + 14))
    drop = drop.filter(ImageFilter.GaussianBlur(18)).point(lambda v: int(v * 0.7))
    im = Image.composite(Image.new("RGB", im.size, (0, 0, 0)), im, drop)
    from PIL import ImageDraw
    shape = Image.new("L", card.size, 0)
    ImageDraw.Draw(shape).rounded_rectangle([1, 1, card.width - 2, card.height - 2],
                                            radius=14, fill=255)
    im.paste(card, (x, y), shape)
    fill, ink = T.ACCENTS["yellow"]
    T._headline(im, HEADLINE, 180, int((x - 70) / 1.38), 34, fill, ink,
                max_lines=4, leading=1.0, band="middle", margin=34,
                shadow=12, drop=(5, 6))
    im.save(out, quality=92)
    return out


def main() -> None:
    out = Path.home() / "Desktop/north-korea-crypto-long.mp4"
    work = Path.home() / "Desktop/.north-korea-crypto-long-work"
    made = render_long(
        SECTIONS, out, work, brand=CRYPTO, meta=META, voice=VOICE,
        music=MUSIC,
        callouts=None,
        # The title is the search. Last three long forms opened
        # Search / Counter / Stamp. Question only - no answer on screen.
        opener=Search("how does north korea steal crypto"),
        emphasis=["never breached", "what it does"],
        thumb_headline=HEADLINE,
        thumb_accent="yellow",
        endcard=ENDCARD, endcard_lead=7.0,
        title_at=10.0, title_hold=5.4,
    )
    # `render_long`'s own thumbnail is replaced by the hand-built one.
    made["thumb"] = thumbs(Path(made["thumb"]))
    for k, v in made.items():
        print(f"{k}: {v}")


if __name__ == "__main__":
    if "--thumb" in sys.argv:
        print(thumbs(Path.home() / "Desktop/north-korea-crypto-long-thumb.jpg"))
    else:
        main()
