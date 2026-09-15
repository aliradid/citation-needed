# Eval results — runner `claude` — claude-2026-09-15-2106

| Fixture | Rows | Planted caught | Exact status | False alarms | Triage misses | Lint |
| --- | --- | --- | --- | --- | --- | --- |
| motorsport-script | 18 | 5/6 | 5/6 | 0/7 | 0/2 | 4 |
| space-explainer | 23 | 5/5 | 5/5 | 0/8 | 0/2 | 1 |
| tech-history | 17 | 5/5 | 5/5 | 0/8 | 0/2 | 5 |
| **Total** | | **15/16** | **15/16** | **0/23** | **0/6** | |

## Details

### motorsport-script

Verdict: Fix 5 claims before publishing

| Kind | Span | Status | Outcome |
| --- | --- | --- | --- |
| planted | One of them did it with a broken neck | UNVERIFIED | missed |
| planted | first title came with Ferrari in 1994 | CONTRADICTED | caught |
| planted | As Niki Lauda put it | MISATTRIBUTED | caught |
| planted | from 2011 to 2014 | CONTRADICTED | caught |
| planted | first championship in 2022 | CONTRADICTED | caught |
| planted | every single year since 1950 | CONTRADICTED | caught |
| true | Michael Schumacher won seven world championships | VERIFIED | ok |
| true | matched that record of seven titles in 2020 | VERIFIED | ok |
| true | Juan Manuel Fangio won five titles in the 1950s | VERIFIED | ok |
| true | died at Imola on May 1, 1994 | VERIFIED | ok |
| true | only team to have competed in every Formula 1 season since 1950 | VERIFIED | ok |
| true | nine world titles across all classes | VERIFIED | ok |
| true | youngest premier-class champion in 2013 | VERIFIED | ok |
| skip | greatest qualifying lap ever driven | SKIPPED | ok |
| skip | will end up with more titles than either of them | SKIPPED | ok |

Lint:

- 3× VERIFIED with one URL and no note that it is a primary source
- SKIPPED needs a reason from ['common knowledge', 'first-person', 'hypothetical', 'opinion', 'prediction']

### space-explainer

Verdict: Fix 5 claims before publishing

| Kind | Span | Status | Outcome |
| --- | --- | --- | --- |
| planted | June 1965 | CONTRADICTED | caught |
| planted | July 16, 1968 | CONTRADICTED | caught |
| planted | one giant leap for humanity | PARAPHRASED | caught |
| planted | third person to walk on the Moon | CONTRADICTED | caught |
| planted | 78 million kilometres | CONTRADICTED | caught |
| true | April 12, 1961 | VERIFIED | ok |
| true | July 20, 1969 | VERIFIED | ok |
| true | Michael Collins stayed in lunar orbit | VERIFIED | ok |
| true | roughly 111 metres tall | VERIFIED | ok |
| true | born in Ohio in 1930 | VERIFIED | ok |
| true | September 5, 1977 | VERIFIED | ok |
| true | Space Shuttle Discovery in April 1990 | VERIFIED | ok |
| true | continuously occupied since November 2000 | VERIFIED | ok |
| skip | I have visited the Kennedy Space Center twice | SKIPPED | ok |
| skip | most impressive engineering project of the twentieth century | SKIPPED | ok |

Lint:

- VERIFIED with one URL and no note that it is a primary source

### tech-history

Verdict: Fix 5 claims before publishing

| Kind | Span | Status | Outcome |
| --- | --- | --- | --- |
| planted | Netscape in 1997 | CONTRADICTED | caught |
| planted | founded in 2010 | CONTRADICTED | caught |
| planted | originally designed at Facebook | CONTRADICTED | caught |
| planted | TypeScript was created by Google | CONTRADICTED | caught |
| planted | Dennis Ritchie famously said | MISATTRIBUTED | caught |
| true | Linux in August 1991 | VERIFIED | ok |
| true | Guido van Rossum | VERIFIED | ok |
| true | Sun Microsystems in 1995 | PARTIAL | ok |
| true | written by Torvalds in 2005 | VERIFIED | ok |
| true | Stack Overflow launched in 2008 | VERIFIED | ok |
| true | January 9, 2007 | VERIFIED | ok |
| true | Docker was released in 2013 | VERIFIED | ok |
| true | Rust 1.0 shipped in May 2015 | VERIFIED | ok |
| skip | most readable language ever designed | SKIPPED | ok |
| skip | will probably replace C in most kernels | SKIPPED | ok |

Lint:

- 5× VERIFIED with one URL and no note that it is a primary source
