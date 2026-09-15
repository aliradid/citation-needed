# Report format

Three parts, in this order. Keep the headings exactly as shown so tools can parse the
report.

## 1. Summary line

One line, then the verdict.

```
Checked 12 claims: 8 verified, 1 partial, 1 unverified, 2 contradicted, 0 skipped.
Verdict: Fix 2 claims before publishing.
```

Verdict rules:

- `Safe to publish` when no row is CONTRADICTED, OUTDATED, MISATTRIBUTED, PARAPHRASED,
  or MISLEADING.
- `Fix N claims before publishing` otherwise, where N counts those rows.
- `Not verified` when no claim could be checked against sources (no web access).

## 2. Ledger

(URLs in the examples below are illustrative. In a real report every URL comes from
a tool result in the session.)

A markdown table with exactly these five columns. One row per claim, numbered in the
order the claims appear in the text. The Claim column holds the verbatim span from the
text, in quotes, so a reader can find it with search.

```
## Ledger

| # | Claim | Status | Evidence | Fix |
| --- | --- | --- | --- | --- |
| 1 | "July 16, 1968" | CONTRADICTED | https://www.nasa.gov/mission/apollo-11/ — launch date given as July 16, 1969 | July 16, 1969 |
| 2 | "one giant leap for humanity" | PARAPHRASED | https://www.nasa.gov/history/... — transcript reads "one giant leap for mankind" | "one giant leap for mankind" |
| 3 | "first woman in space" | VERIFIED | https://www.esa.int/... — Tereshkova, Vostok 6, 16 June 1963; https://www.britannica.com/... — same | |
| 4 | "the greatest mission ever flown" | SKIPPED | opinion | |
| 5 | "about 400,000 people worked on Apollo" | UNVERIFIED | searched: "how many people worked on Apollo program", "Apollo program workforce 400,000 NASA" — figures range 300,000 to 400,000, no primary source found | |
```

Evidence column rules:

- Every URL came from a tool result in this session.
- After each URL, a dash and a few words on what the page says about this claim.
- For UNVERIFIED, write `searched:` followed by the queries you ran.
- For SKIPPED, write the reason only: opinion, prediction, first-person, hypothetical,
  common knowledge.
- For UNCHECKED, write `budget` or `no web access`.
- For internal inconsistencies, write `internal —` and the two spans that conflict.

Fix column rules:

- Required for CONTRADICTED, OUTDATED, MISATTRIBUTED, PARAPHRASED, MISLEADING.
- The replacement text, or for MISLEADING the context to add.
- Empty for everything else.

## 3. Annotated copy

Heading `## Annotated copy`, then the text unchanged except for markers inserted
immediately after each problem claim. Format:

```
[CN-<row> <STATUS>: <short reason> — <domain of best source>]
```

Examples:

```
Apollo 11 launched on July 16, 1968 [CN-1 CONTRADICTED: July 16, 1969 — nasa.gov] and
landed four days later.
```

```
Armstrong said it was "one giant leap for humanity" [CN-2 PARAPHRASED: "for mankind" — nasa.gov].
```

Rules:

- Markers only on CONTRADICTED, OUTDATED, MISATTRIBUTED, PARAPHRASED, MISLEADING,
  UNVERIFIED and UNCHECKED rows. VERIFIED, PARTIAL and SKIPPED get no marker.
- Never change the surrounding words, punctuation, or formatting.
- If the text is long (more than about 1,500 words) in audit mode, return only the
  paragraphs that contain markers, each preceded by its paragraph number.

## Guard mode variant

When you wrote the text yourself, deliver it as: the draft with markers, then a
`## Receipts` heading with the ledger minus SKIPPED rows, then the summary line. No
annotated copy section, since the draft already carries the markers.

## "Just the problems" variant

Summary line, then the ledger with only rows that are not VERIFIED, PARTIAL, or
SKIPPED. No annotated copy.
