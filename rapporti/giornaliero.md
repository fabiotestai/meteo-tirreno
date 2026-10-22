# Raccolta e verifica giornaliera

Data UTC: 2026-10-22

Quota stimata: 8280 chiamate/giorno (senza retry o corse manuali).

I punteggi sono dei modelli grezzi. Nessun riallenamento MOS.

Direzione -1 = non disponibile: conta fra le assenze, senza avvisi di fuori scala.

| Stazione | Ultima velocità UTC | Ritardo h | Direzione N/D nel campione QC | Ore valide 30 / 365 giorni |
|---|---|---|---|---|
| Genova - Porto Antico | 2026-10-21T10:00:00+00:00 | 24.7 | 303 | 692 / 8444 |
| La Spezia | 2026-10-21T10:00:00+00:00 | 24.7 | 365 | 681 / 8382 |
| Portovenere | 2026-10-21T10:00:00+00:00 | 24.7 | 326 | 687 / 8421 |
| Luni - Provasco | 2026-10-21T10:00:00+00:00 | 24.7 | 217 | 701 / 8530 |

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
| Genova - Porto Antico | 30 | icon2i | 0 | 692 | 1.64 | 22.0 |
| Genova - Porto Antico | 30 | iconeu | 0 | 692 | 1.87 | 28.4 |
| Genova - Porto Antico | 30 | ecmwf | 0 | 692 | 1.8 | 33.9 |
| Genova - Porto Antico | 30 | icon2i | 1 | 692 | 1.88 | 25.0 |
| Genova - Porto Antico | 30 | iconeu | 1 | 692 | 1.92 | 30.4 |
| Genova - Porto Antico | 30 | ecmwf | 1 | 692 | 1.82 | 38.2 |
| Genova - Porto Antico | 30 | icon2i | 2 | 692 | 2.0 | 24.0 |
| Genova - Porto Antico | 30 | iconeu | 2 | 692 | 1.94 | 34.3 |
| Genova - Porto Antico | 30 | ecmwf | 2 | 692 | 1.81 | 38.3 |
| Genova - Porto Antico | 30 | aromehd | 0 | 692 | 1.78 | 20.3 |
| Genova - Porto Antico | 30 | icon2i | 0 | 692 | 1.64 | 22.0 |
| Genova - Porto Antico | 30 | aromehd | 1 | 692 | 2.05 | 24.6 |
| Genova - Porto Antico | 30 | icon2i | 1 | 692 | 1.88 | 25.0 |
| Genova - Porto Antico | 365 | icon2i | 0 | 8444 | 1.78 | 22.6 |
| Genova - Porto Antico | 365 | iconeu | 0 | 8444 | 2.16 | 24.8 |
| Genova - Porto Antico | 365 | ecmwf | 0 | 8444 | 2.01 | 28.7 |
| Genova - Porto Antico | 365 | icon2i | 1 | 7354 | 1.89 | 22.8 |
| Genova - Porto Antico | 365 | iconeu | 1 | 7354 | 2.33 | 26.7 |
| Genova - Porto Antico | 365 | ecmwf | 1 | 7354 | 2.13 | 29.7 |
| Genova - Porto Antico | 365 | icon2i | 2 | 7220 | 1.99 | 24.3 |
| Genova - Porto Antico | 365 | iconeu | 2 | 7220 | 2.43 | 28.5 |
| Genova - Porto Antico | 365 | ecmwf | 2 | 7220 | 2.17 | 29.3 |
| Genova - Porto Antico | 365 | aromehd | 0 | 1750 | 1.7 | 25.6 |
| Genova - Porto Antico | 365 | icon2i | 0 | 1750 | 1.67 | 27.6 |
| Genova - Porto Antico | 365 | aromehd | 1 | 1743 | 1.95 | 29.1 |
| Genova - Porto Antico | 365 | icon2i | 1 | 1743 | 1.79 | 29.2 |
| La Spezia | 30 | icon2i | 0 | 681 | 1.74 | 31.2 |
| La Spezia | 30 | iconeu | 0 | 681 | 1.8 | 41.4 |
| La Spezia | 30 | ecmwf | 0 | 681 | 3.46 | 54.3 |
| La Spezia | 30 | icon2i | 1 | 681 | 1.78 | 35.8 |
| La Spezia | 30 | iconeu | 1 | 681 | 1.81 | 43.6 |
| La Spezia | 30 | ecmwf | 1 | 681 | 3.44 | 58.2 |
| La Spezia | 30 | icon2i | 2 | 681 | 1.72 | 37.9 |
| La Spezia | 30 | iconeu | 2 | 681 | 1.88 | 44.7 |
| La Spezia | 30 | ecmwf | 2 | 681 | 3.35 | 60.3 |
| La Spezia | 30 | aromehd | 0 | 681 | 1.71 | 28.5 |
| La Spezia | 30 | icon2i | 0 | 681 | 1.74 | 31.2 |
| La Spezia | 30 | aromehd | 1 | 681 | 1.71 | 32.3 |
| La Spezia | 30 | icon2i | 1 | 681 | 1.78 | 35.8 |
| La Spezia | 365 | icon2i | 0 | 8382 | 2.21 | 35.3 |
| La Spezia | 365 | iconeu | 0 | 8382 | 2.3 | 40.0 |
| La Spezia | 365 | ecmwf | 0 | 8382 | 3.99 | 53.3 |
| La Spezia | 365 | icon2i | 1 | 7288 | 2.14 | 38.8 |
| La Spezia | 365 | iconeu | 1 | 7288 | 2.25 | 40.8 |
| La Spezia | 365 | ecmwf | 1 | 7288 | 3.96 | 55.2 |
| La Spezia | 365 | icon2i | 2 | 7151 | 2.19 | 39.7 |
| La Spezia | 365 | iconeu | 2 | 7151 | 2.28 | 42.5 |
| La Spezia | 365 | ecmwf | 2 | 7151 | 4.0 | 57.4 |
| La Spezia | 365 | aromehd | 0 | 1736 | 1.83 | 32.0 |
| La Spezia | 365 | icon2i | 0 | 1736 | 2.02 | 35.8 |
| La Spezia | 365 | aromehd | 1 | 1728 | 1.87 | 38.4 |
| La Spezia | 365 | icon2i | 1 | 1728 | 2.0 | 39.5 |
| Portovenere | 30 | icon2i | 0 | 687 | 2.16 | 26.4 |
| Portovenere | 30 | iconeu | 0 | 687 | 2.86 | 30.2 |
| Portovenere | 30 | ecmwf | 0 | 687 | 2.46 | 49.3 |
| Portovenere | 30 | icon2i | 1 | 687 | 2.14 | 29.2 |
| Portovenere | 30 | iconeu | 1 | 687 | 2.9 | 31.0 |
| Portovenere | 30 | ecmwf | 1 | 687 | 2.43 | 47.4 |
| Portovenere | 30 | icon2i | 2 | 687 | 2.24 | 31.0 |
| Portovenere | 30 | iconeu | 2 | 687 | 2.91 | 32.4 |
| Portovenere | 30 | ecmwf | 2 | 687 | 2.3 | 46.8 |
| Portovenere | 30 | aromehd | 0 | 687 | 1.85 | 29.1 |
| Portovenere | 30 | icon2i | 0 | 687 | 2.16 | 26.4 |
| Portovenere | 30 | aromehd | 1 | 687 | 1.94 | 30.9 |
| Portovenere | 30 | icon2i | 1 | 687 | 2.14 | 29.2 |
| Portovenere | 365 | icon2i | 0 | 8421 | 2.3 | 33.3 |
| Portovenere | 365 | iconeu | 0 | 8421 | 2.83 | 37.5 |
| Portovenere | 365 | ecmwf | 0 | 8421 | 2.96 | 46.3 |
| Portovenere | 365 | icon2i | 1 | 7331 | 2.39 | 34.6 |
| Portovenere | 365 | iconeu | 1 | 7331 | 2.93 | 37.6 |
| Portovenere | 365 | ecmwf | 1 | 7331 | 2.93 | 46.7 |
| Portovenere | 365 | icon2i | 2 | 7184 | 2.42 | 36.2 |
| Portovenere | 365 | iconeu | 2 | 7184 | 2.95 | 39.0 |
| Portovenere | 365 | ecmwf | 2 | 7184 | 3.02 | 48.2 |
| Portovenere | 365 | aromehd | 0 | 1743 | 1.97 | 32.4 |
| Portovenere | 365 | icon2i | 0 | 1743 | 2.11 | 30.4 |
| Portovenere | 365 | aromehd | 1 | 1734 | 2.02 | 34.9 |
| Portovenere | 365 | icon2i | 1 | 1734 | 2.09 | 33.5 |
| Luni - Provasco | 30 | icon2i | 0 | 701 | 1.08 | 28.9 |
| Luni - Provasco | 30 | iconeu | 0 | 701 | 1.37 | 48.1 |
| Luni - Provasco | 30 | ecmwf | 0 | 701 | 1.61 | 49.2 |
| Luni - Provasco | 30 | icon2i | 1 | 701 | 1.15 | 31.4 |
| Luni - Provasco | 30 | iconeu | 1 | 701 | 1.38 | 48.1 |
| Luni - Provasco | 30 | ecmwf | 1 | 701 | 1.67 | 49.6 |
| Luni - Provasco | 30 | icon2i | 2 | 701 | 1.18 | 31.7 |
| Luni - Provasco | 30 | iconeu | 2 | 701 | 1.35 | 49.3 |
| Luni - Provasco | 30 | ecmwf | 2 | 701 | 1.58 | 49.2 |
| Luni - Provasco | 30 | aromehd | 0 | 701 | 1.38 | 32.0 |
| Luni - Provasco | 30 | icon2i | 0 | 701 | 1.08 | 28.9 |
| Luni - Provasco | 30 | aromehd | 1 | 701 | 1.4 | 31.0 |
| Luni - Provasco | 30 | icon2i | 1 | 701 | 1.15 | 31.4 |
| Luni - Provasco | 365 | icon2i | 0 | 8530 | 1.34 | 30.7 |
| Luni - Provasco | 365 | iconeu | 0 | 8530 | 1.52 | 44.0 |
| Luni - Provasco | 365 | ecmwf | 0 | 8530 | 2.04 | 52.3 |
| Luni - Provasco | 365 | icon2i | 1 | 7419 | 1.38 | 32.2 |
| Luni - Provasco | 365 | iconeu | 1 | 7419 | 1.54 | 45.7 |
| Luni - Provasco | 365 | ecmwf | 1 | 7419 | 2.01 | 51.9 |
| Luni - Provasco | 365 | icon2i | 2 | 7280 | 1.44 | 34.7 |
| Luni - Provasco | 365 | iconeu | 2 | 7280 | 1.62 | 48.3 |
| Luni - Provasco | 365 | ecmwf | 2 | 7280 | 2.03 | 53.4 |
| Luni - Provasco | 365 | aromehd | 0 | 1781 | 1.44 | 33.5 |
| Luni - Provasco | 365 | icon2i | 0 | 1781 | 1.16 | 30.0 |
| Luni - Provasco | 365 | aromehd | 1 | 1773 | 1.47 | 36.5 |
| Luni - Provasco | 365 | icon2i | 1 | 1773 | 1.13 | 31.8 |
