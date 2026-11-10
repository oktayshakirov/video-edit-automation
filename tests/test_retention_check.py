"""`tools/retention_check.py` times a script's opening and flags the shapes
the curves punished: an early sentence 2, an opener that leaves the frame
bare, a crypto Short over its length. On scripts written into a temp folder.
"""

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO / "tools"))
spec = importlib.util.spec_from_file_location(
    "retention_check", REPO / "tools/retention_check.py")
rc = importlib.util.module_from_spec(spec)
sys.modules["retention_check"] = rc
spec.loader.exec_module(rc)

LONG_Q = "If you buy Tesla on a blockchain, do you really own Tesla?"
BODY = [("You own a token, and the share has someone else's name on it.",)] + \
       [("A custodian holds the real shares for everyone at once.",)] * 5 + \
       [("So find out whose name is on it.",)]


def write(tmp_path, channel, question, call="render(S, opener_holds=True)",
          body=BODY, gap=1.0):
    d = tmp_path / f"{channel}-short"
    d.mkdir(exist_ok=True)
    p = d / "t.py"
    p.write_text(
        f"SENTENCES = {[(question,)] + body!r}\n"
        f"GAPS = {[gap] + [0.6] * len(body)!r}\n"
        "def render(*a, **k): pass\n"
        "def Stamp(*a, **k): return None\n"
        "S = SENTENCES\n"
        f"def main():\n    {call}\n")
    return p


def test_the_timeline_is_words_over_rate_plus_gaps(tmp_path):
    ft = rc.features(write(tmp_path, "crypto", LONG_Q))
    assert ft["w1"] == 12
    assert abs(ft["s1_end"] - 12 / rc.RATE) < 1e-6
    assert abs(ft["s2_start"] - (12 / rc.RATE + 1.0)) < 1e-6


def test_a_full_question_and_a_held_opener_pass(tmp_path, capsys):
    p = write(tmp_path, "crypto", LONG_Q,
              call='render(S, opener=Stamp("A", "B", at_word="token"), opener_holds=True)')
    assert rc.check(p) == []


def test_an_early_sentence_2_is_flagged(tmp_path, capsys):
    flags = rc.check(write(tmp_path, "tinnitus", "Will it go away?", gap=0.5))
    assert any("sentence 2 starts" in f for f in flags)


def test_an_opener_without_the_hold_is_flagged(tmp_path, capsys):
    p = write(tmp_path, "crypto", LONG_Q,
              call='render(S, opener=Stamp("A", "B", at_word="token"))')
    assert any("opener_holds" in f for f in rc.check(p))


def test_a_crypto_short_over_its_length_is_flagged_and_tinnitus_is_not(tmp_path, capsys):
    long_body = BODY[:1] + BODY[1:2] * 14 + BODY[-1:]
    assert any("E17" in f for f in rc.check(write(tmp_path, "crypto", LONG_Q, body=long_body)))
    assert not any("E17" in f for f in rc.check(write(tmp_path, "tinnitus", LONG_Q, body=long_body)))


def test_half_gone_and_never():
    pts = [{"seconds": s, "watchPct": w} for s, w in ((0.5, 120), (5, 80), (9, 58), (40, 20))]
    assert rc.curve_stats(pts)["half"] == 9
    assert rc.curve_stats(pts[:2])["never"]
