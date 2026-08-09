"""Every tunable number in Phase 1 lives here.

The tuning round after the first real run touches this file and nothing else.
Values marked GUESS have never been validated against footage.
"""

# Proxy and container constants are shared with the other projects; re-exported
# here so drone modules can keep importing everything from one config.
from ..core.config import (          # noqa: F401
    DB_NAME, PROXY_DIRNAME, PROXY_FPS, PROXY_WIDTH, VIDEO_EXTS,
)

# --- feature tracking ----------------------------------------------------
MAX_FEATURES = 300
FEATURE_QUALITY = 0.01
MIN_FEATURE_DIST = 8
REDETECT_BELOW = 60          # re-seed features when tracked count drops under this
MIN_TRACKED_FOR_FIT = 12     # below this, the affine fit is untrustworthy

# --- move classification (GUESS: all per-second, never validated) ---------
HOVER_PAN_MAX = 0.015        # frame-widths/sec below which nothing is moving
HOVER_ROT_MAX = 1.0          # deg/sec
HOVER_ZOOM_MAX = 0.01        # fractional zoom/sec

# Weights that put translation, rotation and zoom on a comparable scale, used
# both to pick the dominant move and to build motion_energy. (GUESS)
W_PAN = 1.0
W_ROT = 0.05
W_ZOOM = 2.0

# --- reporting -----------------------------------------------------------
LOW_CONFIDENCE = 0.6         # fraction of frames with a usable affine fit


# =========================================================================
# Phase 2 — music analysis
# =========================================================================

SR = 22050                   # analysis sample rate; plenty for beats and RMS
HOP = 512                    # ~23ms frames at SR

BEATS_PER_BAR = 4            # GUESS in general, safe for 4/4 produced music

# The beat grid is found by direct search over (period, phase) within this
# range, not taken from librosa's reported tempo. librosa returned 152.11 BPM
# for a 75.00 BPM track and the downstream least-squares fit made that look
# clean; the search scores each candidate by how much onset energy actually
# lands on it, so a wrong tempo loses by orders of magnitude instead of passing.
# Widen this only for genuinely fast or slow material — a wider range is more
# octave ambiguity, not more accuracy.
BPM_SEARCH_LO = 55.0
BPM_SEARCH_HI = 185.0

# Downbeat voting uses onset strength restricted below this, so the kick decides
# the phase rather than the snare (which sits on 2 and 4 and is louder broadband).
DOWNBEAT_FMAX = 200.0

# Target number of bars per structural section. Segment count is derived from
# track length so short tracks don't get chopped into meaningless pieces.
BARS_PER_SECTION = 8

# Snap section boundaries onto phrase lines. Slots restart at every boundary, so
# a boundary landing off-phrase throws every cut after it a bar out of step with
# the music and stays wrong for the rest of the track.
#
# Turning this on RE-LAYS THE SLOT GRID after the first moved boundary, which
# changes which clip lands in which slot from that point on. It is the correct
# setting musically, but it cannot be combined with holding an approved running
# order — the two are mutually exclusive.
SNAP_SECTIONS_TO_PHRASE = True


# =========================================================================
# Phase 3 — edit decisions
# =========================================================================

# Name of the event the timeline lands in inside Final Cut. A display name, so
# it takes spaces and capitals — unlike the Python module name, which cannot.
EVENT_NAME = "Claude Drone"

TIMELINE_FPS = 30            # overridden from the footage; all cuts snap to this

# Legal slot lengths in bars, longest first. The engine takes the longest one a
# clip can actually fill — the reverse of imposing a grid and hunting for footage.
LEGAL_SLOT_BARS = (8, 4, 2, 1)

# Section energy (0..1) -> preferred slot length in bars. (GUESS)
SLOT_BARS_BY_ENERGY = ((0.33, 4), (0.66, 2), (1.01, 1))

# Retiming is SPEED-UP ONLY. Slow motion is never used: nothing below 1.0.
# rate is source frames consumed per timeline frame, so 2.0 fits twice as much
# clip into the same slot. This is also how long selects earn their keep — a
# 45s take is no longer mostly waste.
ALLOW_SPEEDUP = True
SPEED_CHOICES = (1.0, 2.0)

# "If a clip is too long, do it 2x" — so 2x is gated on the clip actually being
# long, not on the engine wanting more coverage. Without this gate, coverage
# pressure alone speeds up half the video and the whole thing reads time-lapsed.
SPEEDUP_MIN_REMAINING = 12.0   # seconds of unused material required for 2x

