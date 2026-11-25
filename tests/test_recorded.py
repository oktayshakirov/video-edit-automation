"""The recorded voice keeps the right take of every sentence.

No Whisper here: the transcript is written by hand, the way Whisper returns
it (digits for numbers, punctuation on the words), with the two things a
real read has - a false start, and a sentence read twice.
"""

import numpy as np

from video_automation.core.recorded import align, norm, number_words


def words(text: str, start: float = 0.0, step: float = 0.3):
    out, t = [], start
    for w in text.split():
        out.append({"w": " " + w, "s": round(t, 2), "e": round(t + step * 0.8, 2)})
        t += step
    return out


def test_numbers_read_the_same_either_way():
    assert number_words(587) == "five hundred eighty seven".split()
    assert norm("587 job postings") == norm("five hundred and eighty-seven job postings")
    assert norm("1,816 BTC") == norm("one thousand eight hundred sixteen BTC")
    assert norm("10%") == ["ten", "percent"]


def test_false_start_and_retake_are_cut():
    script = [norm("I let AI read 587 job postings in one week."),
              norm("Only four were worth applying to."),
              norm("The rest were fake, stale, or wanted ten years of experience."),
              norm("It is the pile.")]
    heard = words(
        "I let AI read 500 and... Sorry. "                       # 0-6: false start
        "I let AI read 587 job postings in one week. "           # 7-16
        "Only 4 were worth applying to. "                        # 17-22
        "The rest were fake, old, or asked for 10 years of experience. "  # 23-34: first read
        "Um, let me say that again. "                            # 35-40
        "The rest were fake, stale, or wanted 10 years of experience. "   # 41-51: kept
        "It is the pile.")
    takes = align(script, heard)
    assert [(t.first, t.last) for t in takes] == [(7, 16), (17, 22), (41, 51), (52, 55)]
    assert all(t.score == 1.0 for t in takes)


def test_a_missing_sentence_stops_the_build():
    import pytest
    script = [norm("Only four were worth applying to."),
              norm("This line was never read aloud at all.")]
    with pytest.raises(ValueError, match="never read aloud"):
        align(script, words("Only 4 were worth applying to."))


def test_the_read_aloud_script_says_what_the_build_looks_for():
    """`tools/oktai_script.py` prints spoken halves and the chapter titles."""
    import importlib.util
    from pathlib import Path
    from video_automation.crypto.shots import Shot
    from video_automation.longform import Section
    from video_automation.oktai import reading_order
    spec = importlib.util.spec_from_file_location(
        "oktai_script", Path(__file__).resolve().parents[1] / "tools/oktai_script.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    secs = [Section(title="Why nobody answers", sentences=[
        (("587 postings", "five hundred and eighty seven postings"), "in a week."),
        ("Four were real.",)], shots=[Shot(graphic="stat", payload=("587",)), None])]
    lines = [mod._spoken(s) for s in reading_order(sections=secs)]
    assert lines == ["Why nobody answers",
                     "five hundred and eighty seven postings in a week.",
                     "Four were real."]
    assert mod._face_marks(lines, [("in a week", 3.0)]) == {0, 1, 2}


def test_a_long_scripted_gap_is_silence_even_inside_one_take():
    """A sound example plays in a gap of 1s or more: Oktay's own short pause
    there would put the clip on his next line, so the gap is written."""
    import numpy as np
    from video_automation.core import recorded as rc
    words = [{"s": 0.0, "e": 0.4}, {"s": 0.5, "e": 0.9},     # sentence 1
             {"s": 1.1, "e": 1.5}, {"s": 1.6, "e": 2.0}]     # sentence 2, 0.2s later
    takes = [rc.Take(0, 0, 1, 1.0, {}, 0), rc.Take(1, 2, 3, 1.0, {}, 0)]
    audio = np.zeros(int(2.5 * rc.SR))
    _, joined = rc._bounds(takes, words, audio, [0.5, 0.5], max_pause=0.8)
    assert joined == [False, True]                 # a short gap: his own pause
    _, joined = rc._bounds(takes, words, audio, [6.0, 0.5], max_pause=0.8)
    assert joined == [False, False]                # a long one: room tone, 6s


# --- the first real recording (2026-11-22) -----------------------------------

