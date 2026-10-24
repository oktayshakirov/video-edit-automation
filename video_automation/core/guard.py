"""A render stops itself before it takes the Mac down with it.

On 2026-10-24 the MacBook kernel-panicked mid-render: two `render_shots` jobs
held 29 GB on a 16 GB machine, the compressor filled, swap grew until the disk
was nearly out of room, WindowServer could not get memory to draw with, and
the watchdog rebooted the machine. The renderer has been fixed
(`longform.clip.VideoShot` streams its frames), but nothing stopped a render
that went wrong — and the next memory hog may not be the renderer at all.

Two checks, both cheap enough to run every second of output:

* **Before the render: is there room for swap?** On macOS swap lives on the
  data volume, so free disk is the machine's last reserve of memory. Below
  `MIN_FREE_GB` the render refuses to start, with a message, instead of
  starting a job the machine cannot finish.

* **During the render: is the kernel in trouble?** `kern.memorystatus_vm_
  pressure_level` is the same signal Activity Monitor's pressure graph shows
  (1 normal, 2 warning, 4 critical). Critical aborts the render, and so does
  free disk falling under `FLOOR_GB` - that is swap eating the volume, which is
  exactly the slope the panic came down. Warning prints once and carries on.

An abort kills the encoder and raises `RenderGuardError`; the partial output is
left for inspection. A crashed render costs minutes, a panicked Mac costs
whatever else was open.
"""

from __future__ import annotations

import ctypes
import ctypes.util
import shutil
import subprocess
import sys
import time
from pathlib import Path

# Room the render needs to start: enough for its own output and temp files and
# for swap to grow into if something else on the machine spikes.
MIN_FREE_GB = 15.0
# Under this mid-render, swap is consuming the disk - stop while there is still
# room for the system to recover.
FLOOR_GB = 5.0

NORMAL, WARNING, CRITICAL = 1, 2, 4


class RenderGuardError(RuntimeError):
    pass


_libc = None


def pressure_level() -> int | None:
    """The kernel's memory-pressure level, or None where it cannot be read."""
    global _libc
    if sys.platform != "darwin":
        return None
    if _libc is None:
        _libc = ctypes.CDLL(ctypes.util.find_library("c"), use_errno=True)
    v = ctypes.c_int(0)
    size = ctypes.c_size_t(ctypes.sizeof(v))
    if _libc.sysctlbyname(b"kern.memorystatus_vm_pressure_level",
                          ctypes.byref(v), ctypes.byref(size), None, 0) != 0:
        return None
    return v.value


def free_gb(path: Path) -> float:
    """Free space on the volume holding `path`, in GB.

    Measured on the path itself rather than `/`, which on macOS is the sealed
    system volume and reports room the user does not have.
    """
    p = Path(path)
    while not p.exists() and p != p.parent:
        p = p.parent
    return shutil.disk_usage(p).free / 1e9


def preflight(out: Path, min_free_gb: float = MIN_FREE_GB) -> None:
    """Refuse to start a render the machine has no room to finish."""
    free = free_gb(out)
    if free < min_free_gb:
        raise RenderGuardError(
            f"only {free:.1f} GB free on the volume for {out} - a render needs "
            f"{min_free_gb:.0f} GB, because swap lives on that disk and a full "
            f"one is how the Mac panicked on 2026-10-24. Free space first "
            f"(the clean-storage skill), then render.")
    level = pressure_level()
    if level is not None and level >= CRITICAL:
        raise RenderGuardError(
            "memory pressure is already critical - close whatever is holding "
            "memory (another render, Blender, ACE-Step, Gradle) before starting.")


class Watch:
    """Called once per output frame; checks the machine every `every` frames.

    `stop` runs before an abort raises - the caller passes its encoder's
    `kill`, so ffmpeg does not sit on a half-written pipe after the error.
    """

    def __init__(self, out: Path, every: int = 30, floor_gb: float = FLOOR_GB,
                 stop=None):
        self.out, self.every, self.floor_gb = Path(out), max(1, every), floor_gb
        self.stop = stop
        self.frames = 0
        self.warned = False

    def _abort(self, msg: str) -> None:
        if self.stop is not None:
            self.stop()
        raise RenderGuardError(msg)

    def __call__(self) -> None:
        self.frames += 1
        if self.frames % self.every == 0:
            self.check(f"{self.frames} frames")

    def check(self, progress: str) -> None:
        """One look at the machine; `progress` says how far the render got."""
        level = pressure_level()
        if level is not None and level >= CRITICAL:
            self._abort(
                f"memory pressure went critical {progress} into "
                f"{self.out.name} - render stopped before the system ran out of "
                f"memory. Close other heavy jobs and render again.")
        free = free_gb(self.out)
        if free < self.floor_gb:
            self._abort(
                f"free disk fell to {free:.1f} GB {progress} into "
                f"{self.out.name} - swap is filling the volume, render stopped.")
        if level is not None and level >= WARNING and not self.warned:
            self.warned = True
            print(f"[guard] memory pressure is at warning while rendering "
                  f"{self.out.name}; it will stop if it goes critical.",
                  file=sys.stderr)


def run(cmd: list, out: Path, check: bool = True,
        capture_output: bool = False) -> subprocess.CompletedProcess:
    """`subprocess.run` for an ffmpeg job with no Python frame loop to watch.

    The cut-and-crop, HDR and ping-pong encodes hand the whole job to one
    ffmpeg call, so there is no per-frame hook - this preflights, then looks at
    the machine once a second while ffmpeg runs, and kills it on the same
    signals `Watch` aborts on. `communicate` with a timeout keeps draining the
    pipes between looks, so a captured stderr cannot fill and stall the job.
    """
    preflight(out)
    pipe = subprocess.PIPE if capture_output else None
    proc = subprocess.Popen(cmd, stdout=pipe, stderr=pipe)

    def stop():
        proc.kill()
        proc.communicate()

    watch = Watch(out, stop=stop)
    started = time.monotonic()
    while True:
        try:
            stdout, stderr = proc.communicate(timeout=1.0)
            break
        except subprocess.TimeoutExpired:
            watch.check(f"{time.monotonic() - started:.0f}s")
    if check and proc.returncode:
        raise subprocess.CalledProcessError(proc.returncode, cmd, stdout, stderr)
    return subprocess.CompletedProcess(cmd, proc.returncode, stdout, stderr)
