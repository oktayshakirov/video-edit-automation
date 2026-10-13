"""Datamosh transitions: the second shot's motion smeared over the first.

Not the `glitch` mode in `transitions.py`, which is a drawn RGB-split cut. This
breaks the codec itself, which is the TikTok "reality glitching" look.

## Why it works

Compressed video stores a full picture only at keyframes. Every frame between
is motion vectors plus a residual, applied to the frame before. Drop the second
shot's keyframe and the decoder never gets its picture: it keeps pushing the
first shot's last frame around with the second shot's motion. Repeat one of
those P-frames (a *bloom*) and its motion re-applies, so the smear grows.

MPEG-4 Part 2 is the codec, with no B-frames and one keyframe per shot. It is
where the effect was found, its raw stream splits on one start code
(`00 00 01 B6`), and its 16px blocks are the look.

## The two halves, and why they are built differently

**In: the mosh.** `mosh()` splices shot A's tail with shot B's P-frames.

**Drone motion is usually too slow per frame.** At 1x a slow orbit or a
rotation barely moves A and it reads as a freeze with streaks. Feed `mosh()`
a sped-up copy of B (`_segment(speed=...)`; 3-4x) and heal into B at 1x.

**The motion source has to have parallax.** A takes B's *shapes* because B's
motion field has edges where B's objects are: near towers moving against the
sky. A locked-off shot (a hyperlapse) gives near-zero vectors and the mosh
reads as a crossfade. `push_zoom` (a synthetic push-in) has motion but no
edges: A only zooms, which the user called "unrelated" - it is kept as a
fallback, not a fix. When the incoming shot is static, mosh into a shot that
moves (an orbit) instead, or borrow a moving shot's vectors for `mosh(b=...)`.

**Out: the heal.** `heal()` hands back to clean B block by block while the
mosh keeps moving underneath. Each block clears crisply in a few frames, and
*when* it clears follows a long tail: half go in the first quarter of the
~2.5s window, the rest drop out one by one. `motion_ramp()` slows the mosh
from 4x to 1x across it, so the leftovers drift to a stop. `cut()` is the
whole signed-off cut. Rejected exits, in order: a 4-frame snap ("it just
disappears"); a 0.8s linear block heal ("stopping too quick"); a mirrored
unwind, B scattered by A's motion and played backwards ("further away from the
effect"); and a soft fade of every block at once, which reads as a crossfade.

## Bit depth

The codec is 8-bit. Sources are taken down to 8 bits with **no colour
conversion**, so an HLG segment keeps its HLG code values and only that window
loses two bits. Everything else in and out of here is `yuv420p10le`. Tag the
result with whatever the segment was: the caller's `out_args`.
"""

from __future__ import annotations

import subprocess
from pathlib import Path

import numpy as np

VOP = b"\x00\x00\x01\xb6"


def _run(cmd: list[str]) -> None:
    subprocess.run(cmd, check=True, capture_output=True)


def _m4v(src: Path, dst: Path, vf: str, frames: int | None, q: int) -> None:
    """Encode to a raw MPEG-4 stream: no B-frames, a single keyframe."""
    limit = ["-frames:v", str(frames)] if frames else []
    _run(["ffmpeg", "-v", "error", "-y", "-i", str(src), *limit, "-vf",
          f"{vf},format=yuv420p", "-an", "-c:v", "mpeg4", "-q:v", str(q),
          "-bf", "0", "-g", "99999", "-sc_threshold", "1000000000",
          "-f", "m4v", str(dst)])


def _vops(data: bytes) -> tuple[bytes, list[bytes]]:
    """Split a raw MPEG-4 stream into its header and its VOPs."""
    idx, i = [], 0
    while (i := data.find(VOP, i)) != -1:
        idx.append(i)
        i += 4
    return data[:idx[0]], [data[s:e] for s, e in zip(idx, idx[1:] + [len(data)])]


def _kind(vop: bytes) -> str:
    return "IPBS"[vop[4] >> 6]


