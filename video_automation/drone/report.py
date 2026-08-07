"""Human-readable review of the index. This is the artefact you validate against."""

from __future__ import annotations

from .config import LOW_CONFIDENCE


def print_report(conn) -> None:
    rows = list(conn.execute(
        "SELECT filename, duration, move_type, motion_energy, pan_rate, "
        "rot_rate, zoom_rate, sharpness, highlight_clip, confidence "
        "FROM clips ORDER BY motion_energy"
    ))
    if not rows:
        print("Index is empty.")
        return

    print(f"{'clip':<22} {'dur':>6} {'move':<10} {'energy':>7} "
          f"{'pan/s':>7} {'rot/s':>7} {'zoom/s':>7} {'sharp':>7} {'blown':>6} {'conf':>5}")
    print("-" * 100)
    for fn, dur, move, energy, pan, rot, zoom, sharp, hi, conf in rows:
        flag = " !" if conf < LOW_CONFIDENCE else ""
        name = fn if len(fn) <= 21 else fn[:18] + "..."
        print(f"{name:<22} {dur:>5.1f}s {move:<10} {energy:>7.3f} "
              f"{pan:>7.3f} {rot:>7.2f} {zoom:>7.3f} "
              f"{sharp:>7.1f} {hi*100:>5.1f}% {conf:>5.2f}{flag}")

    total = sum(r[1] for r in rows)
    print(f"\n{len(rows)} clips, {total/60:.1f} min total")
    print("! = low tracking confidence, motion values unreliable")
