# ZPE-Geo Novelty Card

**Product:** ZPE-Geo
**Domain:** Deterministic encoding, compression, and retrieval of geospatial movement traces.
**What we sell:** Smaller trajectory archives with spatial lookup and maneuver-aware analytics for mobility and fleet data.

## Novel contributions

1. **Directional trajectory packet contract** -- ZPE-Geo normalizes XY or WGS84 traces into a deterministic step stream, quantizes each step into an 8-way direction bin plus magnitude and speed bins, and then packs stable runs into the `.zpgeo` payload format. Code: [`code/zpe_geo/codec.py:72-111`](../../../code/zpe_geo/codec.py), [`code/zpe_geo/codec.py:124-211`](../../../code/zpe_geo/codec.py). Nearest prior art (if known): generic delta/RLE trajectory codecs and polyline simplifiers such as Douglas-Peucker. What is genuinely new here: the repo's specific movement-token contract and packed run semantics for replayable trajectory storage, not the underlying quantization or packing primitives by themselves.
2. **Encoded-trace H3 bridge with deterministic verification surface** -- The repo derives deduplicated H3 cell paths from WGS84 trajectories and checks point-to-cell-to-centroid roundtrips against a deterministic drift threshold, while preserving explicit backend/fallback behavior. Code: [`code/zpe_geo/h3bridge.py:25-61`](../../../code/zpe_geo/h3bridge.py), [`code/zpe_geo/h3bridge.py:63-102`](../../../code/zpe_geo/h3bridge.py). Nearest prior art (if known): standard H3 indexing libraries and cell-coverage utilities. What is genuinely new here: the lane-local coupling between the trace representation, cell-path derivation, and reproducible roundtrip verification surface.
3. **Maneuver primitives over the same directional alphabet** -- Maneuver scoring reuses the trajectory direction-token stream to classify turning, merge, stop, and straight motion without introducing a second feature language. Code: [`code/zpe_geo/maneuver.py:17-36`](../../../code/zpe_geo/maneuver.py), [`code/zpe_geo/maneuver.py:78-99`](../../../code/zpe_geo/maneuver.py). Nearest prior art (if known): rule-based maneuver heuristics over trajectory points. What is genuinely new here: that the maneuver layer is expressed directly over the same eight-direction token surface used by the codec, which keeps compression and behavior scoring on one deterministic representation.

## Standard techniques used (explicit, not novel)

- Local tangent-plane projection from WGS84 coordinates.
- Scalar magnitude quantization and speed binning.
- Varint encoding and byte packing.
- Run-length-style grouping of stable step runs.
- H3 spatial indexing.
- Haversine distance checks and heuristic rule scoring.

## Compass-8 / 8-primitive architecture

YES -- ZPE-Geo uses an 8-direction movement alphabet in the live codec and maneuver layers. See [`code/zpe_geo/codec.py:61-69`](../../../code/zpe_geo/codec.py), [`code/zpe_geo/codec.py:137-200`](../../../code/zpe_geo/codec.py), and [`code/zpe_geo/maneuver.py:10-36`](../../../code/zpe_geo/maneuver.py).

## Open novelty questions for the license agent

- The strongest novelty claim appears to be the combined `.zpgeo` directional packet contract; please decide whether the H3 bridge and maneuver primitives should be scheduled as independent novelty items or only as dependent surfaces of that core representation.
