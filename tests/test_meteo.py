"""Test: python -m unittest discover -s tests"""
import io
import json
import tempfile
import unittest
import urllib.error
from pathlib import Path
from unittest import mock

from meteo import openmeteo
from meteo.build import build, wind_frames
from meteo.config import build_grid
from meteo.wind import (
    beaufort,
    interpolate,
    interpolate_wind,
    speed_dir_to_uv,
    uv_to_speed_dir,
    wind_name,
)


class TestWind(unittest.TestCase):
    def test_libeccio_blows_towards_north_east(self):
        u, v = speed_dir_to_uv(10, 225)  # da SW
        self.assertGreater(u, 0)
        self.assertGreater(v, 0)

    def test_roundtrip(self):
        for d in (0, 45, 135, 225, 315, 359):
            s, d2 = uv_to_speed_dir(*speed_dir_to_uv(12.5, d))
            self.assertAlmostEqual(s, 12.5, places=6)
            self.assertAlmostEqual((d2 - d + 180) % 360 - 180, 0, places=6)

    def test_names(self):
        self.assertEqual(wind_name(0), "Tramontana")
        self.assertEqual(wind_name(225), "Libeccio")
        self.assertEqual(wind_name(315), "Maestrale")
        self.assertEqual(wind_name(350), "Tramontana")

    def test_beaufort(self):
        self.assertEqual(beaufort(0.5), 0)
        self.assertEqual(beaufort(15), 4)
        self.assertEqual(beaufort(25), 6)
        self.assertEqual(beaufort(70), 12)

    def test_interpolate_half_hour(self):
        out = interpolate([0, 3600], [10, 20], [0, 1800, 3600, 5400])
        self.assertEqual(out, [10, 15, 20, None])

    def test_interpolate_gap(self):
        self.assertEqual(interpolate([0, 3600], [None, 20], [1800]), [None])

    def test_direction_through_north(self):
        # 350° -> 10°: a metà deve essere ~0°, non 180°
        s, d = interpolate_wind([0, 3600], [10, 10], [350, 10], [1800])
        self.assertAlmostEqual((d[0] + 180) % 360 - 180, 0, places=6)
        self.assertGreater(s[0], 9.5)


class TestGrid(unittest.TestCase):
    def test_order_north_west_first(self):
        g = build_grid({"lon_min": 8, "lon_max": 9, "lat_min": 43, "lat_max": 44, "grid_step": 0.5})
        self.assertEqual((g.nx, g.ny), (3, 3))
        self.assertEqual(g.points()[0], (44.0, 8.0))
        self.assertEqual(g.points()[-1], (43.0, 9.0))


class TestOpenMeteoParsing(unittest.TestCase):
    def test_multi_location_and_chunks(self):
        pts = [(44.0 + i * 0.01, 9.0) for i in range(150)]
        calls = []

        def fake_get(url, params):
            calls.append(params)
            n = len(params["latitude"].split(","))
            item = {"hourly": {"time": [0, 3600], "wind_speed_10m": [5, 6], "wind_direction_10m": [200, 210]}}
            return [item] * n if n > 1 else item

        with mock.patch.object(openmeteo, "_get", side_effect=fake_get):
            out = openmeteo.fetch_hourly(pts, ["wind_speed_10m", "wind_direction_10m"], "icon_eu", 4)
        self.assertEqual(len(out), 150)
        self.assertEqual(len(calls), 2)
        self.assertEqual(calls[0]["models"], "icon_eu")
        self.assertEqual(calls[0]["wind_speed_unit"], "kn")

    def test_minutely_limit_waits_a_minute(self):
        body = b'{"error":true,"reason":"Minutely API request limit exceeded. Please try again in one minute."}'
        err = urllib.error.HTTPError("u", 429, "Too Many Requests", {}, io.BytesIO(body))
        ok = mock.MagicMock()
        ok.__enter__.return_value = io.BytesIO(b'{"hourly": {}}')
        with mock.patch.object(openmeteo.urllib.request, "urlopen", side_effect=[err, ok]), \
                mock.patch.object(openmeteo.time, "sleep") as sleep:
            self.assertEqual(openmeteo._get("https://x", {}), {"hourly": {}})
        sleep.assert_called_once_with(openmeteo.MINUTE_WAIT)

    def test_wind_frames_shape(self):
        series = [{"time": [0, 3600], "wind_speed_10m": [10, 10], "wind_direction_10m": [270, 270]}] * 4
        u, v = wind_frames(series, [0, 1800, 3600])
        self.assertEqual(len(u), 3)
        self.assertEqual(len(u[0]), 4)
        self.assertGreater(u[1][0], 5)  # Ponente: soffia verso est, ~5.1 m/s


class TestDemoBuild(unittest.TestCase):
    def test_demo_files(self):
        with tempfile.TemporaryDirectory() as d:
            meta = build(Path(d), demo=True)
            files = sorted(p.name for p in Path(d).iterdir())
            self.assertIn("meta.json", files)
            self.assertIn("spots.json", files)
            w = json.loads((Path(d) / "wind_icon2i.json").read_text())
            self.assertEqual(len(w["u"]), len(meta["times"]))
            self.assertEqual(len(w["u"][0]), w["nx"] * w["ny"])


if __name__ == "__main__":
    unittest.main()
