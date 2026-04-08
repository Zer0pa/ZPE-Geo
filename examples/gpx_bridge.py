#!/usr/bin/env python3
"""Roundtrip a small GPX track through zpe-geo encoding and back to GPX."""

from __future__ import annotations

import argparse
import json
import tempfile
import xml.etree.ElementTree as ET
from datetime import datetime, timezone
from pathlib import Path

from zpe_geo.codec import decode_trajectory, encode_trajectory


REPO_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_INPUT = REPO_ROOT / "examples" / "data" / "sample_route.gpx"
GPX_NS = "http://www.topografix.com/GPX/1/1"


def _parse_time(value: str) -> float:
    return datetime.fromisoformat(value.replace("Z", "+00:00")).timestamp()


def _format_time(value: float) -> str:
    return datetime.fromtimestamp(value, tz=timezone.utc).isoformat().replace("+00:00", "Z")


def _load_gpx(path: Path) -> dict:
    root = ET.parse(path).getroot()
    points = []
    for idx, trkpt in enumerate(root.findall(".//{*}trkpt")):
        lat = float(trkpt.attrib["lat"])
        lon = float(trkpt.attrib["lon"])
        time_node = trkpt.find("{*}time")
        t_value = float(idx)
        if time_node is not None and time_node.text:
            t_value = _parse_time(time_node.text)
        points.append(
            {
                "t": t_value,
                "lat": lat,
                "lon": lon,
                "speed": 0.0,
                "cog": 0.0,
            }
        )
    if len(points) < 2:
        raise ValueError(f"GPX input requires at least two track points: {path}")
    return {
        "trajectory_id": path.stem,
        "coord_system": "wgs84",
        "points": points,
    }


def _write_gpx(decoded: dict, output_path: Path) -> None:
    ET.register_namespace("", GPX_NS)
    root = ET.Element(f"{{{GPX_NS}}}gpx", attrib={"version": "1.1", "creator": "zpe-geo examples/gpx_bridge.py"})
    trk = ET.SubElement(root, f"{{{GPX_NS}}}trk")
    name = ET.SubElement(trk, f"{{{GPX_NS}}}name")
    name.text = decoded.get("trajectory_id", "zpe-geo-roundtrip")
    seg = ET.SubElement(trk, f"{{{GPX_NS}}}trkseg")
    for point in decoded["points"]:
        trkpt = ET.SubElement(
            seg,
            f"{{{GPX_NS}}}trkpt",
            attrib={"lat": f"{float(point['lat']):.8f}", "lon": f"{float(point['lon']):.8f}"},
        )
        time_node = ET.SubElement(trkpt, f"{{{GPX_NS}}}time")
        time_node.text = _format_time(float(point["t"]))
    output_path.parent.mkdir(parents=True, exist_ok=True)
    ET.ElementTree(root).write(output_path, encoding="utf-8", xml_declaration=True)


def _default_output_path() -> Path:
    temp_root = Path(tempfile.gettempdir()) / "zpe_geo_examples"
    return temp_root / "sample_route.roundtrip.gpx"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", default=str(DEFAULT_INPUT), help="Input GPX file.")
    parser.add_argument("--output", default=str(_default_output_path()), help="Output GPX file.")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    input_path = Path(args.input).resolve()
    output_path = Path(args.output).resolve()

    trajectory = _load_gpx(input_path)
    decoded = decode_trajectory(encode_trajectory(trajectory, quant_step_m=0.25).payload)
    decoded["trajectory_id"] = f"{trajectory['trajectory_id']}_roundtrip"
    _write_gpx(decoded, output_path)

    summary = {
        "input_path": str(input_path),
        "input_points": len(trajectory["points"]),
        "output_path": str(output_path),
        "output_points": len(decoded["points"]),
    }
    print(json.dumps(summary, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
