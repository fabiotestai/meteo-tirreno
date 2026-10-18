"""Prova di fattibilità del passo 3: le fonti dati rispondono da qui?

Uso:
    python -m meteo.fattibilita

Serve a sapere se il job giornaliero può girare su un runner GitHub (IP in
datacenter esteri) o se deve girare dal Mac. Per ogni fonte fa una richiesta
piccola ma vera, con gli stessi client della verifica, e riporta quanti dati
arrivano e quanto è recente l'ultimo:

    ARPAL archivio   ultimi 10 giorni orari di una stazione (sessione ASP + CSV)
    OMIRL            tabella del vento e grafici a 10 minuti delle stazioni
    Open-Meteo       previous runs di ICON-2I e ora dell'ultima corsa

Il ritardo dell'ultimo dato dice anche quanto può essere "fresco" il job
incrementale. Su GitHub Actions i risultati escono come annotazioni e come
tabella nel riepilogo della corsa. Esce con codice 1 se una fonte fallisce.
"""
from __future__ import annotations

import json
import os
import socket
import time
import traceback
import urllib.request
import xml.etree.ElementTree as ET
from datetime import date, datetime, timedelta, timezone

from . import arpal, openmeteo
from .build import annotate
from .config import load_config

OMIRL_API = "https://omirl.regione.liguria.it/Omirl/rest"
ICON_2I = "ICON-2I"


def _utc(t: float) -> str:
    return datetime.fromtimestamp(t, timezone.utc).strftime("%d/%m %H:%M UTC")


def _late(t: float) -> str:
    """Ritardo dell'ultimo dato rispetto ad adesso, in ore."""
    return f"{(time.time() - t) / 3600:.1f} h fa"


def _omirl(path: str) -> bytes:
    req = urllib.request.Request(f"{OMIRL_API}/{path}", headers={"User-Agent": openmeteo.USER_AGENT})
    with urllib.request.urlopen(req, timeout=60) as resp:
        return resp.read()


def omirl_series(xml: bytes) -> dict[str, list[tuple[int, float]]]:
    """Grafico OMIRL (XML) -> {nome della serie: [(unix, valore), ...]}.

    Ogni serie è una lista di <data> con due <item>: istante in millisecondi
    (UTC) e valore. Nel grafico "Vento" ci sono velocità, raffica e direzione.
    """
    out = {}
    for series in ET.fromstring(xml).iter("dataSeries"):
        points = []
        for d in series.iter("data"):
            items = d.findall("item")
            if len(items) == 2 and items[1].text:
                points.append((int(items[0].text) // 1000, float(items[1].text)))
        out[series.findtext("name") or "?"] = points
    return out


def check_arpal(stations: list[dict]) -> str:
    st = stations[0]
    end = date.today()
    start = max(end - timedelta(days=10), date(end.year, 1, 1))  # il portale vuole un solo anno
    t0 = time.time()
    data = arpal.Archive(timeout=120, retries=2).hourly(st["codice"], start, end)
    if not data:
        raise RuntimeError(f"nessun dato per {st['nome']} dal {start:%d/%m} al {end:%d/%m}")
    last = max(data)
    return f"{st['nome']}: {len(data)} ore in {time.time() - t0:.0f} s, ultima {_utc(last)} ({_late(last)})"


def check_omirl(stations: list[dict]) -> str:
    table = json.loads(_omirl("stations/sensorvalues/Vento"))
    codes = {r["code"] for r in table.get("tableRows", [])}
    parts = [f"tabella vento: {len(codes)} stazioni"]
    for st in stations:
        if st["omirl"] not in codes:
            raise RuntimeError(f"{st['nome']} ({st['omirl']}) assente dalla tabella del vento")
        series = omirl_series(_omirl(f"charts/{st['omirl']}/Vento"))
        speed = next((v for k, v in series.items() if k.lower().startswith("velocit")), [])
        if not speed:
            raise RuntimeError(f"{st['nome']}: grafico senza serie di velocità")
        last = max(t for t, _ in speed)
        parts.append(f"{st['omirl']} {len(speed)} valori, ultimo {_late(last)}")
    return "; ".join(parts)


def check_openmeteo(stations: list[dict], models: list[dict]) -> str:
    model = next(m for m in models if m["label"] == ICON_2I)
    st = stations[0]
    end = date.today() - timedelta(days=1)
    res = openmeteo.fetch_previous_runs(
        (st["lat"], st["lon"]), ["wind_speed_10m"], model["id"],
        (end - timedelta(days=2)).isoformat(), end.isoformat(), 2,
    )
    full = [sum(v is not None for v in res[d]["wind_speed_10m"]) for d in range(3)]
    if not any(full):
        raise RuntimeError("previous runs vuote")
    init = openmeteo.fetch_run_init(model["meta"])
    return f"{ICON_2I} previous runs ore valide (giorno 0/1/2): {full[0]}/{full[1]}/{full[2]}; ultima corsa {_utc(init)}"


def run() -> bool:
    cfg = load_config()
    stations = cfg["verifica"]["stazioni"]
    checks = [
        ("ARPAL archivio", lambda: check_arpal(stations)),
        ("OMIRL", lambda: check_omirl(stations)),
        ("Open-Meteo", lambda: check_openmeteo(stations, cfg["models"])),
    ]
    where = os.environ.get("RUNNER_NAME") or socket.gethostname()
    rows, ok = [], True
    for name, fn in checks:
        t0 = time.time()
        try:
            msg = fn()
            annotate("notice", f"{name} OK", msg)
            rows.append((name, "OK", msg))
        except Exception as e:  # una fonte che cade non ferma le altre
            ok = False
            msg = f"{type(e).__name__}: {e}"
            annotate("error", f"{name} FALLITO", f"{msg} (dopo {time.time() - t0:.0f} s)")
            traceback.print_exc()
            rows.append((name, "FALLITO", msg))
    summary = os.environ.get("GITHUB_STEP_SUMMARY")
    if summary:
        with open(summary, "a", encoding="utf-8") as f:
            f.write(f"## Prova di fattibilità ({where}, {_utc(time.time())})\n\n| Fonte | Esito | Dettaglio |\n|---|---|---|\n")
            for r in rows:
                f.write("| " + " | ".join(x.replace("|", "/") for x in r) + " |\n")
    return ok


def main() -> None:
    raise SystemExit(0 if run() else 1)


if __name__ == "__main__":
    main()
