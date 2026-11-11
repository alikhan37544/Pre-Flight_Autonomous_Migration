# PreFlight deck — independent layman + visual audit, Round 2

**Deck:** <http://127.0.0.1:8091/index.html> — 23 slides
**Auditor:** Independent layman / visual reviewer. No Guidewire, Gosu, APD, CDA, App Events, or PreFlight domain knowledge assumed.
**Date:** 2026-11-11
**Viewports:** 1440 × 900 and 390 × 844, with speaker notes opened on **every** slide.
**Method:** cold read at both viewports; `←`/`→` through all 23 slides; notes toggled with `n` on every slide; clean and notes-open captures; full-page 390 captures; DOM measurements; keyboard/focus checks; resource and console logs; all 23 PDF pages rendered and inspected. No deck, app, fixture, or source file was edited. This report and the screenshots are the only additions.

**Evidence:** [1440 notes](screenshots/slides-layman-2/1440) · [1440 clean](screenshots/slides-layman-2/clean-1440) · [390 notes](screenshots/slides-layman-2/390) · [390 clean](screenshots/slides-layman-2/clean-390) · [390 full-page](screenshots/slides-layman-2/390-full) · [PDF pages](screenshots/slides-layman-2/pdf) · `deck-1440.json`, `deck-390.json`, `console.json`, `requests.json`.

**Scoring calibration:** 10 = a first-time viewer can retell it with no explanation; 7 = clear after one careful read; 5 = needs the speaker/notes; 3 = requires domain knowledge; 0 = unusable. Scores are for the whole deck, not its best slide.

---

## 0. Verdict

**6.5 / 10 — a real improvement over Round 1 (5.8), but still not layman-clean.**

The two Round 1 comprehension blockers are fixed. Slide 18 no longer says Planner compiles; it now says “Planner assembles and seals the codebase plan… nothing is compiled,” and the title is “Cascade 10 and Harbor 11 human gates stay open.” Scribe/Planner is explicitly explained on slides 13 and 17. The Harbor APD/APN contradiction is gone, the 3-vs-4 assumption states are labeled, the mobile and PDF footers carry the full boundary, slide 9's static scroll instruction is gone, and slide 19's patch counts are explicitly non-cumulative.

What remains is a smaller but still material set of comprehension and trust defects:

1. **The deck has two evidence denominators.** Slides 1, 4, 12, and 20 say **126 evidence records/items**; slides 13 and 14 say **101 evidence records**. The 126 is the packet total (101 discovery + 25 review evidence), but the deck never labels the split at the point where 101 appears. This is the single most visible count conflict left.
2. **The gate-level reconciliation is self-contradictory.** Slide 15 says “the 11 gates live at assumption and rule-group level, not package level. Slide 14 shows the only package-level gate, G-03.” G-03 is one of the 3 assumption gates *and* the gate printed on WP-05; the sentence says all gates are not package-level and then says one is. See [detail-15-level](screenshots/slides-layman-2/detail-15-level.png).
3. **The “offline / no external calls” claim is not reconciled with the optional live reasoning run.** Slide 13's fine print cites `mimo-v2.6-flash` making 3 “live” calls, while the title badge says `OFFLINE` and slide 4 says “no external calls.” The deck does not say whether that optional run used a network endpoint. A judge will ask.
4. **Glossary coverage is late and incomplete.** APD and Gosu are defined on slide 13, 11 slides after first use; SARIF is used on slide 17 and defined on slide 18. PCF, typelist, entity, Qusar, GWCP, LOB, IAA, and SME are never defined on a slide; “disposition” is explained only by example. Slide 17 uses Qusar/GWCP with no glossary at all.
5. **Typography and whitespace are still the visual weak points.** The 10.6px floor is better than 10px but still small for projection; slides 9 and 20 leave about a third of the page blank; slides 14, 16, and 19 still use unreadable 5–6px screenshot fragments.

| # | Category | Score | One-line rationale |
|---:|---|---:|---|
| 1 | Narrative arc & section logic | **7** | Strong thesis and section labels; the two-loop story still arrives late and the 101/126 split interrupts it. |
| 2 | Glossary & first-use definitions | **5** | Good per-slide glossaries on 13/18; PCF, typelist, entity, Qusar, GWCP, LOB, IAA, SME are undefined; APD/Gosu arrive 11 slides after first use; SARIF is defined one slide after first use. |
| 3 | Visual hierarchy & whitespace | **5** | Slides 9 and 20 are ~35% empty; 2, 4, 10, 21, 22 also have large dead zones; 13–18 are well filled. |
| 4 | Typography & readability | **5** | 10.5–10.6px table labels dominate slides 3, 14, 15, 20; screenshot text is 4.7–8.7px on 9, 14, 15, 16, 19. |
| 5 | Color & contrast | **9** | Consistent palette; sampled pairs pass AA; status is not color-only. |
| 6 | Charts, tables & data graphics | **6** | Slide 19 non-cumulative fix is good; slide 3 has no dot legend and mixes capability with output type; slide 9 still clips a column; 6/8 and 30/30 labels are ambiguous. |
| 7 | Screenshot quality & evidence legibility | **5** | Slide 10 and 17 are good; 6/7/8 borderline; 14/16/19 are decorative fragments; 390 correctly hides most images. |
| 8 | Consistency & terminology | **6** | Scribe/Planner, 3/4, Harbor, and 10/11 fixed; 126/101, 31 evidence/links, 12 mappings/dispositions, and the two different “11 gates” remain. |
| 9 | Data integrity & count coherence | **6** | Core arithmetic is strong; 101/126 and the G-03 level contradiction are material. |
| 10 | Animation & interaction polish | **9** | Restrained slide-enter and subtle agent pulse; reduced-motion disables all; no autoplay; zero console errors. |
| 11 | Print / PDF handout | **8** | 23 pages, 16:9, tagged, embedded fonts, footer on every page; still has 10px fine print, blank pages, tiny screenshots, and the same 101/G-03 errors. |
| 12 | Mobile 390 & accessibility | **7** | Complete footer, images hidden, resume table stacks, notes readable; matrix/table scroll has no cue, several tables are cramped, code clips, touch targets are 23px high. |

**Overall: 6.5 / 10 (78/120).**
**Layman comprehension: 6.5 / 10.**
**Trust: 7 / 10.**

---

## 1. Round 1 issue status

