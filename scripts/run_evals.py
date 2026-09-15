#!/usr/bin/env python3
"""Run and score citation-needed evals.

Fixtures live in evals/fixtures/<name>.md with ground truth in
evals/fixtures/<name>.truth.json:

    {
      "planted": [{"id": "p1", "span": "July 16, 1968", "expected": ["CONTRADICTED"],
                   "note": "launched July 16, 1969"}],
      "true":    [{"span": "July 20, 1969"}],
      "skip":    [{"span": "I have visited", "reason": "first-person"}]
    }

Scoring needs no judge model: we know which claims are wrong, so we measure
whether the agent caught them (recall), whether it wrongly flagged true claims
(false alarms), and whether it left opinions alone (triage).

Subcommands:
    validate                         check fixtures and truth files
    run --runner NAME [options]      run fixtures through an agent CLI and score
    score REPORT.md TRUTH.json       score an existing report
    rescore RESULTS_DIR              re-score saved reports after a scorer change

``run`` reads runner definitions from evals/runners.json (copy
evals/runners.example.json). A runner is a command list; the token {SKILL}
is replaced with the skill body, {PROMPT} with the task prompt, {OUT} with a
file the runner writes its final message to. If {PROMPT} is absent the prompt
is passed on stdin. If {SKILL} is absent the skill body is prepended to the
prompt.
"""

from __future__ import annotations

import argparse
import datetime as dt
import difflib
import json
import os
import re
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
FIXTURES = ROOT / "evals" / "fixtures"
RESULTS = ROOT / "evals" / "results"
SKILL = ROOT / "skills" / "citation-needed" / "SKILL.md"

sys.path.insert(0, str(ROOT / "scripts"))
from validate_report import PROBLEM_STATUSES, Report, parse_report, validate  # noqa: E402

TASK_PROMPT = (
    "Use the citation-needed skill to audit the text between the <text> tags. "
    "You have web search; use it. Return the full report exactly as the skill's "
    "report format specifies: the summary line, the '## Ledger' table with columns "
    "# | Claim | Status | Evidence | Fix, and the '## Annotated copy'. "
    "Put the verbatim span from the text in the Claim column.\n\n<text>\n{text}\n</text>"
)


def _norm(s: str) -> str:
    s = s.lower()
    s = s.replace("’", "'").replace("‘", "'").replace("“", '"').replace("”", '"')
    s = re.sub(r"[–—]", "-", s)
    s = re.sub(r"\s+", " ", s).strip(" \"'.,;:")
    return s


def skill_body() -> str:
    text = SKILL.read_text(encoding="utf-8")
    return re.sub(r"^---[^\S\r\n]*\r?\n[\s\S]*?\r?\n---[^\S\r\n]*(?:\r?\n|$)", "", text).strip()


def load_fixtures(names: list[str] | None = None) -> list[tuple[str, str, dict]]:
    out = []
    for md in sorted(FIXTURES.glob("*.md")):
        name = md.stem
        if names and name not in names:
            continue
        truth = FIXTURES / f"{name}.truth.json"
        if not truth.exists():
            raise SystemExit(f"missing {truth}")
        out.append((name, md.read_text(encoding="utf-8"), json.loads(truth.read_text(encoding="utf-8"))))
    return out


def validate_fixtures() -> list[str]:
    problems = []
    fixtures = load_fixtures()
    if not fixtures:
        problems.append("no fixtures found")
    for name, text, truth in fixtures:
        for key in ("planted", "true", "skip"):
            if key not in truth or not isinstance(truth[key], list):
                problems.append(f"{name}: truth file needs a '{key}' list")
                continue
            for item in truth[key]:
                span = item.get("span", "")
                if not span:
                    problems.append(f"{name}: {key} item without span")
                    continue
                n = text.count(span)
                if n == 0:
                    problems.append(f"{name}: {key} span not found verbatim: {span!r}")
                elif n > 1:
                    problems.append(f"{name}: {key} span appears {n} times, must be unique: {span!r}")
                if key == "planted":
                    exp = item.get("expected", [])
                    if not exp or not set(exp) <= PROBLEM_STATUSES:
                        problems.append(f"{name}: planted {span!r} expected must be a subset of {sorted(PROBLEM_STATUSES)}")
        ids = [p.get("id") for p in truth.get("planted", [])]
        if len(ids) != len(set(ids)):
            problems.append(f"{name}: duplicate planted ids")
    return problems


def match_rows(report: Report, span: str) -> list:
    """Rows whose claim overlaps the span: the claim contains the span, or the span
    contains the claim (min 6 chars). Agents often split one sentence into several
    atomic claims, so a planted error may live in any of them."""
    ns = _norm(span)
    out = []
    for row in report.rows:
        nc = _norm(row.claim)
        if not nc:
            continue
        if ns in nc or (len(nc) >= 6 and nc in ns):
            out.append(row)
            continue
        # Partial overlap: the agent trimmed or extended the span ("his first title
        # came with Ferrari" vs "first title came with Ferrari in 1994").
        m = difflib.SequenceMatcher(None, ns, nc).find_longest_match(0, len(ns), 0, len(nc))
        if m.size >= 10 and m.size >= 0.6 * min(len(ns), len(nc)):
            out.append(row)
    return out


