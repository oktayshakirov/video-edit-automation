"""Sleeping with tinnitus — long-form 16:9 for YouTube.

Source: tinnitus-blog/content/posts/tinnitus-and-sleep.mdx.

**Why this post.** It is the site's highest-intent uncovered page — "how to
sleep with tinnitus" is a two-in-the-morning search, the post is marked
`featured`, and the answer routes straight to this brand's own masking sessions
and app. It also has the one thing an explainer needs and most health posts do
not: **a single counterintuitive reframe that fits in a sentence.** Your
tinnitus did not get louder. Your room got quieter.

**Beat variety chosen before the script**, per the crypto skill's silhouette
rule. Six beats, six different outlines, each used exactly once:

    quote → compare → checklist → grid → stat → steps

`compare` carries the mechanism, because day-versus-midnight is literally an
A/B and 16:9 is a very good shape for one. `checklist` runs `flow=True` — the
narration says "earplugs make it worse" as the cross lands, so holding the
verdict back would put the picture behind the voice.

**No `bars`.** The gaming cut earned one because the article carried a decibel
table, and a budget is a proportion. This post has no figures to draw against a
limit, and inventing a scale to fill a beat slot would be the one thing `bars`
must never do. Six beats without it is still six silhouettes.

**The picture library fails this post almost completely**, and the filenames are
why it took a contact sheet to find out. Screened and rejected: `sleeping-
woman.jpg` is a woman in a hammock in full daylight; `evening-routine.jpg` is
somebody cheering at a television; `silence.jpg` is a teal studio "shh" stock
shot; `sleeping-kid.jpg` — the article's own hero — is a sleeping child at
L220, both blinding and the wrong subject for adult sleep advice. `relaxing-
woman.jpg` and `sound-therapy-headphones.jpg` are both women wearing headphones
in bed, which contradicts the very advice the section gives (speaker, not
earbuds, for all-night use) — off-message is worse than off-palette.

What survives is two images, **neither of which can take a full frame**:
`therapy.jpg` at L143 and `audiologist.jpg` at L179, both well over the ~L82
ceiling for a full-frame site photograph. Both sit in beat picture columns
where they are downscaled and small.

So **the one photograph in this cut is stock** — `AWAKE_PHOTO`, a lit face in a
dark bedroom at L36, which is inside the ceiling and can therefore take the
full frame. It is also the thumbnail, which is the point: one picture doing
both jobs.

**Water appears once, and it carries a line.** The first cut used the
calm-water stock four times with nothing on it, and unlabelled water under a
script about bedrooms illustrates nothing — it is wallpaper, and it was called
out on review. Rain on a window replaced three of those, and rain earns its
place because it is one of the sounds the post actually recommends: the footage
is now the subject rather than filler.

**The background behind every drawn beat is `core.backdrop`**, not the ruled
grid this format used to draw. That grid stepped a whole pixel at a time on a
layer moving 40 px/s and it juddered worst on the long beats — which is what
"the background is laggy at 1:00 and 1:35" was. See that module.

**The medical line.** Everything factual is the article's own: the contrast
mechanism, the three compounding factors, sound set *just below* the tinnitus,
speaker over earbuds, the twenty-minute rule, a fixed wake time. Sound therapy
is described as making tinnitus less noticeable — never as treating it. Talking
therapy for insomnia is named as the first-line treatment for chronic insomnia,
which is the article's claim about insomnia and not a claim about tinnitus.
Nothing promises sleep. Disclaimer in `Meta.credits`.

**Phonemes.** Avoided: `CBT`, `CBT-I`, `MBSR`, `ENT` — the narration says
"talking therapy for insomnia" and "an audiologist or a sleep specialist",
which is what they mean to this audience anyway. Times are spelled out ("eleven
at night", "twenty minutes") rather than left as digits; the digits stay on
screen where they read better. `tinnitus` itself is safe.

Run from the repo root:

    PYTHONPATH=. .venv/bin/python projects/tinnitus-long/tinnitus-and-sleep.py
"""

from pathlib import Path

from video_automation.core import music
from video_automation.core.brand import TINNITUS
from video_automation.core.stock import CACHE as STOCK
from video_automation.crypto.shots import Shot
from video_automation.longform import Meta, Section, render_long

IMG = Path.home() / "Coding/tinnitus-blog/public/images"

