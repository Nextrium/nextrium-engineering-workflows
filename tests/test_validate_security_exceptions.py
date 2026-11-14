"""Positive and negative tests for security exception review-date validation."""

from datetime import date, timedelta
import unittest

from scripts.validate_security_exceptions import validate

HEADER = "| ID | Finding | Scope | Rationale | Owner | Last reviewed | Review cadence | Status |"


def ledger(reviewed: str) -> str:
    return "\n".join(
        [
            "# Security Exceptions",
            "",
            HEADER,
            "|---|---|---|---|---|---|---|---|",
            f"| SECEX-001 | Example | Exact scope | Rationale | Team | {reviewed} | Quarterly | Active |",
        ]
    )


class ValidateSecurityExceptionsTests(unittest.TestCase):
    TODAY = date(2026, 11, 14)

    def test_current_review_passes(self):
        self.assertEqual(validate(ledger("2026-11-14"), self.TODAY), 1)

    def test_review_at_120_day_boundary_passes(self):
        reviewed = (self.TODAY - timedelta(days=120)).isoformat()
        self.assertEqual(validate(ledger(reviewed), self.TODAY), 1)

    def test_stale_review_fails(self):
        reviewed = (self.TODAY - timedelta(days=121)).isoformat()
        with self.assertRaisesRegex(ValueError, "maintainer review is overdue"):
            validate(ledger(reviewed), self.TODAY)

    def test_future_review_date_fails(self):
        with self.assertRaisesRegex(ValueError, "date is in the future"):
            validate(ledger("2026-11-15"), self.TODAY)

    def test_malformed_review_date_fails(self):
        with self.assertRaisesRegex(ValueError, "must be YYYY-MM-DD"):
            validate(ledger("14-11-2026"), self.TODAY)

    def test_missing_exception_rows_fail(self):
        content = "\n".join([HEADER, "|---|---|---|---|---|---|---|---|"])
        with self.assertRaisesRegex(ValueError, "No security exception entries"):
            validate(content, self.TODAY)

    def test_missing_table_header_fails(self):
        with self.assertRaisesRegex(ValueError, "table or Last reviewed column is missing"):
            validate("# Security Exceptions\nNo table", self.TODAY)


if __name__ == "__main__":
    unittest.main()
