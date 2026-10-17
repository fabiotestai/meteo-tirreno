"""Lettura di config.toml e costruzione della griglia."""
from __future__ import annotations

import tomllib
from dataclasses import dataclass
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


@dataclass(frozen=True)
class Grid:
    lons: list[float]  # da ovest a est
    lats: list[float]  # da nord a sud (ordine richiesto dalla mappa)
    step: float

    @property
    def nx(self) -> int:
        return len(self.lons)

    @property
    def ny(self) -> int:
        return len(self.lats)

    def points(self) -> list[tuple[float, float]]:
        """(lat, lon) riga per riga, partendo da nord-ovest."""
        return [(lat, lon) for lat in self.lats for lon in self.lons]


def load_config(path: Path | None = None) -> dict:
    path = path or ROOT / "config.toml"
    with open(path, "rb") as f:
        return tomllib.load(f)


def _steps(start: float, stop: float, step: float) -> list[float]:
    n = int(round((stop - start) / step)) + 1
    return [round(start + i * step, 4) for i in range(n)]


def build_grid(area: dict) -> Grid:
    step = float(area["grid_step"])
    lons = _steps(area["lon_min"], area["lon_max"], step)
    lats = list(reversed(_steps(area["lat_min"], area["lat_max"], step)))
    return Grid(lons=lons, lats=lats, step=step)
