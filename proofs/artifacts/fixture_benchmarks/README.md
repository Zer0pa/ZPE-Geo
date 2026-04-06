# Fixture Benchmarks

| Fixture | Compression Ratio | Encode Mean (us) | Decode Mean (us) | Exact Coordinate Matches | Max Abs Error |
| --- | ---: | ---: | ---: | ---: | ---: |
| ais_noaa_fixture_v1.json | 1096.67 | 1708.0 | 664.5 | 0/190 | 0.000001279826 |
| av_argoverse2_fixture_v1.json | 264.34 | 590.5 | 164.0 | 0/210 | 0.024982542405 |

Exact coordinate equality is reported as observed.
The current codec does not produce exact coordinate equality on the shipped fixtures, so this artifact preserves that result instead of suppressing it.
