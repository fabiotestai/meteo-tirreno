r"""Applicazione in produzione delle correzioni MOS (correzioni/mos.json).

Nessuna dipendenza dall'allenamento (meteo/mos.py): qui si legge il file, si sceglie per
ogni ora la correzione giusta e la si applica. Formule e contratto sono in meteo/mos.py.

Giorno di anticipo. I coefficienti sono allenati su "previous runs" di Open-Meteo, dove
previous_dayN è la corsa con anticipo in [24·N, 24·N + passo delle corse) ore (misurato con le
single runs: ICON-2I, corse ogni 12 h, dà 0-11 h, 24-35 h, 48-59 h). Per le previsioni
correnti l'anticipo è L = T - inizio della corsa del modello di riferimento (il primo: ICON-2I) e
si usa il giorno d più vicino:
    d = \lfloor (L + 6) / 24 \rfloor
(0 per L <= 17 h, 1 per 18-41 h, 2 oltre), limitato al massimo allenato. Gli altri modelli hanno
corse in orari diversi, quindi il loro anticipo reale differisce di poche ore da quello del
riferimento: è dentro la variabilità dell'allenamento.
"""
from __future__ import annotations

import json
import math
import time
from pathlib import Path

from .config import ROOT
from .wind import speed_dir_to_uv, uv_to_speed_dir, wind_name

SCHEMA_VERSION = 1  # versione dello schema di mos.json che questo codice sa leggere
MAX_AGE_DAYS = 60  # oltre, i coefficienti si considerano scaduti e il MOS non si mostra
PATH = ROOT / "correzioni" / "mos.json"


# ---------------------------------------------------------------- vento: fonte, direzione


def mean_wind(winds: list[tuple[float, float]]) -> tuple[float, float]:
    """(velocità, direzione) del vento medio di più modelli: media dei VETTORI, mai delle direzioni."""
    us, vs = zip(*(speed_dir_to_uv(s, d) for s, d in winds))
    return uv_to_speed_dir(sum(us) / len(us), sum(vs) / len(vs))


def source_wind(modelli: list[str], fc: dict) -> tuple[float, float]:
    """(velocità, direzione) da cui si leggono settore e rotazione: un modello o la media di più."""
    if len(modelli) == 1:
        w = fc[modelli[0]]
        return w["vel"], w["dir"]
    return mean_wind([(fc[m]["vel"], fc[m]["dir"]) for m in modelli])


def rotated_direction(fonte: list[str], rotazione: dict[str, float], fc: dict) -> float:
    _, d = source_wind(fonte, fc)
    return (d + rotazione[wind_name(d)]) % 360.0


# ---------------------------------------------------------------- una correzione


def features(ingressi: list, t: int, fc: dict) -> list[float]:
    """Riga di X: intercetta, ingressi, armoniche dell'ora UTC."""
    w = 2 * math.pi * (t % 86400) / 86400
    return [1.0, *(fc[m][q] for m, q in ingressi), math.sin(w), math.cos(w)]


def predict_value(corr: dict, t: int, fc: dict) -> float:
    beta = corr["settori"][wind_name(source_wind(corr["fonte"], fc)[1])]
    return max(0.0, sum(b * x for b, x in zip(beta, features(corr["ingressi"], t, fc))))


def apply_correction(corr: dict, t: int, fc: dict) -> dict:
    """Valore corretto in nodi; per la velocità anche la direzione corretta in gradi.

    fc = {modello: {"vel": nodi, "dir": gradi, "raf": nodi o None}}, t = istante unix UTC.
    """
    value = predict_value(corr, t, fc)
    if corr["grandezza"] == "vel":
        d = corr["direzione"]
        return {"vel": value, "dir": rotated_direction(d["fonte"], d["rotazione"], fc)}
    return {"raf": value}


# ---------------------------------------------------------------- il file


def load_corrections(path: Path | None = None, now: float | None = None) -> tuple[dict | None, str | None]:
    """(file, motivo): il file solo se esiste, ha lo schema giusto ed è abbastanza recente."""
    path = path or PATH
    if not path.exists():
        return None, f"{path.name} non trovato"
    try:
        mos = json.loads(path.read_text())
    except ValueError as e:
        return None, f"{path.name} illeggibile: {e}"
    if mos.get("versione") != SCHEMA_VERSION:
        return None, f"schema {mos.get('versione')} invece di {SCHEMA_VERSION}"
    age = ((now if now is not None else time.time()) - mos["generated"]) / 86400
    if age > MAX_AGE_DAYS:
        return None, f"coefficienti vecchi di {age:.0f} giorni (massimo {MAX_AGE_DAYS})"
    return mos, None


