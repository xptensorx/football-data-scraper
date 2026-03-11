from __future__ import annotations

import csv
import os
from pathlib import Path
from typing import Iterable

from .schema import CSV_COLUMNS, MatchEventRow, validate_columns


def ensure_parent_dir(path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)


def write_rows_csv(path: Path, rows: Iterable[MatchEventRow], append: bool) -> int:
    """
    Writes rows to CSV. If append=True and file exists, appends without re-writing header.
    Returns number of rows written.
    """
    ensure_parent_dir(path)

    file_exists = path.exists()
    mode = "a" if append else "w"
    newline = ""

    written = 0
    with path.open(mode, newline=newline, encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=CSV_COLUMNS, extrasaction="ignore")

        if not (append and file_exists):
            validate_columns(writer.fieldnames)
            writer.writeheader()

        for r in rows:
            writer.writerow(r.to_csv_dict())
            written += 1
    return written