def test_a_stumble_inside_a_sentence_keeps_the_second_try():
    """"AI tools love... AI tools love stock footage": the first copy goes."""
    from video_automation.core.recorded import restarts
    heard = words("The first giveaway is the picture. "
                  "AI tools love AirTools log stock footage, "
                  "and stock footage loves to say something.")
    script = [norm("The first giveaway is the picture."),
              norm("AI tools love stock footage, and stock footage loves to say something.")]
    cut = restarts([norm(w["w"]) for w in heard], heard, script)
    assert [heard[i]["w"].strip() for i in sorted(cut)] == ["AI", "tools", "love"]
    # In the take, the stumble between the two copies is cut out.
    takes = align(script, heard)
    gone = [heard[k]["w"].strip() for a, b in takes[1].cuts for k in range(a + 1, b)]
    assert gone == ["AirTools", "log"]


def test_a_stumble_mid_sentence_is_cut_and_both_halves_kept():
    """The second recording: "stock footage and it was love stock food and
    stock footage loves" - the clean first half, the stumble cut, the rest."""
    script = [norm("AI tools love stock footage, and stock footage loves to say something.")]
    heard = words("AI tools love stock footage and it was love stock food "
                  "and stock footage loves to say something.")
    tk = align(script, heard)[0]
    assert heard[tk.first]["w"].strip() == "AI"
    gone = [heard[k]["w"].strip() for a, b in tk.cuts for k in range(a + 1, b)]
    assert len(gone) == 6 and "it was love stock food" in " ".join(gone)  # one "and" kept


def test_a_restart_never_runs_over_a_full_stop():
    from video_automation.core.recorded import restarts
    heard = words("and a beat underneath. What we learned? "
                  "A beat feels alive because of rhythm.")
    assert not restarts([norm(w["w"]) for w in heard], heard, [])


def test_a_shifted_phrase_is_not_a_restart():
    """"the first seconds, then the edit" is not "the first ten seconds"."""
    from video_automation.core.recorded import restarts
    heard = words("The first seconds, then the edit and the first ten seconds of it.")
    assert not restarts([norm(w["w"]) for w in heard], heard, [])


def test_a_misheard_first_word_stays_in_the_take():
    """Whisper writes "Claude" as "Cloud", "Thanks" as "Short": the take
    must not start a word late and cut the name off."""
    script = [norm("Kokoro reads them."), norm("Claude Code writes the scripts."),
              norm("Thanks for watching, and if you enjoyed it, subscribe for more.")]
    heard = words("Kokoro reads them. Cloud Code writes the scripts. "
                  "Short. for watching and if you enjoyed it subscribe for more.")
    takes = align(script, heard)
    assert heard[takes[1].first]["w"].strip() == "Cloud"
    assert heard[takes[2].first]["w"].strip() == "Short."


def test_a_title_is_not_taken_from_inside_a_longer_sentence():
    """"The first seconds" is a chapter title; "the first ten seconds" a few
    words later is part of the next line, not a later read of the title."""
    script = [norm("The first seconds"), norm("Then the edit, and the first ten seconds of it.")]
    heard = words("The first seconds. Then the edit and the first ten seconds of it. "
                  "Then the edit and the first ten seconds of it.")
    takes = align(script, heard)
    assert (takes[0].first, takes[0].last) == (0, 2)
    assert takes[1].first == 13                    # the retake


def test_long_pauses_inside_a_sentence_are_shortened():
    import numpy as np
    from video_automation.core import recorded as rc
    sr = rc.SR
    tone = (0.3 * np.sin(np.arange(sr) * 2 * np.pi * 220 / sr)).astype(np.float32)
    quiet = np.random.default_rng(0).normal(0, 1e-4, 3 * sr).astype(np.float32)
    short = np.random.default_rng(1).normal(0, 1e-4, int(0.3 * sr)).astype(np.float32)
    audio = np.concatenate([quiet, tone, quiet, tone, short, tone, quiet])
    a, b = 3.0, 3.0 + 1 + 3 + 1 + 0.3 + 1
    parts = rc._tighten(audio, [(a, b)], longer=0.45, keep=0.28)[0]
    kept = sum(y - x for x, y in parts)
    assert len(parts) == 2                        # the 3 s pause cut, the 0.3 s kept
    assert abs(kept - (b - a - 3 + 0.28)) < 0.05


