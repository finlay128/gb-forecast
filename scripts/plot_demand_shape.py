from pathlib import Path

import httpx
import matplotlib.pyplot as plt
import pandas as pd

BASE = "https://data.elexon.co.uk/bmrs/api/v1"
FIGS = Path("figures")
FIGS.mkdir(exist_ok=True)


def fetch(dataset: str, start: str, end: str) -> pd.DataFrame:
    r = httpx.get(
        f"{BASE}/datasets/{dataset}",
        params={
            "publishDateTimeFrom": start,
            "publishDateTimeTo": end,
            "format": "json",
        },
        timeout=30.0,
    )
    r.raise_for_status()
    df = pd.json_normalize(r.json()["data"])
    # startTime is UTC; solar and human behaviour both follow LOCAL time
    df["utc"] = pd.to_datetime(df["startTime"], utc=True)
    df["local"] = df["utc"].dt.tz_convert("Europe/London")
    df["local_day"] = df["local"].dt.date
    df["hour_of_day"] = df["local"].dt.hour + df["local"].dt.minute / 60
    return df.sort_values("utc")


windows = {
    "June 2026": ("2026-06-01T00:00Z", "2026-06-08T00:00Z"),
    "January 2026": ("2026-01-12T00:00Z", "2026-01-19T00:00Z"),
}

fig, axes = plt.subplots(1, 2, figsize=(13, 5), sharey=True)

for ax, (label, (start, end)) in zip(axes, windows.items()):
    df = fetch("INDO", start, end)
    for day, grp in df.groupby("local_day"):
        weekend = pd.Timestamp(day).dayofweek >= 5
        ax.plot(
            grp["hour_of_day"],
            grp["demand"] / 1000,
            color="tab:orange" if weekend else "tab:blue",
            alpha=0.75,
            linewidth=1.4,
            label="weekend" if weekend else "weekday",
        )
    ax.set_title(f"INDO — {label}")
    ax.set_xlabel("hour of day (Europe/London)")
    ax.set_xlim(0, 24)
    ax.set_xticks(range(0, 25, 3))
    ax.grid(alpha=0.3)

    # dedupe legend labels
    handles, labels = ax.get_legend_handles_labels()
    seen = dict(zip(labels, handles))
    ax.legend(seen.values(), seen.keys(), loc="lower right", fontsize=8)

axes[0].set_ylabel("National Demand (GW)")
fig.suptitle("GB National Demand by hour of day — summer vs winter week")
fig.tight_layout()
fig.savefig(FIGS / "2026-07-13_indo_daily_shape.png", dpi=150)
print("wrote", FIGS / "2026-07-13_indo_daily_shape.png")