| Round 1 issue | Status | What I verified |
|---|---|---|
| Slide 18 Planner/compiler contradiction | **Fixed** | Slide 18 now says Planner “assembles and seals the codebase plan”; “nothing is compiled; compile validation is future work.” No “Planner compiles” remains. [detail](screenshots/slides-layman-2/detail-18-title-lede.png) |
| Slide 18 “10/11” ambiguity | **Fixed** | Title is now “Cascade 10 and Harbor 11 human gates stay open.” The run strip separates the two cases. |
| `VehicleRatingQueryQueryService` typo disclosure | **Fixed (disclosed)** | The displayed class is `VehicleRatingQueryService`; the note says the app generator currently produces the doubled name and that the corrected name is shown. The product bug still exists, but the deck no longer hides it. [detail](screenshots/slides-layman-2/detail-18-typo.png) |
| Scribe/Planner mapping | **Fixed** | Slide 13 has a two-column “Feature handoff chain / Codebase cyclic loop” block and a glossary. Slide 17 repeats it. “Same fifth role” is still slightly imprecise, but a viewer can now answer the question. [slide 13](screenshots/slides-layman-2/clean-1440/slide-13.png) |
| 3 vs 4 assumptions labeling | **Fixed** | Slides 8/12 say “Post-decision · 4 assumptions”; slides 13/15 say “Seeded run · 3 assumptions” and explicitly say slides 8/12 are a different state. [slide 15](screenshots/slides-layman-2/clean-1440/slide-15.png) |
| Harbor APD conversion / APN typo | **Fixed** | Harbor badge is “TYPE-LEVEL APD NAMING PREPARATION”; the card says “Not full APD conversion”; the boundary says “not full APD conversion or field mapping.” No `APN` remains. The outcome strip is cropped above the app's program label. [detail](screenshots/slides-layman-2/detail-17-harbor.png) |
| Mobile footer | **Fixed** | At 390 the footer now reads in full: “Synthetic estate · not affiliated with Guidewire · Official Cloud Assurance: not run,” wrapped over two lines. [detail](screenshots/slides-layman-2/detail-390-footer.png) |
| Print/PDF footer | **Fixed** | The PDF has 23 pages; the boundary string is present on all 23 pages, including pages 14–16 and 20. [PDF page 15](screenshots/slides-layman-2/pdf/page-15.png) · [PDF page 20](screenshots/slides-layman-2/pdf/page-20.png) |
| Slide 9 scroll hint | **Fixed** | The static “Scroll horizontally…” instruction is cropped out; the caption now says “8 of the 24 finding rows… full list is in the packet.” The screenshot still clips a `STA` column and leaves a large blank area. [detail](screenshots/slides-layman-2/detail-09-blank.png) |
| Slide 19 non-cumulative patch counts | **Fixed** | The slide now says “Per-scenario exposure — not additive,” with “Cascade has 30 patch-exposures across 22 patches (2+3+7+14+4); Harbor has 28 across 21 (2+3+6+14+3).” [detail](screenshots/slides-layman-2/detail-19-exposure.png) |
| Typography / readability | **Partial** | The floor rose from 10px to 10.6px, but 10.6px is still the dominant size for tables and labels; screenshot text remains below 9px on several slides. |
| Animations | **Pass** | Restrained slide-enter and subtle `agent-pulse`; `prefers-reduced-motion` disables all animation; no autoplay. |
| Glossary | **Partial** | Added 4 terms on slide 13 and 5 on slide 18; not deck-wide, not at first use, and missing the biggest codebase terms. |

---

## 2. First-time viewer answers

### 2.1 Can I explain the product in one sentence?

**Yes.** Slide 1's lede is still the best product sentence: “PreFlight is an offline, evidence-first review of a Guidewire-style policy administration estate. It inventories what exists, links claims to files, records every disposition, and names every unknown — before a migration estimate is signed.”

I can retell the thesis after slide 4: inventory first, evidence links, explicit dispositions, named unknowns, review packet, human approval. That is a strong result.

### 2.2 Can I explain the five agents and Scribe vs Planner?

**Yes, now.** Slide 13 shows Scout → Architect → Guardian → Critic → Scribe, with inputs/outputs. The compare block says the feature path is a straight handoff chain (Scribe seals the review packet) and the codebase path is the cyclic loop (Planner assembles and seals the plan). The glossary on slide 13 defines both. Slide 17 repeats the distinction.

Residual wording: “Same fifth role, different loop” could still be read as “Scribe and Planner are the same role.” The glossary corrects it, but “same fifth slot, different agent” would be clearer.

### 2.3 Can I reconcile the 5 packages / 11 gates / 7 checks / 8 files?

**Mostly, but not completely.**

- 5 packages: WP-01…WP-05 on slide 14; clear.
- 11 gates: 3 assumption gates (G-01…G-03) + 8 rule groups (G-04…G-11); arithmetic is clear on slide 15.
- 7 checks: clear on slide 16.
- 8 bundle files: 5 targets + plan + report + 12-event log; the manifest is the 9th wrapper; clear once read.

The failure is the **level check** on slide 15: “the 11 gates live at assumption and rule-group level, not package level. Slide 14 shows the only package-level gate, G-03.” That sentence says the gates are not package-level and then names a package-level gate. G-03 is one of the 3 assumption gates and is also printed on WP-05; it is not a 12th gate. The current wording creates a contradiction where the slide is trying to remove one. See [detail-15-level](screenshots/slides-layman-2/detail-15-level.png) and [detail-14-g03](screenshots/slides-layman-2/detail-14-g03.png).

### 2.4 Can I tell the Cascade and Harbor stories?

**Yes.** Slide 17 is now the cleanest version of this story: both synthetic, different footprints, 18/22/2/10 vs 20/21/2/11, both `green_with_human_gates`, every patch pending, 13 vs 15 rules fired. The Harbor APD badge and text are consistent, and the outcome strips are no longer cut off. The caption explicitly reconciles the app's “blockers found”/“patches drafted” nouns with the slide's “findings”/“patches.” [slide 17](screenshots/slides-layman-2/clean-1440/slide-17.png)

What I still cannot explain from the slide alone:

- What **Qusar 2026.08** and **GWCP 2027.04** are. The speaker notes define them; the slide does not. [detail-390-qusar](screenshots/slides-layman-2/detail-390-qusar.png)
- What “structural 100 / gate-adjusted 74” means. It looks like a score, but the slide never says out of what, or how a gate reduces 100 to 74.
- Why a 37-character type is a gate if APD's documented limit is 24 characters. The relationship is explained in the fine print on slide 14, but not on slide 17.

### 2.5 Can I tell this is not an actual migration and not official Cloud Assurance?

**Yes, substantially better than Round 1.** The 1440 footer is complete, the 390 footer is complete, and the PDF has the boundary on every page. Slide 13 has the strongest reality-boundary panel; slide 17 has its own; slide 19 labels the release scenario as simulated; slide 23 has the full disclaimer. The print footer is small (10px), but it is present.

Residual: the footer says “Synthetic estate · not affiliated with Guidewire · Official Cloud Assurance: not run.” It does not say “not an actual migration” or “no tenant”; those appear only on slide 13. A print reader on page 15 sees “synthetic” and “not official,” which is probably enough, but “not an actual migration” would be stronger.

### 2.6 Can I understand the code/SARIF slide?

**At the highest level, yes.** The before/after is clear: JDBC + string-concatenated SQL → typed `Query.make(VehicleRating).select().toList()`. The lede now says nothing is compiled, and the SARIF panel explains what SARIF is in two plain sentences. The glossary covers Gosu, APD, CDA, App Events, and SARIF. The typo is disclosed.

What a layman still cannot parse:

- `partialFingerprints.primaryLocationLineHash`, `official_cloud_assurance`, `upload-sarif`, `CR-03` — all in 10.6px, none defined.
- The “app generator currently appends QueryService” disclosure is honest, but “owned by the app team” reads like the deck is passing the bug to someone else. For an independent prototype, that is an odd phrase.
- The “After” code note says “semantic equivalence is gate CR-03”; CR-03 is not defined.

### 2.7 Can I tell the upgrade scenario is simulated?

**Yes.** “5 SIMULATED SCENARIOS,” the dark banner (“simulated release scenario, not a published 2027.04 release”), the table's “APD naming (simulated),” and the footnote all repeat it. The non-cumulative note is now explicit. This is the best-labeled boundary in the deck. [slide 19](screenshots/slides-layman-2/clean-1440/slide-19.png)

Residual: the screenshot caption says “the three recorded resume choices,” but the crop stops at the APD scenario/rework section and does **not** show the three resume choices. The HTML resume table above carries them; the caption and alt are wrong. See [detail-19-shot](screenshots/slides-layman-2/detail-19-shot.png).

