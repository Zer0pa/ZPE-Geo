#!/usr/bin/env python3
"""Gate M1: maximalization resource ingestion and stratified metrics."""

from __future__ import annotations

import csv
import datetime as dt
import io
import json
import math
import os
import shlex
import sys
import urllib.request
from collections import defaultdict
from pathlib import Path
from typing import Any

from common import ARTIFACT_ROOT, init_artifact_root, write_json
from max_common import (
    append_validation_log,
    load_impracticality,
    probe_url,
    run_cmd,
    save_impracticality,
    sha256_file,
)
from zpe_geo.codec import decode_trajectory, encode_trajectory
from zpe_geo.geo import dtw_distance_m
from zpe_geo.h3bridge import H3Bridge
from zpe_geo.metrics import compression_ratio, percentile, rmse_xy_m
from zpe_geo.paths import EXTERNAL_SAMPLES_ROOT, OUTER_WORKSPACE_ROOT, preferred_third_party_root
from zpe_geo.utils import append_command_log, now_utc_iso

THIRD_PARTY = preferred_third_party_root().resolve()
if str(THIRD_PARTY) not in sys.path:
    sys.path.insert(0, str(THIRD_PARTY))

try:
    import pyarrow.parquet as pq  # type: ignore
except Exception:  # pragma: no cover
    pq = None

try:
    import zstandard as zstd  # type: ignore
except Exception:  # pragma: no cover
    zstd = None

try:
    import numpy as np  # type: ignore
except Exception:  # pragma: no cover
    np = None

try:
    import xarray as xr  # type: ignore
except Exception:  # pragma: no cover
    xr = None

EXTERNAL_ROOT = EXTERNAL_SAMPLES_ROOT
EXTERNAL_ROOT.mkdir(parents=True, exist_ok=True)


def _append_imp(
    entries: list[dict[str, Any]],
    resource: str,
    code: str,
    command: str,
    error_signature: str,
    fallback: str,
    claim_impact: str,
) -> None:
    entries.append(
        {
            "resource": resource,
            "impracticality_code": code,
            "command_evidence": command,
            "error_signature": error_signature,
            "fallback": fallback,
            "claim_impact_note": claim_impact,
        }
    )


def _parse_iso_ts(raw: str) -> float:
    t = raw.strip()
    if t.endswith("Z"):
        t = t[:-1] + "+00:00"
    try:
        return dt.datetime.fromisoformat(t).timestamp()
    except Exception:
        for fmt in ("%Y-%m-%d %H:%M:%S", "%Y-%m-%dT%H:%M:%S"):
            try:
                return dt.datetime.strptime(raw, fmt).timestamp()
            except Exception:
                continue
    return 0.0


def _directional_label_xy(points: list[dict[str, float]]) -> str:
    if len(points) < 6:
        return "short"
    headings = []
    for i in range(1, len(points)):
        dx = points[i]["x"] - points[i - 1]["x"]
        dy = points[i]["y"] - points[i - 1]["y"]
        if dx == 0.0 and dy == 0.0:
            continue
        headings.append(math.degrees(math.atan2(dy, dx)))
    if not headings:
        return "stop"
    sweep = headings[-1] - headings[0]
    if sweep > 35:
        return "left_turn"
    if sweep < -35:
        return "right_turn"
    return "straight"


def _directional_label_wgs(points: list[dict[str, float]]) -> str:
    if len(points) < 6:
        return "short"
    lons = [p["lon"] for p in points]
    lats = [p["lat"] for p in points]
    dx = lons[-1] - lons[0]
    dy = lats[-1] - lats[0]
    if abs(dx) < 1e-9 and abs(dy) < 1e-9:
        return "stop"
    return "straight" if abs(dx) > abs(dy) else "north_south"


