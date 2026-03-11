from __future__ import annotations

import csv
import io
from datetime import date as _date
from typing import Iterable, List, Optional

import requests
from dateutil import parser as date_parser

from .normalize import normalize_team_name
from .schema import MatchEventRow


_LEAGUE_NAME_TO_FOOTBALL_DATA_CODE: dict[str, str] = {
    "EPL": "E0",
    "Premier League": "E0",
    "Championship": "E1",
    "LaLiga": "SP1",
    "La Liga": "SP1",
    "SerieA": "I1",
    "Serie A": "I1",
    "Bundesliga": "D1",
}


def _pick(row: dict[str, str], keys: list[str]) -> str:
    for k in keys:
        v = row.get(k, "")
        if v is None:
            continue
        v = str(v).strip()
        if v:
            return v
    return ""


def _parse_int(s: str) -> Optional[int]:
    s = (s or "").strip()
    if not s:
        return None
    try:
        return int(float(s))
    except ValueError:
        return None


def _to_iso_date(s: str) -> str:
    s = (s or "").strip()
    if not s:
        return ""
    try:
        # football-data.co.uk often uses dd/mm/yy or dd/mm/yyyy.
        return date_parser.parse(s, dayfirst=True, fuzzy=True).date().isoformat()
    except Exception:
        return s


def scrape_historical(
    league_name: str,
    season: str,
    *,
    team_aliases: dict[str, str] | None = None,
    league_code: str | None = None,
) -> Iterable[MatchEventRow]:
    """
    Downloads historical match data from football-data.co.uk for a league + season.

    Note: football-data.co.uk provides match-level rows (not per-event timelines),
    so we emit one row per match with `event_type="match"` and empty event fields.
    """
    code = (league_code or "").strip() or _LEAGUE_NAME_TO_FOOTBALL_DATA_CODE.get(league_name)
    if not code:
        raise ValueError(
            f"Missing football-data league code for {league_name!r}. "
            f"Set leagues[].football_data_code in config or extend mapping."
        )

    url = f"https://www.football-data.co.uk/mmz4281/{season}/{code}.csv"
    headers = {"User-Agent": "football-data-scraper/1.0"}
    resp = requests.get(url, headers=headers, timeout=30)
    resp.raise_for_status()

    # Handle potential BOM and mixed encodings conservatively.
    text = resp.content.decode("utf-8-sig", errors="replace")
    reader = csv.DictReader(io.StringIO(text))

    rows: List[MatchEventRow] = []
    for r in reader:
        home_raw = _pick(r, ["HomeTeam", "Home", "Home Team"])
        away_raw = _pick(r, ["AwayTeam", "Away", "Away Team"])
        date_raw = _pick(r, ["Date", "MatchDate", "match_date"])
        if not home_raw or not away_raw or not date_raw:
            continue

        home = normalize_team_name(home_raw, team_aliases)
        away = normalize_team_name(away_raw, team_aliases)
        iso_date = _to_iso_date(date_raw)

        home_score = _parse_int(_pick(r, ["FTHG", "HG", "HomeGoals", "Home Score"]))
        away_score = _parse_int(_pick(r, ["FTAG", "AG", "AwayGoals", "Away Score"]))
        if home_score is None or away_score is None:
            # Skip fixtures with no final score recorded yet.
            continue

        referee = _pick(r, ["Referee", "referee"])

        rows.append(
            MatchEventRow(
                league=league_name,
                season=season,
                date=iso_date or _date.today().isoformat(),
                home_team=home,
                away_team=away,
                venue="",
                home_score=home_score,
                away_score=away_score,
                round="",
                referee=referee,
                attendance=None,
                event_type="match",
                event_time="",
                player="",
            )
        )

    return rows