### 2.8 Can I state the ask?

**Yes.** Slide 23 is clear: one authorised pilot estate, two blind SME annotators, hard feedback. The closing line is memorable. The repository URL is not clickable, and “SME” is never defined on a slide.

---

## 3. Remaining P0/P1 findings

### P0-1. The deck uses two evidence totals without labeling the difference

**Exact slides:** 1, 4, 12, 20 use **126 evidence records/items**; 13 and 14 use **101 evidence records**.

- Slide 1 packet preview: “Evidence records **126**.”
- Slide 4 run strip: “**126** evidence records.”
- Slide 12: “**126** evidence items = full discovery evidence plus review evidence linked to findings.”
- Slide 20: “**126** complete evidence items + audit appendix.”
- Slide 13 Scout card: “300 files · **101 evidence records** · 31 links on PA-VEH-01…”
- Slide 14 lede and run strip: “300 files and **101 evidence records**.”

The underlying data is not fabricated: `packet.json` counts 126 = 101 discovery evidence + 25 review evidence. The deck explains this only on slide 12, in a 10.6px callout, and never says the 101 on slides 13/14 is the discovery subset. A layman sees two totals for the same review and concludes one is stale. This is exactly the kind of count conflict a judge will catch.

**Evidence:** [126 on slide 1](screenshots/slides-layman-2/detail-01-126.png) · [101 on slide 13](screenshots/slides-layman-2/detail-13-101.png) · [101 on slide 14](screenshots/slides-layman-2/detail-14-101.png) · [combined comparison](screenshots/slides-layman-2/detail-counts-126-vs-101.png).

**Fix (one line, applied consistently):** Use “**126 packet evidence items (101 discovery + 25 review)**” on slides 1/4/12/20, and “**101 discovery evidence records**” on slides 13/14. Or change slides 13/14 to “101 discovery records (126 packet items with review evidence).” Do not use “records” for both without the qualifier.

**Related:** Slide 6 says “31 evidence / 12 files”; slides 13/14 say “31 links on PA-VEH-01.” The 31 is probably the same linked set, but the nouns differ. Use “31 linked evidence records” once and keep it. Slide 11 uses “101/101 links”; slide 13 uses “101 evidence records.” The same number names two different objects (links vs evidence records), which compounds the confusion. See [slide 6](screenshots/slides-layman-2/clean-1440/slide-06.png) and [slide 11 metrics](screenshots/slides-layman-2/detail-11-metrics.png).

### P0-2. The G-03 “package-level gate” sentence contradicts itself

**Exact slides:** 14 and 15.

- Slide 14: WP-05 row says “**G-03** / pending”; the right panel says “WP-05 is the only package carrying a gate at handoff (G-03, 37-character APD type).”
- Slide 15: “**Level check:** the 11 gates live at assumption and rule-group level, not package level. Slide 14 shows the only package-level gate, G-03.”

If the 11 gates live at assumption/rule-group level, then G-03 cannot also be the only package-level gate. In the data, G-03 is the 37-character type assumption gate and is attached to WP-05 at handoff; it is one of the 3 assumption gates, not a separate package-level gate. The current wording is a new contradiction introduced while fixing the old 5-packages-vs-11-gates ambiguity.

**Evidence:** [detail-15-level](screenshots/slides-layman-2/detail-15-level.png) · [detail-14-g03](screenshots/slides-layman-2/detail-14-g03.png).

**Fix:** Change slide 15 to: “The 11 gates are at assumption/rule-group level. G-03 also attaches to WP-05 at handoff; it is one of the 3 assumption gates, not a 12th gate.” Change slide 14 to: “WP-05 is the only package that names its gate at handoff (G-03, one of the 3 assumption gates).” Then the 5/11 relationship is clear and consistent.

### P0-3. “Offline / no external calls” is not reconciled with the optional live reasoning run

**Exact slides:** 1, 4, 10, 13.

- Title badge: `OFFLINE`.
- Slide 4 invariant: “No LLM required — Model off; deterministic retrieval; **no external calls**.”
- Slide 10: “Retrieval-only · model off”; “No LLM, no tools, **no external calls**.”
- Slide 13 fine print: “Optional live reasoning run R-20261111-052740-b001: **mimo-v2.6-flash** made 3 citation-checked calls (Scout, Architect, Critic)…”

The slide says “optional” and “the deterministic 7/7 checks and sealed status are unchanged,” which is honest. But it never says whether that optional run used a network endpoint, and it sits in 10.6px fine print under a deck whose headline says offline. A layman may conclude the deck contradicts itself; a judge may ask whether customer fixture text left the machine. The deck should either remove the optional run from the audience slide (keep it in notes/appendix) or label it explicitly: “optional network-opt-in reasoning run; not used for any count, check, or seal.”

**Evidence:** [slide 13 clean](screenshots/slides-layman-2/clean-1440/slide-13.png) · [slide 4](screenshots/slides-layman-2/clean-1440/slide-04.png).

### P1-1. Glossary covers the easy terms, not the load-bearing ones

**What is defined:** Slide 13 defines Gosu, APD, Scribe, Planner. Slide 18 defines Gosu, APD, CDA, App Events, SARIF.

**What is not defined on a slide:** PCF, entity, typelist, Qusar, GWCP, LOB, IAA, SME, disposition (only explained by example), SBT (it is expanded once on slide 2), TP/FP/FN, Wilson interval, CR-03.

**First-use problem:** APD and Gosu are used on slide 2, defined on slides 13/18 — 11 slides later. PCF and typelist are used on slide 2 and never defined. Qusar/GWCP appear on slide 17 and are defined only in the speaker notes. Slide 19 uses GWCP again. Slide 22 uses LOB/IAA; slide 23 uses SME. The deck assumes a Guidewire-literate reader for the first third, then adds glossaries for the last third.

**Evidence:** [slide 2](screenshots/slides-layman-2/clean-1440/slide-02.png) · [slide 17 Qusar/GWCP](screenshots/slides-layman-2/detail-390-qusar.png) · [slide 22](screenshots/slides-layman-2/clean-1440/slide-22.png).

**Fix:** Add a compact “Terms used in this deck” handout (not necessarily a 24th slide) and a one-line first-use definition for APD, PCF, typelist, entity, disposition, Gosu, Qusar, GWCP, LOB, IAA, SME, TP/FP/FN, Wilson, and CR-03. At minimum add Qusar/GWCP to slide 17 and define LOB/IAA on slide 22 and SME on slide 23.

### P1-2. The evaluation labels are still ambiguous

**Exact slide:** 11.

- “**101/101 M3 LINKS + 30/30 SAMPLE**” — is the denominator 101 or 30? The callout explains “101/101 all links plus a 30/30 stratified sample,” but the headline stat reads like two fractions stacked.
- “**6/6 M5 ISSUES · 6/8 SLOTS**” — this is the most confusing metric. “6/6” sounds complete; “6/8” sounds incomplete. The callout says the allowance is “6 of 8 slots,” a fixed two-decoy top-8, not a learned ranking. A layman still cannot tell whether 6/8 is a pass or a miss.
- “**1.00 M6 F1 · 24 TP / 0 FP / 0 FN**” — TP/FP/FN are never expanded on the slide; “F1” is never defined.

**Evidence:** [detail-11-metrics](screenshots/slides-layman-2/detail-11-metrics.png) · [slide 11 clean](screenshots/slides-layman-2/clean-1440/slide-11.png).