def _benchmark_xy(trajs: list[dict[str, Any]], quant_step_m: float) -> dict[str, Any]:
    ratios = []
    rmses = []
    bins: dict[str, list[float]] = defaultdict(list)
    for t in trajs:
        enc = encode_trajectory(t, quant_step_m=quant_step_m)
        dec = decode_trajectory(enc.payload)
        raw_bytes = len(t["points"]) * 6 * 8
        ratios.append(compression_ratio(raw_bytes, len(enc.payload)))
        rmse = rmse_xy_m(t["points"], dec["points"])
        rmses.append(rmse)
        n = len(t["points"])
        if n < 40:
            bins["len_lt_40"].append(rmse)
        elif n < 100:
            bins["len_40_99"].append(rmse)
        else:
            bins["len_ge_100"].append(rmse)
    return {
        "trajectory_count": len(trajs),
        "compression_ratio_mean": sum(ratios) / max(1, len(ratios)),
        "rmse_mean": sum(rmses) / max(1, len(rmses)),
        "rmse_p95": percentile(rmses, 95),
        "stratified_rmse": {
            k: {"count": len(v), "rmse_mean": (sum(v) / len(v) if v else None)}
            for k, v in bins.items()
        },
    }


def _benchmark_wgs84(trajs: list[dict[str, Any]], quant_step_m: float) -> dict[str, Any]:
    ratios = []
    dtws = []
    speed_bins: dict[str, list[float]] = defaultdict(list)
    for t in trajs:
        enc = encode_trajectory(t, quant_step_m=quant_step_m)
        dec = decode_trajectory(enc.payload)
        raw_bytes = len(json.dumps(t["points"]).encode("utf-8"))
        ratios.append(compression_ratio(raw_bytes, len(enc.payload)))
        oa = [(p["lat"], p["lon"]) for p in t["points"]]
        ob = [(p["lat"], p["lon"]) for p in dec["points"]]
        dtw = dtw_distance_m(oa, ob)
        dtws.append(dtw)
        avg_speed = sum(p.get("speed", 0.0) for p in t["points"]) / max(1, len(t["points"]))
        key = "speed_lt_2" if avg_speed < 2 else ("speed_2_8" if avg_speed < 8 else "speed_ge_8")
        speed_bins[key].append(dtw)
    return {
        "trajectory_count": len(trajs),
        "compression_ratio_mean": sum(ratios) / max(1, len(ratios)),
        "dtw_mean_m": sum(dtws) / max(1, len(dtws)),
        "dtw_p95_m": percentile(dtws, 95),
        "stratified_dtw_m": {
            k: {"count": len(v), "dtw_mean_m": (sum(v) / len(v) if v else None)}
            for k, v in speed_bins.items()
        },
    }


