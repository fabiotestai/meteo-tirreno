"""CSV mensili condivisi dal job giornaliero, dalla verifica e dal MOS.

I tempi sono UTC, il vento è in m/s. Gli osservati ARPAL mantengono il tempo
di fine ora del client originale. La lettura accetta anche i vecchi CSV annuali.
Le scritture sono atomiche; un recupero parziale non cancella lo storico.
"""
from __future__ import annotations

import csv
import json
from datetime import datetime, timezone
from pathlib import Path

OBS_HEADER = ["t", "utc", "velocita_ms", "raffica_ms", "direzione"]
FC_HEADER = ["t", "giorno", "velocita_ms", "direzione", "raffica_ms"]


def write_csv(path: Path, header: list[str], rows: list[list]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(".tmp")
    with tmp.open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f, lineterminator="\n")  # stessi byte su Windows e sul runner Linux
        writer.writerow(header)
        writer.writerows(rows)
    tmp.replace(path)


def write_json(path: Path, data: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(".tmp")
    tmp.write_text(json.dumps(data, ensure_ascii=False, allow_nan=False, indent=2) + "\n", encoding="utf-8")
    tmp.replace(path)


def number(value: str) -> float | None:
    return float(value) if value else None


def read_observed(root: Path, code: str) -> dict[int, dict]:
    out = {}
    paths = list((root / "osservati").glob(f"ARPAL_{code}_*.csv"))
    # Prima gli annuali, poi i mensili: il dato nuovo ha la precedenza.
    for path in sorted(paths, key=lambda p: (len(p.stem), p.name)):
        with path.open(encoding="utf-8", newline="") as f:
            for r in csv.DictReader(f):
                out[int(r["t"])] = {"speed": number(r["velocita_ms"]),
                                  "gust": number(r["raffica_ms"]), "dir": number(r["direzione"])}
    return out


def read_forecast(root: Path, code: str, key: str, days: int) -> dict[int, dict]:
    out = {d: {} for d in range(days + 1)}
    for path in sorted((root / "previsioni" / key).glob(f"{code}_*.csv")):
        with path.open(encoding="utf-8", newline="") as f:
            for r in csv.DictReader(f):
                d = int(r["giorno"])
                if d in out:
                    out[d][int(r["t"])] = {"speed": number(r["velocita_ms"]),
                                          "dir": number(r["direzione"]), "gust": number(r["raffica_ms"])}
    return out


def merge_records(old: dict[int, dict], new: dict[int, dict]) -> dict[int, dict]:
    """Aggiorna i valori restituiti; assenze e null non cancellano valori noti."""
    out = {t: dict(v) for t, v in old.items()}
    for t, v in new.items():
        out.setdefault(t, {"speed": None, "gust": None, "dir": None}).update({k: float(x) for k, x in v.items() if x is not None})
    return out


def month(t: int) -> str:
    return datetime.fromtimestamp(t, timezone.utc).strftime("%Y-%m")


def write_observed(root: Path, code: str, records: dict[int, dict]) -> None:
    groups = {}
    for t, v in sorted(records.items()):
        utc = datetime.fromtimestamp(t, timezone.utc).strftime("%Y-%m-%dT%H:%MZ")
        groups.setdefault(month(t), []).append([t, utc, v.get("speed"), v.get("gust"), v.get("dir")])
    for m, rows in groups.items():
        write_csv(root / "osservati" / f"ARPAL_{code}_{m}.csv", OBS_HEADER, rows)


def write_forecast(root: Path, code: str, key: str, records: dict[int, dict]) -> None:
    groups = {}
    for d, series in sorted(records.items()):
        for t, v in sorted(series.items()):
            groups.setdefault(month(t), []).append([t, d, v.get("speed"), v.get("dir"), v.get("gust")])
    for m, rows in groups.items():
        write_csv(root / "previsioni" / key / f"{code}_{m}.csv", FC_HEADER, rows)


def import_cache(source: Path, target: Path, cfg: dict) -> dict:
    """Copia e converte senza rete; rifiuta l'importazione sopra una cache esistente."""
    if source.resolve() == target.resolve() or any(target.glob("osservati/*.csv")) or any(target.glob("previsioni/*/*.csv")):
        raise ValueError("l'importazione richiede una destinazione distinta e vuota")
    from .build import model_key
    total_obs = total_fc = 0
    for st in cfg["verifica"]["stazioni"]:
        code = st["codice"]
        obs = read_observed(source, code)
        write_observed(target, code, obs)
        total_obs += len(obs)
        for model in cfg["models"] + cfg["verifica"].get("confronti", []):
            key = model_key(model["label"])
            fc = read_forecast(source, code, key, int(model.get("giorni_anticipo", cfg["verifica"]["giorni_anticipo"])))
            write_forecast(target, code, key, fc)
            total_fc += sum(map(len, fc.values()))
    if not total_obs or not total_fc:
        raise ValueError("cache sorgente priva di osservati o previsioni")
    return {"ore_osservate": total_obs, "righe_previste": total_fc}
