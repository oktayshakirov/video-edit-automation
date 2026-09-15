"""Do noise-canceling headphones help tinnitus - long-form 16:9 for YouTube.

Source: tinnitus-blog/content/posts/noise-canceling-headphones-for-tinnitus.mdx

**Why this post.** The honest answer is a real reversal, not a hedge: active
noise control removes the outside sound tinnitus was competing with, and for
plenty of people that helps - but strip away every outside sound and some
people's tinnitus gets *more* noticeable, not less, because the brain turns
its own gain up to fill the gap. That is the arc: promise the contradiction
in sentence two, explain the gain mechanism, show both sides with `compare`,
name the real downsides with `grid`, then the one practical fix with `steps`.

**Beat variety, chosen before the script** (silhouette rule, and checked
against the channel's last two article long forms - `does-magnesium-help-
tinnitus` and `brown-noise-vs-white-noise-for-tinnitus` - which both used
`diagram`, so it is skipped here on purpose): `compare` with `name_columns`
(a loud place vs a silent room), `grid` (the real downsides, with icons),
`steps` (the one fix, with icons). Three beats, three silhouettes, none
repeated from the last two builds.

**Every shot has headphones in it, and that is the whole footage brief.**
The first cut was rejected for exactly this: an airplane cabin, a woman in a
dark bedroom, an old man in a chair, hands on a laptop - all dark, all
on-palette, none of them about the subject. A video whose noun is a *device*
has no excuse for that, because unlike gain or habituation this noun can
actually be photographed. So the roster is people wearing headphones, the
headphones themselves, and two AirPods stills; the one airplane shot that
survives sits under the sentence that says "the drone of a plane" and lasts
one sentence.

**The medical line.** This is a low-risk topic - no red flags, no urgent
routing - so the standard disclaimer covers it. Nothing here promises relief;
it states what the article states (ANC can help in noise, can backfire in
silence, pairing with soft sound is the fix) and never claims a cure. No
initialisms are ever spoken - always "noise-canceling," never "ANC."

**The title sequence is the new `TitleOverlay`, not a `Shot(payload=)`.**
See `longform/overlay.py`: the centred-caps-on-a-black-band treatment the
title stamp used to borrow was called ugly on the first cut, and it was the
wrong device anyway - `payload` is a statement the footage illustrates, not a
title. `title_at` puts an animated lower third on the promise line instead.

Run from the repo root:

    PYTHONPATH=. .venv/bin/python projects/tinnitus-long/noise-canceling-headphones-for-tinnitus.py
"""

from pathlib import Path

from video_automation.core import music
from video_automation.core.brand import TINNITUS
from video_automation.core.stock import CACHE as STOCK
from video_automation.crypto.shots import Shot
from video_automation.longform import Meta, Section, render_long

SOURCE_POST = "noise-canceling-headphones-for-tinnitus"

# Clips. Screened with `stock.screen` at 0.5/3/6s and then watched; the
# trailing comment is the luma range and what is actually in the frame.
PUT_ON = STOCK / "videos/man-calm-listening-music-headphones-dark-room-eyes-closed"  # 6614768 30s L44 - putting on over-ear headphones
SOFA = STOCK / "videos/man-sitting-couch-headphones-dark-room-evening"     # 5708839 16s L37 - headphones on, warm lamp, at home
DESK_W = STOCK / "videos/person-headphones-sitting-window-calm-evening"    # 6892729 27s L40 - headphones at a desk, evening
TRAVEL = STOCK / "videos/noise-cancelling-headphones-travel"               # 6700181 20s L56 - reclined, over-ear headphones, cabin seat
STREET = STOCK / "videos/person-walking-city-street-night-headphones-dark-alone"  # 7948198 30s L42 - earbuds in, night street
CALM_W = STOCK / "videos/woman-listening-headphones-calm-dark-room-evening"  # 6688133 30s L34 - hand on the earcup, calm
AIRPODS_V = STOCK / "videos/over-ear-headphones-product-black-background-dark"  # 9636767 20s L1 - wireless earbuds turning on black

