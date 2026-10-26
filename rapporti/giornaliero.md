# Raccolta e verifica giornaliera

Data UTC: 2026-10-26

Quota stimata: 8280 chiamate/giorno (senza retry o corse manuali).

I punteggi sono dei modelli grezzi. Nessun riallenamento MOS.

Direzione -1 = non disponibile: conta fra le assenze, senza avvisi di fuori scala.

| Stazione | Ultima velocità UTC | Ritardo h | Direzione N/D nel campione QC | Ore valide 30 / 365 giorni |
|---|---|---|---|---|
| Genova - Porto Antico | 2026-10-21T10:00:00+00:00 | 121.6 | 300 | 600 / 8351 |
| La Spezia | 2026-10-21T10:00:00+00:00 | 121.6 | 363 | 587 / 8288 |
| Portovenere | 2026-10-21T10:00:00+00:00 | 121.6 | 322 | 596 / 8329 |
| Luni - Provasco | 2026-10-21T10:00:00+00:00 | 121.6 | 215 | 607 / 8436 |

## Avvisi

- Genova - Porto Antico: ARPAL non aggiornato (<urlopen error timed out>); uso della cache
- Genova - Porto Antico: stazione senza velocità valida da oltre 24 h (o mai ricevuta)
- La Spezia: ARPAL non aggiornato (<urlopen error timed out>); uso della cache
- La Spezia: stazione senza velocità valida da oltre 24 h (o mai ricevuta)
- Portovenere: ARPAL non aggiornato (<urlopen error timed out>); uso della cache
- Portovenere: stazione senza velocità valida da oltre 24 h (o mai ricevuta)
- Luni - Provasco: ARPAL non aggiornato (<urlopen error timed out>); uso della cache
- Luni - Provasco: stazione senza velocità valida da oltre 24 h (o mai ricevuta)

## Punteggi sul campione comune