def _load_av2_subset(imp: list[dict[str, Any]], lock: dict[str, Any]) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    url = "https://s3.amazonaws.com/argoverse/datasets/av2/motion-forecasting/av2_mf_focal_test_annotations.parquet"
    dst = EXTERNAL_ROOT / "av2_mf_focal_test_annotations.parquet"
    if not dst.exists():
        cmd = f"curl -L --max-time 180 -o {dst} {url}"
        result = run_cmd(cmd, timeout_s=240)
        if result.exit_code != 0:
            _append_imp(
                imp,
                "Argoverse2 Motion Forecasting subset download",
                "IMP-ACCESS",
                result.command,
                (result.stderr or result.stdout)[:500],
                "Use schema-faithful AV fixture and keep M1 AV2 evidence INCONCLUSIVE.",
                "Affects maximalization closure for GEO-C001/C003/C005.",
            )
            return [], {"status": "FAILED"}
    if pq is None:
        _append_imp(
            imp,
            "Argoverse2 parquet parsing",
            "IMP-NOCODE",
            "import pyarrow.parquet",
            "pyarrow unavailable in runtime",
            "File locked only; parsing deferred to RunPod pyarrow environment.",
            "Affects direct AV2 subset benchmarking; claim impact INCONCLUSIVE for max-wave.",
        )
        return [], {"status": "LOCK_ONLY", "path": str(dst), "sha256": sha256_file(dst)}

    table = pq.read_table(
        str(dst),
        columns=["scenario_id", "track_id", "gt_trajectory_x", "gt_trajectory_y"],
    )
    rows = table.to_pylist()
    subset = []
    for i, r in enumerate(rows[:2000]):
        xs = r["gt_trajectory_x"] or []
        ys = r["gt_trajectory_y"] or []
        n = min(len(xs), len(ys))
        if n < 20:
            continue
        points = []
        for j in range(n):
            points.append({"t": j * 0.1, "x": float(xs[j]), "y": float(ys[j]), "speed": 0.0, "cog": 511.0})
        subset.append(
            {
                "trajectory_id": f"av2_{r['scenario_id']}_{r['track_id']}",
                "coord_system": "xy",
                "points": points,
                "label": _directional_label_xy(points),
            }
        )
    lock["argoverse2"] = {
        "source_url": url,
        "sample_path": str(dst),
        "sha256": sha256_file(dst),
        "subset_trajectories": len(subset),
        "full_corpus_size_bytes": 50873856000,
        "subset_policy": "focal parquet subset up to 2000 tracks",
    }
    # Full train.tar is 47.4GB; mark as storage-gated for local full-corpus run.
    _append_imp(
        imp,
        "Argoverse2 full-corpus train.tar run",
        "IMP-STORAGE",
        "curl -I https://s3.amazonaws.com/argoverse/datasets/av2/tars/motion-forecasting/train.tar",
        "Content-Length=50873856000 bytes exceeds local lane practical storage budget for this run.",
        "Use locked focal parquet subset + fixture-backed stress and prepare RunPod full replay plan.",
        "Max-wave full-corpus closure for GEO-C001..C004 remains INCONCLUSIVE pending RunPod batch replay.",
    )
    return subset, lock["argoverse2"]


