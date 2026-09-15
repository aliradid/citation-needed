# citation-needed

**No claim without a receipt.**

An agent skill that makes AI-written text checkable. It pulls every factual claim out of
a draft, verifies each one against live sources with the agent's own web tools, and
returns an evidence ledger you can open link by link. It flags what is wrong, in place.
It never rewrites your text behind your back, and it never invents a source.

Works in Claude Code, Codex, Cursor, Gemini CLI, OpenCode, Kimi, Qwen, Copilot, Zed and
Grok. One `SKILL.md`, ten thin installers.

```bash
claude plugin marketplace add aliradid/citation-needed
claude plugin install citation-needed@citation-needed
```

Other harnesses: [INSTALL.md](INSTALL.md).

## The problem

A language model writes the most likely next words. A date that *sounds* right comes out
with the same confidence as one that *is* right. Nothing in the default loop forces the
claim to be checked before it reaches a reader. So agents ship articles with the wrong
year, scripts with a quote attributed to the wrong person, and reports with a figure
that was true in 2019.

## What it does

```
/citation-needed  <paste a draft, or a file path, or a URL>
```

```
Checked 14 claims: 9 verified, 1 partial, 1 unverified, 2 contradicted, 1 skipped.
Verdict: Fix 2 claims before publishing.

## Ledger

| # | Claim | Status | Evidence | Fix |
| --- | --- | --- | --- | --- |
| 1 | "July 16, 1968" | CONTRADICTED | nasa.gov/mission/apollo-11 — launch date July 16, 1969 | July 16, 1969 |
| 2 | "one giant leap for humanity" | PARAPHRASED | nasa.gov/history/... — transcript reads "for mankind" | "one giant leap for mankind" |
| 3 | "first woman in space" | VERIFIED | esa.int/... — Tereshkova, Vostok 6, 1963; britannica.com/... — same | |
| 4 | "the most impressive project of the century" | SKIPPED | opinion | |
| … | | | | |

## Annotated copy

Apollo 11 lifted off on July 16, 1968 [CN-1 CONTRADICTED: July 16, 1969 — nasa.gov] and
landed four days later. Armstrong said it was "one giant leap for humanity"
[CN-2 PARAPHRASED: "for mankind" — nasa.gov].
```

Every URL in the ledger came back from a tool call in that session. If the agent could
not find a source, the row says `UNVERIFIED` and lists the queries it tried, so you can
pick up where it stopped.

## Two modes

**Audit.** Ask it to fact-check, verify, source, or audit any text. You get the report
above. Your file is not touched.

**Guard.** When the agent itself writes an article, script, post, newsletter, report, or
anything else it expects you to publish, it checks its own draft first and delivers it
with problem markers inline and a *Receipts* section at the end. Turn guard on for every
session with a flag file:

```bash
touch ~/.claude/.citation-needed-always     # Claude Code
touch ~/.config/opencode/.citation-needed-always   # OpenCode
```

## The evidence standard

A claim is **VERIFIED** when two independent reputable sources agree, or one primary
source confirms it. One reputable secondary source is **PARTIAL**. Independent means
different publishers, neither quoting the other. Primary means the organisation's own
page, the official record, the original document, the transcript, or the person's own
words. Details in [source-tiers.md](skills/citation-needed/references/source-tiers.md).

| Status | Meaning |
| --- | --- |
| VERIFIED | Two independent reputable sources, or one primary source |
| PARTIAL | One reputable secondary source, nothing against it |
| UNVERIFIED | Searched, found nothing either way; queries listed |
| CONTRADICTED | A reputable source says otherwise; fix proposed |
| OUTDATED | Was true, is not any more; current value proposed |
| MISATTRIBUTED | Real quote or fact, wrong person or thing |
| PARAPHRASED | Right idea, wrong words; exact wording proposed |
| MISLEADING | True but missing context that changes the conclusion |
| SKIPPED | Opinion, prediction, first-person, hypothetical, common knowledge |
| UNCHECKED | Not checked: budget, or no web access in this session |

## Hard rules the skill follows

1. Never change a claim silently. It proposes; you apply.
2. Never write a URL from memory. A source is something a tool returned this session.
3. Never mark VERIFIED from memory, from another AI's output, or from the draft itself.
4. Never present a search snippet as a quotation unless it contains the exact words.
5. Never drop a hard claim from the ledger.
6. If it has no web tool, it says so in the first line and marks everything UNCHECKED.

## Dials

| Say | Effect |
| --- | --- |
| `quick check` | One reputable source is enough; snippets OK for low-risk claims |
| `strict` | Only primary sources count as VERIFIED |
| `just the problems` | Summary line plus only the non-verified rows |
| `stop citation-needed` | Off for the rest of the session |

## Cost

Measured with `claude plugin details`: about 130 tokens added to every session for the
skill's description, and about 2,500 tokens when the skill fires. The always-on hook is
harness-only and adds no model context unless you create the flag file. Verification
itself costs whatever the web searches cost; the skill caps them at three per claim.

## Evals

The repo ships fixtures with planted errors and known-true claims, so scoring is
deterministic: did it catch the wrong ones, did it leave the right ones alone, did it
skip the opinions. No judge model.

```bash
python3 scripts/run_evals.py validate
python3 scripts/run_evals.py run --runner claude
```

Latest results, both Claude Code and Codex with live search: **15/16 planted errors
caught with the exact expected status, 0/23 false alarms on true claims, 0/6 opinions
wrongly checked.** Tables and the one miss explained in [evals/RESULTS.md](evals/RESULTS.md).

`scripts/validate_report.py` lints any report against the format, so you can wire it
into a CI step that fails a content pipeline when the verdict is not "Safe to publish".

## Layout

```
skills/citation-needed/SKILL.md          the skill (source of truth)
skills/citation-needed/references/       claim types, source tiers, report format, verifier prompt
scripts/validate_report.py               report linter
scripts/run_evals.py                     eval runner and scorer
evals/fixtures/                          documents with planted errors + ground truth
hooks/                                   always-on hook for Claude Code
.claude-plugin/ .codex-plugin/ .agents/ .cursor/ .opencode/ gemini-extension.json ...
```

## Why a skill and not a service

The agent already has web search. It already reads pages. What it lacks is the
discipline: extract, triage, verify, judge, show receipts, never fake a source. That is
a few hundred lines of instructions, versioned in git, auditable by anyone, and it runs
wherever your agent runs.

## Contributing

Wrong verdicts are the most useful bug reports. Open a
[wrong-verdict issue](.github/ISSUE_TEMPLATE/wrong-verdict.md) with the claim, what the
skill said, and a source that shows the truth. See [CONTRIBUTING.md](CONTRIBUTING.md).

## License

MIT.