def test_whisper_gets_pieces_that_end_in_pauses():
    import numpy as np
    from video_automation.core import recorded as rc
    sr = 16000
    speech = np.random.default_rng(0).normal(0, 0.2, 7 * sr).astype(np.float32)
    gap = np.zeros(sr // 2, np.float32)
    audio = np.concatenate([speech, gap] * 10)          # 75 s, a pause every 7.5 s
    pieces = rc._pieces(audio, sr)
    assert pieces[0][0] == 0 and pieces[-1][1] == len(audio)
    for a, b in pieces[:-1]:
        assert (b - a) / sr <= rc.PIECE[1]
        assert np.abs(audio[b - 400:b + 400]).max() == 0      # cut in a pause


def test_whispers_split_thousands_still_match():
    assert norm("It's 10 ,000 lines long.") == norm("It's ten thousand lines long.")
    assert norm("At 150 words") == norm("At a hundred and fifty words")


def test_the_clean_up_follows_the_room():
    from video_automation.core.recorded import clean_chain
    assert "nf=-56" in clean_chain(-62.0)
    assert "acompressor" not in clean_chain(-62.0)        # "too close to the mic"
    assert "nf=-20" in clean_chain(-10.0)               # clamped
    # His pick (2026-11-24): the boom cut harder, a peak catcher 10.5 dB over
    # the speech - plosives, not words.
    c = clean_chain(-62.0, None, -34.5)
    assert c.count("highpass=f=100:poles=2") == 2 and "equalizer=f=200" in c
    assert "acompressor=threshold=0.06310" in c


def test_a_boomy_dull_voice_is_matched_toward_the_channel_voice():
    """His note on the first Short: too loud, doesn't fit, needs EQ. A voice
    heavy below 400 Hz and dull above 2.5 kHz is cut low and lifted high,
    never more than `EQ_MAX` a band."""
    import numpy as np
    from video_automation.core import recorded as rc
    sr = rc.SR
    rng = np.random.default_rng(0)
    noise = rng.normal(0, 0.1, sr * 4)
    spec = np.fft.rfft(noise)
    f = np.fft.rfftfreq(len(noise), 1 / sr)
    # The channel voice's own spectrum, then boomier and duller than it.
    target = np.interp(np.log(np.maximum(f, 1)), np.log(rc.LTASS_BANDS), rc.TARGET_LTASS)
    shape = 10 ** (target / 20) * np.where(f < 400, 3.0, np.where(f > 2500, 0.3, 1.0))
    voice = np.fft.irfft(spec * shape, len(noise)).astype(np.float32)
    g = rc.eq_gains(voice, sr)
    bands = np.array(rc.LTASS_BANDS)
    assert g[bands < 350].mean() < -1.5
    assert g[(bands > 3000) & (bands < 7000)].mean() > 1.5
    assert np.abs(g).max() <= rc.EQ_MAX + 1e-9
    assert rc.match_eq(voice, sr).startswith("firequalizer=gain_entry=")


def test_the_face_is_cut_on_video_time(tmp_path):
    """QuickTime's .mov starts its sound 0.24 s after its picture: the face
    is cut that much later than the voice's sample time, or the lips lead."""
    import subprocess
    from video_automation.core.facecam import stream_lead
    p = tmp_path / "lead.mov"
    subprocess.run(["ffmpeg", "-v", "error", "-y",
                    "-f", "lavfi", "-i", "color=c=gray:s=64x64:r=30:d=2",
                    "-f", "lavfi", "-i", "sine=f=440:d=2", "-shortest",
                    "-c:v", "libx264", "-c:a", "aac", str(p)], check=True)
    assert stream_lead(p) >= 0.0                       # read, not crashed
    p2 = tmp_path / "shifted.mov"
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(p), "-itsoffset", "0.24",
                    "-i", str(p), "-map", "0:v", "-map", "1:a", "-c", "copy", str(p2)],
                   check=True)
    assert abs(stream_lead(p2) - stream_lead(p) - 0.24) < 0.03