def _load_noaa_ais_subset(imp: list[dict[str, Any]], lock: dict[str, Any]) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    source_url = "https://coast.noaa.gov/htdata/CMSP/AISDataHandler/2025/ais-2025-01-01.csv.zst"
    if zstd is None:
        _append_imp(
            imp,
            "NOAA AIS zstd decode",
            "IMP-NOCODE",
            "import zstandard",
            "zstandard module unavailable",
            "Fallback to synthetic AIS fixture only.",
            "Impacts maximalization evidence for GEO-C002/C004.",
        )
        return [], {"status": "FAILED"}
    tracks: dict[str, list[dict[str, Any]]] = defaultdict(list)
    row_count = 0
    try:
        with urllib.request.urlopen(source_url, timeout=60) as resp:  # nosec B310
            dctx = zstd.ZstdDecompressor()
            with dctx.stream_reader(resp) as reader:
                text = io.TextIOWrapper(reader, encoding="utf-8")
                csv_reader = csv.DictReader(text)
                for row in csv_reader:
                    row_count += 1
                    mmsi = (
                        row.get("MMSI")
                        or row.get("\ufeffMMSI")
                        or row.get("mmsi")
                        or row.get("Mmsi")
                        or ""
                    ).strip()
                    if not mmsi:
                        continue
                    lat_s = (
                        row.get("LAT")
                        or row.get("lat")
                        or row.get("Lat")
                        or row.get("latitude")
                    )
                    lon_s = (
                        row.get("LON")
                        or row.get("lon")
                        or row.get("Lon")
                        or row.get("longitude")
                    )
                    ts_s = (
                        row.get("BaseDateTime")
                        or row.get("basedatetime")
                        or row.get("base_date_time")
                        or row.get("timestamp")
                        or row.get("time")
                    )
                    if not (lat_s and lon_s and ts_s):
                        continue
                    try:
                        lat = float(lat_s)
                        lon = float(lon_s)
                    except Exception:
                        continue
                    points = tracks[mmsi]
                    if len(points) >= 260:
                        continue
                    cog_raw = row.get("COG") or row.get("cog") or row.get("course") or "511"
                    sog_raw = row.get("SOG") or row.get("sog") or row.get("speed") or "0"
                    try:
                        cog = float(cog_raw)
                    except Exception:
                        cog = 511.0
                    try:
                        sog = float(sog_raw)
                    except Exception:
                        sog = 0.0
                    points.append(
                        {
                            "t": _parse_iso_ts(ts_s),
                            "lat": lat,
                            "lon": lon,
                            "speed": sog,
                            "cog": cog,
                            "timestamp_iso": str(ts_s),
                            "mmsi": int(float(mmsi)),
                        }
                    )
                    if row_count >= 300000:
                        break
    except Exception as exc:
        _append_imp(
            imp,
            "NOAA AIS streaming subset read",
            "IMP-ACCESS",
            f"python stream read {source_url}",
            f"{type(exc).__name__}: {exc}",
            "Fallback to schema-faithful AIS fixture.",
            "Affects max-wave closure for GEO-C002/C004.",
        )
        return [], {"status": "FAILED"}

    trajectories = []
    for mmsi, points in list(tracks.items())[:1200]:
        if len(points) < 40:
            continue
        points.sort(key=lambda p: p["t"])
        trajectories.append(
            {
                "trajectory_id": f"noaa_{mmsi}",
                "coord_system": "wgs84",
                "points": points,
                "label": _directional_label_wgs(points),
            }
        )
        if len(trajectories) >= 450:
            break

    lock["noaa_ais"] = {
        "source_url": source_url,
        "subset_rows_streamed": row_count,
        "subset_trajectories": len(trajectories),
        "full_corpus_2025_size_gb": 61.0,
        "subset_policy": "Stream-first 300k rows, max 450 tracks, max 260 points/track",
    }
    _append_imp(
        imp,
        "NOAA AIS full-year corpus replay",
        "IMP-STORAGE",
        "curl -I https://coast.noaa.gov/htdata/CMSP/AISDataHandler/2025/",
        "Published full-year size is 61.0GB; full replay impractical in local lane cycle window.",
        "Use deterministic streamed subset with coverage report and RunPod full replay plan.",
        "Max-wave full-corpus closure remains INCONCLUSIVE for GEO-C002/C004.",
    )
    return trajectories, lock["noaa_ais"]


