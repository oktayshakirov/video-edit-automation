"""What is proof of stake? — long-form 16:9 for YouTube.

Source: crypto-wiki/content/posts/what-is-proof-of-stake.mdx.
**Sixth long-form explainer.** Picked over the two higher-demand pages
(`exchanges/cryptocom` 380, `crypto-etfs-explained` 362) because the user chose
it directly, and it is the natural companion to the already-shipped
`mining-rig.py` (proof of work): same underlying question — what keeps a
stranger honest — answered the other way.

**The article is a features list and the video is not.** "Validators, stake,
selection, attestation, rewards, slashing, pros, cons, history, examples" reads
as a slide deck read aloud. The script instead takes the frame the mining rig
video already established — proof of work is an energy business wearing a
hardware costume — and asks what the alternative actually trades that energy
cost *for*. Everything else (selection algorithm, slashing triggers, staking
pools) answers that one question rather than being its own bullet.

The arc:

* **Hook** — Ethereum turned off every miner it had in 2022, overnight, and
  nothing broke. So what was securing it instead?
* **Reframe** — proof of work spends electricity to prove you did not cheat;
  proof of stake spends money instead. Validators lock a stake as collateral.
* **Deep dive** — the five-step lottery: lock, get picked (stake weight plus
  randomness — not just the richest wallet), propose, attest, get paid.
* **Twist** — slashing: a bad validator does not just waste electricity, the
  protocol takes their money automatically. Four triggers, no court.
* **Twist 2** — it fixed the energy problem, not the scale problem. Wealth
  concentration, staking-pool centralization and the "nothing at stake"
  long-range attack are real, not hypothetical.
* **Mirror/echo** — neither mechanism is free, both are a bet on what makes
  lying expensive. Back to the night the miners were replaced, not saved.

**No financial advice.** The script never says which mechanism is "better",
never names a token to buy, never rates a network's investment merit. Slashing
risk is described as a mechanism, with the article's own disclaimer language
behind it.

**Phonemes, checked with espeak.** `ETH` alone reads correctly as the word
"eth" (`ˈɛθ`). But spelling the number out — "thirty-two ETH" — makes espeak
read the letters E-T-H instead (`ˌiːtˌiːˈeɪtʃ`), while the digit form "32 ETH"
still reads it as the word. So the script writes the digit, never the spelled
number, anywhere it precedes ETH. `proof of stake` and `proof of work` both
read plainly and are said in full throughout — never the initialisms, which
individually phonemize as two separate letters/words spoken oddly rather than
as anything a person would say out loud.

**Ethereum was mispronounced in the first cut and espeak says why.**
`Ethereum` phonemizes to `ˌiːθɚɹˈiːəm` — "ee-thuh-REE-um", stress on the wrong
syllable and a schwa where the vowel should be `ɪɹ`. `Etheerium` returns
`iːθˈɪɹiəm`, which is the brand's own "ee-THEER-ee-um". The respell goes in the
**spoken** half of the `(caption, spoken)` pair so the screen still reads
correctly, exactly as `Binance`/`Bynanse` already does.

**Every picture in this video is fresh, and that is now a rule.** The first
cut was built entirely from assets already shipped in other crypto videos and
the user rejected it on exactly that. An inventory across all six crypto
projects found the channel recycling a tiny pool: `security-combination-lock.jpg`
in **nine** videos, `digital-technology.jpg` in eight, `analysis.jpg`,
`laptop-trading.jpg` and `futuristic-crypto-exchange.jpg` in seven each, and the
`server-room-data-center`, `digital-code-stream-dark` and
`abstract-dark-waves-motion` clips in seven each. That is the templated sameness
`docs/long-form-strategy.md` says gets a channel suppressed, arriving through
the back door of "screen the cache first".

**The site's own library is exhausted for this channel, measured rather than
assumed.** Of 147 post images, only fifteen unused ones pass the dark box at
all, and every one of those is disqualified on other grounds already in this
skill: `kucoin-logo`, `binance-banner`, `whitebit-logo` and `ethereum-2` are
brand logos, `bitfinex-ui` and `gemini-exchange-trading` are platform
screenshots, `proof-of-stake.jpg` is the labelled infographic, and
`ftx-collapse` and `one-coin` are the two files this skill already records as
off-message. So a fresh video now means **fresh stock**, and the site-images-lead
principle in the strategy doc has quietly stopped being achievable here.

**What was fetched and what was rejected.** Twenty-two new queries, contact
sheeted before use — the numbers cannot see subject, and two of these proved it
again. `safe-deposit-box-vault-dark-interior/6406107` passed the box and is a
**van interior**, not a vault; `hands-locking-padlock-dark/10241357` passed at
L0-1 only because it is 99% empty black with a tiny drifting padlock, which is
the luma box being gamed by emptiness rather than by darkness. Also rejected:
`network-nodes/35002190` and `digital-padlock-cyber-security-gold/31360633` on
hue (teal and bright green, the two worst against gold — the second is the same
"matrix rain" this skill already records rejecting once),
`dominoes-falling-dark/38005269` for being the magenta version of a keeper,
`molecular-structure/35967934` because it is a **DNA double helix** and reads as
biology, `gold-bars-dark-background/3752109` because it is **bottle caps**, and
`power-plant-cooling-towers-night/4188242` because it is water at night and
would fight this brand's own blackwater backdrop.

The thirteen clips and six photographs that survived are declared below with
their measured ranges. Most are gold-dominant on near-black, which is the first
time this channel's footage has actually matched its own palette rather than
being blue server rooms dimmed toward it.

**A 10-second clip is a one-use clip in this format, and that is the rule the
first redistribution still got wrong.** `VideoShot` refuses to stretch past
1.33x, so a shot needs its clip to have `clip_at` plus the shot's own length
available — and shots here run to ~4s. Allowing 8s of headroom per use means a
10s source supports exactly one position worth using (two would be 0.5 and 2.0,
which look identical anyway). That is why the second fetch filtered for
**>=14s** before screening anything: the first eight clips could not fill 21
slots under the "no clip more than twice" rule no matter how they were
arranged. Rejected from that batch: both `electric-arc-plasma-energy-dark`
clips, which are magenta plasma balls.

**Beat silhouettes, checked before building.** Six distinct shapes, no
repeats: `stat` (99% less energy), `steps` (the five-step block lottery, now
with an emoji per node), `checklist` (four slashing triggers, flow=True — the
narration states each as fact, not a question), `grid` (the three unresolved
problems), `quote` (the wealth-head-start line), `compare` (proof of work vs
proof of stake, name_columns=True). Item counts vary: 1, 5, 4, 3, 1, 3+3.

**Icons on the `steps` track**, carried over from the tinnitus skill, where the
note was that a bare numbered track is "a list of words". The glyph replaces
the numeral inside each node, so the step reads before its label does. Chosen
against this palette: no bright green and nothing that renders near-black.

**Clip hygiene is checked by arithmetic now, not by eye.** Two separate builds
died on it — first `server-racks-blue-light-dark` (9.2s, called six times with
`clip_at` up to 12.0), then `dominoes-falling-dark` (10.0s at `clip_at=7.5` for
a 3.8s shot). Both times the renderer refused rather than freezing or looping,
which is correct but costs a full render to discover. Every clip below carries
its duration in the trailing comment, and the shot list is validated before
rendering: **<=2 uses per clip, >=8s of headroom on every use, repeats at least
five slots apart.**

Run from the repo root:

    PYTHONPATH=. .venv/bin/python projects/crypto-long/proof-of-stake.py
"""

