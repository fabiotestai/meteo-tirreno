"""Archivio operativo: confini temporali, conservazione della cache e qualità."""
import copy
import json
import tempfile
import unittest
from datetime import date, datetime, timezone
from pathlib import Path
from unittest import mock

from meteo import archivio, giornaliero, verifica
from meteo.config import load_config


def ts(value):
    return int(datetime.fromisoformat(value).replace(tzinfo=timezone.utc).timestamp())


def record(speed=2, direction=225, gust=4):
    return {"speed": speed, "dir": direction, "gust": gust}


class ArchiveTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)

    def test_monthly_import_preserves_annual_and_forecast_values(self):
        cfg = load_config()
        st = cfg["verifica"]["stazioni"][0]
        code = st["codice"]
        old, target = self.root / "old", self.root / "new"
        a, b = ts("2025-12-31T23:00"), ts("2026-01-01T00:00")
        archivio.write_csv(old / "osservati" / f"ARPAL_{code}_2025.csv", archivio.OBS_HEADER,
                           [[a, "", 2, 4, 225], [b, "", 3, None, 0]])
        archivio.write_forecast(old, code, "icon2i", {0: {a: record()}, 1: {b: record(0, 350, None)}})
        before = (old / "osservati" / f"ARPAL_{code}_2025.csv").read_bytes()
        result = archivio.import_cache(old, target, cfg)
        self.assertEqual(result, {"ore_osservate": 2, "righe_previste": 2})
        self.assertEqual(len(list((target / "osservati").glob("*.csv"))), 2)
        self.assertEqual(archivio.read_observed(target, code)[b], record(3, 0, None))
        self.assertEqual(archivio.read_forecast(target, code, "icon2i", 2)[1][b], record(0, 350, None))
        self.assertEqual((old / "osservati" / f"ARPAL_{code}_2025.csv").read_bytes(), before)
        with self.assertRaises(ValueError):
            archivio.import_cache(old, target, cfg)
        with mock.patch.object(verifica, "DATA", target):
            self.assertEqual(len(verifica.load_observed(st, date(2025, 1, 1), date(2026, 1, 1), None, True)), 2)

    def test_repeated_update_corrects_values_without_duplicates_or_losing_nulls(self):
        t = ts("2026-10-18T01:00")
        old = {t: record()}
        new = {t: {"speed": 0, "gust": None}, t + 3600: record(3)}
        merged = archivio.merge_records(old, new)
        self.assertEqual(merged[t], record(0))
        archivio.write_observed(self.root, "X", merged)
        before = next((self.root / "osservati").glob("*.csv")).read_bytes()
        self.assertNotIn(b"\r", before)  # archivio identico su Windows e Linux
        archivio.write_observed(self.root, "X", archivio.merge_records(merged, new))
        self.assertEqual(next((self.root / "osservati").glob("*.csv")).read_bytes(), before)
        self.assertEqual(len(archivio.read_observed(self.root, "X")), 2)

    def test_arpal_new_year_and_partial_response(self):
        st = {"codice": "X"}
        a, b = ts("2025-12-31T23:00"), ts("2026-01-01T01:00")
        archivio.write_observed(self.root, "X", {a: record(), a + 3600: record(3), b: record(4)})
        archive = mock.Mock()
        archive.hourly.side_effect = [{a: record(5)}, {b: record(6)}]
        out, complete = giornaliero.update_observed(self.root, st, date(2025, 12, 31), date(2026, 1, 1), archive)
        self.assertFalse(complete)
        self.assertEqual(len(out), 3)
        self.assertEqual(out[a]["speed"], 5)
        self.assertEqual(archive.hourly.call_args_list, [mock.call("X", date(2025, 12, 31), date(2025, 12, 31)),
                                                       mock.call("X", date(2026, 1, 1), date(2026, 1, 1))])

    def test_empty_or_failed_download_does_not_write_partial_year(self):
        a, b = ts("2025-12-31T23:00"), ts("2026-01-01T01:00")
        archivio.write_observed(self.root, "X", {a: record()})
        for failure in ({}, OSError("rete")):
            archive = mock.Mock()
            archive.hourly.side_effect = [{a: record(5)}, failure]
            with self.assertRaises((ValueError, OSError)):
                giornaliero.update_observed(self.root, {"codice": "X"}, date(2025, 12, 31), date(2026, 1, 1), archive)
            self.assertEqual(archivio.read_observed(self.root, "X"), {a: record()})

    def test_forecast_month_boundary_and_failed_second_month(self):
        st = {"codice": "X", "lat": 44, "lon": 9}
        model = {"label": "ICON-2I", "id": "icon"}
        a, b = ts("2026-09-30T00:00"), ts("2026-10-01T00:00")
        archivio.write_forecast(self.root, "X", "icon2i", {0: {a: record()}})

        def response(t, speed):
            return {"time": [t], 0: {"wind_speed_10m": [speed], "wind_direction_10m": [225], "wind_gusts_10m": [None]}}

        with mock.patch.object(giornaliero.openmeteo, "fetch_previous_runs", side_effect=[response(a, 3), response(b, 4)]) as fetch:
            out, complete = giornaliero.update_forecast(self.root, st, model, date(2026, 9, 30), date(2026, 10, 1), 0)
        self.assertFalse(complete)  # una sola ora per ciascun giorno
        self.assertEqual(len(out[0]), 2)
        self.assertEqual(out[0][a]["gust"], 4)  # null nuovo non cancella raffica precedente
        self.assertEqual(fetch.call_args_list[0].args[3:5], ("2026-09-30", "2026-09-30"))
        before = copy.deepcopy(out)
        with mock.patch.object(giornaliero.openmeteo, "fetch_previous_runs", side_effect=[response(a, 9), OSError("rete")]):
            with self.assertRaises(OSError):
                giornaliero.update_forecast(self.root, st, model, date(2026, 9, 30), date(2026, 10, 1), 0)
        self.assertEqual(archivio.read_forecast(self.root, "X", "icon2i", 0), before)

    def test_malformed_forecast_rejected(self):
        a = ts("2026-10-01T00:00")
        for times, values in (([a], []), ([a, a], [1, 2]), ([a - 3600], [1]), ([a], [float("nan")])):
            data = {"time": times, 0: {v: values for v in verifica.FC_VARS}}
            with self.assertRaises(ValueError):
                giornaliero.forecast_records(data, 0, date(2026, 10, 1), date(2026, 10, 1))


