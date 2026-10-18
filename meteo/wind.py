"""Calcoli sul vento: componenti, nodi, Beaufort, rosa dei venti, interpolazione.

Convenzione meteorologica: la direzione è quella da cui il vento PROVIENE
(Libeccio = 225°, cioè da sud-ovest). Le componenti u (verso est) e v (verso
nord) indicano invece dove il vento VA.
"""
from __future__ import annotations

import math
from typing import Optional, Sequence

KNOT_MS = 0.514444  # 1 nodo in m/s

# Rosa dei venti a 8 settori del Mediterraneo
WIND_NAMES = [
    "Tramontana", "Grecale", "Levante", "Scirocco",
    "Ostro", "Libeccio", "Ponente", "Maestrale",
]

# Limiti superiori della scala Beaufort in nodi (forza 0..11; oltre = 12)
_BEAUFORT_KN = [1, 3, 6, 10, 16, 21, 27, 33, 40, 47, 55, 63]


def speed_dir_to_uv(speed: float, direction_deg: float) -> tuple[float, float]:
    rad = math.radians(direction_deg)
    return -speed * math.sin(rad), -speed * math.cos(rad)


def uv_to_speed_dir(u: float, v: float) -> tuple[float, float]:
    speed = math.hypot(u, v)
    direction = math.degrees(math.atan2(-u, -v)) % 360.0
    return speed, direction


def beaufort(knots: float) -> int:
    for force, limit in enumerate(_BEAUFORT_KN):
        if knots < limit:
            return force
    return 12


def wind_name(direction_deg: float) -> str:
    sector = int(((direction_deg % 360.0) + 22.5) // 45) % 8
    return WIND_NAMES[sector]


def interpolate(
    times: Sequence[int], values: Sequence[Optional[float]], new_times: Sequence[int]
) -> list[Optional[float]]:
    """Interpolazione lineare nel tempo; None se manca uno dei due estremi.

    Per il vento va applicata alle componenti u e v, MAI alla direzione:
    tra 350° e 10° la media lineare darebbe 180°, cioè il vento opposto.
    """
    out: list[Optional[float]] = []
    j = 0
    last = len(times) - 1
    for t in new_times:
        if t < times[0] or t > times[last]:
            out.append(None)
            continue
        while j < last and times[j + 1] < t:
            j += 1
        if times[j] == t:
            out.append(values[j])
            continue
        if j == last:
            out.append(values[last] if times[last] == t else None)
            continue
        a, b = values[j], values[j + 1]
        if a is None or b is None:
            out.append(None)
            continue
        w = (t - times[j]) / (times[j + 1] - times[j])
        out.append(a + (b - a) * w)
    return out


def interpolate_wind(
    times: Sequence[int],
    speeds: Sequence[Optional[float]],
    directions: Sequence[Optional[float]],
    new_times: Sequence[int],
) -> tuple[list[Optional[float]], list[Optional[float]]]:
    """Interpola velocità e direzione passando per le componenti u, v."""
    us: list[Optional[float]] = []
    vs: list[Optional[float]] = []
    for s, d in zip(speeds, directions):
        if s is None or d is None:
            us.append(None)
            vs.append(None)
        else:
            u, v = speed_dir_to_uv(s, d)
            us.append(u)
            vs.append(v)
    ui = interpolate(times, us, new_times)
    vi = interpolate(times, vs, new_times)
    out_s: list[Optional[float]] = []
    out_d: list[Optional[float]] = []
    for u, v in zip(ui, vi):
        if u is None or v is None:
            out_s.append(None)
            out_d.append(None)
        else:
            s, d = uv_to_speed_dir(u, v)
            out_s.append(s)
            out_d.append(d)
    return out_s, out_d


def time_axis(start: int, hours: int, substep_minutes: int) -> list[int]:
    """Istanti (unix, secondi) da start a start+hours con passo substep."""
    step = substep_minutes * 60
    return [start + i * step for i in range(hours * 3600 // step + 1)]


def distance_km(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """Distanza sulla sfera (haversine) tra due punti, in km."""
    p1, p2 = math.radians(lat1), math.radians(lat2)
    a = math.sin((p2 - p1) / 2) ** 2 + math.cos(p1) * math.cos(p2) * math.sin(math.radians(lon2 - lon1) / 2) ** 2
    return 2 * 6371.0 * math.asin(math.sqrt(a))
