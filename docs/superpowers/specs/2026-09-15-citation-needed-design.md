# citation-needed — design

Date: 2026-09-15

## Problem

AI agents write confident prose with invented dates, numbers, quotes and
attributions. Nothing in the agent's default loop forces a claim to be checked
before it is delivered. Existing fact-check skills are either code-only or
tied to one region; existing YouTube/content skill packs contain no
verification step at all.

## Product

`citation-needed` is an agent skill (Claude Code, Codex, Cursor, Gemini CLI,
OpenCode, Kimi, Qwen, Copilot, Zed) with one rule: **no claim without a
receipt**. It extracts every check-worthy factual claim from a text, verifies
each one against live sources with the agent's own web tools, and returns an
evidence ledger. It never silently rewrites the text.

## Decisions (made 2026-09-15)

| Decision | Choice | Why |
| --- | --- | --- |
| Claim scope | Real-world claims only (dates, numbers, names, quotes, events, superlatives, attributions). Not code facts. | One verification path; excellent at one thing. |
| Trigger | Audit mode (on demand) + Guard mode (always-on flag file, and model-invoked when writing publishable content). | Matches the shape of the skills that spread. |
| Unverified claims | Flag in place, never silently fix. Contradicted claims get a proposed correction with a source. | Keeps the human in control. |
| Evidence bar | 2 independent reputable sources, or 1 primary source. 1 secondary source = PARTIAL. | Newsroom standard; easy to explain. |
| Sources | Only URLs returned by a tool call in this session. Never construct a URL from memory. | Kills hallucinated citations. |
| No web access | Report every claim as UNCHECKED with the reason. Never pretend. | Honesty over completeness. |
| Platforms | Full manifests for every platform, all thin wrappers around one canonical `skills/citation-needed/SKILL.md`. | User choice; drift kept cheap by CI sync check. |
| Evals | Fixture documents with planted errors and known-true claims; deterministic scoring (recall of planted errors, false alarms on true claims). No LLM judge needed. | Ground truth is known, so scoring is objective. |
| Name | `citation-needed` | Universally understood; free on GitHub. |

## Components

- `skills/citation-needed/SKILL.md` — canonical behaviour: modes, process,
  claim triage, evidence standard, statuses, report format, rules, overrides.
- `skills/citation-needed/references/` — claim types, source tiers, report
  format with examples, verifier subagent prompt.
- `scripts/validate_report.py` — lints a report (statuses valid, evidence
  present, ledger complete). Used by evals and CI.
- `scripts/run_evals.py` — runs fixtures through a configured agent CLI and
  scores the output against ground truth.
- `evals/fixtures/*.md` + `*.truth.json` — planted-error corpora.
- `hooks/` — SessionStart always-on hook (Node, with POSIX sh fallback).
- Platform manifests: `.claude-plugin/`, `.codex-plugin/`, `.agents/`,
  `.cursor/`, `.opencode/`, `gemini-extension.json`, `GEMINI.md`,
  `kimi.plugin.json`, `qwen-extension.json`.
- `tests/` — unittest: report parsing/scoring, hook parity, manifest and
  mirror consistency.

## Data flow (audit mode)

text → extract claims → triage (skip opinion, first-person, common knowledge)
→ verify each (search → open sources → judge against evidence bar) → ledger
→ report (summary, ledger, annotated copy with markers only on problems).

## Out of scope for v1

Code-fact verification, configurable evidence bars per project, PDF/image
inputs, browser extension, hosted service.
