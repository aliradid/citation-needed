#!/usr/bin/env python3
"""Validate a citation-needed report.

Checks that a report follows references/report-format.md closely enough to be
trusted: every ledger row has a valid status, evidence that matches the status,
a fix where the status requires one, and a summary line whose counts match the
ledger. Exit code 1 on any problem, 0 when clean.

Usage:
    python3 scripts/validate_report.py REPORT.md
    python3 scripts/validate_report.py - < REPORT.md

Importable: ``parse_report(text) -> Report`` and ``validate(report) -> list[str]``.
"""

from __future__ import annotations

import re
import sys
from dataclasses import dataclass, field

STATUSES = {
    "VERIFIED",
    "PARTIAL",
    "UNVERIFIED",
    "CONTRADICTED",
    "OUTDATED",
    "MISATTRIBUTED",
    "PARAPHRASED",
    "MISLEADING",
    "SKIPPED",
    "UNCHECKED",
}
PROBLEM_STATUSES = {"CONTRADICTED", "OUTDATED", "MISATTRIBUTED", "PARAPHRASED", "MISLEADING"}
FIX_REQUIRED = PROBLEM_STATUSES
SKIP_REASONS = {"opinion", "prediction", "first-person", "hypothetical", "common knowledge"}
UNCHECKED_REASONS = {"budget", "no web access"}

URL_RE = re.compile(r"https?://[^\s|)>\]]+")
SUMMARY_RE = re.compile(r"Checked\s+(\d+)\s+claims?\s*:\s*(.*?)\.?\s*$", re.IGNORECASE)
COUNT_RE = re.compile(r"(\d+)\s+([a-z-]+)", re.IGNORECASE)
VERDICT_RE = re.compile(r"Verdict\s*:\s*(.+?)\.?\s*$", re.IGNORECASE)


@dataclass
class Row:
    number: int
    claim: str
    status: str
    evidence: str
    fix: str
    line_no: int

    @property
    def urls(self) -> list[str]:
        return URL_RE.findall(self.evidence)


@dataclass
class Report:
    summary_total: int | None = None
    summary_counts: dict[str, int] = field(default_factory=dict)
    verdict: str | None = None
    rows: list[Row] = field(default_factory=list)
    annotated: str | None = None
    markers: list[str] = field(default_factory=list)


def _split_table_row(line: str) -> list[str]:
    inner = line.strip()
    if inner.startswith("|"):
        inner = inner[1:]
    if inner.endswith("|"):
        inner = inner[:-1]
    # Split on pipes that are not escaped.
    cells = re.split(r"(?<!\\)\|", inner)
    return [c.strip().replace("\\|", "|") for c in cells]


def parse_report(text: str) -> Report:
    report = Report()
    lines = text.splitlines()

    for line in lines:
        m = SUMMARY_RE.search(line)
        if m and report.summary_total is None:
            report.summary_total = int(m.group(1))
            for n, name in COUNT_RE.findall(m.group(2)):
                report.summary_counts[name.upper()] = int(n)
        v = VERDICT_RE.search(line)
        if v and report.verdict is None:
            report.verdict = v.group(1).strip()

    # Find the first markdown table whose header contains Claim and Status.
    in_table = False
    header_seen = False
    for idx, line in enumerate(lines, start=1):
        stripped = line.strip()
        if not in_table:
            if stripped.startswith("|") and "claim" in stripped.lower() and "status" in stripped.lower():
                in_table = True
                header_seen = True
            continue
        if not stripped.startswith("|"):
            break
        cells = _split_table_row(stripped)
        if header_seen and all(set(c) <= set("-: ") for c in cells):
            header_seen = False
            continue
        if len(cells) < 3:
            continue
        cells += [""] * (5 - len(cells))
        num_txt = cells[0].strip("*` ")
        try:
            number = int(num_txt)
        except ValueError:
            continue
        report.rows.append(
            Row(
                number=number,
                claim=cells[1].strip().strip('"“”'),
                status=cells[2].strip().strip("*` ").upper(),
                evidence=cells[3].strip(),
                fix=cells[4].strip(),
                line_no=idx,
            )
        )

    ann = re.search(r"^##\s+Annotated copy\s*$", text, re.MULTILINE | re.IGNORECASE)
    if ann:
        report.annotated = text[ann.end():]
    report.markers = re.findall(r"\[CN-\d+\s+[A-Z]+:[^\]]*\]", text)
    return report