from pathlib import Path

from video_automation.core import music
from video_automation.core.brand import CRYPTO
from video_automation.core.stock import CACHE as STOCK

ROOT_ASSETS = STOCK.parent            # assets/
from video_automation.crypto.shots import SITE_IMAGES, Shot
from video_automation.longform import Meta, Section, render_long

POSTS = SITE_IMAGES / "posts"

# **Every asset below is fresh: fetched for this video and used by no other.**
# Durations are in the trailing comment because a clip shorter than its slot
# raises, and the first build of this video hit exactly that.
NODES = STOCK / "videos/network-nodes-glowing-connections-dark/34994351.mp4"    # 10.0s L22-25 S26
SPHERE = STOCK / "videos/geometric-network-grid-gold-dark/34636451.mp4"         # 10.0s L24-30 S22-27
DOMINO = STOCK / "videos/dominoes-falling-dark/38003914.mp4"                    # 10.0s L11-17 S16-23
GOLDPART = STOCK / "videos/abstract-gold-particles-floating-dark/39038234.mp4"  # 10.0s L14-18 S11-12
TURBINE = STOCK / "videos/wind-turbine-silhouette-night/6279023.mp4"            # 24.8s L20-21 S4-5
CHESS = STOCK / "videos/chess-board-pieces-dark-moody/6599643.mp4"              # 20.9s L33-34 S15-16
PLANT = STOCK / "videos/power-plant-cooling-towers-night/6216703.mp4"           # 15.2s L11-12 S4-5
CHAIN = STOCK / "videos/abstract-blockchain-chain-links-dark/34127955.mp4"      # 20.0s L7-10 S1
# Second fetch, all >=14s: the first eight left the shot list short once the
# "no clip more than twice" and "at least 8s of headroom" rules were applied
# properly. A 10s clip is a *one-use* clip in this format, which is the part
# the first pass got wrong.
GOLDDUST = STOCK / "videos/gold-dust-particles-black-background/10296170.mp4"   # 20.4s L26-31 S29-37
GOLDRAYS = STOCK / "videos/gold-dust-particles-black-background/34645219.mp4"   # 20.0s L43-44 S44-45
HIGHWAY = STOCK / "videos/night-highway-traffic-long-exposure-dark/9299639.mp4" # 24.3s L9-13 S11-13
AERIAL = STOCK / "videos/night-highway-traffic-long-exposure-dark/4062948.mp4"  # 21.8s L19-23 S16-20
SMOKE = STOCK / "videos/smoke-swirling-dark-gold-light/4320605.mp4"             # 30.1s L4-19 S4-10