def judge_span(report: Report, span: str):
    """Return (status, row) for a span: a problem status if any overlapping row has
    one, else the status of the row with the largest overlap."""
    rows = match_rows(report, span)
    if not rows:
        return None, None
    for row in rows:
        if row.status in PROBLEM_STATUSES:
            return row.status, row
    ns = _norm(span)
    best = max(rows, key=lambda r: min(len(_norm(r.claim)), len(ns)))
    return best.status, best


def score(report_text: str, truth: dict) -> dict:
    report = parse_report(report_text)
    lint = validate(report)
    planted = truth.get("planted", [])
    trues = truth.get("true", [])
    skips = truth.get("skip", [])

    details = []
    caught = exact = missed_rows = 0
    for p in planted:
        status, row = judge_span(report, p["span"])
        if row is None:
            missed_rows += 1
            details.append(("planted", p["span"], "NOT IN LEDGER", "missed"))
            continue
        if status in PROBLEM_STATUSES:
            caught += 1
            ok = status in p.get("expected", [])
            exact += ok
            details.append(("planted", p["span"], status, "caught" if ok else "caught (different status)"))
        else:
            details.append(("planted", p["span"], status, "missed"))

    false_alarms = 0
    for t in trues:
        status, row = judge_span(report, t["span"])
        st = status if row else "NOT IN LEDGER"
        if row and status in PROBLEM_STATUSES:
            false_alarms += 1
            details.append(("true", t["span"], st, "FALSE ALARM"))
        else:
            details.append(("true", t["span"], st, "ok"))

    skip_violations = 0
    for sk in skips:
        status, row = judge_span(report, sk["span"])
        st = status if row else "NOT IN LEDGER"
        if row and status != "SKIPPED":
            skip_violations += 1
            details.append(("skip", sk["span"], st, "should be SKIPPED"))
        else:
            details.append(("skip", sk["span"], st, "ok"))

    return {
        "rows": len(report.rows),
        "planted_total": len(planted),
        "planted_caught": caught,
        "planted_exact": exact,
        "planted_missing_from_ledger": missed_rows,
        "true_total": len(trues),
        "false_alarms": false_alarms,
        "skip_total": len(skips),
        "skip_violations": skip_violations,
        "lint_problems": lint,
        "verdict": report.verdict,
        "details": details,
    }


def run_runner(runner: dict, prompt: str, timeout: int) -> str:
    cmd = list(runner["command"])
    skill = skill_body()
    if not any("{SKILL}" in c for c in cmd):
        prompt = (
            "Follow this skill exactly for the task that follows it.\n\n"
            "<skill>\n" + skill + "\n</skill>\n\n" + prompt
        )
    out_file = None
    tmpdir = tempfile.mkdtemp(prefix="cn-eval-")
    if any("{OUT}" in c for c in cmd):
        out_file = os.path.join(tmpdir, "last.md")
    cmd = [
        c.replace("{SKILL}", skill).replace("{PROMPT}", prompt).replace("{OUT}", out_file or "")
        for c in cmd
    ]
    stdin_text = None if any("{PROMPT}" in c for c in runner["command"]) else prompt
    proc = subprocess.run(
        cmd, input=stdin_text, capture_output=True, text=True, encoding="utf-8",
        errors="replace", timeout=timeout, cwd=tmpdir,
    )
    if proc.returncode != 0 and not (out_file and os.path.exists(out_file)):
        raise RuntimeError(f"runner exited {proc.returncode}: {proc.stderr[-2000:]}")
    if out_file and os.path.exists(out_file):
        return Path(out_file).read_text(encoding="utf-8", errors="replace")
    text = proc.stdout
    fmt = runner.get("response_format", "text")
    if fmt == "claude-json":
        try:
            data = json.loads(text)
            return data.get("result", text) if isinstance(data, dict) else text
        except json.JSONDecodeError:
            return text
    return text