def validate(report: Report) -> list[str]:
    problems: list[str] = []
    if not report.rows:
        problems.append("no ledger table found (expected a table with # | Claim | Status | Evidence | Fix)")
        return problems

    seen = set()
    for row in report.rows:
        where = f"row {row.number} (line {row.line_no})"
        if row.number in seen:
            problems.append(f"{where}: duplicate row number")
        seen.add(row.number)
        if not row.claim:
            problems.append(f"{where}: empty claim")
        if row.status not in STATUSES:
            problems.append(f"{where}: unknown status '{row.status}'")
            continue
        ev = row.evidence.lower()
        if row.status == "VERIFIED":
            if len(row.urls) < 1:
                problems.append(f"{where}: VERIFIED without any source URL")
            elif len(row.urls) < 2 and "primary" not in ev:
                problems.append(f"{where}: VERIFIED with one URL and no note that it is a primary source")
        elif row.status == "PARTIAL":
            if len(row.urls) < 1:
                problems.append(f"{where}: PARTIAL without a source URL")
        elif row.status in PROBLEM_STATUSES:
            if len(row.urls) < 1 and "internal" not in ev:
                problems.append(f"{where}: {row.status} without a source URL or 'internal'")
        elif row.status == "UNVERIFIED":
            if "searched" not in ev:
                problems.append(f"{where}: UNVERIFIED must list the queries ('searched: ...')")
        elif row.status == "SKIPPED":
            if not any(r in ev for r in SKIP_REASONS):
                problems.append(f"{where}: SKIPPED needs a reason from {sorted(SKIP_REASONS)}")
        elif row.status == "UNCHECKED":
            if not any(r in ev for r in UNCHECKED_REASONS):
                problems.append(f"{where}: UNCHECKED needs 'budget' or 'no web access'")
        if row.status in FIX_REQUIRED and not row.fix:
            problems.append(f"{where}: {row.status} requires a proposed fix")

    if report.summary_total is None:
        problems.append("no summary line found ('Checked N claims: ...')")
    else:
        if report.summary_total != len(report.rows):
            problems.append(
                f"summary says {report.summary_total} claims but ledger has {len(report.rows)} rows"
            )
        actual: dict[str, int] = {}
        for row in report.rows:
            actual[row.status] = actual.get(row.status, 0) + 1
        for status, n in report.summary_counts.items():
            if status in STATUSES and actual.get(status, 0) != n:
                problems.append(
                    f"summary says {n} {status.lower()} but ledger has {actual.get(status, 0)}"
                )
    if report.verdict is None:
        problems.append("no verdict line found ('Verdict: ...')")
    else:
        n_problems = sum(1 for r in report.rows if r.status in PROBLEM_STATUSES)
        checked = any(r.status not in {"UNCHECKED", "SKIPPED"} for r in report.rows)
        v = report.verdict.lower()
        if not checked and not v.startswith("not verified"):
            problems.append("verdict should be 'Not verified' when no claim was checked")
        elif checked and n_problems == 0 and not v.startswith("safe to publish"):
            problems.append("verdict should be 'Safe to publish' when no row is a problem status")
        elif checked and n_problems > 0 and not v.startswith("fix"):
            problems.append(f"verdict should be 'Fix {n_problems} claims before publishing'")

    for marker in report.markers:
        m = re.match(r"\[CN-(\d+)\s+([A-Z]+):", marker)
        if not m:
            continue
        n, status = int(m.group(1)), m.group(2)
        row = next((r for r in report.rows if r.number == n), None)
        if row is None:
            problems.append(f"marker {marker[:40]}... refers to row {n}, which is not in the ledger")
        elif row.status != status:
            problems.append(f"marker for row {n} says {status} but the ledger says {row.status}")
    return problems


def main(argv: list[str]) -> int:
    if len(argv) != 2:
        print(__doc__)
        return 2
    src = argv[1]
    text = sys.stdin.read() if src == "-" else open(src, encoding="utf-8").read()
    report = parse_report(text)
    problems = validate(report)
    if problems:
        for p in problems:
            print(f"FAIL: {p}")
        print(f"{len(problems)} problem(s) in {len(report.rows)} row(s)")
        return 1
    print(f"OK: {len(report.rows)} rows, verdict: {report.verdict}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