# A speed-up reads as intent on an energetic section and as a mistake on a calm
# one, so it is penalised in inverse proportion to section energy.
PENALTY_SPEEDUP_WHEN_CALM = 0.55

HEAD_TRIM = 0.3              # seconds skipped at the head of a select (settle-in)

# Force a clip's play direction, overriding AUTO_REVERSE:
# {filename substring: True/False}. The automatic rule only knows which way the
# camera travelled, so it will happily reverse a shot containing traffic, water
# or shadows and send them backwards. That is a judgement from watching, which
# the index cannot make.
CLIP_REVERSE_OVERRIDE: dict[str, bool] = {}

# Extra seconds to ignore at the head of named clips, on top of HEAD_TRIM:
# {filename substring: seconds}. For when the opening of a select is weaker than
# the rest — overexposed, unsteady — which is a judgement the index cannot make.
# Slices are handed out sequentially, so skipping the head also shifts every
# later use of that clip one segment along.
CLIP_HEAD_SKIP: dict[str, float] = {}
MIN_TAIL_MARGIN = 0.1        # never run to the exact last frame

# Source ranges never to use, in seconds: {filename substring: [[from, to], ...]}.
# For a bad stretch in the middle of an otherwise good take — a gust, a rotation,
# a moment the framing goes wrong. CLIP_HEAD_SKIP only covers a weak opening;
# without this the only way to avoid a mid-clip fault is to drop the slot that
# happens to land on it, and because slices are handed out by an advancing
# cursor, the *next* use of that clip then lands on the same fault instead.
CLIP_SKIP_RANGES: dict[str, list[list[float]]] = {}

# Variety penalties, applied against the previously placed clip. (GUESS)
PENALTY_SAME_MOVE = 0.35
PENALTY_SAME_GROUP = 0.25
PENALTY_CLOSE_HUE = 0.15
HUE_CLOSE_DEG = 25.0

# Reuse. A clip may return after this many slots, and takes a later region.
REUSE_COOLDOWN_SLOTS = 4
PENALTY_REUSE = 0.40         # applied at zero gap, decaying to 0 across the window
REUSE_RECENCY_WINDOW = 12    # slots over which the reuse penalty decays
PENALTY_OVERUSE = 0.18       # spreads the library; at 0.05 one clip took 19% of the cut

# Musical phrases are 4 bars. Holding a longer shot on the phrase boundary and
# shorter ones inside it is what stops a section reading as metronomic.
PHRASE_BARS = 4
PHRASE_ACCENT_MULTIPLIER = 2  # slot length preference at a phrase boundary

# Hard ceiling on a single shot regardless of bar maths. At 95 BPM an 8-bar slot
# is 20 seconds, which is a lot of one drone shot in a four-minute video.
MAX_SHOT_SECONDS = 12.0

# A slow orbit or a steady lateral looks near-identical in any short window, so
# two 1-bar cuts from one read as the same shot played twice. Moves whose framing
# changes quickly (push_in, pull_back, vertical) do not have that problem.
# hover was in this list and is now out: it was my addition, never asked for,
# and it lengthened the cut away from the pacing that read best.
MIN_SLOT_BARS_BY_MOVE = {"orbit": 2, "lateral": 2}

# Ceiling on how many slots one clip may take. Raised now that speed-ups let a
# long take be consumed in a few large bites instead of many small ones.
MAX_USES_DEFAULT = 8
MAX_USES_BY_MOVE = {"orbit": 3}

# Pressure toward using the whole library rather than the head of every clip.
W_COVERAGE = 0.25             # favours clips with material left
W_BITE = 0.30                 # favours consuming more of a clip per cut

# What to do when every clip is spent and slots remain. Rewinding cursors fills
# the timeline by replaying footage already on screen, which reads as the edit
# repeating itself — the complaint it looks like, rather than the "we ran out"
# it actually is. Ending a few seconds short is the cheaper failure, so that is
# the default; the engine says which one it did either way.
REWIND_WHEN_EXHAUSTED = False

# Two clips that travel the same way read as the same shot. Reversing one buys
# variety for free. Only applied to moves where reversal just flips direction —
# reversing a push_in would turn it into a pull_back, which is a different shot.
AUTO_REVERSE = True
REVERSIBLE_MOVES = {"lateral", "vertical"}