# Screened with `stock.screen` at 0.5/3/6/9s; trailing comment is the range
# across the whole clip, not one frame.
AWAKE = STOCK / "videos/insomnia-awake-night-bed"
NIGHT = STOCK / "videos/sleeping-night-calm-dark"
TIREDM = STOCK / "videos/tired-man-rubbing-temples-dark"
TIREDW = STOCK / "videos/headache-stress-tired-woman-dark"
WATER = STOCK / "videos/calm-water-ripple-dark"
WAVES = STOCK / "videos/abstract-dark-waves-motion"
SOUND = STOCK / "videos/sound-wave-visualization-dark"
RAIN = STOCK / "videos/rain-on-window-at-night-dark"
LAMP = STOCK / "videos/bedside-lamp-dark-bedroom-night"
CLOCK = STOCK / "videos/alarm-clock-night-dark-bedroom"
BEDW = STOCK / "videos/caucasian-woman-awake-in-bed-night-dark-bedroom"
SITW = STOCK / "videos/blonde-woman-insomnia-bed-night-dark"
TIREDP = STOCK / "videos/stressed-man-dark-studio-portrait-grey"
ENDCARD = STOCK / "videos/subscribe/4928934.mp4"

# The one photograph in the cut. Screened L26 S35, inside the ~L82 ceiling a
# full-frame picture has to meet — the site's own library had nothing close
# (see above), so this is stock. The visible clock reading 4:56 does the
# section's work without a caption.
AWAKE_PHOTO = STOCK / "photos/woman-awake-in-bed-at-night-dark-room-insomnia/6943991.jpg"

# **Same source as the Short's thumbnail — the user's rule is to always match
# the pair.** This is the photo from the user's own Pexels pick
# (pexels.com/photo/9787924), an overhead shot of a woman asleep beside her
# phone. `side="left"` puts the type over the plain pillow and leaves the
# phone visible on the picture side, which ties the type directly to what the
# photo is actually of.
THUMB_PHOTO = STOCK / "photos/woman-sleeping-beside-smartphone/9787924.jpg"

VOICE = "mia-calm"              # af_heart at 1.00. `ivy` was tried and cut —
                                # the British read was not wanted, and the
                                # profile is deleted rather than left lying
                                # around. This is the channel's own reader at
                                # an unhurried pace, which is the delivery a
                                # bedtime script wanted anyway. Candidate.

# Picked by ear by the user, over the generated `bright` preset. Stored trimmed
# in `assets/brand/music/` because it is 7.7s and loops twenty-nine times
# across this cut — see `core/music.py` for why the trim is not optional.
MUSIC = music.track("night-drift")

URL = "https://tinnitushelp.me/blog/tinnitus-and-sleep"
A = 16 / 9


