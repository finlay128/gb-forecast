# Decisions

## D-001 — Forecast target is INDO (National Demand), not ITSDO
**Date:** 2026-07-13

**Decision.** The demand target is INDO — Initial National Demand outturn, half-hourly, `/datasets/INDO`.

**Evidence.** Transmission System Demand = National Demand + station transformer load + pumped-storage pumping + interconnector exports. Measured over 2026-06-01..08, ITSDO − INDO: mean 2208 MW, sd 1008, range 514–5129. Strongly diurnal: ~3.0 GW at 03–04 UTC, ~1.5 GW at 15–16 UTC. The overnight maximum is the pumped-storage signature; the wide range is interconnector flows. Both confirmed directly in FUELINST, which shows several GW of interconnector flow varying period to period.

**Alternative rejected.** ITSDO. It bundles ~2 GW of *price-driven trading behaviour* — pumping schedules, export flows — into the target. These are not predictable from weather and calendar. Including them would guarantee a large, structured, permanently unexplainable residual.

**Consequence.** Benchmark against **NDF**, not TSDF, from `/forecast/demand/day-ahead/earliest`.

Revisit if I later add a price/trading layer to the project, at which point the ITSDO − INDO spread becomes an interesting target in its own right rather than noise.

---

## D-002 — Forecast INDO as published; do not reconstruct underlying demand
**Date:** 2026-07-13

**Decision.** Model the published INDO series directly, embedded-solar artefact and all. Do not add estimated embedded generation back to construct a "true consumption" target.

**Evidence.** INDO is transmission-level and therefore net of embedded generation. The artefact is plainly visible: in June, weekday demand ramps to ~26 GW by 09:00, sags to 21–25 GW across 10:00–15:00, then peaks at 27–29 GW at 18:00–19:00. January shows a flat 37–40 GW daytime plateau with no midday trough. Britain does not use less electricity at lunchtime in June; rooftop PV is serving that load behind the meter. (`figures/2026-07-13_indo_daily_shape.png`)

The magnitude fits: AGWS midday solar over the same week ranges 5.7–8.7 GW against a ~4–5 GW sag. The lowest-solar day is also the flattest.

**Alternative rejected.** Reconstruct demand as INDO + embedded solar. There is no series that supports this:
- **AGWS** (`/generation/actual/per-type/wind-and-solar`) is a NESO *model estimate*, not metered output, and is missing ~21 of 48 settlement periods on a typical day — including SP25, the middle of the solar peak. Absence is not zero: the dataset publishes explicit 0.0 rows overnight, so a missing row is missing data. It cannot be filled without fabricating observations.
- **FUELINST** has no SOLAR category at all. Embedded generation is invisible to a metered transmission feed by construction.

Reconstructing would mean defining my target variable as a function of someone else's model output, interpolated across holes. Every error in NESO's PV estimate would become an error in my ground truth, and I could never separate "my model is wrong" from "my target is wrong".

**Consequence.** The model must be given **irradiance / clear-sky features** at the population-weighted points, interacted with time of day, so it can *learn* the embedded-solar hole rather than having it surgically removed with a leaky instrument. This is a modelling requirement, not an optional feature.

Revisit if a complete, metered embedded-generation series becomes available, or if residual analysis shows the model systematically fails to capture the summer midday shape despite irradiance features — which would suggest the artefact needs handling structurally rather than as a covariate.

---

## D-003 — Wind target definition