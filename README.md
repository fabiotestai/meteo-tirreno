# Vento Tirreno–Ligure

Mappa del vento per il Mar Ligure e l'alto Tirreno, con vento animato, timeline a 30 minuti e confronto fra modelli. Usa gli stessi dati aperti che stanno dietro a Windy, con in più ICON-2I, il modello italiano a ~2 km che Windy non offre.

## Cosa fa

- **Mappa**: vento a 10 m colorato in nodi, particelle animate, timeline a passi di 30 minuti per 72 ore.
- **Tre modelli**: ICON-2I (ItaliaMeteo, ~2 km), ICON-EU (DWD, ~7 km), ECMWF IFS (open data 0.25°).
- **Tocco sulla mappa**: velocità, forza Beaufort e direzione col nome del vento (Libeccio, Maestrale…) per tutti e tre i modelli nello stesso punto.
- **Spot costieri**: tabella ogni 3 ore con i tre modelli affiancati, raffiche, pioggia e onda.
- **MOS** (Genova, Golfo della Spezia, Marina di Carrara): colonne di vento e raffica corrette statisticamente sulla stazione ARPAL vicina, con nella scheda quanto la correzione ha ridotto l'errore su mesi mai usati per allenare.

## Come funziona

```
config.toml          zona, passo griglia, modelli, spot
meteo/openmeteo.py   download JSON da Open-Meteo (solo libreria standard)
meteo/wind.py        componenti u/v, nodi, Beaufort, rosa dei venti, interpolazione a 30'
meteo/build.py       pipeline: scarica -> interpola -> scrive web/data/*.json
web/index.html       la mappa (Leaflet + animazione su canvas)
.github/workflows/   aggiornamento automatico ogni 3 ore + pubblicazione su GitHub Pages
tests/               test (python -m unittest discover -s tests)
```

Le uscite dei modelli sono orarie; la timeline a 30 minuti si ottiene interpolando le **componenti u e v**, mai la direzione (tra 350° e 10° la media della direzione darebbe 180°, il vento opposto).

Nessuna dipendenza esterna: basta Python 3.11 o più recente.

## Metterla online (una volta sola)

1. Crea su GitHub un repository nuovo (anche privato va bene per il codice, ma GitHub Pages gratuito richiede che sia **pubblico**).
2. Carica questi file mantenendo le cartelle.
3. In *Settings → Pages* scegli **Source: GitHub Actions**.
4. In *Actions* apri "Aggiorna previsioni" e premi **Run workflow**.

Dopo un paio di minuti la mappa è su `https://<utente>.github.io/<repository>/`, e si aggiorna da sola ogni 3 ore.

## Provarla sul computer

```bash
python -m meteo.build          # dati reali
python -m meteo.build --demo   # dati sintetici, senza rete (la pagina lo segnala con un avviso)
python -m http.server -d web 8000
```

Poi apri `http://localhost:8000`.

## Limiti da sapere

- **Licenza Open-Meteo**: l'API gratuita è per uso non commerciale. Per farne un prodotto a pagamento serve il loro piano commerciale oppure il download diretto dei GRIB dagli enti (ECMWF e ItaliaMeteo sono open data con attribuzione).
- **Quota**: ogni punto conta come chiamata; il limite gratuito è circa 10.000 al giorno. Con griglia 0.2°, 3 modelli e 8 aggiornamenti al giorno si usano circa 8.000 chiamate. Se infittisci la griglia o aggiungi modelli, riduci la frequenza nel workflow.
- **Primo test reale ancora da fare**: il codice è stato verificato con dati sintetici e test automatici, ma l'ambiente in cui è stato scritto non poteva raggiungere Open-Meteo. Al primo lancio controlla il log di "Scarica ed elabora".

## Prossime fasi

1. Osservazioni reali: stazioni ARPAL e MeteoHub, boe; confronto previsione/osservato.
2. Correzione statistica (MOS) per zona e direzione del vento, allenata anche sugli archivi di previsioni passate.
3. Download GRIB diretto (ICON-2I da MeteoHub, ECMWF open data a risoluzione piena) al posto di Open-Meteo.
4. Mappa delle onde e delle correnti (Copernicus Marine, WW3 MEDITA).

Dati: ItaliaMeteo–ARPAE (ICON-2I), DWD (ICON-EU), ECMWF (CC BY 4.0), tramite Open-Meteo. Mappa di base © OpenStreetMap, © CARTO.
