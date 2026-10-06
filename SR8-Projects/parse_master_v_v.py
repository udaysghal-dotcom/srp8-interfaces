#!/usr/bin/env python3
"""Parse ADR_Database(MASTER V&V).csv into one JSON file per project ID.

Each row becomes ``<Project ID>.json`` in the same directory as this script.
Empty cells are written as null. ADR columns are kept in order, including
duplicates, and blank ADR cells are dropped.

Usage:
    python parse_master_v_v.py
"""

from __future__ import annotations

import csv
import json
from pathlib import Path

DIRECTORY = Path(__file__).resolve().parent
CSV_PATH = DIRECTORY / "ADR_Database(MASTER V&V).csv"

ADR_COLUMNS = (
    "1st ADR",
    "2nd ADR",
    "3rd ADR",
    "4th ADR",
    "5th ADR",
    "6th ADR",
)


def cell(value: str | None) -> str | None:
    if value is None:
        return None
    text = value.strip()
    return text or None


def row_to_record(row: dict[str, str]) -> dict:
    adrs = [adr for column in ADR_COLUMNS if (adr := cell(row.get(column)))]
    return {
        "project_id": cell(row.get("Project ID")),
        "project_name": cell(row.get("Project Name")),
        "primary_department": cell(row.get("Primary Department")),
        "secondary_department": cell(row.get("Secondary Department")),
        "adrs": adrs,
    }


def main() -> None:
    with CSV_PATH.open(newline="", encoding="utf-8-sig") as handle:
        rows = list(csv.DictReader(handle))

    written = 0
    for row in rows:
        record = row_to_record(row)
        project_id = record["project_id"]
        if not project_id:
            continue
        out_path = DIRECTORY / f"{project_id}.json"
        out_path.write_text(
            json.dumps(record, indent=2, ensure_ascii=False) + "\n",
            encoding="utf-8",
        )
        written += 1

    print(f"Wrote {written} project JSON files to {DIRECTORY}")


if __name__ == "__main__":
    main()
