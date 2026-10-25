# Raccolta e verifica giornaliera

Data UTC: 2026-10-25

Quota stimata: 8280 chiamate/giorno (senza retry o corse manuali).

I punteggi sono dei modelli grezzi. Nessun riallenamento MOS.

Direzione -1 = non disponibile: conta fra le assenze, senza avvisi di fuori scala.

| Stazione | Ultima velocità UTC | Ritardo h | Direzione N/D nel campione QC | Ore valide 30 / 365 giorni |
|---|---|---|---|---|
| Genova - Porto Antico | 2026-10-21T10:00:00+00:00 | 96.2 | 300 | 624 / 8375 |
| La Spezia | 2026-10-21T10:00:00+00:00 | 96.2 | 363 | 610 / 8312 |
| Portovenere | 2026-10-21T10:00:00+00:00 | 96.2 | 323 | 620 / 8352 |
| Luni - Provasco | 2026-10-21T10:00:00+00:00 | 96.2 | 215 | 631 / 8460 |

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
| Genova - Porto Antico | 30 | icon2i | 0 | 624 | 1.64 | 20.1 |
| Genova - Porto Antico | 30 | iconeu | 0 | 624 | 1.91 | 26.7 |
| Genova - Porto Antico | 30 | ecmwf | 0 | 624 | 1.82 | 32.2 |
| Genova - Porto Antico | 30 | icon2i | 1 | 624 | 1.92 | 23.8 |
| Genova - Porto Antico | 30 | iconeu | 1 | 624 | 1.96 | 29.2 |
| Genova - Porto Antico | 30 | ecmwf | 1 | 624 | 1.86 | 37.1 |
| Genova - Porto Antico | 30 | icon2i | 2 | 624 | 2.01 | 21.2 |
| Genova - Porto Antico | 30 | iconeu | 2 | 624 | 1.97 | 33.6 |
| Genova - Porto Antico | 30 | ecmwf | 2 | 624 | 1.85 | 37.3 |
| Genova - Porto Antico | 30 | aromehd | 0 | 624 | 1.8 | 18.7 |
| Genova - Porto Antico | 30 | icon2i | 0 | 624 | 1.64 | 20.1 |
| Genova - Porto Antico | 30 | aromehd | 1 | 624 | 2.1 | 23.0 |
| Genova - Porto Antico | 30 | icon2i | 1 | 624 | 1.92 | 23.8 |
| Genova - Porto Antico | 365 | icon2i | 0 | 8375 | 1.78 | 22.3 |
| Genova - Porto Antico | 365 | iconeu | 0 | 8375 | 2.16 | 24.8 |
| Genova - Porto Antico | 365 | ecmwf | 0 | 8375 | 2.01 | 28.5 |
| Genova - Porto Antico | 365 | icon2i | 1 | 7285 | 1.88 | 22.6 |
| Genova - Porto Antico | 365 | iconeu | 1 | 7285 | 2.34 | 26.7 |
| Genova - Porto Antico | 365 | ecmwf | 1 | 7285 | 2.13 | 29.3 |
| Genova - Porto Antico | 365 | icon2i | 2 | 7151 | 1.98 | 24.0 |
| Genova - Porto Antico | 365 | iconeu | 2 | 7151 | 2.43 | 28.5 |
| Genova - Porto Antico | 365 | ecmwf | 2 | 7151 | 2.17 | 29.1 |
| Genova - Porto Antico | 365 | aromehd | 0 | 1750 | 1.7 | 25.6 |
| Genova - Porto Antico | 365 | icon2i | 0 | 1750 | 1.67 | 27.6 |
| Genova - Porto Antico | 365 | aromehd | 1 | 1743 | 1.95 | 29.1 |
| Genova - Porto Antico | 365 | icon2i | 1 | 1743 | 1.79 | 29.2 |
| La Spezia | 30 | icon2i | 0 | 610 | 1.77 | 30.5 |
| La Spezia | 30 | iconeu | 0 | 610 | 1.84 | 42.4 |
| La Spezia | 30 | ecmwf | 0 | 610 | 3.47 | 53.1 |
| La Spezia | 30 | icon2i | 1 | 610 | 1.81 | 35.9 |
| La Spezia | 30 | iconeu | 1 | 610 | 1.86 | 44.9 |
| La Spezia | 30 | ecmwf | 1 | 610 | 3.46 | 58.3 |
| La Spezia | 30 | icon2i | 2 | 610 | 1.76 | 38.5 |
| La Spezia | 30 | iconeu | 2 | 610 | 1.91 | 45.1 |
| La Spezia | 30 | ecmwf | 2 | 610 | 3.43 | 59.1 |
| La Spezia | 30 | aromehd | 0 | 610 | 1.73 | 28.7 |
| La Spezia | 30 | icon2i | 0 | 610 | 1.77 | 30.5 |
| La Spezia | 30 | aromehd | 1 | 610 | 1.74 | 32.0 |
| La Spezia | 30 | icon2i | 1 | 610 | 1.81 | 35.9 |
| La Spezia | 365 | icon2i | 0 | 8312 | 2.2 | 35.1 |
| La Spezia | 365 | iconeu | 0 | 8312 | 2.29 | 39.8 |
| La Spezia | 365 | ecmwf | 0 | 8312 | 3.97 | 53.5 |
| La Spezia | 365 | icon2i | 1 | 7218 | 2.13 | 38.6 |
| La Spezia | 365 | iconeu | 1 | 7218 | 2.24 | 40.6 |
| La Spezia | 365 | ecmwf | 1 | 7218 | 3.94 | 55.4 |
| La Spezia | 365 | icon2i | 2 | 7081 | 2.17 | 39.6 |
| La Spezia | 365 | iconeu | 2 | 7081 | 2.27 | 42.3 |
| La Spezia | 365 | ecmwf | 2 | 7081 | 3.98 | 57.6 |
| La Spezia | 365 | aromehd | 0 | 1736 | 1.83 | 32.0 |
| La Spezia | 365 | icon2i | 0 | 1736 | 2.02 | 35.8 |
| La Spezia | 365 | aromehd | 1 | 1728 | 1.87 | 38.4 |
| La Spezia | 365 | icon2i | 1 | 1728 | 2.0 | 39.5 |
| Portovenere | 30 | icon2i | 0 | 620 | 2.22 | 26.6 |
| Portovenere | 30 | iconeu | 0 | 620 | 2.95 | 30.2 |
| Portovenere | 30 | ecmwf | 0 | 620 | 2.44 | 49.6 |
| Portovenere | 30 | icon2i | 1 | 620 | 2.21 | 29.8 |
| Portovenere | 30 | iconeu | 1 | 620 | 2.99 | 31.3 |
| Portovenere | 30 | ecmwf | 1 | 620 | 2.44 | 48.0 |
| Portovenere | 30 | icon2i | 2 | 620 | 2.3 | 32.1 |
| Portovenere | 30 | iconeu | 2 | 620 | 3.0 | 32.1 |
| Portovenere | 30 | ecmwf | 2 | 620 | 2.35 | 47.0 |
| Portovenere | 30 | aromehd | 0 | 620 | 1.87 | 29.5 |
| Portovenere | 30 | icon2i | 0 | 620 | 2.22 | 26.6 |
| Portovenere | 30 | aromehd | 1 | 620 | 1.97 | 31.4 |
| Portovenere | 30 | icon2i | 1 | 620 | 2.21 | 29.8 |
| Portovenere | 365 | icon2i | 0 | 8352 | 2.29 | 33.1 |
| Portovenere | 365 | iconeu | 0 | 8352 | 2.84 | 37.2 |
| Portovenere | 365 | ecmwf | 0 | 8352 | 2.92 | 46.2 |
| Portovenere | 365 | icon2i | 1 | 7262 | 2.37 | 34.4 |
| Portovenere | 365 | iconeu | 1 | 7262 | 2.94 | 37.3 |
| Portovenere | 365 | ecmwf | 1 | 7262 | 2.9 | 46.4 |
| Portovenere | 365 | icon2i | 2 | 7115 | 2.39 | 35.7 |
| Portovenere | 365 | iconeu | 2 | 7115 | 2.95 | 38.7 |
| Portovenere | 365 | ecmwf | 2 | 7115 | 2.98 | 48.0 |
| Portovenere | 365 | aromehd | 0 | 1743 | 1.97 | 32.4 |
| Portovenere | 365 | icon2i | 0 | 1743 | 2.11 | 30.4 |
| Portovenere | 365 | aromehd | 1 | 1734 | 2.02 | 34.9 |
| Portovenere | 365 | icon2i | 1 | 1734 | 2.09 | 33.5 |
| Luni - Provasco | 30 | icon2i | 0 | 631 | 1.12 | 29.5 |
| Luni - Provasco | 30 | iconeu | 0 | 631 | 1.4 | 48.8 |
| Luni - Provasco | 30 | ecmwf | 0 | 631 | 1.63 | 48.1 |
| Luni - Provasco | 30 | icon2i | 1 | 631 | 1.18 | 32.1 |
| Luni - Provasco | 30 | iconeu | 1 | 631 | 1.42 | 49.0 |
| Luni - Provasco | 30 | ecmwf | 1 | 631 | 1.68 | 49.5 |
| Luni - Provasco | 30 | icon2i | 2 | 631 | 1.21 | 32.6 |
| Luni - Provasco | 30 | iconeu | 2 | 631 | 1.37 | 49.6 |
| Luni - Provasco | 30 | ecmwf | 2 | 631 | 1.6 | 47.4 |
| Luni - Provasco | 30 | aromehd | 0 | 631 | 1.41 | 32.8 |
| Luni - Provasco | 30 | icon2i | 0 | 631 | 1.12 | 29.5 |
| Luni - Provasco | 30 | aromehd | 1 | 631 | 1.43 | 31.1 |
| Luni - Provasco | 30 | icon2i | 1 | 631 | 1.18 | 32.1 |
| Luni - Provasco | 365 | icon2i | 0 | 8460 | 1.34 | 30.5 |
| Luni - Provasco | 365 | iconeu | 0 | 8460 | 1.51 | 44.0 |
| Luni - Provasco | 365 | ecmwf | 0 | 8460 | 2.03 | 52.2 |
| Luni - Provasco | 365 | icon2i | 1 | 7349 | 1.37 | 32.0 |
| Luni - Provasco | 365 | iconeu | 1 | 7349 | 1.53 | 45.6 |
| Luni - Provasco | 365 | ecmwf | 1 | 7349 | 2.01 | 51.6 |
| Luni - Provasco | 365 | icon2i | 2 | 7210 | 1.43 | 34.5 |
| Luni - Provasco | 365 | iconeu | 2 | 7210 | 1.61 | 48.5 |
| Luni - Provasco | 365 | ecmwf | 2 | 7210 | 2.02 | 53.2 |
| Luni - Provasco | 365 | aromehd | 0 | 1781 | 1.44 | 33.5 |
| Luni - Provasco | 365 | icon2i | 0 | 1781 | 1.16 | 30.0 |
| Luni - Provasco | 365 | aromehd | 1 | 1773 | 1.47 | 36.5 |
| Luni - Provasco | 365 | icon2i | 1 | 1773 | 1.13 | 31.8 |
