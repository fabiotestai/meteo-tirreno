# Archivio dati Vento Tirreno–Ligure

CSV mensili originali ARPAL e Open-Meteo in `dati/`; velocità in m/s, direzioni meteorologiche, tempi UTC.
Gli osservati ARPAL sono datati alla fine dell’ora. Le previsioni conservano `previous_dayN`.

Fonti: [ARPAL](https://www.arpal.liguria.it/) e [Open-Meteo](https://open-meteo.com/), attribuzione [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/).

`rapporti/` contiene controlli qualità e punteggi dei modelli grezzi su 30/365 giorni.
I valori fuori scala sono esclusi solo dal rapporto: i CSV originali restano disponibili.
Le sequenze costanti sono sospette, non automaticamente scartate.
Dati assenti nelle risposte successive vengono conservati e segnalati, poiché una risposta incompleta non dimostra la revoca di una misura.

`correzioni/mos.json` è la copia iniziale dei coefficienti operativi. Nessun riallenamento automatico ancora attivo.
`rapporti/coefficienti/` conserva i coefficienti per hash e `rapporti/registro_mos/` registra quando il job li ha letti.
Questo registro non certifica quali coefficienti fossero online nelle precedenti corse della mappa.

Il codice e i workflow sono nel ramo di sviluppo `passo-2-mos`. La schedulazione è ancora disattivata.
