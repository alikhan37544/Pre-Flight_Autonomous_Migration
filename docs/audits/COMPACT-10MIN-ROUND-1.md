# PreFlight compact 10-minute deck + demo visualization — independent layman + visual audit (Round 1)

**Deck:** <http://127.0.0.1:8092/compact-10min.html> — 12 slides  
**Companion visualization:** <http://127.0.0.1:8092/demo-visual.html>  
**Auditor:** Fresh independent layman / visual reviewer. No prior knowledge of Guidewire, Gosu, APD, CDA, App Events, SARIF, or PreFlight.  
**Date:** 2026-11-11  
**Deck viewports:** 1920 × 1080, 1440 × 900, 1280 × 720, 1024 × 768, 390 × 844  
**Demo viewports:** 1920 × 1080, 1440 × 900, 390 × 844  
**Environment:** Headless Chromium 1254 through Playwright 1.65, DPR 1. Normal and `prefers-reduced-motion: reduce` contexts.  
**Method:** keyboard navigation through all 12 slides (`Home`, `End`, arrows, hash deep links); speaker notes opened with `n` on every slide; clean and notes screenshots; DOM measurements for font sizes, overflow, text bounds, header widths, and target sizes; print/PDF inspection with and without background graphics; network and console capture; current test/CLI verification. No deck, demo, app, or data files were edited. The only additions are this report and its screenshots.

**Evidence:** [screenshots/compact-1](screenshots/compact-1) · [deck metrics](screenshots/compact-1/deck-metrics.json) · [notes metrics](screenshots/compact-1/notes-metrics.json) · [demo metrics](screenshots/compact-1/demo-metrics.json) · [layout measurements](screenshots/compact-1/measure.json) · [PDF with background](screenshots/compact-1/compact-10min-print.pdf) · [PDF without background](screenshots/compact-1/compact-10min-print-nobg.pdf)

**Scoring calibration:** 10 = a first-time viewer can retell it with no explanation; 7 = clear after one careful read; 5 = needs the speaker or notes; 3 = requires domain knowledge or repair; 0 = unusable. Scores are for the whole artifact, not its best slide. I was deliberately harsh. For “would I trust this,” 10 = I would forward it as evidence; 0 = I would not cite it.

---

## 0. Verdict

**6.4 / 10 — a genuinely strong evidence story wrapped in an artifact that is not yet ready for a first-time 10-minute audience.**

The compact cut is a real improvement over the long deck. The thesis is sharp, the gate discipline is unusually clear, the upgrade arithmetic is correct, the evidence card is excellent, and the reality boundary is repeated rather than buried. I could explain PreFlight after slides 1–3 and 11–12 without help.

But the deck fails the “first-time viewer needs no explanation” test in three important places:

1. **The mobile header collapses almost every headline.** At 390 px, the fixed-width badge sits beside the heading, leaving S7’s `h2` **83 px wide and 11 lines tall**. Ten of twelve slides have a squeezed heading; S7’s slide becomes 2,148 px long. This is not clipping, but it is a layout failure.
2. **Slide 9 says the codebase lane is the “same five-agent crew,” but the five boxes are Cascade, Harbor, Rule pack, Critic, Planner.** Only two are agents. The actual codebase loop in the deck’s own S3 note is Scout → Architect → Guardian → Critic → Planner. This is exactly the Scribe/Planner confusion the deck otherwise fixes.
3. **The deck’s own “current” evidence is stale.** S10 says the **current pytest suite is 481 passed**, and its speaker notes warn “Do not say 520-plus unless you re-run.” I re-ran: **520 passed**. The 5.8/10 audit score on the same slide is from the earlier 23-slide deck, not this compact artifact, and is not labelled as such.

The print failure is also material: with background graphics off — the common Chrome PDF default — the dark footer and its repeated “Official Cloud Assurance: not run” boundary become nearly invisible, and the dark S9 visual turns into a white wireframe. The PDF is otherwise well paginated: 12 pages, 16:9, footer on every page.

**Bottom line:** show slides 1–3, 7, 11, and 12 internally today. Do not send the default/no-background PDF, and do not show the mobile deck until the header fix. Fix the P0 items and this becomes a strong 8/10 technical deck.

### What I could explain after one cold pass

- PreFlight is an offline, synthetic review of a Guidewire-style estate that inventories files, links claims to evidence, names unknowns as questions, and keeps every change pending a human.
- The feature path is Scout → Architect → Guardian → Critic → Scribe; the codebase lab is Scout → Architect → Guardian → Critic → Planner.
- The gates stay open: 11 gates, 0 resolved, 0 auto-approved, 0 deployed.
- The upgrade story: a green signal is release-bound; a simulated release change invalidates it; a human chooses revalidate, rollback, or defer.
- The boundary: synthetic estate, no tenant, no compile, not official Cloud Assurance, not an actual migration.

### What I could not explain without the notes

- What `PCF`, `Gosu`, `typelist`, `SARIF`, `APD`, `JMS`, `JDBC`, `CSP`, `CSRF`, `IAA`, or `LOB` mean on first encounter. The glossary is on S11 and covers only five terms.
- Why S9’s bottom “same five-agent crew” contains Cascade, Harbor, Rule pack, Critic, Planner.
- Whether the audit trail has 9, 11, or 12 events, and which number belongs to which chain/state.
- What Planner’s “2 iterations” is meant to convey, and why Critic’s headline number is “0.”
- How the 74/100 and 71/100 human-gate-adjusted scores were computed.
- Why S9 is “one run” when it contains R-DEMO-001 plus two codebase estates.

---

## 1. Scores

| # | Category | Score | Rationale |
|---:|---|---:|---|
| 1 | Product purpose | **8** | “Evidence before the estimate” is clear on S1–S2. A layman still has to infer what a Guidewire “policy estate” is; one sentence would close it. |
| 2 | Five-agent clarity | **6** | S3 and S4 are strong; S9’s “same five-agent crew” is false, and the demo’s codebase Critic/Planner cards obscure the outputs. |
| 3 | Handoff clarity | **6** | “Chain, not loop” and “Scribe vs Planner” work on S3/S4. S9’s labeled “cyclic rework” lane has no loop, and the demo’s feature mode still shows a rework arc. |
| 4 | Gate / human-approval clarity | **9** | The strongest idea in the deck. 11 gates, 0 approved, 0 auto-approved, 0 deployed, “a human decides” are repeated and unambiguous. |
| 5 | Migration-story clarity | **7** | Cascade 18/22/2/10 and Harbor 20/21/2/11 are clear and synthetic. Dense slides, `P&C`/`Qusar` jargon, and S9’s “one run” scope blur the story. |
| 6 | Code-level clarity | **5** | S6 is engineer-grade and honest, but a layman cannot parse Gosu, JDBC, JMS, servlet, SARIF, or `_gen` without the notes. The glossary arrives five slides too late. |
| 7 | Upgrade clarity | **8** | S7 is the best-argued slide: generation invalidation, three human choices, correct non-cumulative exposure. APD is undefined and the chip order is implicit. |
| 8 | Evidence / audit clarity | **7** | S8’s evidence card, excerpt hash, verify commands, and “what the record does not prove” are excellent. The 9/11/12 event counts and the missing open-question example cost it. |
| 9 | Visual hierarchy | **5** | Polished type and color, but S4’s table is stretched into empty space, S5 duplicates its counts in a tiny strip, S9 is half-empty at 1920, and mobile headlines collapse. |
| 10 | Typography / readability | **6** | Good type scale on desktop; 11 px labels everywhere, 14 px body, one- or two-word lines on mobile, and 7 px units in the demo. |
| 11 | Animation / polish | **8** | Restrained slide transitions and agent pulse; reduced motion is respected. The progress bar, demo auto-play, and feature-mode rework arc are the blemishes. |
| 12 | Mobile / print / accessibility | **3** | Mobile headline collapse, footer timing hint below two screens of content, notes focus bug, 22–28 px targets, print footer loss, untagged PDF, 7 px demo text. |
| 13 | 10-minute readiness | **6** | The 600-second plan is exact on paper; the bar contradicts it, S8/S10/S11/S12 require 165–187 wpm, and S12 says “slow down” with only 25 seconds. |
| 14 | Would I trust this | **5** | The evidence model is credible and the verify commands pass; the stale 481, the old 5.8 score, and S9’s false crew label are exactly the kinds of errors this product claims to catch. |

