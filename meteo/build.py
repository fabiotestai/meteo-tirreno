"""Costruisce i file JSON letti dalla mappa web.

Uso:
    python -m meteo.build                 # dati reali da Open-Meteo
    python -m meteo.build --demo          # dati sintetici, per provare la pagina offline
    python -m meteo.build --out web/data  # cartella di destinazione (predefinita)

File prodotti in --out:
    meta.json          data di generazione, modelli, asse dei tempi, griglia
    wind_<modello>.json   campo di vento u/v (m/s) per ogni istante, per la mappa animata
    spots.json         serie orarie per gli spot: vento, raffiche, pioggia, onda
"""
from __future__ import annotations

import argparse
import json
import math
import time
from pathlib import Path

from . import openmeteo
from .config import ROOT, Grid, build_grid, load_config
from .wind import KNOT_MS, interpolate, interpolate_wind, speed_dir_to_uv, time_axis

GRID_VARS = ["wind_speed_10m", "wind_direction_10m"]
SPOT_VARS = ["wind_speed_10m", "wind_direction_10m", "wind_gusts_10m", "precipitation"]
WAVE_VARS = ["wave_height", "wave_direction", "wave_period"]


def _r(x, nd=1):
    return None if x is None else round(x, nd)


def model_key(label: str) -> str:
    return "".join(c for c in label.lower() if c.isalnum())


# ---------------------------------------------------------------- campo di vento


def wind_frames(series: list[dict], axis: list[int]) -> tuple[list[list], list[list]]:
    """Da serie orarie per punto (nodi, gradi) a frame u/v in m/s sull'asse a 30'."""
    per_point_u, per_point_v = [], []
    for s in series:
        sp, di = interpolate_wind(s["time"], s["wind_speed_10m"], s["wind_direction_10m"], axis)
        us, vs = [], []
        for speed, direction in zip(sp, di):
            if speed is None:
                us.append(None)
                vs.append(None)
            else:
                u, v = speed_dir_to_uv(speed * KNOT_MS, direction)
                us.append(_r(u))
                vs.append(_r(v))
        per_point_u.append(us)
        per_point_v.append(vs)
    # trasposizione: frame[t][punto]
    u_frames = [list(col) for col in zip(*per_point_u)]
    v_frames = [list(col) for col in zip(*per_point_v)]
    return u_frames, v_frames


def grid_header(grid: Grid) -> dict:
    return {
        "nx": grid.nx,
        "ny": grid.ny,
        "lo1": grid.lons[0],
        "la1": grid.lats[0],
        "dx": grid.step,
        "dy": grid.step,
    }


# ---------------------------------------------------------------- spot


def spot_record(spot: dict, per_model: dict[str, dict], waves: dict | None, hours: list[int]) -> dict:
    rec = {"name": spot["name"], "lat": spot["lat"], "lon": spot["lon"], "models": {}, "waves": None}
    for key, s in per_model.items():
        rec["models"][key] = {
            "speed": [_r(x) for x in interpolate(s["time"], s["wind_speed_10m"], hours)],
            "dir": [_r(x, 0) for x in interpolate(s["time"], s["wind_direction_10m"], hours)],
            "gust": [_r(x) for x in interpolate(s["time"], s["wind_gusts_10m"], hours)],
            "rain": [_r(x) for x in interpolate(s["time"], s["precipitation"], hours)],
        }
    if waves:
        rec["waves"] = {
            "height": [_r(x) for x in interpolate(waves["time"], waves["wave_height"], hours)],
            "dir": [_r(x, 0) for x in interpolate(waves["time"], waves["wave_direction"], hours)],
            "period": [_r(x) for x in interpolate(waves["time"], waves["wave_period"], hours)],
        }
    return rec


# ---------------------------------------------------------------- dati sintetici


