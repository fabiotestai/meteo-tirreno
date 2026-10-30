# Raccolta e verifica giornaliera

Data UTC: 2026-10-30

Quota stimata: 8280 chiamate/giorno (senza retry o corse manuali).

I punteggi sono dei modelli grezzi. Nessun riallenamento MOS.

Direzione -1 = non disponibile: conta fra le assenze, senza avvisi di fuori scala.

| Stazione | Ultima velocità UTC | Ritardo h | Direzione N/D nel campione QC | Ore valide 30 / 365 giorni |
|---|---|---|---|---|
| Genova - Porto Antico | 2026-10-30T10:00:00+00:00 | 1.7 | 302 | 710 / 8458 |
| La Spezia | 2026-10-30T10:00:00+00:00 | 1.7 | 368 | 692 / 8392 |
| Portovenere | 2026-10-30T10:00:00+00:00 | 1.7 | 325 | 706 / 8435 |
| Luni - Provasco | 2026-10-30T10:00:00+00:00 | 1.7 | 213 | 715 / 8547 |

## Avvisi

- Portovenere ICON-2I: previsioni non aggiornate (Expecting value: line 1 column 1 (char 0)); uso della cache
- Portovenere AROME HD: previsioni non aggiornate (Expecting value: line 1 column 1 (char 0)); uso della cache

## Punteggi sul campione comune

