# A real report

Unedited output from running the skill on the planted-error fixture
[`evals/fixtures/space-explainer.md`](../evals/fixtures/space-explainer.md), Claude Code with live
web search, 2026-10-15. Every URL below was returned by a search tool in that session.

Scored against the fixture's ground truth: **caught 5/5 planted errors, 0/8 false alarms,
0/2 opinions wrongly checked.** Reproduce it with
`python3 scripts/run_evals.py run --runner claude --fixture space-explainer`.

The report is shown as produced. `scripts/validate_report.py` flags 3 rows (6, 13, 23) as VERIFIED
with a single URL and no primary-source note, a real format miss we keep visible rather than hide.

---

Checked 24 claims: 14 verified, 2 partial, 0 unverified, 4 contradicted, 1 paraphrased, 3 skipped.
Verdict: Fix 5 claims before publishing.

I worked from search results and did not open the full pages. Low-risk facts rest on those results; the numbers and the quote I checked against several results.

## Ledger

| # | Claim | Status | Evidence | Fix |
| --- | --- | --- | --- | --- |
| 1 | "Yuri Gagarin became the first human in space on April 12, 1961" | VERIFIED | https://www.howitworksdaily.com/vostok-1-how-the-first-spacecraft-to-take-humans-into-space-worked/ — Vostok 1 was the first human spaceflight; https://refractor.io/space/april-12-1961-a-remarkable-date-in-human-history/ — April 12, 1961 | |
| 2 | "completing a single orbit aboard Vostok 1" | PARTIAL | https://www.howitworksdaily.com/vostok-1-how-the-first-spacecraft-to-take-humans-into-space-worked/ — search results describe one orbit of about 108 minutes total flight time. I found no second independent source. | |
| 3 | "Valentina Tereshkova followed as the first woman in space" | VERIFIED | https://www.guinnessworldrecords.com/world-records/first-female-in-space — first woman in space, 16 June 1963; https://space.com/21571-valentina-tereshkova.html — first woman in space | |
| 4 | "in June 1965" | CONTRADICTED | https://www.guinnessworldrecords.com/world-records/first-female-in-space — launch 16 June 1963; https://britannica.com/print/article/587896 — Vostok 6 flight is 1963 | June 1963 |
| 5 | "flying solo on Vostok 6" | VERIFIED | https://space.com/21571-valentina-tereshkova.html — she is the only woman to make a solo space journey; https://www.guinnessworldrecords.com/world-records/first-female-in-space — Vostok 6 | |
| 6 | "Eight years after Gagarin" | VERIFIED | https://www.fox29.com/news/apollo-11-launched-50-years-ago-on-july-16-1969 — Apollo 11 launched in 1969, and 1969 − 1961 = 8. The text's own "1968" in claim 8 conflicts with this. | |
| 7 | "Apollo 11 lifted off from Kennedy Space Center" | VERIFIED | https://www.deseret.com/2019/7/16/8937274/apollo-11-astronaut-returns-to-launch-pad-50-years-later/ — liftoff from KSC Launch Complex 39A; https://www.fox29.com/news/apollo-11-launched-50-years-ago-on-july-16-1969 | |
| 8 | "on July 16, 1968" | CONTRADICTED | https://www.fox29.com/news/apollo-11-launched-50-years-ago-on-july-16-1969 — launched July 16, 1969; https://www.deseret.com/2019/7/16/8937274/apollo-11-astronaut-returns-to-launch-pad-50-years-later/ — same date. Also internal: 1961 + 8 = 1969. | July 16, 1969 |
| 9 | "The crew landed on the Moon on July 20, 1969" | VERIFIED | https://www.deseret.com/2019/7/16/8937274/apollo-11-astronaut-returns-to-launch-pad-50-years-later/ — Armstrong and Aldrin landed in Eagle on July 20, 1969; https://dlab.epfl.ch/wikispeedia/wpcd/wp/a/Apollo_11.htm | |
| 10 | "Michael Collins stayed in lunar orbit aboard the command module" | VERIFIED | https://www.deseret.com/2019/7/16/8937274/apollo-11-astronaut-returns-to-launch-pad-50-years-later/ — Collins stayed in lunar orbit tending Columbia; https://www.space.com/16280-buzz-aldrin.html — Collins was command module pilot | |
| 11 | "\"That's one small step for a man, one giant leap for humanity.\"" | PARAPHRASED | https://www.npr.org/sections/thetwo-way/2014/07/20/333196066/45-years-ago-armstrong-took-his-one-small-step — Armstrong's line ends "mankind"; https://www.rmg.co.uk/discover/explore/apollo-11-crew. Armstrong intended "a man" but it was reportedly inaudible. | "That's one small step for [a] man, one giant leap for mankind." |
| 12 | "Buzz Aldrin was the third person to walk on the Moon" | CONTRADICTED | https://www.space.com/16280-buzz-aldrin.html — "the second man on the moon"; https://www.npr.org/sections/thetwo-way/2014/07/20/333196066/45-years-ago-armstrong-took-his-one-small-step — Aldrin became the second man to set foot on the Moon | Buzz Aldrin was the second person to walk on the Moon. |
| 13 | "stood roughly 111 metres tall" | VERIFIED | https://solarsystem.nasa.gov/news/382/10-things-rockets-we-love-saturn-v — NASA gives 363 ft, which is about 110.6 m; the rounding is acceptable | |
| 14 | "Neil Armstrong was born in Ohio in 1930" | VERIFIED | https://www.britannica.com/summary/Neil-Armstrong — born Aug. 5, 1930, Wapakoneta, Ohio; https://www.ohioana.org/anniversary-of-ohios-man-on-the-moon/ | |
| 15 | "I have visited the Kennedy Space Center twice" | SKIPPED | first-person | |
| 16 | "in my view Apollo remains the most impressive engineering project of the twentieth century" | SKIPPED | opinion | |
| 17 | "Robots went further." | SKIPPED | opinion | |
| 18 | "Voyager 1 launched on September 5, 1977" | VERIFIED | https://earthsky.org/space/voyager-1-1-light-day-from-earth-november-17-18-2026/ — launched Sept 5, 1977; https://www.scienceabc.com/nature/universe/farthest-man-made-object-space-probe.html | |
| 19 | "remains the most distant human-made object" | VERIFIED | https://earthsky.org/space/voyager-1-1-light-day-from-earth-november-17-18-2026/ — about 172.6 AU in early 2026, with Voyager 2 second at about 144 AU; https://iflscience.com/its-official-voyager-1-will-cross-the-1-light-day-threshold-on-november-18-2026-82733. Nothing contradicts this as of today. | |
| 20 | "Mars orbits at an average distance of about 78 million kilometres from the Sun" | CONTRADICTED | https://starchild.gsfc.nasa.gov/docs/StarChild/solar_system_level1/mars_facts.html — NASA lists about 228 million km; https://lco.global/spacebook/solar-system/mars/ — 1.524 AU, 2.279×10^8 km | Mars orbits at an average distance of about 228 million kilometres from the Sun. |
| 21 | "which is why the trip there takes months" | PARTIAL | https://space.com/24701-how-long-does-it-take-to-get-to-mars.html — Mars trips take roughly 4 to 11 months. The distance-as-cause link rests on the wrong figure in claim 20, but the corrected distance supports a trip of months. | |
| 22 | "The Hubble Space Telescope was launched aboard Space Shuttle Discovery" | VERIFIED | https://www.nasa.gov/mission/sts-31 — STS-31, Discovery, with Hubble as the primary payload | |
| 23 | "in April 1990" | VERIFIED | https://www.nasa.gov/mission/sts-31 — launch April 24, 1990, with deployment on April 25 | |
| 24 | "the International Space Station has been continuously occupied since November 2000" | VERIFIED | https://www.nasa.gov/?p=419068 — NASA says continuously occupied since November 2000; https://www.nationalgeographic.com/science/2020/10/humans-have-lived-on-international-space-station-20-years-straight — Expedition 1 arrived Nov 2000 | |