def test_a_word_said_in_two_goes_is_kept_whole():
    """A slow "FF... FFmpeg" came back as "FFM" + "FFMPAG": the cut began on
    "peg" until the fragment before it was taken in."""
    script = [norm("Python draws every graphic."), norm("FFmpeg cuts the video.")]
    heard = words("Python draws every graphic. FFM FFMPAG cuts the video.")
    takes = align(script, heard)
    assert heard[takes[1].first]["w"].strip() == "FFM"


def test_speech_is_sped_up_but_the_gaps_keep_their_length():
    """His note: "speed up my voice with about 1.25 or 1.5". The sound
    examples play in the gaps, so those stay as long as written."""
    import numpy as np
    from video_automation.core import recorded as rc
    sr = rc.SR
    tone = (0.3 * np.sin(np.arange(2 * sr) * 2 * np.pi * 180 / sr)).astype(np.float32)
    gap = np.zeros(sr, np.float32)
    voice = np.concatenate([tone, gap, tone])
    edl = [{"out": 0.0, "dur": 1.0, "src": 10.0}, {"out": 1.0, "dur": 1.0, "src": 12.0},
           {"out": 2.0, "dur": 1.0, "gap": True},
           {"out": 3.0, "dur": 2.0, "src": 20.0}]
    out, new = rc._speed_up(voice, edl, 1.25)
    assert abs(len(out) / sr - (4 / 1.25 + 1)) < 0.05
    gaps = [s for s in new if s.get("gap")]
    assert len(gaps) == 1 and abs(gaps[0]["dur"] - 1.0) < 1e-3
    assert all(abs(s["rate"] - 1.25) < 0.02 for s in new if not s.get("gap"))
    # A source second maps through the rate; the second segment starts 0.8 s in.
    assert abs(rc.src_to_out(new, 12.0) - 0.8) < 0.02
    assert abs(rc.src_to_out(new, 21.0) - (new[3]["out"] + 0.8)) < 0.02


def test_the_face_plays_at_the_voices_rate():
    from video_automation.core.facecam import _pieces
    segs = [{"out": 0.0, "dur": 0.8, "src": 10.0, "rate": 1.25},
            {"out": 0.8, "dur": 1.0, "gap": True},
            {"out": 1.8, "dur": 1.6, "src": 20.0, "rate": 1.25}]
    p = _pieces(segs, 0.4, 2.6, 0.2)
    assert p[0] == ("src", 10.0 + 0.4 * 1.25 + 0.2, 0.4, 1.25)
    assert p[1][0] == "still" and abs(p[1][2] - 1.0) < 1e-9
    assert p[2][0] == "src" and abs(p[2][1] - 20.2) < 1e-9 and abs(p[2][2] - 0.8) < 1e-9


def test_breaths_between_words_become_room_tone_and_words_stay():
    """His note: "the previous one had gaps between sentences where you could
    hear noises". A breath between two words goes; a word Whisper did not
    write down (as loud as speech, longer than a click) stays."""
    import numpy as np
    from video_automation.core import recorded as rc
    sr = rc.SR
    rng = np.random.default_rng(0)
    room = lambda s: rng.normal(0, 3e-4, int(s * sr)).astype(np.float32)
    word = lambda s: (0.2 * np.sin(np.arange(int(s * sr)) * 2 * np.pi * 150 / sr)).astype(np.float32)
    breath = lambda s: rng.normal(0, 3e-3, int(s * sr)).astype(np.float32)   # ~+20 dB
    audio = np.concatenate([room(2), word(0.5), room(0.2), breath(0.3), room(0.2),
                            word(0.5), room(0.3), word(0.4), room(0.3), word(0.5), room(2)])
    t = 2.0
    w1 = {"w": "one", "s": t, "e": t + 0.5}; t += 0.5 + 0.7
    w2 = {"w": "two", "s": t, "e": t + 0.5}; t += 0.5 + 0.3
    hidden = (t, t + 0.4); t += 0.4 + 0.3                     # said, not transcribed
    w3 = {"w": "three", "s": t, "e": t + 0.5}
    out = rc.clean_gaps(audio, [w1, w2, w3])
    b0, b1 = int((2.5 + 0.25) * sr), int((2.5 + 0.45) * sr)
    assert np.abs(out[b0:b1]).max() < np.abs(audio[b0:b1]).max() / 3     # breath gone
    h0, h1 = int((hidden[0] + 0.05) * sr), int((hidden[1] - 0.05) * sr)
    assert np.allclose(out[h0:h1], audio[h0:h1])                         # word kept
    s0, s1 = int(2.05 * sr), int(2.45 * sr)
    assert np.allclose(out[s0:s1], audio[s0:s1])                         # words untouched