| Stazione | Finestra | Modello | Giorno | N | MAE kn | MAE direzione ° |
|---|---|---|---|---|---|---|
| Genova - Porto Antico | 30 | icon2i | 0 | 710 | 1.71 | 20.7 |
| Genova - Porto Antico | 30 | iconeu | 0 | 710 | 1.89 | 24.7 |
| Genova - Porto Antico | 30 | ecmwf | 0 | 710 | 1.9 | 30.5 |
| Genova - Porto Antico | 30 | icon2i | 1 | 710 | 2.01 | 24.0 |
| Genova - Porto Antico | 30 | iconeu | 1 | 710 | 1.97 | 26.3 |
| Genova - Porto Antico | 30 | ecmwf | 1 | 710 | 1.94 | 33.8 |
| Genova - Porto Antico | 30 | icon2i | 2 | 710 | 2.17 | 22.3 |
| Genova - Porto Antico | 30 | iconeu | 2 | 710 | 2.02 | 30.7 |
| Genova - Porto Antico | 30 | ecmwf | 2 | 710 | 1.98 | 33.2 |
| Genova - Porto Antico | 30 | aromehd | 0 | 710 | 1.88 | 19.1 |
| Genova - Porto Antico | 30 | icon2i | 0 | 710 | 1.71 | 20.7 |
| Genova - Porto Antico | 30 | aromehd | 1 | 710 | 2.13 | 24.3 |
| Genova - Porto Antico | 30 | icon2i | 1 | 710 | 2.01 | 24.0 |
| Genova - Porto Antico | 365 | icon2i | 0 | 8458 | 1.78 | 22.2 |
| Genova - Porto Antico | 365 | iconeu | 0 | 8458 | 2.15 | 24.7 |
| Genova - Porto Antico | 365 | ecmwf | 0 | 8458 | 2.02 | 28.4 |
| Genova - Porto Antico | 365 | icon2i | 1 | 7368 | 1.88 | 22.3 |
| Genova - Porto Antico | 365 | iconeu | 1 | 7368 | 2.33 | 26.5 |
| Genova - Porto Antico | 365 | ecmwf | 1 | 7368 | 2.14 | 29.1 |
| Genova - Porto Antico | 365 | icon2i | 2 | 7234 | 1.99 | 23.8 |
| Genova - Porto Antico | 365 | iconeu | 2 | 7234 | 2.43 | 28.3 |
| Genova - Porto Antico | 365 | ecmwf | 2 | 7234 | 2.18 | 28.9 |
| Genova - Porto Antico | 365 | aromehd | 0 | 1952 | 1.74 | 24.9 |
| Genova - Porto Antico | 365 | icon2i | 0 | 1952 | 1.68 | 26.6 |
| Genova - Porto Antico | 365 | aromehd | 1 | 1945 | 1.97 | 28.8 |
| Genova - Porto Antico | 365 | icon2i | 1 | 1945 | 1.8 | 27.9 |
| La Spezia | 30 | icon2i | 0 | 692 | 1.76 | 30.7 |
| La Spezia | 30 | iconeu | 0 | 692 | 1.85 | 39.7 |
| La Spezia | 30 | ecmwf | 0 | 692 | 3.66 | 49.2 |
| La Spezia | 30 | icon2i | 1 | 692 | 1.8 | 33.9 |
| La Spezia | 30 | iconeu | 1 | 692 | 1.9 | 44.9 |
| La Spezia | 30 | ecmwf | 1 | 692 | 3.7 | 54.2 |
| La Spezia | 30 | icon2i | 2 | 692 | 1.78 | 39.3 |
| La Spezia | 30 | iconeu | 2 | 692 | 1.97 | 44.5 |
| La Spezia | 30 | ecmwf | 2 | 692 | 3.7 | 56.1 |
| La Spezia | 30 | aromehd | 0 | 692 | 1.74 | 29.5 |
| La Spezia | 30 | icon2i | 0 | 692 | 1.76 | 30.7 |
| La Spezia | 30 | aromehd | 1 | 692 | 1.77 | 32.9 |
| La Spezia | 30 | icon2i | 1 | 692 | 1.8 | 33.9 |
| La Spezia | 365 | icon2i | 0 | 8392 | 2.19 | 34.9 |
| La Spezia | 365 | iconeu | 0 | 8392 | 2.28 | 39.9 |
| La Spezia | 365 | ecmwf | 0 | 8392 | 3.94 | 53.5 |
| La Spezia | 365 | icon2i | 1 | 7298 | 2.11 | 38.2 |
| La Spezia | 365 | iconeu | 1 | 7298 | 2.22 | 40.7 |
| La Spezia | 365 | ecmwf | 1 | 7298 | 3.91 | 55.4 |
| La Spezia | 365 | icon2i | 2 | 7161 | 2.15 | 39.3 |
| La Spezia | 365 | iconeu | 2 | 7161 | 2.26 | 42.2 |
| La Spezia | 365 | ecmwf | 2 | 7161 | 3.95 | 57.8 |
| La Spezia | 365 | aromehd | 0 | 1932 | 1.82 | 31.6 |
| La Spezia | 365 | icon2i | 0 | 1932 | 1.99 | 35.4 |
| La Spezia | 365 | aromehd | 1 | 1924 | 1.86 | 37.8 |
| La Spezia | 365 | icon2i | 1 | 1924 | 1.97 | 38.2 |
| Portovenere | 30 | icon2i | 0 | 684 | 2.32 | 26.8 |
| Portovenere | 30 | iconeu | 0 | 684 | 3.15 | 32.3 |
| Portovenere | 30 | ecmwf | 0 | 684 | 2.59 | 52.8 |
| Portovenere | 30 | icon2i | 1 | 684 | 2.31 | 29.8 |
| Portovenere | 30 | iconeu | 1 | 684 | 3.2 | 33.3 |
| Portovenere | 30 | ecmwf | 1 | 684 | 2.57 | 51.2 |
| Portovenere | 30 | icon2i | 2 | 684 | 2.37 | 32.7 |
| Portovenere | 30 | iconeu | 2 | 684 | 3.19 | 33.4 |
| Portovenere | 30 | ecmwf | 2 | 684 | 2.52 | 50.0 |
| Portovenere | 30 | aromehd | 0 | 684 | 1.96 | 30.4 |
| Portovenere | 30 | icon2i | 0 | 684 | 2.32 | 26.8 |
| Portovenere | 30 | aromehd | 1 | 684 | 2.12 | 32.5 |
| Portovenere | 30 | icon2i | 1 | 684 | 2.31 | 29.8 |
| Portovenere | 365 | icon2i | 0 | 8413 | 2.29 | 32.8 |
| Portovenere | 365 | iconeu | 0 | 8413 | 2.85 | 37.1 |
| Portovenere | 365 | ecmwf | 0 | 8413 | 2.9 | 46.1 |
| Portovenere | 365 | icon2i | 1 | 7323 | 2.36 | 34.0 |
| Portovenere | 365 | iconeu | 1 | 7323 | 2.94 | 37.1 |
| Portovenere | 365 | ecmwf | 1 | 7323 | 2.87 | 46.3 |
| Portovenere | 365 | icon2i | 2 | 7176 | 2.39 | 35.2 |
| Portovenere | 365 | iconeu | 2 | 7176 | 2.96 | 38.4 |
| Portovenere | 365 | ecmwf | 2 | 7176 | 2.96 | 47.7 |
| Portovenere | 365 | aromehd | 0 | 1922 | 1.99 | 32.0 |
| Portovenere | 365 | icon2i | 0 | 1922 | 2.14 | 29.8 |
| Portovenere | 365 | aromehd | 1 | 1913 | 2.06 | 34.6 |
| Portovenere | 365 | icon2i | 1 | 1913 | 2.12 | 32.7 |
| Luni - Provasco | 30 | icon2i | 0 | 715 | 1.25 | 30.2 |
| Luni - Provasco | 30 | iconeu | 0 | 715 | 1.46 | 46.1 |
| Luni - Provasco | 30 | ecmwf | 0 | 715 | 1.81 | 48.9 |
| Luni - Provasco | 30 | icon2i | 1 | 715 | 1.29 | 31.6 |
| Luni - Provasco | 30 | iconeu | 1 | 715 | 1.49 | 47.4 |
| Luni - Provasco | 30 | ecmwf | 1 | 715 | 1.83 | 51.3 |
| Luni - Provasco | 30 | icon2i | 2 | 715 | 1.34 | 30.6 |
| Luni - Provasco | 30 | iconeu | 2 | 715 | 1.46 | 46.6 |
| Luni - Provasco | 30 | ecmwf | 2 | 715 | 1.77 | 50.0 |
| Luni - Provasco | 30 | aromehd | 0 | 715 | 1.52 | 29.6 |
| Luni - Provasco | 30 | icon2i | 0 | 715 | 1.25 | 30.2 |
| Luni - Provasco | 30 | aromehd | 1 | 715 | 1.59 | 27.8 |
| Luni - Provasco | 30 | icon2i | 1 | 715 | 1.29 | 31.6 |
| Luni - Provasco | 365 | icon2i | 0 | 8547 | 1.34 | 30.6 |
| Luni - Provasco | 365 | iconeu | 0 | 8547 | 1.51 | 44.3 |
| Luni - Provasco | 365 | ecmwf | 0 | 8547 | 2.03 | 52.1 |
| Luni - Provasco | 365 | icon2i | 1 | 7436 | 1.37 | 32.1 |
| Luni - Provasco | 365 | iconeu | 1 | 7436 | 1.53 | 45.6 |
| Luni - Provasco | 365 | ecmwf | 1 | 7436 | 2.0 | 51.6 |
| Luni - Provasco | 365 | icon2i | 2 | 7297 | 1.42 | 34.2 |
| Luni - Provasco | 365 | iconeu | 2 | 7297 | 1.6 | 48.2 |
| Luni - Provasco | 365 | ecmwf | 2 | 7297 | 2.02 | 53.1 |
| Luni - Provasco | 365 | aromehd | 0 | 1985 | 1.44 | 32.4 |
| Luni - Provasco | 365 | icon2i | 0 | 1985 | 1.18 | 30.4 |
| Luni - Provasco | 365 | aromehd | 1 | 1977 | 1.48 | 34.7 |
| Luni - Provasco | 365 | icon2i | 1 | 1977 | 1.15 | 31.8 |
