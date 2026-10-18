"""Test del MOS (fase 2). Dati sintetici, nessun accesso alla rete."""
import json
import math
import random
import unittest

from meteo.mos import (
    add_equations,
    apply_correction,
    assess,
    block_bootstrap,
    build_samples,
    choose_direction,
    direction_sources,
    features,
    fit,
    make_spec,
    mean_wind,
    normal_equations,
    ridge,
    ridge_from_normal,
    shrunk_median,
    solve,
    train_correction,
)
from meteo.wind import KNOT_MS, WIND_NAMES, wind_name


def synthetic(n=3000, seed=0, rot=20.0):
    """Osservato = 1 + 0.8·previsto + brezza diurna; direzione ruotata di `rot`; da Libeccio.

    La raffica osservata è 1.8 volte la velocità osservata; quella prevista è 1.5·previsto
    più un disturbo indipendente, così non è collineare con la velocità prevista.
    """
    rng = random.Random(seed)
    observed, forecast = {}, {}
    for i in range(n):
        t = i * 3600
        f = rng.uniform(8, 20)  # osservato sempre sopra la soglia di direzione
        o = 1 + 0.8 * f + 2 * math.sin(2 * math.pi * ((t % 86400) / 3600) / 24)
        forecast[t] = {"speed": f * KNOT_MS, "dir": 225.0, "gust": (1.5 * f + rng.uniform(-1, 1)) * KNOT_MS}
        observed[t] = {"speed": o * KNOT_MS, "dir": 225.0 + rot, "gust": 1.8 * o * KNOT_MS}
    return observed, forecast


class TestAlgebra(unittest.TestCase):
    def test_solve(self):
        x = solve([[2, 1], [1, 3]], [3, 5])
        self.assertAlmostEqual(x[0], 0.8)
        self.assertAlmostEqual(x[1], 1.4)

    def test_ridge_pulls_to_prior(self):
        xs, ys = [[1, 1], [1, 2], [1, 3]], [2, 4, 6]
        free = ridge(xs, ys, 1e-9, [0, 0])
        self.assertAlmostEqual(free[1], 2, places=5)
        held = ridge(xs, ys, 1e9, [5, -1])
        self.assertAlmostEqual(held[0], 5, places=3)
        self.assertAlmostEqual(held[1], -1, places=3)

    def test_normal_equations_add_up(self):
        xs = [[1, 2], [1, 3], [1, 5], [1, 7]]
        ys = [1.0, 2.0, 4.0, 5.0]
        whole = normal_equations(xs, ys)
        parts = add_equations([normal_equations(xs[:2], ys[:2]), normal_equations(xs[2:], ys[2:]), None])
        for ra, rb in zip(whole[0], parts[0]):
            self.assertEqual(ra, rb)
        self.assertEqual(whole[1], parts[1])
        self.assertEqual(ridge_from_normal(*whole, 1.0, [0, 0]), ridge(xs, ys, 1.0, [0, 0]))


class TestWindHelpers(unittest.TestCase):
    def test_features_hour_harmonics(self):
        row = features([["m", "vel"]], 6 * 3600, {"m": {"vel": 10.0}})  # 06 UTC: seno al massimo
        self.assertEqual(row[:2], [1.0, 10.0])
        self.assertAlmostEqual(row[2], 1.0)
        self.assertAlmostEqual(row[3], 0.0, places=9)

    def test_mean_wind_through_north(self):
        _, d = mean_wind([(10, 350), (10, 10)])
        self.assertAlmostEqual((d + 180) % 360 - 180, 0, places=6)

    def test_shrunk_median_is_robust_and_shrunk(self):
        self.assertEqual(shrunk_median([]), 0.0)
        many = [20.0] * 200 + [-170.0] * 10  # i pochi valori anomali non spostano la mediana
        self.assertAlmostEqual(shrunk_median(many), 20 * 210 / 260, places=6)
        self.assertLess(shrunk_median([20.0] * 5), 2.0)  # poche ore: quasi nessuna rotazione

    def test_direction_sources(self):
        self.assertEqual(direction_sources(["icon2i"]), [["icon2i"]])
        self.assertEqual(
            direction_sources(["icon2i", "iconeu", "ecmwf"]),
            [["icon2i"], ["iconeu"], ["ecmwf"], ["icon2i", "iconeu", "ecmwf"], ["icon2i", "iconeu"]],
        )


