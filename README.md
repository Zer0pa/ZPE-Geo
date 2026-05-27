# ZPE-Geo

> Product-page mirror for `/encoding/ZPE-Geo/`.
> Live public repo: [Zer0pa/ZPE-Geo](https://github.com/Zer0pa/ZPE-Geo).
> GitHub Markdown cannot reproduce the website typography, CSS, JavaScript, scroll behavior, or live bento layout; this README translates the product page into GitHub-safe Markdown evidence blocks.

## 0. Install / Developer Commands

The product page is the positioning authority. This section is the only retained developer-surface material from the previous root README.

```bash
Deterministic trajectory codec. Compact zpgeo packets, documented spatial error bounds, and sub-millisecond maneuver search. Install from PyPI: `pip install zpe-geo
git clone https://github.com/Zer0pa/ZPE-Geo.git zpe-geo
python -m pip install -e ".[dev,h3]"
python -m pytest code/tests -q
```

## Product Page Mirror

**Product-page title:** ZPE-Geo · Trajectory archive/search codec · Zer0pa

**Product-page description:** ZPE-Geo · deterministic trajectory archive/search codec · 13.78× on 34,668-way OSM extract · 27.3× GeoLife real GPS · 21.0× real AIS · simulated p95 query 0.064 ms · PyPI v0.1.1 stale pending release

### Hero Translation

> 00 · ZPE-GEO · TRAJECTORY ARCHIVEDEVELOPER-READY · B3 OPEN Journeys Seen as Paths, Not Points. A trajectory archive for the shape of the route · ZPE-Geo · PyPI zpe-geo v0.1.1 · github.com/Zer0pa/ZPE-Geo GPS records where you were. It cannot show what the journey looked like. ZPE-Geo keeps the path itself — the curve of the road, the arc of the vessel, the sweep of the turn — as a compact archive packet. Movement compresses 13.78× on a 34,668-way OpenStreetMap extract; a maneuver query returns P@10 = 1.0 on 210 trajectories. Scope is bounded: archive and search only, not navigation, not lossless geometry.

## Positioning

| Field | Value |
| --- | --- |
| Section | encoding |
| Product route | /encoding/ZPE-Geo/ |
| Live public repository | https://github.com/Zer0pa/ZPE-Geo |
| Repo identity used here | ZPE-Geo |
| Website display identity | ZPE-Geo |
| Verdict | BLOCKED |
| Posture | always_in_beta |
| Headline metric | On a 34,668-way Rhode Island OSM extract, ZPE-Geo compresses JSON→zpgeo at 13.8× vs Douglas-Peucker 6.5× at ε=0.5 m. Real-world AIS, GeoLife GPS, and OSM extracts land in the 12.7×–27.3× band on the same DP calibration. |
| Honest blocker | No claim of blind-clone closure (GEO-C001); No claim of full-corpus closure (GEO-C002); No claim of release readiness (GEO-C004) |
| Mechanics asset from product page | GEO.gif |

## Key Metrics

| Metric | Value | Baseline |
| --- | --- | --- |
| COMPRESSION_AIS_SYNTHETIC | 450.8× mean | Douglas-Peucker 314.8× |
| COMPRESSION_AV_SYNTHETIC | 123.1× mean | — |
| MANEUVER_PRECISION | P@10 = 1.0 (all query types) | 210-traj fixture + 1,610-traj scale eval |
| QUERY_LATENCY_P95 | 0.040 ms mean / 0.064 ms p95 | Simulated 10 M trajectory corpus |

## Proof Anchors

| Path | State |
| --- | --- |
| proofs/artifacts/2026-03-21_operator_status/README.md | VERIFIED |
| proofs/artifacts/2026-03-21_operator_status/phase0311_runpod/max_claim_resource_map.json | VERIFIED |
| proofs/artifacts/2026-03-21_operator_status/release_alignment/TECHNICAL_ALIGNMENT_REPORT.md | VERIFIED |
| proofs/artifacts/2026-02-20_zpe_geo_wave1/geo_ais_benchmark.json | VERIFIED |
| proofs/artifacts/2026-02-20_zpe_geo_wave1/geo_av_benchmark.json | VERIFIED |
| proofs/artifacts/2026-02-20_zpe_geo_wave1/geo_ais_fidelity.json | VERIFIED |

## What We Prove

- encode_trajectory and decode_trajectory round-trip shipped XY and WGS84 fixtures without dropping point counts — exercised by code/tests/test_codec.py, code/tests/test_roundtrip.py, code/tests/test_edge_cases.py → proofs/artifacts/fixture_benchmarks/
- ManeuverSearchIndex builds and answers deterministic label, bounding-box, and radius queries on repo-local fixtures with P@10 = 1.0 across all query types — exercised by code/tests/test_search.py, code/tests/test_search_comprehensive.py → geo_maneuver_search_eval.json
- H3Bridge round-trip and cell-path behavior stays stable across tested resolutions and edge coordinates — exercised by code/tests/test_h3bridge.py, code/tests/test_h3bridge_resolution.py → geo_h3_roundtrip_results.json
- The repo-root package installs as an editable package and builds as a distribution — GitHub Actions CI + local python -m build → TECHNICAL_ALIGNMENT_REPORT.md
- Compression ratio 13.8× mean on 34,668-way real-world OSM extract vs Douglas-Peucker 6.5× at ε=0.5 m — aggregate corpus, not single-sequence → osm_parity_full_corpus_report.json
- Query latency mean 0.040 ms, p95 0.064 ms on simulated 10 M trajectory corpus (deterministic index replication over 210-trajectory fixture) → geo_query_latency_benchmark.json
- Online encode latency mean 0.107 ms, p95 0.122 ms (threshold: 10 ms) across 39,907 streamed updates → geo_stream_latency.json
- Real-world AIS (21.0×), GeoLife GPS (27.3×), OSM Monaco (12.7×) compression ratios on 5-trajectory public-domain extracts → real_world_benchmarks/

## What We Do Not Claim

- Lossless coordinate equality is not claimed. Round-trip error is bounded, not zero: max 1.28 × 10⁻⁶° on AIS WGS84, max 0.025 m on AV XY fixtures at the shipped quantization step.
- ACM 2025 dataset parity is INCONCLUSIVE — supplementary dataset alignment was not completed. The ACM 2025 comparison row is not an independently verified benchmark against the paper's dataset.
- Full-corpus aggregate fidelity on the 34,668-way Rhode Island OSM extract: DTW p95 32.4 m vs DP 16.8 m — this is a FAIL relative to Douglas-Peucker on static road-graph fidelity. Acceptable for archival use; not claimed suitable for road-graph navigation.
- The 10 M trajectory query latency result uses deterministic index replication over the 210-trajectory fixture; it is not a full-corpus live run.
- No real-time streaming reconstruction guarantee beyond the 10 ms p95 threshold documented in the stream latency artifact.
- No claim of superiority over all compression algorithms. Comparison is scoped to Douglas-Peucker with documented calibration parameters.
- This codec does not implement lossless geometry storage. It is not a substitute for formats requiring exact coordinate preservation (e.g., legal survey, precision navigation).

## Blockers / Failures

> No claim of blind-clone closure (GEO-C001); No claim of full-corpus closure (GEO-C002); No claim of release readiness (GEO-C004)

## Verification Surface

| Code | Check | Verdict |
| --- | --- | --- |
| V_01 | code/tests/test_codec.py — encode_trajectory / decode_trajectory round-trip; no point-count drop on XY and WGS84 fixtures | PASS |
| V_02 | code/tests/test_roundtrip.py — Byte-exact determinism; coordinate error within documented bounds | PASS |
| V_03 | code/tests/test_edge_cases.py — Edge coordinate inputs, empty trajectories, single-point degenerate cases | PASS |
| V_04 | code/tests/test_search.py — ManeuverSearchIndex label, bounding-box, radius queries on 210-traj fixture | PASS |
| V_05 | code/tests/test_search_comprehensive.py — P@10 = 1.0 across all query types; 1,610-traj scale eval | PASS |
| V_06 | code/tests/test_h3bridge.py — H3Bridge round-trip stability across tested resolutions | PASS |
| V_07 | code/tests/test_h3bridge_resolution.py — Cell-path behavior at edge coordinates; resolution sweep | PASS |
| V_08 | GitHub Actions CI — Package installs as editable; python -m build produces distribution | PASS |

## License

| Field | Value |
| --- | --- |
| License | SAL-7.0 |
| Authority source | March 21 operator status pack |

## Upcoming Workstreams

| Category | Summary |
| --- | --- |
| Research-Deferred — Investigation Underway | ACM 2025 dataset alignment resolution. INCONCLUSIVE alignment must be diagnosed; either the comparison is fixed or the dataset is formally excluded with rationale. |
| Research-Deferred — Investigation Underway | Adaptive primitive for road-graph fidelity. Foundations exist via H3 indexing; primitive-level investigation needed to close the regression vs Douglas-Peucker on static road graphs. |

## Related Repos

No related repos are declared on the product page frontmatter.

<details>
<summary>Full Visible Product-Page Bento Translation</summary>

This section preserves the product page cells as Markdown text blocks. It intentionally omits shared site navigation, footer chrome, CSS, and scripts.

### Bento Cell 1

> 00 · ZPE-GEO · TRAJECTORY ARCHIVEDEVELOPER-READY · B3 OPEN Journeys Seen as Paths, Not Points. A trajectory archive for the shape of the route · ZPE-Geo · PyPI zpe-geo v0.1.1 · github.com/Zer0pa/ZPE-Geo GPS records where you were. It cannot show what the journey looked like. ZPE-Geo keeps the path itself — the curve of the road, the arc of the vessel, the sweep of the turn — as a compact archive packet. Movement compresses 13.78× on a 34,668-way OpenStreetMap extract; a maneuver query returns P@10 = 1.0 on 210 trajectories. Scope is bounded: archive and search only, not navigation, not lossless geometry.

### Bento Cell 2

> 01 · THE GAPARCHIVE/SEARCH GAP GPS captures where you were. It cannot tell you what the journey looked like.

### Bento Cell 3

> 02 · MARKETSADJACENT FORECASTS Maritime analytics ’31$2.6 B Maritime analytics ’35$7.6 B Maritime information ’30$23.2 B Fleet telematics ’30$36.2 B Autonomous vehicle data ’30$11.5 B Mordor Intelligence, MRFR, ResearchAndMarkets · external trajectory-adjacent forecasts, not a ZPE-Geo revenue claim.

### Bento Cell 4

> 03 · VALUE $36.2B Fleet telematics by 2030; ZPE-Geo addresses the archive-and-search slice, not navigation or fleet intelligence.

### Bento Cell 5

> 04 · INSIGHT A route is not its waypoints — it is its arc.

### Bento Cell 6

> 05.1 · CURRENT TECHCOORDINATES, NOT PATHS GPS logs, GeoJSON files, parquet tables: a journey today becomes a list of timestamped coordinates. The shape between them — its curve, its arc — is inferred later, or lost.

### Bento Cell 7

> 05.2 · OUR TECHKEEP THE PATH ZPE-Geo encodes movement as delta packets that hold the shape of the journey, not just its points. Compression reaches 13.78× on a 34,668-way OpenStreetMap extract, 27.3× on real GeoLife GPS, 21.0× on real NOAA AIS. A maneuver index finds routes by the movement inside them.

### Bento Cell 8

> 05.3 · BENCHMARKSDECLARED FIXTURES OSM13.78×34,668 ways GeoLife GPS27.3×real extract NOAA AIS21.0×real extract P@101.0maneuver search ZPE OSM13.78× DP OSM6.45× max-wave0/2 MISS Status: two larger corpora (Argoverse2, NOAA) not yet passing · full-set extension pending.

### Bento Cell 9

> 06 · MEASUREMENTOSM · REAL EXTRACTS · BLOCKERS Every metric stays tied to declared OSM, AIS, and GPS surfaces.

### Bento Cell 10

> 06.1 · COMPARATIVE PERFORMANCEOSM EXTRACT VS BASELINE ZPE-Geo OSM13.78× smaller DP baseline6.45× Argoverse2 max-waveMISS NOAA max-waveMISS OpenStreetMap full extract (34,668 ways) · Douglas-Peucker ε=0.5 m baseline for comparison · Argoverse2 and NOAA larger corpora not yet passing · parity with the ACM-2025 reference still open. GeoLife real GPS 27.3× · real NOAA AIS 21.0×.

### Bento Cell 11

> 07 · KEY METRICSOSM EXTRACT · REAL GPS/AIS

### Bento Cell 12

> 07.1 · OSM EXTRACT 13.78× vs DP 6.45× · 34,668-way OSM extract

### Bento Cell 13

> 07.2 · GEOLIFE REAL 27.3× Real GPS extract · 5 trajectories

### Bento Cell 14

> 07.3 · QUERY P95 0.064ms Spatial-range query · mean 0.040 ms

### Bento Cell 15

> 07.4 · WAYS EVALUATED 34,668 OSM full extract · real OpenStreetMap ways

### Bento Cell 16

> 07.5 · RELEASE v0.1.1 PyPI live but stale · 0.1.2 pending

### Bento Cell 17

> 08 · DETERMINISMDECLARED-FIXTURE REPLAY Same trajectory bytes,same query results on fixtures.

### Bento Cell 18

> 08.1 · WHAT DETERMINISTIC MEANSREPEATABLE ON DECLARED SURFACES On declared repo fixtures, the delta-stream codec produces repeatable compressed bytes under local replay; maneuver queries return stable match sets. Full-corpus extracts — Argoverse2 and NOAA — missed the max-wave check and remain open. AV fidelity reports p95 1.86 m and max 2.17 m against a 1.0 m threshold; that surface is unresolved. ACM-2025 parity stays inconclusive. The archive-and-search claim is bounded: declared OSM and trajectory fixtures only.

### Bento Cell 19

> 08.2 · THE FIDELITY GAP Honest Blocker · Bound to OSM ways and declared fixtures. AV fidelity p95/max exceed the 1.0 m threshold; OSM DTW p95 trails Douglas-Peucker. Argoverse2 / NOAA max-wave and full-corpus closure remain open. PyPI v0.1.1 is stale; 0.1.2 pending. No lossless-geometry, navigation-system, or road-graph claim.

### Bento Cell 20

> 09 EVERY JOURNEY BECOMES A QUERYABLE PATH.

### Bento Cell 21

> 09.1 · THE AMBITION The aim is not a better mapping system. It is the archive beneath one. When a trajectory keeps its shape, a route can be stored compact and retrieved by the path it traces — searched by behavior, not by timestamp. Reaching it depends on closing max-wave, full-corpus, and blind-clone gaps.

### Bento Cell 22

> 09.2 · WHAT WORKS NOW Working today: 13.78× archive compression and P@10 = 1.0 maneuver search on declared OpenStreetMap fixtures.

### Bento Cell 23

> 09.3 · WHAT'S STILL OPEN Still open: max-wave on Argoverse2 and NOAA, full-corpus closure, blind-clone replay, a current PyPI release.

### Bento Cell 24

> 09.4 · AIS ARCHIVES · NEAR-TERM (12–24 MO) Vessel histories searched by route shape A maritime analyst holding decades of AIS feeds can keep them compact and ask the archive “show every approach into this harbor that arced like this one.” Search by behavior, not by ship name or date.

### Bento Cell 25

> 09.5 · FLEET AUDIT · NEAR-TERM (12–24 MO) A compliance question becomes a search For a fleet operator answering a regulator, the incident becomes a query against the route library, not a reconstruction from raw logs. The answer returns before the auditor finishes the question, because retrieval beats reassembly.

### Bento Cell 26

> 09.6 · TRAJECTORY IDENTITY · MID-TERM (24–48 MO) A route gets a durable name When the same journey produces the same compact packet on two captures, a route stops being a list of points and becomes a citable thing. A mapping engineer can refer to a specific maneuver the way archivists refer to a specific document — by name, not by reconstruction.

### Bento Cell 27

> 09.7 · AV ROUTE LIBRARIES · MID-TERM (24–48 MO) Self-driving fleets keep every test mile A mean 123.1× on synthetic AV XY means autonomous-vehicle teams stop choosing which test routes to delete. The full library — every edge case, every odd intersection, every demonstration drive — stays affordable to retain and ready to retrieve.

### Bento Cell 28

> 09.8 · MOVEMENT CUSTODY · PARADIGM (48 MO+) Movement history acquires provenance If the open checks close, a specific route at a specific time can be pointed to, retrieved, and compared against an external record. That is the substrate beneath maritime liability, autonomous-vehicle accountability, and continental-scale fleet governance.

</details>

---

Source mapping: product route `/encoding/ZPE-Geo/` -> live public repo `Zer0pa/ZPE-Geo`. README generated from product-page authority plus retained install/dev commands only.
