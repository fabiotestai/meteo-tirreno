# Vento Tirreno–Ligure — istruzioni per agenti di codice

Mappa del vento stile Windy per Mar Ligure e alto Tirreno, online su
https://fabiotestai.github.io/meteo-tirreno/ (GitHub Pages, aggiornata da GitHub Actions ogni 3 ore).

Questo file vale per qualsiasi agente (Codex, Claude Code, altri). Se cambi regole o stato del
progetto, aggiorna questo file e non solo il codice.

## Chi ci lavora

Fabio: laureato in fisica, va in barca e conosce bene il vento della zona. Scrive in italiano:
rispondi in italiano, anche nei messaggi di commit. Formule in notazione LaTeX, non in testo semplice.
È anche un progetto da portfolio per il passaggio a data analyst / data engineer: il codice deve
restare leggibile, con commenti che spiegano il perché delle scelte.

## Struttura

- `config.toml`: riquadro, passo griglia (0.2°), orizzonte 72 h, modelli, spot costieri.
- `meteo/openmeteo.py`: download JSON da Open-Meteo, solo libreria standard, 100 punti per richiesta.
- `meteo/wind.py`: u/v, nodi, Beaufort, nomi dei venti, interpolazione temporale.
- `meteo/build.py`: pipeline → `wind_<modello>.json`, `spots.json`, `meta.json`. `--demo` per dati sintetici senza rete.
- `web/index.html`: Leaflet 1.9.4 + canvas (campo colorato e particelle). Pane "wind" a z-index 350,
  etichette Esri a 450. Mappa di base Esri Dark Gray Canvas (nessuna chiave), fallback OpenStreetMap.
- `.github/workflows/aggiorna.yml`: test → build → deploy Pages. Ogni push su `main` ripubblica il sito.

## Comandi

```bash
python -m unittest discover -s tests   # test: devono passare prima di ogni commit
python -m meteo.build --demo           # build con dati sintetici, senza rete
python -m meteo.build                  # build con dati reali (consuma quota Open-Meteo)
python -m http.server -d web 8000      # anteprima su http://localhost:8000
```

Sul PC Windows di Fabio usa `py` al posto di `python`.
In ambienti senza accesso a internet (per esempio un sandbox cloud) usa solo `--demo` e i test.

## Regole che non vanno rotte

- Nessuna dipendenza Python esterna: deve girare con `python -m meteo.build` su un runner pulito
  (Python 3.11+). Niente pip install, niente requirements.txt.
- L'interpolazione del vento si fa sulle componenti u, v, mai sulla direzione (350°→10° darebbe 180°).
- Direzione = da dove PROVIENE il vento (Libeccio 225°); le frecce nella pagina indicano dove va.
- Un modello che fallisce non deve bloccare gli altri; gli errori escono come annotazioni `::warning`/`::error`.
- Quota Open-Meteo gratuita ~10.000 chiamate/giorno (una per punto): oggi ~8.000. Ricalcolare prima
  di infittire la griglia o aggiungere modelli. L'API gratuita è solo per uso non commerciale.
- Non lanciare build con dati reali in loop o in test automatici: brucia quota.
- Non modificare il workflow di deploy senza dirlo esplicitamente nel riepilogo.

## Stato (19 ottobre 2026)

Fatto: pipeline con ICON-2I, ICON-EU, ECMWF e onde; mappa con timeline a 30', confronto modelli al tocco,
schede degli 8 spot; deploy automatico funzionante con dati reali.

Prossime fasi, in ordine:
1. Osservazioni reali (stazioni ARPAL e MeteoHub, boe) e confronto previsione/osservato.
2. Correzione statistica (MOS) per zona, direzione del vento e situazione: Fabio corregge già a occhio
   gli errori di Windy sulla pioggia, l'idea è renderlo misurabile. Valutare gli archivi di previsioni
   passate di Open-Meteo per allenarla subito.
3. Export GRIB per i software di navigazione (qtVlm, Expedition) e vista "campo di regata"
   (confronto modelli ora per ora su un punto).
4. Download GRIB diretto (ICON-2I da MeteoHub, ECMWF open data) al posto di Open-Meteo.
5. Mappa onde e correnti (Copernicus Marine, WW3 MEDITA).

Prima di iniziare una fase nuova, proponi un piano breve e aspetta conferma.