# **Third fetch: concrete subjects, after the second cut read as wallpaper.**
# The user's note was that the abstracts "feel more like a background than main
# footage" and lose attention across a long video, and they were right - the
# second pass over-corrected toward on-palette abstraction and ended up with
# gold dust, smoke, particles and geometry carrying whole sections. These are
# people and hardware.
MAN = STOCK / "videos/man-working-computer-dark-office-night/8311535.mp4"       # 23.0s L19-28 S10-13
CODER = STOCK / "videos/programmer-coding-screen-dark-night/13522186.mp4"       # 14.0s L35-37 S5-6
MONITORS = STOCK / "videos/programmer-coding-screen-dark-night/5240935.mp4"     # 23.0s L20-21 S25-29
FARM = STOCK / "videos/crypto-mining-farm-rows-of-machines/31710201.mp4"        # 20.0s L30-44 S0

# Stock photographs, also fresh. The site's own library could not supply these:
# everything in it dark enough for this palette is already in three to nine
# other videos, and the only unused files that pass the box are brand logos and
# platform screenshots, both of which this format bans.
PH = STOCK / "photos"
ETHCOINS = PH / "stack-of-coins-dark-moody/20534456.jpg"            # L27.6 S2.0
BTCCOINS = PH / "gold-coins-dark-background-macro/29968366.jpg"     # L40.6 S12.6
TRAILS = PH / "abstract-gold-light-trails-black/19253590.jpg"       # L20.2 S24.2
STRIPES = PH / "abstract-dark-gold-geometric/18415806.jpg"          # L17.5 S15.1
POLY = PH / "abstract-dark-gold-geometric/30869731.jpg"             # L30.6 S4.5
CITYGRID = PH / "night-city-power-grid-lights-aerial/33803466.jpg"  # L31.5 S30.5
GPUCARDS = PH / "graphics-card-gpu-dark-background/8622912.jpg"     # L27.4 S4.3  two RTX cards on black
GPUCOPPER = PH / "graphics-card-gpu-dark-background/34552790.jpg"   # L31.6 S23.9 copper-finned GPU
CHIPS = PH / "motherboard-chip-macro-dark/36169770.jpg"             # L36.0 S14.3
# Fiat, for the line that says "Money." - see the note in section two.
CASH = PH / "banknotes-low-key-photography/10149288.jpg"            # L67.1 S28.4