**Overall: 6.4 / 10 unweighted (89/14).** That is a technical-review score, not a first-time-audience score. The evidence/gate story is 8–9; the mobile/print/update-hygiene story is 3–5.

---

## 2. Requested checks

| Check | Result | Evidence |
|---|---|---|
| Clipping / overflow at five viewports | **Pass** | No horizontal overflow; `body.scrollHeight - clientHeight = 0` for every slide at all five viewports; no text outside the slide; print text stays inside each 1600×900 page. Mobile content is scrollable, not clipped. |
| Tiny text | **Fail / partial** | Deck floor is 11 px; S5’s raster strip is ~7–8 px effective at 1024; demo mobile units are **7 px**, details 9.5 px, mode labels 7.5 px. |
| Stale counts | **Fail** | S10 says **481** current; current `pytest` is **520 passed**. S10’s 5.8/10 is from the 23-slide deck. See P0-1. |
| Contradictions | **Fail** | S9’s “same five-agent crew”; demo feature mode’s rework arc under “Straight handoff”; S8’s 9/11/12 event numbers; S4’s 11 gates / 11 audit events; footer bar vs elapsed clock. |
| Scribe / Planner confusion | **Partial** | S3/S4 explain the distinction correctly; S9 re-confuses it; demo’s Planner card says “2 iterations” while the narration says “seals 2 plans.” |
| “10/11” ambiguity | **Pass literal / partial residual** | No literal `10/11` in the compact deck. S5 clearly labels Cascade 10 and Harbor 11. S9’s footer says “11 open gates” while the same view contains Cascade 10 + Harbor 11 with no scope label. |
| APN typo | **Pass** | Zero occurrences of `APN` in the compact deck. The old defect is gone. |
| APD conversion overclaim | **Pass, with visibility caveat** | S5 says “APD deliverable is type-level naming preparation only — not full APD conversion or field mapping.” The disclaimer is correct but buried in 14 px body text. |
| CDA wording | **Pass** | S11: “Cloud Data Access: S3 Parquet export/streaming; not a synchronous read.” Accurate and precise. |
| Non-cumulative patch counts | **Pass arithmetic / partial labels** | 2+3+7+14+4 = 30 Cascade exposures across 22 patches; 2+3+6+14+3 = 28 Harbor exposures across 21. The strip says “never sum the rows.” The per-chip 7/6 and 4/3 order is not labelled Cascade/Harbor. |
| Missing reality boundary | **Deck pass / demo partial** | Deck repeats “Official Cloud Assurance: not run” in every footer and on S1/S9/S11/S12. Demo desktop footer has “not affiliated with Guidewire”; at 390 the footer boundary, `Synthetic` meta, and brand sub are hidden, and the reality card does not include non-affiliation. Print without background loses the boundary. |
| Footer / PDF issues | **Partial** | 12 pages, 1200×675.12 pt, footer and page numbers repeated; no text clipping. With background off the footer is faint, S9 loses its dark canvas, and S4’s table rows are stretched. PDF is untagged. |
| Broken links | **Pass** | Only content link is S9’s “Open full visualization”; it resolves to the local demo. Deep link `#slide-7` and skip link work. No 404s. Repo/deck paths on S12 are plain text, not links. |
| External requests | **Pass** | One local HTML request per page; zero external fonts, scripts, styles, images, or CDNs. The only image is inline base64; the favicon is a data URI. |
| Console errors | **Pass** | 0 console messages and 0 page errors across all deck and demo runs. |
| 10-minute timing hint | **Partial** | Every note has a `Timing:` cue; all 12 ranges match `data-start`/`data-end`; total exactly 600 s. Pacing and the progress bar are the problems. |
| Progress bar | **Fail** | S1 says `00:00 elapsed · 10:00 left` with a **5.83%** bar; S12 says `09:35 elapsed · 00:25 left` with a **100%** bar. The bar uses each slide’s end time, not elapsed. |
| Notes on every slide | **Pass content / fail focus** | 12/12 notes present; 0 overflow at 1440 and 390; timing hints present. After `n`, focus remains on `BODY`/`notes-toggle` in 12/12 runs — not the notes panel. |
| Play / pause / step / reset | **Pass** | All four work; Step disables at 6; Play becomes Replay; Reset returns to 0. Keyboard arrows work. Demo auto-plays on load, which is a separate UX issue. |
| Feature / codebase toggle | **Pass mechanics / partial clarity** | Toggle updates kicker, agents, counts, lane copy, pips, and rework label. Codebase cards’ Critic/Planner hierarchy is unclear; mobile hides Planner’s Harbor foot. |
| Reduced motion | **Pass** | Demo loads at step 6 with `1e-06s` animation/transition durations and no auto-play. Deck CSS also disables animation/transitions. |
| PDF pagination | **Pass** | 12 pages; 16:9 page size; one slide per page; footer repeated; no text outside the page. |

---

## 3. What passed cleanly

These are not small wins; they are the reason the deck is worth fixing.

