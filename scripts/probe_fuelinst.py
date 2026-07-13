import httpx, pandas as pd

pd.set_option("display.width", 160)
BASE = "https://data.elexon.co.uk/bmrs/api/v1"

r = httpx.get(
    f"{BASE}/generation/outturn/summary",
    params={
        "from": "2026-06-02T00:00Z",
        "to": "2026-06-04T00:00Z",
        "format": "json",
    },
    timeout=30.0,
)
r.raise_for_status()
payload = r.json()
df = pd.json_normalize(
    payload["data"],
    record_path="data",
    meta=["startTime", "settlementPeriod"],
)

print(df.dtypes, "\n")
print(df.head(8).to_string(), "\n")

for col in df.columns:
    if df[col].nunique() < 25:
        print(f"{col}: {sorted(df[col].unique())[:25]}")