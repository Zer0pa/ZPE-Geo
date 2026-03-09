"""Domain constants for zpe-geo."""

from __future__ import annotations

from .paths import ARTIFACT_BUNDLE_NAME

DIRECTIONS = ("N", "NE", "E", "SE", "S", "SW", "W", "NW")
DIR_TO_INDEX = {name: idx for idx, name in enumerate(DIRECTIONS)}
INDEX_TO_DIR = {idx: name for idx, name in enumerate(DIRECTIONS)}

# Unit vectors in East/North axis order.
DIR_VECTORS = {
    0: (0.0, 1.0),  # N
    1: (0.70710678, 0.70710678),  # NE
    2: (1.0, 0.0),  # E
    3: (0.70710678, -0.70710678),  # SE
    4: (0.0, -1.0),  # S
    5: (-0.70710678, -0.70710678),  # SW
    6: (-1.0, 0.0),  # W
    7: (-0.70710678, 0.70710678),  # NW
}

MAGIC = b"ZPGEO1"
VERSION = 1
DEFAULT_QUANT_STEP_M = 0.05
DEFAULT_SAMPLE_DT_MS = 100
DEFAULT_ARTIFACT_ROOT = f"proofs/artifacts/{ARTIFACT_BUNDLE_NAME}"

CLAIMS = {
    "GEO-C001": "AV CR >= 20x",
    "GEO-C002": "AIS CR >= 25x",
    "GEO-C003": "AV RMSE <= 1 m",
    "GEO-C004": "AIS DTW <= 50 m",
    "GEO-C005": "Maneuver P@10 >= 0.90",
    "GEO-C006": "Search latency < 1 s",
    "GEO-C007": "AIS online encode < 10 ms",
    "GEO-C008": "H3 roundtrip consistent",
}