# Stills, each used once. All 6000px+, so every one bleeds off all four edges
# at `max_upscale` rather than rendering as a fitted panel.
PH = STOCK / "photos"
P_PORTRAIT = PH / "man-wearing-headphones-dark-moody-portrait/31510586.jpg"   # L31 - over-ear headphones, straight to camera
P_WARM = PH / "man-wearing-headphones-dark-moody-portrait/18464243.jpg"       # L25 - warm side light, headphones at the neck
# A flat-lay rather than the other still-life in this folder (6179026), which
# carries a legible wordmark across the earcup - this one's marks are small
# round emblems that read as a headphone detail rather than as a brand.
P_PRODUCT = PH / "over-ear-headphones-dark-still-life/1649771.jpg"            # L21 - the headphones themselves, on black
P_AIRPODS = PH / "wireless-earbuds-dark-background-product/30981655.jpg"      # L17 - earbuds and case lit in the brand's own peach
P_AIRPODS2 = PH / "wireless-earbuds-dark-background-product/10885669.jpg"     # L30 - earbuds beside a phone, on black

# The user's own pick. Bright teal where the rest of this channel is near
# black, which is the point of a thumbnail rather than a problem with it: it
# is the one asset that has to win a grid of dark rectangles, and the
# headphones are unmistakable at feed size.
THUMB_PHOTO = PH / "woman-holding-headphones-close-up/3757028.jpg"            # 7360x4912 - pexels.com/photo/3757028

ENDCARD = STOCK / "videos/subscribe/4928934.mp4"

VOICE = "mia"                        # the explainer default, per the project doc
MUSIC = music.track("night-drift")   # the prepared track, shared with thecrypto.wiki

URL = "https://tinnitushelp.me/blog/noise-canceling-headphones-for-tinnitus"


