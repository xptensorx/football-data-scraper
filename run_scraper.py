from __future__ import annotations

import json
from pathlib import Path

from scraper.current_season import scrape_current_season
from scraper.io import write_rows_csv


def main() -> None:
    base_dir = Path(__file__).resolve().parent
    cfg_path = base_dir / "config" / "default.json"
    cfg = json.loads(cfg_path.read_text(encoding="utf-8"))

    out_path = base_dir / cfg.get("output_csv", "output/matches_events.csv")
    append = bool(cfg.get("append", True))

    # Placeholder season label until wired to a real source.
    season = "CURRENT"
    written_total = 0

    for league in cfg.get("leagues", []):
        league_name = league["name"]
        rows = scrape_current_season(league_name, season)
        written_total += write_rows_csv(out_path, rows, append=append)

    print(f"Wrote {written_total} rows to {out_path}")


if __name__ == "__main__":
    main()

