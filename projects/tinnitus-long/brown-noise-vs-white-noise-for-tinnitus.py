"""White noise vs brown noise for tinnitus - long-form 16:9 for YouTube.

Source: tinnitus-blog/content/posts/brown-noise-vs-white-noise-for-tinnitus.mdx

**Why this post.** "White noise vs brown noise for tinnitus" is a real
high-volume evergreen search, and the honest answer is counterintuitive: the
colour is the least important choice. What matters is roughly matching the
pitch of your tinnitus and keeping the volume low - the article says so
outright ("Set the volume like this - it matters more than the colour"). The
arc: kill the colour-wheel anxiety, explain what the colours actually are,
match colour to pitch, then spend the longest chapter on partial masking and
the volume arms race, a short chapter on notched therapy, and an honest close
that masking makes tonight easier and does not treat the tinnitus.

**Beats, chosen before the script** (silhouette + rotation rule - the last
three tinnitus long forms all ran compare / stat / steps, so this set drops
stat and steps and leans on the two new shapes):

- `grid` - the five noise colours, each with what it sounds like and an icon.
- `compare` with `name_columns` - a high whistle vs a low hum, and which
  colour each one wants.
- `gauge` - partial masking against the point where you have buried the
  ringing completely. The marker crosses the line and the fill turns; this is
  the "say the point, then show it" rule inside one beat, and the section the
  article itself flags as mattering most.
- `diagram` - notched sound therapy, the lateral-inhibition mechanism, four
  nodes, no loop. The kind of causal chain nothing else in the library draws.

Four distinct silhouettes: full-width cards, two named columns, one scale,
boxes-and-arrows. All four animate against the voice (`span_p` / `open_p`).

**The medical line.** Every claim is the article's own. Masking is described
by what it does - it overlaps the frequency region, it gives partial cover, it
leaves gentle exposure for habituation - never by what it will do for the
viewer. No cure, no promise of relief. The close is the article's own honest
summary: masking makes tonight easier to sit with; it does not treat the
tinnitus. No initialisms spoken.

**Footage.** Stock plus the drawn beats - the site's images for this post are
600-800px and shot bright (`kid-and-dad-with-headphones.jpg` 800px, most
others 600px and well over L100), so nothing from the library is dark enough
or large enough to cut, the same call the caffeine and pulsatile pairs made.
Every clip screened with `stock.screen` across its length; trailing comment is
the luma range.

**Phonemes.** `tinnitus` -> `tˈɪnɪɾəs`, `decibels`, `masking`, `notched`,
`habituation` all phonemize cleanly. "lateral inhibition" appears only on the
diagram card, never spoken. No initialisms.

Run from the repo root:

    PYTHONPATH=. .venv/bin/python projects/tinnitus-long/brown-noise-vs-white-noise-for-tinnitus.py
"""

from pathlib import Path

from video_automation.core import music
from video_automation.core.brand import TINNITUS
from video_automation.core.stock import CACHE as STOCK
from video_automation.crypto.shots import Shot
from video_automation.longform import Meta, Section, render_long

SOURCE_POST = "brown-noise-vs-white-noise-for-tinnitus"