def test_cut_ranges_split_a_sentences_pieces():
    from video_automation.core.recorded import _cut_out
    assert _cut_out([[(0.0, 5.0)]], [[(1.0, 2.0)]]) == [[(0.0, 1.0), (2.0, 5.0)]]
    assert _cut_out([[(0.0, 1.0), (3.0, 5.0)]], [[(0.5, 4.0)]]) == [[(0.0, 0.5), (4.0, 5.0)]]


def test_an_onset_search_with_nothing_quiet_stays_out_of_the_word_before():
    """No quiet frame in reach used to return the far end of the reach -
    inside the word before: "paragraph. And here, the whole paragraph" kept
    "...graph." in front of the retake (2026-11-23)."""
    import numpy as np
    from video_automation.core.recorded import SR, _edge
    t = np.arange(int(1.0 * SR)) / SR
    audio = (0.3 * np.sin(2 * np.pi * 220 * t)).astype(np.float32)
    dip = slice(int(0.62 * SR), int(0.64 * SR))         # the word boundary
    audio[dip] *= 0.2
    at = _edge(audio, 0.7, 0.0, quiet_db=-80.0, back=True, reach=0.3)
    assert 0.6 <= at <= 0.66, at                         # the dip, not 0.4


def test_a_single_extra_word_at_a_sentence_edge_is_heard(monkeypatch, tmp_path):
    """One word of the failed attempt before a retake - "stops *begin*, and
    one track" - is cut at a sentence's edge; one inside a sentence still
    is not (2026-11-23)."""
    import numpy as np
    from video_automation.core import recorded
    heard = words("underneath begin and one track every time")
    monkeypatch.setattr(recorded, "transcribe", lambda *a, **k: heard)
    script = norm("a beat underneath and one track every time")
    voice = np.zeros(recorded.SR, np.float32)
    edge = recorded._extra_words(voice, script[2:], tmp_path, {0, 1, len(script) - 2})
    assert [x["text"] for x in edge] == ["begin"] and edge[0]["prev"] is None
    assert recorded._extra_words(voice, script[2:], tmp_path, {0}) == []


def test_the_camera_box_leaves_with_its_sentence(tmp_path):
    """His note (2026-11-23): the box stayed while he read the next line,
    looking at the page."""
    from video_automation.core.facecam import cues
    srt = tmp_path / "x.srt"
    srt.write_text("1\n00:00:01,000 --> 00:00:02,000\nAnd this one is me.\n\n"
                   "2\n00:00:02,400 --> 00:00:06,000\nFor four months, I let AI\n\n"
                   "3\n00:00:06,000 --> 00:00:09,000\nmake almost ninety videos.\n")
    long = cues(srt, on=[("And this one is me", 6.0)], hook=None, last=None)
    assert long[0][1] > 5.0
    short = cues(srt, on=[("And this one is me", 6.0)], hook=None, last=None,
                 sentences=[(1.0, 2.0), (2.4, 9.0)])
    assert short == [(1.0, 2.25)]


def test_a_pin_names_a_sentence_and_its_seconds(tmp_path):
    """The editor's pick of a take (2026-11-23): a read broken off and said
    again whole came back spliced from both."""
    from video_automation.core.recorded import Recording
    r = Recording(tmp_path / "x.wav", pins={"AI tools love stock footage.": (157.4, 159.5)})
    assert norm(list(r.pins)[0]) == ["ai", "tools", "love", "stock", "footage"]


