# Raccolta e verifica giornaliera

Data UTC: 2026-10-24

Quota stimata: 8280 chiamate/giorno (senza retry o corse manuali).

I punteggi sono dei modelli grezzi. Nessun riallenamento MOS.

Direzione -1 = non disponibile: conta fra le assenze, senza avvisi di fuori scala.

| Stazione | Ultima velocità UTC | Ritardo h | Direzione N/D nel campione QC | Ore valide 30 / 365 giorni |
|---|---|---|---|---|
| Genova - Porto Antico | 2026-10-21T10:00:00+00:00 | 71.8 | 300 | 647 / 8399 |
| La Spezia | 2026-10-21T10:00:00+00:00 | 71.8 | 363 | 634 / 8336 |
| Portovenere | 2026-10-21T10:00:00+00:00 | 71.8 | 324 | 643 / 8375 |
| Luni - Provasco | 2026-10-21T10:00:00+00:00 | 71.8 | 215 | 653 / 8484 |

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
| Genova - Porto Antico | 30 | icon2i | 0 | 647 | 1.63 | 21.0 |
| Genova - Porto Antico | 30 | iconeu | 0 | 647 | 1.89 | 27.1 |
| Genova - Porto Antico | 30 | ecmwf | 0 | 647 | 1.8 | 32.7 |
| Genova - Porto Antico | 30 | icon2i | 1 | 647 | 1.9 | 24.4 |
| Genova - Porto Antico | 30 | iconeu | 1 | 647 | 1.94 | 29.4 |
| Genova - Porto Antico | 30 | ecmwf | 1 | 647 | 1.82 | 37.3 |
| Genova - Porto Antico | 30 | icon2i | 2 | 647 | 1.99 | 22.1 |
| Genova - Porto Antico | 30 | iconeu | 2 | 647 | 1.96 | 33.6 |
| Genova - Porto Antico | 30 | ecmwf | 2 | 647 | 1.81 | 37.6 |
| Genova - Porto Antico | 30 | aromehd | 0 | 647 | 1.78 | 19.1 |
| Genova - Porto Antico | 30 | icon2i | 0 | 647 | 1.63 | 21.0 |
| Genova - Porto Antico | 30 | aromehd | 1 | 647 | 2.07 | 23.5 |
| Genova - Porto Antico | 30 | icon2i | 1 | 647 | 1.9 | 24.4 |
| Genova - Porto Antico | 365 | icon2i | 0 | 8399 | 1.78 | 22.3 |
| Genova - Porto Antico | 365 | iconeu | 0 | 8399 | 2.16 | 24.8 |
| Genova - Porto Antico | 365 | ecmwf | 0 | 8399 | 2.01 | 28.7 |
| Genova - Porto Antico | 365 | icon2i | 1 | 7309 | 1.88 | 22.6 |
| Genova - Porto Antico | 365 | iconeu | 1 | 7309 | 2.34 | 26.7 |
| Genova - Porto Antico | 365 | ecmwf | 1 | 7309 | 2.13 | 29.4 |
| Genova - Porto Antico | 365 | icon2i | 2 | 7175 | 1.99 | 24.0 |
| Genova - Porto Antico | 365 | iconeu | 2 | 7175 | 2.43 | 28.5 |
| Genova - Porto Antico | 365 | ecmwf | 2 | 7175 | 2.17 | 29.2 |
| Genova - Porto Antico | 365 | aromehd | 0 | 1750 | 1.7 | 25.6 |
| Genova - Porto Antico | 365 | icon2i | 0 | 1750 | 1.67 | 27.6 |
| Genova - Porto Antico | 365 | aromehd | 1 | 1743 | 1.95 | 29.1 |
| Genova - Porto Antico | 365 | icon2i | 1 | 1743 | 1.79 | 29.2 |
| La Spezia | 30 | icon2i | 0 | 634 | 1.75 | 30.1 |
| La Spezia | 30 | iconeu | 0 | 634 | 1.82 | 41.4 |
| La Spezia | 30 | ecmwf | 0 | 634 | 3.43 | 53.7 |
| La Spezia | 30 | icon2i | 1 | 634 | 1.79 | 35.1 |
| La Spezia | 30 | iconeu | 1 | 634 | 1.83 | 43.9 |
| La Spezia | 30 | ecmwf | 1 | 634 | 3.42 | 58.2 |
| La Spezia | 30 | icon2i | 2 | 634 | 1.74 | 37.9 |
| La Spezia | 30 | iconeu | 2 | 634 | 1.9 | 44.6 |
| La Spezia | 30 | ecmwf | 2 | 634 | 3.38 | 59.0 |
| La Spezia | 30 | aromehd | 0 | 634 | 1.72 | 28.5 |
| La Spezia | 30 | icon2i | 0 | 634 | 1.75 | 30.1 |
| La Spezia | 30 | aromehd | 1 | 634 | 1.72 | 31.8 |
| La Spezia | 30 | icon2i | 1 | 634 | 1.79 | 35.1 |
| La Spezia | 365 | icon2i | 0 | 8336 | 2.21 | 35.3 |
| La Spezia | 365 | iconeu | 0 | 8336 | 2.29 | 39.9 |
| La Spezia | 365 | ecmwf | 0 | 8336 | 3.98 | 53.4 |
| La Spezia | 365 | icon2i | 1 | 7242 | 2.13 | 38.8 |
| La Spezia | 365 | iconeu | 1 | 7242 | 2.24 | 40.8 |
| La Spezia | 365 | ecmwf | 1 | 7242 | 3.95 | 55.3 |
| La Spezia | 365 | icon2i | 2 | 7105 | 2.18 | 39.8 |
| La Spezia | 365 | iconeu | 2 | 7105 | 2.28 | 42.5 |
| La Spezia | 365 | ecmwf | 2 | 7105 | 3.98 | 57.5 |
| La Spezia | 365 | aromehd | 0 | 1736 | 1.83 | 32.0 |
| La Spezia | 365 | icon2i | 0 | 1736 | 2.02 | 35.8 |
| La Spezia | 365 | aromehd | 1 | 1728 | 1.87 | 38.4 |
| La Spezia | 365 | icon2i | 1 | 1728 | 2.0 | 39.5 |
| Portovenere | 30 | icon2i | 0 | 643 | 2.2 | 26.3 |
| Portovenere | 30 | iconeu | 0 | 643 | 2.93 | 30.2 |
| Portovenere | 30 | ecmwf | 0 | 643 | 2.41 | 49.3 |
| Portovenere | 30 | icon2i | 1 | 643 | 2.18 | 29.4 |
| Portovenere | 30 | iconeu | 1 | 643 | 2.96 | 31.2 |
| Portovenere | 30 | ecmwf | 1 | 643 | 2.4 | 47.6 |
| Portovenere | 30 | icon2i | 2 | 643 | 2.27 | 31.5 |
| Portovenere | 30 | iconeu | 2 | 643 | 2.97 | 32.0 |
| Portovenere | 30 | ecmwf | 2 | 643 | 2.31 | 46.7 |
| Portovenere | 30 | aromehd | 0 | 643 | 1.85 | 29.0 |
| Portovenere | 30 | icon2i | 0 | 643 | 2.2 | 26.3 |
| Portovenere | 30 | aromehd | 1 | 643 | 1.95 | 30.9 |
| Portovenere | 30 | icon2i | 1 | 643 | 2.18 | 29.4 |
| Portovenere | 365 | icon2i | 0 | 8375 | 2.29 | 33.1 |
| Portovenere | 365 | iconeu | 0 | 8375 | 2.84 | 37.4 |
| Portovenere | 365 | ecmwf | 0 | 8375 | 2.94 | 46.2 |
| Portovenere | 365 | icon2i | 1 | 7285 | 2.37 | 34.4 |
| Portovenere | 365 | iconeu | 1 | 7285 | 2.93 | 37.5 |
| Portovenere | 365 | ecmwf | 1 | 7285 | 2.91 | 46.4 |
| Portovenere | 365 | icon2i | 2 | 7138 | 2.41 | 35.9 |
| Portovenere | 365 | iconeu | 2 | 7138 | 2.95 | 38.8 |
| Portovenere | 365 | ecmwf | 2 | 7138 | 3.0 | 48.0 |
| Portovenere | 365 | aromehd | 0 | 1743 | 1.97 | 32.4 |
| Portovenere | 365 | icon2i | 0 | 1743 | 2.11 | 30.4 |
| Portovenere | 365 | aromehd | 1 | 1734 | 2.02 | 34.9 |
| Portovenere | 365 | icon2i | 1 | 1734 | 2.09 | 33.5 |
| Luni - Provasco | 30 | icon2i | 0 | 653 | 1.1 | 29.3 |
| Luni - Provasco | 30 | iconeu | 0 | 653 | 1.39 | 48.4 |
| Luni - Provasco | 30 | ecmwf | 0 | 653 | 1.63 | 48.2 |
| Luni - Provasco | 30 | icon2i | 1 | 653 | 1.17 | 31.8 |
| Luni - Provasco | 30 | iconeu | 1 | 653 | 1.41 | 48.6 |
| Luni - Provasco | 30 | ecmwf | 1 | 653 | 1.68 | 49.4 |
| Luni - Provasco | 30 | icon2i | 2 | 653 | 1.2 | 32.1 |
| Luni - Provasco | 30 | iconeu | 2 | 653 | 1.36 | 49.6 |
| Luni - Provasco | 30 | ecmwf | 2 | 653 | 1.6 | 47.4 |
| Luni - Provasco | 30 | aromehd | 0 | 653 | 1.39 | 32.4 |
| Luni - Provasco | 30 | icon2i | 0 | 653 | 1.1 | 29.3 |
| Luni - Provasco | 30 | aromehd | 1 | 653 | 1.41 | 31.2 |
| Luni - Provasco | 30 | icon2i | 1 | 653 | 1.17 | 31.8 |
| Luni - Provasco | 365 | icon2i | 0 | 8484 | 1.34 | 30.6 |
| Luni - Provasco | 365 | iconeu | 0 | 8484 | 1.51 | 44.1 |
| Luni - Provasco | 365 | ecmwf | 0 | 8484 | 2.04 | 52.3 |
| Luni - Provasco | 365 | icon2i | 1 | 7373 | 1.37 | 32.1 |
| Luni - Provasco | 365 | iconeu | 1 | 7373 | 1.53 | 45.8 |
| Luni - Provasco | 365 | ecmwf | 1 | 7373 | 2.01 | 51.8 |
| Luni - Provasco | 365 | icon2i | 2 | 7234 | 1.43 | 34.8 |
| Luni - Provasco | 365 | iconeu | 2 | 7234 | 1.61 | 48.5 |
| Luni - Provasco | 365 | ecmwf | 2 | 7234 | 2.03 | 53.5 |
| Luni - Provasco | 365 | aromehd | 0 | 1781 | 1.44 | 33.5 |
| Luni - Provasco | 365 | icon2i | 0 | 1781 | 1.16 | 30.0 |
| Luni - Provasco | 365 | aromehd | 1 | 1773 | 1.47 | 36.5 |
| Luni - Provasco | 365 | icon2i | 1 | 1773 | 1.13 | 31.8 |
