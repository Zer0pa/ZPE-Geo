#!/usr/bin/env python3
"""Download, convert, and benchmark real-world geospatial extracts."""

from __future__ import annotations

import csv
import io
import json
import sys
import tempfile
import urllib.request
import zipfile
from collections import defaultdict
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import osmium
import pyarrow.parquet as pq
import zstandard as zstd

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.run_benchmark import benchmark_fixture_path, write_json
from zpe_geo.utils import ensure_dir

REPO_ROOT = ROOT.parent
REAL_WORLD_FIXTURE_ROOT = ROOT / "fixtures" / "real_world"
REAL_WORLD_ARTIFACT_ROOT = REPO_ROOT / "proofs" / "artifacts" / "real_world_benchmarks"

NOAA_URL = "https://coast.noaa.gov/htdata/CMSP/AISDataHandler/2025/ais-2025-01-01.csv.zst"
GEOLIFE_URL = (
    "https://download.microsoft.com/download/f/4/8/"
    "f4894aa5-fdbc-481e-9285-d5f8c4c4f039/Geolife%20Trajectories%201.3.zip"
)
NYC_URL = "https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_2026-01.parquet"
OSM_URL = "https://download.geofabrik.de/europe/monaco-latest.osm.pbf"


@dataclass(frozen=True)
class DatasetStatus:
    dataset: str
    status: str
    detail: str
    source_url: str
    fixture_path: str | None = None
    benchmark_path: str | None = None


def download(url: str, dest: Path) -> Path:
    if dest.exists():
        return dest
    ensure_dir(dest.parent)
    with urllib.request.urlopen(url, timeout=120) as response, dest.open("wb") as handle:
        while True:
            chunk = response.read(1024 * 1024)
            if not chunk:
                break
            handle.write(chunk)
    return dest


def write_markdown(path: Path, statuses: list[DatasetStatus]) -> None:
    lines = [
        "# Real-World Dataset Acquisition",
        "",
        "| Dataset | Status | Detail | Fixture | Benchmark |",
        "| --- | --- | --- | --- | --- |",
    ]
    for status in statuses:
        fixture = status.fixture_path or "-"
        benchmark = status.benchmark_path or "-"
        lines.append(
            f"| {status.dataset} | {status.status} | {status.detail} | {fixture} | {benchmark} |"
        )
    lines.append("")
    path.write_text("\n".join(lines), encoding="utf-8")


def build_noaa_fixture(download_root: Path) -> Path:
    source_path = download(NOAA_URL, download_root / "ais-2025-01-01.csv.zst")
    out_path = REAL_WORLD_FIXTURE_ROOT / "noaa_ais_day_extract.json"

    trajectories_by_mmsi: dict[str, list[dict[str, Any]]] = defaultdict(list)
    first_seen: list[str] = []
    rows_scanned = 0

    with source_path.open("rb") as compressed:
        reader = zstd.ZstdDecompressor().stream_reader(compressed)
        text = io.TextIOWrapper(reader, encoding="utf-8", newline="")
        csv_reader = csv.DictReader(text)
        for row in csv_reader:
            rows_scanned += 1
            mmsi = (row.get("mmsi") or "").strip()
            lat = row.get("latitude")
            lon = row.get("longitude")
            stamp = row.get("base_date_time")
            if not (mmsi and lat and lon and stamp):
                continue
            if mmsi not in trajectories_by_mmsi:
                first_seen.append(mmsi)
            points = trajectories_by_mmsi[mmsi]
            if len(points) >= 20:
                continue
            timestamp = datetime.strptime(stamp, "%Y-%m-%d %H:%M:%S").replace(
                tzinfo=timezone.utc
            )
            points.append(
                {
                    "t": timestamp.timestamp(),
                    "timestamp_iso": timestamp.isoformat(),
                    "lat": float(lat),
                    "lon": float(lon),
                    "speed": float(row.get("sog") or 0.0),
                    "cog": float(row.get("cog") or 0.0),
                    "mmsi": int(mmsi),
                }
            )
            ready = sum(1 for key in first_seen if len(trajectories_by_mmsi[key]) >= 12)
            if ready >= 5 and rows_scanned >= 10000:
                break

    trajectories = []
    for mmsi in first_seen:
        points = sorted(trajectories_by_mmsi[mmsi], key=lambda point: point["t"])
        if len(points) < 12:
            continue
        trajectories.append(
            {
                "trajectory_id": f"noaa_{mmsi}",
                "coord_system": "wgs84",
                "domain": "noaa_ais",
                "points": points[:20],
            }
        )
        if len(trajectories) == 5:
            break

    if not trajectories:
        raise RuntimeError("failed to extract NOAA AIS trajectories")

    payload = {
        "metadata": {
            "source_url": NOAA_URL,
            "reference": "NOAA MarineCadastre daily AIS CSV extract",
            "license": "public domain (per MarineCadastre FAQ)",
            "rows_scanned": rows_scanned,
            "trajectory_count": len(trajectories),
        },
        "trajectories": trajectories,
    }
    write_json(out_path, payload)
    return out_path


