r"""Correzione statistica (MOS) di velocità, direzione e raffiche del vento, per stazione (fase 2).

Uso:
    python -m meteo.mos      # usa i file in dati/ scaricati da `python -m meteo.verifica`

Si conosce solo ciò che è noto al momento della previsione: velocità, direzione e raffica
PREVISTE e l'ora del giorno. Il settore che seleziona i coefficienti è quindi quello
previsto (rosa a 8 venti), mai quello osservato.

Velocità e raffica, per stazione x giorno di anticipo x insieme di modelli x settore s:
    \hat o = \beta_{s,0} + \sum_k \beta_{s,k} x_k
             + \beta_{s,a}\sin\tfrac{2\pi h}{24} + \beta_{s,b}\cos\tfrac{2\pi h}{24}
con x_k gli ingressi in nodi (le velocità previste dei modelli; per le raffiche anche le
loro raffiche previste) e h l'ora UTC (ciclo delle brezze). Ogni settore è tirato verso il
fit comune a tutti i settori (ridge):
    (X_s^T X_s + \lambda I)\,\beta_s = X_s^T y_s + \lambda\,\beta_{pool}
così un settore con poche ore resta vicino al comportamento medio.

Direzione: si sceglie da quali modelli prenderla (uno solo o la media dei loro vettori) e
se ruotarla. La rotazione per settore è la mediana degli scarti (che minimizza l'errore
assoluto medio, quello che si misura), smorzata se le ore sono poche:
    \Delta_s = \frac{n_s}{n_s + \lambda_{dir}}\,\operatorname{med}_i(\delta_i),
    \delta_i = d^o_i - d^f_i \in (-180°, 180°]
sulle sole ore con vento OSSERVATO sopra la soglia (come nella verifica).
Sono due scelte distinte, ciascuna sul proprio errore: la fonte della direzione in uscita (sull'errore
di direzione) e la fonte che assegna le ore ai settori dei coefficienti (sull'errore di velocità o di
raffica).

Validazione: si allena prima di [mos].test_dal e si misura dopo, su mesi mai visti, come se
il MOS fosse andato in produzione quel giorno. Le scelte (fonte della direzione, rotazione,
\lambda) si fanno sull'ultimo 20% del periodo di allenamento, mai sulla prova. L'incertezza
sul guadagno è un bootstrap a blocchi di un giorno (le ore vicine non sono indipendenti).
Il file operativo è allenato su tutto il periodo.

Contratto con la produzione: correzioni/mos.json (versione SCHEMA_VERSION)
    correzioni[]   una per stazione x modello x giorno di anticipo x grandezza ("vel" o "raf")
        ingressi   [[modello, "vel"|"raf"], ...] nell'ordine delle colonne di x
        fonte      modelli la cui direzione (media dei vettori) sceglie il settore dei coefficienti
        settori    {settore: coefficienti}; x = [1, ingressi..., sin(2πh/24), cos(2πh/24)]
        direzione  (solo "vel") {fonte, ruota, rotazione}: direzione corretta = direzione prevista dalla
                   fonte + rotazione[settore previsto dalla stessa fonte]
    valutazione[]  i punteggi sulla prova; documentazione, non serve per applicare
    apply_correction(corr, t, previsioni) (in correzione.py) applica una correzione, con
        previsioni = {modello: {"vel": nodi, "dir": gradi, "raf": nodi o None}}, t = unix UTC
Il dizionario che si valuta è lo stesso che finisce nel file: ciò che si misura è ciò che si pubblica.
"""
from __future__ import annotations

import json
import math
import random
import time
from datetime import date, datetime, timezone
from pathlib import Path

from .build import annotate, model_key
from .config import ROOT, load_config
from .correzione import SCHEMA_VERSION, apply_correction, features, predict_value, rotated_direction, source_wind
from .verifica import DATA, _write_csv, angle_diff, load_forecast, load_observed, scalar_scores, scores
from .wind import KNOT_MS, WIND_NAMES, wind_name

LAMBDA_DIR = 50.0  # ore equivalenti di "nessuna rotazione" nella mediana della direzione
POOL_RIDGE = 1e-3  # regolarizzazione minima del fit comune, solo per la stabilità numerica
COMBINED = "combinato"
NO_ROTATION = {name: 0.0 for name in WIND_NAMES}


# ---------------------------------------------------------------- algebra minima


