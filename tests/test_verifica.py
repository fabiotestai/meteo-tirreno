"""Test della fase 1 (osservati ARPAL, previous runs, punteggi). Nessun accesso alla rete."""
import calendar
import unittest
from datetime import date
from unittest import mock

from meteo import openmeteo
from meteo.arpal import parse_report
from meteo.verifica import _months, angle_diff, compare, evaluate, scores
from meteo.wind import KNOT_MS

# Estratto reale (accorciato) del CSV del portale: un blocco per parametro, fine riga \r\n
REPORT = (
    "\r\n\r\n"
    '"Stazione",PORTOVENERE - COMUNE\r\n'
    '"Parametro",VENTO - DIREZIONE DI PROVENIENZA DEL VENTO PREVALENTE (Gradi_Nord)\r\n\r\n'
    '"Inizio rilevazione","Fine rilevazione","Valore","Dataset","Valido"\r\n'
    '"01/03/2025 00:00","01/03/2025 01:00","360","Tutti i dati","S\xec"\r\n'
    '"01/03/2025 01:00","01/03/2025 02:00","23","Tutti i dati","S\xec"\r\n'
    "\r\n"
    '"Stazione",PORTOVENERE - COMUNE\r\n'
    '"Parametro",VENTO - INTENSIT\xc0 MEDIA DEL VENTO (m/s)\r\n\r\n'
    '"Inizio rilevazione","Fine rilevazione","Valore","Dataset","Valido"\r\n'
    '"01/03/2025 00:00","01/03/2025 01:00","3.7","Tutti i dati","S\xec"\r\n'
    '"01/03/2025 01:00","01/03/2025 02:00",".9","Tutti i dati","No"\r\n'
    "\r\n"
    '"Stazione",PORTOVENERE - COMUNE\r\n'
    '"Parametro",VENTO - INTENSIT\xc0 MASSIMA DEL VENTO (m/s)\r\n\r\n'
    '"Inizio rilevazione","Fine rilevazione","Valore","Dataset","Valido"\r\n'
    '"01/03/2025 00:00","01/03/2025 01:00","6.5","Tutti i dati","S\xec"\r\n'
)


def t(y, m, d, h):
    return calendar.timegm((y, m, d, h, 0, 0))


class TestArpalParsing(unittest.TestCase):
    def test_blocks_merged_by_end_of_hour(self):
        data = parse_report(REPORT)
        first = t(2025, 3, 1, 1)  # il valore dell'ora 00-01 è datato alle 01 UTC
        self.assertEqual(data[first], {"dir": 360.0, "speed": 3.7, "gust": 6.5})

    def test_invalid_values_dropped(self):
        data = parse_report(REPORT)
        self.assertEqual(data[t(2025, 3, 1, 2)], {"dir": 23.0})  # velocità ".9" marcata non valida


class TestPreviousRuns(unittest.TestCase):
    def test_variable_names_and_split_by_day(self):
        seen = {}

        def fake_get(url, params):
            seen.update(params)
            names = params["hourly"].split(",")
            return {"hourly": {"time": [0, 3600], **{n: [1.0, 2.0] for n in names if "gusts" not in n}}}

        with mock.patch.object(openmeteo, "_get", side_effect=fake_get):
            out = openmeteo.fetch_previous_runs(
                (44.0, 9.0), ["wind_speed_10m", "wind_gusts_10m"], "icon_eu", "2025-01-01", "2025-01-31", 2
            )
        self.assertIn("wind_speed_10m_previous_day2", seen["hourly"])
        self.assertEqual(seen["wind_speed_unit"], "ms")
        self.assertEqual(out[0]["wind_speed_10m"], [1.0, 2.0])
        self.assertEqual(out[2]["wind_speed_10m"], [1.0, 2.0])
        self.assertEqual(out[1]["wind_gusts_10m"], [None, None])  # variabile assente -> None


