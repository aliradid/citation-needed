# Claim types and triage

A claim is any statement a reader could google and call out. This file shows what to
extract, how fine to split, and what to skip.

## Split to atoms

Extract one claim per checkable fact, each with the verbatim span it came from.

Text: "Apollo 11 launched from Kennedy Space Center on July 16, 1969 and landed four
days later with Armstrong and Aldrin aboard the lunar module."

Claims:

1. Apollo 11 launched from Kennedy Space Center — span: "launched from Kennedy Space Center"
2. Apollo 11 launched on July 16, 1969 — span: "July 16, 1969"
3. Apollo 11 landed four days after launch — span: "landed four days later"
4. Armstrong was aboard the lunar module — span: "Armstrong"
5. Aldrin was aboard the lunar module — span: "Aldrin"

Claims 4 and 5 are low risk and can share a search, but they get separate rows so a
reader can see each one was checked.

## Types, with what "verified" needs

| Type | Examples | What confirms it |
| --- | --- | --- |
| Date, duration | "in 1889", "for 27 years", "last Tuesday" | Primary record or two independent sources giving the same date. Watch time zones and local vs UTC for recent events. |
| Number | "111 metres", "$3.2 billion", "42%", "third largest" | The original dataset, filing, or report. Check unit, year, and whether the figure is nominal or adjusted. |
| Name, role, affiliation | "CEO of X", "professor at Y", "born in Z" | The organisation's own page, an official biography, or two independent reputable sources. Roles change; check the date. |
| Event | "won the 2021 title", "the plant closed in March" | Official results, the organisation's announcement, or two independent reports. |
| Quote | "'We never planned to sell,' she said" | The transcript, recording, original interview, or the person's own post. Exact wording, speaker, and occasion. |
| Causal | "the recall caused the stock to fall 8%" | Rarely provable. VERIFIED only if a primary source states the causation; otherwise PARTIAL at best and note that correlation is what the sources show. |
| Superlative, first | "the largest", "the first woman to" | A source that states the superlative explicitly, not one that merely mentions a big number. |
| Current state | "is the record holder", "the latest version is" | A source dated recently enough. If the only source is old, mark OUTDATED risk in the evidence note. |
| Legal, medical, financial, safety | "is illegal in", "reduces risk by", "returns 9% a year" | Primary sources only: statute, regulator, peer-reviewed study, filing. Never a blog. |

## What to skip (SKIPPED, with the reason)

| Skip | Example | Reason to write |
| --- | --- | --- |
| Opinion or judgement | "the greatest driver of his era" | opinion |
| Prediction | "will win next year" | prediction |
| First-person experience or intent | "I drove it for a week", "we will ship in Q3" | first-person |
| Hypothetical, fiction, satire | "imagine a world where" | hypothetical |
| Common knowledge | "water boils at 100 °C at sea level" | common knowledge |

Common knowledge means an encyclopedia lead would state it without a citation. If you
hesitate, it is not common knowledge; check it.

Do not skip a claim because it is hard, because it is probably right, or because
checking it would take three searches. Those are UNVERIFIED or UNCHECKED, never
SKIPPED.

## Risk order

When budget is limited, verify in this order:

1. Anything about a named living person (roles, actions, quotes, wrongdoing)
2. Legal, medical, financial, safety
3. Exact quotes
4. Numbers and dates
5. Events and superlatives
6. Everything else
