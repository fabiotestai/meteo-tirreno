"""Verifica previsto/osservato del vento sulle stazioni vicine agli spot (fase 1).

Uso:
    python -m meteo.verifica                  # scarica ciò che manca e calcola
    python -m meteo.verifica --solo-cache     # nessun download, solo i file in dati/

Dati:
    osservati   archivio orario ARPAL (media, massimo e direzione nell'ora)
    previsti    Open-Meteo "previous runs": per ogni ora il valore previsto
                0, 1, 2... giorni prima, alle coordinate della stazione

Modelli in [[verifica.confronti]] (es. AROME HD, archivio corto) si valutano
a parte, testa a testa con un modello di riferimento sulle sole ore comuni ai
due: il campione comune dei modelli della mappa resta lo stesso.

I download restano in dati/ (non versionata): gli anni e i mesi conclusi non
si riscaricano, quelli in corso sì.

Uscite:
    web/data/verifica.json   punteggi per stazione, modello, giorno di anticipo, settore
    dati/verifica.csv        gli stessi punteggi in forma tabellare (una riga per gruppo)

Punteggi, con f = previsto e o = osservato (velocità in nodi), su N ore:
    bias       \\bar e = \\frac{1}{N}\\sum_i (f_i - o_i)
    MAE        \\frac{1}{N}\\sum_i |f_i - o_i|
    RMSE       \\sqrt{\\frac{1}{N}\\sum_i (f_i - o_i)^2}
    r          correlazione di Pearson tra f e o
    RMSE vett. \\sqrt{\\frac{1}{N}\\sum_i [(u^f_i - u^o_i)^2 + (v^f_i - v^o_i)^2]}
               errore sul vettore vento: tiene insieme intensità e direzione
    MAE dir.   \\frac{1}{N'}\\sum_i |\\delta_i|, con \\delta_i = ((d^f_i - d^o_i + 180) \\bmod 360) - 180,
               solo sulle N' ore con vento OSSERVATO sopra la soglia (sotto, la direzione è
               rumore); le ore non dipendono dalla previsione, così i confronti sono equi
"""
from __future__ import annotations

import argparse
import csv
import json
import math
import time
from datetime import date, datetime, timedelta, timezone
from pathlib import Path

from . import arpal, openmeteo
from .build import annotate, model_key
from .config import ROOT, load_config
from .wind import KNOT_MS, speed_dir_to_uv, wind_name, WIND_NAMES

DATA = ROOT / "dati"
FC_VARS = ["wind_speed_10m", "wind_direction_10m", "wind_gusts_10m"]


# ---------------------------------------------------------------- cache osservati


def _utc(t: int) -> str:
    return datetime.fromtimestamp(t, timezone.utc).strftime("%Y-%m-%dT%H:%MZ")


def _num(x: str) -> float | None:
    return float(x) if x != "" else None