def build_geolife_fixture(download_root: Path) -> Path:
    source_path = download(GEOLIFE_URL, download_root / "geolife.zip")
    out_path = REAL_WORLD_FIXTURE_ROOT / "geolife_extract.json"

    trajectories = []
    with zipfile.ZipFile(source_path) as archive:
        plt_names = sorted(
            name for name in archive.namelist() if name.endswith(".plt") and "/Trajectory/" in name
        )
        for member in plt_names:
            with archive.open(member) as handle:
                lines = handle.read().decode("utf-8", "ignore").splitlines()[6:]
            points = []
            for line in lines:
                parts = [part.strip() for part in line.split(",")]
                if len(parts) < 7:
                    continue
                stamp = datetime.strptime(
                    f"{parts[5]}T{parts[6]}", "%Y-%m-%dT%H:%M:%S"
                ).replace(tzinfo=timezone.utc)
                points.append(
                    {
                        "t": stamp.timestamp(),
                        "timestamp_iso": stamp.isoformat(),
                        "lat": float(parts[0]),
                        "lon": float(parts[1]),
                        "speed": 0.0,
                    }
                )
                if len(points) == 32:
                    break
            if len(points) < 12:
                continue
            trajectories.append(
                {
                    "trajectory_id": member.replace("/", "_"),
                    "coord_system": "wgs84",
                    "domain": "geolife",
                    "points": points,
                }
            )
            if len(trajectories) == 5:
                break

    if not trajectories:
        raise RuntimeError("failed to extract GeoLife trajectories")

    payload = {
        "metadata": {
            "source_url": GEOLIFE_URL,
            "reference": "Microsoft Research GeoLife GPS Trajectories 1.3",
            "trajectory_count": len(trajectories),
        },
        "trajectories": trajectories,
    }
    write_json(out_path, payload)
    return out_path


def inspect_nyc_schema(download_root: Path) -> tuple[list[str], Path]:
    source_path = download(NYC_URL, download_root / "yellow_tripdata_2026-01.parquet")
    parquet = pq.ParquetFile(source_path)
    return parquet.schema.names, source_path


class WayCollector(osmium.SimpleHandler):
    def __init__(self) -> None:
        super().__init__()
        self.trajectories: list[dict[str, Any]] = []

    def way(self, way: osmium.osm.Way) -> None:
        if len(self.trajectories) >= 5 or "highway" not in way.tags:
            return
        points = []
        for idx, node in enumerate(way.nodes):
            if not node.location.valid():
                continue
            points.append(
                {
                    "t": float(idx),
                    "lat": float(node.location.lat),
                    "lon": float(node.location.lon),
                    "speed": 0.0,
                }
            )
            if len(points) == 32:
                break
        if len(points) < 12:
            return
        self.trajectories.append(
            {
                "trajectory_id": f"osm_way_{way.id}",
                "coord_system": "wgs84",
                "domain": "osm",
                "tags": {"highway": way.tags.get("highway", "")},
                "points": points,
            }
        )


def build_osm_fixture(download_root: Path) -> Path:
    source_path = download(OSM_URL, download_root / "monaco-latest.osm.pbf")
    out_path = REAL_WORLD_FIXTURE_ROOT / "osm_monaco_way_extract.json"

    collector = WayCollector()
    collector.apply_file(str(source_path), locations=True)
    if not collector.trajectories:
        raise RuntimeError("failed to extract OSM way trajectories")

    payload = {
        "metadata": {
            "source_url": OSM_URL,
            "reference": "Geofabrik Monaco latest extract",
            "trajectory_count": len(collector.trajectories),
        },
        "trajectories": collector.trajectories,
    }
    write_json(out_path, payload)
    return out_path