def test_a_quiet_final_s_is_kept_and_not_given_to_the_room():
    """The third take (2026-11-23): "minutes", "seconds", "graphics" lost
    their "s" - all hiss and little level, under the gap clean-up's line."""
    import numpy as np
    from scipy.signal import butter, sosfilt
    from video_automation.core import recorded as rc
    sr = rc.SR
    rng = np.random.default_rng(1)
    room = lambda s: rng.normal(0, 3e-4, int(s * sr)).astype(np.float32)
    vowel = lambda s: (0.2 * np.sin(np.arange(int(s * sr)) * 2 * np.pi * 180 / sr)).astype(np.float32)
    sos = butter(4, [4500, 9000], btype="band", fs=sr, output="sos")
    hiss = sosfilt(sos, rng.normal(0, 0.02, int(0.12 * sr))).astype(np.float32)  # ~+16 dB
    audio = np.concatenate([room(1.5), vowel(0.4), hiss, room(0.6), vowel(0.4), room(1.5)])
    w1 = {"w": "minutes.", "s": 1.5, "e": 1.9}             # Whisper ends before the "s"
    w2 = {"w": "the", "s": 1.9 + 0.12 + 0.6, "e": 1.9 + 0.12 + 1.0}
    out = rc.clean_gaps(audio, [w1, w2])
    s0, s1 = int(1.91 * sr), int(2.0 * sr)
    assert np.allclose(out[s0:s1], audio[s0:s1])            # the "s" stays


def test_a_short_is_cut_from_the_long_forms_lines():
    from video_automation.crypto.shots import Shot
    from video_automation.longform.plan import Section
    from video_automation.oktai import from_long
    secs = [Section(title="x", card=False,
                    sentences=[("One.",), ("Two, and more.",), ("Three.",)],
                    shots=[Shot(graphic="stat"), None, Shot(graphic="quote")],
                    gaps=[0.4, 1.5, 0.4])]
    sents, shots, gaps = from_long(secs, ["Two, and", "Three"],
                                   {"OWN": (("Mine.",), Shot(graphic="bars"), 0.5)})
    assert sents == [("Two, and more.",), ("Three.",)] and shots[0] is None
    assert gaps == [1.5, 0.4] and shots[1].graphic == "quote"


def test_a_window_can_be_the_take_and_its_pickups():
    """Lines recorded later are joined on the take's end (2026-11-23); the
    long form looks in its own part and in the pickups, not in the Short's."""
    from video_automation.core.recorded import _in_window
    w = [(0.0, 492.1), (560.0, 1e9)]
    assert _in_window(w, 10) and _in_window(w, 600) and not _in_window(w, 520)
    assert _in_window((0.0, 5.0), 3) and not _in_window((0.0, 5.0), 6)
    assert _in_window(None, 999)


def test_a_pickup_read_at_the_end_wins_out_of_order():
    """Lines read again after the take, joined on its end (2026-11-24): the
    re-read is used wherever its line sits, and the rest stay in order."""
    take = words("one two three four. five six seven eight. nine ten eleven twelve.")
    pick = words("five six seven eight.", start=20.0)
    script = [norm("one two three four"), norm("five six seven eight"),
              norm("nine ten eleven twelve")]
    takes = align(script, take + pick, free_from=19.0)
    allw = take + pick
    assert allw[takes[1].first]["s"] >= 20.0          # the pickup
    assert allw[takes[0].first]["s"] < 1 and allw[takes[2].first]["s"] < 5


def test_a_word_edge_snaps_to_its_source_neighbour_not_a_pickup():
    """A word just before its piece, after a gap, is not placed by a pickup
    piece that plays earlier in the output (2026-11-24: a caption after a
    sound example started 8 s early)."""
    from video_automation.core.recorded import src_to_out
    edl = [{"out": 0.0, "dur": 3.0, "src": 600.0},      # a pickup, first out
           {"out": 3.0, "dur": 2.0, "src": 100.0},
           {"out": 5.0, "dur": 7.0, "gap": True},
           {"out": 12.0, "dur": 2.0, "src": 105.0}]
    assert src_to_out(edl, 104.98, snap=True) is None   # in the scripted gap
    edl[2:] = [{"out": 5.0, "dur": 2.0, "src": 103.0}]  # a cut inside one take
    assert src_to_out(edl, 102.5, snap=True) == 5.0