**Fix:** Write the headline as “M3: 101/101 links supported; 30/30 sample re-checked”; “M5: 6/6 relevant issues found within the 8-slot allowance (6 slots used)”; “M6: F1 1.00 — 24 true positives, 0 false positives, 0 false negatives.” Spell out TP/FP/FN and F1 in the caveat. The underlying numbers are fine; the labels are not.

### P1-3. Slide 3's capability matrix still lacks a legend and mixes two semantics

**Exact slide:** 3.

The matrix has full teal dots, half dots, and empty dots, but no legend. The cell labels under “Review packet” are outputs (“findings,” “estimate,” “handover,” “issues,” “6 sections”), not yes/no capability values, so the column mixes “does it produce a review packet?” with “what kind of output is it?” The top chips look like filters but are static tags. A layman can read the row labels but not the scoring logic.

**Evidence:** [slide 3 clean](screenshots/slides-layman-2/clean-1440/slide-03.png) · [390 matrix](screenshots/slides-layman-2/detail-390-matrix.png).

**Fix:** Add `● present · ◐ partial · ○ absent` above the table. Move the output words to a separate “what it produces” note or label the column “Review packet / output” and use a consistent scale. Style the chips as labels, not controls.

### P1-4. Slides 9 and 20 leave a third of the page empty

**Exact slides:** 9, 20 (also 2, 4, 10, 21, 22, but less severe).

- Slide 9: content ends at ~595px; the footer starts at 862px. About 267px (30%) of the slide is blank under the table and callouts. The screenshot still clips the `STA` column and the “Inspect” buttons. [detail-09-blank](screenshots/slides-layman-2/detail-09-blank.png)
- Slide 20: table ends at ~510px, security chips at ~530px; blank to 862px. About 332px (37%) is empty. [detail-20-blank](screenshots/slides-layman-2/detail-20-blank.png)
- Slide 2: left column ends at ~530px; bottom band at ~760px; ~230px dead zone.
- Slide 4: “What each stage writes” rows are separated by 70–80px of white space and have no 01–09 numbers; the bottom half reads like a table with missing rows.
- Slide 10: assistant cards stretch to ~790px; content inside ends at ~635px; ~155px of empty card.
- Slide 21: left panel content ends at ~705px, panel border at ~846px; right column ends at ~670px. Slide 22: right column ends at ~590px, left at ~720px; ~240px blank on the right.

**Fix:** On slide 9, add an HTML “8 of 24” mini-table or a “how to read this” callout in the blank space; on slide 20, add a “what this means for the demo” callout or enlarge the table. On slide 4, number the stage writes 01–09 and reduce the row gaps. On slide 10, add the assistant's actual answer below the screenshot or reduce the card height. On 21/22, use the blank space for a “why this matters” line.

### P1-5. Mobile tables still hide their key columns without a cue

**Exact slides:** 3, 7, 14 (and 15, 21 to a lesser degree).

- Slide 3 at 390: the matrix shows only `TOOL / SERVICE` and a cut `INVENTO…`; the other five columns are off-screen. The region is focusable and has an aria-label, but there is no visible “swipe →” cue. [detail-390-matrix](screenshots/slides-layman-2/detail-390-matrix.png)
- Slide 14 at 390: the package table shows WP, target, and a cut disposition; evidence/bytes/gate are off-screen. WP IDs wrap as “WP-\n01.” No cue. [detail-390-wp](screenshots/slides-layman-2/detail-390-wp.png)
- Slide 7 at 390: the “REASON” column is so narrow that “not parsed as source” wraps one word per line, and “XML parse error, line 1” wraps into four lines. It is readable but looks broken. [detail-390-reason](screenshots/slides-layman-2/detail-390-reason.png)
- Slide 15 at 390: the assumption-gate “Decision needed” column wraps heavily; readable but slow.
- Slide 21 at 390: the prior-art table is 3 narrow columns with 5–6 line cells; readable but slow.

**Fix:** Add a visible “swipe →” label or a fade/chevron to the matrix and package tables; stack slide 7's excluded-file rows as label/value pairs; add `white-space: nowrap` to WP IDs or stack the package table; on slide 15/21, allow the table to scroll or stack rows.

### P1-6. Three screenshots are still decorative, not evidence

**Exact slides:** 14, 16, 19.

- Slide 14: `migrator-scout` shown 674×234 (0.47 scale); UI text ~5–6px. The table above is the content. The caption says the table is built from `migration.json`, not the screenshot. Fine as a texture, but it does not earn the space.
- Slide 16: `migrator-critic` 674×216 and `migrator-scribe` 610×216; UI text ~4.7–6.1px. The screenshots are cropped fragments: the left starts mid-content, the right starts mid-sentence. The HTML tables carry the data.
- Slide 19: `codebase-upgrade` 610×144; UI text ~4.7–5.5px. The crop shows the APD scenario and rework, but not the resume choices the caption claims. [detail-19-shot](screenshots/slides-layman-2/detail-19-shot.png)

Slides 6/7/8 are borderline (0.67 scale, ~7.4–8.7px); slide 9 is ~6.4–7.6px; slide 12 is ~7.6–9.0px. Slide 10 (assistant panels) and slide 17 (outcome strips) are the only screenshots that remain readable at 1440.

**Fix:** Apply the same rule as Round 1: if the UI text will render below ~9px, replace the screenshot with HTML or a focused crop. For slide 19, either crop the actual resume-choice panel or change the caption/alt to “APD scenario and rework; resume choices are in the table.” For slide 16, remove the screenshots or enlarge one to a legible crop. For slide 14, remove the screenshot or make it a single evidence-row crop at 1:1.

### P1-7. Caption/alt text overclaims the visible crop

| Slide | Claim | Reality |
|---:|---|---|
| 15 | Alt: “3 open assumption gates… 8 rule groups… 6 high-impact gates and the **sealed bundle below**.” | The crop stops before the sealed bundle section. The HTML bottom band carries the “open is a status” message, not the seal. |
| 19 | Caption: “Upgrade tab: generation bump, invalidated green signal, and the **three recorded resume choices**.” Alt repeats “revalidate/rollback/defer resume options.” | The crop shows the APD scenario, generation 1→2, rework, and PASS; the three resume choices are below the crop. [detail-19-shot](screenshots/slides-layman-2/detail-19-shot.png) |
| 9 | Caption: “Clean crop below the app's table-scroll hint: 8 of 24…”. | The hint is gone and 8 rows are visible, but the `STA` and `Insp` columns are still clipped. The caption does not mention the clipped column. |
| 12 | Caption: “crop shows A-01, live register has four rows including A-DEC-04.” | Accurate, and clearly disclosed. This one is good. |
| 8 | Caption: “M-12 is below this crop and is shown schematically in panel 4.” | Accurate. This one is good. |
| 17 | Caption: “Outcome strips only… app says blockers found and patches drafted; cards call the same counts findings and patches.” | Accurate; the strips are complete. This one is good. |

**Fix:** Align every caption/alt with what is actually visible. If the screenshot is a fragment, say “fragment” and name the missing panel; do not claim it shows the three resume choices or the sealed bundle.

### P1-8. The two “11 gates” runs are not distinguished enough

**Exact slides:** 13/15 vs 18.

- Slide 13/15: the **feature migrator** for PA-VEH-01 has 11 gates (3 assumptions + 8 rule groups).
- Slide 17/18: **Harbor P&C** in the codebase lab has 11 human gates.

Both are “11 human gates.” A viewer moving from slide 15 to 18 may think the Harbor number is the same 11, especially because slide 18's title uses “Cascade 10 and Harbor 11” and slide 15 already used “11 gates.” The deck distinguishes “feature migrator” and “codebase lab,” but the number collision is real.

