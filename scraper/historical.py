from __future__ import annotations

from typing import Iterable, List

from .normalize import normalize_team_name
from .schema import MatchEventRow


def scrape_historical(
    league_name: str,
    season: str,
    *,
    team_aliases: dict[str, str] | None = None,
) -> Iterable[MatchEventRow]:
    """
    Historical scraper stub.

    Replace with real integration that iterates all rounds/matches in a season
    and emits one CSV row per event (goals/subs/cards/stats entries, etc.).
    """
    # Placeholder example with a "goal" event.
    home = normalize_team_name("Historical Home", team_aliases)
    away = normalize_team_name("Historical Away", team_aliases)

    rows: List[MatchEventRow] = [
        MatchEventRow(
            league=league_name,
            season=season,
            date="2000-01-01",
            home_team=home,
            away_team=away,
            venue="",
            home_score=1,
            away_score=0,
            round="",
            referee="",
            attendance=None,
            event_type="goal",
            event_time="12",
            player="Example Scorer",
        )
    ]
    return rows

