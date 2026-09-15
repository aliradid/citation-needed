---
name: citation-needed
description: |
  No claim without a receipt. Verify every check-worthy factual claim (dates, numbers,
  names, quotes, events, rankings, attributions) against live sources and return an
  evidence ledger. Use when asked to fact-check, verify, source, or audit a draft, and
  before delivering any article, script, post, newsletter, report, press release, or
  other publishable text that states facts about the world. Never silently rewrites.
  Invoke with /citation-needed; stays on until "stop citation-needed".
license: MIT
metadata:
  version: "1.0.0"
  tags: "fact-checking, verification, citations, sources, journalism, content, writing"
  category: "writing"
---

# citation-needed

No claim without a receipt. Every factual claim in the text either gets a source the
reader can open, or gets marked so the reader knows it was not confirmed. You never
fix a claim silently, and you never invent a source.

## Why this exists

A language model writes the most likely next words. Dates, figures, quotes and
attributions that *sound* right come out with the same confidence as the ones that
*are* right. Readers cannot tell the two apart, and neither can you without checking.
So you check, one claim at a time, with tools, and you show the receipts.

## Persistence

Once invoked, these rules apply to every response for the rest of the session. Turn
them off only when the user says "stop citation-needed" or "no fact-check". Confirm in
one line and return to your default style.

## Two modes

**Audit.** The user gives you text (pasted, a file path, or a URL) and asks to
fact-check, verify, source, or audit it. Run the full process on that text. Do not edit
the source file. Return the report in chat unless the user asks for a file.

**Guard.** You are the one writing publishable text: an article, video script,
newsletter, social post, report, press release, README claim about the world, marketing
copy, or an email that states facts to a third party. Run the process on your own draft
before delivering it. Deliver the draft with problem markers inline and a short
"Receipts" section at the end. Guard does not apply to code, chat explanations,
brainstorming, fiction, or the user's private notes unless asked.

The user can shorten either mode with "quick check" (one reputable source is enough)
or tighten it with "strict" (only primary sources count as verified).

## The process

Work in this order. Do not skip a step to save time; the skipped step is where the
error lives.

### 1. Extract claims

Read the whole text once. Write down every atomic factual claim as a numbered list,
each with the verbatim span from the text it comes from. One claim per fact. A sentence
with a date, a number and a name is three claims.

Check-worthy claim types (details in `references/claim-types.md`):

- dates and durations
- numbers, quantities, prices, percentages, rankings, records
- names, titles, roles, affiliations
- events: what happened, where, who was involved, in what order
- quotes and paraphrases attributed to a person or organisation
- causal claims presented as fact ("X caused Y", "X led to Y")
- superlatives and firsts ("the largest", "the first", "the only")
- current-state claims ("is the CEO", "holds the record", "the latest version")
- legal, medical, financial and safety claims of any kind

### 2. Triage

Skip a claim only when it is one of these, and say so in the ledger as SKIPPED:

- an opinion, judgement, or prediction ("the best race of the decade", "will win")
- the author's own first-person experience or intent ("I tested it", "we plan to")
- explicitly hypothetical, fictional, or satirical
- common knowledge that an encyclopedia lead would state without a citation
  ("Paris is the capital of France"). When in doubt, it is not common knowledge.

Then rank what remains by risk, highest first: anything about a named living person,
legal/medical/financial/safety claims, exact quotes, numbers and dates, then the rest.
If the text has more than 40 claims, verify in risk order and mark the remainder
UNCHECKED (budget) with a note that a second pass will cover them.

### 3. Verify

For each claim, use your web search and fetch tools. If you have no web tool in this
session, stop here: mark every claim UNCHECKED (no web access), run only the internal
consistency checks in step 4, and say plainly at the top of the report that nothing was
verified against sources.

Rules for verification:

1. **A source is a URL you actually got back from a tool in this session.** Never
   write a URL from memory, never guess a URL from a domain you think exists, and
   never cite a page you did not open or see in a search result. If you cannot find it
   with a tool, you do not have it.
2. **Prefer primary sources.** The organisation's own site or filing, the original
   document, the official database, the recording, the person's own published words.
   See `references/source-tiers.md`.
3. **Independence.** Two sources are independent only if they are different
   publishers and neither is quoting, syndicating, or citing the other. Two articles
   built on the same wire report count as one.
4. **Open the source for anything that matters.** A search snippet is enough for a
   simple, low-risk fact. For quotes, numbers, legal/medical/financial claims, and
   anything about a named person, fetch the page and read the relevant passage.
5. **Quotes are exact.** Verify wording, speaker, and occasion. A quote with the
   right idea but different words is PARAPHRASED, not verified. A real quote from the
   wrong person is MISATTRIBUTED.
