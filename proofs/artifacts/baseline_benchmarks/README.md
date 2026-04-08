# Real-World Baseline Benchmarks

| Dataset | Trajectories | Points | Raw JSON Bytes | ZPE Bytes | ZPE Ratio | Max Error |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| NOAA AIS extract | 5 | 60 | 8545 | 406 | 21.05x | 0.014429029350 |
| GeoLife extract | 5 | 160 | 17935 | 657 | 27.30x | 0.000549743650 |
| OSM Monaco extract | 5 | 100 | 6107 | 480 | 12.72x | 0.000311479106 |

| Dataset | Baseline | Baseline Bytes | ZPE Bytes | Improvement vs Baseline |
| --- | --- | ---: | ---: | ---: |
| NOAA AIS extract | gzip | 2009 | 406 | 4.95x |
| NOAA AIS extract | douglas_peucker | 520 | 406 | 1.28x |
| GeoLife extract | gzip | 2820 | 657 | 4.29x |
| GeoLife extract | douglas_peucker | 440 | 657 | 0.67x |
| OSM Monaco extract | gzip | 1728 | 480 | 3.60x |
| OSM Monaco extract | douglas_peucker | 424 | 480 | 0.88x |
