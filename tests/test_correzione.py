"""Test dell'applicazione del MOS in produzione e della sua integrazione nella pipeline. Nessuna rete."""
import json
import tempfile
import time
import unittest
from pathlib import Path
from unittest import mock

from meteo import build, correzione
from meteo.correzione import corrected_series, corrections_for, lead_day, load_corrections, station_block
from meteo.wind import WIND_NAMES, distance_km

HOUR = 3600
MODELS3 = ["icon2i", "iconeu", "ecmwf"]


def fake_corr(station, day, quantity, models, level, name=None):
    """Correzione che restituisce sempre `level`: così si vede quale giorno è stato applicato."""
    qs = ("vel",) if quantity == "vel" else ("vel", "raf")
    beta = [level] + [0.0] * (len(models) * len(qs) + 2)
    corr = {"stazione": station, "modello": name or ("combinato" if quantity == "vel" else "icon2i+iconeu"),
            "giorno": day, "grandezza": quantity, "modelli": models,
            "ingressi": [[m, q] for m in models for q in qs], "fonte": [models[0]], "lambda": 30.0,
            "ore_settore": {}, "pool": beta, "settori": {n: beta for n in WIND_NAMES}}
    if quantity == "vel":
        corr["direzione"] = {"fonte": [models[0]], "ruota": False, "rotazione": {n: 0.0 for n in WIND_NAMES}}
    return corr


def fake_mos(stations, now=None, version=1):
    corrs, evals = [], []
    for code in stations:
        for d in range(3):
            corrs.append(fake_corr(code, d, "vel", MODELS3, 10 + d))
            corrs.append(fake_corr(code, d, "raf", ["icon2i", "iconeu"], 20 + d))
        corrs.append(fake_corr(code, 1, "vel", ["icon2i"], 99, name="icon2i"))  # insieme più povero: non va scelto
        evals += [
            {"stazione": code, "grandezza": "vel", "modello": "combinato", "giorno": 1, "n": 100, "grezzo": {"mae": 2.0}, "mos": {"mae": 1.5}},
            {"stazione": code, "grandezza": "raf", "modello": "icon2i+iconeu", "giorno": 1, "n": 100, "grezzo": {"mae": 3.0}, "mos": {"mae": 2.0}},
        ]
    return {"versione": version, "generated": int(now or time.time()), "test_dal": "2026-04-14", "correzioni": corrs, "valutazione": evals}


def fake_series(hours, models=MODELS3, vel=8.0, direction=225.0, gust=12.0):
    return {m: {"time": list(hours), "wind_speed_10m": [vel] * len(hours),
                "wind_direction_10m": [direction] * len(hours), "wind_gusts_10m": [gust] * len(hours)} for m in models}


class TestLeadDay(unittest.TestCase):
    def test_nearest_day(self):
        got = [lead_day(h, 2) for h in (0, 8, 17, 18, 26, 41, 42, 59, 71)]
        self.assertEqual(got, [0, 0, 0, 1, 1, 1, 2, 2, 2])

    def test_capped_and_negative(self):
        self.assertEqual(lead_day(70, 1), 1)
        self.assertIsNone(lead_day(-1, 2))


class TestLoadCorrections(unittest.TestCase):
    def _write(self, mos):
        d = tempfile.mkdtemp()
        p = Path(d) / "mos.json"
        p.write_text(json.dumps(mos))
        return p

    def test_ok(self):
        mos, why = load_corrections(self._write(fake_mos(["S"])))
        self.assertIsNone(why)
        self.assertEqual(mos["versione"], 1)

    def test_missing_stale_and_wrong_schema(self):
        self.assertIn("non trovato", load_corrections(Path("/nonexistent/mos.json"))[1])
        old = fake_mos(["S"], now=time.time() - 61 * 86400)
        mos, why = load_corrections(self._write(old))
        self.assertIsNone(mos)
        self.assertIn("vecchi", why)
        mos, why = load_corrections(self._write(fake_mos(["S"], version=2)))
        self.assertIsNone(mos)
        self.assertIn("schema", why)

    def test_unreadable(self):
        p = self._write({})
        p.write_text("{non json")
        self.assertIn("illeggibile", load_corrections(p)[1])


class TestSelection(unittest.TestCase):
    def test_richest_model_set_wins(self):
        corrs = corrections_for(fake_mos(["S"]), "S")
        self.assertEqual(corrs["vel"][1]["modelli"], MODELS3)  # non l'insieme povero con un solo modello
        self.assertEqual(sorted(corrs["vel"]), [0, 1, 2])
        self.assertEqual(corrs["raf"][0]["modelli"], ["icon2i", "iconeu"])
        self.assertEqual(corrections_for(fake_mos(["S"]), "altra"), {})


