"""Why are Bitcoin miners switching to AI? - long-form 16:9 for YouTube.

Source: crypto-wiki/content/posts/why-wall-street-is-betting-big-on-bitcoin-miners-for-ai.mdx.

**The angle.** The article is framed as news - a researcher's resignation, a
hedge fund's positions, named mining stocks and puts against chipmakers. None
of that goes in the video: `crypto.md` puts evergreen before news, the named
people carry per-video accuracy risk, and a fund's longs and shorts are a stock
tip by another name. What survives is the mechanism the whole trade rests on:
AI's bottleneck is *energized capacity*, a new data center waits years for a
grid connection, and a mining site already has one. The twist is that a mining
hall is not an AI hall by default, and the risk is that hosting income rides
the AI spending cycle.

**No financial advice, anywhere.** No company, ticker, fund, price or direction
is named. "Investors" is as specific as the money gets.

## The beats

Checked against the last three crypto long-forms (fear-greed: dial / bars /
diagram / quote / checklist; rug-pull: diagram / grid / gauge / steps / stat;
vitalik: compare / grid / quote / stat / steps):

* `grid` - what a mining site already has
* `bars` - time to powered capacity, new build against retrofit
* `stat` - the 2024 halving's block reward
* `compare` - mining income against hosting income
* `checklist` (flow, all struck) - what a mining hall is missing for AI

**No ASIC-farm footage exists in the cache or on Pexels** - every "mining
farm" query came back as coins on a table, stickers, a warehouse or a football
crowd. So the mining site is drawn (`grid`, `compare`) and the clips are the
act around it: pylons, a substation, cranes on a night build site, racks, a
network switch, trading screens under "investors".

**Thumbnail: pylons at dusk, no person.** A frame of the opening clip.

Phonemes checked with espeak-ng: AI, GPU, megawatts, substation, halving.

Run from the repo root:

    PYTHONPATH=. .venv/bin/python projects/crypto-long/miners-ai.py
"""

from pathlib import Path
from pathlib import Path as _P

from video_automation.core import music
from video_automation.core.brand import CRYPTO
from video_automation.core.stock import CACHE as STOCK
from video_automation.crypto.shots import Shot
from video_automation.longform import Meta, Section, render_long

SOURCE_POST = "why-wall-street-is-betting-big-on-bitcoin-miners-for-ai"

V = STOCK / "videos"
BRAND = _P(__file__).resolve().parents[2] / "assets/brand"

GPU_FANS = V / "computer-cooling-fan-dark/5467009.mp4"                 # 25.7s L12-19, GPU fans lit green/red
PYLONS = V / "high-voltage-power-lines-night/854741.mp4"               # 19.4s L52-82, pylons and a plant at dusk
PYLON_WIN = V / "electricity-pylon-power-lines-dusk/36669029.mp4"      # 15.0s L60, a pylon at dusk through a window
SUBSTATION = V / "electrical-substation-night/30264077.mp4"            # 15.2s L5, a lit substation from the air, night
RACKS = V / "data-center-gpu-servers/5028622.mp4"                      # 31.6s L70-91, server racks
RACK_HAND = V / "engineer-walking-data-center-dark/7670467.mp4"        # 14.8s L22-39, a technician reaching into a rack
CHIP = V / "microchip-processor-macro-dark/35977437.mp4"               # 20.9s L44-49, a processor on a circuit board
FIBER = V / "fiber-optic-light-cables-dark/8817471.mp4"                # 20.9s L39-49, fibre ends lit
BUILD = V / "construction-site-crane-night/35039490.mp4"               # 18.7s L44, a build site at night, trucks
CRANE = V / "construction-site-crane-night/7317317.mp4"                # 27.9s L37, a crane over a half-built tower
CITY_BUILD = V / "construction-site-crane-night/6164053.mp4"           # 15.0s L27-74, towers going up, night city
SWITCH = V / "server-room-data-center-dark-aisle/7140937.mp4"         # 14.3s L67-71, a network switch, cables seated
PYLON = V / "electricity-pylon-power-lines-dusk/27427299.mp4"         # 13.7s L100, one pylon against cloud
TOWERS = V / "power-plant-cooling-towers-night/4188245.mp4"            # 22.4s L87-101, cooling towers, sunset silhouette
TRADE1 = V / "stock-market-screen-dark/37962424.mp4"                   # 29.9s L23-32, a trading desk, charts
TRADE2 = V / "stock-market-screen-dark/38698438.mp4"                   # 20.3s L15, candles on a monitor
TRADE3 = V / "stock-market-screen-dark/38783512.mp4"                   # 21.7s L19-20, a falling chart on a monitor
CITY = V / "data-center-night-exterior/5744341.mp4"                    # 30.0s L41-43, a city from the air at night

BEATGROUND = BRAND / "beat-ground-crypto.jpg"
THUMB = BRAND / "graphics/miners-ai-pylons.jpg"                        # frame 3s of PYLONS
ENDCARD = V / "subscribe/4928934.mp4"