- **Keyboard navigation works:** `Home`, `End`, ArrowLeft/ArrowRight, and hash deep links all update the active slide, footer, section label, and page count. At 390, changing slides resets scroll to the top of the slide.
- **Speaker notes are complete:** every slide has notes; all 12 notes fit without scrolling at 1440 and 390; the timing ranges sum to exactly 600 seconds.
- **No clipping or horizontal overflow:** at 1920, 1440, 1280, 1024, and 390, no slide’s content exceeds the slide box; no text is cut; no horizontal scrollbar. The mobile problem is a narrow column, not lost content.
- **No external calls, no console errors:** the deck and demo each make one local document request. The deck’s “offline by construction” claim is true in the browser.
- **The demo fits its three viewports:** 1920×1080, 1440×900, and 390×844 all have `scrollHeight == innerHeight`; at 390 the controls remain visible at the bottom. The issue is text size, not overflow.
- **The evidence commands work:** `preflight verify-audit R-DEMO-001` → `OK (9 events, head e832da05dd9fac2e)`; `verify-packet` → `OK`; `verify-migration` → `OK - 12 events verified`.
- **The counts mostly reconcile:** 300 files, 101 evidence, 31 links, 24 findings, 12 dispositions, 5 packages, 5 targets, 11 gates (3 + 8), 6 high, 7/7 checks, 8 sealed files, 12-event migration log, 0 auto-approved, 0 deployed. The freeze manifest has 18/18 recorded hashes recomputing, and M3 is 101/101 evidence links.
- **The compact-deck fixes held:** no `APN` typo; no `10/11`; APD conversion explicitly disclaimed; CDA correctly described as streaming/export; non-cumulative exposure arithmetic correct; reality boundary repeated.
- **Reduced motion works:** demo final state, no auto-play, 1e-06s transitions; deck CSS disables animation/transitions.
- **PDF with background graphics on is structurally sound:** 12 pages, 16:9, footer on every page, page numbers correct, no clipping.

---

## 4. P0 — fix before showing this to a first-time audience

### P0-1. S10’s “current” pytest count is stale — 481 vs 520 — and the 5.8/10 is from the old 23-slide deck

**Observed.** S10’s first stat card reads:

> `current pytest suite`  
> `481 PASSED AT THIS SNAPSHOT · 2026-11-11`

The S10 speaker note says:

> “The current pytest suite has 481 passing tests at this snapshot. **Do not say 520-plus unless you re-run and get that number.**”

I re-ran the current suite:

```text
.venv/bin/python -m pytest -o addopts=""
...
================== 520 passed, 1 warning in 92.38s (0:01:32) ===================
```

The same stale number appears in `README.md` (badge and table) and `docs/VERIFICATION.md`. S10 also says:

> “Independent layman + visual audit, round 1: 5.8/10”

The 5.8/10 is the overall score in `docs/audits/SLIDES-LAYMAN-ROUND-1.md`, which audited the **23-slide** deck. The compact 12-slide cut is a different artifact. The slide does not say that.

**Why it matters.** The deck’s whole thesis is “every claim has evidence.” A checkable, explicitly “current” number that is 39 tests stale is the worst possible error for this deck. Worse, the speaker note tells the presenter not to say the correct number. The old audit score also reads as a current quality claim for an artifact it did not score.

**Fix.** Replace 481 with the current count, preferably generated from the test run at build time. Update the note, README badge, and `VERIFICATION.md` together. Add the commit hash and date. Either remove the 5.8/10 or label it “prior 23-slide deck audit; this compact cut is Round 1.” Do not show an audit score you are not re-scoring.

**Evidence.** [S10 stat card](screenshots/compact-1/detail-10-pytest-stat.png) · [S10 notes](screenshots/compact-1/detail-10-note-520.png) · [S10 full](screenshots/compact-1/deck-1440x900-slide-10.png) · [S10 notes full](screenshots/compact-1/notes-1440x900-slide-10.png)

![S10 current pytest stat](screenshots/compact-1/detail-10-pytest-stat.png)

![S10 note warns against the correct current count](screenshots/compact-1/detail-10-note-520.png)

---

### P0-2. At 390, the fixed header badge squeezes every headline into an 83–260 px column

**Observed.** At 390 × 844, `.slide-head` stays a flex row. The badge is `flex: none` and consumes 164–265 px of the 358 px content width; the `h2` and lede get the remainder.

Measured `h2` widths and line counts at 390:

| Slide | `h2` width | Lines | Badge width |
|---|---:|---:|---:|
| S7 Upgrade resilience | **83 px** | **11** | 265 px |
| S5 Codebase lab | **89 px** | **7** | 259 px |
| S4 Feature demo | **156 px** | **8** | 192 px |
| S2 The problem | **173 px** | **5** | 175 px |
| S6 Code-level refactor | **158 px** | **5** | 190 px |
| S8 Evidence & audit | **172 px** | **6** | 176 px |
| S10 Engineering rigor | **174 px** | **4** | 174 px |
| S11 Reality boundary | **184 px** | **5** | 164 px |
| S3 Five-agent handoff | **260 px** | **3** | 88 px |

S1 and S12 have no badge and use the full 358 px.

S7’s headline becomes:

> A  
> green  
> signal  
> is  
> release-  
> bound.  
> Revalidate,  
> roll  
> back,  
> or  
> defer.

The lede is squeezed into the same column; S7’s full page is **2,148 px tall**. S5 is 1,725 px; S4 1,863 px; S11 1,818 px. The deck is readable only by scrolling, and the 10-minute timing hint at the footer is not visible while reading the top of a long slide.

**Why it matters.** This is the single largest visual failure. It affects ten of twelve slides, makes the first-time mobile experience look broken, and turns a slide deck into a long narrow document. It is not clipping — all text is present — but the reading experience is unacceptable for a presentation.

**Fix.** At `@media (max-width: 900px)`, stack the head:

```css
.slide-head { flex-direction: column; align-items: flex-start; gap: 8px; }
.slide-head-main { width: 100%; }
.head-badge { align-self: flex-start; }
h2 { max-width: none; }
.lede { max-width: none; }
```

Then re-test S7 and S5 at 390: the `h2` should be ~358 px wide, not 83–89 px. Consider moving the badge above the kicker or below the lede, not beside the headline. This will also reduce the 2,148 px slide height and bring the footer timing hint closer.

**Evidence.** [S7 mobile headline](screenshots/compact-1/detail-07-mobile-headline.png) · [S5 mobile headline](screenshots/compact-1/detail-05-mobile-headline.png) · [S7 full](screenshots/compact-1/deck-390x844-slide-07.png) · [S5 full](screenshots/compact-1/deck-390x844-slide-05.png)

![S7 at 390: 83 px headline column, 11 lines](screenshots/compact-1/detail-07-mobile-headline.png)

---

### P0-3. Print without background graphics loses the footer boundary and the S9 dark visual

**Observed.** The PDF is 12 pages at 1200 × 675.12 pt (16:9), with the footer repeated on every page. With background graphics on, the footer is dark and readable; with background graphics off — the default in many Chrome “Save as PDF” flows — the footer becomes pale text on white, the progress bar disappears, and S9’s dark full-bleed visual turns into a white wireframe.

The CSS has no `print-color-adjust`:

```text
grep -n "print-color-adjust" docs/presentation/compact-10min.html
→ none
```

Page 1 without background: `PreFlight · synthetic rehearsal`, `Official Cloud Assurance: not run`, the clock, and `01 / 12` are all faint. S9 without background loses the dark canvas, node fills, purple codebase lane, amber authority band, and the visual hierarchy that makes the recap work. The footer boundary is the deck’s repeated trust statement; it must survive print.

**Why it matters.** A PDF handout is the version most likely to be forwarded without the presenter. If the boundary disappears, the handout can be read as a real migration review. The S9 dark visual is also the visual recap; without its background it is a wireframe.

**Fix.** Add an exact print-color rule and test the failure mode:

