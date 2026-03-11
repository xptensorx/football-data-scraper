from __future__ import annotations

from datetime import date
from typing import Iterable, List

from .normalize import normalize_team_name
from .schema import MatchEventRow


def scrape_current_season(
    league_name: str,
    season: str,
    *,
    team_aliases: dict[str, str] | None = None,
) -> Iterable[MatchEventRow]:
    """
    Current-season scraper stub.

    Replace this with a real source integration (API or HTML parsing).
    It returns rows in the unified (match + event) CSV schema.
    """
    # Placeholder example row (no real network calls yet).
    today = date.today().isoformat()
    home = normalize_team_name("Home FC", team_aliases)
    away = normalize_team_name("Away FC", team_aliases)

    rows: List[MatchEventRow] = [
        MatchEventRow(
            league=league_name,
            season=season,
            date=today,
            home_team=home,
            away_team=away,
            venue="",
            home_score=0,
            away_score=0,
            round="",
            referee="",
            attendance=None,
            event_type="",
            event_time="",
            player="",
        )
    ]
    return rows