def _write_csv(path: Path, header: list[str], rows: list[list]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(".tmp")
    with open(tmp, "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(header)
        w.writerows(rows)
    tmp.replace(path)  # niente file a metà se il download si interrompe


def load_observed(station: dict, start: date, today: date, archive_factory, offline: bool) -> dict[int, dict]:
    """{fine ora unix: {"speed", "gust", "dir"} in m/s e gradi}, anno per anno."""
    out: dict[int, dict] = {}
    for year in range(start.year, today.year + 1):
        path = DATA / "osservati" / f"ARPAL_{station['codice']}_{year}.csv"
        if not offline and (year == today.year or not path.exists()):
            first = max(start, date(year, 1, 1))
            last = min(today, date(year, 12, 31))
            print(f"  ARPAL {station['nome']} {year} ...", flush=True)
            data = archive_factory().hourly(station["codice"], first, last)
            rows = [[t, _utc(t), v.get("speed", ""), v.get("gust", ""), v.get("dir", "")] for t, v in sorted(data.items())]
            _write_csv(path, ["t", "utc", "velocita_ms", "raffica_ms", "direzione"], rows)
        if path.exists():
            with open(path) as f:
                for r in csv.DictReader(f):
                    out[int(r["t"])] = {
                        "speed": _num(r["velocita_ms"]),
                        "gust": _num(r["raffica_ms"]),
                        "dir": _num(r["direzione"]),
                    }
    return out


# ---------------------------------------------------------------- cache previsti


def _months(start: date, end: date):
    y, m = start.year, start.month
    while (y, m) <= (end.year, end.month):
        first = date(y, m, 1)
        nxt = date(y + (m == 12), m % 12 + 1, 1)
        yield first, nxt - timedelta(days=1)
        y, m = nxt.year, nxt.month


def load_forecast(station: dict, model: dict, start: date, today: date, days: int, offline: bool) -> dict[int, dict[int, dict]]:
    """{giorno di anticipo: {ora unix: {"speed", "dir", "gust"}}}, mese per mese."""
    out: dict[int, dict[int, dict]] = {d: {} for d in range(days + 1)}
    since = max(start, date.fromisoformat(model.get("archivio_dal", start.isoformat())))
    last_day = today - timedelta(days=1)  # l'ultimo giorno completo
    folder = DATA / "previsioni" / model_key(model["label"])
    for first, last in _months(since, last_day):
        path = folder / f"{station['codice']}_{first:%Y-%m}.csv"
        complete = last < last_day
        if not offline and (not complete or not path.exists()):
            print(f"  {model['label']} {station['nome']} {first:%Y-%m} ...", flush=True)
            res = openmeteo.fetch_previous_runs(
                (station["lat"], station["lon"]), FC_VARS, model["id"],
                max(first, since).isoformat(), min(last, last_day).isoformat(), days,
            )
            rows = []
            for d in range(days + 1):
                s, di, g = (res[d][v] for v in FC_VARS)
                for i, t in enumerate(res["time"]):
                    if s[i] is not None and di[i] is not None:
                        rows.append([t, d, s[i], di[i], "" if g[i] is None else g[i]])
            _write_csv(path, ["t", "giorno", "velocita_ms", "direzione", "raffica_ms"], rows)
        if path.exists():
            with open(path) as f:
                for r in csv.DictReader(f):
                    d = int(r["giorno"])
                    if d <= days:
                        out[d][int(r["t"])] = {
                            "speed": float(r["velocita_ms"]),
                            "dir": float(r["direzione"]),
                            "gust": _num(r["raffica_ms"]),
                        }
    return out


# ---------------------------------------------------------------- punteggi


def angle_diff(a: float, b: float) -> float:
    """Differenza a - b ricondotta tra -180° e +180°."""
    return (a - b + 180.0) % 360.0 - 180.0


def scalar_scores(f: list[float], o: list[float]) -> dict:
    """Bias, MAE, RMSE e correlazione di una grandezza scalare (previsto f, osservato o)."""
    n = len(f)
    if n == 0:
        return {"n": 0}
    err = [a - b for a, b in zip(f, o)]
    mf, mo = sum(f) / n, sum(o) / n
    sf = math.sqrt(sum((x - mf) ** 2 for x in f))
    so = math.sqrt(sum((x - mo) ** 2 for x in o))
    cov = sum((x - mf) * (y - mo) for x, y in zip(f, o))
    return {
        "n": n,
        "oss_media": round(mo, 2),
        "prev_media": round(mf, 2),
        "bias": round(sum(err) / n, 2),
        "mae": round(sum(abs(e) for e in err) / n, 2),
        "rmse": round(math.sqrt(sum(e * e for e in err) / n), 2),
        "r": round(cov / (sf * so), 3) if sf > 0 and so > 0 else None,
    }


def scores(pairs: list[tuple[dict, dict]], min_dir_kn: float) -> dict:
    """Punteggi su coppie (previsto, osservato) con velocità in nodi.

    L'errore di direzione si conta sulle ore con vento OSSERVATO sopra la soglia:
    la scelta delle ore non dipende dalla previsione, quindi modelli e
    correzioni diverse si confrontano sulle stesse ore. (Filtrare anche sulla
    velocità prevista, come si faceva all'inizio, dà a ogni previsione un
    insieme di ore diverso e falsa i confronti.)
    """
    if not pairs:
        return {"n": 0}
    out = scalar_scores([p["speed"] for p, _ in pairs], [q["speed"] for _, q in pairs])
    vec = 0.0
    for p, q in pairs:
        uf, vf = speed_dir_to_uv(p["speed"], p["dir"])
        uo, vo = speed_dir_to_uv(q["speed"], q["dir"])
        vec += (uf - uo) ** 2 + (vf - vo) ** 2
    dirs = [abs(angle_diff(p["dir"], q["dir"])) for p, q in pairs if q["speed"] >= min_dir_kn]
    gusts = [p["gust"] - q["gust"] for p, q in pairs if p.get("gust") is not None and q.get("gust") is not None]
    return {
        **out,
        "rmse_vett": round(math.sqrt(vec / len(pairs)), 2),
        "n_dir": len(dirs),
        "mae_dir": round(sum(dirs) / len(dirs), 1) if dirs else None,
        "n_raffica": len(gusts),
        "bias_raffica": round(sum(gusts) / len(gusts), 2) if gusts else None,
    }


def _kn(rec: dict) -> dict:
    return {
        "speed": rec["speed"] / KNOT_MS,
        "dir": rec["dir"],
        "gust": None if rec.get("gust") is None else rec["gust"] / KNOT_MS,
    }


def evaluate(observed: dict[int, dict], forecasts: dict[str, dict[int, dict[int, dict]]], days: int, min_dir_kn: float) -> list[dict]:
    """Righe di punteggio per modello x giorno x campione x settore.

    "comune": solo le ore in cui TUTTI i modelli hanno la previsione per quel
    giorno di anticipo, così il confronto tra modelli è sulle stesse ore.
    "completo": tutte le ore disponibili per quel modello.
    Il settore è quello di provenienza OSSERVATO (rosa a 8 venti).
    """
    obs = {t: _kn(v) for t, v in observed.items() if v.get("speed") is not None and v.get("dir") is not None}
    rows = []
    for d in range(days + 1):
        common = set(obs)
        for fc in forecasts.values():
            common &= set(fc[d])
        for key, fc in forecasts.items():
            for sample, hours in (("comune", common), ("completo", set(obs) & set(fc[d]))):
                pairs = [(_kn(fc[d][t]), obs[t]) for t in sorted(hours)]
                groups: dict[str | None, list] = {None: pairs}
                for p in pairs:
                    groups.setdefault(wind_name(p[1]["dir"]), []).append(p)
                for sector in [None, *WIND_NAMES]:
                    sc = scores(groups.get(sector, []), min_dir_kn)
                    if sc["n"]:
                        rows.append({"modello": key, "giorno": d, "campione": sample, "settore": sector, **sc})
    return rows


def compare(observed: dict[int, dict], extra: tuple[str, dict], reference: tuple[str, dict], days: int, min_dir_kn: float) -> list[dict]:
    """Testa a testa tra un modello extra e uno di riferimento, sulle sole ore comuni ai due.

    Tiene solo il campione "comune": il "completo" del riferimento è già nel
    confronto principale.
    """
    rows = evaluate(observed, dict([extra, reference]), days, min_dir_kn)
    return [{**r, "confronto": extra[0]} for r in rows if r["campione"] == "comune"]


# ---------------------------------------------------------------- resoconto


def _score_table(rows: list[dict], labels: dict[str, str]) -> list[str]:
    lines = ["| modello | giorno | ore | oss. kn | bias kn | MAE kn | RMSE kn | r | RMSE vett. kn | MAE dir. ° | bias raffica kn |"]
    lines.append("|---|---|---|---|---|---|---|---|---|---|---|")
    for r in rows:
        if r["campione"] == "comune" and r["settore"] is None:
            lines.append(
                f"| {labels[r['modello']]} | {r['giorno']} | {r['n']} | {r['oss_media']} | {r['bias']:+} | {r['mae']} | {r['rmse']} "
                f"| {r['r']} | {r['rmse_vett']} | {r['mae_dir']} | {'' if r['bias_raffica'] is None else format(r['bias_raffica'], '+')} |"
            )
    return lines


def report(station: dict, rows: list[dict], labels: dict[str, str], pairs: dict[str, list[dict]] | None = None) -> str:
    """Tabelle Markdown leggibili a terminale (campione comune)."""
    lines = [f"\n## {station['spot']} — {station['nome']}\n"]
    lines += _score_table(rows, labels)
    for key, prow in (pairs or {}).items():
        if prow:
            lines.append(f"\nConfronto separato {labels[key]}, stesse ore del riferimento:\n")
            lines += _score_table(prow, labels)
    main = [k for k in labels if any(r["modello"] == k for r in rows)]  # solo i modelli del confronto principale
    lines.append("\nBias di velocità (kn) per settore osservato, giorno 1:\n")
    lines.append("| settore | ore | " + " | ".join(labels[k] for k in main) + " |")
    lines.append("|---|---|" + "---|" * len(main))
    for sector in WIND_NAMES:
        cells = {r["modello"]: r for r in rows if r["campione"] == "comune" and r["giorno"] == 1 and r["settore"] == sector}
        if cells:
            n = next(iter(cells.values()))["n"]
            lines.append(f"| {sector} | {n} | " + " | ".join(f"{cells[k]['bias']:+}" if k in cells else "" for k in main) + " |")
    return "\n".join(lines)


# ---------------------------------------------------------------- main


def run(out_dir: Path, offline: bool = False, since: date | None = None) -> dict:
    cfg = load_config()
    vcfg = cfg["verifica"]
    days = int(vcfg["giorni_anticipo"])
    min_dir_kn = float(vcfg["vento_minimo_direzione_kn"])
    start = since or date.fromisoformat(vcfg["dal"])
    today = datetime.now(timezone.utc).date()
    labels = {model_key(m["label"]): m["label"] for m in cfg["models"]}
    extras = vcfg.get("confronti", [])
    labels_all = {**labels, **{model_key(m["label"]): m["label"] for m in extras}}

    session: list[arpal.Archive] = []

    def archive() -> arpal.Archive:  # una sola sessione ARPAL, aperta solo se serve
        if not session:
            session.append(arpal.Archive())
        return session[0]

    stations_out, all_rows, texts = [], [], []
    for st in vcfg["stazioni"]:
        print(f"[{st['nome']}]", flush=True)
        try:
            observed = load_observed(st, start, today, archive, offline)
        except Exception as e:  # una stazione che fallisce non blocca le altre
            annotate("warning", f"ARPAL {st['nome']} saltata", f"{type(e).__name__}: {e}")
            continue
        forecasts = {}
        for m in cfg["models"]:
            try:
                forecasts[model_key(m["label"])] = load_forecast(st, m, start, today, days, offline)
            except Exception as e:
                annotate("warning", f"{m['label']} {st['nome']} saltato", f"{type(e).__name__}: {e}")
        if not observed or not forecasts:
            continue
        rows = [{**r, "confronto": None} for r in evaluate(observed, forecasts, days, min_dir_kn)]
        pairs = {}
        for m in extras:
            key, ref = model_key(m["label"]), model_key(m["riferimento"])
            if ref not in forecasts:
                continue
            d = min(days, int(m["giorni_anticipo"]))
            try:
                fc = load_forecast(st, m, start, today, d, offline)
            except Exception as e:
                annotate("warning", f"{m['label']} {st['nome']} saltato", f"{type(e).__name__}: {e}")
                continue
            pairs[key] = compare(observed, (key, fc), (ref, forecasts[ref]), d, min_dir_kn)
        texts.append(report(st, rows, labels_all, pairs))
        times = sorted(observed)
        stations_out.append({**st, "ore_osservate": len(times), "dal": _utc(times[0]), "al": _utc(times[-1])})
        all_rows += [{"stazione": st["codice"], **r} for r in rows + [r for p in pairs.values() for r in p]]

    if not all_rows:
        raise RuntimeError("nessuna stazione verificata: vedi gli avvisi sopra")

    result = {
        "generated": int(time.time()),
        "unita": "nodi, gradi",
        "giorni_anticipo": days,
        "vento_minimo_direzione_kn": min_dir_kn,
        "modelli": labels,
        "confronti": [{"modello": model_key(m["label"]), "label": m["label"], "riferimento": model_key(m["riferimento"]),
                       "dal": m["archivio_dal"], "giorni_anticipo": m["giorni_anticipo"]} for m in extras],
        "stazioni": stations_out,
        "punteggi": all_rows,
    }
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / "verifica.json").write_text(json.dumps(result, ensure_ascii=False, separators=(",", ":")))
    keys = ["stazione", "confronto", "modello", "giorno", "campione", "settore", "n", "oss_media", "prev_media", "bias", "mae",
            "rmse", "r", "rmse_vett", "n_dir", "mae_dir", "n_raffica", "bias_raffica"]
    _write_csv(DATA / "verifica.csv", keys, [[r.get(k) if r.get(k) is not None else "" for k in keys] for r in all_rows])
    print("\n".join(texts))
    print(f"\nFatto: {out_dir / 'verifica.json'}, {DATA / 'verifica.csv'}")
    return result


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--out", type=Path, default=ROOT / "web" / "data")
    ap.add_argument("--solo-cache", action="store_true", help="nessun download, usa i file in dati/")
    ap.add_argument("--dal", type=date.fromisoformat, help="inizio del periodo (AAAA-MM-GG)")
    args = ap.parse_args()
    try:
        run(args.out, offline=args.solo_cache, since=args.dal)
    except Exception as e:
        annotate("error", "Verifica fallita", f"{type(e).__name__}: {e}")
        raise SystemExit(1)


if __name__ == "__main__":
    main()