# Screened with `stock.screen` across the clip AND watched frame-by-frame -
# several folder names lied (`woman-looking-out-window` was a woman reading in
# a rustic shed; `deep-ocean-underwater` was near-black and empty), so every
# clip here has had a real frame looked at. Trailing comment is the luma
# range.
LISTEN_M = STOCK / "videos/man-listening-music-dark-room-night"              # 7948198 29.5s L37-42/S6-8 - earphones, head down - opener
CONTEMPLATE_M = STOCK / "videos/man-contemplating-window-night-city-dark"    # 4538212 16s L51/S9 - at a window (caffeine-approved)
THINK_M2 = STOCK / "videos/person-thinking-dark-room-serious"               # 7698440 28s L42-46/S11-15 - pensive profile
THINK_M3 = STOCK / "videos/man-sitting-alone-thinking-dark-room-decision"    # 8458662 24.6s L41/S8 - man alone on a stool
RIPPLE = STOCK / "videos/calm-dark-water-ripple-slow-night"                  # 11287848 30s L21/S23 - dark blue water
OCEAN = STOCK / "videos/ocean-waves-dark-night-moody"                       # 16764714 24.6s L46/S17 - waves, "roar"
RAIN = STOCK / "videos/rain-on-window-at-night-dark"                        # 15161525 16s L31/S13 - rain on glass (precedent)
RAIN2 = STOCK / "videos/raindrops-glass-night-dark"                        # 29900465 14.8s L42/S22 - rain, warm bokeh
STARS = STOCK / "videos/dark-starry-sky-slow-drift-night-calm"             # 12354568 11s L13/S2 - calm night sky
VOL_KNOB = STOCK / "videos/hand-turning-volume-knob-dark"                  # 12213088 10s L15/S7 (spike-short precedent)
PHONE = STOCK / "videos/man-looking-at-phone-worried-dark"                 # 7699007 13.5s L36/S13 - person + phone at night, screen not shown
NEURONS = STOCK / "videos/brain-neurons-abstract-dark"                    # 29184317 10s L24-27/S42-48 - amber neurons (first ~5s)
NODES = STOCK / "videos/network-nodes-glowing-connections-dark"           # 34992134 10s L15/S7 - grey node cluster
NODES2 = STOCK / "videos/network-nodes-glowing-connections-dark"          # 35002501 10s L34/S8 - grey node cluster
LAMP = STOCK / "videos/bedside-lamp-dark-bedroom-night"                   # 10387906 25s L46/S24 - person in bed, bedside table
RELAX_W = STOCK / "videos/woman-relaxing-calm-eyes-closed-dark"           # 5114850 7.7s L45/S14 - calm face (first ~5s only)
AWAKE = STOCK / "videos/person-lying-awake-in-bed-night-dark"             # 8376628 21s L27-31/S14-18
CEIL = STOCK / "videos/ceiling-dark-bedroom-night-calm"                   # 11956219 28.5s L30/S6 - a bed at night
ENDCARD = STOCK / "videos/subscribe/4928934.mp4"

# A clean object shot - white earbuds on dark fabric - shared with the Short's
# cover and the 16:9 thumbnail. Headphones say the topic without a face to
# place, and the two-colour headline is what carries the hook.
THUMB_PHOTO = (STOCK / "photos"
               / "person-earphones-dark-portrait"
               / "18573077.jpg")

VOICE = "mia"                       # the explainer default, per the project doc
MUSIC = music.track("night-drift")  # the prepared track, shared with the Short

URL = "https://tinnitushelp.me/blog/brown-noise-vs-white-noise-for-tinnitus"