| Stazione | Finestra | Modello | Giorno | N | MAE kn | MAE direzione ° |
|---|---|---|---|---|---|---|
| Genova - Porto Antico | 30 | icon2i | 0 | 600 | 1.66 | 20.6 |
| Genova - Porto Antico | 30 | iconeu | 0 | 600 | 1.91 | 27.6 |
| Genova - Porto Antico | 30 | ecmwf | 0 | 600 | 1.8 | 33.1 |
| Genova - Porto Antico | 30 | icon2i | 1 | 600 | 1.94 | 24.5 |
| Genova - Porto Antico | 30 | iconeu | 1 | 600 | 1.98 | 30.3 |
| Genova - Porto Antico | 30 | ecmwf | 1 | 600 | 1.84 | 38.1 |
| Genova - Porto Antico | 30 | icon2i | 2 | 600 | 2.04 | 21.8 |
| Genova - Porto Antico | 30 | iconeu | 2 | 600 | 1.99 | 35.1 |
| Genova - Porto Antico | 30 | ecmwf | 2 | 600 | 1.84 | 38.3 |
| Genova - Porto Antico | 30 | aromehd | 0 | 600 | 1.82 | 19.2 |
| Genova - Porto Antico | 30 | icon2i | 0 | 600 | 1.66 | 20.6 |
| Genova - Porto Antico | 30 | aromehd | 1 | 600 | 2.13 | 23.7 |
| Genova - Porto Antico | 30 | icon2i | 1 | 600 | 1.94 | 24.5 |
| Genova - Porto Antico | 365 | icon2i | 0 | 8351 | 1.78 | 22.3 |
| Genova - Porto Antico | 365 | iconeu | 0 | 8351 | 2.16 | 24.8 |
| Genova - Porto Antico | 365 | ecmwf | 0 | 8351 | 2.01 | 28.5 |
| Genova - Porto Antico | 365 | icon2i | 1 | 7261 | 1.88 | 22.5 |
| Genova - Porto Antico | 365 | iconeu | 1 | 7261 | 2.34 | 26.6 |
| Genova - Porto Antico | 365 | ecmwf | 1 | 7261 | 2.14 | 29.3 |
| Genova - Porto Antico | 365 | icon2i | 2 | 7127 | 1.98 | 23.9 |
| Genova - Porto Antico | 365 | iconeu | 2 | 7127 | 2.43 | 28.4 |
| Genova - Porto Antico | 365 | ecmwf | 2 | 7127 | 2.18 | 29.1 |
| Genova - Porto Antico | 365 | aromehd | 0 | 1750 | 1.7 | 25.6 |
| Genova - Porto Antico | 365 | icon2i | 0 | 1750 | 1.67 | 27.6 |
| Genova - Porto Antico | 365 | aromehd | 1 | 1743 | 1.95 | 29.1 |
| Genova - Porto Antico | 365 | icon2i | 1 | 1743 | 1.79 | 29.2 |
| La Spezia | 30 | icon2i | 0 | 587 | 1.78 | 29.4 |
| La Spezia | 30 | iconeu | 0 | 587 | 1.85 | 43.1 |
| La Spezia | 30 | ecmwf | 0 | 587 | 3.5 | 52.7 |
| La Spezia | 30 | icon2i | 1 | 587 | 1.81 | 35.4 |
| La Spezia | 30 | iconeu | 1 | 587 | 1.86 | 45.6 |
| La Spezia | 30 | ecmwf | 1 | 587 | 3.5 | 58.8 |
| La Spezia | 30 | icon2i | 2 | 587 | 1.77 | 37.9 |
| La Spezia | 30 | iconeu | 2 | 587 | 1.91 | 46.2 |
| La Spezia | 30 | ecmwf | 2 | 587 | 3.46 | 59.7 |
| La Spezia | 30 | aromehd | 0 | 587 | 1.75 | 29.2 |
| La Spezia | 30 | icon2i | 0 | 587 | 1.78 | 29.4 |
| La Spezia | 30 | aromehd | 1 | 587 | 1.76 | 31.9 |
| La Spezia | 30 | icon2i | 1 | 587 | 1.81 | 35.4 |
| La Spezia | 365 | icon2i | 0 | 8288 | 2.2 | 35.0 |
| La Spezia | 365 | iconeu | 0 | 8288 | 2.29 | 39.9 |
| La Spezia | 365 | ecmwf | 0 | 8288 | 3.95 | 53.6 |
| La Spezia | 365 | icon2i | 1 | 7194 | 2.12 | 38.5 |
| La Spezia | 365 | iconeu | 1 | 7194 | 2.23 | 40.5 |
| La Spezia | 365 | ecmwf | 1 | 7194 | 3.92 | 55.5 |
| La Spezia | 365 | icon2i | 2 | 7057 | 2.17 | 39.6 |
| La Spezia | 365 | iconeu | 2 | 7057 | 2.27 | 42.1 |
| La Spezia | 365 | ecmwf | 2 | 7057 | 3.96 | 57.8 |
| La Spezia | 365 | aromehd | 0 | 1736 | 1.83 | 32.0 |
| La Spezia | 365 | icon2i | 0 | 1736 | 2.02 | 35.8 |
| La Spezia | 365 | aromehd | 1 | 1728 | 1.87 | 38.4 |
| La Spezia | 365 | icon2i | 1 | 1728 | 2.0 | 39.5 |
| Portovenere | 30 | icon2i | 0 | 596 | 2.21 | 26.0 |
| Portovenere | 30 | iconeu | 0 | 596 | 2.93 | 30.2 |
| Portovenere | 30 | ecmwf | 0 | 596 | 2.46 | 50.5 |
| Portovenere | 30 | icon2i | 1 | 596 | 2.19 | 29.3 |
| Portovenere | 30 | iconeu | 1 | 596 | 2.95 | 31.5 |
| Portovenere | 30 | ecmwf | 1 | 596 | 2.46 | 48.2 |
| Portovenere | 30 | icon2i | 2 | 596 | 2.29 | 31.9 |
| Portovenere | 30 | iconeu | 2 | 596 | 2.96 | 32.4 |
| Portovenere | 30 | ecmwf | 2 | 596 | 2.34 | 47.3 |
| Portovenere | 30 | aromehd | 0 | 596 | 1.87 | 29.2 |
| Portovenere | 30 | icon2i | 0 | 596 | 2.21 | 26.0 |
| Portovenere | 30 | aromehd | 1 | 596 | 1.96 | 30.9 |
| Portovenere | 30 | icon2i | 1 | 596 | 2.19 | 29.3 |
| Portovenere | 365 | icon2i | 0 | 8329 | 2.29 | 33.1 |
| Portovenere | 365 | iconeu | 0 | 8329 | 2.83 | 37.2 |
| Portovenere | 365 | ecmwf | 0 | 8329 | 2.91 | 46.2 |
| Portovenere | 365 | icon2i | 1 | 7239 | 2.36 | 34.4 |
| Portovenere | 365 | iconeu | 1 | 7239 | 2.92 | 37.1 |
| Portovenere | 365 | ecmwf | 1 | 7239 | 2.88 | 46.5 |
| Portovenere | 365 | icon2i | 2 | 7092 | 2.39 | 35.6 |
| Portovenere | 365 | iconeu | 2 | 7092 | 2.94 | 38.5 |
| Portovenere | 365 | ecmwf | 2 | 7092 | 2.97 | 48.0 |
| Portovenere | 365 | aromehd | 0 | 1743 | 1.97 | 32.4 |
| Portovenere | 365 | icon2i | 0 | 1743 | 2.11 | 30.4 |
| Portovenere | 365 | aromehd | 1 | 1734 | 2.02 | 34.9 |
| Portovenere | 365 | icon2i | 1 | 1734 | 2.09 | 33.5 |
| Luni - Provasco | 30 | icon2i | 0 | 607 | 1.14 | 28.8 |
| Luni - Provasco | 30 | iconeu | 0 | 607 | 1.41 | 48.6 |
| Luni - Provasco | 30 | ecmwf | 0 | 607 | 1.63 | 47.1 |
| Luni - Provasco | 30 | icon2i | 1 | 607 | 1.19 | 31.2 |
| Luni - Provasco | 30 | iconeu | 1 | 607 | 1.44 | 48.9 |
| Luni - Provasco | 30 | ecmwf | 1 | 607 | 1.68 | 47.9 |
| Luni - Provasco | 30 | icon2i | 2 | 607 | 1.23 | 31.9 |
| Luni - Provasco | 30 | iconeu | 2 | 607 | 1.39 | 49.2 |
| Luni - Provasco | 30 | ecmwf | 2 | 607 | 1.59 | 46.1 |
| Luni - Provasco | 30 | aromehd | 0 | 607 | 1.42 | 32.2 |
| Luni - Provasco | 30 | icon2i | 0 | 607 | 1.14 | 28.8 |
| Luni - Provasco | 30 | aromehd | 1 | 607 | 1.46 | 30.3 |
| Luni - Provasco | 30 | icon2i | 1 | 607 | 1.19 | 31.2 |
| Luni - Provasco | 365 | icon2i | 0 | 8436 | 1.34 | 30.5 |
| Luni - Provasco | 365 | iconeu | 0 | 8436 | 1.51 | 44.2 |
| Luni - Provasco | 365 | ecmwf | 0 | 8436 | 2.03 | 52.2 |
| Luni - Provasco | 365 | icon2i | 1 | 7325 | 1.37 | 32.0 |
| Luni - Provasco | 365 | iconeu | 1 | 7325 | 1.53 | 45.6 |
| Luni - Provasco | 365 | ecmwf | 1 | 7325 | 2.01 | 51.6 |
| Luni - Provasco | 365 | icon2i | 2 | 7186 | 1.43 | 34.4 |
| Luni - Provasco | 365 | iconeu | 2 | 7186 | 1.61 | 48.5 |
| Luni - Provasco | 365 | ecmwf | 2 | 7186 | 2.02 | 53.2 |
| Luni - Provasco | 365 | aromehd | 0 | 1781 | 1.44 | 33.5 |
| Luni - Provasco | 365 | icon2i | 0 | 1781 | 1.16 | 30.0 |
| Luni - Provasco | 365 | aromehd | 1 | 1773 | 1.47 | 36.5 |
| Luni - Provasco | 365 | icon2i | 1 | 1773 | 1.13 | 31.8 |