```css
@media print {
  *, *::before, *::after {
    -webkit-print-color-adjust: exact;
    print-color-adjust: exact;
  }
}
```

Test both `print_background=True` and `print_background=False`; require the footer, page number, and S9 background to remain legible in both. Add a line to the PDF/help text: “Enable Background graphics if your print dialog offers the option.” The table stretch on print page 4 is a separate P0-5.

**Evidence.** [PDF page 1, background off](screenshots/compact-1/pdf-background-off-page-01.png) · [PDF page 1, background on](screenshots/compact-1/pdf-background-on-page-01.png) · [PDF page 9, background off](screenshots/compact-1/pdf-background-off-page-09.png) · [PDF page 9, background on](screenshots/compact-1/pdf-background-on-page-09.png) · [Footer crop](screenshots/compact-1/detail-pdf-footer-nobg.png)

![PDF page 1 with backgrounds off: footer nearly disappears](screenshots/compact-1/pdf-background-off-page-01.png)

![PDF page 9 with backgrounds off: the dark recap becomes a wireframe](screenshots/compact-1/pdf-background-off-page-09.png)

---

### P0-4. S9’s “same five-agent crew” is not the five agents — and “cyclic rework” has no loop

**Observed.** S9’s bottom lane header says:

> `CODEBASE LAB · SAME FIVE-AGENT CREW, CYCLIC REWORK`

The five boxes underneath are:

> **Cascade · Harbor · Rule pack · Critic · Planner**

Only Critic and Planner are agents. Cascade and Harbor are synthetic estates; Rule pack is a rule pack. The actual codebase loop, stated on S3, is **Scout → Architect → Guardian → Critic → Planner**. The bottom lane contains none of Scout, Architect, or Guardian. It also draws only straight horizontal connectors; there is no loop arc despite “cyclic rework.”

The footer under the same visual says:

> `11 open gates · 6 high · 7/7 checks · 8 sealed files · 0 deployed`

Those are feature-run metrics (R-DEMO-001), while the bottom lane shows Cascade 10 and Harbor 11 gates. A viewer sees “11” twice in different scopes with no label.

The title is also “One run, two migration shapes, zero deployment,” but S9 contains R-DEMO-001 plus two codebase estates — not one run.

**Why it matters.** This is the exact Scribe/Planner and “five-agent” confusion the deck fixes on S3/S4, reintroduced on the recap slide. A first-time viewer cannot map the five boxes to the five agents, cannot see the loop, and cannot tell which 11 is the feature run.

**Fix.** Either show the actual five codebase agents (Scout, Architect, Guardian, Critic, Planner) and put Cascade/Harbor/Rule pack counts in a side stat row, or rename the lane **“Codebase outcomes · two synthetic estates”** and stop calling it a five-agent crew. Add the rework arc if you keep “cyclic.” Label the footer **“Feature run R-DEMO-001: 11 gates”** or move the feature footer into the top lane. Change the title to “One method, two migration shapes” or label the three datasets explicitly.

**Evidence.** [S9 at 1440](screenshots/compact-1/deck-1440x900-slide-09.png) · [Bottom lane crop](screenshots/compact-1/detail-09-bottom-lane.png) · [S9 at 390](screenshots/compact-1/deck-390x844-slide-09.png)

![S9 bottom lane: Cascade, Harbor, Rule pack, Critic, Planner labelled “same five-agent crew”](screenshots/compact-1/detail-09-bottom-lane.png)

---

### P0-5. S4’s handoff table stretches to fill the body and leaves 100+ px of blank space per row

**Observed.** At 1920 × 1080, the table starts at y≈268 and ends at y≈990. Five rows plus the header take ~722 px; each row is ~144 px tall, but most rows contain only two lines of 14 px text. The “why pending” column text sits at the top of each row; the rest is blank. At 1440 the rows are ~115 px; at print page 4 they are similarly stretched. The right sidebar ends much earlier, so the slide is simultaneously overfilled in the table and underfilled on the right.

At 390 the table reflows to stacked cards and works much better. The problem is desktop/tablet/print.

**Why it matters.** S4 is the handoff ledger — the slide that should make the five-agent sequence concrete. Instead it is the least scannable slide on the deck; the eye has to jump across long blank bands. In print, the table looks unfinished. This is a layout bug, not a content problem.

**Fix.** Stop the table from stretching as a grid item:

```css
table.handoff { align-self: start; height: auto; }
.handoff-layout > table { align-self: start; }
```

Or wrap the table in a `div` that does not stretch. Let rows size to content. Then rebalance the sidebar or use the recovered space for a short “what to inspect next” note. Test at 1920, 1440, 1024, and in the PDF.

**Evidence.** [S4 at 1920](screenshots/compact-1/deck-1920x1080-slide-04.png) · [Table crop](screenshots/compact-1/detail-04-table-stretch.png) · [S4 print page 4](screenshots/compact-1/pdf-background-on-page-04.png)

![S4 at 1920: rows fill the page but the text does not](screenshots/compact-1/detail-04-table-stretch.png)

---

### P0-6. The progress bar contradicts the elapsed clock at both ends

**Observed.** The bar is set to each slide’s **end** time, while the adjacent label is “elapsed” (the slide’s start):

- S1: `00:00 elapsed · 10:00 left`, bar **5.83%**.
- S2: `00:35 elapsed · 09:25 left`, bar **13.33%**.
- S7: `05:55 elapsed · 04:05 left`, bar **67.5%**.
- S12: `09:35 elapsed · 00:25 left`, bar **100%**.

The same values appear in the PDF. The bar is internally consistent with `data-end`, but not with “elapsed.” At S12 the bar is full while 25 seconds remain; at S1 it shows progress before any time has elapsed.

**Why it matters.** This is a 10-minute deck; the footer is the speaker’s only timing instrument. A full bar at 09:35 tells the speaker to stop 25 seconds early, and a 5.8% bar at 00:00 looks like a bug. The deck’s timing is otherwise exact; the bar undermines it.

**Fix.** Use the slide start for the bar (`start / 600`), or change the label to “planned end” and add a separate live timer. The simplest consistent fix is start-based: S1 0%, S12 95.83%. If you want a live clock, update it every second; if you want a cue card, label it “cue at 09:35” rather than “elapsed.” Test the PDF page 1 and page 12.

**Evidence.** [S1 footer crop](screenshots/compact-1/detail-progress-slide-01.png) · [S12 footer crop](screenshots/compact-1/detail-progress-slide-12.png) · [S1 full](screenshots/compact-1/deck-1440x900-slide-01.png) · [S12 full](screenshots/compact-1/deck-1440x900-slide-12.png)

![S1: 00:00 elapsed, bar already 5.83%](screenshots/compact-1/detail-progress-slide-01.png)

![S12: 00:25 left, bar already 100%](screenshots/compact-1/detail-progress-slide-12.png)

---

## 5. P1 — fix before external sharing

### P1-1. Opening speaker notes does not move focus into the panel