SECTIONS = [
    # --- hook: name the subject in sentence one, write the promise last -----
    Section(
        title="The colour wheel",
        card=False,
        sentences=[
            ("Your favourite tinnitus app has a colour wheel now.",),
            ("White, pink, brown, green -",
             "and nothing telling you which one to pick."),
            ("So here is the short version.",),
            ("The colour matters less than two other things:",
             "getting close to the pitch of your ringing,",
             "and keeping it quiet."),
            ("By the end you will know which colour to start with tonight,",
             "and how loud to set it."),
        ],
        shots=[
            # Opens on the same face the Short opens on - a person listening
            # with earphones, which is also what the earbuds thumbnail shows.
            Shot(clip=LISTEN_M / "7948198.mp4", clip_at=8.0),
            Shot(clip=PHONE / "7699007.mp4"),
            None,
            Shot(clip=CONTEMPLATE_M / "4538212.mp4"),
            Shot(clip=RIPPLE / "11287848.mp4",
                 payload=("", "WHITE NOISE VS BROWN NOISE FOR TINNITUS")),
        ],
        gaps=[0.55, 0.60, 0.55, 0.55, 0.80],
    ),

    # --- reframe: the colours are real recipes, so `grid` ------------------
    Section(
        title="What do the noise colours actually mean?",
        spoken_title="So what do the noise colours actually mean?",
        sentences=[
            ("The names are not marketing.",
             "Each colour is a real description of how the sound spreads its "
             "energy across low and high."),
            ("You will see five of them most often.",),
            # grid - one caption chunk per card, five cards.
            ("White noise is a flat, even hiss, like television static.",
             "Pink noise pulls the energy down a little, and sounds like "
             "steady rain.",
             "Brown noise pulls it down hard, into a deep waterfall.",
             "Grey noise is shaped to match how your own ears hear.",
             "And green noise sits in the middle, like a forest."),
            ("Here is the catch.",
             "White noise sounds far harsher than that flat recipe suggests,",
             "because your ears are much more sensitive to high sounds than "
             "low ones."),
            ("That is why pink and brown feel more natural.",
             "They are leaning against your hearing instead of fighting it."),
        ],
        shots=[
            Shot(clip=NODES2 / "35002501.mp4"),
            Shot(clip=THINK_M3 / "8458662.mp4", clip_at=3.0),
            Shot(graphic="grid",
                 payload=([("White noise", "a sharp, even hiss", "\U0001F4FA"),
                           ("Pink noise", "steady rain, the safe default",
                            "\U0001F327️"),
                           ("Brown noise", "a deep waterfall", "\U0001F30A"),
                           ("Grey noise", "shaped to your hearing",
                            "\U0001F39A️"),
                           ("Green noise", "forest and open field",
                            "\U0001F332")],
                          "THE NOISE COLOURS")),
            Shot(clip=THINK_M2 / "7698440.mp4", clip_at=3.0),
            Shot(clip=RAIN / "15161525.mp4", clip_at=8.0),
        ],
        gaps=[0.55, 0.60, 0.45, 0.60, 0.80],
    ),

    # --- match the colour to the pitch, so `compare` ----------------------
    Section(
        title="Which colour matches your tinnitus?",
        spoken_title="So which colour matches your tinnitus?",
        sentences=[
            ("Masking works by overlap.",
             "A sound only covers your tinnitus if it carries energy at the "
             "same pitch."),
            ("So it comes down to what your tinnitus actually sounds like.",),
            # compare, name_columns -> 8 chunks: 2 headings + 3 + 3 items.
            ("If it is a high whistle or ring -",
             "the most common kind by far,",
             "sitting up at a high pitch,",
             "start with white or pink.",
             "If it is a low hum or roar instead -",
             "less common, but real,",
             "sitting down low,",
             "reach for brown."),
            ("Put white noise under a low hum and it does nothing useful.",
             "It misses the hum completely and piles tiring hiss on top."),
            ("If you have no idea what pitch yours is, use pink,",
             "and give each colour a full evening before you judge it."),
        ],
        shots=[
            Shot(clip=NODES / "34992134.mp4"),
            Shot(clip=CONTEMPLATE_M / "4538212.mp4", clip_at=8.0),
            Shot(graphic="compare",
                 payload=("A high whistle or ring",
                          ["The most common kind",
                           "Sits up at a high pitch",
                           "Start with white or pink"],
                          "A low hum or roar",
                          ["Less common, but real",
                           "Sits down low",
                           "Reach for brown"],
                          True)),
            Shot(clip=OCEAN / "16764714.mp4"),
            Shot(clip=RAIN2 / "29900465.mp4"),
        ],
        gaps=[0.55, 0.65, 0.45, 0.70, 0.80],
    ),

    # --- the twist: volume matters more than colour, so `gauge` -----------
    Section(
        title="How loud should it be?",
        spoken_title="So how loud should it be?",
        sentences=[
            ("This matters more than the colour,",
             "and almost everyone gets it wrong."),
            ("The instinct is to turn it up until the ringing is gone.",),
            ("Aim for something called partial masking.",),
            # gauge - chunk 0 draws the scale and the line, chunk 1 crosses it.
            ("Set the sound just below your tinnitus, so you can still faintly "
             "hear it underneath.",
             "Push it past that line, burying the ringing completely, and you "
             "lose the gentle exposure your brain needs to tune it out."),
            ("And keep it under about eighty decibels.",
             "Masking runs for hours, so the total adds up."),
            ("For all night, use a speaker on the bedside table, not earbuds.",
             "Sealed ears make the ringing louder the moment the sound "
             "stops."),
        ],
        shots=[
            Shot(clip=VOL_KNOB / "12213088.mp4"),
            None,  # hold the volume knob through "the instinct is to turn it up"
            Shot(clip=AWAKE / "8376628.mp4"),
            Shot(graphic="gauge",
                 payload=("BURIED", 0.80, "the ringing is gone", 0.44,
                          "partial masking - aim here",
                          "HOW LOUD SHOULD IT BE?")),
            Shot(clip=LAMP / "10387906.mp4"),
            Shot(clip=CEIL / "11956219.mp4"),
        ],
        gaps=[0.55, 0.85, 0.60, 0.45, 0.65, 0.85],
    ),

    # --- a different approach entirely, so `diagram` ---------------------
    Section(
        title="What about notched sound therapy?",
        spoken_title="So what about notched sound therapy?",
        sentences=[
            ("There is a completely different approach worth knowing about.",),
            ("Instead of covering your tinnitus, notched therapy removes its "
             "exact pitch from the sound.",),
            # diagram - four nodes, one caption chunk each, no loop.
            ("It cuts your exact pitch out of music or noise.",
             "That frequency band goes quiet.",
             "Nerve cells around it start turning the area down.",
             "And over months, the overactive signal can weaken."),
            ("The evidence is genuinely mixed,",
             "and it needs you to know your tinnitus pitch fairly well."),
            ("It is a slow experiment, not a quick fix -",
             "but it is free to try."),
        ],
        shots=[
            Shot(clip=NEURONS / "29184317.mp4"),
            Shot(clip=NODES2 / "35002501.mp4", clip_at=3.0),
            Shot(graphic="diagram",
                 payload=([("Cut out your exact pitch", "from music or noise",
                            "\U0001F3AF"),
                           ("That band goes quiet", None, "\U0001F515"),
                           ("Neighbouring nerve cells turn it down",
                            "lateral inhibition", "\U0001F9E0"),
                           ("The overactive signal weakens",
                            "over months, not nights", "\U0001F4C9")],
                          "NOTCHED SOUND THERAPY", False)),
            Shot(clip=NODES / "34992134.mp4", clip_at=3.0),
            Shot(clip=THINK_M2 / "7698440.mp4", clip_at=15.0),
        ],
        gaps=[0.55, 0.60, 0.45, 0.70, 0.80],
    ),

    # --- close: echo the opening, keep the expectation honest ------------
    Section(
        title="So which one do you start with?",
        spoken_title="So which one do you start with?",
        sentences=[
            ("Start with pink.",),
            ("Move toward white if your tinnitus is a high whistle,",
             "toward brown if it is a low hum."),
            ("Keep the volume just under the ringing,",
             "and give each colour a full night before you switch."),
            ("And keep the expectation honest.",),
            ("Masking makes tonight easier to sit with.",
             "It does not treat the tinnitus itself -",
             "the things that change that work slower, in the background."),
            ("So tonight, when the room goes quiet:",
             "which colour are you reaching for?"),
        ],
        shots=[
            Shot(clip=RAIN / "15161525.mp4", clip_at=6.0),
            Shot(clip=RIPPLE / "11287848.mp4"),
            Shot(clip=STARS / "12354568.mp4"),
            Shot(clip=LISTEN_M / "7948198.mp4", clip_at=22.0),
            Shot(clip=RELAX_W / "5114850.mp4"),
            Shot(clip=OCEAN / "16764714.mp4", clip_at=12.0),
        ],
        gaps=[0.80, 0.55, 0.55, 0.80, 0.55, 2.40],
    ),
]