**Fix:** On slide 18, write “Harbor P&C (codebase lab): 11 gates” and on slide 15 “PA-VEH-01 (feature review): 11 gates.” A small “different run” label next to both would remove the collision.

### P1-9. “Structural 100 / gate-adjusted 74” is undefined

**Exact slide:** 17 (repeated in the speaker notes).

The cards say “green_with_human_gates · 13 rules fired · **structural 100 / gate-adjusted 74**.” A layman can guess 100 is good, but not what is being scored, why Harbor is 71, or how a gate reduces 100 to 74. The speaker notes say “structural score reads 100/100 for both, but the human-gate-adjusted scores are 74 and 71; the gap is the point,” which is a better explanation — but it is not on the slide.

**Fix:** Add a one-line definition: “Structural = pattern coverage before human review (100 = all mapped); gate-adjusted = structural score after unresolved high-impact gates (Cascade 74, Harbor 71).” Or remove the two numbers if they are not essential to the story.

---

## 4. Twelve category assessments

### 4.1 Narrative arc & section logic — 7/10

The thesis is sharp and consistent: inventory → evidence → dispositions → assumptions → packet → human gate. The section labels in the chrome (Title, The problem, The gap, Solution, Evidence model, Demo 01–14, Engineering rigor, Novelty, Viability, Close) give orientation. Slides 13–20 form a coherent second act; slides 21–23 land the honesty and the ask.

The weakness is the jump from the feature review (slides 5–12) to the five-agent migrator (13–16) to the codebase lab (17–19). The deck does not preview the two-loop structure until slide 13; a first-time viewer spends eight slides in one workflow and then discovers a second one. Round 1 asked for a bridge after slide 4; it is still missing. A single “two loops, one evidence model” line on slide 4 or 12 would help.

### 4.2 Glossary & first-use definitions — 5/10

This is the biggest layman gap after the count conflict. The per-slide glossaries on 13 and 18 are well written, but they are late and partial. APD/Gosu are used on slide 2 and defined on slide 13; PCF/typelist are used on slide 2 and never defined; Qusar/GWCP are used on slide 17 and defined only in the notes; LOB/IAA on slide 22 and SME on slide 23 are never defined on a slide. The glossary cards are 10.6px at the bottom of already-dense slides; a layman may not notice them.

The deck needs a deck-wide glossary handout (or a terms box on slide 3/4) and first-use definitions for the load-bearing terms. The current approach is better than Round 1 but not enough for a cold viewer.

### 4.3 Visual hierarchy & whitespace — 5/10

The grammar is consistent: teal kicker, large headline, gray lede, cards/tables. Slides 13, 15, 16, 17, 18, and 23 use the page well. But slides 9 and 20 leave 30–37% blank, and slides 2, 4, 10, 21, and 22 have visible dead zones. The inconsistency reads as unfinished rather than deliberate. The PDF makes it worse because the blank areas do not reflow.

The worst offenders are slide 9 (blank under the findings table) and slide 20 (blank under the security chips). Both could use a short “what this means” panel without adding new claims.

### 4.4 Typography & readability — 5/10

The 10.6px floor is still too small for projection. Measured at 1440:

| Slide | Visible text nodes ≤10.7px | Notable content |
|---:|---:|---|
| 3 | 78 / 91 | every matrix header, dot label, and tool sub-label |
| 14 | 59 / 76 | every table cell, including target paths and evidence IDs |
| 15 | 73 / 83 | gate tables and stat labels |
| 20 | 43 / 53 | fix table and security chips |
| 19 | 66 / 86 | scenario table and resume table |
| 11 | 38 / 90 | chart labels and caveats |

Body copy is fine (14–16px), and headlines are 37–50px. The problem is the long tail: 10.5–10.6px labels and table cells, plus 4.7–8.7px effective screenshot text on slides 9/14/15/16/19. The deck's own floor is called “projector legibility,” but 10.6px at 1440 is not comfortable on a projector or a phone.

### 4.5 Color & contrast — 9/10

The palette is consistent and purposeful: ink chrome, white paper, teal structure, amber warning, red reality boundary, green success. Sampled pairs:

| Pair | Ratio | Result |
|---|---:|---|
| #5B6B78 on #F6F8FA | 5.17:1 | pass AA |
| #5B6B78 on #FFFFFF | 5.50:1 | pass AA |
| #8A5A12 on #FBF1DF | 5.28:1 | pass AA |
| #8E2F2F on #FAEDEC | 7.08:1 | pass AA |
| #2E6A4E on #EAF4EE | 5.68:1 | pass AA |
| #7F95A3 on #1B2833 | 4.81:1 | pass AA |
| #7D94A2 on #1B2833 | 4.74:1 | pass AA |

Status is not color-only: gates have HIGH/MED text, risk dots have labels, findings have severity text, and the matrix has labels under each dot. The missing dot legend is a chart issue, not a color-contrast issue.

### 4.6 Charts, tables & data graphics — 6/10

- Slide 11's Wilson chart is readable at 1440, and the dot/line legend is clear. The metric labels are the weak point; see P1-2.
- Slide 3's matrix has no dot legend and mixes capability with output type; see P1-3.
- Slide 9's table is still a clipped screenshot: 8 of 24 rows, `STA`/`Insp` cut. The caption now says 8 of 24, which is good, but the visual still looks broken.
- Slide 14/15 tables are clear at 1440 but 10.6px; slide 15's G-03 level line is contradictory.
- Slide 19's non-cumulative exposure note is the best table fix in the deck; the 390 scenario table is cramped but fits, and the resume table stacks correctly.
- Slide 20/21 tables are readable at 1440 but small and sparse; mobile 21 is very slow to read.
- Slide 7's 390 reason column is the worst mobile table: one word per line.

### 4.7 Screenshot quality & evidence legibility — 5/10

The deck finally uses the right asset on slide 17 (outcome strips only) and the right crop on slide 9 (no scroll hint), and slide 10's assistant panels are readable. But the scale problem remains on 14/16/19, and 6/7/8/9/12 are borderline. The 390 breakpoint now hides most screenshots, which is a genuine improvement: no more 3–4px UI text on a phone. The cost is that mobile loses the visual evidence, but the HTML summaries carry the key claims.

The screenshot captions are not always honest about the crop: slide 19 claims the three resume choices, slide 15 claims the sealed bundle. See P1-7.

### 4.8 Consistency & terminology — 6/10

Fixed in Round 2: Scribe/Planner, 3 vs 4 assumptions, Harbor APD/APN, 10/11 title. Those were the big ones.

Remaining:

| Concept | Names | Where | Risk |
|---|---|---|---|
| Evidence total | 126 records/items vs 101 records | 1/4/12/20 vs 13/14 | Looks stale or contradictory. |
| Feature evidence | 31 evidence records vs 31 links | 6 vs 13/14 | Same number, different noun. |
| Links vs records | 101/101 links vs 101 evidence records | 11 vs 13/14 | Same number, different object. |
| Dispositions | 12 dispositions vs 12 mappings | 8/14 vs 12 | Same set, different noun. |
| 11 gates | feature migrator 11 vs Harbor 11 | 13/15 vs 17/18 | Same number, different run. |
| Fifth agent | “same fifth role” for Scribe/Planner | 13/17 | Could imply same agent. |
| Score | “structural 100 / gate-adjusted 74” | 17 | Undefined. |
| Status | `green_with_human_gates`, “green · gated” | 17 | Raw token vs label. |

### 4.9 Data integrity & count coherence — 6/10

