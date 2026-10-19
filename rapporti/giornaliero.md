# Raccolta e verifica giornaliera

Data UTC: 2026-10-19

Quota stimata: 8280 chiamate/giorno (senza retry o corse manuali).

I punteggi sono dei modelli grezzi. Nessun riallenamento MOS.

| Stazione | Ultima velocità UTC | Ritardo h | Ore valide 30 / 365 giorni |
|---|---|---|---|
| Genova - Porto Antico | 2026-10-18T07:00:00+00:00 | 31.4 | 688 / 8436 |
| La Spezia | 2026-10-18T07:00:00+00:00 | 31.4 | 679 / 8380 |
| Portovenere | 2026-10-18T07:00:00+00:00 | 31.4 | 682 / 8416 |
| Luni - Provasco | 2026-10-18T07:00:00+00:00 | 31.4 | 697 / 8521 |

## Avvisi

- Genova - Porto Antico: stazione senza velocità valida da oltre 24 h (o mai ricevuta)
- Genova - Porto Antico: 308 ore con valori fuori scala
- La Spezia: stazione senza velocità valida da oltre 24 h (o mai ricevuta)
- La Spezia: 364 ore con valori fuori scala
- Portovenere: stazione senza velocità valida da oltre 24 h (o mai ricevuta)
- Portovenere: 328 ore con valori fuori scala
- Luni - Provasco: stazione senza velocità valida da oltre 24 h (o mai ricevuta)
- Luni - Provasco: 223 ore con valori fuori scala

## Punteggi sul campione comune

