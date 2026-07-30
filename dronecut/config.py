"""Every tunable number in Phase 1 lives here.

The tuning round after the first real run touches this file and nothing else.
Values marked GUESS have never been validated against footage.
"""

VIDEO_EXTS = {".mp4", ".mov", ".m4v", ".mkv", ".avi"}

# --- proxy ---------------------------------------------------------------
PROXY_WIDTH = 320
PROXY_FPS = 10
PROXY_DIRNAME = ".analysis_cache"
DB_NAME = "clip_index.sqlite"

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
MIN_TAIL_MARGIN = 0.1        # never run to the exact last frame

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

# Fade the picture to black under the closing music fade. Length follows
# MUSIC_FADE_SECONDS so the two land together.
FADE_TO_BLACK = True

# If the footage runs out before the track does, end the music under the last
# shot rather than letting it play over black.
MUSIC_FADE_SECONDS = 4.0

W_SLOT_LENGTH = 0.30         # how hard to push toward the preferred length

# Weight on matching clip motion energy to section musical energy. (GUESS)
W_ENERGY_MATCH = 1.0