The core arithmetic is strong: 300 files, 8 features, 24 findings / 8 rules, 12 dispositions, 5 packages, 3 + 8 = 11 gates, 7 checks, 8 bundle files, 9/11 audit events, 12-event migrator log, 18/22/2/10, 20/21/2/11, 30/28 exposure across 22/21, 16 rule families, 13/15 rules fired, 18/20 SARIF results, 481 tests, 18/18 freeze hashes. I did not find a fabricated or stale count in the core execution claims.

The failures are presentation-level:

1. 126 vs 101 evidence, unlabeled.
2. G-03 “package-level” contradiction.
3. 101 links vs 101 evidence records, unlabeled.
4. 31 evidence vs 31 links.
5. 12 dispositions vs 12 mappings.
6. 6/8 and 30/30 labels.
7. 11 gates collision.
8. `structural` undefined.

### 4.10 Animation & interaction polish — 9/10

Only two animations: a 0.34s slide-enter and a 3s `agent-pulse` on the five agent cards (two iterations, staggered). Both are subtle; the agent pulse is a box-shadow, not a layout shift. `prefers-reduced-motion: reduce` sets all animations/transitions to none. No autoplay, no parallax, no scroll-jacking. The favicon 404 from Round 1 is fixed with a data-URI icon. No console messages on any slide.

### 4.11 Print / PDF handout — 8/10

**Passes:** 23 pages; 1200 × 675.12 pt (16:9); `Tagged: yes`; fonts embedded; all backgrounds present; boundary footer on every page; no page-count mismatch.

**Remaining:**

1. The footer is 10px gray; it is present but easy to miss. It says “Synthetic estate · not affiliated with Guidewire · Official Cloud Assurance: not run,” not “not an actual migration” or “no tenant.”
2. Blank space on pages 2, 4, 9, 10, 20, 21, 22. Page 20 is ~37% empty; page 9 ~30%.
3. Page 9 still has the clipped `STA` column.
4. Pages 16 and 19 still have 5–6px screenshot fragments.
5. Page 1 hides the packet note/quote in print (`.packet-note`/`.packet-quote { display:none }`), leaving the dark panel with a blank bottom; the footer still carries the boundary.
6. Page 23's repository and deck paths are plain text, not links.
7. Page 14/15 carry the 101/G-03 issues.

### 4.12 Mobile 390 & accessibility — 7/10

**Works:** No horizontal page overflow (`document.scrollWidth = 390` on all slides); the footer is complete; images are hidden below 640px except the assistant panels, so the 3–4px screenshot problem is gone; the resume table stacks with `data-label`; notes are full-screen and readable; the page resets scroll to the top on slide change; matrix/code regions are focusable; skip link, focus rings, `inert` notes, and reduced motion all work.

**Fails:** Touch targets at 390 are still 23px high (Notes 43.8×23, Help 37.7×23, PDF 36×23; notes close 28×28). The matrix (slide 3) and package table (slide 14) are horizontally scrollable but have no visible cue. Slide 7's reason column wraps one word per line. Slide 14's WP IDs split “WP-\n01.” Slide 18's “After” code line clips at the right edge; it is focusable/scrollable but has no visible cue. The fixed 58px footer overlays content at the fold (expected for a fixed footer, but it makes the first viewport look cut). The 390 deck is 844–2023px tall per slide; some slides are 2.4 viewports.

---

## 5. Mobile 390 audit

**Overall:** text reflows cleanly; no page-level horizontal overflow; the footer is fixed. The deck is readable as a document, but several tables lose their key columns and the visual evidence is mostly hidden.

**What works:**

- Headlines, ledes, callouts, and section cards reflow.
- The 5-agent cards stack vertically with downward arrows.
- The resume-options table on slide 19 now stacks as “Option / What it does / Status recorded” pairs; the Round 1 broken column is fixed.
- Slide 10's assistant panels are readable (upscaled to 620px from 347px, soft but legible).
- Slide 11 replaces the SVG chart with a readable mobile interval list.
- Slide 17's cards carry the 18/22/2/10 and 20/21/2/11 numbers even without the outcome strip.
- The footer shows the complete boundary.
- Notes are full-screen, 13px, and scrollable.

**What fails:**

1. **Slide 3 matrix:** only `TOOL / SERVICE` and a cut `INVENTO…` are visible; no swipe cue. [detail-390-matrix](screenshots/slides-layman-2/detail-390-matrix.png)
2. **Slide 14 package table:** WP/target/disposition only; evidence/bytes/gate off-screen; WP IDs wrap. [detail-390-wp](screenshots/slides-layman-2/detail-390-wp.png)
3. **Slide 7 reason column:** “not parsed as source” and “XML parse error, line 1” wrap one word per line. [detail-390-reason](screenshots/slides-layman-2/detail-390-reason.png)
4. **Slide 18 code:** the `return Query.make(VehicleRating).select().toList()` line clips at the right edge; no visible scroll cue. [detail-390-code-after](screenshots/slides-layman-2/detail-390-code-after.png)
5. **Slide 6:** the callout still says “click any highlighted evidence-bearing node,” but the spine screenshot is hidden at 390. A mobile reader is told to click something they cannot see.
6. **Touch targets:** 23px high; below the 24×24 minimum and far below 44×44.
7. **Slide 15/21 tables:** readable but very narrow; 5–6 line cells.
8. **Slide 19 scenario table:** cramped headers and cells; readable but slow.

**Mobile verdict:** a real improvement over Round 1 because the unreadable screenshots are gone and the resume table is fixed. Still not a phone-first deck: the comparison tables are the product, and they are exactly what gets clipped.

---

## 6. Print / PDF audit

**Measurements:**

| Check | Result |
|---|---|
| Pages | **23** |
| Page size | **1200 × 675.12 pt** (16:9) |
| Tagged | **yes** |
| Fonts | embedded (Liberation Sans/Mono, DejaVu Sans Mono) |
| Boundary footer | present on **all 23 pages** |
| Page count vs deck | 23 = 23 |
| Console/HTTP needed for PDF | none |

**Page-by-page:**

- **Page 1:** title and packet preview; the packet note/quote are hidden by print CSS, but the footer carries “Official Cloud Assurance: not run.” The dark panel has a blank bottom.
- **Page 2:** clear, but a large blank middle/left zone; the bottom band is pinned low.
- **Page 4:** the 3×3 “What each stage writes” grid has 70–80px vertical gaps and no stage numbers; looks like a table with missing rows.
- **Page 9:** the static scroll hint is gone and the caption says 8 of 24, but the `STA`/`Insp` columns are clipped and ~30% of the page is blank.
- **Page 10:** assistant cards are readable, but ~155px of empty card space under the answers.
- **Page 14/15:** the 101 evidence issue and the G-03 level contradiction are both present.
- **Page 16:** the Critic/Scribe screenshots are 5–6px fragments; the HTML tables carry the content.
- **Page 17:** fixed; the outcome strips are complete; Harbor APD is consistent.
- **Page 18:** fixed; code fits; the title and Planner/compiler wording are correct; glossary is present.
- **Page 19:** non-cumulative note is fixed; the screenshot caption still claims the three resume choices, but the crop does not show them.
- **Page 20:** ~37% blank under the security chips; the boundary footer is present.
- **Page 21:** left panel has ~140px blank inside it; right column ends ~176px above the bottom.
- **Page 22:** right column ends ~240px above the bottom; the left risk panel and roadmap fill more.
- **Page 23:** closing, disclaimer, footer; repository/deck paths are not clickable.

