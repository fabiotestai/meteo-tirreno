"""Download da Open-Meteo (solo libreria standard, nessuna dipendenza).

Open-Meteo ridistribuisce in JSON gli stessi modelli (ICON-2I, ICON-EU,
ECMWF open data...) che altrimenti andrebbero scaricati in GRIB dai singoli
enti. È la via più rapida per la prima versione; il download GRIB diretto
può sostituirla più avanti senza toccare il resto della pipeline.

Nota licenza: l'API gratuita è per uso non commerciale. Per un prodotto
pubblico a pagamento serve il piano commerciale o il download diretto.
"""
from __future__ import annotations

import json
import time
import urllib.error
import urllib.parse
import urllib.request
from typing import Any, Iterable, Sequence

FORECAST_URL = "https://api.open-meteo.com/v1/forecast"
MARINE_URL = "https://marine-api.open-meteo.com/v1/marine"
PREVIOUS_RUNS_URL = "https://previous-runs-api.open-meteo.com/v1/forecast"
CHUNK = 100  # punti per richiesta (le coordinate vanno nell'URL)
USER_AGENT = "meteo-tirreno/0.1 (progetto personale)"


def _get(url: str, params: dict[str, Any], retries: int = 3) -> Any:
    query = urllib.parse.urlencode(params, safe=",")
    req = urllib.request.Request(f"{url}?{query}", headers={"User-Agent": USER_AGENT})
    for attempt in range(retries):
        try:
            with urllib.request.urlopen(req, timeout=60) as resp:
                return json.load(resp)
        except urllib.error.HTTPError as e:
            body = e.read().decode("utf-8", "replace")[:300]
            if e.code in (429, 500, 502, 503, 504) and attempt < retries - 1:
                time.sleep(5 * (attempt + 1))
                continue
            raise RuntimeError(f"Open-Meteo {e.code}: {body}") from e
        except urllib.error.URLError:
            if attempt < retries - 1:
                time.sleep(5 * (attempt + 1))
                continue
            raise
    raise RuntimeError("unreachable")


def _chunks(seq: Sequence, size: int) -> Iterable[Sequence]:
    for i in range(0, len(seq), size):
        yield seq[i : i + size]


def _as_list(data: Any) -> list[dict]:
    # una sola coordinata -> oggetto; più coordinate -> lista
    return data if isinstance(data, list) else [data]


def _coords(points: Sequence[tuple[float, float]]) -> dict[str, str]:
    return {
        "latitude": ",".join(f"{lat:.4f}" for lat, _ in points),
        "longitude": ",".join(f"{lon:.4f}" for _, lon in points),
    }


def fetch_hourly(
    points: Sequence[tuple[float, float]],
    variables: Sequence[str],
    model: str | None,
    forecast_days: int,
    marine: bool = False,
) -> list[dict[str, list]]:
    """Serie orarie per ogni punto, nello stesso ordine di `points`.

    Ritorna una lista di dict {"time": [unix...], <variabile>: [valori...]}.
    Vento in nodi; tempi in UTC (unix, secondi).
    """
    out: list[dict[str, list]] = []
    for chunk in _chunks(points, CHUNK):
        params: dict[str, Any] = {
            **_coords(chunk),
            "hourly": ",".join(variables),
            "forecast_days": forecast_days,
            "timeformat": "unixtime",
            "timezone": "GMT",
        }
        if not marine:
            params["wind_speed_unit"] = "kn"
        if model:
            params["models"] = model
        data = _as_list(_get(MARINE_URL if marine else FORECAST_URL, params))
        if len(data) != len(chunk):
            raise RuntimeError(f"attesi {len(chunk)} punti, ricevuti {len(data)}")
        for item in data:
            hourly = item.get("hourly") or {}
            out.append({k: hourly.get(k, []) for k in ["time", *variables]})
    return out


def fetch_previous_runs(
    point: tuple[float, float],
    variables: Sequence[str],
    model: str,
    start_date: str,
    end_date: str,
    days: int,
) -> dict:
    """Previsioni passate di un punto, separate per giorni di anticipo.

    Per ogni ora T, "previous_dayN" è il valore previsto per T dalla corsa
    uscita circa N giorni prima (anticipo tra 24·N e 24·N+23 ore); N = 0 è la
    corsa più recente. Serve per verificare il modello come lo si usa davvero,
    a 1-2 giorni, e non solo sulle prime ore di ogni corsa.

    Ritorna {"time": [unix...], 0: {var: [...]}, 1: {var: [...]}, ...}.
    Vento in m/s; tempi in UTC.
    """
    names = {(var, d): var if d == 0 else f"{var}_previous_day{d}" for var in variables for d in range(days + 1)}
    params = {
        "latitude": f"{point[0]:.4f}",
        "longitude": f"{point[1]:.4f}",
        "hourly": ",".join(names.values()),
        "models": model,
        "start_date": start_date,
        "end_date": end_date,
        "wind_speed_unit": "ms",
        "timeformat": "unixtime",
        "timezone": "GMT",
    }
    hourly = _get(PREVIOUS_RUNS_URL, params).get("hourly") or {}
    times = hourly.get("time", [])
    out: dict = {"time": times}
    for (var, d), name in names.items():
        out.setdefault(d, {})[var] = hourly.get(name) or [None] * len(times)
    return out