SECTIONS = [
    # --- hook: name tinnitus in sentence one, the reversal in sentence two -
    Section(
        title="Noise-canceling headphones",
        card=False,
        sentences=[
            ("You buy noise-canceling headphones to make your tinnitus quieter.",),
            ("You put them on,",
             "and the ringing gets louder instead."),
            ("That is not a broken pair of headphones.",
             "It is how your brain handles quiet."),
            ("Stay with this and you will know when noise-canceling actually "
             "helps, when it can backfire, and the one setting that fixes it "
             "either way.",),
        ],
        shots=[
            Shot(clip=PUT_ON / "6614768.mp4", clip_at=0.0),
            Shot(image=P_PORTRAIT, zoom=1.12, aspect=16 / 9, bias=0.42),
            None,
            Shot(clip=SOFA / "5708839.mp4", clip_at=0.0),
        ],
        gaps=[0.90, 0.55, 0.85, 0.45],
    ),

    # --- mechanism: what noise-canceling is actually doing, no beat ------
    Section(
        title="What Is Noise-Canceling Actually Doing?",
        spoken_title="So what is noise-canceling actually doing?",
        sentences=[
            ("Tiny microphones on the outside listen to the noise around you.",),
            ("And the headphones generate the exact opposite wave,",
             "to cancel it out before it reaches your ear."),
            ("It works best on one kind of sound: steady, low, and constant - "
             "an engine hum, an air conditioner, the drone of a plane.",),
            ("It is not built for a doorbell, a voice, or a sudden clatter.",),
        ],
        shots=[
            Shot(image=P_PRODUCT, zoom=1.14, aspect=16 / 9, bias=0.5),
            Shot(clip=DESK_W / "6892729.mp4", clip_at=0.0),
            # The one airplane shot in the cut, under the one sentence that
            # names a plane, for one sentence only.
            Shot(clip=TRAVEL / "6700181.mp4", clip_at=0.0),
            Shot(clip=STREET / "7948198.mp4", clip_at=0.0),
        ],
        gaps=[0.34, 0.55, 0.60, 0.85],
    ),

    # --- does the quiet help? the real reversal, so `compare` -------------
    Section(
        title="Does the Quiet Actually Help?",
        spoken_title="But does the quiet actually help?",
        sentences=[
            ("So does the quiet noise-canceling makes actually help?",
             "It depends on where you already are."),
            # 8 caption chunks: two headings plus three items a side, in the
            # order the voice says them. No lead-in sentence inside the span.
            ("In a loud place,",
             "it cuts the drone and the clatter,",
             "it lowers your stress,",
             "and your tinnitus can feel smaller by comparison.",
             "In a silent room,",
             "there is nothing left to compete with it,",
             "your brain turns its own gain up to fill the gap,",
             "and the ringing can feel louder, not quieter."),
            ("So the headphones did not change your tinnitus at all.",
             "They only changed what was around it."),
        ],
        shots=[
            Shot(image=P_AIRPODS, zoom=1.12, aspect=16 / 9, bias=0.5),
            # No `picture=` here - `compare` uses both halves of the frame and
            # the beat now refuses one rather than printing its right-hand
            # column through the photograph, which is what the first cut did.
            Shot(graphic="compare",
                 payload=("In a loud place",
                          ["It cuts the drone and the clatter",
                           "It lowers your stress",
                           "Your tinnitus can feel smaller by comparison"],
                          "In a silent room",
                          ["There is nothing left to compete with it",
                           "Your brain turns its own gain up",
                           "The ringing can feel louder, not quieter"],
                          True)),
            Shot(clip=PUT_ON / "6614768.mp4", clip_at=15.0),
        ],
        gaps=[0.45, 0.70, 0.85],
    ),

    # --- why quiet backfires: the gain mechanism, no beat -----------------
    Section(
        title="Why Would Quiet Make It Louder?",
        spoken_title="So why would quiet make it louder?",
        sentences=[
            ("Your hearing system is always listening for signal,",
             "even signal that is not really there."),
            ("Take away the outside noise,",
             "and there is nothing left to mask the one your brain was "
             "already making."),
            ("So in a very quiet room,",
             "your own ring can suddenly be the loudest thing in the house."),
        ],
        shots=[
            Shot(clip=CALM_W / "6688133.mp4", clip_at=0.0),
            None,
            Shot(clip=SOFA / "5708839.mp4", clip_at=6.0),
        ],
        gaps=[0.55, 0.60, 0.85],
    ),

    # --- the real downsides, so `grid` ------------------------------------
    Section(
        title="What Should You Watch For?",
        spoken_title="Now, what should you actually watch for?",
        sentences=[
            ("For a few people,",
             "the headphones add a few problems of their own."),
            ("A feeling of pressure or fullness in the ear.",
             "A faint hiss of their own, from the electronics.",
             "Muffled alarms, doorbells, and other people's voices.",
             "And a real cost, for the models that do this well."),
            ("None of that means anything is wrong with you.",
             "It just means the headphones are not free of trade-offs."),
        ],
        shots=[
            Shot(clip=TRAVEL / "6700181.mp4", clip_at=9.0),
            Shot(graphic="grid",
                 payload=([("Pressure or fullness in the ear", "", "\U0001F616"),
                           ("A faint hiss of their own", "", "\U000026A1"),
                           ("Muffled alarms and voices", "", "\U0001F514"),
                           ("A real cost, for the good ones", "", "\U0001F4B0")],
                          "WHAT TO WATCH FOR")),
            Shot(clip=STREET / "7948198.mp4", clip_at=15.0),
        ],
        gaps=[0.45, 0.70, 0.85],
    ),

    # --- the one fix, so `steps` -------------------------------------------
    Section(
        title="How Do You Use Them Right?",
        spoken_title="So how do you use them right?",
        sentences=[
            ("The fix is not to throw them away.",
             "It is to stop asking them for total silence."),
            ("Play a soft, steady sound through them.",
             "Keep it just under your tinnitus, not over it.",
             "Save total silence for when you actually want to sleep.",
             "And take them off for a few minutes every hour."),
            ("That one change is usually the difference between headphones "
             "that help,",
             "and headphones that backfire."),
        ],
        shots=[
            Shot(image=P_AIRPODS2, zoom=1.12, aspect=16 / 9, bias=0.5),
            Shot(graphic="steps",
                 payload=([("A soft, steady sound underneath", "\U0001F30A"),
                           ("Just under your tinnitus, not over it", "\U0001F509"),
                           ("Save real silence for sleep", "\U0001F634"),
                           ("Off for a few minutes every hour", "\U000023F0")],
                          "THE ONE FIX")),
            # Pushed in hard: the earbuds sit small and centred on pure black
            # in the source, so at the default 1.06 - and at 2.4, which was
            # tried - the frame reads as empty rather than as a product shot.
            # 4.2 is a real upscale and survives it because the subject is a
            # smooth glossy object on black with no fine detail to smear.
            Shot(clip=AIRPODS_V / "9636767.mp4", clip_at=8.0, zoom=4.2),
        ],
        gaps=[0.45, 0.70, 0.85],
    ),

    # --- close: the echo, then the real question --------------------------
    Section(
        title="Is It Actually Worth It?",
        spoken_title="So, is it actually worth it?",
        sentences=[
            ("So noise-canceling headphones were never built to fix tinnitus,",
             "and they still are not one."),
            ("Paired with a little sound instead of none at all,",
             "they can make a loud world quiet",
             "without turning up your own ring."),
            ("So next time the noise gets to be too much,",
             "would you reach for silence,",
             "or would you reach for sound?"),
        ],
        shots=[
            Shot(clip=CALM_W / "6688133.mp4", clip_at=16.0),
            Shot(image=P_WARM, zoom=1.12, aspect=16 / 9, bias=0.45),
            Shot(clip=DESK_W / "6892729.mp4", clip_at=12.0),
        ],
        gaps=[0.60, 0.90, 3.00],
    ),
]