SECTIONS = [
    # --- hook: the room everybody knows ----------------------------------
    Section(
        title="Two in the morning",
        card=False,
        sentences=[
            ("It is two in the morning.",
             "The house is silent.",
             "And your ears are not."),
            ("All day it was manageable.",
             "Now it is the only thing in the room."),
            ("So you lie there",
             "waiting for it to fade",
             "so you can finally sleep."),
            # Split deliberately. As one sentence this ran long on a single
            # shot and it sits at 10-20s, which is where the retention drop
            # is steepest.
            ("Here is the part that changes it:",
             "your tinnitus did not get louder tonight."),
            ("By the end of this",
             "you will know exactly why nights are worse,",
             "what to put in the room,",
             "and the one setting almost everybody gets wrong."),
        ],
        shots=[
            # A face, at night, moving, on frame one — the note from the
            # first tinnitus cut. This reads as "awake at 3am" instantly and
            # no photograph in the library gets close.
            Shot(clip=AWAKE / "6944078.mp4"),            # L27-35 S24-33
            None,
            Shot(clip=AWAKE / "8376628.mp4", clip_at=2.0),   # L25-30 S13-17
            # The title stamp, on the turn rather than the opening frame.
            Shot(clip=LAMP / "10387906.mp4",             # L36-46 S23-29
                 payload=("", "WHY IT IS WORSE AT NIGHT")),
            Shot(clip=NIGHT / "11956219.mp4"),           # L29-31 S6
        ],
    ),

    # --- the reframe: it is a contrast, not a volume ----------------------
    Section(
        title="Your room got quieter",
        spoken_title="So start with what actually changed.",
        sentences=[
            ("Tinnitus is not heard on its own.",
             "It is heard against",
             "whatever else you can hear."),
            ("All day there is traffic outside,",
             "people talking,",
             "a fridge humming in the next room."),
            ("None of that is loud.",
             "All of it is covering part of the sound.",
             "Then you turn everything off."),
            ("A dark bedroom at eleven at night",
             "is the quietest place",
             "most people ever spend time in."),
            ("So nothing got louder.",
             "The thing it was competing with",
             "went away."),
        ],
        shots=[
            Shot(graphic="quote",
                 payload=("Your tinnitus did not get louder. "
                          "Your room got quieter.",
                          "what actually changed at bedtime")),
            Shot(clip=SOUND / "34645273.mp4"),           # L7 S2
            None,
            Shot(clip=NIGHT / "11956328.mp4", clip_at=4.0),
            Shot(clip=WAVES / "27980029.mp4"),           # L2-4 S2-6
        ],
    ),

    # --- the mechanism, as an A/B ----------------------------------------
    Section(
        title="What the day was doing for you",
        spoken_title="So what was the day actually doing for you?",
        sentences=[
            ("Look at the two rooms side by side",
             "and the whole thing stops being mysterious."),
            # One caption chunk per compare item, left column then right,
            # with no lead-in inside the beat's own span.
            ("Traffic and voices outside.",
             "Appliances running.",
             "A task in front of you.",
             "Silence.",
             "Nothing to do but listen.",
             "And a whole day of tiredness behind you."),
            ("Same ears.",
             "Same sound.",
             "Completely different experience of it."),
        ],
        shots=[
            Shot(clip=TIREDP / "6415592.mp4"),           # L18-19 S6
            Shot(graphic="compare",
                 payload=("Your day",
                          ["Traffic, voices, the street",
                           "Appliances and background hum",
                           "Attention already occupied"],
                          "Your bedroom at 11pm",
                          ["Almost no ambient sound",
                           "Nothing competing for attention",
                           "Tolerance at its lowest"])),
            Shot(clip=BEDW / "30285719.mp4"),            # L24 S10
        ],
    ),

    # --- the twist: the instinct is backwards ----------------------------
    Section(
        title="So why does chasing quiet backfire?",
        sentences=[
            ("Which means the obvious move",
             "is the wrong one."),
            ("If the sound is worse when it is quiet,",
             "the instinct is to make it quieter still.",
             "Earplugs. Thicker curtains.",
             "A room with nothing in it."),
            ("Every one of those",
             "removes more of the sound",
             "that was covering it."),
            # `flow=True`: the narration is delivering the verdicts itself,
            # so holding the marks back would put the picture behind the
            # voice. One caption chunk per row, in row order.
            ("Earplugs make it stand out more.",
             "A soundproofed bedroom does the same.",
             "Lying there waiting it out",
             "teaches your brain that bed is where you fight it.",
             "Low, steady sound in the room",
             "is the one that goes the other way."),
            ("So stop trying to sleep in silence.",
             "Silence is the problem,",
             "not the goal."),
        ],
        shots=[
            Shot(clip=TIREDM / "4588472.mp4"),
            None,
            Shot(clip=AWAKE / "8376628.mp4", clip_at=6.0),
            Shot(graphic="checklist",
                 payload=([("Earplugs at night", False),
                           ("Soundproofing the room", False),
                           ("Waiting for it to fade", False),
                           ("Low steady sound in the room", True)],
                          "WHAT QUIET ACTUALLY DOES",
                          True),                     # flow
                 picture=IMG / "anxiety-girl.jpg"),
            None,
        ],
        # The checklist needs room for its verdicts to land.
        gaps=[0.34, 0.34, 0.34, 0.34, 0.90],
    ),

    # --- what to put in the room -----------------------------------------
    Section(
        title="What to put in the room",
        spoken_title="So what do you actually put in the room?",
        sentences=[
            ("Not music with words in it.",
             "Something steady",
             "that your attention slides off."),
            # One chunk per grid card, in card order.
            ("White noise, if your tinnitus is a high ring.",
             "Brown noise, if it sits lower.",
             "Or rain, a fan, waves — if hiss irritates you."),
            ("And it goes in the room,",
             "on a speaker,",
             "not in your ears."),
            ("Earbuds worn for eight hours",
             "irritate the ear canal,",
             "and sealing the ear",
             "blocks the ambient sound you are adding on purpose."),
        ],
        shots=[
            Shot(clip=RAIN / "4458918.mp4"),             # L20-21 S16-23
            Shot(graphic="grid",
                 payload=([("White noise",
                            "Suits a high-pitched ring"),
                           ("Brown noise",
                            "Suits a lower, deeper tone"),
                           ("Rain, fan or waves",
                            "Gentler if hiss irritates you")],
                          "STEADY SOUND, NO WORDS")),
            # The line is "it goes in the room, on a speaker, not in your
            # ears", so the room is the subject. The second rain clip sat here
            # until `mia-calm` grew the slot past its 10s length.
            Shot(clip=LAMP / "10387906.mp4", clip_at=8.0),   # L36-46 S23-29
            None,
        ],
    ),

    # --- the setting everybody gets wrong ---------------------------------
    Section(
        title="The setting almost everybody gets wrong",
        spoken_title="And here is the setting almost everybody gets wrong.",
        sentences=[
            ("The instinct is to turn it up",
             "until the ringing disappears."),
            ("Do the opposite.",),
            ("Set it just below your tinnitus.",
             "Quiet enough",
             "that you can still faintly hear the ringing underneath."),
            ("Just below.",
             "That is the whole trick."),
            ("And if you are still awake",
             "after about twenty minutes —",
             "get up."),
            ("Read somewhere dim until you are sleepy,",
             "then go back.",
             "Lying there frustrated",
             "is the habit worth breaking."),
        ],
        shots=[
            Shot(clip=SOUND / "34645273.mp4", clip_at=4.0),
            None,
            Shot(clip=NIGHT / "11956219.mp4", clip_at=12.0),
            # **The only water shot in the video, and it carries a line.**
            # The first cut used this footage four times with nothing on it,
            # and unlabelled water under a script about bedrooms is wallpaper
            # — it illustrates nothing and the user called it out. One shot,
            # on the section's punch line, is what the footage is good for.
            Shot(clip=WATER / "11028763.mp4",            # L28-31 S6-7
                 payload=("", "Just below. Not on top.")),
            Shot(graphic="stat",
                 payload=("20", "MINUTES",
                          "Still awake after that? Get out of bed.")),
            Shot(clip=CLOCK / "35999376.mp4"),           # L34-35 S25-28
        ],
        # Buy the stat a beat — it is the line the section is built toward.
        gaps=[0.34, 0.60, 0.34, 0.90, 1.00, 0.34],
    ),

    # --- the procedure ----------------------------------------------------
    Section(
        title="Tonight, in order",
        spoken_title="So what does tonight actually look like?",
        sentences=[
            ("Four things, in this order.",),
            ("Put steady sound in the room, on a speaker.",
             "Set it just below the ringing.",
             "Out of bed if you are still awake after twenty minutes.",
             "And keep your wake-up time fixed, whatever happened."),
            ("That last one is the one people drop.",),
            ("Sleeping in after a bad night",
             "feels like mercy",
             "and reliably wrecks the following one."),
        ],
        shots=[
            Shot(clip=SITW / "6951594.mp4"),             # L45-49 S16-21
            Shot(graphic="steps",
                 payload=(["Sound in the room, on a speaker",
                           "Set it just below the ringing",
                           "Up after 20 minutes awake",
                           "Fixed wake time, every day"],
                          "TONIGHT")),
            Shot(clip=TIREDP / "6415592.mp4", clip_at=12.0),
            None,
        ],
    ),

    # --- when it is bigger than a bedtime routine -------------------------
    Section(
        title="When it is more than a bad night",
        spoken_title="And when is it more than a bad night?",
        sentences=[
            ("Sound in the room fixes the contrast.",
             "It does not fix everything."),
            ("If sleeplessness has become a nightly pattern,",
             "talking therapy for insomnia",
             "is the treatment with the strongest evidence behind it."),
            ("And if the tinnitus is new,",
             "or getting louder,",
             "or only in one ear,",
             "or comes with dizziness or hearing loss —"),
            ("that is a reason to see",
             "an audiologist or a sleep specialist.",
             "Not to panic.",
             "To get the cause named."),
        ],
        shots=[
            Shot(image=AWAKE_PHOTO, zoom=1.10, pan=(0.02, -0.01),
                 aspect=A, bias=0.45),
            Shot(graphic="quote",
                 payload=("Sound changes the room. "
                          "Therapy changes the pattern.",
                          "two different problems"),
                 picture=IMG / "therapy.jpg"),
            Shot(clip=TIREDW / "4588228.mp4", clip_at=9.0),
            Shot(graphic="stat",
                 payload=("4", "RED FLAGS",
                          "New · louder · one ear · with dizziness"),
                 picture=IMG / "audiologist.jpg"),
        ],
    ),

    # --- close: the echo --------------------------------------------------
    Section(
        title="Give the room something to say",
        spoken_title="So where does that leave tonight?",
        sentences=[
            ("You were never trying to sleep through a loud sound.",
             "You were trying to sleep",
             "in a room with nothing else in it."),
            ("So give the room something quiet to do.",
             "Just below the ringing.",
             "Not on top of it."),
            ("Your tinnitus did not get louder tonight.",
             "Your room got quieter.",
             "And a room is the easier one to change."),
            ("If that helped,",
             "subscribe for more videos like this one."),
        ],
        shots=[
            Shot(clip=NIGHT / "11956219.mp4", clip_at=5.0),
            Shot(clip=RAIN / "4458918.mp4", clip_at=4.0),
            Shot(clip=NIGHT / "11956328.mp4", clip_at=6.0),
            Shot(clip=WAVES / "27980029.mp4", clip_at=1.0),
        ],
        # 3.20 -> 2.30. The endcard sting runs its own 7s over the outro, so
        # the tail does not also need three seconds of silence after the last
        # line; `mia-calm` reads ~9% slower than the voice this was written
        # against and that put the cut over four minutes.
        gaps=[0.34, 0.34, 0.90, 2.30],
    ),
]

