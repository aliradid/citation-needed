# Latest eval results

Run on 2026-09-15 against skill version 1.0.0, from a clean checkout, with live web
search. Scoring is deterministic (see `README.md` in this folder). Raw per-fixture
reports are in the run folders under `results/`.

| Runner | Version | Planted caught | Exact status | False alarms | Triage misses |
| --- | --- | --- | --- | --- | --- |
| Claude Code CLI (`claude -p`, default model) | 2.1.261 | **15/16** | 15/16 | **0/23** | **0/6** |
| Codex CLI (`codex --search exec`, default model) | 0.154.0 | **15/16** | 15/16 | **0/23** | **0/6** |

Per fixture:

| Fixture | Claude caught | Codex caught | False alarms (both) |
| --- | --- | --- | --- |
| motorsport-script | 5/6 | 5/6 | 0/7 |
| space-explainer | 5/5 | 5/5 | 0/8 |
| tech-history | 5/5 | 5/5 | 0/8 |

Full tables: [claude](results/claude-2026-09-15-2106/RESULTS.md),
[codex](results/codex-2026-09-15-2107/RESULTS.md).

## What the miss is

Both runners marked the hook line "One of them did it with a broken neck" UNVERIFIED
after three searches instead of CONTRADICTED. The claim is false (no seven-time
champion won a title with a broken neck; the broken neck belongs to five-time champion
Fangio, Monza 1952), but disproving it means proving a negative. The reader still gets
an inline `[CN-n UNVERIFIED: ...]` marker, which is the honest outcome when no source
speaks either way. An earlier run of the same fixture on Claude did catch it as
MISATTRIBUTED by finding the Fangio story, so it is reachable.

## What the lint column says

Codex cites one URL per VERIFIED claim and does not say when that URL is a primary
source, so the linter flags most of its VERIFIED rows against the two-sources-or-one-
primary rule. Claude cites two sources for most claims. Neither produced a false alarm,
so the looser sourcing did not change any verdict in these fixtures; it does mean a
Codex ledger gives the reader fewer receipts to open.

## Reproduce

```bash
cp evals/runners.example.json evals/runners.json
python3 scripts/run_evals.py run --runner claude
python3 scripts/run_evals.py run --runner codex
```
