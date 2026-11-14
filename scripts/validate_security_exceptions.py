#!/usr/bin/env python3
"""Validate human-review freshness and reconcile Gitleaks ignores with active exceptions."""

from __future__ import annotations

import argparse
from datetime import date
from pathlib import Path
import re
import sys

HEADER = "| ID | Finding | Scope | Rationale | Owner | Last reviewed | Review cadence | Status |"
MAX_REVIEW_AGE_DAYS = 120
EXCEPTION_ID = re.compile(r"SECEX-[0-9]{3}")


def validate(
    content: str,
    today: date,
    ignore_content: str = "",
    allow_empty_ledger: bool = False,
) -> int:
    lines = content.splitlines()
    try:
        header_index = lines.index(HEADER)
    except ValueError as exc:
        raise ValueError("Security exception table or Last reviewed column is missing.") from exc

    if header_index + 1 >= len(lines) or not lines[header_index + 1].lstrip().startswith("|---"):
        raise ValueError("Security exception table separator is missing.")

    rows: list[tuple[str, str]] = []
    failures: list[str] = []
    for line_number, line in enumerate(lines[header_index + 2 :], header_index + 3):
        if not line.strip():
            break
        if not line.startswith("|"):
            if line.lstrip().startswith("|"):
                failures.append(f"Line {line_number}: indented Markdown table row is not allowed.")
            break
        cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
        if len(cells) != 8:
            failures.append(
                f"Line {line_number}: malformed exception row has {len(cells)} columns; expected 8."
            )
            continue
        exception_id, reviewed_text = cells[0], cells[5]
        if not EXCEPTION_ID.fullmatch(exception_id):
            failures.append(f"Line {line_number}: unrecognised exception ID {exception_id!r}.")
            continue
        rows.append((exception_id, line))
        try:
            reviewed = date.fromisoformat(reviewed_text)
        except ValueError:
            failures.append(f"{exception_id}: Last reviewed must be YYYY-MM-DD.")
            continue

        age = (today - reviewed).days
        if age < 0:
            failures.append(f"{exception_id}: review date is in the future.")
        elif age > MAX_REVIEW_AGE_DAYS:
            failures.append(
                f"{exception_id}: last review is {age} days old; maintainer review is overdue."
            )

    if not rows and not allow_empty_ledger:
        failures.append("No security exception entries found; review the exception ledger.")

    ignore_entries = [
        line.strip()
        for line in ignore_content.splitlines()
        if line.strip() and not line.lstrip().startswith("#")
    ]
    active_rows = [
        row for exception_id, row in rows
        if "active" in row.lower()
    ]
    for entry in ignore_entries:
        parts = entry.split(":")
        if len(parts) < 4 or not any(all(part in row for part in parts) for row in active_rows):
            failures.append(
                f"Gitleaks ignore entry is not documented by an active exception: {entry}"
            )

    if not rows and ignore_entries:
        failures.append("An empty exception ledger requires an empty Gitleaks ignore file.")

    if failures:
        raise ValueError("\n".join(failures))
    return len(rows)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--ledger-path", default="docs/SECURITY-EXCEPTIONS.md")
    parser.add_argument("--ignore-path", default=".gitleaksignore")
    parser.add_argument("--allow-empty-ledger", action="store_true")
    args = parser.parse_args()
    try:
        ledger = Path(args.ledger_path).read_text(encoding="utf-8")
        ignore_path = Path(args.ignore_path)
        ignore_content = ignore_path.read_text(encoding="utf-8") if ignore_path.exists() else ""
        count = validate(ledger, date.today(), ignore_content, args.allow_empty_ledger)
    except (OSError, ValueError) as exc:
        print(exc, file=sys.stderr)
        return 1
    print(f"All {count} security exception(s) have a review date within the 120-day window.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
