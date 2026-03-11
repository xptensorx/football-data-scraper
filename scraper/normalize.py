from __future__ import annotations

import re
from typing import Dict


_WS = re.compile(r"\s+")


def normalize_team_name(name: str, alias_map: Dict[str, str] | None = None) -> str:
    """
    Normalize team names for consistent cross-league output.
    This is intentionally conservative; extend alias_map over time.
    """
    n = _WS.sub(" ", (name or "").strip())
    if not n:
        return n

    # Common punctuation normalization
    n = n.replace("\u00a0", " ")  # non-breaking space
    n = n.replace("’", "'")

    if alias_map:
        return alias_map.get(n, n)
    return n