# **The site's own diagram, pre-composed onto a 1920x1080 slide.**
# This skill bans an infographic from a full-frame *Ken Burns* shot because the
# move crops its title off the top and its last row off the bottom. That ban is
# about the move, not the picture — but handing the raw 1000x667 file to a
# `Shot` with `zoom=1.0` was **not** enough, and the first attempt shipped with
# the title clipped: covering 1920 from a 1000px source needs 1.92x, the
# ceiling is 1.90, and the renderer got close enough to fill the width and then
# cropped ~90px off the top and bottom to make the height fit.
#
# Rather than fight the cover/fit boundary, the diagram is composited onto a
# frame-sized canvas *once*, by `tools/make_slide.py`. The asset then bleeds off
# all four edges by construction, so no crop is possible and no rule is bent —
# and it gets a 6% margin and the brand hairline for free.
DIAGRAM = ROOT_ASSETS / "brand/slides/proof-of-stake-slide.jpg"     # 1920x1080

ENDCARD = STOCK / "videos/subscribe/4928934.mp4"

VOICE = "mia"

MUSIC = music.track("night-drift")

URL = "https://thecrypto.wiki/posts/what-is-proof-of-stake"

A = 16 / 9


SECTIONS = [
    # --- the hook. No card. Open on motion, not a still. -------------------
    Section(
        title="The night mining stopped",
        card=False,
        sentences=[
            ("In twenty twenty-two,",
             "one of the biggest networks in crypto",
             "turned off every miner it had."),
            ("Overnight.",),
            # The reversal — it contradicts the expectation the line before it
            # sets up, so it takes the long gap.
            ("Nothing broke.",),
            ("So what was actually securing it instead?",),
            ("Stay to the end",
             "and you will know how a blockchain stays honest",
             "without burning a single watt to prove it -",
             "and the number that made the switch possible."),
            ("Ninety-nine percent.",),
            ("That is roughly how much less electricity",
             "the network now uses."),
            ("Not a smaller mining operation.",
             "No mining at all."),
        ],
        shots=[
            Shot(clip=PLANT, clip_at=0.5),
            Shot(clip=MAN, clip_at=1.0),
            None,                                    # ride the shot
            Shot(clip=FARM, clip_at=1.0),
            Shot(clip=TURBINE, clip_at=2.0,
                 payload=("", "How a blockchain stays honest without mining")),
            Shot(graphic="stat",
                 payload=("99%", "LESS ENERGY",
                          "Roughly what the switch away from mining saved"),
                 backdrop=STRIPES),
            None,                                    # hold the figure
            Shot(image=CITYGRID, zoom=1.10, pan=(0.02, 0.01),
                 aspect=A, bias=0.5),
        ],
        gaps=[0.60, 0.85, 0.90, 0.60, 0.60, 1.10, 0.55, 0.85],
    ),

    # --- reframe: what proof of stake spends instead of electricity --------
    Section(
        title="So what replaced the machines?",
        spoken_title="So what actually replaced the machines?",
        sentences=[
            ("Proof of work spends electricity",
             "to prove you did not cheat."),
            ("Proof of stake spends something else instead.",),
            ("Money.",),
            ("Validators lock up a stake of the network's own coin",
             "as collateral."),
            ("It works like a security deposit.",),
            ("Behave, and you earn rewards.",),
            ("Cheat,",
             "and the protocol can take the deposit itself."),
            ("No warehouse.",
             "No fans.",
             "No electricity bill to win."),
        ],
        shots=[
            # "Proof of work spends electricity" - the card that spends it,
            # not a field of gold dust. Concrete beats on-palette.
            Shot(image=GPUCOPPER, zoom=1.10, pan=(0.02, 0.01),
                 aspect=A, bias=0.5),
            Shot(image=BTCCOINS, zoom=1.10, pan=(0.02, 0.01),
                 aspect=A, bias=0.5),
            # **"Money." lands on fiat, not on Ethereum.** It read as a
            # contradiction: the voice says the generic word and the screen
            # showed the specific crypto the sentence is deliberately *not*
            # about yet. Banknotes are the picture of the word.
            Shot(image=CASH, zoom=1.11, pan=(-0.02, 0.01),
                 aspect=A, bias=0.5),
            None,                                    # hold the coins
            None,
            Shot(clip=MONITORS, clip_at=1.0),
            Shot(clip=PLANT, clip_at=7.0,
                 payload=("", "The protocol enforces it automatically")),
            Shot(clip=HIGHWAY, clip_at=1.0),
        ],
        gaps=[0.60, 0.85, 1.10, 0.55, 0.60, 0.55, 0.90, 0.85],
    ),

    # --- deep dive: the five-step block lottery -----------------------------
    Section(
        title="So how do you actually become a validator?",
        sentences=[
            # espeak stresses `Ethereum` on the wrong syllable; the respell
            # rides in the spoken half so the caption still reads correctly.
            (("On Ethereum,", "On Etheerium,"),
             "the entry price is 32 ETH."),
            ("Lock it up,",
             "and you are one of the validators."),
            # Lead-in for the beat, deliberately outside its own sentence.
            ("From there,",
             "it is the same five steps every time."),
            # The beat's own sentence — one chunk per step, which is what
            # times the reveals.
            ("Lock the stake as collateral.",
             "Get picked - stake weight, plus randomness.",
             "Propose the block.",
             "Other validators vote yes.",
             "Get paid, or get slashed."),
            ("The randomness matters.",),
            ("Otherwise the richest wallet",
             "would win every single time."),
            ("And once two-thirds of the validators agree,",
             "the block is done.",
             "No more waiting for another rig to catch up."),
        ],
        shots=[
            Shot(image=ETHCOINS, zoom=1.10, pan=(0.02, -0.01),
                 aspect=A, bias=0.5,
                 note=("32 ETH", "the deposit that buys a shot at the next block")),
            # The site's own architecture diagram, whole, as a slide.
            Shot(image=DIAGRAM, zoom=1.0, pan=(0.0, 0.0), aspect=16 / 9, bias=0.5),
            None,                                    # hold the diagram
            # **Icons on the track**, per the tinnitus skill: the numeral is
            # replaced by the glyph inside each node, so the step reads before
            # its label does. A padlock for the deposit, a die for the
            # randomness the narration is about to insist on, a block, a ballot
            # and the money that is either paid or taken.
            Shot(graphic="steps",
                 payload=([("Lock the stake", "\U0001F512"),
                           ("Get picked", "\U0001F3B2"),
                           ("Propose the block", "\U0001F4E6"),
                           ("Validators vote", "\U0001F5F3\uFE0F"),
                           ("Paid, or slashed", "\U0001F4B0")],
                          "HOW A BLOCK GETS MADE")),
            Shot(clip=CHESS, clip_at=1.0),
            None,                                    # hold the board
            Shot(clip=GOLDRAYS, clip_at=0.5,
                 payload=("", "No rig to catch up to")),
        ],
        gaps=[0.55, 0.60, 0.60, 0.90, 0.55, 0.85, 0.85],
    ),

    # --- the twist: slashing takes the money, no court involved -------------
    Section(
        title="So what actually stops them lying?",
        sentences=[
            ("The word for this is slashing.",),
            ("In proof of work,",
             "a bad miner just wastes electricity."),
            ("In proof of stake,",
             "a bad validator loses money -",
             "automatically."),
            ("Four things trigger it,",
             "and the protocol catches all of them itself."),
            ("Signing two conflicting blocks.",
             "Going offline for too long.",
             "Proposing an invalid block.",
             "Trying to rewrite old history."),
            ("Any one of those,",
             "and part of the stake is gone",
             "before you can argue about it."),
            ("No court.",
             "No refund.",
             "The code just runs."),
        ],
        shots=[
            Shot(clip=SMOKE, clip_at=1.0),
            Shot(clip=TURBINE, clip_at=14.0),
            Shot(image=TRAILS, zoom=1.11, pan=(0.02, 0.01),
                 aspect=A, bias=0.5),
            None,                                    # ride the trails
            Shot(graphic="checklist",
                 payload=([("Signing two conflicting blocks", True),
                           ("Going offline too long", True),
                           ("Proposing an invalid block", True),
                           ("Rewriting old history", True)],
                          "WHAT GETS YOU SLASHED", True),
                 picture=POLY),
            Shot(clip=MAN, clip_at=12.0),
            # "No court. No refund. The code just runs." - the code, literally.
            # This slot held an abstract geometric solid and was called ugly.
            Shot(clip=CODER, clip_at=1.0),
        ],
        gaps=[0.60, 0.55, 0.90, 0.60, 0.90, 0.85, 0.90],
    ),

    # --- the second twist: it traded one problem for another ---------------
    Section(
        title="So did it just trade one problem for another?",
        sentences=[
            ("Proof of stake fixed the energy problem.",),
            ("It did not fix scale.",),
            ("It swapped one kind of advantage for another.",),
            ("Three problems came with it.",),
            ("The rich can compound.",
             "Staking pools concentrate the vote.",
             "An old key could still try to rewrite the past."),
            ("None of them is hypothetical.",
             "All three are on the criticism list",
             "of every major network."),
            ("The richest wallets do not need a warehouse. "
             "They just need to already be rich.",),
            ("So call it a fair trade,",
             "or call it a new kind of gatekeeper.",
             "Either way, it is not neutral."),
        ],
        shots=[
            Shot(clip=AERIAL, clip_at=1.0),
            None,                                    # ride the turbines
            Shot(image=BTCCOINS, zoom=1.11, pan=(0.02, 0.01),
                 aspect=A, bias=0.5),
            Shot(clip=DOMINO, clip_at=0.5),
            Shot(graphic="grid",
                 payload=([("The rich can compound",
                            "More stake wins more stake, faster than savings ever could"),
                           ("Staking pools concentrate the vote",
                            "Most people delegate to a handful of large operators"),
                           ("An old key, a new fork",
                            "A validator who already exited could still try to rewrite history")],
                          "PROOF OF STAKE HAS ITS OWN PROBLEMS")),
            Shot(image=CHIPS, zoom=1.11, pan=(-0.02, 0.01),
                 aspect=A, bias=0.45),
            Shot(graphic="quote",
                 payload=("The richest wallets do not need a warehouse. "
                          "They just need to already be rich.",
                          "not a hardware advantage - a head start"),
                 picture=ETHCOINS),
            Shot(clip=GOLDPART, clip_at=1.0),
        ],
        gaps=[0.60, 0.85, 0.60, 0.60, 0.90, 0.70, 2.40, 0.85],
    ),

    # --- mirror, echo, the ask -----------------------------------------------
    Section(
        title="So which one actually wins?",
        sentences=[
            ("Neither one is free.",),
            ("Proof of work and proof of stake",
             "are just two different bets",
             "on what keeps a stranger honest."),
            ("Put them side by side.",),
            ("Proof of work.",
             "Expensive hardware.",
             "A real electricity bill.",
             "Anyone with a rig can try.",
             "Now proof of stake.",
             "A staked deposit instead.",
             "Almost no running cost.",
             "Money buys the entry, not effort."),
            ("Neither one asks you to trust a stranger.",
             "Both ask you to trust the cost of lying."),
            ("So - back to that night in twenty twenty-two.",),
            ("The miners did not need saving.",
             "They needed replacing.",
             "And they were - by a deposit, not a machine."),
            ("The full breakdown is linked below,",
             "and nothing here is financial advice.",
             "If that was useful, subscribe."),
        ],
        shots=[
            Shot(image=TRAILS, zoom=1.10, pan=(-0.02, 0.01),
                 aspect=A, bias=0.4),
            Shot(clip=CHESS, clip_at=11.0),
            None,                                    # ride the chain
            Shot(graphic="compare",
                 payload=("Proof of work",
                          ["Expensive hardware", "A real electricity bill",
                           "Anyone with a rig can try"],
                          "Proof of stake",
                          ["A staked deposit instead", "Almost no running cost",
                           "Money buys the entry, not effort"],
                          True)),
            Shot(image=CITYGRID, zoom=1.10, pan=(0.02, -0.01),
                 aspect=A, bias=0.5),
            # The echo: the industrial plant the video opened on, under the
            # line that reframes the opening one.
            Shot(clip=HIGHWAY, clip_at=13.0),
            # "The miners did not need saving. They needed replacing." - the
            # hardware being talked about, not smoke.
            Shot(image=GPUCARDS, zoom=1.10, pan=(0.02, 0.01),
                 aspect=A, bias=0.5),
            # Held on the abstract, so YouTube's end-screen cards have
            # somewhere uncluttered to sit.
            Shot(clip=AERIAL, clip_at=12.0),
        ],
        gaps=[0.60, 0.60, 0.55, 0.90, 0.80, 0.85, 0.85, 2.60],
    ),
]

