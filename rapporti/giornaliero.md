# Raccolta e verifica giornaliera

Data UTC: 2026-11-14

Quota stimata: 8280 chiamate/giorno (senza retry o corse manuali).

I punteggi sono dei modelli grezzi. Nessun riallenamento MOS.

Direzione -1 = non disponibile: conta fra le assenze, senza avvisi di fuori scala.

| Stazione | Ultima velocità UTC | Ritardo h | Direzione N/D nel campione QC | Ore valide 30 / 365 giorni |
|---|---|---|---|---|
| Genova - Porto Antico | 2026-11-14T10:00:00+00:00 | 2.5 | 303 | 708 / 8457 |
| La Spezia | 2026-11-14T10:00:00+00:00 | 2.5 | 358 | 698 / 8402 |
| Portovenere | 2026-11-14T10:00:00+00:00 | 2.5 | 313 | 712 / 8447 |
| Luni - Provasco | 2026-11-14T10:00:00+00:00 | 2.5 | 213 | 708 / 8547 |

## Avvisi

- Luni - Provasco ICON-2I: previsioni non aggiornate (<urlopen error _ssl.c:994: The handshake operation timed out>); uso della cache

## Punteggi sul campione comune

| Stazione | Finestra | Modello | Giorno | N | MAE kn | MAE direzione ° |
|---|---|---|---|---|---|---|
| Genova - Porto Antico | 30 | icon2i | 0 | 708 | 1.8 | 15.4 |
| Genova - Porto Antico | 30 | iconeu | 0 | 708 | 2.42 | 16.6 |
| Genova - Porto Antico | 30 | ecmwf | 0 | 708 | 2.41 | 22.3 |
| Genova - Porto Antico | 30 | icon2i | 1 | 708 | 2.1 | 16.8 |
| Genova - Porto Antico | 30 | iconeu | 1 | 708 | 2.6 | 15.5 |
| Genova - Porto Antico | 30 | ecmwf | 1 | 708 | 2.44 | 21.7 |
| Genova - Porto Antico | 30 | icon2i | 2 | 708 | 2.38 | 20.0 |
| Genova - Porto Antico | 30 | iconeu | 2 | 708 | 2.66 | 18.1 |
| Genova - Porto Antico | 30 | ecmwf | 2 | 708 | 2.56 | 22.1 |
| Genova - Porto Antico | 30 | aromehd | 0 | 708 | 2.13 | 14.3 |
| Genova - Porto Antico | 30 | icon2i | 0 | 708 | 1.8 | 15.4 |
| Genova - Porto Antico | 30 | aromehd | 1 | 708 | 2.23 | 17.7 |
| Genova - Porto Antico | 30 | icon2i | 1 | 708 | 2.1 | 16.8 |
| Genova - Porto Antico | 365 | icon2i | 0 | 8457 | 1.76 | 21.9 |
| Genova - Porto Antico | 365 | iconeu | 0 | 8457 | 2.17 | 24.2 |
| Genova - Porto Antico | 365 | ecmwf | 0 | 8457 | 2.05 | 28.1 |
| Genova - Porto Antico | 365 | icon2i | 1 | 7367 | 1.88 | 22.0 |
| Genova - Porto Antico | 365 | iconeu | 1 | 7367 | 2.35 | 25.7 |
| Genova - Porto Antico | 365 | ecmwf | 1 | 7367 | 2.17 | 28.7 |
| Genova - Porto Antico | 365 | icon2i | 2 | 7244 | 2.0 | 23.6 |
| Genova - Porto Antico | 365 | iconeu | 2 | 7244 | 2.46 | 27.4 |
| Genova - Porto Antico | 365 | ecmwf | 2 | 7244 | 2.22 | 28.4 |
| Genova - Porto Antico | 365 | aromehd | 0 | 2307 | 1.81 | 21.9 |
| Genova - Porto Antico | 365 | icon2i | 0 | 2307 | 1.69 | 23.7 |
| Genova - Porto Antico | 365 | aromehd | 1 | 2300 | 2.02 | 25.0 |
| Genova - Porto Antico | 365 | icon2i | 1 | 2300 | 1.83 | 24.5 |
| La Spezia | 30 | icon2i | 0 | 698 | 1.99 | 39.0 |
| La Spezia | 30 | iconeu | 0 | 698 | 2.02 | 35.3 |
| La Spezia | 30 | ecmwf | 0 | 698 | 4.12 | 45.5 |
| La Spezia | 30 | icon2i | 1 | 698 | 2.1 | 39.8 |
| La Spezia | 30 | iconeu | 1 | 698 | 2.12 | 40.5 |
| La Spezia | 30 | ecmwf | 1 | 698 | 4.38 | 48.9 |
| La Spezia | 30 | icon2i | 2 | 698 | 2.1 | 41.2 |
| La Spezia | 30 | iconeu | 2 | 698 | 2.14 | 37.6 |
| La Spezia | 30 | ecmwf | 2 | 698 | 4.33 | 48.2 |
| La Spezia | 30 | aromehd | 0 | 698 | 1.89 | 30.6 |
| La Spezia | 30 | icon2i | 0 | 698 | 1.99 | 39.0 |
| La Spezia | 30 | aromehd | 1 | 698 | 1.89 | 32.9 |
| La Spezia | 30 | icon2i | 1 | 698 | 2.1 | 39.8 |
| La Spezia | 365 | icon2i | 0 | 8402 | 2.19 | 35.4 |
| La Spezia | 365 | iconeu | 0 | 8402 | 2.28 | 39.8 |
| La Spezia | 365 | ecmwf | 0 | 8402 | 3.95 | 53.4 |
| La Spezia | 365 | icon2i | 1 | 7308 | 2.11 | 38.8 |
| La Spezia | 365 | iconeu | 1 | 7308 | 2.23 | 40.8 |
| La Spezia | 365 | ecmwf | 1 | 7308 | 3.94 | 55.3 |
| La Spezia | 365 | icon2i | 2 | 7182 | 2.16 | 39.7 |
| La Spezia | 365 | iconeu | 2 | 7182 | 2.25 | 41.9 |
| La Spezia | 365 | ecmwf | 2 | 7182 | 3.97 | 57.3 |
| La Spezia | 365 | aromehd | 0 | 2284 | 1.84 | 31.6 |
| La Spezia | 365 | icon2i | 0 | 2284 | 2.0 | 37.1 |
| La Spezia | 365 | aromehd | 1 | 2276 | 1.87 | 36.8 |
| La Spezia | 365 | icon2i | 1 | 2276 | 2.01 | 39.5 |
| Portovenere | 30 | icon2i | 0 | 712 | 2.59 | 30.2 |
| Portovenere | 30 | iconeu | 0 | 712 | 3.92 | 34.3 |
| Portovenere | 30 | ecmwf | 0 | 712 | 3.08 | 45.4 |
| Portovenere | 30 | icon2i | 1 | 712 | 2.81 | 32.6 |
| Portovenere | 30 | iconeu | 1 | 712 | 4.0 | 36.4 |
| Portovenere | 30 | ecmwf | 1 | 712 | 3.16 | 46.2 |
| Portovenere | 30 | icon2i | 2 | 712 | 3.02 | 34.7 |
| Portovenere | 30 | iconeu | 2 | 712 | 4.03 | 35.1 |
| Portovenere | 30 | ecmwf | 2 | 712 | 3.26 | 46.1 |
| Portovenere | 30 | aromehd | 0 | 712 | 2.43 | 34.3 |
| Portovenere | 30 | icon2i | 0 | 712 | 2.59 | 30.2 |
| Portovenere | 30 | aromehd | 1 | 712 | 2.67 | 31.5 |
| Portovenere | 30 | icon2i | 1 | 712 | 2.81 | 32.6 |
| Portovenere | 365 | icon2i | 0 | 8447 | 2.31 | 32.5 |
| Portovenere | 365 | iconeu | 0 | 8447 | 2.92 | 37.0 |
| Portovenere | 365 | ecmwf | 0 | 8447 | 2.92 | 45.5 |
| Portovenere | 365 | icon2i | 1 | 7357 | 2.4 | 33.8 |
| Portovenere | 365 | iconeu | 1 | 7357 | 3.03 | 37.2 |
| Portovenere | 365 | ecmwf | 1 | 7357 | 2.91 | 45.8 |
| Portovenere | 365 | icon2i | 2 | 7221 | 2.46 | 34.8 |
| Portovenere | 365 | iconeu | 2 | 7221 | 3.06 | 38.4 |
| Portovenere | 365 | ecmwf | 2 | 7221 | 3.0 | 46.9 |
| Portovenere | 365 | aromehd | 0 | 2301 | 2.12 | 32.5 |
| Portovenere | 365 | icon2i | 0 | 2301 | 2.23 | 30.0 |
| Portovenere | 365 | aromehd | 1 | 2292 | 2.21 | 33.7 |
| Portovenere | 365 | icon2i | 1 | 2292 | 2.29 | 32.6 |
| Luni - Provasco | 30 | icon2i | 0 | 685 | 1.54 | 32.4 |
| Luni - Provasco | 30 | iconeu | 0 | 685 | 1.65 | 46.7 |
| Luni - Provasco | 30 | ecmwf | 0 | 685 | 1.95 | 56.2 |
| Luni - Provasco | 30 | icon2i | 1 | 685 | 1.61 | 35.0 |
| Luni - Provasco | 30 | iconeu | 1 | 685 | 1.73 | 47.1 |
| Luni - Provasco | 30 | ecmwf | 1 | 685 | 2.01 | 59.8 |
| Luni - Provasco | 30 | icon2i | 2 | 685 | 1.79 | 32.0 |
| Luni - Provasco | 30 | iconeu | 2 | 685 | 1.78 | 44.6 |
| Luni - Provasco | 30 | ecmwf | 2 | 685 | 1.96 | 59.2 |
| Luni - Provasco | 30 | aromehd | 0 | 685 | 2.09 | 37.5 |
| Luni - Provasco | 30 | icon2i | 0 | 685 | 1.54 | 32.4 |
| Luni - Provasco | 30 | aromehd | 1 | 685 | 2.24 | 34.6 |
| Luni - Provasco | 30 | icon2i | 1 | 685 | 1.61 | 35.0 |
| Luni - Provasco | 365 | icon2i | 0 | 8524 | 1.36 | 31.0 |
| Luni - Provasco | 365 | iconeu | 0 | 8524 | 1.53 | 44.6 |
| Luni - Provasco | 365 | ecmwf | 0 | 8524 | 2.04 | 52.8 |
| Luni - Provasco | 365 | icon2i | 1 | 7413 | 1.39 | 32.8 |
| Luni - Provasco | 365 | iconeu | 1 | 7413 | 1.56 | 46.0 |
| Luni - Provasco | 365 | ecmwf | 1 | 7413 | 2.01 | 52.4 |
| Luni - Provasco | 365 | icon2i | 2 | 7285 | 1.46 | 34.6 |
| Luni - Provasco | 365 | iconeu | 2 | 7285 | 1.64 | 48.5 |
| Luni - Provasco | 365 | ecmwf | 2 | 7285 | 2.02 | 53.8 |
| Luni - Provasco | 365 | aromehd | 0 | 2311 | 1.6 | 34.8 |
| Luni - Provasco | 365 | icon2i | 0 | 2311 | 1.25 | 31.1 |
| Luni - Provasco | 365 | aromehd | 1 | 2303 | 1.67 | 36.8 |
| Luni - Provasco | 365 | icon2i | 1 | 2303 | 1.24 | 32.8 |
