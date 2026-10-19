"""Raccolta incrementale e verifica operativa del vento, senza riallenare il MOS.

python -m meteo.giornaliero --data dati --out rapporti --solo-cache
python -m meteo.giornaliero --importa dati --data <cartella-vuota>

Il job usa CSV mensili. Gli originali non vengono filtrati: i controlli di
qualità producono un campione separato per la verifica. Tutti i tempi sono UTC.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import math
import os
from datetime import date, datetime, timedelta, timezone
from pathlib import Path

from . import archivio, arpal, openmeteo
from .build import annotate, model_key
from .config import ROOT, load_config
from .verifica import FC_VARS, _months, compare, evaluate


def timestamp(day: date) -> int:
    return int(datetime.combine(day, datetime.min.time(), timezone.utc).timestamp())


def year_ranges(start: date, end: date):
    for year in range(start.year, end.year + 1):
        yield max(start, date(year, 1, 1)), min(end, date(year, 12, 31))


def quality(records: dict[int, dict], now: datetime, cfg: dict) -> tuple[dict, dict]:
    """Limiti fisici configurabili; sequenze costanti solo sospette, non escluse.

    Un vento calmo può essere costante davvero: il blocco del sensore richiede
    ispezione e non basta, da solo, a eliminare automaticamente delle ore.
    """
    clean, invalid, stuck = {}, [], []
    max_speed, max_gust = float(cfg["velocita_massima_ms"]), float(cfg["raffica_massima_ms"])
    run, previous, previous_t = [], None, None
    for t, v in sorted(records.items()):
        if t > now.timestamp():
            continue
        bad = [k for k, limit in (("speed", max_speed), ("gust", max_gust), ("dir", 360))
               if v.get(k) is not None and (not math.isfinite(v[k]) or not 0 <= v[k] <= limit)]
        if bad:
            invalid.append({"t": t, "campi": bad})
        good = {k: (None if k in bad else v.get(k)) for k in ("speed", "gust", "dir")}
        if good["speed"] is not None or good["gust"] is not None:
            clean[t] = good
        signature = tuple(good[k] for k in ("speed", "gust", "dir"))
        if run and signature == previous and t == previous_t + 3600:
            run.append(t)
        else:
            if len(run) >= int(cfg["ore_sensore_costante"]):
                stuck.append({"dal": run[0], "al": run[-1], "ore": len(run)})
            run = [t] if all(x is not None for x in signature) else []
        previous, previous_t = signature, t
    if len(run) >= int(cfg["ore_sensore_costante"]):
        stuck.append({"dal": run[0], "al": run[-1], "ore": len(run)})
    last = max((t for t, v in clean.items() if v["speed"] is not None), default=None)
    late = (now.timestamp() - last) / 3600 if last is not None else None
    return clean, {"ore_fuori_scala": invalid, "sensore_costante_sospetto": stuck,
                   "ultima_velocita": last, "ritardo_ore": round(late, 1) if late is not None else None,
                   "muta": late is None or late > 24}


def forecast_records(res: dict, days: int, first: date, last: date) -> dict[int, dict]:
    """Valida la struttura prima di salvare: niente sostituzioni con array troncati."""
    times = res["time"]
    if not times or len(set(times)) != len(times):
        raise ValueError("previsioni vuote o tempi duplicati")
    out = {d: {} for d in range(days + 1)}
    for d in out:
        series = res[d]
        if any(len(series[v]) != len(times) for v in FC_VARS):
            raise ValueError("array delle previsioni di lunghezza diversa")
        for i, t in enumerate(times):
            if not timestamp(first) <= t < timestamp(last + timedelta(days=1)):
                raise ValueError("ora prevista fuori dal periodo richiesto")
            vals = {k: series[v][i] for k, v in zip(("speed", "dir", "gust"), FC_VARS)}
            if any(x is not None and not math.isfinite(x) for x in vals.values()):
                raise ValueError("previsioni non finite")
            if vals["speed"] is not None and vals["dir"] is not None:
                out[d][t] = vals
    if not out[0]:
        raise ValueError("nessuna previsione valida al giorno 0")
    return out


def quota(cfg: dict) -> dict:
    """Stima prudente delle chiamate equivalenti, esclusi retry e corse manuali.

    Le richieste incrementali durano <= 10 giorni e hanno <= 9 variabili:
    una per stazione/modello, due quando il periodo attraversa il mese.
    https://open-meteo.com/en/pricing (definizione delle chiamate equivalenti).
    """
    from .config import build_grid
    points = len(build_grid(cfg["area"]).points())
    spots = len(cfg["spots"])
    models = len(cfg["models"])
    stations_mos = sum(bool(s.get("in_mappa")) for s in cfg["verifica"]["stazioni"])
    production = 8 * ((points + spots) * models + spots + stations_mos * models)
    daily = 2 * len(cfg["verifica"]["stazioni"]) * (models + len(cfg["verifica"].get("confronti", [])))
    return {"mappa_8_corse": production, "giornaliero_massimo": daily, "totale": production + daily,
            "limite_gratuito": 10000, "esclusi": "retry, backfill, metadati statici e corse manuali"}


def update_observed(root: Path, st: dict, first: date, last: date, archive) -> tuple[dict, bool]:
    old = archivio.read_observed(root, st["codice"])
    new = {}
    for a, b in year_ranges(first, last):
        part = archive.hourly(st["codice"], a, b)
        if not part:
            raise ValueError(f"ARPAL vuoto dal {a} al {b}; cache conservata")
        if any(not timestamp(a) < t <= timestamp(b + timedelta(days=1)) for t in part):
            raise ValueError("ARPAL: fine ora fuori dal periodo richiesto")
        if any(not math.isfinite(x) for v in part.values() for x in v.values() if x is not None):
            raise ValueError("ARPAL: valori non finiti")
        new.update(part)
    # Le ore già presenti ma non restituite restano; il riepilogo segnala l'ambiguità.
    missing = {t for t in old if timestamp(first) < t <= timestamp(last + timedelta(days=1))} - set(new)
    merged = archivio.merge_records(old, new)
    archivio.write_observed(root, st["codice"], merged)
    return merged, not missing


def update_forecast(root: Path, st: dict, model: dict, first: date, last: date, days: int) -> tuple[dict, bool]:
    key = model_key(model["label"])
    old = archivio.read_forecast(root, st["codice"], key, days)
    merged = {d: dict(s) for d, s in old.items()}
    complete = True
    since = max(first, date.fromisoformat(model.get("archivio_dal", first.isoformat())))
    for a, b in _months(since, last):
        a, b = max(a, since), min(b, last)
        res = openmeteo.fetch_previous_runs((st["lat"], st["lon"]), FC_VARS, model["id"], a.isoformat(), b.isoformat(), days)
        new = forecast_records(res, days, a, b)
        expected = set(range(timestamp(a), timestamp(b + timedelta(days=1)), 3600))
        # Giorni 1/2 possono mancare strutturalmente (es. ECMWF raffiche, buchi ICON).
        complete &= expected <= set(new[0])
        for d in merged:
            merged[d] = archivio.merge_records(merged[d], new[d])
    archivio.write_forecast(root, st["codice"], key, merged)
    return merged, complete


def snapshot_coefficients(path: Path, out: Path) -> dict:
    """Conserva il file operativo per contenuto; non lo ricalcola retroattivamente."""
    content = path.read_bytes()
    obj = json.loads(content)
    if obj.get("versione") != 1:
        raise ValueError("versione MOS non supportata")
    digest = hashlib.sha256(content).hexdigest()
    target = out / "coefficienti" / f"{digest}.json"
    if not target.exists():
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(content)
    return {"sha256": digest, "generated": obj["generated"], "file": f"coefficienti/{digest}.json"}


def summary(result: dict) -> str:
    lines = ["# Raccolta e verifica giornaliera", "", f"Data UTC: {result['data_utc']}", "",
             f"Quota stimata: {result['quota']['totale']} chiamate/giorno (senza retry o corse manuali).", "",
             "I punteggi sono dei modelli grezzi. Nessun riallenamento MOS.", "",
             "| Stazione | Ultima velocità UTC | Ritardo h | Ore valide 30 / 365 giorni |", "|---|---|---|---|"]
    for st in result["stazioni"]:
        q = st["qualita"]
        last = datetime.fromtimestamp(q["ultima_velocita"], timezone.utc).isoformat() if q["ultima_velocita"] else "mai"
        lines.append(f"| {st['nome']} | {last} | {q['ritardo_ore']} | {st['finestre']['30']['ore_valide']} / {st['finestre']['365']['ore_valide']} |")
    lines += ["", "## Avvisi", ""] + [f"- {w}" for w in result["avvisi"]]
    if not result["avvisi"]:
        lines.append("Nessuno.")
    lines += ["", "## Punteggi sul campione comune", "", "| Stazione | Finestra | Modello | Giorno | N | MAE kn | MAE direzione ° |", "|---|---|---|---|---|---|---|"]
    for st in result["stazioni"]:
        for window, block in st["finestre"].items():
            for r in block["punteggi"]:
                if r["campione"] == "comune" and r["settore"] is None:
                    lines.append(f"| {st['nome']} | {window} | {r['modello']} | {r['giorno']} | {r['n']} | {r['mae']} | {r['mae_dir']} |")
    return "\n".join(lines) + "\n"


def run(root: Path, out: Path, cfg: dict, now: datetime, offline: bool = False,
        force_full: bool = False, coefficients: Path | None = None) -> dict:
    today = now.date()
    ccfg, vcfg = cfg["giornaliero"], cfg["verifica"]
    if not 1 <= int(ccfg["sovrapposizione_giorni"]) <= 10 or not 0 <= int(vcfg["giorni_anticipo"]) <= 2:
        raise ValueError("stima della quota valida solo con sovrapposizione <= 10 giorni e anticipo <= 2")
    if int(ccfg["finestra_storica_giorni"]) < 365:
        raise ValueError("la ricarica completa deve coprire almeno i 365 giorni della verifica")
    state_path = root / "stato.json"
    state = json.loads(state_path.read_text(encoding="utf-8")) if state_path.exists() else {}
    full_state = state.setdefault("ricarica_arpal", {})
    result = {"data_utc": today.isoformat(), "generated": int(now.timestamp()), "solo_cache": offline,
              "stazioni": [], "avvisi": [], "mos": None, "quota": quota(cfg)}
    if result["quota"]["totale"] >= result["quota"]["limite_gratuito"]:
        raise ValueError("quota prevista Open-Meteo troppo alta: rivedere la configurazione")

    def warn(message):
        result["avvisi"].append(message)
        annotate("warning", "Raccolta giornaliera", message)

    if coefficients:
        result["mos"] = snapshot_coefficients(coefficients, out)
        archivio.write_json(out / "registro_mos" / today.strftime("%Y-%m") / f"{int(now.timestamp())}.json",
                            {"rilevato": int(now.timestamp()), **result["mos"]})
    archive = None
    for st in vcfg["stazioni"]:
        code = st["codice"]
        observed = archivio.read_observed(root, code)
        full = force_full or full_state.get(code) != today.strftime("%Y-%m")
        first = today - timedelta(days=int(ccfg["finestra_storica_giorni"] if full else ccfg["sovrapposizione_giorni"]))
        if not offline:
            try:
                if archive is None:
                    archive = arpal.Archive(timeout=60, retries=2)
                observed, complete = update_observed(root, st, first, today, archive)
                if complete and full:
                    full_state[code] = today.strftime("%Y-%m")
                if not complete:
                    warn(f"{st['nome']}: ARPAL non ha restituito alcune ore già note; conservate, ricarica non confermata")
            except Exception as e:
                warn(f"{st['nome']}: ARPAL non aggiornato ({e}); uso della cache")
        observed, qc = quality({t: v for t, v in observed.items()
                                if t >= timestamp(today - timedelta(days=365))}, now, ccfg)
        if qc["muta"]:
            warn(f"{st['nome']}: stazione senza velocità valida da oltre 24 h (o mai ricevuta)")
        if qc["ore_fuori_scala"]:
            warn(f"{st['nome']}: {len(qc['ore_fuori_scala'])} ore con valori fuori scala")
        if qc["sensore_costante_sospetto"]:
            warn(f"{st['nome']}: {len(qc['sensore_costante_sospetto'])} sequenze costanti da controllare")
        fcs, extras = {}, {}
        for model in cfg["models"] + vcfg.get("confronti", []):
            key = model_key(model["label"])
            days = int(model.get("giorni_anticipo", vcfg["giorni_anticipo"]))
            fc = archivio.read_forecast(root, code, key, days)
            if not offline:
                try:
                    fc, complete = update_forecast(root, st, model, today - timedelta(days=int(ccfg["sovrapposizione_giorni"])), today - timedelta(days=1), days)
                    if not complete:
                        warn(f"{st['nome']} {model['label']}: risposta incompleta al giorno 0; dati precedenti conservati")
                except Exception as e:
                    warn(f"{st['nome']} {model['label']}: previsioni non aggiornate ({e}); uso della cache")
            # Tutti i modelli configurati restano nel confronto anche se vuoti.
            (extras if model in vcfg.get("confronti", []) else fcs)[key] = fc
        windows = {}
        for length in (30, 365):
            start, stop = timestamp(today - timedelta(days=length)), timestamp(today)
            obs = {t: v for t, v in observed.items() if start <= t < stop}
            rows = evaluate(obs, fcs, int(vcfg["giorni_anticipo"]), float(vcfg["vento_minimo_direzione_kn"]))
            for model in vcfg.get("confronti", []):
                key, ref = model_key(model["label"]), model_key(model["riferimento"])
                if ref in fcs:
                    rows += compare(obs, (key, extras[key]), (ref, fcs[ref]), int(model["giorni_anticipo"]), float(vcfg["vento_minimo_direzione_kn"]))
            valid = sum(v.get("speed") is not None and v.get("dir") is not None for v in obs.values())
            common = {str(d): next((r["n"] for r in rows if r["giorno"] == d and r["campione"] == "comune"
                                   and r["settore"] is None and not r.get("confronto")), 0)
                      for d in range(int(vcfg["giorni_anticipo"]) + 1)}
            if not any(common.values()):
                warn(f"{st['nome']}: nessuna ora comune ai modelli nella finestra di {length} giorni")
            windows[str(length)] = {"dal": start, "al_escluso": stop, "ore_attese": length * 24,
                                    "ore_valide": valid, "ore_comuni_per_anticipo": common, "punteggi": rows}
        result["stazioni"].append({"codice": code, "nome": st["nome"], "qualita": qc, "finestre": windows})
    if not offline:
        archivio.write_json(state_path, state)
    archivio.write_json(out / "giornaliero.json", result)
    report = summary(result)
    (out / "giornaliero.md").write_text(report, encoding="utf-8")
    if os.environ.get("GITHUB_STEP_SUMMARY"):
        with open(os.environ["GITHUB_STEP_SUMMARY"], "a", encoding="utf-8") as f:
            f.write(report)
    return result


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--data", type=Path, default=ROOT / "dati")
    ap.add_argument("--out", type=Path, default=ROOT / "dati" / "rapporti")
    ap.add_argument("--importa", type=Path, help="importa la cache in --data e termina, senza rete")
    ap.add_argument("--solo-cache", action="store_true")
    ap.add_argument("--ricarica-completa", action="store_true")
    ap.add_argument("--correzioni", type=Path, help="file operativo da conservare per la futura sorveglianza")
    args = ap.parse_args()
    cfg = load_config()
    if args.importa:
        print(json.dumps(archivio.import_cache(args.importa, args.data, cfg), ensure_ascii=False))
        return
    result = run(args.data, args.out, cfg, datetime.now(timezone.utc), args.solo_cache, args.ricarica_completa, args.correzioni)
    if not any(st["finestre"]["365"]["ore_valide"] for st in result["stazioni"]):
        annotate("error", "Raccolta senza dati", "nessuna ora osservata valida negli ultimi 365 giorni")
        raise SystemExit(1)


if __name__ == "__main__":
    main()
