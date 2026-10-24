"""The render guard refuses and aborts on the right signals, and only those.

What these cover is the 2026-10-24 panic's two slopes - memory pressure going
critical and swap eating the disk - without needing a machine in trouble to
see them. The pressure reading and the free disk are faked; nothing renders.
"""

import sys

import pytest

from video_automation.core import guard
from video_automation.core.guard import (CRITICAL, NORMAL, WARNING,
                                         RenderGuardError, Watch, preflight)


@pytest.fixture
def machine(monkeypatch):
    state = {"level": NORMAL, "free": 70.0}
    monkeypatch.setattr(guard, "pressure_level", lambda: state["level"])
    monkeypatch.setattr(guard, "free_gb", lambda path: state["free"])
    return state


def test_preflight_passes_with_room(machine, tmp_path):
    preflight(tmp_path / "out.mp4")


def test_preflight_refuses_a_full_disk(machine, tmp_path):
    machine["free"] = 9.0
    with pytest.raises(RenderGuardError, match="9.0 GB free"):
        preflight(tmp_path / "out.mp4")


def test_preflight_refuses_critical_pressure(machine, tmp_path):
    machine["level"] = CRITICAL
    with pytest.raises(RenderGuardError, match="critical"):
        preflight(tmp_path / "out.mp4")


def test_watch_only_checks_every_n_frames(machine, tmp_path):
    w = Watch(tmp_path / "out.mp4", every=30)
    machine["level"] = CRITICAL
    for _ in range(29):
        w()                         # frames 1-29 never look
    with pytest.raises(RenderGuardError, match="30 frames"):
        w()


@pytest.mark.parametrize("level,free", [(CRITICAL, 70.0), (NORMAL, 4.0)])
def test_watch_aborts_and_stops_the_encoder(machine, tmp_path, level, free):
    stopped = []
    w = Watch(tmp_path / "out.mp4", every=1, stop=lambda: stopped.append(1))
    w()
    machine["level"], machine["free"] = level, free
    with pytest.raises(RenderGuardError):
        w()
    assert stopped == [1]


def test_watch_warns_once_and_carries_on(machine, tmp_path, capsys):
    machine["level"] = WARNING
    w = Watch(tmp_path / "out.mp4", every=1)
    for _ in range(5):
        w()
    assert capsys.readouterr().err.count("[guard]") == 1


@pytest.mark.skipif(sys.platform != "darwin", reason="macOS sysctl")
def test_pressure_level_reads_the_kernel():
    assert guard.pressure_level() in (NORMAL, WARNING, CRITICAL)


def test_free_gb_walks_up_to_an_existing_dir(tmp_path):
    assert guard.free_gb(tmp_path / "not" / "made" / "yet.mp4") > 0


def test_run_returns_like_subprocess_run(machine, tmp_path):
    r = guard.run(["sh", "-c", "echo hi; echo err >&2"], tmp_path / "o.mp4",
                  capture_output=True)
    assert (r.returncode, r.stdout, r.stderr) == (0, b"hi\n", b"err\n")


def test_run_raises_on_failure(machine, tmp_path):
    import subprocess
    with pytest.raises(subprocess.CalledProcessError):
        guard.run(["sh", "-c", "exit 3"], tmp_path / "o.mp4")


def test_run_kills_a_job_when_pressure_goes_critical(machine, tmp_path,
                                                     monkeypatch):
    import time
    calls = {"n": 0}

    def level():                    # normal for the preflight, critical after
        calls["n"] += 1
        return NORMAL if calls["n"] == 1 else CRITICAL
    monkeypatch.setattr(guard, "pressure_level", level)
    t0 = time.monotonic()
    with pytest.raises(RenderGuardError, match="critical"):
        guard.run(["sleep", "30"], tmp_path / "o.mp4")
    assert time.monotonic() - t0 < 5
