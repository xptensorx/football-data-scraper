from __future__ import annotations

import json
import time
from datetime import date
from pathlib import Path

from scraper.historical import scrape_historical
from scraper.io import write_rows_csv


def _football_data_season_for_day(d: date) -> str:
    # football-data.co.uk uses "2324" style season IDs (startYYendYY).
    start_year = d.year if d.month >= 7 else d.year - 1
    end_year = start_year + 1
    return f"{start_year % 100:02d}{end_year % 100:02d}"


def _previous_season_id(season_id: str) -> str:
    # "2324" -> "2223"
    if len(season_id) != 4 or not season_id.isdigit():
        raise ValueError(f"Invalid season id {season_id!r}; expected '2324' format")
    start_yy = int(season_id[:2])
    end_yy = int(season_id[2:])
    return f"{(start_yy - 1) % 100:02d}{(end_yy - 1) % 100:02d}"


def _resolve_seasons(seasons_cfg: object) -> list[str]:
    # Supports:
    # - explicit list: ["2324", "2223", ...]
    # - dict mode: {"mode":"current_and_previous","count":2}
    if isinstance(seasons_cfg, list):
        return [str(s).strip() for s in seasons_cfg if str(s).strip()]

    if isinstance(seasons_cfg, dict):
        mode = str(seasons_cfg.get("mode", "current_and_previous"))
        count = int(seasons_cfg.get("count", 2))
        if count <= 0:
            return []

        if mode == "current_and_previous":
            cur = _football_data_season_for_day(date.today())
            seasons: list[str] = [cur]
            while len(seasons) < count:
                seasons.append(_previous_season_id(seasons[-1]))
            return seasons

        raise ValueError(f"Unsupported seasons mode {mode!r} (expected 'current_and_previous' or an explicit list)")

    # Default
    return _resolve_seasons({"mode": "current_and_previous", "count": 2})


def main() -> None:
    base_dir = Path(__file__).resolve().parent
    cfg_path = base_dir / "config" / "default.json"
    cfg = json.loads(cfg_path.read_text(encoding="utf-8"))

    out_path = base_dir / cfg.get("output_csv", "output/matches_events.csv")
    append = bool(cfg.get("append", True))
    rate_limit_seconds = float(cfg.get("rate_limit_seconds", 0.0) or 0.0)

    seasons_cfg = cfg.get("seasons", {"mode": "current_and_previous", "count": 2})
    seasons = _resolve_seasons(seasons_cfg)

    written_total = 0
    for league in cfg.get("leagues", []):
        league_name = league["name"]
        league_code = league.get("football_data_code") or league.get("code")
        for season in seasons:
            rows = scrape_historical(league_name, season, league_code=league_code)
            written_total += write_rows_csv(out_path, rows, append=append)
            if rate_limit_seconds > 0:
                time.sleep(rate_limit_seconds)

    print(f"Wrote {written_total} rows to {out_path}")


if __name__ == "__main__":
    main()