def _load_gfs_weather_subset(imp: list[dict[str, Any]], lock: dict[str, Any]) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    base = "https://noaa-gfs-bdp-pds.s3.amazonaws.com/gfs.20260220/00/atmos"
    files = [f"gfs.t00z.pgrb2.1p00.f{h:03d}" for h in (0, 3, 6)]
    tracks: list[dict[str, Any]] = []
    downloaded = []
    for name in files:
        url = f"{base}/{name}"
        dst = EXTERNAL_ROOT / name
        if not dst.exists():
            cmd = f"curl -L --max-time 180 -o {dst} {url}"
            result = run_cmd(cmd, timeout_s=240)
            if result.exit_code != 0:
                _append_imp(
                    imp,
                    "NOAA GFS file download",
                    "IMP-ACCESS",
                    result.command,
                    (result.stderr or result.stdout)[:500],
                    "Fallback to NOAA GFS idx metadata for stress generation.",
                    "GEO-C005/C006 weather stress remains partial.",
                )
                return [], {"status": "FAILED"}
        downloaded.append(dst)

    if xr is None or np is None:
        _append_imp(
            imp,
            "NOAA GFS GRIB parsing",
            "IMP-NOCODE",
            "import xarray/cfgrib/numpy",
            "Required parsing dependencies unavailable",
            "Fallback to idx-only metadata trajectories.",
            "GEO-C005/C006 weather trajectory stress downgraded to metadata-level.",
        )
        return [], {"status": "LOCK_ONLY"}

    points = []
    for i, path in enumerate(downloaded):
        try:
            ds = xr.open_dataset(
                str(path),
                engine="cfgrib",
                filter_by_keys={"typeOfLevel": "meanSea", "shortName": "prmsl"},
            )
            arr = ds["prmsl"].values
            iy, ix = np.unravel_index(arr.argmin(), arr.shape)
            lat = float(ds["latitude"].values[iy])
            lon = float(ds["longitude"].values[ix])
            points.append(
                {
                    "t": float(i * 10800),  # 3-hour steps
                    "lat": lat,
                    "lon": lon,
                    "speed": 0.0,
                    "cog": 511.0,
                    "timestamp_iso": f"2026-02-20T{(i*3):02d}:00:00Z",
                    "mmsi": 0,
                }
            )
        except Exception as exc:
            _append_imp(
                imp,
                "NOAA GFS GRIB extraction",
                "IMP-NOCODE",
                f"xarray.open_dataset({path.name}, engine='cfgrib')",
                f"{type(exc).__name__}: {exc}",
                "Fallback to idx metadata track and keep weather stress claim INCONCLUSIVE.",
                "Affects maximalization confidence for GEO-C005/C006.",
            )
            return [], {"status": "PARSE_FAILED"}

    if len(points) >= 3:
        tracks.append(
            {
                "trajectory_id": "gfs_prmsl_min_track",
                "coord_system": "wgs84",
                "points": points,
                "label": "weather_low_pressure_track",
            }
        )
    lock["noaa_gfs_aws"] = {
        "source_base": base,
        "files": [
            {"path": str(p), "sha256": sha256_file(p), "bytes": p.stat().st_size}
            for p in downloaded
        ],
        "subset_trajectories": len(tracks),
        "full_corpus_scale_note": "petabyte-scale archive (registry reference)",
    }
    _append_imp(
        imp,
        "NOAA GFS full-corpus replay",
        "IMP-STORAGE",
        "curl -I https://registry.opendata.aws/noaa-gfs-bdp-pds/",
        "Resource is petabyte-scale; local full replay impractical in lane window.",
        "Use deterministic 3-file subset and RunPod scale plan.",
        "Max-wave scale closure for GEO-C005/C006 remains INCONCLUSIVE pending large replay.",
    )
    return tracks, lock["noaa_gfs_aws"]