def solve(a: list[list[float]], b: list[float]) -> list[float]:
    """Sistema lineare a x = b (eliminazione di Gauss con pivot parziale)."""
    n = len(b)
    m = [row[:] + [b[i]] for i, row in enumerate(a)]
    for c in range(n):
        p = max(range(c, n), key=lambda r: abs(m[r][c]))
        if abs(m[p][c]) < 1e-12:
            raise ValueError("sistema singolare")
        m[c], m[p] = m[p], m[c]
        for r in range(c + 1, n):
            k = m[r][c] / m[c][c]
            for j in range(c, n + 1):
                m[r][j] -= k * m[c][j]
    x = [0.0] * n
    for r in range(n - 1, -1, -1):
        x[r] = (m[r][n] - sum(m[r][j] * x[j] for j in range(r + 1, n))) / m[r][r]
    return x


def normal_equations(xs: list[list[float]], ys: list[float]) -> tuple[list[list[float]], list[float]]:
    """X^T X e X^T y: bastano a risolvere il ridge con qualsiasi \\lambda senza rileggere i dati."""
    k = len(xs[0])
    a = [[0.0] * k for _ in range(k)]
    b = [0.0] * k
    for x, y in zip(xs, ys):
        for i in range(k):
            xi = x[i]
            b[i] += xi * y
            row = a[i]
            for j in range(i, k):
                row[j] += xi * x[j]
    for i in range(k):
        for j in range(i):
            a[i][j] = a[j][i]
    return a, b


def add_equations(eqs: list) -> tuple[list[list[float]], list[float]]:
    """Somma di equazioni normali: i dati di gruppi disgiunti si sommano."""
    eqs = [e for e in eqs if e]
    k = len(eqs[0][1])
    a = [[sum(e[0][i][j] for e in eqs) for j in range(k)] for i in range(k)]
    b = [sum(e[1][i] for e in eqs) for i in range(k)]
    return a, b


def ridge_from_normal(a: list[list[float]], b: list[float], lam: float, prior: list[float]) -> list[float]:
    r"""\arg\min \|y - X\beta\|^2 + \lambda\|\beta - prior\|^2, dalle equazioni normali."""
    k = len(b)
    aa = [[a[i][j] + (lam if i == j else 0.0) for j in range(k)] for i in range(k)]
    return solve(aa, [b[i] + lam * prior[i] for i in range(k)])


def ridge(xs: list[list[float]], ys: list[float], lam: float, prior: list[float]) -> list[float]:
    return ridge_from_normal(*normal_equations(xs, ys), lam, prior)


# ---------------------------------------------------------------- dati, in nodi


def _kn(x: float | None) -> float | None:
    return None if x is None else x / KNOT_MS


def forecast_kn(rec: dict) -> dict:
    return {"vel": rec["speed"] / KNOT_MS, "dir": rec["dir"], "raf": _kn(rec.get("gust"))}


def observed_kn(rec: dict) -> dict:
    return {"vel": _kn(rec["speed"]), "dir": rec["dir"], "raf": _kn(rec.get("gust"))}


def build_samples(observed: dict[int, dict], forecasts: dict[str, dict[int, dict]], quantity: str) -> list[dict]:
    """Ore con osservato e previsione di TUTTI i modelli dati (quindi stesse ore per ogni modello).

    quantity è la grandezza da prevedere, "vel" o "raf": per "raf" servono anche la raffica
    osservata e quelle previste.
    """
    out = []
    for t in sorted(observed):
        o = observed_kn(observed[t])
        if o["vel"] is None or o["dir"] is None or o[quantity] is None:
            continue
        if any(t not in fc for fc in forecasts.values()):
            continue
        fc = {m: forecast_kn(f[t]) for m, f in forecasts.items()}
        if any(w[quantity] is None for w in fc.values()):
            continue
        out.append({"t": t, "fc": fc, "obs": o})
    return out


# ---------------------------------------------------------------- vento: fonte, settore, direzione


def direction_sources(models: list[str]) -> list[list[str]]:
    """Fonti candidate della direzione: ogni modello da solo, la media di tutti, la media dei due ICON."""
    sources = [[m] for m in models]
    if len(models) > 1:
        sources.append(list(models))
    icon = [m for m in models if m.startswith("icon")]
    if 1 < len(icon) < len(models):
        sources.append(icon)
    return sources