**Observed.** After pressing `n` on every slide at 1440 and 390, the panel was open (`open` class, `aria-hidden="false"`, `inert=false`, toggle `aria-pressed="true"`) but `document.activeElement` was `BODY` on slide 1 and `notes-toggle` on slides 2–12. It was never `notes-close`. The orange focus ring stays on the Notes button while the panel is open.

The cause is the visibility transition: `.notes-panel` transitions `visibility` over .22 s; `openNotes()` calls `notesClose.focus()` while the panel is still `visibility:hidden`, so Chromium ignores the focus. A manual `focus()` after the transition works.

**Why it matters.** Keyboard and screen-reader users open the notes but stay outside them; Tab continues through the chrome instead of the note text. The notes also cover 430 px of a 1440 screen (359 px of 390), so a presenter cannot point at the right-hand content while reading them.

**Fix.** Move focus after the panel is visible — `requestAnimationFrame` after removing the visibility transition, `transitionend`, or a short timeout. Add `role="dialog"`/`aria-modal` if the panel is meant to be modal, or leave it non-modal but focus the first note. Also consider a presenter-window mode or a layout shift so notes do not cover the slide’s right column.

**Evidence.** [Notes 1440 slide 3](screenshots/compact-1/notes-1440x900-slide-03.png) · [Focus crop](screenshots/compact-1/detail-notes-focus.png) · [Notes 390 slide 4](screenshots/compact-1/notes-390x844-slide-04.png)

![Notes panel open, focus ring still on Notes](screenshots/compact-1/detail-notes-focus.png)

---

### P1-2. The standalone demo auto-plays and fires six step announcements without user initiation

**Observed.** On a normal load, the demo sets `playing=true` and schedules step 1 after 850 ms. At 1.2 s it is already at Step 1, the button says **Pause**, and the live region says “Step 1 of 6. Scout maps 300 files…”. It continues through six steps at 900–950 ms each. A first-time viewer never sees a stable “Ready” state; a screen-reader user gets rapid unsolicited announcements.

**Why it matters.** A demo linked from a presentation should start when the presenter is ready. The auto-play also defeats the purpose of the Play button: the page is already playing before the viewer reads the title. For screen-reader users, six polite live-region updates in ~6 seconds are disruptive and cannot be paused before they start.

**Fix.** Start paused. Keep the reduced-motion final-state behavior, but do not auto-play in the normal context. If auto-play is a deliberate kiosk mode, gate it behind a visible “Autoplay” control and do not announce every step to the live region. At minimum, stop auto-play when the page is not visible or when the user has not interacted.

**Evidence.** [Auto-play at 1.2 s](screenshots/compact-1/demo-1440x900-autoplay-1s.png) · [Step 0](screenshots/compact-1/demo-1440x900-step0.png)

---

### P1-3. Demo codebase cards make Critic and Planner look like “0” and “2 iterations”

**Observed.** In codebase mode at 1440 and 390:

- **Critic:** big number **0**, unit `AUTO-APPROVALS`; detail “every displayed diff applied”; foot “checks pass · human decision still required.” The narration says “Critic applies every displayed diff and makes 0 auto-approvals.”
- **Planner:** big number **2**, unit `ITERATIONS`; detail `Cascade 18 / 22 / 10` (unlabelled); foot `Harbor 20 / 21 / 11 · findings / patches / gates` on desktop, **hidden at 390**. The narration says “Planner seals 2 codebase plans.”

At 390 the Planner card loses Harbor entirely and never says “plans”; the only visible numbers are `2` and `Cascade 18 / 22 / 10`.

**Why it matters.** The codebase mode is supposed to be the “same five agents, cyclic” story. Instead, the fifth agent’s card does not show what it produces, and the fourth agent’s headline reads like a failure (“0”). This is a five-agent clarity problem in the companion visualization.

**Fix.** Make Critic’s primary output “every diff applied” or “checks pass” with “0 auto-approvals” as the footnote. Make Planner’s primary output “2 plans sealed” or “2 review bundles”; put `Cascade 18/22/10 · Harbor 20/21/11` in a labelled two-row detail. Do not hide the Harbor row at 390; if space is tight, stack the two estates rather than dropping one.

**Evidence.** [Codebase 1440 step 6](screenshots/compact-1/demo-1440x900-codebase-step6.png) · [Codebase 390 step 6](screenshots/compact-1/demo-390x844-codebase-step6.png) · [Critic/Planner crop](screenshots/compact-1/detail-demo-mobile-planner.png)

![Codebase mobile: Critic reads 0, Planner reads 2 iterations, Harbor is hidden](screenshots/compact-1/detail-demo-mobile-planner.png)

---

### P1-4. S8’s 9/11/12 event numbers need a state table

**Observed.** S8 simultaneously shows:

- “Audit head read live · **9 seed events, 11 after two reviewer decisions**.”
- `verify-audit` output: **`OK (9 events, head …)`**.
- `verify-migration` output: **`OK - 12 events verified`**.

The 9 is the live seed run; the 11 is an isolated post-decision packet; the 12 is the separate migrator log. The notes explain this, but the slide does not. The title also promises an “open question,” yet the evidence card shows no assumption/open-question example. A first-time viewer sees 9, 11, and 12 in two adjacent cards and cannot tell which is which.

**Why it matters.** This is the trust slide. Confusing state counts in the trust slide is worse than confusing them anywhere else. The verify command demonstrates 9, while the headline says 11 after decisions; a viewer who runs the command sees a different number.

**Fix.** Add a compact three-row table:

| Chain | State | Count |
|---|---|---:|
| Review packet audit | seed | 9 |
| Review packet audit | post-decision copy | 11 |
| Migrator log | run | 12 |

Label the verify block “seed-state run” or run it against the post-decision copy. Add one assumption card with an owner and the question that would close it, so the “open question” in the title is actually shown.

**Evidence.** [S8 at 1440](screenshots/compact-1/deck-1440x900-slide-08.png) · [Event/verify crop](screenshots/compact-1/detail-08-event-numbers.png) · [S8 notes](screenshots/compact-1/notes-1440x900-slide-08.png)

![S8: 9 seed events, 11 after decisions, 12 migration events, with no state table](screenshots/compact-1/detail-08-event-numbers.png)

---

### P1-5. S4’s “STATE LABEL” mixes 11 gates with 11 audit events

**Observed.** S4’s right sidebar says:

> “Seed-state run: 3 assumptions and 11 gates. After two reviewer decisions the packet has 4 assumptions and **11 audit events**; the migrator chain count is not silently reused.”

“11 gates” and “11 audit events” are different units with the same number, in adjacent sentences. The card is called “STATE LABEL” but mixes the seed and post-decision states in one paragraph. “Migrator chain count” is internal jargon.

**Why it matters.** This is the remaining 3-vs-4 / 10-vs-11 ambiguity in a new form. A viewer can read “11” as a reused gate count or an audit count. The slide’s main table already explains why each row is pending; this card adds cognitive load without adding a decision.

**Fix.** Rewrite as two labelled states, or move it to notes:

> “This slide uses the seed run: 3 assumptions, 11 gates. The post-decision packet (4 assumptions, 11 audit events) is a different snapshot; don’t mix the two counts.”