def mosh(a: Path, b: Path, dst: Path, *, frames: int, fps: int,
         size: tuple[int, int], a_tail: int = 8, bloom_at: int = 6,
         bloom_n: int = 0, push_zoom: float = 1.0,
         push_centre: tuple[float, float] = (0.5, 0.5), q: int = 3) -> Path:
    """`frames` frames of B's motion over A's last frame, lossless 10-bit.

    `a` is the whole outgoing segment. `b` supplies the motion and is only
    read for its P-frames, so it can be a different shot from the one `heal()`
    resolves into: a shot with parallax, whose motion field has edges where its
    buildings are, is what bends A into B's shapes. `a_tail` frames of A prime the decoder so its state is A's last
    picture. `push_zoom` > 1 swaps B's own motion for a push-in, for footage
    that barely moves.
    """
    work = dst.parent
    n_a = int(subprocess.run(
        ["ffprobe", "-v", "error", "-count_frames", "-select_streams", "v:0",
         "-show_entries", "stream=nb_read_frames", "-of", "csv=p=0", str(a)],
        check=True, capture_output=True, text=True).stdout.strip().rstrip(","))
    _m4v(a, work / "mosh-a.m4v",
         f"select='gte(n,{n_a - a_tail})',setpts=N/{fps}/TB", None, q)

    span = frames - bloom_n             # P-frames B has to supply
    w, h = size
    cx, cy = push_centre
    vf = (f"zoompan=z='pow({push_zoom},on/{span})':x='(iw-iw/zoom)*{cx}':"
          f"y='(ih-ih/zoom)*{cy}':d=1:s={w}x{h}:fps={fps}"
          if push_zoom != 1.0 else "null")
    _m4v(b, work / "mosh-b.m4v", vf, span + 1, q)

    head, fa = _vops((work / "mosh-a.m4v").read_bytes())
    _, fb = _vops((work / "mosh-b.m4v").read_bytes())
    assert _kind(fb[0]) == "I" and {_kind(f) for f in fb[1:]} == {"P"}, \
        "B must be one keyframe and P-frames only"
    p = fb[1:]                          # B's keyframe is gone: that is the mosh
    p = p[:bloom_at] + [p[bloom_at]] * bloom_n + p[bloom_at:]
    raw = work / "mosh.m4v"
    raw.write_bytes(head + b"".join(fa) + b"".join(p))

    _run(["ffmpeg", "-v", "error", "-y", "-r", str(fps), "-i", str(raw),
          "-vf", f"select='gte(n,{a_tail})',setpts=N/{fps}/TB,format=yuv420p10le",
          "-frames:v", str(frames), "-c:v", "ffv1", str(dst)])
    return dst