| Stazione | Finestra | Modello | Giorno | N | MAE kn | MAE direzione ° |
|---|---|---|---|---|---|---|
| Genova - Porto Antico | 30 | icon2i | 0 | 681 | 1.58 | 24.1 |
| Genova - Porto Antico | 30 | iconeu | 0 | 681 | 1.85 | 29.4 |
| Genova - Porto Antico | 30 | ecmwf | 0 | 681 | 1.72 | 34.4 |
| Genova - Porto Antico | 30 | icon2i | 1 | 681 | 1.63 | 24.1 |
| Genova - Porto Antico | 30 | iconeu | 1 | 681 | 1.86 | 32.0 |
| Genova - Porto Antico | 30 | ecmwf | 1 | 681 | 1.75 | 38.5 |
| Genova - Porto Antico | 30 | icon2i | 2 | 681 | 1.65 | 24.0 |
| Genova - Porto Antico | 30 | iconeu | 2 | 681 | 1.92 | 35.4 |
| Genova - Porto Antico | 30 | ecmwf | 2 | 681 | 1.75 | 37.8 |
| Genova - Porto Antico | 30 | aromehd | 0 | 681 | 1.64 | 22.6 |
| Genova - Porto Antico | 30 | icon2i | 0 | 681 | 1.58 | 24.1 |
| Genova - Porto Antico | 30 | aromehd | 1 | 681 | 1.91 | 25.0 |
| Genova - Porto Antico | 30 | icon2i | 1 | 681 | 1.63 | 24.1 |
| Genova - Porto Antico | 365 | icon2i | 0 | 8429 | 1.77 | 22.7 |
| Genova - Porto Antico | 365 | iconeu | 0 | 8429 | 2.16 | 24.9 |
| Genova - Porto Antico | 365 | ecmwf | 0 | 8429 | 2.01 | 28.7 |
| Genova - Porto Antico | 365 | icon2i | 1 | 7339 | 1.87 | 22.7 |
| Genova - Porto Antico | 365 | iconeu | 1 | 7339 | 2.33 | 26.7 |
| Genova - Porto Antico | 365 | ecmwf | 1 | 7339 | 2.13 | 29.6 |
| Genova - Porto Antico | 365 | icon2i | 2 | 7205 | 1.96 | 24.3 |
| Genova - Porto Antico | 365 | iconeu | 2 | 7205 | 2.43 | 28.5 |
| Genova - Porto Antico | 365 | ecmwf | 2 | 7205 | 2.17 | 29.2 |
| Genova - Porto Antico | 365 | aromehd | 0 | 1669 | 1.65 | 26.1 |
| Genova - Porto Antico | 365 | icon2i | 0 | 1669 | 1.63 | 28.1 |
| Genova - Porto Antico | 365 | aromehd | 1 | 1662 | 1.9 | 29.0 |
| Genova - Porto Antico | 365 | icon2i | 1 | 1662 | 1.68 | 28.6 |
| La Spezia | 30 | icon2i | 0 | 671 | 1.65 | 30.9 |
| La Spezia | 30 | iconeu | 0 | 671 | 1.64 | 41.1 |
| La Spezia | 30 | ecmwf | 0 | 671 | 2.95 | 53.5 |
| La Spezia | 30 | icon2i | 1 | 671 | 1.6 | 33.4 |
| La Spezia | 30 | iconeu | 1 | 671 | 1.62 | 42.6 |
| La Spezia | 30 | ecmwf | 1 | 671 | 2.96 | 58.3 |
| La Spezia | 30 | icon2i | 2 | 671 | 1.61 | 37.1 |
| La Spezia | 30 | iconeu | 2 | 671 | 1.69 | 44.7 |
| La Spezia | 30 | ecmwf | 2 | 671 | 2.92 | 60.2 |
| La Spezia | 30 | aromehd | 0 | 671 | 1.62 | 27.8 |
| La Spezia | 30 | icon2i | 0 | 671 | 1.65 | 30.9 |
| La Spezia | 30 | aromehd | 1 | 671 | 1.6 | 30.8 |
| La Spezia | 30 | icon2i | 1 | 671 | 1.6 | 33.4 |
| La Spezia | 365 | icon2i | 0 | 8372 | 2.21 | 35.3 |
| La Spezia | 365 | iconeu | 0 | 8372 | 2.29 | 40.1 |
| La Spezia | 365 | ecmwf | 0 | 8372 | 3.97 | 53.3 |
| La Spezia | 365 | icon2i | 1 | 7278 | 2.12 | 38.7 |
| La Spezia | 365 | iconeu | 1 | 7278 | 2.23 | 40.8 |
| La Spezia | 365 | ecmwf | 1 | 7278 | 3.94 | 55.2 |
| La Spezia | 365 | icon2i | 2 | 7141 | 2.18 | 39.9 |
| La Spezia | 365 | iconeu | 2 | 7141 | 2.26 | 42.4 |
| La Spezia | 365 | ecmwf | 2 | 7141 | 3.99 | 57.5 |
| La Spezia | 365 | aromehd | 0 | 1656 | 1.8 | 31.7 |
| La Spezia | 365 | icon2i | 0 | 1656 | 1.99 | 35.8 |
| La Spezia | 365 | aromehd | 1 | 1648 | 1.84 | 38.2 |
| La Spezia | 365 | icon2i | 1 | 1648 | 1.94 | 38.8 |
| Portovenere | 30 | icon2i | 0 | 674 | 2.01 | 24.2 |
| Portovenere | 30 | iconeu | 0 | 674 | 2.69 | 30.3 |
| Portovenere | 30 | ecmwf | 0 | 674 | 2.18 | 42.9 |
| Portovenere | 30 | icon2i | 1 | 674 | 2.0 | 25.8 |
| Portovenere | 30 | iconeu | 1 | 674 | 2.7 | 30.7 |
| Portovenere | 30 | ecmwf | 1 | 674 | 2.16 | 42.4 |
| Portovenere | 30 | icon2i | 2 | 674 | 2.07 | 26.3 |
| Portovenere | 30 | iconeu | 2 | 674 | 2.73 | 33.0 |
| Portovenere | 30 | ecmwf | 2 | 674 | 2.05 | 41.9 |
| Portovenere | 30 | aromehd | 0 | 674 | 1.8 | 26.2 |
| Portovenere | 30 | icon2i | 0 | 674 | 2.01 | 24.2 |
| Portovenere | 30 | aromehd | 1 | 674 | 1.82 | 29.0 |
| Portovenere | 30 | icon2i | 1 | 674 | 2.0 | 25.8 |
| Portovenere | 365 | icon2i | 0 | 8408 | 2.3 | 33.4 |
| Portovenere | 365 | iconeu | 0 | 8408 | 2.83 | 37.8 |
| Portovenere | 365 | ecmwf | 0 | 8408 | 2.94 | 46.2 |
| Portovenere | 365 | icon2i | 1 | 7318 | 2.38 | 34.4 |
| Portovenere | 365 | iconeu | 1 | 7318 | 2.92 | 37.7 |
| Portovenere | 365 | ecmwf | 1 | 7318 | 2.91 | 46.7 |
| Portovenere | 365 | icon2i | 2 | 7171 | 2.41 | 35.9 |
| Portovenere | 365 | iconeu | 2 | 7171 | 2.94 | 39.1 |
| Portovenere | 365 | ecmwf | 2 | 7171 | 3.0 | 48.2 |
| Portovenere | 365 | aromehd | 0 | 1660 | 1.96 | 31.3 |
| Portovenere | 365 | icon2i | 0 | 1660 | 2.06 | 29.8 |
| Portovenere | 365 | aromehd | 1 | 1651 | 1.99 | 34.5 |
| Portovenere | 365 | icon2i | 1 | 1651 | 2.04 | 32.5 |
| Luni - Provasco | 30 | icon2i | 0 | 689 | 0.99 | 30.1 |
| Luni - Provasco | 30 | iconeu | 0 | 689 | 1.22 | 48.4 |
| Luni - Provasco | 30 | ecmwf | 0 | 689 | 1.51 | 48.4 |
| Luni - Provasco | 30 | icon2i | 1 | 689 | 0.99 | 30.9 |
| Luni - Provasco | 30 | iconeu | 1 | 689 | 1.17 | 48.1 |
| Luni - Provasco | 30 | ecmwf | 1 | 689 | 1.55 | 47.4 |
| Luni - Provasco | 30 | icon2i | 2 | 689 | 0.99 | 32.2 |
| Luni - Provasco | 30 | iconeu | 2 | 689 | 1.2 | 50.9 |
| Luni - Provasco | 30 | ecmwf | 2 | 689 | 1.52 | 47.9 |
| Luni - Provasco | 30 | aromehd | 0 | 689 | 1.21 | 30.9 |
| Luni - Provasco | 30 | icon2i | 0 | 689 | 0.99 | 30.1 |
| Luni - Provasco | 30 | aromehd | 1 | 689 | 1.15 | 32.4 |
| Luni - Provasco | 30 | icon2i | 1 | 689 | 0.99 | 30.9 |
| Luni - Provasco | 365 | icon2i | 0 | 8513 | 1.34 | 30.8 |
| Luni - Provasco | 365 | iconeu | 0 | 8513 | 1.52 | 44.0 |
| Luni - Provasco | 365 | ecmwf | 0 | 8513 | 2.03 | 52.3 |
| Luni - Provasco | 365 | icon2i | 1 | 7402 | 1.37 | 32.1 |
| Luni - Provasco | 365 | iconeu | 1 | 7402 | 1.53 | 45.7 |
| Luni - Provasco | 365 | ecmwf | 1 | 7402 | 2.01 | 51.7 |
| Luni - Provasco | 365 | icon2i | 2 | 7263 | 1.43 | 34.9 |
| Luni - Provasco | 365 | iconeu | 2 | 7263 | 1.61 | 48.4 |
| Luni - Provasco | 365 | ecmwf | 2 | 7263 | 2.02 | 53.4 |
| Luni - Provasco | 365 | aromehd | 0 | 1698 | 1.38 | 33.1 |
| Luni - Provasco | 365 | icon2i | 0 | 1698 | 1.13 | 30.4 |
| Luni - Provasco | 365 | aromehd | 1 | 1690 | 1.39 | 37.2 |
| Luni - Provasco | 365 | icon2i | 1 | 1690 | 1.08 | 31.7 |
