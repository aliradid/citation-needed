# Evals

The evals measure whether the skill does the one thing it promises: catch wrong claims
without inventing problems in right ones.

## How it works

Each fixture in `fixtures/` is a short, realistic document with a mix of:

- **planted errors** — wrong dates, numbers, attributions and misquotes, with the
  correct value recorded in the `.truth.json` file
- **true claims** — well-established facts that a good checker must not flag
- **skip spans** — opinions, predictions and first-person lines that must be SKIPPED

Because the ground truth is known, scoring is deterministic. No judge model.

| Metric | Meaning |
| --- | --- |
| Planted caught | planted errors whose ledger row has a problem status (CONTRADICTED, OUTDATED, MISATTRIBUTED, PARAPHRASED, MISLEADING) |
| Exact status | planted errors caught with the expected status |
| False alarms | true claims wrongly given a problem status |
| Triage misses | opinion/prediction/first-person spans not marked SKIPPED |
| Lint | report-format problems found by `scripts/validate_report.py` |

## Run

```bash
cp evals/runners.example.json evals/runners.json   # edit models/flags as you like
python3 scripts/run_evals.py validate               # fixtures and truth files are consistent
python3 scripts/run_evals.py run --runner claude    # needs the claude CLI and web access
python3 scripts/run_evals.py run --runner codex     # needs the codex CLI
```

Results land in `results/<runner>-<timestamp>/` with each raw report and a
`RESULTS.md` table. Commit `RESULTS.md` files you want to share; raw reports are
gitignored.

Score a report you produced by hand:

```bash
python3 scripts/run_evals.py score my-report.md evals/fixtures/space-explainer.truth.json
```

## Adding a fixture

1. Write `fixtures/<name>.md`. Keep it under 500 words and make it read like something a
   person would publish.
2. Plant 4 to 6 errors. Each must have a single, unambiguous correct answer that a
   primary or two reputable sources confirm.
3. Add 6 to 8 true claims that are well established and stable.
4. Add 2 or more skip spans.
5. Every `span` must appear exactly once, verbatim, in the fixture. Run
   `python3 scripts/run_evals.py validate`.
