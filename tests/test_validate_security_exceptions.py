"""Positive and negative tests for exception-ledger validation."""

from datetime import date, timedelta
import unittest

from scripts.validate_security_exceptions import validate

HEADER = "| ID | Finding | Scope | Rationale | Owner | Last reviewed | Review cadence | Status |"
IGNORE = "deadbeef:.github/workflows/security-baseline.yml:aws-access-token:49"


def ledger(reviewed: str, row_id: str = "SECEX-001", status: str = "Active") -> str:
    return "\n".join(
        [
            "# Security Exceptions",
            "",
            HEADER,
            "|---|---|---|---|---|---|---|---|",
            f"| {row_id} | Finding | deadbeef:.github/workflows/security-baseline.yml:aws-access-token:49 | Rationale | Team | {reviewed} | Quarterly | {status} |",
        ]
    )


class ValidateSecurityExceptionsTests(unittest.TestCase):
    TODAY = date(2026, 11, 14)

    def test_current_review_passes(self):
        self.assertEqual(validate(ledger("2026-11-14"), self.TODAY, IGNORE), 1)

    def test_review_at_120_day_boundary_passes(self):
        reviewed = (self.TODAY - timedelta(days=120)).isoformat()
        self.assertEqual(validate(ledger(reviewed), self.TODAY, IGNORE), 1)

    def test_stale_review_fails(self):
        reviewed = (self.TODAY - timedelta(days=121)).isoformat()
        with self.assertRaisesRegex(ValueError, "maintainer review is overdue"):
            validate(ledger(reviewed), self.TODAY, IGNORE)

    def test_future_review_date_fails(self):
        with self.assertRaisesRegex(ValueError, "date is in the future"):
            validate(ledger("2026-11-15"), self.TODAY, IGNORE)

    def test_malformed_review_date_fails(self):
        with self.assertRaisesRegex(ValueError, "must be YYYY-MM-DD"):
            validate(ledger("14-11-2026"), self.TODAY, IGNORE)

    def test_missing_review_date_fails(self):
        with self.assertRaisesRegex(ValueError, "must be YYYY-MM-DD"):
            validate(ledger(""), self.TODAY, IGNORE)

    def test_missing_exception_rows_fail_by_default(self):
        content = "\n".join([HEADER, "|---|---|---|---|---|---|---|---|"])
        with self.assertRaisesRegex(ValueError, "No security exception entries"):
            validate(content, self.TODAY)

    def test_empty_ledger_is_allowed_only_with_empty_ignore_file(self):
        content = "\n".join([HEADER, "|---|---|---|---|---|---|---|---|"])
        self.assertEqual(validate(content, self.TODAY, "", allow_empty_ledger=True), 0)
        with self.assertRaisesRegex(ValueError, "not documented by an active exception"):
            validate(content, self.TODAY, IGNORE, allow_empty_ledger=True)

    def test_missing_table_header_fails(self):
        with self.assertRaisesRegex(ValueError, "table or Last reviewed column is missing"):
            validate("# Security Exceptions\nNo table", self.TODAY)

    def test_malformed_row_with_fewer_than_eight_columns_fails(self):
        content = ledger("2026-11-14").replace(
            "| SECEX-001 | Finding | deadbeef:.github/workflows/security-baseline.yml:aws-access-token:49 | Rationale | Team | 2026-11-14 | Quarterly | Active |",
            "| SECEX-001 | Finding | Rationale | Team | 2026-11-14 | Active |",
        )
        with self.assertRaisesRegex(ValueError, "expected 8"):
            validate(content, self.TODAY)

    def test_typoed_exception_id_fails(self):
        with self.assertRaisesRegex(ValueError, "unrecognised exception ID"):
            validate(ledger("2026-11-14", row_id="SECEX-00X"), self.TODAY)

    def test_stray_table_row_fails(self):
        content = ledger("2026-11-14") + "\n| NOT-AN-EXCEPTION | stray | row |"
        with self.assertRaisesRegex(ValueError, "expected 8"):
            validate(content, self.TODAY)

    def test_indented_table_row_fails(self):
        content = ledger("2026-11-14").replace("| SECEX-001", "  | SECEX-001")
        with self.assertRaisesRegex(ValueError, "indented Markdown table row"):
            validate(content, self.TODAY)

    def test_missing_leading_pipe_fails(self):
        content = ledger("2026-11-14").replace("| SECEX-001", "SECEX-001", 1)
        with self.assertRaisesRegex(ValueError, "must start with"):
            validate(content, self.TODAY)

    def test_ignore_entry_must_match_active_exception(self):
        with self.assertRaisesRegex(ValueError, "not documented by an active exception"):
            validate(ledger("2026-11-14"), self.TODAY, "untracked:ignore:entry:1")

    def test_inactive_exception_does_not_authorise_ignore(self):
        with self.assertRaisesRegex(ValueError, "not documented by an active exception"):
            validate(ledger("2026-11-14", status="Inactive"), self.TODAY, IGNORE)


if __name__ == "__main__":
    unittest.main()
