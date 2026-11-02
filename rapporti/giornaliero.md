# Raccolta e verifica giornaliera

Data UTC: 2026-11-02

Quota stimata: 8280 chiamate/giorno (senza retry o corse manuali).

I punteggi sono dei modelli grezzi. Nessun riallenamento MOS.

Direzione -1 = non disponibile: conta fra le assenze, senza avvisi di fuori scala.

| Stazione | Ultima velocità UTC | Ritardo h | Direzione N/D nel campione QC | Ore valide 30 / 365 giorni |
|---|---|---|---|---|
| Genova - Porto Antico | 2026-11-02T13:00:00+00:00 | 0.9 | 301 | 710 / 8459 |
| La Spezia | 2026-11-02T13:00:00+00:00 | 0.9 | 366 | 692 / 8394 |
| Portovenere | 2026-11-02T13:00:00+00:00 | 0.9 | 323 | 708 / 8437 |
| Luni - Provasco | 2026-11-02T13:00:00+00:00 | 0.9 | 210 | 713 / 8550 |

## Avvisi

- Genova - Porto Antico ICON-2I: previsioni non aggiornate (The read operation timed out); uso della cache
- Genova - Porto Antico ICON-EU: previsioni non aggiornate (Open-Meteo 503: {"error":true,"reason":"The service is overloaded"}); uso della cache
- Genova - Porto Antico ECMWF: previsioni non aggiornate (Open-Meteo 503: {"error":true,"reason":"The service is overloaded"}); uso della cache
- Genova - Porto Antico AROME HD: previsioni non aggiornate (Open-Meteo 503: {"reason":"The service is overloaded","error":true}); uso della cache
- La Spezia ICON-2I: previsioni non aggiornate (<urlopen error _ssl.c:993: The handshake operation timed out>); uso della cache
- La Spezia ICON-EU: previsioni non aggiornate (Open-Meteo 503: {"reason":"The service is overloaded","error":true}); uso della cache
- La Spezia ECMWF: previsioni non aggiornate (Open-Meteo 503: {"reason":"The service is overloaded","error":true}); uso della cache
- La Spezia AROME HD: previsioni non aggiornate (Open-Meteo 503: {"reason":"The service is overloaded","error":true}); uso della cache
- Portovenere ICON-2I: previsioni non aggiornate (<urlopen error _ssl.c:993: The handshake operation timed out>); uso della cache
- Portovenere ICON-EU: previsioni non aggiornate (Open-Meteo 503: {"error":true,"reason":"The service is overloaded"}); uso della cache
- Portovenere ECMWF: previsioni non aggiornate (Open-Meteo 503: {"reason":"The service is overloaded","error":true}); uso della cache
- Portovenere AROME HD: previsioni non aggiornate (Open-Meteo 503: {"error":true,"reason":"The service is overloaded"}); uso della cache
- Luni - Provasco ICON-2I: previsioni non aggiornate (<urlopen error _ssl.c:993: The handshake operation timed out>); uso della cache
- Luni - Provasco ICON-EU: previsioni non aggiornate (Open-Meteo 503: {"error":true,"reason":"The service is overloaded"}); uso della cache
- Luni - Provasco ECMWF: previsioni non aggiornate (Open-Meteo 503: {"error":true,"reason":"The service is overloaded"}); uso della cache
- Luni - Provasco AROME HD: previsioni non aggiornate (Open-Meteo 503: {"reason":"The service is overloaded","error":true}); uso della cache

## Punteggi sul campione comune

