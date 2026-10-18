# Vento Tirreno–Ligure

Mappa del vento stile Windy per Mar Ligure e alto Tirreno, online su
https://fabiotestai.github.io/meteo-tirreno/ (GitHub Pages, aggiornata da GitHub Actions ogni 3 ore).

## Chi ci lavora

Fabio: laureato in fisica, va in barca e conosce bene il vento della zona. Scrive in italiano.
Vuole le formule in notazione LaTeX, non in testo semplice. È anche un progetto da portfolio
per il passaggio a data analyst / data engineer, quindi il codice deve restare leggibile e motivato.

## Struttura

- `config.toml`: riquadro, passo griglia (0.2°), orizzonte 72 h, modelli, spot costieri.
- `meteo/openmeteo.py`: download JSON da Open-Meteo, solo libreria standard, 100 punti per richiesta.
- `meteo/wind.py`: u/v, nodi, Beaufort, nomi dei venti, interpolazione temporale.
- `meteo/build.py`: pipeline → `wind_<modello>.json`, `spots.json`, `meta.json`. `--demo` per dati sintetici senza rete.
- `web/index.html`: Leaflet 1.9.4 + canvas (campo colorato e particelle). Pane "wind" a z-index 350,
  etichette Esri a 450. Mappa di base Esri Dark Gray Canvas (nessuna chiave), fallback OpenStreetMap.
- `.github/workflows/aggiorna.yml`: test → build → deploy Pages.

## Regole che non vanno rotte

- Nessuna dipendenza Python esterna: deve girare con `python -m meteo.build` su un runner pulito.
- L'interpolazione del vento si fa sulle componenti u, v, mai sulla direzione (350°→10° darebbe 180°).
- Direzione = da dove PROVIENE il vento (Libeccio 225°); le frecce nella pagina indicano dove va.
- Un modello che fallisce non deve bloccare gli altri; gli errori escono come annotazioni `::warning`/`::error`.
- Quota Open-Meteo gratuita ~10.000 chiamate/giorno (una per punto): oggi ~8.000. Ricalcolare prima
  di infittire la griglia o aggiungere modelli. L'API gratuita è solo per uso non commerciale.
- Test: `python -m unittest discover -s tests`, devono passare prima di ogni push.

## Stato (18 ottobre 2026)

Fatto: pipeline con ICON-2I, ICON-EU, ECMWF e onde; mappa con timeline a 30', confronto modelli al tocco,
schede degli 8 spot; deploy automatico funzionante con dati reali.

Prossime fasi, in ordine:
1. Osservazioni reali (stazioni ARPAL e MeteoHub, boe) e confronto previsione/osservato.
2. Correzione statistica (MOS) per zona, direzione del vento e situazione: Fabio corregge già a occhio
   gli errori di Windy sulla pioggia, l'idea è renderlo misurabile. Valutare gli archivi di previsioni
   passate di Open-Meteo per allenarla subito.
3. Download GRIB diretto (ICON-2I da MeteoHub, ECMWF open data) al posto di Open-Meteo.
4. Mappa onde e correnti (Copernicus Marine, WW3 MEDITA).