META = Meta(
    title="What Is Proof of Stake? The Blockchain Without Miners",
    hook="Ethereum turned off every miner it had in 2022 and nothing broke. "
         "Here is what actually replaced the hardware.",
    url=URL,
    summary="How proof of stake actually works: locking a stake as collateral "
            "instead of burning electricity, how validators get picked, what "
            "slashing punishes and how, and the wealth-concentration problem "
            "it did not solve.",
    tags=["what is proof of stake", "proof of stake explained",
          "proof of stake vs proof of work", "ethereum validators",
          "staking explained", "crypto slashing", "crypto for beginners",
          "ethereum merge"],
    cta=f"The full breakdown of staking, slashing and validator selection: {URL}",
    credits=["Footage: Pexels (Pexels licence, no attribution required).",
             "Music: oosongoo, via Pixabay.",
             "Nothing in this video is financial advice."],
)


def main() -> None:
    out = Path.home() / "Desktop/proof-of-stake-long.mp4"
    work = Path.home() / "Desktop/.proof-of-stake-long-work"
    made = render_long(
        SECTIONS, out, work, brand=CRYPTO, meta=META, voice=VOICE,
        music=MUSIC,
        callouts=None,
        # The title's own question, tightened, accent on the word carrying the
        # tension.
        #
        # **The abstract solid was rejected on the user's note that it is
        # ugly, and the replacement is the video's own subject.** "What
        # replaced the miners?" over two graphics cards on black shows *the
        # thing that got replaced*, which opens the loop without answering it -
        # the answer is a staked deposit, and no card is on screen. It also
        # fixes the earlier problem that every candidate was either generic
        # (a pile of coins) or off-message (Bitcoin coins, when Bitcoin is the
        # chain that still has miners).
        #
        # L27/S4, whole subject, real black down one side for the type. No
        # `thumb_side`: the scorer picks crop and side together.
        # **Fitted, not cover-cropped.** The first cut let the scorer choose,
        # and it zoomed into one card and cut the other in half — the subject
        # was neither whole nor legible. `crop_zoom` below 1.0 is the engine's
        # own "stop covering the frame" mode: the picture is scaled to the size
        # asked for and set on black with a 260px falloff, so the whole pair of
        # cards survives and the type sits on real black rather than on a scrim
        # over detail. Swept 0.55/0.70/0.78/0.85 and looked: 0.85 starts
        # clipping the cards at the bottom edge, 0.55 leaves them small, 0.78
        # is the largest that keeps both whole.
        #
        # `side` is passed because `crop_at` bypasses the scorer, so there is
        # no layout pass left to infer a side from.
        thumb_headline="What replaced the [miners?]",
        thumb_image=GPUCARDS,
        thumb_accent="cyan",
        thumb_crop_at=(1.0, 0.5), thumb_crop_zoom=0.78, thumb_side="left",
        endcard=ENDCARD, endcard_lead=7.0,
    )
    for k, v in made.items():
        print(f"{k}: {v}")


if __name__ == "__main__":
    main()