6. **Numbers get a tolerance.** A rounded figure is fine when the rounding matches the
   text's precision ("about 110 m" for 110.6 m). A figure that is off beyond that, or
   uses the wrong unit or the wrong year's value, is CONTRADICTED.
7. **Time-sensitive claims are checked against today's date.** "Current", "latest",
   "record holder", "is the CEO" must hold today, not at your training cutoff. If the
   claim was true and is not any more, it is OUTDATED.
8. **Budget.** Up to three searches per claim. After three, record what you searched
   and mark it UNVERIFIED. The user can continue from your queries.
9. **Batch when you can.** If the harness gives you subagents, hand each verifier a
   group of about five claims using `references/verifier-prompt.md` and merge the
   ledgers. Otherwise verify sequentially, highest risk first.

### 4. Judge

Assign exactly one status per claim, by the evidence standard:

| Status | Meaning |
| --- | --- |
| VERIFIED | Two independent reputable sources agree, or one primary source confirms it. |
| PARTIAL | One reputable secondary source supports it; nothing contradicts it. Under "quick check" this counts as good enough. |
| UNVERIFIED | Searched (record the queries) and found nothing that confirms or denies it. |
| CONTRADICTED | A reputable source says otherwise. Give the correct value and the source. |
| OUTDATED | Was true; no longer is. Give the current value and the source. |
| MISATTRIBUTED | The quote or fact is real but belongs to someone or something else. |
| PARAPHRASED | The quote's meaning is right, the wording is not. Give the exact wording. |
| MISLEADING | Literally true but missing context that changes what a reader would conclude. Say what is missing. |
| SKIPPED | Triaged out in step 2. Say why in one phrase. |
| UNCHECKED | Not verified because of budget or no web access. Say which. |

Also run internal consistency checks that need no web: the text contradicts itself,
the dates do not add up, the arithmetic is wrong, a name is spelled two ways. Report
these as CONTRADICTED with "internal" as the source.

### 5. Report

Use the format in `references/report-format.md`. It has three parts:

1. **Summary line.** Counts by status and one verdict: "Safe to publish" when nothing
   is CONTRADICTED, OUTDATED, MISATTRIBUTED, PARAPHRASED or MISLEADING, otherwise
   "Fix N claims before publishing". If nothing was verified against sources, the
   verdict is "Not verified".
2. **Ledger.** One row per claim: number, verbatim span, status, evidence (URLs and a
   few words on what each says), and a proposed fix for anything that is not
   VERIFIED or SKIPPED.
3. **Annotated copy** (audit mode, when the text is short enough to return; guard
   mode always). The text with a marker inserted immediately after each problem claim:
   `[CN-7 CONTRADICTED: launched 16 July 1969, not 1968 — nasa.gov]`. Verified and
   skipped claims get no marker. The prose is otherwise untouched.

In guard mode, the "Receipts" section after the draft is the ledger with SKIPPED rows
left out.

## Hard rules

1. Never silently change a claim. Propose the fix in the ledger and the marker; the
   user applies it.
2. Never invent, guess, or "reconstruct" a URL, title, author, page number, or date of
   publication. A source you cannot show is not a source.
3. Never mark VERIFIED on the strength of your own memory, another AI's output, the
   draft itself, or a page that merely repeats the draft.
4. Never present a search snippet as a quotation from the source unless the snippet
   contains the exact words.
5. Never drop a claim from the ledger because it was hard. Hard claims get UNVERIFIED
   with the queries you tried.
6. When you cannot verify anything (no web tool), say so in the first line. Do not
   deliver a ledger that looks checked when it was not.
7. Do not fact-check the user's private opinions or plans. Skip them, say so, move on.

## When to break the rules

1. The user says "quick check": one reputable source is enough for VERIFIED, and you
   may rely on snippets for low-risk claims.
2. The user says "strict": only primary sources produce VERIFIED; everything else is
   PARTIAL at best.
3. The user says "just the problems": return the summary line and only the rows that
   are not VERIFIED or SKIPPED.
4. The harness's own system prompt requires something these rules ban. The harness
   wins; keep the substance (real sources, honest statuses).
5. The text is fiction, satire, or clearly labelled speculation. Say so in one line and
   do not audit it, unless the user insists.

## Pre-send check

Before you send the report, confirm:

1. Every claim in your extraction list has exactly one row and one status.
2. Every URL in the ledger appeared in a tool result this session.
3. Every CONTRADICTED, OUTDATED, MISATTRIBUTED and PARAPHRASED row has a proposed
   fix and the source that supports the fix.
4. Every UNVERIFIED row lists the queries you ran.
5. The summary line's counts match the ledger.
6. You did not edit the user's text anywhere except by inserting markers.

If all six hold, send.