META = Meta(
    title="How to Sleep With Tinnitus: Why It Is Worse at Night",
    hook="Your tinnitus did not get louder at bedtime — your room got "
         "quieter. Here is what to put in the room, and the volume setting "
         "almost everybody gets wrong.",
    url=URL,
    summary="Why tinnitus feels worse the moment the lights go out, why "
            "chasing silence with earplugs and soundproofing makes it stand "
            "out more, which kind of steady sound suits which kind of "
            "tinnitus, why the sound belongs on a speaker rather than in "
            "your ears, and the counterintuitive volume rule — set it just "
            "below the ringing, not loud enough to bury it.",
    # Thirteen, matching the two long-form uploads already on the channel —
    # the first draft had eight, which is thin against the channel's own
    # convention. The first five become the hashtag line, so the search
    # phrase leads.
    tags=["tinnitus", "how to sleep with tinnitus", "tinnitus at night",
          "sound therapy", "white noise", "brown noise", "insomnia",
          "ringing in ears", "tinnitus help", "tinnitus and sleep",
          "cant sleep tinnitus", "tinnitus masking", "sleep hygiene"],
    cta=f"Full guide, the night-time routine and sources: {URL}",
    credits=["Additional footage: Pexels (Pexels licence, no attribution "
             "required).", "Music: generated for this channel.",
             "",
             "This video is general information, not medical advice. If your "
             "tinnitus is new, persistent, in one ear only, or comes with "
             "hearing loss or dizziness, see a doctor or audiologist."],
)