def fmt_results_md(runner_name: str, results: list[tuple[str, dict]], stamp: str) -> str:
    lines = [
        f"# Eval results — runner `{runner_name}` — {stamp}",
        "",
        "| Fixture | Rows | Planted caught | Exact status | False alarms | Triage misses | Lint |",
        "| --- | --- | --- | --- | --- | --- | --- |",
    ]
    tot = {"pt": 0, "pc": 0, "pe": 0, "tt": 0, "fa": 0, "st": 0, "sv": 0}
    for name, r in results:
        lines.append(
            f"| {name} | {r['rows']} | {r['planted_caught']}/{r['planted_total']} | "
            f"{r['planted_exact']}/{r['planted_total']} | {r['false_alarms']}/{r['true_total']} | "
            f"{r['skip_violations']}/{r['skip_total']} | {len(r['lint_problems'])} |"
        )
        tot["pt"] += r["planted_total"]; tot["pc"] += r["planted_caught"]; tot["pe"] += r["planted_exact"]
        tot["tt"] += r["true_total"]; tot["fa"] += r["false_alarms"]
        tot["st"] += r["skip_total"]; tot["sv"] += r["skip_violations"]
    lines.append(
        f"| **Total** | | **{tot['pc']}/{tot['pt']}** | **{tot['pe']}/{tot['pt']}** | "
        f"**{tot['fa']}/{tot['tt']}** | **{tot['sv']}/{tot['st']}** | |"
    )
    lines += ["", "## Details", ""]
    for name, r in results:
        lines += [f"### {name}", "", f"Verdict: {r['verdict']}", "", "| Kind | Span | Status | Outcome |", "| --- | --- | --- | --- |"]
        for kind, span, st, outcome in r["details"]:
            lines.append(f"| {kind} | {span} | {st} | {outcome} |")
        if r["lint_problems"]:
            groups: dict[str, int] = {}
            for p in r["lint_problems"]:
                key = re.sub(r"^row \d+ \(line \d+\): ", "", p)
                groups[key] = groups.get(key, 0) + 1
            lines += ["", "Lint:", ""] + [f"- {n}× {k}" if n > 1 else f"- {k}" for k, n in groups.items()]
        lines.append("")
    return "\n".join(lines)


def cmd_validate(_args) -> int:
    problems = validate_fixtures()
    for p in problems:
        print(f"FAIL: {p}")
    if not problems:
        print(f"OK: {len(list(FIXTURES.glob('*.md')))} fixtures valid")
    return 1 if problems else 0


def cmd_score(args) -> int:
    r = score(Path(args.report).read_text(encoding="utf-8"), json.loads(Path(args.truth).read_text(encoding="utf-8")))
    print(fmt_results_md("manual", [(Path(args.report).stem, r)], dt.date.today().isoformat()))
    return 0


def cmd_run(args) -> int:
    runners_path = Path(args.runners)
    if not runners_path.exists():
        print(f"no {runners_path}; copy evals/runners.example.json to evals/runners.json and edit it")
        return 2
    runners = json.loads(runners_path.read_text(encoding="utf-8"))
    if args.runner not in runners:
        print(f"unknown runner {args.runner!r}; available: {', '.join(runners)}")
        return 2
    runner = runners[args.runner]
    stamp = dt.datetime.now().strftime("%Y-%m-%d-%H%M")
    out_dir = Path(args.out) / f"{args.runner}-{stamp}"
    out_dir.mkdir(parents=True, exist_ok=True)
    results = []
    for name, text, truth in load_fixtures(args.fixture):
        print(f"[{args.runner}] {name} ...", flush=True)
        try:
            response = run_runner(runner, TASK_PROMPT.format(text=text), args.timeout)
        except Exception as e:  # noqa: BLE001
            print(f"  error: {e}")
            (out_dir / f"{name}.error.txt").write_text(str(e), encoding="utf-8")
            continue
        (out_dir / f"{name}.report.md").write_text(response, encoding="utf-8")
        r = score(response, truth)
        results.append((name, r))
        print(
            f"  caught {r['planted_caught']}/{r['planted_total']}, false alarms {r['false_alarms']}/{r['true_total']}, "
            f"triage misses {r['skip_violations']}/{r['skip_total']}, lint {len(r['lint_problems'])}"
        )
    md = fmt_results_md(args.runner, results, stamp)
    (out_dir / "RESULTS.md").write_text(md, encoding="utf-8")
    print(f"\nwrote {out_dir / 'RESULTS.md'}")
    return 0


def cmd_rescore(args) -> int:
    d = Path(args.dir)
    runner_name = d.name.rsplit("-", 4)[0] if "-" in d.name else d.name
    results = []
    truths = {name: truth for name, _t, truth in load_fixtures()}
    for rep in sorted(d.glob("*.report.md")):
        name = rep.name[: -len(".report.md")]
        if name not in truths:
            print(f"skip {rep.name}: no fixture named {name}")
            continue
        results.append((name, score(rep.read_text(encoding="utf-8"), truths[name])))
    md = fmt_results_md(runner_name, results, d.name)
    (d / "RESULTS.md").write_text(md, encoding="utf-8")
    print(md.split("## Details")[0])
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("validate").set_defaults(fn=cmd_validate)
    s = sub.add_parser("score"); s.add_argument("report"); s.add_argument("truth"); s.set_defaults(fn=cmd_score)
    rs = sub.add_parser("rescore", help="re-score every *.report.md in a results dir and rewrite RESULTS.md")
    rs.add_argument("dir"); rs.set_defaults(fn=cmd_rescore)
    r = sub.add_parser("run")
    r.add_argument("--runner", required=True)
    r.add_argument("--runners", default=str(ROOT / "evals" / "runners.json"))
    r.add_argument("--fixture", action="append", help="fixture name (repeatable); default all")
    r.add_argument("--out", default=str(RESULTS))
    r.add_argument("--timeout", type=int, default=1200)
    r.set_defaults(fn=cmd_run)
    args = ap.parse_args()
    return args.fn(args)


if __name__ == "__main__":
    sys.exit(main())