class QualityTests(unittest.TestCase):
    def setUp(self):
        self.cfg = load_config()["giornaliero"]
        self.now = datetime(2026, 10, 19, 12, tzinfo=timezone.utc)

    def test_physical_limits_nan_stale_station_and_original_preserved(self):
        t = ts("2026-10-18T00:00")
        original = {t: record(), t + 3600: record(-1, float("nan"), 300)}
        clean, qc = giornaliero.quality(original, self.now, self.cfg)
        self.assertEqual(clean, {t: record()})
        self.assertTrue(qc["muta"])
        self.assertEqual(qc["ore_fuori_scala"][0]["campi"], ["speed", "gust", "dir"])
        self.assertEqual(original[t + 3600]["speed"], -1)

    def test_constant_sensor_warns_without_excluding_calm_and_gap_breaks_run(self):
        t = ts("2026-10-18T00:00")
        original = {t + i * 3600: record(0, 0, 0) for i in range(25)}
        clean, qc = giornaliero.quality(original, self.now, self.cfg)
        self.assertEqual(len(clean), 25)
        self.assertEqual(qc["sensore_costante_sospetto"][0]["ore"], 25)
        del original[t + 12 * 3600]
        self.assertFalse(giornaliero.quality(original, self.now, self.cfg)[1]["sensore_costante_sospetto"])
        empty = {t + i * 3600: record(None, None, None) for i in range(25)}
        self.assertFalse(giornaliero.quality(empty, self.now, self.cfg)[1]["sensore_costante_sospetto"])