def _stop_ending(sr=48000):
    """Room hiss, a vowel, 0.1 s of closure, a 0.08 s release, room again."""
    from scipy.signal import butter, sosfilt
    rng = np.random.default_rng(3)
    a = (rng.standard_normal(int(3.0 * sr)) * 2e-4).astype(np.float32)
    t = np.arange(int(0.3 * sr)) / sr
    n = len(t)
    a[int(0.5 * sr):int(0.5 * sr) + n] += (0.2 * np.sin(2 * np.pi * 180 * t)).astype(np.float32)
    burst = sosfilt(butter(4, [4000, 9000], btype="band", fs=sr, output="sos"),
                    rng.standard_normal(int(0.08 * sr))) * 0.02
    a[int(0.9 * sr):int(0.9 * sr) + len(burst)] += burst.astype(np.float32)
    a[int(2.0 * sr):int(2.0 * sr) + n] += (0.2 * np.sin(2 * np.pi * 200 * t)).astype(np.float32)
    return a, sr


def _band_db(a, sr, t0, t1):
    from scipy.signal import butter, sosfilt
    hf = sosfilt(butter(4, [3500, 11000], btype="band", fs=sr, output="sos"),
                 a.astype(np.float64))[int(t0 * sr):int(t1 * sr)]
    return 10 * np.log10(float((hf ** 2).mean()) + 1e-12)


def test_the_gap_clean_up_keeps_a_final_stops_release():
    """ "code" lost its "d" to room tone and was heard as "Colt" (2026-11-24):
    the closure's silence is not the end of the word."""
    from video_automation.core.recorded import clean_gaps
    a, sr = _stop_ending()
    words = [{"w": "code", "s": 0.5, "e": 0.8}, {"w": "next", "s": 2.0, "e": 2.3}]
    out = clean_gaps(a, words, sr=sr)
    assert _band_db(out, sr, 0.9, 0.98) > _band_db(a, sr, 0.9, 0.98) - 3


def test_the_end_edge_reaches_past_the_closure_to_the_release():
    from video_automation.core.recorded import _release
    a, sr = _stop_ending()
    quiet = 10 * np.log10(float((a[int(1.2 * sr):int(1.9 * sr)] ** 2).mean())) + 15
    assert _release(a, 0.82, 1.9, quiet, sr=sr) >= 0.98
    # Ending on a vowel, nothing follows: the end stays.
    b, _ = _stop_ending()
    k = int(0.15 * sr)
    b[int(0.85 * sr):int(0.85 * sr) + k] = a[int(1.3 * sr):int(1.3 * sr) + k]
    assert _release(b, 0.82, 1.9, quiet, sr=sr) == 0.82


def test_the_gap_clean_up_still_removes_a_breath_after_a_word():
    """The bridge to a release stops short of a breath: 0.4 s of hiss is
    room tone, as before (2026-11-22: "noises in the gaps")."""
    from scipy.signal import butter, sosfilt
    from video_automation.core.recorded import clean_gaps
    a, sr = _stop_ending()
    rng = np.random.default_rng(5)
    breath = sosfilt(butter(4, [3000, 9000], btype="band", fs=sr, output="sos"),
                     rng.standard_normal(int(0.4 * sr))) * 0.01
    a[int(1.05 * sr):int(1.05 * sr) + len(breath)] += breath.astype(np.float32)
    words = [{"w": "code", "s": 0.5, "e": 0.8}, {"w": "next", "s": 2.0, "e": 2.3}]
    out = clean_gaps(a, words, sr=sr)
    assert _band_db(out, sr, 1.15, 1.4) < _band_db(a, sr, 1.15, 1.4) - 15


def test_the_report_flags_a_word_that_hides_a_stumble(tmp_path, capsys):
    """A 1.5 s "what" was "Here is", a throat-clear and the line again
    (2026-11-24): the report says to listen, unless the line is pinned."""
    from video_automation.core import recorded as r
    ws = words("here is what i learned.")
    ws[2]["e"] = ws[2]["s"] + 1.5
    toks = norm("here is what i learned")
    takes = align([toks], ws)
    rec = r.Recording(audio=tmp_path / "take.mov")
    rec.pins = {}
    r._write_sidecars(rec, [("Here is what I learned.",)], [toks], takes, ws,
                      [], [[0.0, 3.0]])
    assert "stumble may hide" in rec.report.read_text()
    rec.pins = {"Here is what I learned.": (0.0, 3.0)}
    r._write_sidecars(rec, [("Here is what I learned.",)], [toks], takes, ws,
                      [], [[0.0, 3.0]])
    assert "stumble may hide" not in rec.report.read_text()