If it stays, add a visual two-column “Seed / Post-decision” comparison with units in the column headers. Do not put the same number next to two different nouns.

**Evidence.** [S4 at 1440](screenshots/compact-1/deck-1440x900-slide-04.png) · [State card crop](screenshots/compact-1/detail-04-scribe-planner-state.png)

---

### P1-6. Demo feature mode still shows the codebase rework arc under “Straight handoff”

**Observed.** In Feature chain mode, the section note says “Straight handoff · nothing auto-approved,” but the dashed rework arc and the label **“REWORK PATH · codebase loop”** are still visible under the chain. At 390 the section note is hidden entirely, so the only nearby explanation is the small rework label. The deck’s S3 explicitly says “Chain, not loop.”

The codebase mode is the one that should show the arc; in feature mode it is a contradiction, not a legend.

**Why it matters.** A first-time viewer cannot tell whether the feature chain loops. This is the same chain-vs-loop confusion the deck is trying to settle. The visual should not require the reader to parse “codebase loop” as an inactive legend.

**Fix.** Hide `.rework` in feature mode, or render it at very low opacity with an explicit “not used in this mode” label. In codebase mode, keep the amber animated arc. At 390, keep a short “straight handoff” label near the mode toggle, not just the rework label.

**Evidence.** [Feature step 0](screenshots/compact-1/demo-1440x900-step0.png) · [Rework crop](screenshots/compact-1/detail-demo-feature-rework.png) · [Feature mobile](screenshots/compact-1/demo-390x844-step0.png)

![Feature mode with the codebase rework arc still visible](screenshots/compact-1/detail-demo-feature-rework.png)

---

### P1-7. The glossary is too late and too small for the jargon load

**Observed.** Jargon appears on S2/S5/S6/S7/S8/S10 before the S11 glossary:

- `PCF`, `entity`, `typelist`, `Gosu` (S2, S6)
- `P&C`, `Qusar` (S5)
- `JMS`, `JDBC`, `servlet`, `App Events`, `SARIF` (S6)
- `APD`, `mTLS`, `Gosu API`, `Cloud API` (S7)
- `xpath`, `xml_xpath`, `verified-doc`, `excerpt_sha256` (S8)
- `CSP`, `CSRF`, `YAML alias bombs`, `zip-slip` (S10)
- `IAA`, `LOB` (S12)

The S11 glossary defines only **Gosu, APD, CDA, App Events, SARIF**. It does not define PCF, typelist, JMS, JDBC, `_gen`, `draft_ready`, `verified-doc`, `IAA`, or `LOB`. Even the five definitions arrive after the terms have been used for eight slides.

**Why it matters.** This is the main reason the code and evidence slides need the speaker. A layman can follow the thesis and the gates, but not the implementation. The user asked for a first-time viewer with no explanation; this is where that fails.

**Fix.** Add a compact “Plain language” panel to S2 or S3, or inline definitions at first use:

- Guidewire = the insurance core system; estate = its configuration + custom code.
- PCF = screen/page configuration; Gosu = Guidewire’s JVM language.
- SARIF = machine-readable static-analysis output; advisory, not a compliance verdict.
- APD = Advanced Product Designer; CDA = Cloud Data Access.
- `_gen` = generated files; `draft_ready` = a draft awaiting human approval.
- IAA = inter-annotator agreement; LOB = line of business.

Move the S11 glossary earlier or duplicate the five key terms on S2/S3. Keep S11 for the full list.

**Evidence.** [S2](screenshots/compact-1/deck-1440x900-slide-02.png) · [S6](screenshots/compact-1/deck-1440x900-slide-06.png) · [S8](screenshots/compact-1/deck-1440x900-slide-08.png) · [S11 glossary](screenshots/compact-1/deck-1440x900-slide-11.png)

---

### P1-8. On mobile, the timing hint lives below two screens of content

**Observed.** At 390, S7 is 2,148 px tall; S4 1,863; S11 1,818; S5 1,725. The footer containing `05:55 elapsed · 04:05 left` and the progress bar sits after the content. The chrome hides the section label at ≤440, so while you are reading the top of S7 there is no visible timing cue. The deck is a 10-minute presentation, but the mobile footer is a bottom-of-document footer, not a persistent cue.

**Why it matters.** A presenter using a phone cannot pace the talk without scrolling to the bottom of each long slide. This compounds P0-2: the headline squeeze makes the slides long, and the timing hint is then farther away.

**Fix.** Put a compact `05:55 / 04:05` and a 3 px progress bar in the sticky chrome on mobile, or make a slim sticky footer. The full footer can remain at the bottom. This also gives the audience a visible time cue.

**Evidence.** [S7 full 390](screenshots/compact-1/deck-390x844-slide-07.png) · [S1 full 390](screenshots/compact-1/deck-390x844-slide-01.png)

---

### P1-9. The 10-minute script is exact on paper but rushed at the end

**Observed.** The 12 notes total **1,323 words**. At 150 wpm that is 8.8 minutes before pauses; at 130 wpm it is 10.2 minutes. The late cues require:

| Slide | Words | Cue | Required wpm |
|---|---:|---:|---:|
| S8 Evidence & audit | 125 | 45 s | 167 |
| S10 Engineering rigor | 109 | 35 s | 187 |
| S11 Reality boundary | 124 | 45 s | 165 |
| S12 Close | 77 | 25 s | 185 |

S12’s note says “Slow down and close” but allocates 25 seconds for 77 words. S10 says “Pick two proofs” in 35 seconds while the slide has four stat cards, two body cards, and a bottom strip. S8 has 45 seconds for an evidence card, hash chain, and three verify commands.

**Why it matters.** The deck is sold as a 10-minute cut. The first eight minutes have slack (S3 91 wpm, S4 106, S5 98); the last four slides are sprinting. A cold presenter will overrun or skip the boundary. There is no room for a demo glitch, a question, or a pause.

**Fix.** Rebalance the cue table: give S8, S10, S11, and S12 +10–15 seconds each; take it from S3/S4/S5, which have room. S12 should be 35–40 seconds, not 25. Update `data-start`/`data-end`, all footers, and the notes. Rehearse with a stopwatch; the script should fit 10:00 with at least 30 seconds of slack.

**Evidence.** [Notes S10](screenshots/compact-1/notes-1440x900-slide-10.png) · [Notes S12](screenshots/compact-1/notes-1440x900-slide-12.png) · [S7 footer](screenshots/compact-1/deck-1440x900-slide-07.png)

---

### P1-10. Tap targets are 22–28 px, not 44 px

**Observed.** At 390:

- Deck chrome: Notes 45 × 26; Help 38 × 26; PDF 36 × 26.
- Notes close: 28 × 28.
- Demo controls: 52 × 27 (Play/Step), 59 × 27 (Reset).
- Demo mode toggle: 82 × 24 / 88 × 24.
- S9 “Open full visualization” link: 164 × **22**.
- PDF/skip/help targets similarly small.

Most are above the 24 px WCAG 2.5.8 AA floor, but all are far below the 44 px comfortable-touch target; the 22 px S9 link is below 24. The deck is otherwise mobile-friendly in width; the controls are the weak point.