class RunTests(unittest.TestCase):
    def setUp(self):
        annotations = mock.patch.object(giornaliero, "annotate")
        annotations.start()
        self.addCleanup(annotations.stop)
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name) / "dati"
        self.out = Path(self.tmp.name) / "rapporti"
        self.cfg = load_config()
        self.cfg["verifica"]["stazioni"] = self.cfg["verifica"]["stazioni"][:1]
        self.cfg["verifica"]["confronti"] = []
        self.cfg["models"] = self.cfg["models"][:2]
        self.now = datetime(2026, 10, 19, 12, tzinfo=timezone.utc)
        self.code = self.cfg["verifica"]["stazioni"][0]["codice"]
        t = ts("2026-10-18T01:00")
        self.t = t
        archivio.write_observed(self.root, self.code, {t: record(3), t + 3600: record(4)})
        archivio.write_forecast(self.root, self.code, "icon2i", {d: {t: record(0), t + 3600: record(9)} for d in range(3)})
        archivio.write_forecast(self.root, self.code, "iconeu", {d: {t: record(4)} for d in range(3)})

    def run_job(self, offline):
        return giornaliero.run(self.root, self.out, self.cfg, self.now, offline=offline)

    def test_offline_windows_common_sample_and_no_network(self):
        with mock.patch.object(giornaliero.arpal, "Archive", side_effect=AssertionError("rete")), mock.patch.object(giornaliero.openmeteo, "fetch_previous_runs", side_effect=AssertionError("rete")):
            result = self.run_job(True)
        station = result["stazioni"][0]
        self.assertEqual(station["finestre"]["30"]["ore_valide"], 2)
        rows = [r for r in station["finestre"]["30"]["punteggi"] if r["campione"] == "comune" and r["settore"] is None]
        self.assertEqual({r["n"] for r in rows}, {1})
        self.assertTrue(all(r["n_dir"] == 1 for r in rows))  # previsto calmo non elimina l'ora
        self.assertFalse((self.root / "stato.json").exists())
        self.assertTrue((self.out / "giornaliero.md").exists())

    def test_all_network_failures_keep_cache_and_model_membership(self):
        with mock.patch.object(giornaliero.arpal, "Archive", side_effect=OSError("ARPAL")), mock.patch.object(giornaliero.openmeteo, "fetch_previous_runs", side_effect=OSError("OM")):
            result = self.run_job(False)
        self.assertEqual(len(archivio.read_observed(self.root, self.code)), 2)
        self.assertTrue(any("ARPAL non aggiornato" in w for w in result["avvisi"]))
        self.assertEqual(json.loads((self.root / "stato.json").read_text())["ricarica_arpal"], {})
        # Un modello totalmente mancante non deve far apparire un falso campione comune.
        next((self.root / "previsioni" / "iconeu").glob("*.csv")).unlink()
        result = self.run_job(True)
        rows = result["stazioni"][0]["finestre"]["30"]["punteggi"]
        self.assertFalse(any(r["campione"] == "comune" for r in rows))

    def test_monthly_refresh_marked_only_after_complete_response(self):
        with mock.patch.object(giornaliero, "update_observed", return_value=({self.t: record()}, True)) as update, mock.patch.object(giornaliero.arpal, "Archive"), mock.patch.object(giornaliero, "update_forecast", return_value=({d: {} for d in range(3)}, True)):
            self.run_job(False)
            self.assertEqual(update.call_args.args[2], date(2025, 10, 19))
            self.run_job(False)
            self.assertEqual(update.call_args.args[2], date(2026, 10, 9))
        self.assertEqual(json.loads((self.root / "stato.json").read_text())["ricarica_arpal"][self.code], "2026-10")

    def test_snapshot_retains_old_coefficients_and_records_detection(self):
        path = Path(self.tmp.name) / "mos.json"
        path.write_text('{"versione":1,"generated":1}')
        a = giornaliero.snapshot_coefficients(path, self.out)
        path.write_text('{"versione":1,"generated":2}')
        b = giornaliero.snapshot_coefficients(path, self.out)
        self.assertNotEqual(a["sha256"], b["sha256"])
        self.assertEqual(json.loads((self.out / a["file"]).read_text())["generated"], 1)

    def test_quota_real_configuration(self):
        self.assertEqual(giornaliero.quota(load_config())["totale"], 8280)


if __name__ == "__main__":
    unittest.main()