class TestSamples(unittest.TestCase):
    def test_needs_every_model_and_gusts_when_asked(self):
        observed, forecast = synthetic(10)
        partial = {t: v for t, v in forecast.items() if t != 0}
        self.assertEqual(len(build_samples(observed, {"a": forecast, "b": partial}, "vel")), 9)
        no_gust = {t: {**v, "gust": None} for t, v in forecast.items()}
        self.assertEqual(len(build_samples(observed, {"a": no_gust}, "vel")), 10)
        self.assertEqual(len(build_samples(observed, {"a": no_gust}, "raf")), 0)


class TestFit(unittest.TestCase):
    def test_recovers_known_relation_and_rotation(self):
        observed, forecast = synthetic()
        data = build_samples(observed, {"icon2i": forecast}, "vel")
        corr = fit(data, make_spec("vel", ["icon2i"]), ["icon2i"], 3, 4, {"fonte": ["icon2i"], "ruota": True})
        beta = corr["settori"]["Libeccio"]
        self.assertAlmostEqual(beta[0], 1, places=3)
        self.assertAlmostEqual(beta[1], 0.8, places=3)
        self.assertAlmostEqual(beta[2], 2, places=3)
        n = corr["ore_settore"]["Libeccio"]
        self.assertAlmostEqual(corr["direzione"]["rotazione"]["Libeccio"], 20 * n / (n + 50), places=3)  # attenuata
        p = apply_correction(corr, data[0]["t"], data[0]["fc"])
        self.assertAlmostEqual(p["vel"], data[0]["obs"]["vel"], places=3)

    def test_empty_sector_falls_back_to_pool(self):
        observed, forecast = synthetic(500)
        data = build_samples(observed, {"icon2i": forecast}, "vel")
        corr = fit(data, make_spec("vel", ["icon2i"]), ["icon2i"], 30, 4, {"fonte": ["icon2i"], "ruota": True})
        self.assertEqual(corr["settori"]["Tramontana"], corr["pool"])
        self.assertEqual(corr["direzione"]["rotazione"]["Tramontana"], 0)

    def test_without_rotation_direction_is_untouched(self):
        observed, forecast = synthetic(500)
        data = build_samples(observed, {"icon2i": forecast}, "vel")
        corr = fit(data, make_spec("vel", ["icon2i"]), ["icon2i"], 30, 4, {"fonte": ["icon2i"], "ruota": False})
        self.assertEqual(apply_correction(corr, 0, data[0]["fc"])["dir"], 225.0)

    def test_json_roundtrip_gives_same_numbers(self):
        """Ciò che si valuta è ciò che si pubblica."""
        observed, forecast = synthetic(800)
        for q in ("vel", "raf"):
            data = build_samples(observed, {"icon2i": forecast}, q)
            direzione = {"fonte": ["icon2i"], "ruota": True} if q == "vel" else None
            corr = fit(data, make_spec(q, ["icon2i"]), ["icon2i"], 30, 4, direzione)
            back = json.loads(json.dumps(corr))
            for s in data[:50]:
                self.assertEqual(apply_correction(corr, s["t"], s["fc"]), apply_correction(back, s["t"], s["fc"]))

    def test_value_never_negative(self):
        corr = {"grandezza": "raf", "ingressi": [["m", "vel"]], "fonte": ["m"], "settori": {"Libeccio": [-50, 0, 0, 0]}}
        self.assertEqual(apply_correction(corr, 0, {"m": {"vel": 5.0, "dir": 225.0}})["raf"], 0)

    def test_gust_model_learns_from_speed_not_from_noise(self):
        observed, forecast = synthetic()
        data = build_samples(observed, {"icon2i": forecast}, "raf")
        train, test = data[:2000], data[2000:]
        corr = train_correction(train, make_spec("raf", ["icon2i"]), [3, 30], 4)
        ev = assess(corr, test, 4)
        self.assertLess(ev["mos"]["mae"], 0.3)  # grezzo: raffica prevista sbagliata di ~7 kn
        self.assertGreater(ev["guadagno_mae"], 0.9)
        self.assertLess(ev["delta_mae_ic95"][1], 0)