**Why it matters.** A phone user has to hit small targets in the chrome and demo controls, often while presenting. The 22 px link is the only route to the companion visualization.

**Fix.** Give mobile chrome buttons and demo controls `min-height: 44px` (or 40–44 with spacing), increase the notes close button to 44, and make the S9 link a block with 44 px height. Keep the visual style; add padding rather than larger type.

**Evidence.** [S9 mobile](screenshots/compact-1/deck-390x844-slide-09.png) · [Demo controls crop](screenshots/compact-1/detail-demo-mobile-controls.png) · [Demo mobile](screenshots/compact-1/demo-390x844-step0.png)

---

### P1-11. The demo loses “not affiliated with Guidewire” on mobile

**Observed.** At 390, the demo hides:

- `.boundary` (the footer line `Synthetic fixtures · local-only · no tenant contacted · not affiliated with Guidewire`) — `display:none`.
- `.meta-synthetic` (the `Synthetic` meta), `.brand-sub` (`Independent research prototype`), and `.meta-local`.

The reality card still says “synthetic fixtures · no tenant · no compile · no official Cloud Assurance · not an actual migration,” so the synthetic/not-real boundary is present. But the **non-affiliation** sentence and the “independent research prototype” label are gone. The subtitle says “Synthetic Guidewire-style migration rehearsal,” which covers “synthetic” but not “not affiliated.”

**Why it matters.** This is a legal/trust boundary, not decoration. On mobile, the companion visualization is the only page a viewer may see; it should not be possible to read it as an official Guidewire artifact.

**Fix.** Add “Not affiliated with Guidewire” to the mobile reality card, or keep a compact boundary line in the footer/controls. Do not rely on a hidden desktop footer. Also keep “independent research prototype” visible at 390.

**Evidence.** [Demo 390 step 0](screenshots/compact-1/demo-390x844-step0.png) · [Demo 390 reduced](screenshots/compact-1/demo-reduced-390x844.png)

---

### P1-12. S5’s outcome strip is tiny, duplicate, and loses the Cascade/Harbor order

**Observed.** S5 includes an inline raster “outcome strip” below the two case cards. It repeats 18/22/2/10 and 20/21/2/11 with app labels `BLOCKERS FOUND`, `PATCHES DRAFTED`, `LOOP PASSES`, `HUMAN GATES`, `green · gated`. The deck already shows those counts in the cards above. At 1024 the strip is ~60 px tall and its labels render at ~7–8 px; they are unreadable. At 1920 the strip is still only ~102 px tall and adds nothing the cards do not. The caption only maps “blockers found → findings” and “patches drafted → patches”; it does not map “loop passes” to “iterations” or “green · gated” to `green_with_human_gates`.

The S7 scenario chips also use `7 / 6` and `4 / 3` without saying which number is Cascade and which is Harbor.

**Why it matters.** The strip is meant to be evidence from the app, but at 1024 it is noise; at 1920 it duplicates. The unlabelled chip order makes the correct non-cumulative arithmetic harder to verify than it should be.

**Fix.** Hide the strip below 1200 px or double its height and label size; remove it if the cards carry the counts. Add `Cascade / Harbor` to the S7 chips (“Gateway mTLS · 7 / 6 (Cascade / Harbor)”) or a small legend. If the strip stays, map all five app labels to the deck terms, not just two.

**Evidence.** [S5 at 1920](screenshots/compact-1/deck-1920x1080-slide-05.png) · [Outcome strip at 1024](screenshots/compact-1/detail-05-outcome-strip-1024.png) · [S7 chips at 1920](screenshots/compact-1/deck-1920x1080-slide-07.png)

![S5 outcome strip at 1024: labels are ~7–8 px](screenshots/compact-1/detail-05-outcome-strip-1024.png)

---

## 6. P2 — polish and consistency

- **Desktop composition is top-heavy.** At 1920, S1’s title ends around y=520 with a ~1,012 px body; S3 ends around y=570; S8 around y=700; S10 around y=790. The anchor-bottom strips float at the bottom, leaving 18–49% of the body empty. Either vertically center the content block, grow the cards, or remove the anchor-bottom strips and let the slides breathe consistently. S4 is the opposite problem (table stretch).
- **S10’s stat hierarchy is wrong.** The first card’s largest element is the phrase “current pytest suite”; the actual number (481, currently stale) is 11 px. Show **520** at 39 px, with “pytest tests passing” and the date below. The other three cards already do this.
- **S10’s rigor claims lack pointers.** “5.8/10,” “8 flaws,” “18/18,” and “101/101” are asserted with no source IDs, commit, or file links. Add a line: `pytest`, `scripts/freeze.py`, `preflight verify-*`, and a commit hash. The deck’s own S1 standard says every claim should be inspectable.
- **Title slide boundary lacks non-affiliation.** S1 says synthetic/no tenant/no compile/not official Cloud Assurance; “not affiliated with Guidewire” appears only on S12. Add it to S1 and/or the repeated footer, especially for handouts and screenshots.
- **S12’s disclaimer is 11 px.** It is the legal/trust sentence; bump to 12–13 px and keep the “Official Cloud Assurance: not run” bold. Expand `IAA` and `LOB` on first use.
- **Links and return path.** S12’s repository and deck paths are plain text. Make them links. S9’s “Open full visualization” opens in the same tab and the demo has no “back to deck” link; open in a new tab or add a return link.
- **PDF is untagged.** `pdfinfo` reports `Tagged: no`. If the PDF is a handout, export a tagged PDF or provide the HTML as the accessible version. The HTML deck has good semantics; the PDF does not inherit them.
- **Demo unlit cards at step 0 are 34% opacity.** The first frame and a paused/reset state are washed out; the cards’ text is meaningful even before it is “lit.” Raise to ~0.55–0.65 or use a border/“pending” marker instead of near-invisibility.
- **Skip link wording.** The deck’s first Tab focuses “Skip to first slide,” which resets a viewer on slide 7 to slide 1. A skip link should bypass the chrome to the current slide content; at minimum rename it “Skip controls” if resetting is intentional.
- **S9’s “Open full visualization” link is 22 px high.** Covered in P1-10, but it is also the only navigation path to the companion; make it a block target and consider a back link.
- **S5’s 74/71 scores have no method.** “Human-gate-adjusted 74/100” is a strong claim; a one-line formula or link to `CASE-STUDIES.md` would make it inspectable.
- **S8’s “verified-doc” tag.** Define it as a claim-strength label from public documentation, not a verified finding. The page currently says “caps what may be inferred,” which is good, but the word “verified” will be over-read.
- **S9’s “one run.”** Label R-DEMO-001, Cascade, and Harbor explicitly; “one run” currently covers three datasets.
- **PDF page 4 table.** The table stretch is P0-5; the print version is the worst case. Re-test after the CSS fix.

---

## 7. Prioritized fix list

### P0 — block a first-time 10-minute showing

