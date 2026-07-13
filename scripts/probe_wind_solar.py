import httpx, pandas as pd

pd.set_option("display.width", 140)

r = httpx.get(
    "https://data.elexon.co.uk/bmrs/api/v1/generation/actual/per-type/wind-and-solar",
    params={
        "from": "2026-06-02T20:00Z",
        "to": "2026-06-04T04:00Z",
        "format": "json",
    },
    timeout=30.0,
)
r.raise_for_status()
df = pd.json_normalize(r.json()["data"])

print(df.dtypes, "\n")
print(df.head(10).to_string(), "\n")

for col in df.columns:
    if df[col].nunique() < 12:
        print(f"{col}: {sorted(df[col].unique())}")


solar = df[df["psrType"] == "Solar"]
present = set(zip(solar["settlementDate"], solar["settlementPeriod"]))
missing = [sp for sp in range(1, 49)
           if ("2026-06-03", sp) not in present]
print("missing SPs on 2026-06-03:", missing)