META = Meta(
    title="Can Noise-Canceling Headphones Make Tinnitus Worse?",
    hook="Active noise control blocks the outside sound your tinnitus was "
         "competing with - which helps in a noisy place and can backfire in "
         "a silent one. Here is why quiet can make the ringing louder, the "
         "real downsides worth knowing, and the one setting that fixes it "
         "either way.",
    url=URL,
    summary="How active noise control actually works, why it helps in a "
            "noisy place but can make tinnitus more noticeable in total "
            "silence, the real downsides some people run into, and the "
            "practical fix - pairing the headphones with soft sound instead "
            "of total silence.",
    tags=["tinnitus", "noise canceling headphones tinnitus",
          "noise cancelling headphones tinnitus", "ANC and tinnitus",
          "does silence make tinnitus worse", "sound therapy for tinnitus",
          "ringing in ears"],
    cta=f"Full article and sources: {URL}",
    credits=["Footage: Pexels (Pexels licence, no attribution required).",
             "Music: night-drift.",
             "",
             "This video is general information, not medical advice. If "
             "your tinnitus is new, one-sided, pulsing with your heartbeat, "
             "worsening, or comes with dizziness or hearing loss, see a "
             "doctor or an ear specialist."],
)


def main() -> None:
    out = Path.home() / "Desktop/noise-canceling-headphones-for-tinnitus-long.mp4"
    work = Path.home() / "Desktop/.noise-canceling-headphones-for-tinnitus-work"
    made = render_long(
        SECTIONS, out, work, brand=TINNITUS, meta=META, voice=VOICE,
        music=MUSIC, callouts=None,
        endcard=ENDCARD, endcard_lead=7.0,
        # The animated lower third, on the promise line rather than frame one.
        title_at=8.5, title_hold=5.4,
        # Same source and headline as the Short. **The newline is deliberate
        # and load-bearing** - "Headphones on." and "Ringing louder?" are two
        # sentences and each one gets its own row, rather than the wrap
        # splitting them wherever the line lengths happen to even out. See
        # `thumbnails.md`.
        thumb_headline="Headphones on.\nRinging [louder?]",
        thumb_image=THUMB_PHOTO,
        thumb_accent="red", thumb_side="left",
        thumb_crop_at=(0.55, 0.30), thumb_crop_zoom=1.0, thumb_shift=0.26,
    )
    for k, v in made.items():
        print(f"{k}: {v}")


if __name__ == "__main__":
    main()