class TestDirectionChoice(unittest.TestCase):
    def _two_models(self, bias=0.0, n=3000, seed=1):
        """Modello a: direzione esatta (più `bias`); modello b: direzione a caso."""
        rng = random.Random(seed)
        observed, a, b = {}, {}, {}
        for i in range(n):
            t = i * 3600
            d = rng.uniform(0, 360)
            observed[t] = {"speed": 10 * KNOT_MS, "dir": d % 360, "gust": None}
            a[t] = {"speed": 10 * KNOT_MS, "dir": (d - bias) % 360, "gust": None}
            b[t] = {"speed": 10 * KNOT_MS, "dir": rng.uniform(0, 360), "gust": None}
        return build_samples(observed, {"a": a, "b": b}, "vel")

    def test_picks_the_accurate_model_and_no_rotation(self):
        data = self._two_models()
        fonte, ruota = choose_direction(data[:2400], data[2400:], ["a", "b"], 4)
        self.assertEqual(fonte, ["a"])
        self.assertFalse(ruota)

    def test_rotates_when_there_is_a_systematic_error(self):
        data = self._two_models(bias=25.0)
        fonte, ruota = choose_direction(data[:2400], data[2400:], ["a", "b"], 4)
        self.assertEqual(fonte, ["a"])
        self.assertTrue(ruota)


class TestSeparateChoices(unittest.TestCase):
    def test_direction_and_sector_sources_are_chosen_separately(self):
        """Il modello a ha la direzione esatta; ma la velocità osservata dipende dal settore del modello b."""
        rng = random.Random(3)
        observed, a, b = {}, {}, {}
        for i in range(4000):
            t = i * 3600
            d, db, f = rng.uniform(0, 360), rng.uniform(0, 360), rng.uniform(8, 20)
            o = f + 3 * WIND_NAMES.index(wind_name(db))
            observed[t] = {"speed": o * KNOT_MS, "dir": d, "gust": None}
            a[t] = {"speed": f * KNOT_MS, "dir": d, "gust": None}
            b[t] = {"speed": f * KNOT_MS, "dir": db, "gust": None}
        data = build_samples(observed, {"a": a, "b": b}, "vel")
        corr = train_correction(data, make_spec("vel", ["a", "b"]), [3, 30], 4)
        self.assertEqual(corr["direzione"]["fonte"], ["a"])  # per la direzione conta l'errore di direzione
        self.assertEqual(corr["fonte"], ["b"])  # per i settori conta l'errore di velocità


class TestAssess(unittest.TestCase):
    def test_speed_and_direction_gain_on_the_same_hours(self):
        observed, forecast = synthetic()
        data = build_samples(observed, {"icon2i": forecast}, "vel")
        corr = train_correction(data[:2000], make_spec("vel", ["icon2i"]), [3, 30], 4)
        ev = assess(corr, data[2000:], 4)
        self.assertGreater(ev["guadagno_mae"], 0.9)
        self.assertLess(ev["delta_mae_ic95"][1], 0)  # il MOS sbaglia meno, con certezza
        self.assertLess(ev["mos"]["mae_dir"], ev["grezzo"]["mae_dir"])
        self.assertEqual(ev["mos"]["n_dir"], ev["grezzo"]["n_dir"])  # stesse ore: maschera solo sull'osservato
        self.assertLess(ev["delta_mae_dir_ic95"][1], 0)

    def test_block_bootstrap(self):
        diffs = {d: [-1.0, -0.5] for d in range(30)}
        self.assertEqual(block_bootstrap(diffs), (-0.75, -0.75))
        self.assertEqual(block_bootstrap({}), (None, None))


if __name__ == "__main__":
    unittest.main()
