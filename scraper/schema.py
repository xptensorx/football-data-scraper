from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any, Dict, Iterable, Optional


CSV_COLUMNS = [
    "league",
    "season",
    "date",
    "home_team",
    "away_team",
    "venue",
    "home_score",
    "away_score",
    "round",
    "referee",
    "attendance",
    "event_type",
    "event_time",
    "player",
]


@dataclass(frozen=True)
class MatchEventRow:
    league: str
    season: str
    date: str  # ISO yyyy-mm-dd (local date at venue if available)
    home_team: str
    away_team: str
    venue: str
    home_score: int
    away_score: int
    round: str
    referee: str
    attendance: Optional[int]
    event_type: str  # goal/substitution/card/shots_on_goal/... etc.
    event_time: str  # minute, e.g. "67" or "90+2"
    player: str

    def to_csv_dict(self) -> Dict[str, Any]:
        d = asdict(self)
        if d["attendance"] is None:
            d["attendance"] = ""
        return d


def validate_columns(columns: Iterable[str]) -> None:
    cols = list(columns)
    if cols != CSV_COLUMNS:
        raise ValueError(f"CSV columns must be exactly {CSV_COLUMNS}, got {cols}")

