import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

from validate_report import parse_report, validate  # noqa: E402

GOOD = """Checked 5 claims: 1 verified, 1 partial, 1 unverified, 1 contradicted, 1 skipped.
Verdict: Fix 1 claims before publishing.

## Ledger

| # | Claim | Status | Evidence | Fix |
| --- | --- | --- | --- | --- |
| 1 | "July 16, 1968" | CONTRADICTED | https://example.org/apollo — launch date July 16, 1969 | July 16, 1969 |
| 2 | "first woman in space" | VERIFIED | https://example.org/a — Tereshkova 1963; https://example.net/b — same | |
| 3 | "111 metres" | PARTIAL | https://example.org/saturn — 110.6 m | |
| 4 | "400,000 people" | UNVERIFIED | searched: "apollo workforce", "apollo 400000 people" — no primary source | |
| 5 | "greatest mission" | SKIPPED | opinion | |

## Annotated copy

Apollo 11 launched on July 16, 1968 [CN-1 CONTRADICTED: July 16, 1969 — example.org] and landed.
"""


class ParseTests(unittest.TestCase):
    def test_parses_rows_summary_verdict_markers(self):
        r = parse_report(GOOD)
        self.assertEqual(len(r.rows), 5)
        self.assertEqual(r.rows[0].status, "CONTRADICTED")
        self.assertEqual(r.rows[0].claim, "July 16, 1968")
        self.assertEqual(r.rows[0].fix, "July 16, 1969")
        self.assertEqual(r.rows[1].urls, ["https://example.org/a", "https://example.net/b"])
        self.assertEqual(r.summary_total, 5)
        self.assertEqual(r.summary_counts["CONTRADICTED"], 1)
        self.assertEqual(r.verdict, "Fix 1 claims before publishing")
        self.assertEqual(len(r.markers), 1)
        self.assertIn("Apollo 11 launched", r.annotated)

    def test_good_report_validates(self):
        self.assertEqual(validate(parse_report(GOOD)), [])

    def test_escaped_pipe_in_claim(self):
        text = GOOD.replace('"July 16, 1968"', '"a \\| b"')
        r = parse_report(text)
        self.assertEqual(r.rows[0].claim, "a | b")


class ValidateTests(unittest.TestCase):
    def problems(self, text):
        return validate(parse_report(text))

    def test_contradicted_needs_fix(self):
        bad = GOOD.replace("| July 16, 1969 |", "| |")
        self.assertTrue(any("requires a proposed fix" in p for p in self.problems(bad)))

    def test_verified_needs_two_urls_or_primary(self):
        bad = GOOD.replace("; https://example.net/b — same", "")
        self.assertTrue(any("VERIFIED with one URL" in p for p in self.problems(bad)))
        ok = GOOD.replace("; https://example.net/b — same", " (primary source)")
        self.assertFalse(any("VERIFIED" in p for p in self.problems(ok)))

    def test_verified_without_url_fails(self):
        bad = GOOD.replace(
            "https://example.org/a — Tereshkova 1963; https://example.net/b — same", "I remember this"
        )
        self.assertTrue(any("VERIFIED without any source URL" in p for p in self.problems(bad)))

    def test_unverified_needs_queries(self):
        bad = GOOD.replace('searched: "apollo workforce", "apollo 400000 people" — no primary source', "could not find")
        self.assertTrue(any("UNVERIFIED must list" in p for p in self.problems(bad)))

    def test_skipped_needs_reason(self):
        bad = GOOD.replace("| SKIPPED | opinion |", "| SKIPPED | meh |")
        self.assertTrue(any("SKIPPED needs a reason" in p for p in self.problems(bad)))

    def test_unknown_status(self):
        bad = GOOD.replace("| PARTIAL |", "| PROBABLY |")
        self.assertTrue(any("unknown status" in p for p in self.problems(bad)))

    def test_summary_mismatch(self):
        bad = GOOD.replace("Checked 5 claims", "Checked 6 claims")
        self.assertTrue(any("summary says 6 claims" in p for p in self.problems(bad)))
        bad2 = GOOD.replace("1 contradicted", "2 contradicted")
        self.assertTrue(any("summary says 2 contradicted" in p for p in self.problems(bad2)))

    def test_verdict_consistency(self):
        bad = GOOD.replace("Verdict: Fix 1 claims before publishing.", "Verdict: Safe to publish.")
        self.assertTrue(any("verdict should be 'Fix 1" in p for p in self.problems(bad)))

    def test_marker_must_match_ledger(self):
        bad = GOOD.replace("[CN-1 CONTRADICTED:", "[CN-1 OUTDATED:")
        self.assertTrue(any("marker for row 1 says OUTDATED" in p for p in self.problems(bad)))
        bad2 = GOOD.replace("[CN-1 CONTRADICTED:", "[CN-9 CONTRADICTED:")
        self.assertTrue(any("refers to row 9" in p for p in self.problems(bad2)))

    def test_not_verified_verdict_when_nothing_checked(self):
        text = """Checked 2 claims: 2 unchecked.
Verdict: Not verified.

## Ledger

| # | Claim | Status | Evidence | Fix |
| --- | --- | --- | --- | --- |
| 1 | "a" | UNCHECKED | no web access | |
| 2 | "b" | UNCHECKED | no web access | |
"""
        self.assertEqual(self.problems(text), [])
        bad = text.replace("Verdict: Not verified.", "Verdict: Safe to publish.")
        self.assertTrue(any("Not verified" in p for p in self.problems(bad)))

    def test_no_ledger(self):
        self.assertTrue(any("no ledger" in p for p in self.problems("nothing here")))


if __name__ == "__main__":
    unittest.main()
