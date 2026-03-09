"""H3 integration bridge with official backend preference and deterministic fallback."""

from __future__ import annotations

import math
import sys
from typing import Any

from .geo import haversine_m
from .paths import preferred_third_party_root


def _load_h3() -> tuple[str, Any]:
    lane_vendor = preferred_third_party_root()
    if lane_vendor.exists():
        sys.path.insert(0, str(lane_vendor))
    try:
        import h3  # type: ignore

        return "official_h3", h3
    except Exception:
        return "h3lite", None


class H3Bridge:
    def __init__(self, resolution: int = 9) -> None:
        self.resolution = resolution
        self.backend, self._h3 = _load_h3()

    def latlon_to_cell(self, lat: float, lon: float, resolution: int | None = None) -> str:
        res = self.resolution if resolution is None else resolution
        if self.backend == "official_h3":
            assert self._h3 is not None
            return str(self._h3.latlng_to_cell(lat, lon, res))
        # deterministic fallback; not equivalent to real H3 cell IDs.
        scale = 2 ** res
        q = int(round((lon + 180.0) * scale))
        r = int(round((lat + 90.0) * scale / 0.866025403784))
        return f"h3lite:{res}:{q}:{r}"

    def cell_to_latlon(self, cell: str) -> tuple[float, float]:
        if self.backend == "official_h3":
            assert self._h3 is not None
            lat, lon = self._h3.cell_to_latlng(cell)
            return float(lat), float(lon)
        _, res, q, r = cell.split(":")
        scale = 2 ** int(res)
        lon = (int(q) / scale) - 180.0
        lat = (int(r) * 0.866025403784 / scale) - 90.0
        return lat, lon

    def encode_cell_path(self, trajectory: dict[str, Any], resolution: int | None = None) -> list[str]:
        res = self.resolution if resolution is None else resolution
        cells: list[str] = []
        if trajectory.get("coord_system") != "wgs84":
            raise ValueError("H3 bridge expects WGS84 trajectory")
        for p in trajectory["points"]:
            cell = self.latlon_to_cell(p["lat"], p["lon"], res)
            if not cells or cells[-1] != cell:
                cells.append(cell)
        return cells

    def roundtrip_consistent(
        self,
        trajectory: dict[str, Any],
        resolutions: list[int],
        drift_threshold_m: float = 180.0,
    ) -> dict[str, Any]:
        if trajectory.get("coord_system") != "wgs84":
            raise ValueError("H3 roundtrip requires WGS84 trajectory")
        checks: list[dict[str, Any]] = []
        failures = 0
        for res in resolutions:
            path = self.encode_cell_path(trajectory, resolution=res)
            per_res_failures = 0
            drift_max = 0.0
            # Validate each point->cell->centroid->cell cycle and centroid drift.
            for p in trajectory["points"]:
                cell = self.latlon_to_cell(p["lat"], p["lon"], resolution=res)
                lat, lon = self.cell_to_latlon(cell)
                recell = self.latlon_to_cell(lat, lon, resolution=res)
                if recell != cell:
                    per_res_failures += 1
                drift = haversine_m(p["lat"], p["lon"], lat, lon)
                drift_max = max(drift_max, drift)
            failures += per_res_failures
            checks.append(
                {
                    "resolution": res,
                    "cell_count": len(path),
                    "max_reference_drift_m": drift_max,
                    "roundtrip_failures": per_res_failures,
                    "roundtrip_ok": per_res_failures == 0 and drift_max <= drift_threshold_m,
                }
            )
        return {
            "backend": self.backend,
            "resolutions": resolutions,
            "failures": failures,
            "checks": checks,
            "all_consistent": failures == 0 and all(c["roundtrip_ok"] for c in checks),
        }