def demo_series(points, start: int, hours: int, model_index: int, extra: bool) -> list[dict]:
    """Un minimo depressionario che attraversa la zona da ovest a est.

    Serve solo a provare la pagina senza rete: non è una previsione.
    """
    times = [start + h * 3600 for h in range(hours + 1)]
    out = []
    for lat, lon in points:
        sp, di, gu, rn = [], [], [], []
        for h in range(hours + 1):
            # centro del minimo: da Baleari verso il Golfo di Genova
            clon = 6.5 + 0.09 * h + 0.15 * model_index
            clat = 42.0 + 0.035 * h
            dx = (lon - clon) * math.cos(math.radians(lat))
            dy = lat - clat
            r = math.hypot(dx, dy) + 0.3
            # circolazione ciclonica (antioraria) + flusso di fondo da ovest
            mag = 34 * r * math.exp(-r / 1.6) / 1.6
            u = -dy / r * mag + 6
            v = dx / r * mag
            speed = math.hypot(u, v)
            direction = math.degrees(math.atan2(-u, -v)) % 360
            sp.append(round(speed, 1))
            di.append(round(direction))
            gu.append(round(speed * 1.45, 1))
            rn.append(round(max(0.0, 3.0 - r * 1.8), 1))
        rec = {"time": times, "wind_speed_10m": sp, "wind_direction_10m": di}
        if extra:
            rec["wind_gusts_10m"] = gu
            rec["precipitation"] = rn
        out.append(rec)
    return out


def demo_waves(spots, start: int, hours: int) -> list[dict]:
    times = [start + h * 3600 for h in range(hours + 1)]
    return [
        {
            "time": times,
            "wave_height": [round(0.4 + 2.2 * math.exp(-((h - 30 - i) ** 2) / 300), 1) for h in range(hours + 1)],
            "wave_direction": [225] * (hours + 1),
            "wave_period": [round(4 + 3 * math.exp(-((h - 34) ** 2) / 400), 1) for h in range(hours + 1)],
        }
        for i, _ in enumerate(spots)
    ]


# ---------------------------------------------------------------- main


def build(out_dir: Path, demo: bool = False) -> dict:
    cfg = load_config()
    grid = build_grid(cfg["area"])
    hours = int(cfg["forecast"]["hours"])
    sub = int(cfg["forecast"]["substep_minutes"])
    now = int(time.time())
    start = now - now % 3600  # ora intera corrente, UTC
    axis = time_axis(start, hours, sub)
    hourly = time_axis(start, hours, 60)
    days = math.ceil(hours / 24) + 1
    spots = cfg["spots"]
    spot_pts = [(s["lat"], s["lon"]) for s in spots]

    out_dir.mkdir(parents=True, exist_ok=True)
    models_meta = []
    spot_models: dict[str, list[dict]] = {}

    for i, m in enumerate(cfg["models"]):
        key = model_key(m["label"])
        print(f"[{m['label']}] griglia {grid.nx}x{grid.ny} ...", flush=True)
        if demo:
            gseries = demo_series(grid.points(), start, hours, i, extra=False)
            sseries = demo_series(spot_pts, start, hours, i, extra=True)
        else:
            gseries = openmeteo.fetch_hourly(grid.points(), GRID_VARS, m["id"], days)
            sseries = openmeteo.fetch_hourly(spot_pts, SPOT_VARS, m["id"], days)
        u, v = wind_frames(gseries, axis)
        valid = [any(x is not None for x in frame) for frame in u]
        payload = {**grid_header(grid), "u": u, "v": v}
        (out_dir / f"wind_{key}.json").write_text(json.dumps(payload, separators=(",", ":")))
        spot_models[key] = sseries
        models_meta.append(
            {
                "key": key,
                "label": m["label"],
                "note": m.get("note", ""),
                "last_valid": max((t for t, ok in zip(axis, valid) if ok), default=None),
            }
        )

    print("[onde] spot ...", flush=True)
    if demo:
        waves = demo_waves(spots, start, hours)
    else:
        try:
            waves = openmeteo.fetch_hourly(spot_pts, WAVE_VARS, None, days, marine=True)
        except Exception as e:  # le onde non devono bloccare il resto
            print(f"  onde non disponibili: {e}")
            waves = [None] * len(spots)

    spot_recs = [
        spot_record(s, {k: spot_models[k][j] for k in spot_models}, waves[j], hourly)
        for j, s in enumerate(spots)
    ]
    (out_dir / "spots.json").write_text(json.dumps({"times": hourly, "spots": spot_recs}, separators=(",", ":")))

    meta = {
        "generated": now,
        "source": "demo" if demo else "open-meteo",
        "times": axis,
        "grid": grid_header(grid),
        "area": cfg["area"],
        "models": models_meta,
    }
    (out_dir / "meta.json").write_text(json.dumps(meta, separators=(",", ":")))
    print(f"Fatto: {out_dir}")
    return meta


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--out", type=Path, default=ROOT / "web" / "data")
    ap.add_argument("--demo", action="store_true", help="dati sintetici, senza rete")
    args = ap.parse_args()
    build(args.out, demo=args.demo)


if __name__ == "__main__":
    main()
