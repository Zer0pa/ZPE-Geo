# Novelty Card — ZPE-Geo

**Date:** 2026-04-17
**Repo:** ZPE-Geo
**Auditor:** Codex corrective-pass sub-agent
**Compass-8:** YES

---

## Product

**Name:** ZPE-Geo
**Domain:** Geospatial trajectory encoding
**Value proposition:** Deterministic, storage-efficient compression of movement traces (AIS vessel tracks, AV telemetry, fleet routes) with H3 hexagonal spatial indexing preserved during encoding, enabling downstream spatial queries without decoding raw coordinates.

---

## Compass-8: YES

The codec uses an explicit 8-compass bearing quantization scheme.

**Code evidence:**

- `code/zpe_geo/constants.py:7–21` — `DIRECTIONS` tuple defines 8 cardinal + intercardinal labels `("N", "NE", "E", "SE", "S", "SW", "W", "NW")`. `DIR_VECTORS` maps each of the 8 compass indices to a unit vector in East/North axis order (0=N through 7=NW).

- `code/zpe_geo/codec.py:61–69` — `_direction_from_dxdy` and `_direction_from_cog` both bin a bearing into one of 8 sectors using `int(((bearing + 22.5) // 45.0) % 8)`. The `+ 22.5` offset centres each 45° sector on its compass label; `% 8` wraps NW back to 0-indexed range.

---

## Novel contributions (this repo)

1. **Compass-8 direction tokenisation for trajectory segments.** Each displacement vector is quantized to one of 8 compass bins before encoding. This is the primary vocabulary reduction step that enables RLE gains.

2. **Magnitude quantisation per segment.** Segment lengths are binned at a configurable `quant_step` (default 0.05 m). Together with direction quantisation, this produces a compact (direction, magnitude) token stream.

3. **Speed quantisation.** Instantaneous speed is also quantized before storage, giving a 3-field token `(direction, magnitude, speed)` per segment.

4. **Run-length encoding on the token stream.** Consecutive identical tokens are collapsed to `(token, count)` pairs. The combination of direction + magnitude + speed quantisation with RLE on geospatial traces is the specific codec design of this repo.

5. **H3 hexagonal spatial index built during encoding.** H3 cell membership is computed and attached at encode time, enabling spatial-range queries against the compressed representation without decompression to raw coordinates.

---

## Standard techniques (not claimed as novel)

- H3 hierarchical hexagonal indexing (Uber H3 library).
- Run-length encoding (RLE) — general lossless compression primitive.
- Bearing-to-compass-sector binning (standard navigational convention).
- Dynamic time warping (DTW) — used in evaluation, not encoding.
- Douglas-Peucker simplification (used as competitive baseline only).
- Maneuver classification via nearest-neighbour search in codec space.

---

## Scope boundary

Novelty claims are scoped to this repo's codec implementation only. They do not extend to the broader ZPE portfolio architecture, ZPE-IMC integration layer, or any sibling codec repo.
