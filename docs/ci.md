# Block a publish on unverified claims

`scripts/validate_report.py` lints a citation-needed report against the format: valid
statuses, evidence that matches each status, a fix where one is required, and summary
counts that match the ledger. It exits 1 on any problem and needs only Python 3.

```bash
python3 scripts/validate_report.py report.md
python3 scripts/validate_report.py - < report.md
```

## GitHub Actions recipe

Generate the report in a step where your agent has web access, save it as
`report.md`, then lint it and gate on the verdict:

```yaml
- uses: actions/checkout@v4
- uses: actions/setup-python@v5
  with: { python-version: "3.x" }
- name: Report is well formed
  run: python3 scripts/validate_report.py report.md
- name: Block unless safe to publish
  run: grep -q "Verdict: Safe to publish" report.md
```

The linter checks that the report is honest in form. It does not check the facts; the
links in the ledger are for a human to open.
