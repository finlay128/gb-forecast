# Log

## 2026-07-13 — Data Status endpoints don't cover demand or wind
All 12 `/data-status/{X}` endpoints are balancing-mechanism datasets
(BOALF, BOAV, BOD, DISBSAD, DISEBSP, DISPTAV, EBOCF, FREQ, ISPSTACK,
NETBSAD, PN, REMIT). None for INDO/ITSDO/WINDFOR.

→ Publication lag and revision behaviour must be established empirically:
re-pull the same settlement date at intervals and diff. Don't go looking
for a metadata endpoint that tells you; there isn't one.

## 2026-07-13 — /datasets/ITSDO filters on publish time, not settlement date
Params are `publishDateTimeFrom/To` only; nothing is required. Contrast
with `/demand/outturn` (INDO), which filters on settlement date.

→ Two implications: (a) backfilling ITSDO by settlement date needs a
generous publish window plus client-side filtering; (b) (settlementDate,
settlementPeriod) may not be a unique key — the dataset may be an
append-only publication log. UNVERIFIED — test before designing the
schema.

## 2026-07-13 — INDO and ITSDO have no /stream variants
Most of the `/datasets/ family` have a stream twin with a lighter JSON
payload. INDO and ITSDO don't.

→ Backfilling the primary demand series will use the standard endpoints:
heavier payloads, and likely a max query window (check the
x-max-day-range-* extensions in swagger.json for both). Chunk the backfill
and rate-limit it — there's a documented 429.