import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

import run_evals  # noqa: E402

TRUTH = {
    "planted": [
        {"id": "p1", "span": "July 16, 1968", "expected": ["CONTRADICTED"]},
        {"id": "p2", "span": "one giant leap for humanity", "expected": ["PARAPHRASED"]},
        {"id": "p3", "span": "78 million kilometres", "expected": ["CONTRADICTED"]},
    ],
    "true": [{"span": "July 20, 1969"}, {"span": "born in Ohio in 1930"}],
    "skip": [{"span": "I have visited", "reason": "first-person"}],
}

REPORT = """Checked 6 claims: 1 verified, 3 contradicted, 1 unverified, 1 skipped.
Verdict: Fix 3 claims before publishing.

## Ledger

| # | Claim | Status | Evidence | Fix |
| --- | --- | --- | --- | --- |
| 1 | "lifted off from Kennedy Space Center on July 16, 1968" | CONTRADICTED | https://x.org/a — 1969 | July 16, 1969 |
| 2 | "one giant leap for humanity" | CONTRADICTED | https://x.org/b — mankind | for mankind |
| 3 | "78 million kilometres" | UNVERIFIED | searched: "mars distance sun" | |
| 4 | "July 20, 1969" | VERIFIED | https://x.org/c — yes; https://y.org/d — yes | |
| 5 | "born in Ohio in 1930" | CONTRADICTED | https://x.org/e — 1931 | 1931 |
| 6 | "I have visited the Kennedy Space Center twice" | SKIPPED | first-person | |
"""


class ScoreTests(unittest.TestCase):
    def test_scoring(self):
        r = run_evals.score(REPORT, TRUTH)
        self.assertEqual(r["planted_total"], 3)
        self.assertEqual(r["planted_caught"], 2)  # p3 was UNVERIFIED, not caught
        self.assertEqual(r["planted_exact"], 1)  # p2 caught as CONTRADICTED, expected PARAPHRASED
        self.assertEqual(r["false_alarms"], 1)  # true claim 'born in Ohio' flagged
        self.assertEqual(r["skip_violations"], 0)
        self.assertEqual(r["lint_problems"], [])

    def test_split_claims_credit_any_flagged_atom(self):
        # Agent split "first title came with Ferrari in 1994" into two rows; the
        # flagged atom must count as caught even though the shorter row is VERIFIED.
        report = """Checked 2 claims: 1 verified, 1 contradicted.
Verdict: Fix 1 claims before publishing.

## Ledger

| # | Claim | Status | Evidence | Fix |
| --- | --- | --- | --- | --- |
| 1 | "in 1994" | VERIFIED | https://x.org/a — yes; https://y.org/b — yes | |
| 2 | "his first title came with Ferrari" | CONTRADICTED | https://x.org/c — Benetton | Benetton |
"""
        truth = {"planted": [{"id": "p", "span": "first title came with Ferrari in 1994", "expected": ["CONTRADICTED"]}], "true": [], "skip": []}
        r = run_evals.score(report, truth)
        self.assertEqual(r["planted_caught"], 1)
        self.assertEqual(r["planted_exact"], 1)

    def test_missing_row_counts_as_missed(self):
        truth = dict(TRUTH, planted=TRUTH["planted"] + [{"id": "p9", "span": "not in report", "expected": ["CONTRADICTED"]}])
        r = run_evals.score(REPORT, truth)
        self.assertEqual(r["planted_missing_from_ledger"], 1)

    def test_skip_violation(self):
        report = REPORT.replace("| SKIPPED | first-person |", "| UNVERIFIED | searched: visits |")
        r = run_evals.score(report, TRUTH)
        self.assertEqual(r["skip_violations"], 1)

    def test_match_is_whitespace_and_quote_insensitive(self):
        report = REPORT.replace('"July 20, 1969"', "“July  20, 1969”")
        r = run_evals.score(report, TRUTH)
        self.assertEqual(r["false_alarms"], 1)
        self.assertTrue(any(d[1] == "July 20, 1969" and d[3] == "ok" for d in r["details"]))

    def test_results_markdown(self):
        r = run_evals.score(REPORT, TRUTH)
        md = run_evals.fmt_results_md("test", [("fx", r)], "2026-01-01")
        self.assertIn("| fx | 6 | 2/3 | 1/3 | 1/2 | 0/1 | 0 |", md)


class FixtureTests(unittest.TestCase):
    def test_fixtures_are_consistent(self):
        self.assertEqual(run_evals.validate_fixtures(), [])

    def test_every_fixture_has_enough_material(self):
        for name, _text, truth in run_evals.load_fixtures():
            self.assertGreaterEqual(len(truth["planted"]), 4, name)
            self.assertGreaterEqual(len(truth["true"]), 6, name)
            self.assertGreaterEqual(len(truth["skip"]), 2, name)

    def test_skill_body_strips_frontmatter(self):
        body = run_evals.skill_body()
        self.assertFalse(body.startswith("---"))
        self.assertIn("# citation-needed", body)

    def test_runner_substitution_inserts_skill_when_no_token(self):
        # Runner without {SKILL} gets the skill prepended to the prompt via stdin.
        runner = {"command": [sys.executable, "-X", "utf8", "-c", "import sys; print(sys.stdin.read())"]}
        out = run_evals.run_runner(runner, "TASK", timeout=60)
        self.assertIn("<skill>", out)
        self.assertIn("TASK", out)

    def test_runner_prompt_token_and_out_file(self):
        runner = {
            "command": [
                sys.executable,
                "-c",
                "import sys; open(sys.argv[1],'w',encoding='utf-8').write('R:'+sys.argv[2])",
                "{OUT}",
                "{PROMPT}",
            ]
        }
        out = run_evals.run_runner(runner, "TASK", timeout=60)
        self.assertTrue(out.startswith("R:Follow this skill"))
        self.assertTrue(out.endswith("TASK"))


if __name__ == "__main__":
    unittest.main()
