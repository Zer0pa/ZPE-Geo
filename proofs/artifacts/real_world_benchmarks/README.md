# Real-World Dataset Acquisition

| Dataset | Status | Detail | Fixture | Benchmark |
| --- | --- | --- | --- | --- |
| NOAA AIS | completed | Extracted five real vessel trajectories from the official 2025-01-01 daily CSV. | code/fixtures/real_world/noaa_ais_day_extract.json | proofs/artifacts/real_world_benchmarks/noaa_ais_day_extract_benchmark.json |
| GeoLife GPS Trajectories | completed | Extracted five track files from the official GeoLife 1.3 ZIP. | code/fixtures/real_world/geolife_extract.json | proofs/artifacts/real_world_benchmarks/geolife_extract_benchmark.json |
| NYC Taxi Trip Records | blocked | Official 2026 parquet lacks direct pickup/dropoff lat/lon columns; only zone-style fields are available. | - | - |
| OpenStreetMap Node Dumps | completed | Extracted five Monaco highway ways from the official Geofabrik PBF using osmium. | code/fixtures/real_world/osm_monaco_way_extract.json | proofs/artifacts/real_world_benchmarks/osm_monaco_way_extract_benchmark.json |
| Argoverse 2 Motion Forecasting | blocked | Official source requires registration, so no unattended download was possible. | - | - |
| Porto Taxi Trajectories | blocked | Official Kaggle distribution requires account-authenticated access. | - | - |