**Print verdict:** a usable handout with a real boundary footer and a tagged PDF — a clear Round 1 improvement. It still carries the deck's count/gate errors and does not reflow its dead zones.

---

## 7. Technical checks

| Check | Result |
|---|---|
| Slides present | 23/23; counter and footer match 01–23 |
| Console messages/errors | **0** (including no favicon 404) |
| Requests | **30**, all `127.0.0.1:8091`; 14 unique images × 2 viewports + 2 documents |
| External requests | **0** |
| Failed requests | **0** |
| Broken images | **0**; all 14 image assets load with natural dimensions |
| 1440 DOM overflow/clipping | **0** among visible slide elements |
| 390 page horizontal overflow | **0**; `document.scrollWidth = 390` on all slides |
| 390 intentional scroll regions | slide 3 matrix, slide 14 package table |
| Code block keyboard access | fixed: slide 18 code blocks have `tabindex="0"` and `role="region"` |
| Matrix keyboard access | fixed: slides 3/14 matrix wrappers are focusable and labelled |
| Reduced motion | `prefers-reduced-motion` sets all animations/transitions to none |
| Touch targets at 390 | Notes 43.8×23, Help 37.7×23, PDF 36×23; notes close 28×28 |
| PDF | 23 pages, 16:9, tagged, embedded fonts, footer all pages |

The deck is fully local. The optional live reasoning run is a separate app feature cited in slide 13's fine print; the deck itself makes no external requests.

---

## 8. Prioritized fixes

### P0 — fix before showing this to a lay audience

| # | Slide(s) | Issue | Fix |
|---:|---|---|---|
| P0-1 | 1, 4, 12, 13, 14, 20 | **126 vs 101 evidence records** with no denominator label. | Use “126 packet evidence items (101 discovery + 25 review)” on 1/4/12/20 and “101 discovery records” on 13/14. Or add a one-line footnote on 13/14: “101 discovery records; 126 packet items with review evidence.” |
| P0-2 | 14, 15 | **G-03 “only package-level gate”** contradicts “the 11 gates live at assumption and rule-group level.” | Change slide 15 to: “The 11 gates are at assumption/rule-group level. G-03 also attaches to WP-05 at handoff; it is one of the 3 assumption gates, not a 12th gate.” Change slide 14 to “WP-05 names its gate at handoff (G-03, one of the 3 assumption gates).” |
| P0-3 | 1, 4, 10, 13 | **“Offline / no external calls”** vs optional live `mimo-v2.6-flash` run. | Remove the optional live run from the audience slide, or label it “optional network-opt-in; not used for any count, check, or seal.” Do not leave it as 10.6px fine print under an `OFFLINE` badge. |

### P1 — high-value comprehension and visual fixes

| # | Slide(s) | Issue | Fix |
|---:|---|---|---|
| P1-1 | 2, 17, 22, 23 | Glossary gaps: PCF, typelist, entity, disposition, Qusar, GWCP, LOB, IAA, SME; APD/Gosu defined 11 slides late. | Add a compact terms handout or a first-use box; add Qusar/GWCP to slide 17, LOB/IAA to 22, SME to 23, PCF/typelist/entity/disposition to 2/3. |
| P1-2 | 11 | M3 30/30, M5 6/8, M6 TP/FP/FN labels are ambiguous. | Rewrite as “101/101 links + 30/30 sample,” “6/6 relevant issues within 8 slots (6 used),” “24 true positives / 0 false positives / 0 false negatives.” Define F1 and Wilson. |
| P1-3 | 3 | Matrix has no dot legend; mixes capability with output type. | Add `● present / ◐ partial / ○ absent`; separate “what it produces” from “does it do this?”; style chips as labels. |
| P1-4 | 9, 20 | ~30–37% blank; slide 9 clips `STA`/`Insp`. | Add an HTML 8-of-24 table or “how to read this” callout; add a “what this means” callout on 20; crop slide 9 before `STA` or widen the image. |
| P1-5 | 3, 7, 14 | 390 tables lose key columns with no cue; slide 7 reason column wraps one word per line; WP IDs split. | Add visible “swipe →” cues; stack slide 7 rows; `white-space: nowrap` on WP or stack the package table. |
| P1-6 | 14, 16, 19 | 5–6px screenshot fragments; slide 19 caption claims resume choices that are not visible. | Replace with HTML or a 1:1 crop; recrop slide 19 to include the resume choices or change the caption/alt to “APD scenario and rework.” |
| P1-7 | 15 | Alt text claims “sealed bundle below” but the crop stops before it. | Change alt to what is visible, or recrop to include the sealed bundle. |
| P1-8 | 13, 15, 17, 18 | Two different “11 gates” runs; “structural 100 / gate-adjusted 74” undefined. | Qualify “PA-VEH-01 feature review: 11 gates” vs “Harbor codebase: 11 gates”; define structural/gate-adjusted in one line on 17. |
| P1-9 | 6, 13, 14 | “31 evidence records” vs “31 links”; 101 links vs 101 evidence records. | Use “31 linked evidence records” and “101/101 links” consistently; add a one-line count legend on 13/14. |
| P1-10 | 2, 4, 10, 21, 22 | Dead zones (slide 2 ~230px; slide 4 70–80px row gaps; slide 10 ~155px empty cards; 21/22 ~140–240px). | Number and tighten slide 4; add a short “so what” panel or enlarge the table; reduce card height or add content. |

### P2 — polish

- Slide 2: cite or name the vendor behind “six to eight weeks”; “vendor estimate” is labeled but unattributed.
- Slide 1: label `2026-11-09` as “run date,” not an unlabeled date.
- Slide 12: say “12 dispositions (also called mappings)” once; the tiny line says “12 mappings.”
- Slide 13/17: change “Same fifth role” to “Same fifth slot, different agent.”
- Slide 18: replace “owned by the app team” with “known generator artifact; not fixed in this build,” and define CR-03.
- Slide 23: make the repository and deck paths clickable, or add a QR code; enlarge the disclaimer from 10.6px.
- PDF: add “not an actual migration / no tenant” to the footer; make the footer 11–12px; reduce blank pages 9/20/21/22; page 1 keep the packet note.
- Mobile: raise top-chrome buttons to ≥44×44 and the notes close button to ≥44×44; add a “screenshot hidden at mobile” note to slide 6 or remove the “click” instruction.
- Slide 15/21: stack the gate/prior-art tables at 390 or add scroll cues.

### First 60 minutes (highest return)

1. Fix the **126/101** label on slides 1/4/12/13/14/20.
2. Fix the **G-03 level check** line on slides 14/15.
3. Fix **M3/M5/M6** labels on slide 11.
4. Add **Qusar/GWCP** definitions to slide 17 and **PCF/typelist** to slide 2/3.
5. Fix the **slide 19 caption/alt** and **slide 15 alt**.
6. Add **swipe cues** to slides 3/14 at 390 and stack slide 7's excluded-file table.

---

## 9. Acceptance tests for the next round

