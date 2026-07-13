import httpx, pandas as pd

BASE = "https://data.elexon.co.uk/bmrs/api/v1"
FROM, TO = "2026-06-01T00:00Z", "2026-06-08T00:00Z"

def fetch(dataset: str, **params) -> pd.DataFrame:
    r = httpx.get(f"{BASE}/datasets/{dataset}",
                  params={"format": "json", **params}, timeout=30.0)
    r.raise_for_status()
    return pd.json_normalize(r.json()["data"])

itsdo = fetch("ITSDO", publishDateTimeFrom=FROM, publishDateTimeTo=TO)
indo  = fetch("INDO",  publishDateTimeFrom=FROM, publishDateTimeTo=TO)

print(indo.dtypes, "\n", indo.head().to_string(), "\n")
print("INDO dupe keys:", indo.duplicated(["settlementDate", "settlementPeriod"]).sum())

key = ["settlementDate", "settlementPeriod"]
both = itsdo.merge(indo, on=key, suffixes=("_itsdo", "_indo"))
both["gap"] = both["demand_itsdo"] - both["demand_indo"]
both["utc"] = pd.to_datetime(both["startTime_itsdo"])

print(both["gap"].describe())
print(both.groupby(both["utc"].dt.hour)["gap"].mean().round(0).to_string())