from pathlib import Path
import httpx, pandas as pd, matplotlib.pyplot as plt

BASE = "https://data.elexon.co.uk/bmrs/api/v1"
FROM, TO = "2026-06-01T00:00Z", "2026-06-08T00:00Z"
FIGS = Path("figures"); FIGS.mkdir(exist_ok=True)

def get(path, **params):
    r = httpx.get(f"{BASE}{path}", params={"format": "json", **params}, timeout=30.0)
    r.raise_for_status()
    return pd.json_normalize(r.json()["data"])

indo = get("/datasets/INDO", publishDateTimeFrom=FROM, publishDateTimeTo=TO)
ws   = get("/generation/actual/per-type/wind-and-solar", **{"from": FROM, "to": TO})

# EDIT these two lines once the probe tells you the real names
solar = ws[ws["psrType"] == "Solar"][["settlementDate", "settlementPeriod", "quantity"]]
solar = solar.rename(columns={"quantity": "solar"})

df = indo.merge(solar, on=["settlementDate", "settlementPeriod"], how="left")
print("unmatched INDO rows:", df["solar"].isna().sum())

df["reconstructed"] = df["demand"] + df["solar"]
df["local"] = pd.to_datetime(df["startTime"], utc=True).dt.tz_convert("Europe/London")
df["hod"] = df["local"].dt.hour + df["local"].dt.minute / 60
df["day"] = df["local"].dt.date

fig, ax = plt.subplots(figsize=(9, 5.5))
for day, g in df.groupby("day"):
    g = g.sort_values("hod")
    ax.plot(g["hod"], g["demand"] / 1000, color="tab:blue", alpha=0.6, lw=1.2)
    ax.plot(g["hod"], g["reconstructed"] / 1000, color="tab:red", alpha=0.6, lw=1.2)

ax.plot([], [], color="tab:blue", label="INDO (as published)")
ax.plot([], [], color="tab:red", label="INDO + estimated embedded solar")
ax.set(xlabel="hour of day (Europe/London)", ylabel="GW",
       title="Does adding embedded solar back close the midday sag? June 2026")
ax.set_xlim(0, 24); ax.set_xticks(range(0, 25, 3)); ax.grid(alpha=0.3); ax.legend()
fig.tight_layout()
fig.savefig(FIGS / "2026-07-13_embedded_solar_test.png", dpi=150)

peak = df[df["hod"].between(11, 15)].groupby("day")["solar"].max() / 1000
print("\nmax midday solar by day (GW):\n", peak.round(2).to_string())

print("INDO rows:", len(indo), "solar rows:", len(solar))
print("solar SPs present:", sorted(solar["settlementPeriod"].unique()))
print("\nrows per day:")
print(solar.groupby("settlementDate").size())
print("\ndupes on key:",
      solar.duplicated(["settlementDate", "settlementPeriod"]).sum())