def test_a_short_cut_from_the_long_form_takes_each_lines_best_read():
    """`free_from=0`: a line read later in the take is not swapped for a
    similar one read earlier to keep script order (2026-11-24: "I know,
    because I made almost ninety of them" played as "I know this, because I
    made a lot of it")."""
    take = words("i know this because i made a lot of it. "
                 "one two three four. five six seven eight. "
                 "i know because i made almost ninety of them.")
    script = [norm("i know because i made almost ninety of them"),
              norm("five six seven eight")]
    ordered = align(script, take)
    free = align(script, take, free_from=0.0)
    assert take[ordered[0].first]["s"] < take[ordered[1].first]["s"]
    assert take[free[0].first]["s"] > take[free[1].first]["s"]     # the 1.00 read
    assert free[0].score == 1.0


def test_pickups_are_shaped_and_levelled_to_the_take():
    """The pickups were read a day later in another room (2026-11-24): their
    long-term spectrum and level move to the take's before the chain."""
    from scipy.signal import butter, sosfilt
    from video_automation.core.recorded import SR, ltass, match_pickups
    rng = np.random.default_rng(1)

    def speechy(n):
        x = rng.normal(0, 1, n)
        env = (np.sin(np.arange(n) / SR * 2 * np.pi * 2.5) > -0.2).astype(float)
        return x * env

    take = speechy(SR * 20) * 0.05
    pick = speechy(SR * 20) * 0.05
    lows = sosfilt(butter(2, 400, "low", fs=SR, output="sos"), pick)
    mids = sosfilt(butter(2, [1200, 3000], "band", fs=SR, output="sos"), pick)
    pick = (pick + 1.5 * lows - 0.6 * mids) * 0.5        # boomier, duller, quieter
    audio = np.concatenate([take, pick]).astype(np.float32)
    out = match_pickups(audio, 20.0)
    k = SR * 20
    before = np.abs(ltass(audio[k:]) - ltass(audio[:k])).mean()
    after = np.abs(ltass(out[k:]) - ltass(out[:k])).mean()
    assert after < before * 0.5
    assert np.allclose(out[:k], audio[:k])                    # the take untouched
    rms = lambda x: np.sqrt(np.mean(x ** 2))
    assert abs(20 * np.log10(rms(out[k:]) / rms(out[:k]))) < 1.0


def test_lines_read_in_one_breath_split_after_the_s():
    """"...stock clips, and the same template" (2026-11-24): Whisper started
    "and" inside the "s"; the split goes in the quiet after it."""
    from video_automation.core.recorded import SR, _split
    rng = np.random.default_rng(3)
    t = np.arange(int(0.6 * SR)) / SR
    x = np.zeros_like(t)
    x[t < 0.20] = 0.3 * np.sin(2 * np.pi * 180 * t[t < 0.20])          # "clip-"
    s = (t >= 0.20) & (t < 0.36)
    x[s] = 0.05 * rng.normal(0, 1, s.sum())                               # "-s"
    v = t >= 0.46
    x[v] = 0.3 * np.sin(2 * np.pi * 160 * t[v])                           # "and"
    x += 1e-4 * rng.normal(0, 1, len(x))
    cut = _split(x, 0.20, 0.55)                 # Whisper's boundary was 0.30
    assert 0.36 <= cut <= 0.46


def test_dereverb_shortens_a_tail_and_keeps_the_word():
    from video_automation.core.recorded import SR, dereverb
    rng = np.random.default_rng(4)
    t = np.arange(int(1.0 * SR)) / SR
    word = np.where(t < 0.3, np.sin(2 * np.pi * 220 * t) * 0.3, 0.0)
    ir = rng.normal(0, 1, int(0.5 * SR)) * np.exp(-6.9 * np.arange(int(0.5 * SR)) / SR / 0.5)
    ir[0] = 30.0
    wet = np.convolve(word, ir)[:len(t)]
    wet /= np.abs(wet).max()
    dry = dereverb(wet.astype(np.float32), t60=0.5)
    def db(x, a, b):
        return 10 * np.log10(np.mean(x[int(a * SR):int(b * SR)] ** 2) + 1e-12)
    tail_in, tail_out = db(wet, 0.40, 0.55) - db(wet, 0.1, 0.25), db(dry, 0.40, 0.55) - db(dry, 0.1, 0.25)
    assert tail_out < tail_in - 4