def build_benchmark(fixture_path: Path) -> Path:
    result = benchmark_fixture_path(fixture_path)
    out_path = REAL_WORLD_ARTIFACT_ROOT / f"{fixture_path.stem}_benchmark.json"
    write_json(out_path, result)
    return out_path


def main() -> None:
    ensure_dir(REAL_WORLD_FIXTURE_ROOT)
    ensure_dir(REAL_WORLD_ARTIFACT_ROOT)
    statuses: list[DatasetStatus] = []

    with tempfile.TemporaryDirectory(prefix="zpe-geo-real-world-") as tmpdir:
        download_root = Path(tmpdir)

        noaa_fixture = build_noaa_fixture(download_root)
        noaa_benchmark = build_benchmark(noaa_fixture)
        statuses.append(
            DatasetStatus(
                dataset="NOAA AIS",
                status="completed",
                detail="Extracted five real vessel trajectories from the official 2025-01-01 daily CSV.",
                source_url=NOAA_URL,
                fixture_path=str(noaa_fixture.relative_to(REPO_ROOT)),
                benchmark_path=str(noaa_benchmark.relative_to(REPO_ROOT)),
            )
        )

        geolife_fixture = build_geolife_fixture(download_root)
        geolife_benchmark = build_benchmark(geolife_fixture)
        statuses.append(
            DatasetStatus(
                dataset="GeoLife GPS Trajectories",
                status="completed",
                detail="Extracted five track files from the official GeoLife 1.3 ZIP.",
                source_url=GEOLIFE_URL,
                fixture_path=str(geolife_fixture.relative_to(REPO_ROOT)),
                benchmark_path=str(geolife_benchmark.relative_to(REPO_ROOT)),
            )
        )

        nyc_columns, _nyc_source = inspect_nyc_schema(download_root)
        write_json(REAL_WORLD_ARTIFACT_ROOT / "nyc_taxi_schema_columns.json", nyc_columns)
        required_nyc_columns = {
            "pickup_latitude",
            "pickup_longitude",
            "dropoff_latitude",
            "dropoff_longitude",
        }
        if required_nyc_columns.issubset(set(nyc_columns)):
            statuses.append(
                DatasetStatus(
                    dataset="NYC Taxi Trip Records",
                    status="blocked",
                    detail="Schema unexpectedly exposed lat/lon columns, but extraction support is not implemented.",
                    source_url=NYC_URL,
                )
            )
        else:
            statuses.append(
                DatasetStatus(
                    dataset="NYC Taxi Trip Records",
                    status="blocked",
                    detail="Official 2026 parquet lacks direct pickup/dropoff lat/lon columns; only zone-style fields are available.",
                    source_url=NYC_URL,
                )
            )

        osm_fixture = build_osm_fixture(download_root)
        osm_benchmark = build_benchmark(osm_fixture)
        statuses.append(
            DatasetStatus(
                dataset="OpenStreetMap Node Dumps",
                status="completed",
                detail="Extracted five Monaco highway ways from the official Geofabrik PBF using osmium.",
                source_url=OSM_URL,
                fixture_path=str(osm_fixture.relative_to(REPO_ROOT)),
                benchmark_path=str(osm_benchmark.relative_to(REPO_ROOT)),
            )
        )

        statuses.append(
            DatasetStatus(
                dataset="Argoverse 2 Motion Forecasting",
                status="blocked",
                detail="Official source requires registration, so no unattended download was possible.",
                source_url="https://www.argoverse.org/av2.html",
            )
        )
        statuses.append(
            DatasetStatus(
                dataset="Porto Taxi Trajectories",
                status="blocked",
                detail="Official Kaggle distribution requires account-authenticated access.",
                source_url="https://www.kaggle.com/datasets/crailtap/uber-taxi-for-porto-portugal",
            )
        )

    report = {
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "statuses": [status.__dict__ for status in statuses],
    }
    write_json(REAL_WORLD_ARTIFACT_ROOT / "acquisition_report.json", report)
    write_markdown(REAL_WORLD_ARTIFACT_ROOT / "README.md", statuses)


if __name__ == "__main__":
    main()
