# Agent guide

Map of this repository for coding agents. It does not replace the skill rules in
`skills/citation-needed/SKILL.md`.

## Start here

1. `README.md` — purpose and user-facing behaviour.
2. `INSTALL.md` — per-platform installation.
3. `skills/citation-needed/SKILL.md` — the canonical skill. Everything else wraps it.
4. `CONTRIBUTING.md` — checks to run before a pull request.

## Repository map

| Area | Location | Purpose |
| --- | --- | --- |
| Canonical skill | `skills/citation-needed/SKILL.md` | Source of truth for behaviour |
| References | `skills/citation-needed/references/` | Claim types, source tiers, report format, verifier prompt |
| Cursor mirror | `.cursor/skills/citation-needed/SKILL.md` | Byte-identical copy; CI checks it |
| Claude Code | `.claude-plugin/`, `hooks/` | Plugin manifest, marketplace, always-on hook |
| Codex | `.codex-plugin/`, `.agents/plugins/`, `skills/citation-needed/agents/openai.yaml` | Plugin and marketplace metadata |
| Gemini CLI | `gemini-extension.json`, `GEMINI.md`, `skills/citation-needed/agents/gemini.toml` | Extension and standalone command |
| OpenCode | `opencode.json`, `.opencode/` | Plugin and command |
| Kimi, Qwen, Grok | `kimi.plugin.json`, `qwen-extension.json`, `plugin.json` | Manifests |
| Evals | `evals/`, `scripts/run_evals.py` | Fixtures with planted errors, deterministic scoring |
| Report linter | `scripts/validate_report.py` | Checks a report against the format |
| Tests | `tests/` | unittest suite |

## Source-of-truth rules

- Change `SKILL.md` first, then copy it to the `.cursor` mirror.
- Keep `metadata.version` in `SKILL.md`, every manifest, and `CHANGELOG.md` aligned.
- Do not add a rule that lets a claim be VERIFIED without a tool-returned URL.

## Verification

```bash
python3 -m unittest discover -s tests -v
python3 scripts/run_evals.py validate
claude plugin validate .
```

Only run commands needed for the task at hand. Do not read secrets or files outside
this repository.