def shrunk_median(values: list[float]) -> float:
    """Mediana smorzata verso 0 quando i dati sono pochi: med · n / (n + \\lambda_dir)."""
    if not values:
        return 0.0
    v = sorted(values)
    n = len(v)
    med = v[n // 2] if n % 2 else (v[n // 2 - 1] + v[n // 2]) / 2
    return med * n / (n + LAMBDA_DIR)


def sector_rotation(samples: list[dict], fonte: list[str], min_dir_kn: float) -> dict[str, float]:
    """Rotazione per settore previsto, sulle ore con vento osservato >= soglia."""
    deltas: dict[str, list[float]] = {name: [] for name in WIND_NAMES}
    for s in samples:
        if s["obs"]["vel"] < min_dir_kn:
            continue
        _, d = source_wind(fonte, s["fc"])
        deltas[wind_name(d)].append(angle_diff(s["obs"]["dir"], d))
    return {name: round(shrunk_median(v), 3) for name, v in deltas.items()}


def direction_mae(samples: list[dict], direction, min_dir_kn: float) -> float:
    errs = [abs(angle_diff(direction(s), s["obs"]["dir"])) for s in samples if s["obs"]["vel"] >= min_dir_kn]
    return sum(errs) / len(errs) if errs else math.inf


def choose_direction(inner: list[dict], valid: list[dict], models: list[str], min_dir_kn: float) -> tuple[list[str], bool]:
    """Fonte della direzione e rotazione sì/no: quella con meno errore in validazione.

    A parità vince la prima (ICON-2I, senza rotazione).
    """
    best = None
    for fonte in direction_sources(models):
        rotation = sector_rotation(inner, fonte, min_dir_kn)
        for ruota in (False, True):
            rot = rotation if ruota else NO_ROTATION
            mae = direction_mae(valid, lambda s: rotated_direction(fonte, rot, s["fc"]), min_dir_kn)
            if best is None or mae < best[0]:
                best = (mae, fonte, ruota)
    return best[1], best[2]


# ---------------------------------------------------------------- regressione per settore


def make_spec(quantity: str, models: list[str]) -> dict:
    """Che cosa si corregge e con quali ingressi."""
    qs = ("vel",) if quantity == "vel" else ("vel", "raf")
    return {"grandezza": quantity, "modelli": models, "ingressi": [[m, q] for m in models for q in qs]}


def sector_stats(train: list[dict], spec: dict, fonte: list[str]) -> dict:
    """Equazioni normali per settore (previsto, dalla `fonte`) e su tutte le ore."""
    groups: dict[str, tuple[list, list]] = {name: ([], []) for name in WIND_NAMES}
    for s in train:
        name = wind_name(source_wind(fonte, s["fc"])[1])
        groups[name][0].append(features(spec["ingressi"], s["t"], s["fc"]))
        groups[name][1].append(s["obs"][spec["grandezza"]])
    eq = {name: normal_equations(xs, ys) if xs else None for name, (xs, ys) in groups.items()}
    return {"eq": eq, "pool": add_equations(list(eq.values())), "ore": {n: len(g[0]) for n, g in groups.items()}}


def fit(
    train: list[dict], spec: dict, fonte: list[str], lam: float, min_dir_kn: float,
    direzione: dict | None = None, stats: dict | None = None,
) -> dict:
    """Una correzione completa: serializzabile in JSON e applicabile con apply_correction.

    `fonte` assegna le ore ai settori dei coefficienti; `direzione` ({"fonte", "ruota"}, solo per la
    velocità) dice come ricavare la direzione in uscita.
    """
    stats = stats or sector_stats(train, spec, fonte)
    a, b = stats["pool"]
    pool = ridge_from_normal(a, b, POOL_RIDGE, [0.0] * len(b))
    settori = {name: ridge_from_normal(*eq, lam, pool) if eq else pool for name, eq in stats["eq"].items()}
    corr = {
        **spec,
        "fonte": fonte,
        "lambda": lam,
        "ore_settore": stats["ore"],
        "pool": [round(x, 6) for x in pool],
        "settori": {name: [round(x, 6) for x in beta] for name, beta in settori.items()},
    }
    if direzione:
        rot = sector_rotation(train, direzione["fonte"], min_dir_kn) if direzione["ruota"] else dict(NO_ROTATION)
        corr["direzione"] = {**direzione, "rotazione": rot}
    return corr


def train_correction(train: list[dict], spec: dict, lambdas: list[float], min_dir_kn: float) -> dict:
    """Allena una correzione. Due scelte distinte, sull'ultimo 20% (in ordine di tempo) dei dati di
    allenamento e ciascuna sul proprio errore:
    - fonte della direzione in uscita e rotazione sì/no, sull'errore di direzione (solo velocità);
    - fonte dei settori e \\lambda, sull'errore della grandezza corretta.
    Poi si riallena su tutti i dati."""
    q = spec["grandezza"]
    cut = int(len(train) * 0.8)
    inner, valid = train[:cut], train[cut:]
    direzione = None
    if q == "vel":
        dfonte, ruota = choose_direction(inner, valid, spec["modelli"], min_dir_kn)
        direzione = {"fonte": dfonte, "ruota": ruota}
    best = None
    for fonte in direction_sources(spec["modelli"]):
        stats = sector_stats(inner, spec, fonte)
        for lam in lambdas:
            corr = fit(inner, spec, fonte, lam, min_dir_kn, None, stats)
            mae = sum(abs(predict_value(corr, s["t"], s["fc"]) - s["obs"][q]) for s in valid) / len(valid)
            if best is None or mae < best[0]:
                best = (mae, fonte, lam)
    return fit(train, spec, best[1], best[2], min_dir_kn, direzione)


# ---------------------------------------------------------------- valutazione


def block_bootstrap(diffs: dict[int, list[float]], n: int = 2000, seed: int = 0) -> tuple[float | None, float | None]:
    """Intervallo al 95% della media di diffs ricampionando giorni interi."""
    days = list(diffs.values())
    if not days:
        return None, None
    rng = random.Random(seed)
    means = []
    for _ in range(n):
        pick = [rng.choice(days) for _ in days]
        means.append(sum(sum(d) for d in pick) / sum(len(d) for d in pick))
    means.sort()
    return round(means[int(0.025 * n)], 2), round(means[int(0.975 * n) - 1], 2)


def assess(corr: dict, test: list[dict], min_dir_kn: float) -> dict:
    """Grezzo (primo modello) contro correzione, sulle stesse ore di prova."""
    q, ref = corr["grandezza"], corr["modelli"][0]
    pred = [apply_correction(corr, s["t"], s["fc"]) for s in test]
    obs = [s["obs"][q] for s in test]
    raw = [s["fc"][ref][q] for s in test]
    got = [p[q] for p in pred]
    out: dict = {"n": len(test), "giorni": len({s["t"] // 86400 for s in test})}
    if q == "vel":
        o_pair = [{"speed": o, "dir": s["obs"]["dir"]} for o, s in zip(obs, test)]
        out["grezzo"] = scores([({"speed": r, "dir": s["fc"][ref]["dir"]}, o) for r, s, o in zip(raw, test, o_pair)], min_dir_kn)
        out["mos"] = scores([({"speed": g, "dir": p["dir"]}, o) for g, p, o in zip(got, pred, o_pair)], min_dir_kn)
        by_day: dict[int, list[float]] = {}
        for s, p in zip(test, pred):
            if s["obs"]["vel"] >= min_dir_kn:
                od = s["obs"]["dir"]
                by_day.setdefault(s["t"] // 86400, []).append(
                    abs(angle_diff(p["dir"], od)) - abs(angle_diff(s["fc"][ref]["dir"], od))
                )
        out["delta_mae_dir_ic95"] = list(block_bootstrap(by_day))
    else:
        out["grezzo"] = scalar_scores(raw, obs)
        out["mos"] = scalar_scores(got, obs)
    diffs: dict[int, list[float]] = {}
    for s, g, r, o in zip(test, got, raw, obs):
        diffs.setdefault(s["t"] // 86400, []).append(abs(g - o) - abs(r - o))
    out["guadagno_mae"] = round(1 - out["mos"]["mae"] / out["grezzo"]["mae"], 3)
    out["delta_mae_ic95"] = list(block_bootstrap(diffs))
    return out


# ---------------------------------------------------------------- resoconto


def _ci(ci: list | None) -> str:
    return "" if not ci or ci[0] is None else f"[{ci[0]:+}, {ci[1]:+}]"


def report(station: dict, rows: list[dict], labels: dict[str, str], test_dal: str) -> str:
    """Tabelle Markdown leggibili a terminale."""
    lines = [f"\n## {station['spot']} — {station['nome']} (prova dal {test_dal})\n"]
    vel = [r for r in rows if r["grandezza"] == "vel"]
    if vel:
        lines.append("Velocità e direzione (kn, gradi; ΔMAE = MOS − grezzo, IC95 a blocchi di un giorno):\n")
        lines.append("| modello | giorno | ore | MAE grezzo → MOS | ΔMAE IC95 | bias grezzo → MOS | MAE dir. grezzo → MOS | ΔMAE dir. IC95 | direzione da | settori da | λ |")
        lines.append("|---|---|---|---|---|---|---|---|---|---|---|")
        for r in vel:
            g, m = r["grezzo"], r["mos"]
            fonte = " + ".join(labels[k] for k in r["fonte_dir"]) + (" ruotata" if r["ruota"] else "")
            settori = " + ".join(labels[k] for k in r["fonte"])
            lines.append(
                f"| {labels[r['modello']]} | {r['giorno']} | {r['n']} | {g['mae']} → {m['mae']} | {_ci(r['delta_mae_ic95'])} "
                f"| {g['bias']:+} → {m['bias']:+} | {g['mae_dir']} → {m['mae_dir']} | {_ci(r['delta_mae_dir_ic95'])} | {fonte} | {settori} | {r['lambda']:g} |"
            )
    raf = [r for r in rows if r["grandezza"] == "raf"]
    if raf:
        lines.append("\nRaffiche (kn; grezzo = raffica prevista da ICON-2I, osservato = massimo orario ARPAL):\n")
        lines.append("| ingressi | giorno | ore | MAE grezzo → MOS | ΔMAE IC95 | bias grezzo → MOS | r grezzo → MOS | λ |")
        lines.append("|---|---|---|---|---|---|---|---|")
        for r in raf:
            g, m = r["grezzo"], r["mos"]
            lines.append(
                f"| {' + '.join(labels[k] for k in r['modelli'])} | {r['giorno']} | {r['n']} | {g['mae']} → {m['mae']} "
                f"| {_ci(r['delta_mae_ic95'])} | {g['bias']:+} → {m['bias']:+} | {g['r']} → {m['r']} | {r['lambda']:g} |"
            )
    return "\n".join(lines)


def criteria(results: list[dict]) -> list[str]:
    """Verdetti sintetici, da leggere insieme alle tabelle."""
    comb = [r for r in results if r["grandezza"] == "vel" and r["modello"] == COMBINED]
    gust = [r for r in results if r["grandezza"] == "raf"]
    out = []
    if comb:
        better = sum(r["mos"]["mae_dir"] <= r["grezzo"]["mae_dir"] for r in comb)
        sure = sum(r["delta_mae_dir_ic95"][1] is not None and r["delta_mae_dir_ic95"][1] < 0 for r in comb)
        out.append(f"Direzione del MOS combinato <= ICON-2I grezzo: {better}/{len(comb)} (stazione x giorno); con IC95 sotto zero: {sure}/{len(comb)}")
    for name in sorted({r["modello"] for r in gust}):
        part = [r for r in gust if r["modello"] == name]
        sure = sum(r["delta_mae_ic95"][1] is not None and r["delta_mae_ic95"][1] < 0 for r in part)
        out.append(f"MAE raffica ({name}) ridotto con IC95 sotto zero: {sure}/{len(part)}")
    return out


# ---------------------------------------------------------------- main


def run(out_dir: Path) -> dict:
    cfg = load_config()
    vcfg, mcfg = cfg["verifica"], cfg["mos"]
    days = int(vcfg["giorni_anticipo"])
    min_dir_kn = float(vcfg["vento_minimo_direzione_kn"])
    start = date.fromisoformat(vcfg["dal"])
    split = int(datetime.fromisoformat(mcfg["test_dal"]).replace(tzinfo=timezone.utc).timestamp())
    lambdas = [float(x) for x in mcfg["lambda"]]
    today = datetime.now(timezone.utc).date()

    keys = [model_key(m["label"]) for m in cfg["models"]]
    gust_models = [model_key(label) for label in mcfg["raffiche"]]
    labels = {model_key(m["label"]): m["label"] for m in cfg["models"]}
    labels[COMBINED] = "MOS combinato"
    sets = [(k, "vel", [k]) for k in keys] + [(COMBINED, "vel", keys), (gust_models[0], "raf", gust_models[:1])]
    if len(gust_models) > 1:
        sets.append(("+".join(gust_models), "raf", gust_models))

    results, corrections, stations, texts = [], [], [], []
    for st in vcfg["stazioni"]:
        observed = load_observed(st, start, today, None, offline=True)
        if not observed:
            annotate("warning", f"MOS {st['nome']} saltato", "nessun osservato in dati/: lancia prima meteo.verifica")
            continue
        fcs = {k: load_forecast(st, m, start, today, days, offline=True) for k, m in zip(keys, cfg["models"])}
        rows = []
        for d in range(days + 1):
            for name, q, models in sets:
                data = build_samples(observed, {m: fcs[m][d] for m in models}, q)
                train = [s for s in data if s["t"] < split]
                test = [s for s in data if s["t"] >= split]
                if len(train) < 500 or not test:
                    continue
                spec = make_spec(q, models)
                corr = train_correction(train, spec, lambdas, min_dir_kn)
                dirc = corr.get("direzione")
                rows.append({"stazione": st["codice"], "grandezza": q, "modello": name, "modelli": models, "giorno": d,
                             "ore_allenamento": len(train), "lambda": corr["lambda"], "fonte": corr["fonte"],
                             "fonte_dir": dirc["fonte"] if dirc else None, "ruota": dirc["ruota"] if dirc else None,
                             **assess(corr, test, min_dir_kn)})
                final = train_correction(data, spec, lambdas, min_dir_kn)  # operativo: tutto il periodo
                corrections.append({"stazione": st["codice"], "modello": name, "giorno": d, "ore_allenamento": len(data), **final})
        results += rows
        stations.append({k: st[k] for k in ("spot", "nome", "codice", "lat", "lon")})
        texts.append(report(st, rows, {**labels, "+".join(gust_models): "ICON-2I + ICON-EU"}, mcfg["test_dal"]))

    if not results:
        raise RuntimeError("nessun MOS allenato: servono i dati di meteo.verifica in dati/")

    out = {
        "versione": SCHEMA_VERSION,
        "generated": int(time.time()),
        "unita": "nodi; gradi da cui proviene il vento; tempi UTC",
        "formato": "x = [1, ingressi..., sin(2πh/24), cos(2πh/24)], h = ora UTC; valore = max(0, settori[settore] · x)",
        "test_dal": mcfg["test_dal"],
        "lambda_dir": LAMBDA_DIR,
        "modelli": labels,
        "stazioni": stations,
        "correzioni": corrections,
        "valutazione": results,
    }
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / "mos.json").write_text(json.dumps(out, ensure_ascii=False, separators=(",", ":")))
    cols = ["stazione", "grandezza", "modello", "giorno", "n", "giorni", "ore_allenamento", "lambda", "guadagno_mae"]
    header = cols + ["fonte_settori", "fonte_dir", "ruota", "dmae_lo", "dmae_hi", "mae_grezzo", "mae_mos", "bias_grezzo", "bias_mos",
                     "mae_dir_grezzo", "mae_dir_mos", "dmae_dir_lo", "dmae_dir_hi"]
    table = []
    for r in results:
        g, m, ci, cd = r["grezzo"], r["mos"], r["delta_mae_ic95"], r.get("delta_mae_dir_ic95", ["", ""])
        table.append([r[c] for c in cols] + ["+".join(r["fonte"]), "+".join(r["fonte_dir"]) if r["fonte_dir"] else "", "" if r["ruota"] is None else r["ruota"], ci[0], ci[1],
                                              g["mae"], m["mae"], g["bias"], m["bias"], g.get("mae_dir", ""), m.get("mae_dir", ""), cd[0], cd[1]])
    _write_csv(DATA / "mos_valutazione.csv", header, table)
    print("\n".join(texts))
    print("\n" + "\n".join(criteria(results)))
    print(f"\nFatto: {out_dir / 'mos.json'}, {DATA / 'mos_valutazione.csv'}")
    return out


def main() -> None:
    try:
        run(ROOT / "correzioni")
    except Exception as e:
        annotate("error", "MOS fallito", f"{type(e).__name__}: {e}")
        raise SystemExit(1)


if __name__ == "__main__":
    main()
