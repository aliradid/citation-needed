# Contributing

Thanks for helping make AI-written text more honest.

## The one rule

`skills/citation-needed/SKILL.md` is the single source of truth. Every platform
adapter is a thin wrapper around it. Change the skill first, then sync:

```bash
cp skills/citation-needed/SKILL.md .cursor/skills/citation-needed/SKILL.md
```

The condensed prompt in `skills/citation-needed/agents/gemini.toml` is a summary; keep
it consistent when a rule changes.

## Before you open a pull request

```bash
python3 -m unittest discover -s tests -v
python3 scripts/run_evals.py validate
claude plugin validate .        # if you have Claude Code installed
```

If you changed the skill's behaviour, run the evals on at least one runner and paste the
`RESULTS.md` table in the PR:

```bash
cp evals/runners.example.json evals/runners.json
python3 scripts/run_evals.py run --runner claude
```

## What makes a good change

- **A rule that removes a class of wrong verdicts.** Show a fixture where the current
  skill fails and the new rule passes.
- **A new fixture.** See `evals/README.md`. Planted errors must have one unambiguous
  correct answer.
- **A platform fix.** Test on that platform and say which version.

## What we will not merge

- Rules that let the skill mark a claim VERIFIED without a source URL from a tool call.
- Anything that lets the skill rewrite the user's text silently.
- Word lists or heuristics that substitute for actually checking a source.

## Versioning

Bump `metadata.version` in `SKILL.md` and every manifest together (the test suite
checks they match), and add a CHANGELOG entry.

## Conduct

Be direct, be kind, assume good faith. Disagreements about facts are settled with
sources, which is rather the point of the project.
