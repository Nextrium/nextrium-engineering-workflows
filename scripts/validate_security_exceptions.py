#!/usr/bin/env python3
"""Validate that every security exception has a current human review date."""

from datetime import date
from pathlib import Path
import sys

HEADER = "| ID | Finding | Scope | Rationale | Owner | Last reviewed | Review cadence | Status |"
MAX_REVIEW_AGE_DAYS = 120


def validate(content: str, today: date) -> int:
    lines = content.splitlines()
    try:
        start = lines.index(HEADER) + 2
    except ValueError as exc:
        raise ValueError("Security exception table or Last reviewed column is missing.") from exc

    rows = [line for line in lines[start:] if line.startswith("| SECEX-")]
    if not rows:
        raise ValueError("No security exception entries found; review the exception ledger.")

    failures = []
    for row in rows:
        cells = [cell.strip() for cell in row.strip("|").split("|")]
        if len(cells) < 8:
            failures.append(f"Malformed exception row: {row}")
            continue

        exception_id, reviewed_text = cells[0], cells[5]
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

    if failures:
        raise ValueError("\n".join(failures))
    return len(rows)


def main() -> int:
    path = Path("docs/SECURITY-EXCEPTIONS.md")
    try:
        count = validate(path.read_text(encoding="utf-8"), date.today())
    except (OSError, ValueError) as exc:
        print(exc, file=sys.stderr)
        return 1
    print(f"All {count} security exception(s) have a review date within the 120-day window.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
