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
  Per gli spot con una stazione `in_mappa` (config) aggiunge a `spots.json` la serie MOS; se `correzioni/mos.json`
  manca, ha più di 60 giorni o la rete fallisce, il MOS sparisce dalla pagina e il resto procede.
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
- `meteo/correzione.py`: applicazione del MOS in produzione (legge `correzioni/mos.json`, nessuna dipendenza
  dall'allenamento). Giorno di anticipo d = ⌊(L+6)/24⌋, con L = ora − inizio dell'ultima corsa di ICON-2I
  (`fetch_run_init`); la corrispondenza con `previous_dayN` è stata MISURATA con le single runs di Open-Meteo.

## Regole che non vanno rotte

- Nessuna dipendenza Python esterna: deve girare con `python -m meteo.build` su un runner pulito.
- L'interpolazione del vento si fa sulle componenti u, v, mai sulla direzione (350°→10° darebbe 180°).
- Direzione = da dove PROVIENE il vento (Libeccio 225°); le frecce nella pagina indicano dove va.
- Un modello che fallisce non deve bloccare gli altri; gli errori escono come annotazioni `::warning`/`::error`.
- Quota Open-Meteo gratuita ~10.000 chiamate/giorno (una per punto): oggi ~8.100 (comprese le 9 delle tre stazioni del MOS). Ricalcolare prima
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
agli spot al largo senza dirlo. Il MOS è applicato nelle schede di Genova, Golfo della Spezia e Marina di Carrara (colonne MOS e Raff. MOS)
ma non è ancora pubblicato né aggiornato dalla CI: `correzioni/mos.json` si rigenera a mano (`meteo.verifica`,
poi `meteo.mos`) e scade dopo 60 giorni.
Buco noto: Open-Meteo non ha ICON-2I previous_day1/2 da metà aprile a metà giugno 2026.

## Piano dei prossimi passi (concordato il 18 ottobre 2026)

Fatti in locale, non ancora pubblicati: 1 (MOS v2 con raffiche e direzione) e 2 (MOS nelle schede dei 3 spot).
Prima di ogni passo nuovo Fabio vuole una conferma esplicita; push su `main` solo se lo dice (pubblica il sito).

3. Dati e verifica automatici:
   - prova di fattibilità: un workflow manuale che chiama ARPAL (archivio e OMIRL) e Open-Meteo da un runner GitHub.
     Rischio principale: i server regionali potrebbero bloccare gli IP esteri; piano B = aggiornamento dal Mac (launchd) con push.
     Fatto il 18/10/2026: `python -m meteo.fattibilita` + `.github/workflows/fattibilita.yml` (gira sul ramo `prova-fattibilita`,
     nessun deploy). Da rete italiana tutto OK: l'archivio ARPAL arriva fino a ~2 h prima (basta per l'incrementale),
     OMIRL (`/Omirl/rest/charts/<codice>/Vento`, XML, 7 giorni a 10', orari UTC) a pochi minuti; codici OMIRL in config.
     Esito dal runner GitHub (corsa 39113546715, 18/10/2026): tutto OK, stessi numeri che dall'Italia (ARPAL 247 ore in 6 s,
     ultima 2 h prima; OMIRL a 0,2 h; Open-Meteo completo). Nessun blocco degli IP esteri: il piano B dal Mac non serve.
     Una prova sola: il job giornaliero deve comunque gestire un ARPAL che non risponde (avviso, nessun blocco).
     Le azioni `checkout@v4`/`setup-python@v5` girano su Node 20, deprecato: aggiornarle anche in `aggiorna.yml`.
   - ramo `dati` con i CSV (osservati e previsioni, divisi per mese) e `correzioni/mos.json`;
   - job giornaliero: ARPAL incrementale (ultimi 10 giorni, sovrascrivendo) più ricarica mensile completa (correzioni a
     posteriori), controlli di qualità (valori fuori scala, sensore bloccato, stazione muta da più di 24 h), verifica su
     finestre di 30 e 365 giorni, MOS riallenato ogni mese su 12 mesi mobili;
   - sorveglianza: se il MOS fa peggio del grezzo per 14 giorni di fila, avviso e la mappa torna al grezzo;
   - nella pagina: ultime 48 h osservate contro previste e punteggi a 30 giorni.
4. Pioggia (idea di partenza: Fabio corregge a occhio gli errori di Windy sulla pioggia, renderlo misurabile): verifica su
   cumulate di 6 h con soglie 0,2, 1 e 5 mm. Con $a$ eventi previsti e osservati, $b$ falsi allarmi, $c$ eventi mancati:
   $POD=\frac{a}{a+c}$, $FAR=\frac{b}{a+b}$, $CSI=\frac{a}{a+b+c}$, bias di frequenza $\frac{a+b}{a+c}$. Probabilità con
   regressione logistica in Python puro (Brier score, diagramma di affidabilità). Pluviometri ARPAL: La Spezia, Portovenere,
   Luni; Genova Porto Antico NO. Chiedere a Fabio quali errori di Windy corregge (orario, quantità, posizione).
5. Toscana (Viareggio, Capraia, Portoferraio): serve un account MeteoHub gratuito (senza login l'archivio è solo 7-10 giorni;
   il token andrebbe in un secret di GitHub).

Dopo: download GRIB diretto (ICON-2I da MeteoHub, ECMWF open data; decodifica in Python puro o job separato con eccodes) e
mappa onde e correnti (Copernicus Marine, WW3 MEDITA). AROME HD da rivalutare a marzo 2027: in 72 giorni (ago–ott 2026) non
ha battuto ICON-2I.

## Come riprendere su un altro computer

1. `git clone https://github.com/fabiotestai/meteo-tirreno.git && cd meteo-tirreno && git checkout passo-2-mos`
   (finché il ramo non è unito a `main`; `main` pubblica il sito a ogni push).
2. Python 3.11 o più recente, nessun pacchetto da installare (`python3 --version`). Sul Mac di Fabio:
   `~/tools/python-3.12/bin/python3`.
3. `python3 -m unittest discover -s tests`: devono passare tutti (59 il 18/10/2026).
4. Fuori da git c'è `dati/` (~22 MB: cache di ARPAL e Open-Meteo, ignorata). O si copia la cartella dal vecchio PC, o si
   rigenera con `python3 -m meteo.verifica` (circa 15 minuti, ~350 richieste; ARPAL va chiamato da una rete normale: da IP
   cloud potrebbe essere bloccato).
5. `python3 -m meteo.mos` (circa 1 minuto) rigenera `correzioni/mos.json`: con gli stessi dati i coefficienti sono
   identici (cambia solo `generated`).
6. Per provare la pagina senza rete: `python3 -m meteo.build --demo`, poi `python3 -m http.server -d web 8000` e aprire
   http://localhost:8000 (la cartella `web/data/` è ignorata da git).
