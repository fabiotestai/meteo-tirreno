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
- `meteo/arpal.py`: archivio orario ARPAL (form ASP a frame, sessione con cookie; un anno per richiesta).
- `meteo/verifica.py`: fase 1, `python -m meteo.verifica` → osservati ARPAL + Open-Meteo previous runs
  alle coordinate delle stazioni, punteggi in `web/data/verifica.json` e `dati/verifica.csv`.
  Cache dei download in `dati/` (non versionata): anni e mesi conclusi non si riscaricano.
  `[[verifica.confronti]]` = modelli solo da verificare (AROME HD), testa a testa con un riferimento.
- `meteo/mos.py`: fase 2, `python -m meteo.mos` (dopo la verifica, usa solo `dati/`). Velocità e raffiche:
  regressione per stazione x giorno x insieme di modelli x settore PREVISTO, ridge verso il fit comune.
  Direzione: fonte (un modello o media dei vettori) e rotazione scelte in validazione. Prova su mesi mai visti
  (`[mos].test_dal`), con IC95 a blocchi di un giorno. Contratto con la produzione: `correzioni/mos.json`
  (versionato, `versione` 1) e `apply_correction()`; il dizionario valutato è quello pubblicato.

## Regole che non vanno rotte

- Nessuna dipendenza Python esterna: deve girare con `python -m meteo.build` su un runner pulito.
- L'interpolazione del vento si fa sulle componenti u, v, mai sulla direzione (350°→10° darebbe 180°).
- Direzione = da dove PROVIENE il vento (Libeccio 225°); le frecce nella pagina indicano dove va.
- Un modello che fallisce non deve bloccare gli altri; gli errori escono come annotazioni `::warning`/`::error`.
- Quota Open-Meteo gratuita ~10.000 chiamate/giorno (una per punto): oggi ~8.000. Ricalcolare prima
  di infittire la griglia o aggiungere modelli. L'API gratuita è solo per uso non commerciale.
- Confronti tra modelli o correzioni sempre sulle STESSE ore, scelte senza guardare la previsione (la
  direzione si misura solo con vento OSSERVATO sopra soglia). Filtrare sulla velocità prevista falsa il confronto:
  ci si era già cascati nella prima verifica.
- Test: `python -m unittest discover -s tests`, devono passare prima di ogni push.
- Sul Mac di Fabio il Python di sistema è 3.9: usare `~/tools/python-3.12/bin/python3` (build standalone).

## Stato (18 ottobre 2026)

Fatto: pipeline con ICON-2I, ICON-EU, ECMWF e onde; mappa con timeline a 30', confronto modelli al tocco,
schede degli 8 spot; deploy automatico funzionante con dati reali.
Fase 1 (verifica su Genova Porto Antico, La Spezia, Portovenere, Luni) e fase 2 (MOS v2: velocità, direzione,
raffiche) fatte e valutate in locale. ICON-2I è il modello grezzo migliore, anche sulla direzione. Su 6 mesi mai
visti (da 14/04/2026) il MOS riduce il MAE della velocità del 15–45% (IC95 sotto zero in 48/48 casi), quello
della direzione del combinato di 3–7° rispetto a ICON-2I grezzo, quello delle raffiche del 1–41%. I coefficienti
valgono ALLE STAZIONI (esposizione locale, ad es. la baia della Spezia ruota il vento): non sono trasferibili
agli spot al largo senza dirlo. Il MOS non è ancora applicato nella mappa né aggiornato dalla CI.
Buco noto: Open-Meteo non ha ICON-2I previous_day1/2 da metà aprile a metà giugno 2026.

Prossime fasi, in ordine:
1. Osservazioni reali (stazioni ARPAL e MeteoHub, boe) e confronto previsione/osservato.
2. Correzione statistica (MOS) per zona, direzione del vento e situazione: Fabio corregge già a occhio
   gli errori di Windy sulla pioggia, l'idea è renderlo misurabile. Valutare gli archivi di previsioni
   passate di Open-Meteo per allenarla subito.
3. Download GRIB diretto (ICON-2I da MeteoHub, ECMWF open data) al posto di Open-Meteo.
4. Mappa onde e correnti (Copernicus Marine, WW3 MEDITA).