VOICE = "mia"
MUSIC = music.track("night-drift")
URL = ("https://thecrypto.wiki/posts/"
       "why-wall-street-is-betting-big-on-bitcoin-miners-for-ai")


SECTIONS = [
    # --- hook. No card. The reversal is sentence one. ----------------------
    Section(
        title="Not a chip shortage",
        card=False,
        sentences=[
            ("AI has a shortage,", "and it is not chips."),
            ("It is power -",
             "megawatts that are already plugged into the grid."),
            ("And some of the companies holding the most of it",
             "are Bitcoin miners."),
            ("Which is why investors started treating mining companies",
             "as AI infrastructure."),
            ("Stay to the end,",
             "and you will know exactly what a mining site has that AI "
             "needs -",
             "and what it still does not."),
        ],
        shots=[
            Shot(clip=GPU_FANS, clip_at=1.0),
            Shot(clip=PYLONS, clip_at=6.0),
            Shot(clip=RACKS, clip_at=2.0),
            Shot(clip=TRADE1, clip_at=1.0),
            Shot(clip=RACK_HAND, clip_at=1.0),
        ],
        gaps=[0.85, 0.60, 0.60, 0.55, 0.85],
    ),

    # --- reframe: an AI data center is an electricity problem --------------
    Section(
        title="What does an AI data center need?",
        spoken_title="So what does an AI data center actually need?",
        sentences=[
            ("Training a model is not a software problem first.",
             "It is an electricity problem."),
            ("And a Bitcoin mining site already has four of the things it "
             "needs.",),
            # the grid's own sentence - one caption chunk per card.
            ("Power at scale - fifty to five hundred megawatts on one site,",
             "a substation and a grid connection already built,",
             "cooling designed for hot, dense machines,",
             "and years of practice turning its load up and down with the "
             "grid."),
            ("For a decade, mining turned electricity into hashes.",
             "AI turns the same electricity into computation."),
        ],
        shots=[
            Shot(clip=CHIP, clip_at=1.0),
            Shot(clip=FIBER, clip_at=1.0),
            Shot(graphic="grid", backdrop=BEATGROUND,
                 payload=([("Power at scale", "50 to 500 MW on one site"),
                           ("A grid connection", "the substation is already built"),
                           ("Cooling", "designed for hot, dense machines"),
                           ("Grid flexibility", "used to turning load up and down")],
                          "WHAT A MINING SITE ALREADY HAS")),
            Shot(clip=PYLON_WIN, clip_at=1.0),
        ],
        gaps=[0.60, 0.60, 1.00, 0.85],
    ),

    # --- deep dive: the grid connection is the scarce thing ----------------
    Section(
        title="Why is a grid connection worth so much?",
        spoken_title="So why is that grid connection worth so much?",
        sentences=[
            ("Because a brand-new data center has to wait for one.",),
            # the bars' own sentence - one chunk per row.
            ("A new build can take two to three years to get powered,",
             "a mining site retooled for AI can take three to nine months."),
            ("The transformers are already delivered.",
             "The permits already exist."),
            ("In a market short on power,",
             "that head start is the product."),
        ],
        shots=[
            Shot(clip=BUILD, clip_at=1.0),
            Shot(graphic="bars", backdrop=BEATGROUND,
                 payload=([("New data center", 1.00, "24-36 months"),
                           ("Retooled mining site", 0.25, "3-9 months")],
                          "TIME TO POWERED CAPACITY")),
            Shot(clip=PYLON, clip_at=1.0),
            Shot(clip=CRANE, clip_at=1.0),
        ],
        gaps=[0.60, 1.10, 0.60, 0.85],
    ),

    # --- mining income against hosting income -------------------------------
    Section(
        title="How is hosting AI different from mining?",
        spoken_title="So how is hosting AI different from mining?",
        sentences=[
            ("Mining income moves with things no miner controls.",),
            ("In April twenty twenty-four, the halving cut the reward for "
             "every block",
             "from six point two five bitcoin to three point one two five."),
            # the compare's own sentence - 2 headings + 3 + 3 = 8 chunks.
            ("Take the mining side.",
             "It is paid in bitcoin,",
             "it moves with price and difficulty,",
             "and the reward halves roughly every four years.",
             "Now compare that with AI hosting.",
             "A client pays per rack or per kilowatt,",
             "under a contract that runs for years,",
             "tied to uptime, not to the price of a coin."),
            ("That is why many miners do not pick one.",
             "They keep mining, and rent part of the site to AI."),
        ],
        shots=[
            Shot(clip=TRADE2, clip_at=1.0),
            Shot(graphic="stat", backdrop=BEATGROUND,
                 payload=("3.125 BTC", "BLOCK REWARD AFTER THE 2024 HALVING",
                          "Down from 6.25 - the same work earns half",
                          False)),
            Shot(graphic="compare", backdrop=BEATGROUND,
                 payload=("MINING",
                          ["Paid in bitcoin",
                           "Moves with price",
                           "Halves every 4 years"],
                          "AI HOSTING",
                          ["Paid per rack or kW",
                           "Multi-year contract",
                           "Tied to uptime"],
                          True)),
            Shot(clip=RACKS, clip_at=14.0),
        ],
        gaps=[0.55, 0.85, 1.10, 0.85],
    ),

    # --- twist: a mining hall is not an AI hall by default ------------------
    Section(
        title="Is a mining site already an AI data center?",
        spoken_title="But is a mining site really an AI data center already?",
        sentences=[
            ("Not by default.",),
            ("A typical mining hall is missing four things.",),
            # the checklist's own sentence - flow=True, one chunk per item.
            ("Not the liquid cooling that GPU racks need,",
             "not the fast network that training clusters depend on,",
             "not the security standards enterprise clients check,",
             "and not the staff trained on GPUs instead of mining machines."),
            ("Bolt GPU racks into an air-cooled hall,",
             "and they overheat and slow themselves down."),
            ("The power is the head start.",
             "The retrofit is still real work."),
        ],
        shots=[
            Shot(clip=RACK_HAND, clip_at=5.0),
            Shot(clip=GPU_FANS, clip_at=12.0),
            Shot(graphic="checklist", backdrop=BEATGROUND,
                 payload=([("Liquid cooling for GPU racks", False),
                           ("A low-latency network", False),
                           ("Enterprise security standards", False),
                           ("Staff trained on GPUs", False)],
                          "IS A MINING HALL READY FOR AI?", True)),
            Shot(clip=CHIP, clip_at=10.0),
            Shot(clip=SWITCH, clip_at=1.0),
        ],
        gaps=[0.85, 0.60, 1.20, 0.60, 0.85],
    ),

    # --- the risk, the echo, the ask ----------------------------------------
    Section(
        title="What could still go wrong?",
        spoken_title="And what could still go wrong?",
        sentences=[
            ("Hosting income depends on the AI build-out continuing.",),
            ("If AI spending slows,",
             "the miners that now rely on it feel it directly -",
             "right alongside the AI companies themselves."),
            ("The grid connection does not change.",
             "What it is worth can."),
            ("Nothing in this video is financial advice.",),
            ("So the next time you hear that AI is running out of chips -",
             "would you ask who has the power instead?"),
        ],
        shots=[
            Shot(clip=TRADE3, clip_at=1.0),
            Shot(clip=TOWERS, clip_at=2.0),
            Shot(clip=CITY, clip_at=1.0),
            Shot(clip=SUBSTATION, clip_at=2.0,
                 payload=("", "This is not financial advice.")),
            Shot(clip=CITY_BUILD, clip_at=4.0),
        ],
        gaps=[0.60, 0.85, 0.85, 1.10, 2.30],
    ),
]

