from __future__ import annotations

import json
from pathlib import Path

from scraper.historical import scrape_historical
from scraper.io import write_rows_csv


def _season_labels(mode: str, count: int) -> list[str]:
    # Placeholder labeling. When we wire a real source, this will map to real season IDs.
    if mode == "current_and_previous":
        return ["CURRENT", "PREVIOUS"][:count]
    return [f"SEASON_{i+1}" for i in range(count)]


def main() -> None:
    base_dir = Path(__file__).resolve().parent
    cfg_path = base_dir / "config" / "default.json"
    cfg = json.loads(cfg_path.read_text(encoding="utf-8"))

    out_path = base_dir / cfg.get("output_csv", "output/matches_events.csv")
    append = bool(cfg.get("append", True))

    seasons_cfg = cfg.get("seasons", {"mode": "current_and_previous", "count": 2})
    seasons = _season_labels(seasons_cfg.get("mode", "current_and_previous"), int(seasons_cfg.get("count", 2)))

    written_total = 0
    for league in cfg.get("leagues", []):
        league_name = league["name"]
        for season in seasons:
            rows = scrape_historical(league_name, season)
            written_total += write_rows_csv(out_path, rows, append=append)

    print(f"Wrote {written_total} rows to {out_path}")


if __name__ == "__main__":
    main()