def _frames(src: Path, size: tuple[int, int]):
    """Yield (Y, U, V) uint16 planes from any video, as yuv420p10le."""
    w, h = size
    n = w * h * 3 // 2
    proc = subprocess.Popen(
        ["ffmpeg", "-v", "error", "-i", str(src), "-f", "rawvideo",
         "-pix_fmt", "yuv420p10le", "-"], stdout=subprocess.PIPE)
    while len(buf := proc.stdout.read(n * 2)) == n * 2:
        a = np.frombuffer(buf, "<u2")
        yield (a[:w * h].reshape(h, w),
               a[w * h:w * h * 5 // 4].reshape(h // 2, w // 2),
               a[w * h * 5 // 4:].reshape(h // 2, w // 2))
    proc.stdout.close()
    proc.wait()


def _thresholds(size: tuple[int, int], block: int, centre: tuple[float, float],
                radial: float, seed: int) -> np.ndarray:
    """When each block heals, 0..1: distance from `centre` mixed with noise."""
    w, h = size
    by, bx = np.mgrid[0:-(-h // block), 0:-(-w // block)]   # ceil: 1080 is not /16
    cy, cx = centre[1] * h / block, centre[0] * w / block
    d = np.hypot((bx + 0.5 - cx) / (w / block), (by + 0.5 - cy) / (h / block))
    d /= d.max()
    rng = np.random.default_rng(seed)
    t = radial * d + (1 - radial) * rng.random(d.shape)
    return (t - t.min()) / (t.max() - t.min())


def _luma_order(y: np.ndarray, block: int, seed: int,
                noise: float = 0.25) -> np.ndarray:
    """When each block heals, 0..1, from B's own picture: darkest first.

    Against a sky, B's structure is its dark mass, so the buildings resolve
    out of the mosh before the sky does and the exit reads as B forming
    rather than a wipe. A little noise keeps it from looking like a luma key.
    """
    h, w = y.shape
    gh, gw = -(-h // block), -(-w // block)
    pad = np.pad(y.astype(float), ((0, gh * block - h), (0, gw * block - w)),
                 mode="edge")
    m = pad.reshape(gh, block, gw, block).mean(axis=(1, 3))
    m = (m - m.min()) / max(m.max() - m.min(), 1e-6)
    rng = np.random.default_rng(seed)
    t = (1 - noise) * m + noise * rng.random(m.shape)
    return (t - t.min()) / (t.max() - t.min())


def heal(moshed: Path, mosh_frames: int, clean: Path, dst: Path, *,
         frames: int, heal_frames: int, size: tuple[int, int], fps: int,
         out_args: list[str], block: int = 16, fade: int = 8,
         tail: float = 2.0, noise: float = 0.5,
         centre: tuple[float, float] = (0.5, 0.5), radial: float = 0.6,
         seed: int = 7, order: str = "luma", vf: str = "null") -> Path:
    """The incoming segment, `frames` long: mosh, heal into clean, then clean.

    `moshed` is `mosh()`'s output, `mosh_frames` long. Over its last
    `heal_frames` each block clears to clean B, in `order`: `luma` heals B's dark structure first (the towers come out as
    silhouettes, then the sky), `radial` from `centre` outward. After the mosh
    it is `clean` as it is.

    **The glitch leaves as pixels, not as a fade.** Each block stays crisp and
    clears in `fade` frames; *when* it clears follows a long tail, rank**`tail`
    across the window. With `tail=2` half the blocks are gone in the first
    quarter, so the viewer is on the second video quickly, and scattered
    glitch blocks keep dropping out one by one for the rest of it. Two
    rejected versions: every block fading over a 24-frame window ("stopping
    too quick"), and a soft ease-out where every block fades partway at once,
    which washes the glitch out like a crossfade.
    `vf` runs on the result before it is encoded with `out_args`.
    """
    w, h = size
    t = _thresholds(size, block, centre, radial, seed) if order == "radial" \
        else None
    up_y, up_c = np.ones((block, block)), np.ones((block // 2, block // 2))
    enc = subprocess.Popen(
        ["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt",
         "yuv420p10le", "-s", f"{w}x{h}", "-r", str(fps), "-i", "-",
         "-vf", vf, "-frames:v", str(frames), *out_args, str(dst)],
        stdin=subprocess.PIPE)

    start = None
    moshes = _frames(moshed, size)
    for i, c in enumerate(_frames(clean, size)):
        if i >= frames:
            break
        out = c
        if i < mosh_frames:
            m = next(moshes)
            k = (i - (mosh_frames - heal_frames) + 1) / heal_frames
            if k <= 0:
                out = m
            else:
                if start is None:
                    if t is None:
                        t = _luma_order(c[0], block, seed, noise)
                    rank = t.ravel().argsort().argsort().reshape(t.shape)
                    start = (rank / rank.size) ** tail * (heal_frames - fade)
                a = np.clip((k * heal_frames - start) / fade, 0, 1)
                a = a * a * (3 - 2 * a)
                al = (np.kron(a, up_y)[:h, :w], np.kron(a, up_c)[:h // 2, :w // 2])
                out = tuple((mp * (1 - x) + cp * x).astype("<u2")
                            for mp, cp, x in zip(m, c, (al[0], al[1], al[1])))
        enc.stdin.write(b"".join(np.ascontiguousarray(p).tobytes() for p in out))
    enc.stdin.close()
    if enc.wait():
        raise RuntimeError(f"encode failed: {dst}")
    return dst


def _segment(src: Path, dst: Path, start: float, dur: float, x: float,
             size: tuple[int, int], fps: int, speed: float = 1.0) -> Path:
    """A vertical SDR segment, lossless 10-bit: crop at `x` (0..1).

    `dur` is output seconds; `speed` > 1 plays the source faster, which is how
    a slow drone move is turned into a usable mosh motion source.
    """
    w, h = size
    _run(["ffmpeg", "-v", "error", "-y", "-ss", str(start),
          "-t", str(dur * speed), "-i", str(src), "-vf",
          f"crop=ih*{w}/{h}:ih:(iw-ow)*{x}:0,scale={w}:{h}:flags=lanczos,"
          f"setpts=(PTS-STARTPTS)/{speed},fps={fps},setsar=1,"
          "format=yuv420p10le", "-an", "-c:v", "ffv1", str(dst)])
    return dst


def motion_ramp(src: Path, dst: Path, start: float, x: float,
                size: tuple[int, int], fps: int, speeds: list[float]) -> Path:
    """A motion source whose speed changes frame by frame, lossless 10-bit.

    `speeds[j]` is how many source frames frame j advances. Ramping from 4x
    down to 1x across the heal makes the leftover glitch pixels drift to a
    stop as they fade, instead of thrashing at full speed until they vanish.
    """
    idx = np.round(np.concatenate([[0], np.cumsum(speeds)])).astype(int)
    span = (idx[-1] + 2) / fps
    raw = _segment(src, dst.with_name(f"{dst.stem}-1x.mkv"), start, span, x,
                   size, fps)
    w, h = size
    enc = subprocess.Popen(
        ["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt",
         "yuv420p10le", "-s", f"{w}x{h}", "-r", str(fps), "-i", "-",
         "-c:v", "ffv1", str(dst)], stdin=subprocess.PIPE)
    want, j = list(idx), 0
    for i, f in enumerate(_frames(raw, size)):
        while j < len(want) and want[j] == i:
            enc.stdin.write(b"".join(np.ascontiguousarray(p).tobytes() for p in f))
            j += 1
        if j == len(want):
            break
    enc.stdin.close()
    if enc.wait() or j < len(want):
        raise RuntimeError(f"motion ramp short: {j}/{len(want)} frames, {dst}")
    return dst


def cut(a: Path, b_src: Path, b_start: float, b_x: float, dst: Path, *,
        n: int, fps: int, size: tuple[int, int], out_args: list[str],
        build: int = 30, heal_frames: int = 75, speed: float = 4.0,
        bloom_n: int = 10) -> Path:
    """The incoming shot, `n` frames, with the glitch cut from `a` into it.

    `build` frames of A broken up by B's motion at `speed`x, then a
    `heal_frames` heal into clean B while the motion slows to 1x, then clean B.
    The defaults are the ones the user signed off on the forest-to-circle test.
    """
    work = dst.parent
    clean = _segment(b_src, work / f"{dst.stem}-clean.mkv", b_start,
                     n / fps + 0.2, b_x, size, fps)
    total = build + heal_frames
    ease = 1 - (1 - np.linspace(0, 1, heal_frames)) ** 2
    speeds = [speed] * (build - bloom_n) + list(speed - (speed - 1) * ease)
    motion = motion_ramp(b_src, work / f"{dst.stem}-motion.mkv", b_start, b_x,
                         size, fps, speeds)
    m = mosh(a, motion, work / f"{dst.stem}-mosh.mkv", frames=total, fps=fps,
             size=size, bloom_n=bloom_n)
    return heal(m, total, clean, dst, frames=n, heal_frames=heal_frames,
                size=size, fps=fps, out_args=out_args)


def main() -> None:
    """Test a glitch cut between any two SDR clips: `python -m ...datamosh -h`."""
    import argparse

    ap = argparse.ArgumentParser(description=main.__doc__)
    ap.add_argument("a", type=Path, help="outgoing clip")
    ap.add_argument("b", type=Path, help="incoming clip")
    ap.add_argument("out", type=Path)
    ap.add_argument("--a-start", type=float, default=0.0)
    ap.add_argument("--a-dur", type=float, default=3.0)
    ap.add_argument("--b-start", type=float, default=0.0)
    ap.add_argument("--b-dur", type=float, default=5.0)
    ap.add_argument("--a-x", type=float, default=0.5, help="crop position 0..1")
    ap.add_argument("--b-x", type=float, default=0.5)
    ap.add_argument("--build", type=int, default=30, help="frames of break-up")
    ap.add_argument("--heal", type=int, default=75, help="frames of heal after it")
    ap.add_argument("--speed", type=float, default=4.0, help="motion speed")
    ap.add_argument("--bloom", type=int, default=10, help="repeated P-frames")
    ap.add_argument("--size", default="1080x1920")
    ap.add_argument("--fps", type=int, default=30)
    args = ap.parse_args()

    size = tuple(int(v) for v in args.size.split("x"))
    work = args.out.with_name(f".work-{args.out.stem}")
    work.mkdir(parents=True, exist_ok=True)
    n_a = round(args.a_dur * args.fps)
    a = _segment(args.a, work / "a-long.mkv", args.a_start, args.a_dur + 0.2,
                 args.a_x, size, args.fps)
    _run(["ffmpeg", "-v", "error", "-y", "-i", str(a), "-frames:v", str(n_a),
          "-c:v", "ffv1", str(work / "a.mkv")])
    b = cut(work / "a.mkv", args.b, args.b_start, args.b_x, work / "b.mkv",
            n=round(args.b_dur * args.fps), fps=args.fps, size=size,
            out_args=["-c:v", "ffv1"], build=args.build,
            heal_frames=args.heal, speed=args.speed, bloom_n=args.bloom)
    _run(["ffmpeg", "-v", "error", "-y", "-i", str(work / "a.mkv"), "-i",
          str(b), "-filter_complex", "[0:v][1:v]concat=n=2:v=1[o]", "-map",
          "[o]", "-c:v", "libx264", "-crf", "16", "-pix_fmt", "yuv420p",
          "-movflags", "+faststart", str(args.out)])
    c = n_a / args.fps
    print(f"{args.out}  cut {c:.2f}s, heal {c + args.build / args.fps:.2f}-"
          f"{c + (args.build + args.heal) / args.fps:.2f}s")


if __name__ == "__main__":
    main()