def corrections_for(mos: dict, station: str) -> dict[str, dict[int, dict]]:
    """{"vel": {giorno: correzione}, "raf": {...}} con l'insieme di modelli più ricco disponibile."""
    out: dict[str, dict[int, dict]] = {}
    for q in ("vel", "raf"):
        cands = [c for c in mos["correzioni"] if c["stazione"] == station and c["grandezza"] == q]
        if cands:
            n = max(len(c["modelli"]) for c in cands)
            out[q] = {c["giorno"]: c for c in cands if len(c["modelli"]) == n}
    return out


def lead_day(lead_hours: float, max_day: int) -> int | None:
    """Giorno di anticipo (come in previous runs) più vicino all'anticipo dato; None se negativo."""
    if lead_hours < 0:
        return None
    return min(max_day, int((lead_hours + 6) // 24))


# ---------------------------------------------------------------- serie corretta


def _correction_for(corrs: dict[str, dict[int, dict]], quantity: str, lead: float) -> dict | None:
    """La correzione di `quantity` per il giorno di anticipo di `lead`, se esiste."""
    days = corrs.get(quantity)
    day = lead_day(lead, max(days)) if days else None
    return days.get(day) if day is not None else None


def _forecast_at(series: dict[str, dict], index: dict[str, dict[int, int]], models: list[str], t: int, need_gust: bool) -> dict | None:
    fc = {}
    for m in models:
        i = index.get(m, {}).get(t)
        if i is None:
            return None
        s = series[m]
        vel, direction = s["wind_speed_10m"][i], s["wind_direction_10m"][i]
        gusts = s.get("wind_gusts_10m") or []
        gust = gusts[i] if i < len(gusts) else None
        if vel is None or direction is None or (need_gust and gust is None):
            return None
        fc[m] = {"vel": vel, "dir": direction, "raf": gust}
    return fc


def corrected_series(corrs: dict[str, dict[int, dict]], series: dict[str, dict], ref_init: int, hours: list[int]) -> dict[str, list]:
    """Velocità, direzione e raffica corrette alle ore `hours`; None dove manca un ingresso.

    series = {modello: {"time": [unix], "wind_speed_10m": [kn], "wind_direction_10m": [°], "wind_gusts_10m": [kn]}}.
    """
    index = {m: {t: i for i, t in enumerate(s["time"])} for m, s in series.items()}
    out: dict[str, list] = {"vel": [], "dir": [], "raf": []}
    for t in hours:
        lead = (t - ref_init) / 3600
        vel = dirn = raf = None
        corr = _correction_for(corrs, "vel", lead)
        if corr:
            fc = _forecast_at(series, index, corr["modelli"], t, need_gust=False)
            if fc:
                res = apply_correction(corr, t, fc)
                vel, dirn = round(res["vel"], 1), round(res["dir"]) % 360
        corr = _correction_for(corrs, "raf", lead)
        if corr:
            fc = _forecast_at(series, index, corr["modelli"], t, need_gust=True)
            if fc:
                raf = round(apply_correction(corr, t, fc)["raf"], 1)
        out["vel"].append(vel)
        out["dir"].append(dirn)
        out["raf"].append(raf)
    return out


def evaluation_summary(mos: dict, station: str, corrs: dict[str, dict[int, dict]], day: int = 1) -> dict:
    """Errore medio (MAE, nodi) di previsione grezza e corretta sulla prova, per l'anticipo `day`."""
    out: dict = {"test_dal": mos["test_dal"], "addestrato": mos["generated"]}
    for q in ("vel", "raf"):
        corr = corrs.get(q, {}).get(day)
        ev = next((e for e in mos["valutazione"] if corr and e["stazione"] == station and e["grandezza"] == q
                   and e["modello"] == corr["modello"] and e["giorno"] == day), None)
        if ev:
            out[q] = {"mae_grezzo": ev["grezzo"]["mae"], "mae_mos": ev["mos"]["mae"], "ore": ev["n"]}
    return out


def station_block(mos: dict, station: dict, series: dict[str, dict], ref_init: int, hours: list[int]) -> dict | None:
    """Il blocco `mos` di uno spot: serie corretta e sintesi della prova. None se la stazione non ha correzioni."""
    corrs = corrections_for(mos, station["codice"])
    if "vel" not in corrs:
        return None
    return {
        "stazione": {k: station[k] for k in ("nome", "codice", "lat", "lon")},
        **corrected_series(corrs, series, ref_init, hours),
        "info": evaluation_summary(mos, station["codice"], corrs),
    }