# The thumbnail's photograph is `AWAKE_PHOTO`, used full-frame in the video
# too — the user asked for one picture doing both jobs.
#
# **The scorer picked a frame with no subject in it, twice, before this.**
# `_layout` searches zoom x pan for space quiet enough to take type, and on a
# wide bedroom shot the quietest composition is the one that has cropped the
# sleeper out: the first two renders were a duvet and a dark wall, reading as
# bedding rather than as a person who cannot sleep. Both scored clear. The
# skill's "the scorer loses to the subject" note is exactly this, and the fix
# is not an override — it is a source whose face is too large to crop away.
# This one is a lit face filling a third of the frame with black beside it,
# so every candidate layout keeps him and the type still lands on empty.


def main() -> None:
    out = Path.home() / "Desktop/tinnitus-sleep-long.mp4"
    work = Path.home() / "Desktop/.tinnitus-sleep-work"
    made = render_long(
        SECTIONS, out, work, brand=TINNITUS, meta=META, voice=VOICE,
        music=MUSIC, callouts=None,
        endcard=ENDCARD, endcard_lead=7.0,
        # **The same headline and the same treatment as the Short from this
        # post.** They are published as a pair and should look like one; the
        # type is drawn by `thumb._headline` for both aspects so they cannot
        # drift. "Your room got quieter" tested as the answer to the title's
        # question; the user's call was to keep this one instead, closer to
        # the video's own reframe.
        thumb_headline="Stop sleeping in [silence]",
        thumb_image=THUMB_PHOTO,
        thumb_accent="red",
        thumb_side="left",
    )
    for k, v in made.items():
        print(f"{k}: {v}")


if __name__ == "__main__":
    main()
