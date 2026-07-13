import httpx, pandas as pd

r = httpx.get(
    "https://data.elexon.co.uk/bmrs/api/v1/datasets/ITSDO",
    params={
        "publishDateTimeFrom": "2026-06-01T00:00Z",
        "publishDateTimeTo":   "2026-06-08T00:00Z",
        "format": "json",
    },
    timeout=30.0,
)
r.raise_for_status()
payload = r.json()

print(type(payload), list(payload)[:5] if isinstance(payload, dict) else len(payload))

df = pd.json_normalize(payload["data"] if isinstance(payload, dict) else payload)
print(df.dtypes, "\n")
print(df.head(10).to_string(), "\n")

key = ["settlementDate", "settlementPeriod"]
dupes = df.duplicated(subset=key).sum()
print(f"rows: {len(df)}   duplicate keys: {dupes}")
if dupes:
    ex = df[df.duplicated(subset=key, keep=False)].sort_values(key + ["publishTime"])
    print(ex.head(12).to_string())