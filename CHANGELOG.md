# Changelog

## [1.0.0] — 2026-09-15

First release.

- Canonical skill with audit and guard modes, claim extraction and triage, the
  two-sources-or-one-primary evidence standard, ten honest statuses, and a fixed
  report format (summary, ledger, annotated copy).
- Reference files: claim types, source tiers, report format, verifier subagent prompt.
- Installers for Claude Code, Codex, Cursor, Gemini CLI, OpenCode, Kimi Code, Qwen Code,
  GitHub Copilot, Zed, and Grok.
- Always-on guard via a flag file (Claude Code hook, OpenCode plugin).
- Deterministic evals: three fixtures with planted errors, `run_evals.py`, and
  `validate_report.py`.