1. **Update the evidence numbers.** S10 481 → current 520; update the S10 note, README badge, and `VERIFICATION.md`. Label the 5.8/10 as the old 23-slide audit or remove it.
2. **Fix the 390 header.** Stack `.slide-head` and `.head-badge`; give `h2`/`.lede` the full 358 px. Re-test S7/S5/S4; target h2 ≥ 300 px and no one-word lines.
3. **Fix print color.** Add `print-color-adjust: exact`; test `print_background=False`; require the footer boundary, page numbers, and S9 dark visual to survive.
4. **Rewrite S9’s bottom lane.** Show the actual five codebase agents or rename it “Codebase outcomes”; add the loop; label the feature-run 11 vs Cascade 10/Harbor 11; clarify “one run.”
5. **Fix S4’s table.** `align-self:start; height:auto`; content-height rows at 1920/1440/PDF.
6. **Fix the progress bar.** Use start time or relabel; no 100% bar at 09:35 and no 5.8% bar at 00:00.

### P1 — fix before external sharing

7. **Notes focus.** Focus `notes-close` after the panel is visible; test activeElement on all 12 slides at 1440/390.
8. **Demo auto-play.** Start paused; do not fire six step announcements on load; keep reduced-motion final state.
9. **Demo codebase cards.** Critic primary output = checks/diffs applied; Planner primary output = plans/review bundles; show both estates at 390.
10. **S8 state table.** 9 seed / 11 post-decision / 12 migration log; label the verify command; add the missing assumption/open-question example.
11. **S4 state label.** Separate 3 vs 4 assumptions and 11 gates vs 11 audit events; rewrite or move to notes.
12. **Glossary.** Add PCF, Gosu, SARIF, APD, JMS, JDBC, `_gen`, `draft_ready`, `verified-doc`, IAA, LOB; move key terms earlier.
13. **Mobile timing cue.** Sticky mini-timer in chrome/footer; the footer is two screens down on S7.
14. **Rebalance the 10-minute cues.** +10–15 s for S8/S10/S11/S12, especially S12 (35–40 s); take from S3/S4/S5.
15. **Tap targets.** 44 px minimum for chrome, notes close, demo controls, mode toggle, and S9 link.
16. **Demo mobile boundary.** Add “not affiliated with Guidewire” and “independent research prototype” to the visible mobile page.
17. **S5 strip/chips.** Hide or enlarge the outcome strip below 1200; label Cascade/Harbor order on S7 chips.

### P2 — polish

18. Desktop vertical composition; stop the top-heavy 1920 layouts.
19. S10 stat hierarchy; show the test count as the number.
20. S10 source pointers/commit; align with the deck’s evidence standard.
21. Title non-affiliation; S12 disclaimer size; IAA/LOB expansion.
22. Repo/deck links; demo back link; S9 link target.
23. PDF tagging; accessible HTML alternative.
24. Demo unlit opacity; skip-link wording; S5 74/71 method; `verified-doc` explanation.

---

## 8. Re-check plan

When this round is fixed, retest at minimum:

- **390:** h2 width on S2–S8, S10, S11; slide heights; footer visibility at the top; notes focus; chrome target heights; S9 link target.
- **Print:** `print_background=False` on pages 1, 4, 9, 12; footer boundary; page numbers; S9 dark canvas; S4 row heights; `pdfinfo` page count/size/tagged.
- **Evidence:** `pytest -o addopts=""` → expected count; `preflight verify-audit`, `verify-packet`, `verify-migration`; 18/18 freeze; 101/101 links; S10 count/date/commit.
- **S9:** bottom lane maps to actual agents; loop arc; feature-run footer label; “one run” scope.
- **Demo:** normal load starts paused; Play/Pause/Step/Reset; mode toggle at step 0 and 6; codebase Critic/Planner primary outputs; mobile Harbor visible; reduced-motion final state; auto-play not announcing unsolicited.
- **10-minute:** stopwatch rehearsal from S1 to S12; target 10:00 with ≥30 s slack; confirm S12 is not rushed.

---

## 9. Coverage and screenshot index

Everything is under `docs/audits/screenshots/compact-1/`.

- **Deck clean captures (60):** `deck-{1920x1080,1440x900,1280x720,1024x768,390x844}-slide-01.png` … `-slide-12.png`. Mobile captures are full-page.
- **Speaker-notes captures (24):** `notes-{1440x900,390x844}-slide-01.png` … `-slide-12.png`.
- **Demo captures:** step 0 and codebase step 0/6 at 1920/1440/390; feature step 6 at 1920/1440; codebase step 2 at 1440; `demo-reduced-{1440x900,390x844}.png`; `demo-1440x900-autoplay-1s.png`; `demo-390x844-step0-viewport.png`.
- **PDFs:** `compact-10min-print.pdf` (background on), `compact-10min-print-nobg.pdf` (background off).
- **PDF renders:** `pdf-background-{on,off}-page-{01,04,09}.png`, plus `pdf-bg/` and `pdf-nobg/` raw page renders.
- **Detail crops:** `detail-04-table-stretch.png`, `detail-04-scribe-planner-state.png`, `detail-05-mobile-headline.png`, `detail-05-outcome-strip-1024.png`, `detail-07-mobile-headline.png`, `detail-08-event-numbers.png`, `detail-09-bottom-lane.png`, `detail-10-pytest-stat.png`, `detail-10-note-520.png`, `detail-10-audit-58.png`, `detail-notes-focus.png`, `detail-progress-slide-01.png`, `detail-progress-slide-12.png`, `detail-pdf-footer-nobg.png`, `detail-demo-feature-rework.png`, `detail-demo-mobile-agents.png`, `detail-demo-mobile-controls.png`, `detail-demo-mobile-planner.png`.
- **Contact sheets:** `contact-{1920,1440,1280,1024,390}.png`.
- **Measurements:** `deck-metrics.json`, `notes-metrics.json`, `demo-metrics.json`, `measure.json`.
- **Other:** `deck-1440-help.png`.

Note: `docs/audits/screenshots/` is gitignored by the repository (`.gitignore` line 20), so these images are present locally but will not be committed unless force-added. The report’s links assume the local files remain.

---

## 10. Bottom line

This is not a bad deck. It is a strong, honest, technically literate deck with a real thesis and better evidence discipline than most migration pitches. The gate and evidence sections are the best material; the compact cut is substantially clearer than the 23-slide version. The fixes that held — APN, literal 10/11, APD overclaim, CDA, non-cumulative arithmetic, repeated boundary, offline/console/network hygiene — are real and should be preserved.

But the artifact is not yet ready for the audience it claims to serve:

- a first-time viewer on a phone gets one- and two-word headline columns;
- a reader of the PDF may lose the repeated “Official Cloud Assurance: not run” boundary;
- a viewer of S9 is told a false five-agent crew;
- a presenter is told the current suite is 481 when it is 520;
- a reader of S10 is shown a 5.8/10 score from a different deck;
- a speaker is given a 100% progress bar with 25 seconds left.

Those are fixable. Fix the six P0 items, add a plain-language glossary, rebalance the last four cues, and re-score. I would then expect this to land around 8/10 for a technical audience and 7/10 for a cold layman audience. Today it is 6.4/10, and I would not send the default PDF or show the mobile deck.

**No deck, demo, app, or data files were modified.**
