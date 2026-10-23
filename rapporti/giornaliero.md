# Raccolta e verifica giornaliera

Data UTC: 2026-10-23

Quota stimata: 8280 chiamate/giorno (senza retry o corse manuali).

I punteggi sono dei modelli grezzi. Nessun riallenamento MOS.

Direzione -1 = non disponibile: conta fra le assenze, senza avvisi di fuori scala.

| Stazione | Ultima velocità UTC | Ritardo h | Direzione N/D nel campione QC | Ore valide 30 / 365 giorni |
|---|---|---|---|---|
| Genova - Porto Antico | 2026-10-21T10:00:00+00:00 | 48.6 | 301 | 669 / 8422 |
| La Spezia | 2026-10-21T10:00:00+00:00 | 48.6 | 365 | 658 / 8358 |
| Portovenere | 2026-10-21T10:00:00+00:00 | 48.6 | 324 | 665 / 8399 |
| Luni - Provasco | 2026-10-21T10:00:00+00:00 | 48.6 | 215 | 677 / 8508 |

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
| Genova - Porto Antico | 30 | icon2i | 0 | 669 | 1.62 | 20.8 |
| Genova - Porto Antico | 30 | iconeu | 0 | 669 | 1.87 | 27.1 |
| Genova - Porto Antico | 30 | ecmwf | 0 | 669 | 1.78 | 32.8 |
| Genova - Porto Antico | 30 | icon2i | 1 | 669 | 1.88 | 24.3 |
| Genova - Porto Antico | 30 | iconeu | 1 | 669 | 1.93 | 29.2 |
| Genova - Porto Antico | 30 | ecmwf | 1 | 669 | 1.8 | 37.2 |
| Genova - Porto Antico | 30 | icon2i | 2 | 669 | 1.98 | 22.1 |
| Genova - Porto Antico | 30 | iconeu | 2 | 669 | 1.94 | 33.3 |
| Genova - Porto Antico | 30 | ecmwf | 2 | 669 | 1.79 | 37.4 |
| Genova - Porto Antico | 30 | aromehd | 0 | 669 | 1.75 | 19.0 |
| Genova - Porto Antico | 30 | icon2i | 0 | 669 | 1.62 | 20.8 |
| Genova - Porto Antico | 30 | aromehd | 1 | 669 | 2.03 | 23.6 |
| Genova - Porto Antico | 30 | icon2i | 1 | 669 | 1.88 | 24.3 |
| Genova - Porto Antico | 365 | icon2i | 0 | 8422 | 1.78 | 22.4 |
| Genova - Porto Antico | 365 | iconeu | 0 | 8422 | 2.16 | 24.8 |
| Genova - Porto Antico | 365 | ecmwf | 0 | 8422 | 2.01 | 28.7 |
| Genova - Porto Antico | 365 | icon2i | 1 | 7332 | 1.89 | 22.6 |
| Genova - Porto Antico | 365 | iconeu | 1 | 7332 | 2.33 | 26.7 |
| Genova - Porto Antico | 365 | ecmwf | 1 | 7332 | 2.13 | 29.4 |
| Genova - Porto Antico | 365 | icon2i | 2 | 7198 | 1.99 | 24.1 |
| Genova - Porto Antico | 365 | iconeu | 2 | 7198 | 2.43 | 28.6 |
| Genova - Porto Antico | 365 | ecmwf | 2 | 7198 | 2.17 | 29.2 |
| Genova - Porto Antico | 365 | aromehd | 0 | 1750 | 1.7 | 25.6 |
| Genova - Porto Antico | 365 | icon2i | 0 | 1750 | 1.67 | 27.6 |
| Genova - Porto Antico | 365 | aromehd | 1 | 1743 | 1.95 | 29.1 |
| Genova - Porto Antico | 365 | icon2i | 1 | 1743 | 1.79 | 29.2 |
| La Spezia | 30 | icon2i | 0 | 658 | 1.73 | 30.2 |
| La Spezia | 30 | iconeu | 0 | 658 | 1.79 | 41.1 |
| La Spezia | 30 | ecmwf | 0 | 658 | 3.47 | 53.9 |
| La Spezia | 30 | icon2i | 1 | 658 | 1.77 | 34.9 |
| La Spezia | 30 | iconeu | 1 | 658 | 1.81 | 43.3 |
| La Spezia | 30 | ecmwf | 1 | 658 | 3.44 | 58.1 |
| La Spezia | 30 | icon2i | 2 | 658 | 1.73 | 37.5 |
| La Spezia | 30 | iconeu | 2 | 658 | 1.88 | 43.9 |
| La Spezia | 30 | ecmwf | 2 | 658 | 3.37 | 58.9 |
| La Spezia | 30 | aromehd | 0 | 658 | 1.71 | 28.5 |
| La Spezia | 30 | icon2i | 0 | 658 | 1.73 | 30.2 |
| La Spezia | 30 | aromehd | 1 | 658 | 1.71 | 31.8 |
| La Spezia | 30 | icon2i | 1 | 658 | 1.77 | 34.9 |
| La Spezia | 365 | icon2i | 0 | 8358 | 2.22 | 35.3 |
| La Spezia | 365 | iconeu | 0 | 8358 | 2.3 | 39.9 |
| La Spezia | 365 | ecmwf | 0 | 8358 | 3.99 | 53.4 |
| La Spezia | 365 | icon2i | 1 | 7264 | 2.14 | 38.8 |
| La Spezia | 365 | iconeu | 1 | 7264 | 2.25 | 40.8 |
| La Spezia | 365 | ecmwf | 1 | 7264 | 3.96 | 55.2 |
| La Spezia | 365 | icon2i | 2 | 7127 | 2.19 | 39.7 |
| La Spezia | 365 | iconeu | 2 | 7127 | 2.28 | 42.5 |
| La Spezia | 365 | ecmwf | 2 | 7127 | 4.0 | 57.4 |
| La Spezia | 365 | aromehd | 0 | 1736 | 1.83 | 32.0 |
| La Spezia | 365 | icon2i | 0 | 1736 | 2.02 | 35.8 |
| La Spezia | 365 | aromehd | 1 | 1728 | 1.87 | 38.4 |
| La Spezia | 365 | icon2i | 1 | 1728 | 2.0 | 39.5 |
| Portovenere | 30 | icon2i | 0 | 665 | 2.19 | 26.2 |
| Portovenere | 30 | iconeu | 0 | 665 | 2.89 | 30.1 |
| Portovenere | 30 | ecmwf | 0 | 665 | 2.46 | 49.5 |
| Portovenere | 30 | icon2i | 1 | 665 | 2.17 | 29.0 |
| Portovenere | 30 | iconeu | 1 | 665 | 2.93 | 31.0 |
| Portovenere | 30 | ecmwf | 1 | 665 | 2.43 | 47.7 |
| Portovenere | 30 | icon2i | 2 | 665 | 2.25 | 31.3 |
| Portovenere | 30 | iconeu | 2 | 665 | 2.94 | 31.9 |
| Portovenere | 30 | ecmwf | 2 | 665 | 2.31 | 46.7 |
| Portovenere | 30 | aromehd | 0 | 665 | 1.85 | 29.0 |
| Portovenere | 30 | icon2i | 0 | 665 | 2.19 | 26.2 |
| Portovenere | 30 | aromehd | 1 | 665 | 1.94 | 30.9 |
| Portovenere | 30 | icon2i | 1 | 665 | 2.17 | 29.0 |
| Portovenere | 365 | icon2i | 0 | 8399 | 2.3 | 33.2 |
| Portovenere | 365 | iconeu | 0 | 8399 | 2.84 | 37.4 |
| Portovenere | 365 | ecmwf | 0 | 8399 | 2.96 | 46.2 |
| Portovenere | 365 | icon2i | 1 | 7309 | 2.39 | 34.5 |
| Portovenere | 365 | iconeu | 1 | 7309 | 2.93 | 37.6 |
| Portovenere | 365 | ecmwf | 1 | 7309 | 2.93 | 46.5 |
| Portovenere | 365 | icon2i | 2 | 7162 | 2.42 | 36.0 |
| Portovenere | 365 | iconeu | 2 | 7162 | 2.95 | 38.9 |
| Portovenere | 365 | ecmwf | 2 | 7162 | 3.02 | 48.1 |
| Portovenere | 365 | aromehd | 0 | 1743 | 1.97 | 32.4 |
| Portovenere | 365 | icon2i | 0 | 1743 | 2.11 | 30.4 |
| Portovenere | 365 | aromehd | 1 | 1734 | 2.02 | 34.9 |
| Portovenere | 365 | icon2i | 1 | 1734 | 2.09 | 33.5 |
| Luni - Provasco | 30 | icon2i | 0 | 677 | 1.09 | 29.4 |
| Luni - Provasco | 30 | iconeu | 0 | 677 | 1.38 | 48.2 |
| Luni - Provasco | 30 | ecmwf | 0 | 677 | 1.61 | 47.7 |
| Luni - Provasco | 30 | icon2i | 1 | 677 | 1.16 | 31.7 |
| Luni - Provasco | 30 | iconeu | 1 | 677 | 1.4 | 48.3 |
| Luni - Provasco | 30 | ecmwf | 1 | 677 | 1.67 | 49.0 |
| Luni - Provasco | 30 | icon2i | 2 | 677 | 1.19 | 32.2 |
| Luni - Provasco | 30 | iconeu | 2 | 677 | 1.37 | 49.4 |
| Luni - Provasco | 30 | ecmwf | 2 | 677 | 1.58 | 47.1 |
| Luni - Provasco | 30 | aromehd | 0 | 677 | 1.39 | 32.3 |
| Luni - Provasco | 30 | icon2i | 0 | 677 | 1.09 | 29.4 |
| Luni - Provasco | 30 | aromehd | 1 | 677 | 1.39 | 31.2 |
| Luni - Provasco | 30 | icon2i | 1 | 677 | 1.16 | 31.7 |
| Luni - Provasco | 365 | icon2i | 0 | 8508 | 1.34 | 30.7 |
| Luni - Provasco | 365 | iconeu | 0 | 8508 | 1.51 | 44.0 |
| Luni - Provasco | 365 | ecmwf | 0 | 8508 | 2.04 | 52.4 |
| Luni - Provasco | 365 | icon2i | 1 | 7397 | 1.38 | 32.2 |
| Luni - Provasco | 365 | iconeu | 1 | 7397 | 1.54 | 45.7 |
| Luni - Provasco | 365 | ecmwf | 1 | 7397 | 2.02 | 51.9 |
| Luni - Provasco | 365 | icon2i | 2 | 7258 | 1.44 | 34.8 |
| Luni - Provasco | 365 | iconeu | 2 | 7258 | 1.62 | 48.4 |
| Luni - Provasco | 365 | ecmwf | 2 | 7258 | 2.03 | 53.5 |
| Luni - Provasco | 365 | aromehd | 0 | 1781 | 1.44 | 33.5 |
| Luni - Provasco | 365 | icon2i | 0 | 1781 | 1.16 | 30.0 |
| Luni - Provasco | 365 | aromehd | 1 | 1773 | 1.47 | 36.5 |
| Luni - Provasco | 365 | icon2i | 1 | 1773 | 1.13 | 31.8 |