# ESCALATE: the shot runs at ESCALATE_BODY_SPEED for most of its length, then
# accelerates over the last stretch to ESCALATE_TAIL_SPEED so it launches into
# the next clip. This replaced a ramp that started at 1.0x and accelerated
# throughout; that one looked wrong on this footage. Being already fast and
# escalating only at the end is the move.
ALLOW_RAMPS = True
ESCALATE_BODY_SPEED = 2.0      # 200% for the body of the shot
ESCALATE_TAIL_SECONDS = 1.0    # length of the launch, in timeline seconds
ESCALATE_TAIL_SPEED = 20.0     # 2000% at the very last frame
RAMP_POINTS = 9                # linear segments approximating the curve

# Sustained playback speed must be a whole multiple of real time.
#
# At 100% every source frame maps to one timeline frame and at 200% every
# second one does; both are exact. 160% needs 1.6 source frames per timeline
# frame, so the engine repeats and drops frames on an uneven 5-frame cycle and
# the shot visibly stutters. This is not a rendering setting that can be tuned
# away — it is the frame arithmetic, and it was confirmed on Coast 1, which
# read smooth at 100% and 200% and laggy at 160%.
#
# fit_escalate used to walk body speed down in 0.1 steps looking for the
# fastest profile the footage could fund, which is exactly how 160% and 150%
# got into the last cut. It now steps whole multiples only. A ramp's *tail*
# still sweeps continuously, which is fine: judder needs a sustained speed to
# be visible, and the tail is a one-second accelerating whip.
INTEGER_SPEEDS_ONLY = True

# Slot start bars that receive an escalate, set per project.
#
# Deliberately explicit rather than scored. When an escalate competed for slots
# on merit it won them from other clips and reshuffled the running order, which
# is not acceptable while the order is being approved by hand. As a positional
# upgrade it changes how the already-chosen clip plays and nothing else.
ESCALATE_AT_BARS: tuple[int, ...] = ()

# Force a specific clip into a specific slot: {start bar: filename substring}.
# Set per project. A pin overrides scoring, the reuse cooldown and the use cap —
# it is a direct instruction, not a preference. It still cannot invent footage,
# so a pin whose clip has no material left is reported rather than applied
# silently.
PIN_CLIPS: dict[int, str] = {}

# Slot length for a pin, in bars: {start bar: bars}. Without this the pinned
# clip's length is still chosen by scoring, which can differ from the length the
# clip it replaced happened to have — a 2-bar shot becomes a 1-bar one and the
# replacement does not cover the same span.
PIN_SLOT_BARS: dict[int, int] = {}

# --- location pin overlay --------------------------------------------------
# The animated map pin from assets/, keyed over the opening shot.
#
# Everything here except the timing is captured verbatim from a real Final Cut
# export (assets/fcpxml/location-pin-overlay.xml): the Green Screen Keyer's UID
# and its two base64 payloads are FCP-internal and cannot be authored from a
# specification. The red pin is source 9.833-14.867s of the pack — not
# guessable, since by hue it measures ~345 deg and classifies as pink.
LOCATION_PIN = False
LOCATION_PIN_START = 1.0       # seconds into the timeline
LOCATION_PIN_SECONDS = 5.03    # full length of the red pin segment

# Text beside the pin. Empty string = pin only. The Basic Title generator's uid
# and its three `param key` paths are equally FCP-internal and were captured the
# same way, from a real export — see assets/fcpxml/location-title-overlay.xml.
# The title rides the pin's window, so it needs no timing of its own.
LOCATION_TITLE_TEXT = ""

# Fade the picture to black under the closing music fade. Length follows
# MUSIC_FADE_SECONDS so the two land together.
FADE_TO_BLACK = True

# If the footage runs out before the track does, end the music under the last
# shot rather than letting it play over black.
MUSIC_FADE_SECONDS = 4.0

# --- looping the track -----------------------------------------------------
# When there is more footage than music, play the track a second time instead
# of ending the video early. The song hands off at MUSIC_LOOP_HANDOFF_BAR and
# re-enters at MUSIC_LOOP_RETURN_BAR, under a crossfade.
#
# Both are counted in bars and both must be phrase-aligned, so the bar grid
# continues unbroken and no cut after the splice moves off the beat. Choose them
# for matching arrangement energy: the seam is audible in proportion to how far
# the music jumps across it. A crossfade hides the level change, never a drop
# landing on an intro.
MUSIC_LOOP = False
MUSIC_LOOP_HANDOFF_BAR: int | None = None   # None = last phrase line of the song
MUSIC_LOOP_RETURN_BAR: int | None = None
MUSIC_LOOP_CROSSFADE_BARS = 2

W_SLOT_LENGTH = 0.30         # how hard to push toward the preferred length

# Weight on matching clip motion energy to section musical energy. (GUESS)
W_ENERGY_MATCH = 1.0