META = Meta(
    title="White Noise vs Brown Noise for Tinnitus",
    hook="The colour is the least important choice. What actually matters is "
         "roughly matching the pitch of your tinnitus and keeping the volume "
         "low - here is how each colour sounds, which suits which pitch, and "
         "how to set the level.",
    url=URL,
    summary="What the noise colours actually are, how to match white, pink or "
            "brown to the pitch of your tinnitus, why partial masking beats "
            "burying the sound and how the volume creeps up, and where notched "
            "sound therapy fits.",
    tags=["tinnitus", "white noise vs brown noise", "brown noise for "
          "tinnitus", "white noise for tinnitus", "pink noise tinnitus",
          "sound therapy for tinnitus", "masking tinnitus",
          "ringing in ears"],
    cta=f"Full article, the colour table and sources: {URL}",
    credits=["Footage: Pexels (Pexels licence, no attribution required).",
             "Music: licensed for this channel.",
             "",
             "This video is general information, not medical advice. If your "
             "tinnitus is new, one-sided, pulsing with your heartbeat, "
             "worsening, or comes with dizziness or hearing loss, see a "
             "doctor or an ear specialist."],
)


def main() -> None:
    out = Path.home() / "Desktop/brown-noise-vs-white-noise-long.mp4"
    work = Path.home() / "Desktop/.brown-white-long-work"
    made = render_long(
        SECTIONS, out, work, brand=TINNITUS, meta=META, voice=VOICE,
        music=MUSIC, music_gain=1.0, callouts=None,
        endcard=ENDCARD, endcard_lead=7.0,
        keep_work=True,
        # The headline colour-codes each noise to its own box: {white noise}
        # on a pale plate, [brown noise] on a brown one - the plate is the
        # meaning. The scorer places the type against the earbuds shot with no
        # face to protect.
        thumb_headline="{White noise} or [brown noise]?",
        thumb_image=THUMB_PHOTO,
        thumb_accent="brown",
        thumb_accent2="paper",
    )
    for k, v in made.items():
        print(f"{k}: {v}")


if __name__ == "__main__":
    main()
