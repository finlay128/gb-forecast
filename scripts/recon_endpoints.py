"""Download the Elexon Insights OpenAPI spec and flatten it into a readable CSV."""

import csv
import json
from pathlib import Path

import httpx

SPEC_URL = "https://data.elexon.co.uk/swagger/v1/swagger.json"
RAW_DIR = Path("data/raw")
DOCS_DIR = Path("docs")


def main() -> None:
    RAW_DIR.mkdir(parents=True, exist_ok=True)
    DOCS_DIR.mkdir(parents=True, exist_ok=True)

    resp = httpx.get(SPEC_URL, timeout=30.0)
    resp.raise_for_status()
    spec = resp.json()

    (RAW_DIR / "swagger.json").write_text(json.dumps(spec, indent=2))

    base_url = spec["servers"][0]["url"]
    print(f"base URL: {base_url}\n")

    rows = []
    for path, methods in spec["paths"].items():
        for verb, op in methods.items():
            params = op.get("parameters", [])
            rows.append(
                {
                    "tag": ", ".join(op.get("tags", [])),
                    "path": path,
                    "summary": op.get("summary", ""),
                    "required_params": ",".join(
                        p["name"] for p in params if p.get("required")
                    ),
                    "all_params": ",".join(p["name"] for p in params),
                }
            )

    rows.sort(key=lambda r: (r["tag"], r["path"]))

    out = DOCS_DIR / "endpoints.csv"
    with out.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)

    tags = sorted({r["tag"] for r in rows})
    print(f"{len(rows)} operations across {len(tags)} tags -> {out}\n")
    for tag in tags:
        n = sum(1 for r in rows if r["tag"] == tag)
        print(f"  {n:>4}  {tag}")


if __name__ == "__main__":
    main()