| Stazione | Finestra | Modello | Giorno | N | MAE kn | MAE direzione ° |
|---|---|---|---|---|---|---|
| Genova - Porto Antico | 30 | icon2i | 0 | 686 | 1.74 | 20.6 |
| Genova - Porto Antico | 30 | iconeu | 0 | 686 | 1.97 | 24.4 |
| Genova - Porto Antico | 30 | ecmwf | 0 | 686 | 1.95 | 29.2 |
| Genova - Porto Antico | 30 | icon2i | 1 | 686 | 2.05 | 24.3 |
| Genova - Porto Antico | 30 | iconeu | 1 | 686 | 2.07 | 25.9 |
| Genova - Porto Antico | 30 | ecmwf | 1 | 686 | 2.0 | 32.8 |
| Genova - Porto Antico | 30 | icon2i | 2 | 686 | 2.23 | 22.2 |
| Genova - Porto Antico | 30 | iconeu | 2 | 686 | 2.16 | 30.5 |
| Genova - Porto Antico | 30 | ecmwf | 2 | 686 | 2.04 | 31.4 |
| Genova - Porto Antico | 30 | aromehd | 0 | 686 | 1.89 | 18.9 |
| Genova - Porto Antico | 30 | icon2i | 0 | 686 | 1.74 | 20.6 |
| Genova - Porto Antico | 30 | aromehd | 1 | 686 | 2.1 | 24.5 |
| Genova - Porto Antico | 30 | icon2i | 1 | 686 | 2.05 | 24.3 |
| Genova - Porto Antico | 365 | icon2i | 0 | 8435 | 1.78 | 22.1 |
| Genova - Porto Antico | 365 | iconeu | 0 | 8435 | 2.16 | 24.7 |
| Genova - Porto Antico | 365 | ecmwf | 0 | 8435 | 2.01 | 28.4 |
| Genova - Porto Antico | 365 | icon2i | 1 | 7345 | 1.87 | 22.2 |
| Genova - Porto Antico | 365 | iconeu | 1 | 7345 | 2.33 | 26.4 |
| Genova - Porto Antico | 365 | ecmwf | 1 | 7345 | 2.13 | 29.1 |
| Genova - Porto Antico | 365 | icon2i | 2 | 7211 | 1.98 | 23.7 |
| Genova - Porto Antico | 365 | iconeu | 2 | 7211 | 2.43 | 28.3 |
| Genova - Porto Antico | 365 | ecmwf | 2 | 7211 | 2.18 | 28.8 |
| Genova - Porto Antico | 365 | aromehd | 0 | 2000 | 1.74 | 24.3 |
| Genova - Porto Antico | 365 | icon2i | 0 | 2000 | 1.69 | 25.9 |
| Genova - Porto Antico | 365 | aromehd | 1 | 1993 | 1.96 | 28.0 |
| Genova - Porto Antico | 365 | icon2i | 1 | 1993 | 1.8 | 27.1 |
| La Spezia | 30 | icon2i | 0 | 670 | 1.78 | 30.1 |
| La Spezia | 30 | iconeu | 0 | 670 | 1.88 | 36.0 |
| La Spezia | 30 | ecmwf | 0 | 670 | 3.81 | 47.3 |
| La Spezia | 30 | icon2i | 1 | 670 | 1.81 | 33.6 |
| La Spezia | 30 | iconeu | 1 | 670 | 1.9 | 41.8 |
| La Spezia | 30 | ecmwf | 1 | 670 | 3.86 | 51.8 |
| La Spezia | 30 | icon2i | 2 | 670 | 1.8 | 37.9 |
| La Spezia | 30 | iconeu | 2 | 670 | 1.96 | 42.2 |
| La Spezia | 30 | ecmwf | 2 | 670 | 3.88 | 51.9 |
| La Spezia | 30 | aromehd | 0 | 670 | 1.77 | 29.4 |
| La Spezia | 30 | icon2i | 0 | 670 | 1.78 | 30.1 |
| La Spezia | 30 | aromehd | 1 | 670 | 1.78 | 31.7 |
| La Spezia | 30 | icon2i | 1 | 670 | 1.81 | 33.6 |
| La Spezia | 365 | icon2i | 0 | 8372 | 2.18 | 34.7 |
| La Spezia | 365 | iconeu | 0 | 8372 | 2.27 | 39.7 |
| La Spezia | 365 | ecmwf | 0 | 8372 | 3.94 | 53.4 |
| La Spezia | 365 | icon2i | 1 | 7278 | 2.1 | 38.2 |
| La Spezia | 365 | iconeu | 1 | 7278 | 2.21 | 40.6 |
| La Spezia | 365 | ecmwf | 1 | 7278 | 3.91 | 55.3 |
| La Spezia | 365 | icon2i | 2 | 7141 | 2.14 | 39.1 |
| La Spezia | 365 | iconeu | 2 | 7141 | 2.24 | 42.0 |
| La Spezia | 365 | ecmwf | 2 | 7141 | 3.95 | 57.6 |
| La Spezia | 365 | aromehd | 0 | 1979 | 1.82 | 31.5 |
| La Spezia | 365 | icon2i | 0 | 1979 | 1.98 | 34.8 |
| La Spezia | 365 | aromehd | 1 | 1971 | 1.86 | 37.2 |
| La Spezia | 365 | icon2i | 1 | 1971 | 1.97 | 38.0 |
| Portovenere | 30 | icon2i | 0 | 684 | 2.33 | 26.9 |
| Portovenere | 30 | iconeu | 0 | 684 | 3.25 | 33.5 |
| Portovenere | 30 | ecmwf | 0 | 684 | 2.65 | 51.5 |
| Portovenere | 30 | icon2i | 1 | 684 | 2.35 | 30.5 |
| Portovenere | 30 | iconeu | 1 | 684 | 3.29 | 34.1 |
| Portovenere | 30 | ecmwf | 1 | 684 | 2.62 | 50.3 |
| Portovenere | 30 | icon2i | 2 | 684 | 2.42 | 32.8 |
| Portovenere | 30 | iconeu | 2 | 684 | 3.3 | 34.0 |
| Portovenere | 30 | ecmwf | 2 | 684 | 2.58 | 48.9 |
| Portovenere | 30 | aromehd | 0 | 684 | 1.99 | 30.6 |
| Portovenere | 30 | icon2i | 0 | 684 | 2.33 | 26.9 |
| Portovenere | 30 | aromehd | 1 | 684 | 2.16 | 32.2 |
| Portovenere | 30 | icon2i | 1 | 684 | 2.35 | 30.5 |
| Portovenere | 365 | icon2i | 0 | 8413 | 2.28 | 32.5 |
| Portovenere | 365 | iconeu | 0 | 8413 | 2.85 | 37.1 |
| Portovenere | 365 | ecmwf | 0 | 8413 | 2.9 | 45.8 |
| Portovenere | 365 | icon2i | 1 | 7323 | 2.35 | 33.8 |
| Portovenere | 365 | iconeu | 1 | 7323 | 2.95 | 37.1 |
| Portovenere | 365 | ecmwf | 1 | 7323 | 2.87 | 46.0 |
| Portovenere | 365 | icon2i | 2 | 7176 | 2.39 | 34.8 |
| Portovenere | 365 | iconeu | 2 | 7176 | 2.96 | 38.4 |
| Portovenere | 365 | ecmwf | 2 | 7176 | 2.96 | 47.2 |
| Portovenere | 365 | aromehd | 0 | 1991 | 1.99 | 31.7 |
| Portovenere | 365 | icon2i | 0 | 1991 | 2.14 | 29.5 |
| Portovenere | 365 | aromehd | 1 | 1982 | 2.06 | 34.0 |
| Portovenere | 365 | icon2i | 1 | 1982 | 2.13 | 32.5 |
| Luni - Provasco | 30 | icon2i | 0 | 689 | 1.31 | 30.8 |
| Luni - Provasco | 30 | iconeu | 0 | 689 | 1.52 | 47.1 |
| Luni - Provasco | 30 | ecmwf | 0 | 689 | 1.83 | 52.5 |
| Luni - Provasco | 30 | icon2i | 1 | 689 | 1.35 | 31.7 |
| Luni - Provasco | 30 | iconeu | 1 | 689 | 1.55 | 49.8 |
| Luni - Provasco | 30 | ecmwf | 1 | 689 | 1.86 | 55.6 |
| Luni - Provasco | 30 | icon2i | 2 | 689 | 1.4 | 30.8 |
| Luni - Provasco | 30 | iconeu | 2 | 689 | 1.5 | 49.0 |
| Luni - Provasco | 30 | ecmwf | 2 | 689 | 1.8 | 54.0 |
| Luni - Provasco | 30 | aromehd | 0 | 689 | 1.6 | 29.9 |
| Luni - Provasco | 30 | icon2i | 0 | 689 | 1.31 | 30.8 |
| Luni - Provasco | 30 | aromehd | 1 | 689 | 1.65 | 27.9 |
| Luni - Provasco | 30 | icon2i | 1 | 689 | 1.35 | 31.7 |
| Luni - Provasco | 365 | icon2i | 0 | 8526 | 1.34 | 30.7 |
| Luni - Provasco | 365 | iconeu | 0 | 8526 | 1.51 | 44.5 |
| Luni - Provasco | 365 | ecmwf | 0 | 8526 | 2.03 | 52.4 |
| Luni - Provasco | 365 | icon2i | 1 | 7415 | 1.36 | 32.1 |
| Luni - Provasco | 365 | iconeu | 1 | 7415 | 1.54 | 45.9 |
| Luni - Provasco | 365 | ecmwf | 1 | 7415 | 2.0 | 51.9 |
| Luni - Provasco | 365 | icon2i | 2 | 7276 | 1.42 | 34.2 |
| Luni - Provasco | 365 | iconeu | 2 | 7276 | 1.61 | 48.5 |
| Luni - Provasco | 365 | ecmwf | 2 | 7276 | 2.01 | 53.4 |
| Luni - Provasco | 365 | aromehd | 0 | 2031 | 1.45 | 32.6 |
| Luni - Provasco | 365 | icon2i | 0 | 2031 | 1.19 | 30.5 |
| Luni - Provasco | 365 | aromehd | 1 | 2023 | 1.48 | 34.5 |
| Luni - Provasco | 365 | icon2i | 1 | 2023 | 1.16 | 31.8 |