META = Meta(
    title="Why Are Bitcoin Miners Switching to AI?",
    hook="AI's real shortage is not chips - it is power already connected to "
         "the grid. Here is why Bitcoin mining sites have it, what they still "
         "lack, and what could go wrong.",
    url=URL,
    summary="Why Bitcoin miners are turning mining sites into AI data centers: "
            "power at scale, a grid connection already built, cooling and "
            "grid flexibility. Why a new data center waits two to three years "
            "for power while a retooled mining site can take three to nine "
            "months, how hosting income differs from mining income after the "
            "2024 halving, the four things a mining hall is missing for AI, "
            "and the risk of depending on the AI spending cycle. Nothing here "
            "is financial advice.",
    tags=["bitcoin miners ai", "why are bitcoin miners switching to ai",
          "bitcoin mining ai data centers", "ai data center power",
          "bitcoin mining explained", "ai hosting vs bitcoin mining",
          "bitcoin halving miners", "ai power shortage",
          "crypto mining ai", "bitcoin miners hpc"],
    cta=f"The full guide - the economics, the retrofit and the risks: {URL}",
    credits=["Footage: Pexels (Pexels licence, no attribution required).",
             "Music: oosongoo, via Pixabay.",
             "Nothing in this video is financial advice."],
)


def main() -> None:
    out = Path.home() / "Desktop/crypto-miners-ai-long.mp4"
    work = Path.home() / "Desktop/.crypto-miners-ai-long-work"
    made = render_long(
        SECTIONS, out, work, brand=CRYPTO, meta=META, voice=VOICE,
        music=MUSIC,
        callouts=None,
        thumb_headline="Why AI wants Bitcoin [miners]",
        thumb_image=THUMB,
        thumb_accent="yellow",
        endcard=ENDCARD, endcard_lead=7.0,
        title_at=8.5, title_hold=5.4,
    )
    for k, v in made.items():
        print(f"{k}: {v}")


if __name__ == "__main__":
    main()