## Annotated copy

# Sixty seconds of space history

Yuri Gagarin became the first human in space on April 12, 1961, completing a single orbit aboard Vostok 1. Valentina Tereshkova followed as the first woman in space in June 1965 [CN-4 CONTRADICTED: June 1963 — guinnessworldrecords.com], flying solo on Vostok 6.

Eight years after Gagarin, Apollo 11 lifted off from Kennedy Space Center on July 16, 1968 [CN-8 CONTRADICTED: July 16, 1969 — fox29.com, deseret.com]. The crew landed on the Moon on July 20, 1969, while Michael Collins stayed in lunar orbit aboard the command module. Stepping onto the surface, Neil Armstrong said: "That's one small step for a man, one giant leap for humanity." [CN-11 PARAPHRASED: "That's one small step for [a] man, one giant leap for mankind." — npr.org] Buzz Aldrin was the third person to walk on the Moon [CN-12 CONTRADICTED: second person — space.com]. The Saturn V rocket that carried them stood roughly 111 metres tall.

Neil Armstrong was born in Ohio in 1930. I have visited the Kennedy Space Center twice, and in my view Apollo remains the most impressive engineering project of the twentieth century.

Robots went further. Voyager 1 launched on September 5, 1977 and remains the most distant human-made object. Mars orbits at an average distance of about 78 million kilometres from the Sun [CN-20 CONTRADICTED: about 228 million km — starchild.gsfc.nasa.gov], which is why the trip there takes months. The Hubble Space Telescope was launched aboard Space Shuttle Discovery in April 1990, and the International Space Station has been continuously occupied since November 2000.

Sources:
- [Guinness World Records, first female in space](https://www.guinnessworldrecords.com/world-records/first-female-in-space)
- [Britannica, Valentina Tereshkova](https://britannica.com/print/article/587896)
- [Space.com, Tereshkova](https://space.com/21571-valentina-tereshkova.html)
- [Space.com, Buzz Aldrin](https://www.space.com/16280-buzz-aldrin.html)
- [NPR, 45 years ago Armstrong took his one small step](https://www.npr.org/sections/thetwo-way/2014/07/20/333196066/45-years-ago-armstrong-took-his-one-small-step)
- [Fox29, Apollo 11 launched July 16, 1969](https://www.fox29.com/news/apollo-11-launched-50-years-ago-on-july-16-1969)
- [Deseret News, Apollo 11 astronaut returns to launch pad](https://www.deseret.com/2019/7/16/8937274/apollo-11-astronaut-returns-to-launch-pad-50-years-later/)
- [NASA StarChild, Mars facts](https://starchild.gsfc.nasa.gov/docs/StarChild/solar_system_level1/mars_facts.html)
- [NASA, STS-31](https://www.nasa.gov/mission/sts-31)
- [NASA, Saturn V](https://solarsystem.nasa.gov/news/382/10-things-rockets-we-love-saturn-v)