1. A lay viewer can state the evidence total without seeing two numbers: either “126 packet items = 101 discovery + 25 review” or one consistent total on every slide.
2. A viewer can explain G-03 without hearing “package-level gate” and “not package-level” in the same breath.
3. A viewer can say “PA-VEH-01 feature review has 11 gates; Harbor codebase has 11 gates; they are different runs.”
4. A viewer can define APD, PCF, typelist, entity, disposition, Gosu, Qusar, GWCP, LOB, IAA, and SME from the deck or its handout, without the speaker notes.
5. Slide 11's M3/M5/M6 labels are readable as sentences, not fractions: 101/101 links + 30/30 sample; 6/6 relevant issues within 8 slots; 24 TP/0 FP/0 FN with TP/FP/FN spelled out.
6. No caption or alt text claims a crop shows something it does not (slide 19 resume choices; slide 15 sealed bundle).
7. Every 1440 screenshot has effective UI text ≥9px, or is replaced by HTML; no 5–6px evidence fragment remains on 14/16/19.
8. At 390, every horizontally scrollable table has a visible cue; slide 7's reasons are readable; WP IDs do not split; slide 18's code has a visible scroll affordance.
9. Top-chrome controls are at least 24×24 (preferably 44×44), and the notes close button is at least 44×44.
10. The PDF has the boundary footer on every page, is tagged, is 23 pages, and no page has a 30%+ dead zone without a deliberate reason.

---

## 10. What works well

These are real strengths; the fixes should not erase them.

1. **The thesis is sharp.** “Evidence before the estimate” is memorable and consistent from slide 1 to 23.
2. **The deck is honest.** 95% intervals, “not a benchmark,” “no human IAA,” “research prototype,” “not viable as a standalone product,” and the Reversa concession build trust.
3. **Slides 13, 15, and 16 are the clarity core.** The five-agent cards, the 3+8=11 gate arithmetic, and the 7 checks / 8 seals are the best-explained part of the deck.
4. **Slide 17 is now a strong case-study slide.** The two cards, the complete outcome strips, and the Harbor APD correction work.
5. **Slide 18 is now coherent.** The before/after code, the “nothing is compiled” lede, the SARIF explainer, and the glossary make the code lab understandable at a high level.
6. **Slide 19 is the best boundary-labeled slide.** “5 SIMULATED SCENARIOS,” the dark banner, the non-cumulative note, and the resume table are clear.
7. **The visual system is coherent.** Teal/ink/amber/red/green, consistent card grammar, strong headlines, good contrast, no external assets, no distracting animation.
8. **The speaker notes are substantive and candid.** They often contain the clearest version of the caveats; the deck should not depend on them for first-read clarity.
9. **Mobile and print are materially better.** The 390 footer is complete, the PDF footer is on every page and tagged, and the 390 screenshots that would be 3–4px are hidden.
10. **No technical debt in the deck itself.** No console errors, no external requests, no broken images, no favicon 404, reduced-motion support.

---

## 11. Screenshot index

**Full sets**

- 1440 notes open: `screenshots/slides-layman-2/1440/slide-01-notes.png` … `slide-23-notes.png`
- 1440 clean: `screenshots/slides-layman-2/clean-1440/slide-01.png` … `slide-23.png`
- 390 notes open: `screenshots/slides-layman-2/390/slide-01-notes.png` … `slide-23-notes.png`
- 390 clean: `screenshots/slides-layman-2/clean-390/slide-01.png` … `slide-23.png`
- 390 full-page: `screenshots/slides-layman-2/390-full/slide-01-full.png` … `slide-23-full.png`
- PDF pages: `screenshots/slides-layman-2/pdf/page-01.png` … `page-23.png`
- Capture data: `deck-1440.json`, `deck-390.json`, `console.json`, `requests.json`

**Key details**

- [126 on slide 1](screenshots/slides-layman-2/detail-01-126.png)
- [101 on slide 13](screenshots/slides-layman-2/detail-13-101.png)
- [101 on slide 14](screenshots/slides-layman-2/detail-14-101.png)
- [126 vs 101 comparison](screenshots/slides-layman-2/detail-counts-126-vs-101.png)
- [G-03 level check](screenshots/slides-layman-2/detail-15-level.png)
- [G-03 / WP-05](screenshots/slides-layman-2/detail-14-g03.png)
- [Slide 17 Harbor APD fix](screenshots/slides-layman-2/detail-17-harbor.png)
- [Slide 18 title/lede fix](screenshots/slides-layman-2/detail-18-title-lede.png)
- [Slide 18 typo disclosure](screenshots/slides-layman-2/detail-18-typo.png)
- [Slide 19 non-cumulative note](screenshots/slides-layman-2/detail-19-exposure.png)
- [Slide 19 screenshot vs caption](screenshots/slides-layman-2/detail-19-shot.png)
- [Slide 9 blank/clipped](screenshots/slides-layman-2/detail-09-blank.png)
- [Slide 20 blank](screenshots/slides-layman-2/detail-20-blank.png)
- [Slide 11 metrics](screenshots/slides-layman-2/detail-11-metrics.png)
- [390 matrix clipping](screenshots/slides-layman-2/detail-390-matrix.png)
- [390 package table](screenshots/slides-layman-2/detail-390-wp.png)
- [390 reason column](screenshots/slides-layman-2/detail-390-reason.png)
- [390 code clipping](screenshots/slides-layman-2/detail-390-code-after.png)
- [390 Qusar/GWCP undefined](screenshots/slides-layman-2/detail-390-qusar.png)
- [390 footer complete](screenshots/slides-layman-2/detail-390-footer.png)
- [PDF page 9](screenshots/slides-layman-2/pdf/page-09.png)
- [PDF page 15 (footer present)](screenshots/slides-layman-2/pdf/page-15.png)
- [PDF page 17 (fixed)](screenshots/slides-layman-2/pdf/page-17.png)
- [PDF page 20 (blank)](screenshots/slides-layman-2/pdf/page-20.png)
- [PDF page 21 (blank)](screenshots/slides-layman-2/pdf/page-21.png)
- [PDF page 23](screenshots/slides-layman-2/pdf/page-23.png)

**Notes-open evidence**

- [Slide 13 notes, 1440](screenshots/slides-layman-2/1440/slide-13-notes.png)
- [Slide 18 notes, 1440](screenshots/slides-layman-2/1440/slide-18-notes.png)
- [Slide 18 notes, 390](screenshots/slides-layman-2/390/slide-18-notes.png)

---

## 12. Limitations

- I used only the rendered deck, its speaker notes, the PDF, and the deck's own assets/data. I did not audit the app source or verify the hashes/external claims beyond the deck's evidence.
- I tested in headless Chromium (Playwright) at 1440 × 900 and 390 × 844; no iOS Safari, real projector, or touch hardware.
- I did not run a screen-reader session (NVDA/VoiceOver) or a color-blind simulation; accessibility findings are based on DOM/CSS, keyboard/focus tests, touch-target measurements, the PDF metadata, and sampled contrast.
- The 390 full-page captures show the fixed footer at the viewport bottom mid-document. That is a capture artifact, not a layout bug; in the viewport the footer stays pinned.
- At 1440, the notes drawer intentionally overlays the right 400px of the slide. Use the `clean-1440/` set for visual review and the `1440/` set for notes-open evidence.
- Effective screenshot text sizes are approximate, based on the source UI's 11–13px text and the displayed scale; they are directional, not a pixel measurement of each glyph.
- The optional live reasoning run is cited only as the deck presents it. I did not test whether it used a network endpoint; the finding is that the deck does not reconcile it with its offline/no-external-calls framing.
- The deck and app were not edited. The report and screenshots are the only additions.

**One-line summary:** Round 2 fixes the Round 1 comprehension blockers (slide 18, Scribe/Planner, Harbor APD, 3 vs 4, footer, slide 9 hint, non-cumulative counts), but the deck still reads at 6.5/10 for a lay viewer because the two evidence totals (126 vs 101), the G-03 level contradiction, the late glossary, the 10.6px table type, and the empty bottom thirds on slides 9/20 keep it from being self-explanatory and fully trustworthy.