class TestScores(unittest.TestCase):
    def test_angle_diff_through_north(self):
        self.assertEqual(angle_diff(10, 350), 20)
        self.assertEqual(angle_diff(350, 10), -20)

    def test_known_values(self):
        pairs = [
            ({"speed": 12, "dir": 0}, {"speed": 10, "dir": 0}),
            ({"speed": 8, "dir": 180}, {"speed": 10, "dir": 180}),
        ]
        sc = scores(pairs, min_dir_kn=4)
        self.assertEqual(sc["bias"], 0)
        self.assertEqual(sc["mae"], 2)
        self.assertEqual(sc["rmse"], 2)
        self.assertEqual(sc["rmse_vett"], 2)  # stessa direzione: errore vettoriale = errore di velocità
        self.assertEqual(sc["mae_dir"], 0)

    def test_opposite_direction_is_a_big_vector_error(self):
        sc = scores([({"speed": 10, "dir": 45}, {"speed": 10, "dir": 225})], min_dir_kn=4)
        self.assertEqual(sc["bias"], 0)  # stessa velocità...
        self.assertAlmostEqual(sc["rmse_vett"], 20, places=1)  # ...ma vento opposto
        self.assertEqual(sc["mae_dir"], 180)

    def test_calm_excluded_from_direction(self):
        sc = scores([({"speed": 2, "dir": 0}, {"speed": 2, "dir": 180})], min_dir_kn=4)
        self.assertEqual(sc["n_dir"], 0)
        self.assertIsNone(sc["mae_dir"])


class TestEvaluate(unittest.TestCase):
    def test_common_sample_uses_same_hours(self):
        ms = 10 * KNOT_MS  # 10 nodi in m/s
        observed = {1: {"speed": ms, "dir": 225, "gust": None}, 2: {"speed": ms, "dir": 225, "gust": None}}
        fa = {0: {1: {"speed": ms, "dir": 225}, 2: {"speed": 2 * ms, "dir": 225}}}
        fb = {0: {1: {"speed": ms, "dir": 225}}}  # al modello B manca l'ora 2
        rows = evaluate(observed, {"a": fa, "b": fb}, days=0, min_dir_kn=4)
        get = {(r["modello"], r["campione"]): r for r in rows if r["settore"] is None}
        self.assertEqual(get[("a", "comune")]["n"], 1)
        self.assertEqual(get[("a", "comune")]["bias"], 0)
        self.assertEqual(get[("a", "completo")]["n"], 2)
        self.assertEqual(get[("a", "completo")]["bias"], 5)
        self.assertTrue(any(r["settore"] == "Libeccio" for r in rows))

    def test_pairwise_compare_only_common_hours(self):
        ms = 10 * KNOT_MS
        observed = {t: {"speed": ms, "dir": 270, "gust": None} for t in (1, 2, 3)}
        ref = {0: {t: {"speed": ms, "dir": 270} for t in (1, 2, 3)}, 1: {}}
        extra = {0: {3: {"speed": 2 * ms, "dir": 270}}}  # archivio corto: una sola ora
        rows = compare(observed, ("x", extra), ("ref", ref), days=0, min_dir_kn=4)
        self.assertTrue(rows)
        self.assertTrue(all(r["campione"] == "comune" and r["confronto"] == "x" for r in rows))
        tot = {r["modello"]: r for r in rows if r["settore"] is None}
        self.assertEqual(tot["ref"]["n"], 1)  # il riferimento ristretto all'ora che ha anche l'extra
        self.assertEqual(tot["x"]["bias"], 10)

    def test_months(self):
        m = list(_months(date(2024, 12, 15), date(2025, 2, 3)))
        self.assertEqual(m[0], (date(2024, 12, 1), date(2024, 12, 31)))
        self.assertEqual(m[-1], (date(2025, 2, 1), date(2025, 2, 28)))
        self.assertEqual(len(m), 3)


if __name__ == "__main__":
    unittest.main()
