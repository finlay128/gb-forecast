# Data Sources

## Shortlist Table
| Purpose                               | Endpoint                                       | Code
| ---                                   | ---                                            | ---
| Demand target (national)              | `/demand/outturn/stream`                       | INDO
| Demand target (transmission)          | `/datasets/ITSDO`                              | ITSDO
| Cross-check \ alternative definition  | `/demand/actual/total`                         | ATL/B0610
| Wind actual                           | `/generation/actual/per-type/wind-and-solar`   | AGWS/B1630
| Wind actual (cross-check)             | `/generation/outturn/summary`                  | FUELINST
| Demand benchmark                      | `/forecast/demand/day-ahead/earliest/stream`   | NDF, TSDF
| Wind benchmark                        | `/forecast/generation/wind/earliest/stream`    | WINDFOR
| Wind farm identification              | `/reference/bmunits/all`                       | -
| Official weighted temperature         | `/temperature`                                 | TEMP