class TestCorrectedSeries(unittest.TestCase):
    def setUp(self):
        self.init = 1_800_000_000 - 1_800_000_000 % 86400
        self.hours = [self.init + h * HOUR for h in (0, 20, 45, 80)]
        self.corrs = corrections_for(fake_mos(["S"]), "S")

    def test_day_of_lead_picks_the_right_coefficients(self):
        out = corrected_series(self.corrs, fake_series(self.hours), self.init, self.hours)
        self.assertEqual(out["vel"][:3], [10.0, 11.0, 12.0])  # anticipo 0, 20, 45 h -> giorno 0, 1, 2
        self.assertEqual(out["raf"][:3], [20.0, 21.0, 22.0])
        self.assertEqual(out["dir"][0], 225)  # nessuna rotazione

    def test_beyond_the_horizon_is_empty(self):
        series = fake_series(self.hours[:3])  # le serie finiscono prima dell'ultima ora
        out = corrected_series(self.corrs, series, self.init, self.hours)
        self.assertEqual((out["vel"][3], out["dir"][3], out["raf"][3]), (None, None, None))

    def test_missing_input_means_no_value(self):
        series = fake_series(self.hours)
        series["iconeu"]["wind_speed_10m"][1] = None
        out = corrected_series(self.corrs, series, self.init, self.hours)
        self.assertIsNone(out["vel"][1])
        self.assertIsNone(out["raf"][1])  # la raffica usa anche iconeu
        self.assertIsNotNone(out["vel"][0])

    def test_gust_needs_gust_inputs_but_speed_does_not(self):
        series = fake_series(self.hours)
        series["iconeu"]["wind_gusts_10m"][0] = None
        out = corrected_series(self.corrs, series, self.init, self.hours)
        self.assertIsNotNone(out["vel"][0])
        self.assertIsNone(out["raf"][0])

    def test_hours_before_the_run_are_empty(self):
        out = corrected_series(self.corrs, fake_series(self.hours), self.init + 100 * HOUR, self.hours)
        self.assertEqual(out["vel"], [None] * 4)


class TestStationBlock(unittest.TestCase):
    def test_block_and_summary(self):
        mos = fake_mos(["S"])
        init = 1_800_000_000 - 1_800_000_000 % 86400
        hours = [init + h * HOUR for h in range(3)]
        st = {"nome": "Stazione", "codice": "S", "lat": 44.0, "lon": 9.0}
        block = station_block(mos, st, fake_series(hours), init, hours)
        self.assertEqual(block["stazione"], st)
        self.assertEqual(block["info"]["vel"], {"mae_grezzo": 2.0, "mae_mos": 1.5, "ore": 100})
        self.assertEqual(block["info"]["raf"]["mae_mos"], 2.0)
        self.assertEqual(len(block["vel"]), 3)
        self.assertIsNone(station_block(mos, {**st, "codice": "altra"}, fake_series(hours), init, hours))


class TestPipelineIntegration(unittest.TestCase):
    CODES = ["ME00309", "ME00094", "ME00265"]  # le stazioni `in_mappa` di config.toml

    def _build(self, path):
        with tempfile.TemporaryDirectory() as d, mock.patch.object(correzione, "PATH", path):
            build.build(Path(d), demo=True)
            return json.loads((Path(d) / "spots.json").read_text())

    def test_only_the_three_spots_get_mos_aligned_with_time(self):
        d = tempfile.mkdtemp()
        p = Path(d) / "mos.json"
        p.write_text(json.dumps(fake_mos(self.CODES)))
        spots = self._build(p)
        with_mos = {s["name"] for s in spots["spots"] if "mos" in s}
        self.assertEqual(with_mos, {"Genova", "Golfo della Spezia", "Marina di Carrara"})
        for s in spots["spots"]:
            if "mos" in s:
                self.assertEqual(len(s["mos"]["vel"]), len(spots["times"]))
                self.assertGreater(s["mos"]["stazione"]["distanza_km"], 0)
                self.assertIsNotNone(s["mos"]["vel"][0])

    def test_missing_or_stale_file_removes_mos_without_breaking_the_build(self):
        spots = self._build(Path("/nonexistent/mos.json"))
        self.assertFalse(any("mos" in s for s in spots["spots"]))
        self.assertEqual(len(spots["spots"]), 8)
        d = tempfile.mkdtemp()
        p = Path(d) / "mos.json"
        p.write_text(json.dumps(fake_mos(self.CODES, now=time.time() - 90 * 86400)))
        self.assertFalse(any("mos" in s for s in self._build(p)["spots"]))

    def test_network_failure_removes_mos_without_breaking_the_build(self):
        d = tempfile.mkdtemp()
        p = Path(d) / "mos.json"
        p.write_text(json.dumps(fake_mos(self.CODES)))
        with mock.patch.object(build.openmeteo, "fetch_run_init", side_effect=OSError("rete")):
            with mock.patch.object(correzione, "PATH", p):
                got = build.mos_for_spots(build.load_config(), 0, [0, HOUR], 4, demo=False)
        self.assertEqual(got, {})


class TestDistance(unittest.TestCase):
    def test_one_degree_of_latitude(self):
        self.assertAlmostEqual(distance_km(44.0, 9.0, 45.0, 9.0), 111.19, places=1)
        self.assertEqual(distance_km(44.0, 9.0, 44.0, 9.0), 0)


if __name__ == "__main__":
    unittest.main()