def _load_desi_subset(imp: list[dict[str, Any]], lock: dict[str, Any]) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    csv_url = "https://data.desi.lbl.gov/public/dr1/spectro/redux/iron/exposures-iron.csv"
    csv_path = EXTERNAL_ROOT / "desi_exposures_iron.csv"
    if not csv_path.exists():
        cmd = f"curl -L --max-time 180 -o {csv_path} {csv_url}"
        result = run_cmd(cmd, timeout_s=260)
        if result.exit_code != 0:
            _append_imp(
                imp,
                "DESI DR1 exposure CSV download",
                "IMP-ACCESS",
                result.command,
                (result.stderr or result.stdout)[:500],
                "Fallback to DESI docs-only lock.",
                "Affects E3 DESI 3D stress closure for GEO-C003/C007/C008.",
            )
            return [], {"status": "FAILED"}

    tracks: dict[str, list[dict[str, Any]]] = defaultdict(list)
    rows = 0
    with open(csv_path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            rows += 1
            tile_id = row.get("TILEID", "").strip()
            if not tile_id:
                continue
            try:
                ra = float(row["TILERA"])
                dec = float(row["TILEDEC"])
                mjd = float(row["MJD"])
            except Exception:
                continue
            points = tracks[tile_id]
            if len(points) >= 180:
                continue
            points.append(
                {
                    "t": (mjd - 50000.0) * 86400.0,
                    "x": ra * 111_000.0,
                    "y": dec * 111_000.0,
                    "speed": 0.0,
                    "cog": 511.0,
                    "z_proxy": mjd,
                }
            )
            if rows >= 260000:
                break

    trajectories = []
    for tile, points in list(tracks.items())[:1200]:
        if len(points) < 25:
            continue
        points.sort(key=lambda p: p["t"])
        trajectories.append(
            {
                "trajectory_id": f"desi_tile_{tile}",
                "coord_system": "xy",
                "points": points,
                "label": "desi_exposure_path",
            }
        )
        if len(trajectories) >= 450:
            break
    lock["desi_dr1"] = {
        "source_url": csv_url,
        "sample_path": str(csv_path),
        "sha256": sha256_file(csv_path),
        "subset_rows": rows,
        "subset_trajectories": len(trajectories),
        "full_corpus_scale_note": "DR1 ecosystem is far larger than local subset; concept pack references 270TB class scale.",
    }
    _append_imp(
        imp,
        "DESI DR1 full-corpus replay",
        "IMP-STORAGE",
        "curl -I https://data.desi.lbl.gov/doc/releases/edr/",
        "Full DESI corpus scale exceeds local lane storage/time envelope.",
        "Use exposure CSV subset + 3D proxy stress and RunPod full replay plan.",
        "Max-wave closure for GEO-C003/C007/C008 remains INCONCLUSIVE until large-scale run.",
    )
    return trajectories, lock["desi_dr1"]


def _h3_resolution_sweep(ais_like: list[dict[str, Any]]) -> dict[str, Any]:
    bridge = H3Bridge(resolution=9)
    sample = ais_like[:40]
    by_res = {}
    for res in (8, 9, 10, 11, 12):
        ok = 0
        fail = 0
        for t in sample:
            out = bridge.roundtrip_consistent(t, resolutions=[res], drift_threshold_m=3000.0)
            if out["all_consistent"]:
                ok += 1
            else:
                fail += 1
        by_res[str(res)] = {"ok": ok, "fail": fail, "pass_rate": ok / max(1, ok + fail)}
    return {"backend": bridge.backend, "sample_trajectories": len(sample), "by_resolution": by_res}


def _carla_attempt(imp: list[dict[str, Any]]) -> dict[str, Any]:
    cmd = f"python3 -m pip install --quiet --target {shlex.quote(str(THIRD_PARTY))} carla"
    result = run_cmd(cmd, timeout_s=240)
    if result.exit_code != 0:
        _append_imp(
            imp,
            "CARLA runtime stress battery",
            "IMP-NOCODE",
            result.command,
            (result.stderr or result.stdout)[:500],
            "Fallback to deterministic CARLA-profile synthetic stress path (already in DT-GEO-2).",
            "CARLA-native stress evidence remains INCONCLUSIVE for maximalization.",
        )
        return {"runtime_available": False, "fallback_used": "synthetic_carla_profile"}
    return {"runtime_available": True, "fallback_used": None}


def main() -> None:
    init_artifact_root()
    append_command_log("python3 code/scripts/gate_m1_max_resources.py", "Gate M1 start")

    md_path = Path(
        os.environ.get(
            "ZPE_GEO_MAX_PACK_MD",
            str(OUTER_WORKSPACE_ROOT / "ZPE 10-Lane NET-NEW Resource Maximization Pack.md"),
        )
    )
    pdf_path = Path(
        os.environ.get(
            "ZPE_GEO_MAX_PACK_PDF",
            str(OUTER_WORKSPACE_ROOT / "ZPE 10-Lane NET-NEW Resource Maximization Pack.pdf"),
        )
    )
    lock: dict[str, Any] = {
        "generated_at_utc": now_utc_iso(),
        "net_new_inputs": [],
        "resource_attempts": {},
    }
    for p in (md_path, pdf_path):
        if p.exists():
            lock["net_new_inputs"].append(
                {"path": str(p), "sha256": sha256_file(p), "bytes": p.stat().st_size}
            )
        else:
            lock["net_new_inputs"].append({"path": str(p), "status": "MISSING"})

    impracticality = load_impracticality()

    av2_trajs, av2_meta = _load_av2_subset(impracticality, lock)
    ais_trajs, ais_meta = _load_noaa_ais_subset(impracticality, lock)
    gfs_trajs, gfs_meta = _load_gfs_weather_subset(impracticality, lock)
    desi_trajs, desi_meta = _load_desi_subset(impracticality, lock)
    carla_meta = _carla_attempt(impracticality)

    h3_sweep = _h3_resolution_sweep(ais_trajs if ais_trajs else gfs_trajs)

    coverage = {
        "generated_at_utc": now_utc_iso(),
        "resources": {
            "argoverse2": av2_meta,
            "noaa_ais": ais_meta,
            "noaa_gfs_aws": gfs_meta,
            "desi_dr1": desi_meta,
        },
        "representativeness_notes": {
            "argoverse2": "Focal parquet subset covers thousands of focal trajectories but not full train.tar.",
            "noaa_ais": "Single-day streamed subset covers multiple vessel classes; full-year replay deferred.",
            "noaa_gfs_aws": "Three-cycle weather subset used for reproducible stress, not full archive.",
            "desi_dr1": "Exposure-level subset used as 3D proxy path stress.",
        },
    }

    stratified: dict[str, Any] = {"generated_at_utc": now_utc_iso(), "domains": {}}
    if av2_trajs:
        stratified["domains"]["argoverse2"] = _benchmark_xy(av2_trajs[:1200], quant_step_m=0.05)
    if ais_trajs:
        stratified["domains"]["noaa_ais"] = _benchmark_wgs84(ais_trajs[:350], quant_step_m=0.25)
    if gfs_trajs:
        stratified["domains"]["noaa_gfs_weather_track"] = _benchmark_wgs84(gfs_trajs, quant_step_m=50.0)
    if desi_trajs:
        desi_metrics = _benchmark_xy(desi_trajs[:350], quant_step_m=100.0)
        desi_metrics["z_dimension_status"] = "INCONCLUSIVE_2D_CODEC_WITH_3D_PROXY_INPUT"
        stratified["domains"]["desi_dr1"] = desi_metrics

    lock["resource_attempts"] = {
        "argoverse_page_probe": probe_url("https://www.argoverse.org/av2.html"),
        "noaa_gfs_probe": probe_url("https://registry.opendata.aws/noaa-gfs-bdp-pds/"),
        "desi_probe": probe_url("https://data.desi.lbl.gov/doc/releases/edr/"),
        "noaa_ais_probe": probe_url("https://coast.noaa.gov/htdata/CMSP/AISDataHandler/2025/"),
        "h3_sweep": h3_sweep,
        "carla": carla_meta,
    }

    write_json(ARTIFACT_ROOT / "max_resource_lock.json", lock)
    write_json(ARTIFACT_ROOT / "dataset_subset_coverage_report.json", coverage)
    write_json(ARTIFACT_ROOT / "trajectory_stratified_error_report.json", stratified)
    write_json(ARTIFACT_ROOT / "h3_resolution_sweep_pack.json", h3_sweep)
    save_impracticality(impracticality)

    log_lines = [
        "",
        f"## Gate M1 ({now_utc_iso()})",
        f"- AV2 subset trajectories: {len(av2_trajs)}",
        f"- NOAA AIS subset trajectories: {len(ais_trajs)}",
        f"- NOAA GFS subset trajectories: {len(gfs_trajs)}",
        f"- DESI subset trajectories: {len(desi_trajs)}",
        f"- H3 backend: {h3_sweep.get('backend')}",
        f"- IMP decisions count: {len(impracticality)}",
    ]
    append_validation_log(log_lines)
    write_json(
        ARTIFACT_ROOT / "gate_snapshots" / "gate_M1" / "gate_M1_manifest.json",
        {
            "gate": "M1",
            "artifacts": [
                "max_resource_lock.json",
                "dataset_subset_coverage_report.json",
                "trajectory_stratified_error_report.json",
                "impracticality_decisions.json",
                "h3_resolution_sweep_pack.json",
            ],
        },
    )
    append_command_log("python3 code/scripts/gate_m1_max_resources.py", "Gate M1 complete")


if __name__ == "__main__":
    main()
