"""Archivio storico ARPAL (portale "Ambiente in Liguria - Meteo"), solo libreria standard.

Il portale è un vecchio form ASP a frame: la stazione scelta resta in sessione
sul server, legata a un numero di richiesta (IdRichiesta) e al cookie. Il
client rifà gli stessi passi della pagina:

1. apre la sessione (frameset + frame "Tipo");
2. sceglie la stazione (frame "Punto", azione INSERISCI_TEMA);
3. chiede l'estrazione oraria in CSV; la risposta contiene il link al file
   generato, che poi si scarica.

Vincolo del portale: per i dati orari di una stazione l'intervallo deve stare
dentro lo stesso anno solare. Tutti gli orari sono UTC.

Ogni valore orario ARPAL copre l'intervallo [inizio, fine) e qui viene
datato all'istante di FINE, come si fa per le medie di vento (WMO).
"""
from __future__ import annotations

import calendar
import csv
import http.cookiejar
import io
import re
import time
import urllib.parse
import urllib.request
from datetime import date

BASE = "https://ambientepub.regione.liguria.it/SiraQualMeteo/script/"
USER_AGENT = "meteo-tirreno/0.1 (progetto personale)"

# Codici dei parametri nel portale
SPEED = "VVMDTACWAN"  # intensità media del vento nell'ora (m/s)
GUST = "VV00TACWAN"  # intensità massima del vento nell'ora (m/s)
DIRECTION = "DIRVWAN"  # direzione di provenienza prevalente (gradi da nord)
PARAMS = {SPEED: "speed", GUST: "gust", DIRECTION: "dir"}

# Il CSV riporta il parametro per nome, non per codice
_NAME_TO_KEY = {
    "INTENSITÀ MEDIA DEL VENTO": "speed",
    "INTENSITÀ MASSIMA DEL VENTO": "gust",
    "DIREZIONE DI PROVENIENZA DEL VENTO PREVALENTE": "dir",
}


def _unix(text: str) -> int:
    """'31/12/2025 23:00' (UTC) -> secondi unix."""
    d, h = text.strip().split(" ")
    day, month, year = (int(x) for x in d.split("/"))
    hour, minute = (int(x) for x in h.split(":"))
    return calendar.timegm((year, month, day, hour, minute, 0))


def _key_for(param_line: str) -> str | None:
    upper = param_line.upper()
    for name, key in _NAME_TO_KEY.items():
        if name in upper:
            return key
    return None


def parse_report(text: str) -> dict[int, dict[str, float]]:
    """CSV del portale -> {fine ora unix: {"speed": .., "gust": .., "dir": ..}}.

    Il file ha un blocco per parametro: righe "Stazione" e "Parametro", poi
    l'intestazione e i dati. Si tengono solo i valori marcati validi.
    """
    out: dict[int, dict[str, float]] = {}
    key = None
    for row in csv.reader(io.StringIO(text)):
        if not row or not row[0].strip():
            continue
        first = row[0].strip()
        if first == "Parametro":
            key = _key_for(row[1] if len(row) > 1 else "")
            continue
        if key is None or len(row) < 5 or not re.match(r"\d{2}/\d{2}/\d{4} ", first):
            continue
        value, valid = row[2].strip(), row[4].strip()
        if not value or not valid.upper().startswith("S"):  # "Sì" = dato valido
            continue
        out.setdefault(_unix(row[1]), {})[key] = float(value.replace(",", "."))
    return out


class Archive:
    """Una sessione sul portale; si può riusare per più stazioni in sequenza."""

    def __init__(self, timeout: int = 300, retries: int = 3):
        jar = http.cookiejar.CookieJar()
        self._op = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(jar))
        self._op.addheaders = [("User-Agent", USER_AGENT)]
        self.timeout = timeout
        self.retries = retries
        self._get("PubAccessoDatiMeteo.asp")
        self._get("PubAccessoDatiMeteo11.asp")

    def _get(self, page: str, data: dict | None = None) -> str:
        url = page if page.startswith("http") else BASE + page
        body = urllib.parse.urlencode(data).encode() if data else None
        for attempt in range(self.retries):
            try:
                with self._op.open(url, data=body, timeout=self.timeout) as resp:
                    return resp.read().decode("latin-1")
            except OSError:
                if attempt == self.retries - 1:
                    raise
                time.sleep(10 * (attempt + 1))
        raise RuntimeError("unreachable")

    def _select(self, code: str) -> str:
        page = self._get("PubAccessoDatiMeteo12.asp", {"TipoTema": "STAZIONE", "CodTema": "STAZIONE"})
        m = re.search(r"NAME=IdRichiesta VALUE=(\d+)", page)
        if not m:
            raise RuntimeError("ARPAL: numero di richiesta non trovato nella pagina")
        rid = m.group(1)
        common = {"IdRichiesta": rid, "IdRichiestaCarto": "", "CodTema": "STAZIONE"}
        self._get("PubAccessoDatiMeteo13.asp?" + urllib.parse.urlencode({"Frequenza": "HH", **common, "CodUbic": code}))
        self._get(
            "PubAccessoDatiMeteo12.asp",
            {"CodUbic": code, "Ubic": code, "Frequenza": "HH", "Azione": "INSERISCI_TEMA", **common},
        )
        return rid

    def hourly(self, code: str, start: date, end: date) -> dict[int, dict[str, float]]:
        """Vento orario di una stazione tra start ed end inclusi (stesso anno)."""
        if start.year != end.year:
            raise ValueError("il portale ARPAL accetta un solo anno per richiesta")
        rid = self._select(code)
        query = (
            f"CodParam={','.join(PARAMS)}&CodTema=STAZIONE&IdEstraz=DE&Frequenza=HH"
            f"&TipoOutput=XLS&Separatore=PV&IdRichiesta={rid}&IdRichiestaCarto="
            f"&DataIniz={start:%d/%m/%Y}&InizOra=00:00&DataFine={end:%d/%m/%Y}&FineOra=23:59"
        )
        page = self._get("PubAccessoDatiMeteoPost.asp?" + query)
        link = re.search(r'HREF="([^"]+/report/\d+\.csv)"', page)
        if not link:
            return {}  # nessun dato nel periodo
        return parse_report(self._get(link.group(1)))
