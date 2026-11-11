# PreFlight deck — independent layman + visual audit (Round 1)

**Deck:** <http://127.0.0.1:8091/index.html> — 23 slides
**Auditor:** Independent layman / visual reviewer. No prior knowledge of Guidewire, Gosu, APD, Cloud Data Access, App Events, or PreFlight.
**Date:** 2026-11-11
**Viewports:** 1440 × 900 and 390 × 844
**Method:** keyboard navigation (`→` through all 23 slides, `Home`/`End`, `?` help), speaker notes opened with `n` on every slide, clean and notes screenshots, full-page mobile captures, DOM measurements, printed PDF inspection. No deck or app files were edited.

**Evidence:** [1440 clean shots](screenshots/slides-layman-1/1440) · [1440 notes shots](screenshots/slides-layman-1/1440) (`*-notes.png`) · [390 viewport shots](screenshots/slides-layman-1/390) · [390 full-page shots](screenshots/slides-layman-1/390-full) · [detail crops and PDF renders](screenshots/slides-layman-1) · [capture data, 1440](screenshots/slides-layman-1/deck-1440.json) · [capture data, 390](screenshots/slides-layman-1/deck-390.json)

**Scoring calibration:** 10 = a first-time viewer can retell it with no explanation; 7 = clear after one careful read; 5 = needs the speaker/notes; 3 = requires domain knowledge; 0 = unusable. Scores are for the whole deck, not its best slide. I was deliberately harsh; a Guidewire-literate judge would score the gate, agent, and code sections higher.

---

## 0. Verdict

**5.8 / 10 — polished and honest, but not layman-ready.**

The deck has a strong thesis, a coherent visual language, unusually honest limitations, and a few excellent explainer slides (1, 10, 13, 15, 16, 23). It is also dense with unexplained domain terms, and two of its most important explanations break down: the fifth agent changes identity between the feature and codebase loops without explanation, and slide 18 says the lab both compiles and does not compile. Mobile and print lose critical evidence and, at 390, the persistent disclaimer is truncated.

| # | Category | Score | One-line rationale |
|---:|---|---:|---|
| 1 | Layman comprehension | **5** | I can retell the thesis from slide 1 / slide 4, but APD, PCF, typelist, Gosu, SBT, CUE, CDA, and GWCP arrive before definition. |
| 2 | Product story | **6** | Strong “evidence before estimate” arc; the five-agent story arrives too late and the feature/codebase number spaces are not bridged. |
| 3 | Five-agent clarity | **5** | Scout → Architect → Guardian → Critic → Scribe is clear; Scribe vs Planner, and loop vs chain, are not. |
| 4 | Gate / human-approval clarity | **7** | 11 gates, 7 checks, and 8 sealed files are clear on slides 15–16; the 5 packages ↔ 11 gates relationship is not shown, and 3 vs 4 assumptions is unlabeled. |
| 5 | Migration-story clarity | **6** | Cascade 18/22/2/10 and Harbor 20/21/2/11 are clear and synthetic; the cut-off screenshot and “APD conversion” vs “naming preparation” conflict hurt it. |
| 6 | Code-level clarity | **4** | The JDBC → Query shape is visible, but SARIF is undefined, “Planner compiles” contradicts “not a compiler,” and `10/11` is ambiguous. |
| 7 | Upgrade clarity | **8** | The simulation is stated in four places; table legibility and mobile layout are the remaining issues. |
| 8 | Data integrity | **5** | Count arithmetic mostly reconciles, but 3 vs 4 assumptions, “10/11,” the Harbor conversion label, and multiple caption/image mismatches are material. |
| 9 | Visual hierarchy | **6** | Consistent eyebrow/headline/lede pattern, but several slides leave 30–40% of the page blank while others are overfull. |
| 10 | Typography / readability | **4** | A 10px “floor” is still small for projection; several screenshots render at ~4–7px effective text and are unreadable at 390. |
| 11 | Animation / polish | **8** | Restrained motion, reduced-motion support, no distracting transitions; a missing favicon causes a console 404. |
| 12 | Accessibility / print | **6** | Good semantics, focus, contrast, notes; but PDF is untagged, print drops the boundary disclaimer, and mobile code is not keyboard-scrollable. |

**Overall: 5.8 / 10 (70/12).** The deck is credible for a technical reviewer. For a first-time lay viewer, it needs a glossary, a five-agent overview earlier, state labels on the migrator numbers, and a mobile/print pass.

**The two comprehension blockers I would fix first:**

1. **Slide 18:** “Planner compiles only after both gates agree” versus “the lab is a structural scanner, not a compiler” and “drafts are not compiled.” A viewer cannot tell what the fifth codebase agent actually does.
2. **Slides 13 + 17:** The feature path ends in **Scribe** and is called a “straight handoff chain”; the codebase path ends in **Planner** and is called a “five-agent loop.” No slide explains why the fifth agent changes or how Planner differs from Scribe.

**The two credibility risks:**

3. **3 assumptions (slides 13/15) vs 4 assumptions (slides 8/12).** The 11-gate arithmetic uses the seed-state 3; the post-decision packet has 4. The deck never labels the state, so a judge can reasonably think one number is stale.
4. **Slide 17:** The Harbor card says “APD NAMING PREPARATION” while the app screenshot directly below says “Cloud Retrofit with APD conversion · multi-LOB”; the boundary line then says “APN naming preparation” (likely a typo). The caption tries to explain it, but the slide still contradicts itself.

**The one visual blocker:** At 390, the fixed footer ellipsizes “Synthetic estate · not affiliated with Guid…” and hides “Official Cloud Assurance: not run”; most desktop screenshots are unreadable at phone width. In the PDF, the footer is removed entirely, so pages 14–16 and 20 have no visible boundary at all.

---

## 1. Coverage and measurements

### 1.1 What I did

- Opened the deck cold at 1440 × 900 and advanced with `→` from slide 1 to 23; verified each `aria-label` (“Slide N of 23”).
- Opened speaker notes with `n` on **every** slide and captured both the clean slide and the notes-open state (46 clean + 46 notes captures). Closed with `Esc`. Notes evidence: [slide 13 notes at 1440](screenshots/slides-layman-1/1440/slide-13-notes.png), [slide 13 notes at 390](screenshots/slides-layman-1/390/slide-13-notes.png).
- Tested `Home`, `End`, `?` help, and keyboard focus order. At 390, verified that changing slides resets `scrollY` to 0.
- Captured full-page 390 versions of every slide to inspect content below the fold; the viewport captures alone do not show the complete slide.
- Rendered all 23 pages of `docs/presentation/PreFlight-deck.pdf` at 100 dpi and inspected pages 1, 4, 9, 14–17, 19–23 in detail.
- Collected DOM metrics: viewport overflow, internal scroll regions, image natural vs displayed size, font sizes, focusable regions, and touch-target sizes.
- Read all speaker notes. **The notes are excellent** — they often contain the clearest, most honest explanation in the deck. That is also a problem: a self-serve viewer never sees them.

### 1.2 Measurements

| Check | Result |
|---|---|
| Slides navigated | 23 / 23, no missing or duplicate slide |
| Broken images | **0** — all 17 unique image assets load (`naturalWidth > 0`) |
| External requests | **0** — all resources local |
| Console errors | **1** — `GET /favicon.ico` 404 (not a content image) |
| 1440 DOM overflow/clipping | **0** detected among visible slide elements |
| 390 horizontal page overflow | **0** (`document.scrollWidth = 390` on all slides) |
| 390 slide heights | 940–1891 px (about 1.1–2.2 viewport-heights per slide) |
| Internal horizontal scroll regions | Slide 3 matrix and slide 14 package table are focusable; the slide 18 code blocks are **not** focusable |
| Touch targets at 390 | Notes 44×23, Help 38×23, PDF 36×23 CSS px (below the 44×44 recommendation) |
| PDF | 23 pages, 1200 × 675.12 pt, 16:9, all backgrounds present, **Tagged: no** |
| Key contrast pairs | #5B6B78 on #F6F8FA 5.17:1; #7F95A3 on #1B2833 4.81:1; #8A5A12 on #FBF1DF 5.28:1; #0B6B85 on #F6F8FA 5.71:1 — pass AA for normal text |

The 404 is a favicon, not a broken slide image. The deck is otherwise fully local and offline.

---

## 2. First-time viewer answers

### 2.1 Can I explain the product in one sentence after slide 4?

**Yes — if I quote the title slide. No — if I have to explain it in my own words without the deck's vocabulary.**

My one-sentence answer:

> “PreFlight is an offline, evidence-first review of a Guidewire-style insurance policy system: it inventories the files, links each claim to evidence, records every decision and unknown, and packages the result before a migration estimate is signed.”

That sentence is essentially slide 1's lede: “PreFlight is an offline, evidence-first review of a Guidewire-style policy administration estate. It inventories what exists, links claims to files, records every disposition, and names every unknown — before a migration estimate is signed.” That is the best product sentence in the deck and should be repeated on slide 4 and in the PDF.

What I **cannot** explain after slide 4:

- What **APD**, **PCF**, **typelist**, **Gosu**, **SBT**, **CUE**, **Olios**, or **JDBC** are. They are used on slides 2–4 before any definition. “Disposition” is also unexplained; I can guess it means a decision about a mapping, but the deck never says so in plain language.
- Why a “packet” is different from a dashboard or a report. Slide 4 says “one review packet,” but the difference is only obvious later, on slides 12 and 16.
- Why this is specifically for **Guidewire** and not any codebase. The deck says “Guidewire-style,” but the first four slides don't explain what Guidewire is or why the problem is specific to it.

Slide 4's title, “One pipeline. Nine stages. Every step leaves a trace,” describes the **how**, not the product. A viewer who lands on slide 4 without slides 1–3 would not know what PreFlight is for. The title slide's sentence should be repeated on slide 4.

**Score: 5/10.** The thesis is understandable; the domain is not. See [slide 1](../presentation/index.html#slide-1), [slide 2](../presentation/index.html#slide-2), [slide 3](../presentation/index.html#slide-3), [slide 4](../presentation/index.html#slide-4). Screenshots: [slide 1, 1440](screenshots/slides-layman-1/1440/slide-01.png), [slide 4, 1440](screenshots/slides-layman-1/1440/slide-04.png).

**What I would ask the presenter:** “What is APD? What is a typelist? Is Gosu a language or a file type? What is CUE? What is a disposition, and how is it different from a mapping?” The deck's speaker notes answer some of these; the slides do not.

---

### 2.2 Can I explain the five agents and the difference between the feature loop (Scribe) and codebase loop (Planner)?

**I can explain the first four agents and Scribe. I cannot explain why the codebase loop's fifth agent is Planner, or how Planner differs from Scribe.**

What I can say from slide 13:

| Agent | What I saw |
|---|---|
| **Scout** | Reviews the slice and collects evidence: 300 files, 101 evidence records, 31 links, 24 findings, 12 dispositions. |
| **Architect** | Turns dispositions into 5 work packages / 5 target files; all drafts are local and pending. |
| **Guardian** | Opens 11 human gates: 3 assumptions + 8 rule groups; 6 high impact; 0 resolved. |
| **Critic** | Runs 7 package-integrity checks; 7/7 pass; 0 auto-approved changes. |
| **Scribe** | Seals 8 listed bundle files (5 targets + plan + report + 12-event log); the manifest seals them; status `completed_with_gates`. |

That is a good chain. The cards have clear inputs and outputs, and “No authority to deploy” is unambiguous.

What I cannot explain:

- **Why the fifth agent is different.** Slide 17's strip says “five-agent loop Scout → Architect ↔ Guardian / Critic → **Planner**.” Slide 18 says “Planner compiles only after both gates agree.” But slides 13–16 only introduce **Scribe**. There is no slide that says “Scribe is the feature-packet sealer; Planner is the codebase-patch planner; they are alternative fifth steps.” I had to infer it from a breadcrumb and one sentence.
- **What Planner actually does.** Slide 18 says it compiles; the bottom of the same slide says the lab is “not a compiler” and “Drafts are not compiled.” That is a direct contradiction, not a nuance.
- **Whether the feature path is a loop or a chain.** Slide 13 says “This path is a straight handoff chain; the cyclic rework loop belongs to the codebase lab.” The screenshot on the same slide shows “↻ rework to Architect if a gate fails,” the alt text calls it a “five-agent cycle,” and the caption says “The page calls it a loop; the feature path is a straight handoff chain.” Three different shapes for the same path. A layman cannot tell which is true or why it matters.
- **Why Scribe's “seal” is not approval.** The slide says it, and slide 16 explains “sealed means tamper-evident, not approved,” but the Scribe/Planner role change obscures the point.

The deck's own speaker note for slide 13 says: “If someone calls it a loop, correct the shape: 'The feature path is a straight handoff chain. The cyclic Architect ↔ Guardian/Critic rework is the codebase lab.'” That is exactly the correction that should be on the slide, not only in the notes.

**Score: 5/10.** The five cards are the clearest thing in the deck; the Scribe/Planner question is unanswered, and the loop/chain language is self-contradictory. See [slide 13](../presentation/index.html#slide-13), [slide 17](../presentation/index.html#slide-17), [slide 18](../presentation/index.html#slide-18). Screenshots: [slide 13, 1440](screenshots/slides-layman-1/1440/slide-13.png), [slide 13 loop caption](screenshots/slides-layman-1/detail-13-loop-caption.png), [slide 17 strip](screenshots/slides-layman-1/1440/slide-17.png).

**Fix:** Add a two-column comparison, on slide 13 or 17:

> **Feature packet loop** — Scout → Architect → Guardian → Critic → **Scribe**. Scribe writes and seals the plan, report, manifest, and agent log; 8 listed files; no code is compiled; nothing is approved.
> **Codebase patch loop** — Scout → Architect ↔ Guardian/Critic → **Planner**. Planner turns the approved patch set and SARIF into the codebase plan; compile validation is future work / out of scope; nothing is approved.

Then use “handoff chain” only for the feature path and “loop” only for the codebase rework path; change the app screenshot/caption/alt to match.

---

### 2.3 Are the 5 packages / 11 gates / 7 checks / 8 bundle files understandable and consistent?

**Individually, yes. As one system, not quite.**

| Item | What the deck shows | Where | Verdict |
|---|---|---|---|
| **5 packages** | WP-01…WP-05; 5 target files; `draft_ready` and `pending` | Slide 14 table; slide 13 card; slide 16 check 2/6 | Clear. |
| **11 gates** | 3 assumption gates (G-01…G-03) + 8 rule groups (G-04…G-11); 6 high; 0 resolved | Slide 15 stats and tables | Clear arithmetic: 3 + 8 = 11. |
| **7 checks** | 7 package-integrity checks, all PASS; 0 auto-approved changes | Slide 16 table | Clear. |
| **8 bundle files** | 5 target drafts + plan + report + 12-event log = 8; manifest is the seal wrapper | Slide 16 seal cards and footnote | Clear once read; the 9th manifest file needs the wrapper explanation. |

**What fails the “one system” test:**

1. **The 5 packages and 11 gates are never reconciled on one slide.** Slide 14's “GATE / APPROVAL” column shows only **one** gate (G-03 on WP-05); the other four rows say “— / pending.” Slide 15 then shows 11 gates at the finding/rule-group level. A viewer is left asking: do the 5 packages have 1 gate or 11? The answer is that gates live at the finding/assumption level, not the package level, but the deck never says that. The G-03 mention on slide 14 is the only bridge.

2. **3 vs 4 assumptions is unlabeled.** The 11-gate arithmetic uses **3 assumptions** (slide 13: “11 open gates = 3 assumptions + 8 rule groups”; slide 15: “3 assumptions”). But slide 8 shows **4 assumptions after reject** and slide 12 shows **4 assumptions** post-decision after M-01 accept + M-12 reject. If the migrator ran on the post-decision review, A-DEC-04 would be a fourth assumption; the deck doesn't say whether it is excluded, not yet gated, or stale. The 11-gate number is internally consistent with the seed state, but the deck never labels the migrator run as seed-state. This is a material ambiguity for a judge trying to reconcile the review packet and the agent run.

3. **“10/11 human gates” on slide 18 is ambiguous.** It is intended to mean “Cascade 10 / Harbor 11,” but it reads as “10 of 11 gates” — the opposite of “gates remain open.” Slide 17's cards show 10 and 11 separately; slide 18's title should say “Cascade 10 and Harbor 11” or “all human gates remain open.”

4. **The 8-file logic is good but late.** The “8 = 5 + plan + report + log, plus manifest wrapper” explanation is on slide 16, after the viewer has seen 8, 11, 7, 5, and 12 in quick succession. A one-line recap on slide 16 (“5 packages → 11 gates → 7 checks → 8 sealed files”) would make the whole chain memorable.

**Score: 7/10.** The numbers are arithmetically consistent; the relationships and states are not. See [slide 14](../presentation/index.html#slide-14), [slide 15](../presentation/index.html#slide-15), [slide 16](../presentation/index.html#slide-16). Screenshots: [slide 14, 1440](screenshots/slides-layman-1/1440/slide-14.png), [slide 15, 1440](screenshots/slides-layman-1/1440/slide-15.png), [slide 16, 1440](screenshots/slides-layman-1/1440/slide-16.png).

**Fix:** Put a “state” chip on the migrator slides:

> **Seed review** — 9 audit events, 3 assumptions, 12 pending dispositions → 11 gates.
> **Post-decision packet** — 11 audit events, 4 assumptions (A-DEC-04), 12 dispositions → the packet shown on slide 12.

And add one line on slide 14: “The 11 gates are at finding/rule-group level; the package table shows the only package-level gate, G-03.”

---

### 2.4 Are Cascade and Harbor clear as synthetic migration stories, with the outcomes 18/22/2/10 and 20/21/2/11?

**Yes for the numbers and the contrast. No for the bottom screenshot and the Harbor label.**

What works:

- Slide 17 is explicitly “Two synthetic insurers”; both cards say “synthetic” and “illustrative synthetic footprint.” The numbers are prominent and correctly paired:

| Case | Findings | Patches | Iterations | Human gates | Rules fired | Structural / gate-adjusted |
|---|---:|---:|---:|---:|---:|---|
| Cascade Mutual | 18 | 22 | 2 | 10 | 13 | 100 / 74 |
| Harbor P&C | 20 | 21 | 2 | 11 | 15 | 100 / 71 |

- The story contrast is clear: monoline Personal Auto vs multi-line P&C; small integration surface vs claims/billing/coastal underwriting across application boundaries; more findings/gates for Harbor despite fewer patches. The deck even explains “the numbers differ because the estates differ, not because the method changes.”
- “Both green_with_human_gates” and “every patch pending” make the no-deployment boundary clear.

What fails:

1. **The bottom screenshot is a cut-off fragment.** The figure is `case-studies-outcomes-focus.png` (1210 × 230) displayed at 1307 × 171 with `object-fit: cover` and `object-position: 50% 12%`. It cuts the bottom of the image, exactly where the `18 / 22 / 2 / 10` and `20 / 21 / 2 / 11` outcome strips sit. The caption and alt text claim the outcome strips are shown; they are not. At 1440 it looks like a rendering bug; at 390 it is a sliver. The HTML cards above carry the numbers, so no data is lost, but the figure is misleading and visually broken. See [detail-17-harbor](screenshots/slides-layman-1/detail-17-harbor.png).

2. **The Harbor label contradicts the slide.** The Harbor card badge says **“APD NAMING PREPARATION”**; the app screenshot directly below says **“Cloud Retrofit with APD conversion · multi-LOB.”** The caption then says the visible “APD conversion” label is the app's program label, and the deliverable is type-level naming preparation only. The bottom boundary line says **“Harbor’s APD draft is type-level APN naming preparation only — not full APD conversion or field mapping.”** There are two issues here:
   - A first-time viewer sees “APD conversion” in the screenshot and “naming preparation” in the badge; the caption is 10px fine print.
   - **“APN” is undefined and looks like a typo for APD.** The deck never defines APN. See [detail-17-apn-typo](screenshots/slides-layman-1/detail-17-apn-typo.png).

3. **Terminology drift inside the evidence.** The app crop labels the same 18/20 as “blockers found” (source asset), while the slide says “findings”; the app says “patches drafted” and “loop passes,” while the slide says “patches” and “iterations.” The numbers are consistent, but the nouns are not. A judge comparing the screenshot to the cards will pause.

4. **Qusar / GWCP are unexplained.** “Synthetic Qusar 2026.08 snapshots with a simulated GWCP 2027.04 target” is the most jargon-heavy sentence on the slide. A layman can tell it is a release simulation from “simulated,” but not what Qusar or GWCP are.

**Score: 6/10.** The story and the numbers pass; the cut-off evidence, the Harbor conversion contradiction, and the APN typo fail. See [slide 17](../presentation/index.html#slide-17) and [slide 18](../presentation/index.html#slide-18). Screenshots: [slide 17, 1440](screenshots/slides-layman-1/1440/slide-17.png), [slide 17, 390](screenshots/slides-layman-1/390/slide-17.png), [PDF page 17](screenshots/slides-layman-1/pdf-page-17.png).

**Fix:** Replace the bottom figure with a clean crop of the two outcome strips only (large numbers, no “APD conversion” tag), or remove it and use the HTML cards. Change “APN” to “APD” or define it. Add a one-line “Harbor's APD work is naming preparation only, not conversion” next to the Harbor card, not only in the 10px boundary.

---

### 2.5 Is it clear this is NOT an actual migration and NOT official Cloud Assurance?

**On a 1440 screen: mostly yes. On a 390 screen: weakened. In the PDF: not on every page.**

Where the deck is strong:

- Slide 1: `OFFLINE`, `SYNTHETIC ESTATE`, `INDEPENDENT RESEARCH PROTOTYPE`, `NOT AFFILIATED WITH GUIDEWIRE`; the packet card says “Official Cloud Assurance was not run.”
- Slide 13: a red-bordered **REALITY BOUNDARY** panel: “Synthetic rehearsal, not an actual migration. No tenant contacted. No Gosu/Java compiled against Guidewire. No official Cloud Assurance result.” This is the clearest boundary in the deck.
- Slide 17: “synthetic profiles, not customer references. No customer data, no tenant connection, no Guidewire affiliation.”
- Slide 19: “5 SIMULATED SCENARIOS” and “simulated release scenario, not a published 2027.04 release.”
- Slide 22: “Research prototype,” “not viable as a standalone product on the current evidence.”
- Slide 23: the closing disclaimer.
- The 1440 footer repeats: “Synthetic estate · not affiliated with Guidewire · Official Cloud Assurance: not run.”

Where it fails:

1. **At 390, the footer truncates.** The persistent line becomes “Synthetic estate · not affiliated with Guid…” and the rest — including **“Official Cloud Assurance: not run”** — is ellipsized on every slide. The slide content sometimes repeats the boundary (slide 9 badge, slide 13 panel), but most slides do not. See [detail-390-footer](screenshots/slides-layman-1/detail-390-footer.png) and [390 slide 1](screenshots/slides-layman-1/390/slide-01.png).

2. **In the PDF, the footer is removed.** The print stylesheet hides `.foot`. Pages 14–16 and 20 have no visible “synthetic,” “not actual migration,” or “Official Cloud Assurance not run” statement; page 15 in particular reads like a real Guardian run with real customer findings. The disclaimer only brackets the handout at pages 1 and 23. See [PDF page 15](screenshots/slides-layman-1/pdf-page-15.png) and [PDF page 20](screenshots/slides-layman-1/pdf-page-20.png). The speaker notes for slides 14–16 say “Say the boundary plainly … not an official Cloud Assurance result,” but the audience/PDF reader never sees that.

3. **The screen footer is chrome, not content.** On a 1440 screen it is visible, so I would score the live view 9/10 for boundary clarity. On mobile/print, 5/10. The deck should put a compact boundary line in the slide content or a printed footer on every page.

**Overall: 7/10.** Strong on slide 13 and the live 1440 view; insufficient in the handout and at 390. See [slide 13, 1440](screenshots/slides-layman-1/1440/slide-13.png), [slide 9, 1440](screenshots/slides-layman-1/1440/slide-09.png), [PDF page 15](screenshots/slides-layman-1/pdf-page-15.png).

---

### 2.6 Is the code-level refactor / SARIF slide understandable without knowing Gosu?

**Only at the highest level. The code shape is visible; SARIF, the gates, and the compiler claim are not.**

What I can understand from slide 18:

- “Before” shows JDBC `DriverManager.getConnection`, `createStatement`, and a SQL string built with `+ vin +`.
- “After” shows a typed `Query.make(VehicleRating).select().toList()` in a `VehicleRatingQueryService`-like class.
- The point seems to be: replace string-concatenated SQL with a supported typed query, but the draft is not compiled and semantic equivalence is a gate (CR-03).
- The bottom says the lab is a structural scanner, not a compiler or data-flow engine; drafts are not compiled; every patch is pending.

What I cannot understand:

1. **What SARIF is.** The title, badge, and right panel say “SARIF 2.1.0 — advisory by construction,” “18 results / 13 rules,” “partialFingerprints.primaryLocationLineHash,” “upload-sarif.” There is no plain-language “SARIF is the machine-readable static-analysis output; it is advisory, not a compliance verdict; here is what one result means.” A layman sees a wall of code and JSON vocabulary.

2. **Why the lab both compiles and does not compile.** The lede says: “Architect drafts patches, Guardian re-scans the target, Critic applies every displayed diff, and **Planner compiles only after both gates agree**.” The bottom says: “The lab is a structural scanner, **not a compiler** or data-flow engine. **Drafts are not compiled**; every patch remains pending.” These cannot both be true in the current run. See [detail-18-planner-lede](screenshots/slides-layman-1/detail-18-planner-lede.png) and [detail-18-not-a-compiler](screenshots/slides-layman-1/detail-18-not-a-compiler.png).

3. **“Both gates” is undefined.** Which two? The deck has 10/11 human gates; slide 18 mentions “both gates agree” as if there are exactly two. Is it Guardian and Critic? Architect and Guardian? A viewer cannot tell.

4. **“10/11 human gates” is ambiguous.** It reads as “10 of 11,” which would mean only one gate is open; the slide means “Cascade 10 / Harbor 11” and all remain open. See [detail-18-title](screenshots/slides-layman-1/detail-18-title.png).

5. **The patch screenshot is unreadable.** `codebase-patches-1440x900.png` is displayed at 471 × 162 (33% scale); its UI text is ~4px. It adds visual texture, not evidence. See [slide 18, 1440](screenshots/slides-layman-1/1440/slide-18.png).

6. **There is a visible code typo.** The draft class is `VehicleRatingQueryQueryService` — a doubled “Query.” It may be intentional name composition, but without an explanation it reads as a typo. See [detail-18-queryqueryservice](screenshots/slides-layman-1/detail-18-queryqueryservice.png).

7. **The bottom correction block is a distraction.** The 10px “CDA correction” / “Servlet” paragraph corrects claims from elsewhere; it is important for accuracy but it is not part of the code-level story. It makes the slide feel like an errata page.

**Score: 4/10.** The before/after is a good teaching device; the slide's own claims and vocabulary undercut it. See [slide 18](../presentation/index.html#slide-18), [PDF page 18](screenshots/slides-layman-1/pdf-page-18.png).

**Fix:** Change the lede to: “Architect drafts patches; Guardian re-scans; Critic applies the displayed diff in a sandbox; Planner writes the codebase plan and seal. Nothing is compiled; compile validation is future work.” Add a 3-line SARIF explainer. Change the title to “Cascade 10 / Harbor 11 human gates remain open.” Fix `VehicleRatingQueryQueryService` or explain it. Move the CDA/servlet correction to speaker notes or a footnote.

---

### 2.7 Is the upgrade slide clear that the release scenario is simulated?

**Yes — this is the best-labeled boundary in the deck.**

Evidence on slide 19:

- Badge: **“5 SIMULATED SCENARIOS.”**
- Dark banner: “On detection: assessment generation 1 → 2 · previous green invalidated · affected patches identified · every patch still pending · **simulated release scenario, not a published 2027.04 release**.”
- Body: “PreFlight **simulates** five GWCP release changes …”
- Table first row: **“APD naming (simulated)”** and “24 → 20 characters.”
- Body: “The APD scenario reruns at its **simulated** 20-character limit; the other four remain `revalidation_required` until their drafts are fixed.”
- Footnote: “the 2027.04 release and the 20-character limit are PreFlight simulations, not published Guidewire release notes.”

I can explain: “This is a simulation of five possible release changes; the APD 24→20 limit is a simulated scenario, not a Guidewire announcement; all patches stay pending.”

What is less clear:

- **The table is not labeled as non-cumulative.** The Cascade rows are 2 + 3 + 7 + 14 + 4 = **30** affected patches; the Harbor rows are 2 + 3 + 6 + 14 + 3 = **28**. Slide 17 says Cascade has **22** patches and Harbor **21**. A layman who adds the column will think the counts contradict. The rows are alternative release scenarios, not simultaneous changes, but the slide never says “do not sum” or “each row is an independent scenario.” This is a real data-integrity trap.
- **`revalidation_required`, `rolled_back_to_checkpoint`, `resume_requested`, `upgrade_deferred` are machine states.** The slide explains the three resume choices in plain words; the table's “status recorded” column is readable, but the terms are not defined.
- **At 390, the resume-options table is broken.** “Re-run Architect with the new rule pack” wraps one or two words per line in a narrow “WHAT IT DOES” column; it looks like a rendering failure. See [detail-390-19-resume](screenshots/slides-layman-1/detail-390-19-resume.png).
- **The app screenshot is unreadable** at 610 × 144 (42% scale); the table and APD control carry the content.

**Score: 8/10.** The simulation is clear; the per-scenario table semantics and mobile layout are not. See [slide 19](../presentation/index.html#slide-19), [slide 19, 1440](screenshots/slides-layman-1/1440/slide-19.png), [slide 19, 390](screenshots/slides-layman-1/390/slide-19.png).

**Fix:** Add one line above the table: “Each row is an independent release change; affected-patch counts are not cumulative.” Make the resume table a stacked definition list at 390 (“Revalidate — re-run Architect with the new rule pack — `resume_requested`”).

---

## 3. Visual audit

### 3.1 Hierarchy and whitespace — 6/10

**The good:** There is a consistent slide grammar: small teal kicker → large two-line headline → gray lede → content. The headline is almost always the largest thing; the big numbers on slides 11, 15, and 17 are effective. Slides 13, 15, 16, and 23 have a clear focal point and a confident use of whitespace.

**The problem:** Several slides stop using the bottom third of the page, while others are packed edge to edge. The inconsistency reads as unfinished rather than deliberate:

- **Slide 2:** The four question cards end at ~530px; the bottom band is pinned at ~765px; the left column has a ~230px dead zone. [Screenshot](screenshots/slides-layman-1/1440/slide-02.png)
- **Slide 4:** The “WHAT EACH STAGE WRITES” grid has huge vertical gaps between rows (about 80–100px) and no stage numbers; the lower half looks like a spreadsheet with missing rows. [Screenshot](screenshots/slides-layman-1/1440/slide-04.png)
- **Slide 7:** The screenshot and right-hand table end around 690px; ~180px of blank canvas remains. The slide could enlarge the manifest table instead of leaving it small. [Screenshot](screenshots/slides-layman-1/1440/slide-07.png)
- **Slide 10:** The two assistant cards stretch to ~790px, but the screenshot + callouts inside end around 640px; there is ~150px of empty card. The cards look like empty containers. [Screenshot](screenshots/slides-layman-1/1440/slide-10.png)
- **Slide 20:** The 8-row table ends at ~550px; the bottom ~350px is blank except for the 10px security chips. This is the most visibly unfinished slide. [Screenshot](screenshots/slides-layman-1/1440/slide-20.png)
- **Slide 21:** The left “CLOSEST PRIOR ART” panel extends to ~850px with content ending at ~660px; the right column ends at ~620px. The lower half of the panel and the right side are empty. [Screenshot](screenshots/slides-layman-1/1440/slide-21.png)
- **Slide 22:** The right column ends at the verdict panel (~500px); ~350px of blank space remains below it, while the left kill-risk card extends to ~720px. [Screenshot](screenshots/slides-layman-1/1440/slide-22.png)

**Fix:** Either let panels hug their content, or add a deliberate sidebar/quote/“so what” element to fill the lower zone. Slide 20 would benefit from a short “what this means for the demo” callout; slide 21 from a larger table and a “why this matters” line; slide 10 from larger crops.

### 3.2 Density and typography — 4/10

The deck enforces a **10px floor** for supporting text. That is the problem: 10px is the floor, not a comfortable reading size. At 1440, labels such as “M3 LINKS + 30/30 SAMPLE,” “6 HIGH IMPACT,” “GATE / APPROVAL,” “REVIEW PACKET,” “NO LLM REQUIRED,” and the security chips are 10px. On a projector, they will be marginal; on a phone, they are small. A few decorative labels (agent step numbers, seal labels) compute at **9px**.

The body text is fine: the lede is ~14–16px, headlines 38–50px, card titles 15–20px. The problem is the **long tail of 10px labels and table text**, plus screenshots.

**Effective screenshot text** (source UI text ~11–13px multiplied by display scale; approximate):

| Slide | Image display scale | Approx. effective UI text | Result |
|---:|---:|---:|---|
| 6 | 0.67 | ~7–9px | Legible only if close; callouts compensate. |
| 7 | 0.67 | ~7–9px | Small; HTML table duplicates. |
| 8 | 0.67 | ~7–9px | Small; M-12 row missing. |
| 9 | 0.58 | ~6–7px | **Unreadable table; static “scroll” instruction.** |
| 12 | 0.69 | ~8px | Small; six HTML cards compensate. |
| 13 | 0.91 width, 170px strip | ~3–5px | Decorative strip; not evidence. |
| 14 | 0.47 | ~5px | Unreadable; table above is the content. |
| 15 | 0.57 | ~6px | Small; HTML tables are the content. |
| 16 | 0.42–0.47 | ~5px | Unreadable; remove or enlarge. |
| 17 | 1.08 but cropped | n/a | Outcome strips cut off. |
| 18 | 0.33 | ~4px | Unreadable; remove. |
| 19 | 0.42 | ~5px | Unreadable; remove or enlarge. |
| 10 | ~1.0 | ~11px | **The one demo screenshot that remains readable.** |

At **390**, the same images are displayed at ~250–358px wide, so the effective UI text is roughly **3–4px** on slides 6, 7, 8, 9, 12, 14, 15, 16, 17, 18, and 19. Only slide 10's assistant panels remain readable (they are ~347px crops displayed at ~358px). This is the single biggest mobile visual failure.

**Fix:** Use HTML for the data, not screenshots, at mobile. Hide or replace the desktop screenshots on 6, 7, 8, 9, 12, 13, 14, 15, 16, 17, 18, and 19 with a one-line summary or a tight, magnified crop. On 1440, keep only the screenshots that show something the HTML doesn't (slide 6's spine, slide 10's assistant output) and drop the decorative ones (16, 18, 19).

**Score: 4/10.**

### 3.3 Color — 8/10

The palette is consistent and purposeful: dark ink chrome, white paper cards, teal for structure, amber for warning/attention, red for reality boundary, green for success. The dark closing slide is a strong change of pace. Sampled contrast pairs pass AA (see measurements). Status is not color-only: gates have HIGH/MED text, the matrix has labels, findings have severity text, and the chart has numbers. The matrix's 6px gray dots are the only place where color is the primary carrier, and the labels underneath partly compensate. No change needed beyond a legend.

### 3.4 Charts and tables — 5/10

- **Slide 11 chart:** The 95% Wilson interval chart is readable at 1440: labels, dots, lines, and x-axis 50–100%. The chart legend explains the dot/line, and M6's no-interval state is labeled. The top metric labels are the weak point: “M3 LINKS + 30/30 SAMPLE” and “M5 ISSUES · 6/8 SLOTS” are compressed and ambiguous; “M6 F1 · 24 TP / 0 FP / 0 FN” is a wall of abbreviations. The slide's right-hand caveats are good but 10px. See [slide 11](screenshots/slides-layman-1/1440/slide-11.png).
- **Slide 3 matrix:** There is **no legend** for the teal/gray dots. The cell labels under “Review packet” are outputs (“findings,” “estimate,” “handover,” “issues”), not yes/no capability values, so the column mixes two semantics. The top chips look like filters but are static. See [detail-03-matrix](screenshots/slides-layman-1/detail-03-matrix.png).
- **Slide 9 findings table:** A static screenshot says “Scroll horizontally to see the remaining finding columns.” The “STANDARD” column is cut to “STA,” and only ~8 of 24 findings are visible. A deck/PDF cannot scroll. See [detail-09-static-scroll](screenshots/slides-layman-1/detail-09-static-scroll.png).
- **Slide 14 package table:** Clear at 1440; only one gate shown. At 390, the table is a 760px horizontal scroll region with no visible cue; the first columns are visible, the rest are not.
- **Slide 15/16 tables:** Clear at 1440; HTML, readable. Good.
- **Slide 19 table:** Clear at 1440; mobile scenario table is cramped but fits; the resume table is broken on mobile. The rows are not labeled non-cumulative.
- **Slide 20 table:** Clear at 1440; 8 rows; security chips are tiny.
- **Slide 21 prior-art table:** 10px text; at 390 the “What it establishes” column is ~3 words per line, making tall rows. Readable but slow.

**Fix:** Add a dot legend and separate “capability present” from “output type” on slide 3; replace slide 9's screenshot with an HTML table or a focused crop; make slide 19's rows explicitly non-cumulative; enlarge the 10px table text where possible.

### 3.5 Screenshot quality — 4/10

The assets are crisp and correctly sourced, but the **display sizes** are wrong for a slide deck. The deck uses 1440px app captures as small thumbnails; at 33–47% scale, the UI text is decorative, not readable. Specific failures:

- **Slide 9:** static scroll instruction; table clipped; 8 of 24 rows visible. [detail-09-static-scroll](screenshots/slides-layman-1/detail-09-static-scroll.png)
- **Slide 8:** the key M-12 rejected row is **below the crop**; the slide admits it and shows a schematic. The main evidence for the rejection is not in the screenshot. [slide 8](screenshots/slides-layman-1/1440/slide-08.png)
- **Slide 12:** the assumption register screenshot shows only A-01 while the slide says 4 assumptions; the caption admits the live register has four. The main image and the headline disagree at a glance. [slide 12](screenshots/slides-layman-1/1440/slide-12.png)
- **Slide 14:** caption says “the table shows the first 8 of 31” but the visible evidence table shows one row; the package table above is built from `migration.json`, not the screenshot. The caption is confusing and the screenshot doesn't earn its space. [detail-14-first8](screenshots/slides-layman-1/detail-14-first8.png)
- **Slide 17:** outcome strips cut; “APD conversion” vs “naming preparation” conflict. [detail-17-harbor](screenshots/slides-layman-1/detail-17-harbor.png)
- **Slide 18:** 33% scale; unreadable. [slide 18](screenshots/slides-layman-1/1440/slide-18.png)
- **Slide 19:** 42% scale; unreadable. [slide 19](screenshots/slides-layman-1/1440/slide-19.png)
- **Slide 13:** 170px-tall strip; the UI text is ~3–5px. The full app capture it comes from includes a **“How to read this page”** panel and a **“Glossary for a first-time reader (8 terms)”**; the slide's strip crops both out. The deck already has the explanation it needs in its own capture, but it is not shown. [slide 13](screenshots/slides-layman-1/1440/slide-13.png) · [full app capture](../presentation/assets/agents/migrator-loop-1440x900.png)
- **Slide 15/16:** the screenshots duplicate the HTML tables and are too small to add evidence. [slide 15](screenshots/slides-layman-1/1440/slide-15.png), [slide 16](screenshots/slides-layman-1/1440/slide-16.png)
- **Slide 10:** the two assistant crops are the exception: they are displayed near 1:1 and are readable. [slide 10](screenshots/slides-layman-1/1440/slide-10.png)

**Fix:** Apply a simple rule: if the UI text will render below ~9px, replace the screenshot with HTML or a focused crop. At 390, hide desktop screenshots entirely except slide 10's assistant output. Do not put instructions to scroll inside an image.

### 3.6 Consistency — 5/10

The visual system is consistent; the language is not. The same concepts appear under different names:

| Concept | Names used | Where | Risk |
|---|---|---|---|
| Feature review run | “straight handoff chain” / “five-agent cycle” / “loop” / “page calls it a loop” | Slides 13, 17; alt text; caption | The deck cannot decide the shape. |
| Fifth agent | **Scribe** (feature) / **Planner** (codebase) | Slides 13, 16, 17, 18 | No explanation of the change. |
| Harbor APD deliverable | “APD naming preparation” / “APD conversion” / “APN naming preparation” | Slide 17 badge, screenshot, boundary | Three labels; one likely typo. |
| Same 18/20 counts | “findings” / “blockers found” / “source blockers” | Slide 17 cards vs app crop | Looks like different measures. |
| 2 passes | “iterations” / “loop passes” / “two passes” | Slides 17, 18 | Minor, but adds noise. |
| 12 decisions | “dispositions” / “mappings” | Slides 8, 12, 14 | A judge may think 12 mappings and 12 dispositions are different. |
| 31 evidence | “evidence records” / “evidence links” | Slides 6, 13, 14 | Terminology drift; the number is the same. |
| 10 vs 11 gates | “10/11 human gates” | Slide 18 title | Reads as 10 of 11. |
| 3 vs 4 assumptions | “3 assumptions” / “4 assumptions” | Slides 13/15 vs 8/12 | Looks stale without a state label. |

**Score: 5/10.** The visual identity is strong; the nouns need a single glossary.

### 3.7 Animation / polish — 8/10

The deck is admirably restrained: no distracting slide transitions, a 0.22s progress-bar width transition, a 0.2s notes drawer, and a `prefers-reduced-motion` rule that disables all animation/transition. No auto-playing media, no parallax, no scroll-jacking. The only polish defect is the missing `favicon.ico` (console 404). The print/PDF has no animation, as expected. This category is not where the deck loses points.

### 3.8 Print / PDF — 6/10

**Good:** 23 pages, 1200 × 675.12 pt, 16:9, no chrome, all backgrounds, all 23 slides present, no page count mismatch. The PDF is a usable handout at a high level. Page 1 and page 23 carry the boundary; page 13 carries the reality boundary; page 17/19 carry their boundaries.

**Problems:**

1. **The footer disclaimer is removed.** Pages 14–16 and 20 have no visible “synthetic,” “not actual migration,” or “Official Cloud Assurance: not run.” Page 15 looks like a real Guardian run. See [PDF page 15](screenshots/slides-layman-1/pdf-page-15.png), [PDF page 20](screenshots/slides-layman-1/pdf-page-20.png).
2. **Slide 9's static scroll instruction and clipped table are in the PDF.** A print reader cannot scroll; the table is cut. See [PDF page 9](screenshots/slides-layman-1/pdf-page-09.png).
3. **Slide 17's cut-off figure is in the PDF.** The outcome strips are absent, and the “APD conversion” label remains. See [PDF page 17](screenshots/slides-layman-1/pdf-page-17.png).
4. **The PDF is untagged** (`Tagged: no`), so it has no reading order or alt text for assistive technology. The HTML deck is much better; the PDF is not equivalent.
5. **The whitespace problems remain** on pages 4, 20, and 21; the PDF does not reflow to use the space.

**Score: 6/10.** It prints; it does not fully carry the deck's honesty or legibility.

### 3.9 Accessibility / print — 6/10

**Strong:** semantic `<section>`/`h2` structure, `aria-label` on slides, `aria-live` slide announcements, a skip link, visible focus rings, `inert` closed notes panel, keyboard navigation, help dialog, focusable matrix scroll regions, reduced-motion support, alt text on all images, and contrast that passes AA in sampled pairs. The notes are 13px and readable. My keyboard focus test: Skip link → Notes → Help → PDF, then the body; the help dialog opens and traps focus as expected.

**Weak:**

- **Touch targets:** Notes 44×23, Help 38×23, PDF 36×23 at 390; below 44×44. The notes close button is 28×28.
- **Keyboard scroll:** the slide 18 code blocks have `overflow-x: auto` but no `tabindex`/role, so a keyboard-only user cannot scroll the clipped code. The slide 3/14 matrix scroll regions are focusable and labelled; good. The code blocks are not.
- **Mobile footer:** the persistent disclaimer is truncated, as above.
- **Mobile screenshots:** alt text describes the content, but the visual evidence is unreadable at 390.
- **PDF:** untagged; the printed handout lacks the boundary on key pages.
- **10px text:** the deck's own floor is small for a projected presentation; the 9px seal/step labels are below it.

**Score: 6/10.** The HTML deck is thoughtfully accessible; the mobile/PDF experience is not equivalent.

---

## 4. Data integrity

### 4.1 Count map

| Count | Meaning | Slides | Verdict |
|---|---|---|---|
| **300** | synthetic files | 1, 4, 6, 7, 13, 20 | Consistent. |
| **126** | evidence records / items | 1, 4, 12, 20 | Consistent; “records” vs “items” is a wording drift. |
| **8** | features traced | 1, 4, 12 | Consistent. |
| **24 / 8** | advisory findings / rules | 1, 4, 5, 9, 11, 13, 15 | Consistent; slide 9's visible table shows only ~8 findings, caption says 24. |
| **12** | dispositions (also called mappings); 5 are target changes | 1, 4, 8, 13, 14 | Consistent; “dispositions” vs “mappings” wording. |
| **5** | work packages / target files | 13, 14, 16 | Consistent. |
| **11** | human gates: 3 assumptions + 8 rule groups | 13, 15, 16 | Arithmetic consistent for the **seed** state; 3 vs 4 assumptions is unlabeled. |
| **7** | package-integrity checks | 13, 16 | Consistent. |
| **8** | bundle files: 5 + plan + report + 12-event log | 13, 16 | Consistent; manifest is a 9th wrapper. |
| **9 / 11** | seed / post-decision audit events | 1, 12, 16, 20 | Consistent; 12-event migrator log is a separate chain. |
| **18/22/2/10** | Cascade findings/patches/iterations/gates | 17, 18 | Consistent. |
| **20/21/2/11** | Harbor findings/patches/iterations/gates | 17, 18 | Consistent. |
| **16 / 13 / 15 / 18 / 20** | rule families / fired Cascade / fired Harbor / SARIF results Cascade / Harbor | 18 | Consistent. |
| **2/3/7/14/4** and **2/3/6/14/3** | affected patches per simulated release scenario | 19 | Consistent per row, but sums to 30/28 vs 22/21 totals; not labeled non-cumulative. |
| **481 / 18/18 / 0 / 9** | tests / freeze hashes / raw secrets / seed events | 20 | Consistent. |
| **7/10, 3/10, 8/10, 4/10, 6/10** | author's honest scorecard | 21 | Consistent with the labels and bar widths (verified). |

### 4.2 Arithmetic passes

The core counts are not fabricated or stale in the obvious sense. 3 + 8 = 11; 5 targets + plan + report + log = 8; 10 errors + 8 warnings = 18 findings, and 11 + 9 = 20; 24 findings = 8 rules × 3 per rule. The 2 + 3 + 7 + 14 + 4 = 30 and 2 + 3 + 6 + 14 + 3 = 28 rows are alternative scenarios, not a total. The count arithmetic is mostly disciplined.

### 4.3 Semantic failures / contradictions

1. **“Planner compiles” vs “not a compiler” vs “drafts are not compiled”** — slide 18. This is the clearest contradiction in the deck. It cannot be explained away as a conditional because the same slide says the output is a review bundle and SARIF, not a deployed change, and the bottom says “Drafts are not compiled.” If compile validation is future work (slide 22, roadmap item 07), the current run cannot compile. Fix the sentence.
2. **3 vs 4 assumptions** — slides 13/15 vs 8/12. The 11 gates are seed-state; the packet is post-decision. The deck must label the states. This is not a numeric error, but it is a reader-visible inconsistency in the most important count chain.
3. **“10/11 human gates”** — slide 18 title. Ambiguous between “10 of 11” and “Cascade 10 / Harbor 11.” The rest of the slide says Cascade 10 and Harbor 11, so the slash is the problem.
4. **Harbor “APD conversion” vs “APD naming preparation” vs “APN naming preparation”** — slide 17. The app screenshot and the slide badge/boundary disagree. The caption explains the app label, but the boundary typo “APN” adds a third term. This is a credibility issue, not just a wording preference.
5. **“The page calls it a loop; the feature path is a straight handoff chain”** — slide 13 caption; alt text says “five-agent cycle”; the screenshot shows a rework arrow. The deck is aware of the conflict and documents it instead of resolving it. A layman sees a loop, reads “chain,” and cannot tell which is authoritative.
6. **Slide 9 caption says “the 24 findings” but the visible table shows ~8; only the selected row and a subset are visible.** The caption/alt overclaim what the screenshot shows. The slide should say “8 of 24 shown; full list in packet.”
7. **Slide 12 caption says the crop shows A-01 while the live register has four assumptions.** The main image and the headline (“4 assumptions”) disagree at a glance; the caption is 10px. This is the same pattern as slide 9/17: the screenshot is not the thing the slide says it is.
8. **Slide 17 caption says the outcome strips are shown, but the `object-fit: cover` crop removes them.** The HTML cards carry the numbers, but the caption/alt are false.
9. **Slide 19 rows sum above the stated totals.** The table is per scenario, but a layman can add the column and get 30/28 vs 22/21. Add “not cumulative.”
10. **Slide 14 caption says “first 8 of 31” but the visible evidence table shows one row; the package table is built from `migration.json`, not the screenshot.** The caption is confusing and the screenshot doesn't support the table. The package table itself is the trustworthy source.
11. **Number collisions.** 24 findings vs 24 hard negatives; 8 rules vs 8 bundle files; 11 gates vs 11 audit events; 12 dispositions vs 12-event log; 5 packages vs 5 target files. Each is labelled, but the deck moves fast; a viewer can cross-wire them. A one-line “counts are different objects” legend or a recap table on slide 16 would help.
12. **“31 evidence records” (slide 6) vs “31 links” (slides 13/14).** Probably the same 31; the nouns differ. Use one term or say “31 evidence records / links.”
13. **“12 mappings” (slide 12) vs “12 dispositions” (slides 8/14).** Probably the same 12; define the synonym once.
14. **“blockers found” / “source blockers” (app crop) vs “findings” (slide 17).** Same counts, different nouns. If the app's “blocker” is a finding subtype, say so.
15. **“loop passes” / “iterations” / “passes.”** Same 2, three nouns. Pick one.

**Score: 5/10.** The deck is honest and the arithmetic is largely sound; the semantic contradictions are concentrated on the slides a judge will scrutinize most (13, 17, 18) and the state mismatch (3 vs 4) is easy to fix but currently material.

---

## 5. Mobile 390 audit

**Overall:** The HTML text reflows well. The layout is responsive, there is no horizontal page overflow, and the deck resets scroll to the top on slide change. But the deck becomes a long document (940–1891px per slide), and the visual evidence — the screenshots — does not survive the shrink.

One capture note: the full-page 390 screenshots show the fixed footer pinned mid-document. That is a full-page capture artifact, not a layout bug; in the viewport, the footer stays at the bottom. The real problems are that the footer's text is truncated and that the screenshots are unreadable, not that the footer permanently hides a particular line.

### 5.1 What works

- Headlines, ledes, and HTML tables reflow; no page-level horizontal scroll.
- The five-agent cards, gate table, and seal cards stack cleanly.
- Slide 10's assistant panels are readable (the only screenshots that survive at 390).
- Slide 11's chart is replaced by a readable mobile CI layout (the SVG is hidden; the numbers/labels remain).
- Notes open full-screen and are 13px/readable; the slide change resets `scrollY` to 0.
- Keyboard navigation still works; the matrix scroll regions are focusable and labelled.

### 5.2 What fails

1. **Screenshots are unreadable.** At 390, the 1440px UI captures are displayed at ~250–358px wide; effective text is ~3–4px. This affects slides 6, 7, 8, 9, 12, 13, 14, 15, 16, 17, 18, and 19. Slide 9's findings table and slide 19's upgrade screenshot are the worst. See [390 slide 9](screenshots/slides-layman-1/390/slide-09.png), [390 slide 18](screenshots/slides-layman-1/390/slide-18.png), [390 slide 19](screenshots/slides-layman-1/390/slide-19.png).
2. **The footer disclaimer is truncated.** “Synthetic estate · not affiliated with Guid…” is the persistent line; “Official Cloud Assurance: not run” is gone. See [detail-390-footer](screenshots/slides-layman-1/detail-390-footer.png).
3. **The resume-options table is broken.** The “WHAT IT DOES” column is narrower than the state column; “Re-run Architect with the new rule pack” wraps one or two words per line. See [detail-390-19-resume](screenshots/slides-layman-1/detail-390-19-resume.png).
4. **The slide 3/14 matrix tables are horizontal scroll regions with no visible cue.** The first column is visible; the rest are off-screen. The matrix is focusable and has an aria-label, but a touch user sees a clipped table, not a “swipe” hint. See [detail-390-matrix](screenshots/slides-layman-1/detail-390-matrix.png).
5. **The slide 18 code pane is horizontally clipped and has no scroll cue.** Lines such as the comment and class name are cut at the right edge; the fixed footer sits across the code in the viewport capture. The code block is not keyboard-focusable. See [detail-390-18-code](screenshots/slides-layman-1/detail-390-18-code.png).
6. **The slide 17 screenshot is a fragment.** It shows the top of the two case cards and none of the outcome strips; the HTML cards above are the only readable version. See [detail-390-17-shot](screenshots/slides-layman-1/detail-390-17-shot.png).
7. **Touch targets are 23px high** (Notes 44×23, Help 38×23, PDF 36×23). The notes close button is 28×28. Below the 44×44 guideline.
8. **The top chrome hides the section label** (`.chrome-mid` and `.deck-title` are hidden at ≤900px); the slide kicker still carries the section, but the global orientation is weaker.

### 5.3 Mobile verdict

The deck is **readable as text**, but **not as evidence**. If the deck is judged on a phone, the claims are carried by HTML summaries, not the screenshots. The footer truncation is the most serious content loss; the screenshot legibility is the most serious visual loss.

**Mobile score contribution:** typography/readability 4, visual hierarchy 6, accessibility/print 6, screenshot quality 4. A mobile-specific pass could raise the whole deck by a full point.

---

## 6. What works well

These are real strengths; the fixes should not erase them.

1. **The thesis is sharp.** “Evidence before the estimate” is memorable and consistent from slide 1 to slide 23. The closing “Every claim has evidence. Every unknown has a name. Every change waits for a human.” is excellent.
2. **The deck is honest.** The 95% intervals, “not a benchmark,” “no human IAA,” “research prototype,” “not viable as a standalone product,” and the Reversa prior-art concession build trust. It does not oversell.
3. **Slides 13, 15, and 16 are the clarity core.** The five-agent cards, the 3+8=11 gate arithmetic, and the 7 checks / 8 seals are the best-explained part of the deck.
4. **Slide 10 is the best demo explainer.** The refusal vs cited answer contrast is immediately understandable, and “Model off” is clear.
5. **Slide 19 is the best boundary-labeled slide.** “5 SIMULATED SCENARIOS” plus the dark banner plus the body/footnote make the simulation unmistakable.
6. **The visual system is coherent.** Teal/ink/amber/red/green, consistent card grammar, strong headlines, good contrast, no external assets, no distracting animation.
7. **The speaker notes are substantive and candid.** They contain the clearest version of the caveats and the correct shape of the feature/codebase loops. They are a great presenter aid; the deck should not depend on them for first-read clarity.
8. **The accessibility foundations are good.** Keyboard nav, skip link, aria labels, notes inert, reduced motion, focus rings, alt text, and a focusable mobile matrix.

---

## 7. Prioritized fixes

### P0 — fix before showing this to a lay audience

| # | Slide(s) | Issue | Fix |
|---:|---|---|---|
| P0-1 | 18 | “Planner compiles” vs “not a compiler” vs “drafts are not compiled”; `10/11` ambiguous; `VehicleRatingQueryQueryService` typo | Rewrite the lede to “Planner writes the codebase plan and seal; nothing is compiled; compile validation is future work.” Change the title to “Cascade 10 / Harbor 11 human gates remain open.” Fix the class name or explain it. Move the CDA/servlet correction to notes. |
| P0-2 | 13, 17, 18 | Scribe vs Planner unexplained; feature path called chain/cycle/loop | Add the two-column “feature packet loop (Scribe) / codebase patch loop (Planner)” comparison. Use “handoff chain” only for the feature path; “loop” only for the codebase rework. Update slide 13's caption/alt and the app screenshot text if possible. |
| P0-3 | 13, 15 vs 8, 12 | 3 assumptions vs 4 assumptions; 11 gates vs post-decision state | Add state chips: “Seed review — 9 audit events, 3 assumptions, 11 gates” vs “Post-decision packet — 11 audit events, 4 assumptions (A-DEC-04).” Say explicitly that the migrator run uses the seed state. |
| P0-4 | 17 | Harbor “APD conversion” vs “APD naming preparation”; “APN” typo; outcome strips cut | Replace the bottom screenshot with a clean crop of the two outcome strips, or remove it. Fix “APN” → “APD.” Add “naming preparation only, not conversion” next to the Harbor card. |
| P0-5 | 9 | Static screenshot says “Scroll horizontally”; table cut; only ~8 of 24 findings visible | Replace with an HTML table or a focused, legible crop; label “8 of 24 shown; full list in packet”; never put a scroll instruction inside a static image/PDF. |
| P0-6 | 390 + PDF | Footer truncation hides “Official Cloud Assurance: not run”; PDF drops footer entirely on pages 14–16/20; mobile screenshots unreadable | Make the boundary a persistent slide-content strip (or printed footer on every page), not chrome. At 390, hide/replace desktop screenshots on 6, 7, 8, 9, 12, 13, 14, 15, 16, 17, 18, 19 with HTML summaries or tight crops. |

### P1 — high-value comprehension and visual fixes

| # | Slide(s) | Issue | Fix |
|---:|---|---|---|
| P1-1 | 19 | Table rows sum to 30/28 vs 22/21 totals | Add “Each row is an independent release change; counts are not cumulative.” |
| P1-2 | 14 | 5 packages vs 11 gates not reconciled; only one gate in the package table | Add “Gates live at finding/rule-group level; this table shows the only package-level gate, G-03.” |
| P1-3 | 4 | “WHAT EACH STAGE WRITES” grid has no stage numbers and huge gaps; row/column reading ambiguous | Number the 9 items 01–09 or use a 9-row table; reduce the vertical gaps; repeat the slide 1 product sentence. |
| P1-4 | 3 | Matrix has no dot legend; “Review packet” cells mix capability with output type; chips look like filters | Add “● present / ○ absent” legend; move outputs to a separate note; style the chips as labels, not buttons. |
| P1-5 | 2, 7, 10, 20, 21, 22 | Dead zones (see §3.1) | Rebalance: enlarge the table/screenshot or add a short “so what” panel; do not leave 30–40% blank. |
| P1-6 | 11 | M1–M6 labels are terse; M3 has two denominators; M5 is 6/6 vs 6/8; M6 is abbreviation soup | Add a one-line plain-language metric legend; split M3 into “101/101 links” and “30/30 sample”; explain M5's 6/8 allowance; define TP/FP/FN. |
| P1-7 | 8, 12 | Key rows missing (M-12 below crop; A-01 only) while the headline says 4 assumptions | Use an HTML table or a capture that includes M-12 and all four assumptions; label “A-01 of 4” if the crop stays. |
| P1-8 | 15, 16 | Tiny screenshots duplicate the HTML tables | Remove the screenshots or enlarge to a single legible crop; let the tables and cards carry the slide. |
| P1-9 | deck-wide | APD, PCF, typelist, Gosu, SBT, CUE, CDA, GWCP, Qusar, SARIF, IAA, SME, LOB | Add a one-page glossary handout (not a 24th slide) and define each term at first use. Put the glossary link/notes in the deck. |
| P1-10 | order | Five-agent story arrives at slide 13 after 9 demo slides | Move a 20-second five-agent overview earlier (after slide 4) or add a one-slide “how the evidence is produced” bridge; keep the detailed 13–16 cards. |
| P1-11 | print | PDF untagged; no boundary on pages 14–16/20; page 9 scroll; page 17 cut | Add a printed boundary/footer on every page; export a tagged PDF; fix 9/17. |
| P1-12 | 390 | Resume table broken; code clipped; matrix no scroll cue | Stack the resume options as label/value pairs; make code blocks focusable with a “scroll” hint or wrap; add “swipe →” to matrix tables. |

### First 60 minutes (highest return)

1. Fix slide 18's lede/title: remove “Planner compiles,” say “Cascade 10 / Harbor 11,” fix `VehicleRatingQueryQueryService`.
2. Add the Scribe/Planner comparison and remove the “page calls it a loop” caveat from slide 13.
3. Add the seed/post-decision state chips to slides 13 and 15 (3 vs 4 assumptions).
4. Fix slide 17's `APN` → `APD` and remove or recrop the bottom screenshot.
5. Add “not cumulative” to slide 19.
6. Add the boundary line to the 390 footer/PDF pages and hide the unreadable screenshots at 390.

### P2 — polish

- Fix the favicon 404 (add a local favicon or remove the reference).
- Raise the 390 top-chrome buttons to ≥44px high; enlarge the notes close button.
- Make the slide 23 repository/deck references clickable links, or add a QR code; the current text is not clickable.
- Enlarge the closing disclaimer (10px) and repeat it in the pilot-ask box.
- Fix “Licence” vs “License” and the title slide's 2026-11-09 run date label (“run date,” not “deck date”).
- Add alt text that matches the visible crop on slides 9, 13, 17 (don't say “24 findings” if only 8 are shown; don't say “cycle” if the slide says “chain”; don't say “outcome strips” if they are cut).
- Consider making the “11 gates” and “7 checks” a single recap box on slide 16: “5 packages → 11 gates → 7 checks → 8 sealed files.”
- On slide 2, attribute the 6–8 week vendor estimate to a named source or label it as an industry observation; the rest of the slide is well-sourced.

### Acceptance tests for the next round

1. A lay viewer can answer the seven questions in §2 **without opening the speaker notes**.
2. Slide 18 contains no sentence that says the lab compiles and no sentence that says drafts are not compiled in the same run.
3. A viewer can state whether the 11 gates use 3 or 4 assumptions and why.
4. Every screenshot shown at 1440 has effective UI text ≥9px, or is replaced by HTML; at 390, no screenshot is below ~10px effective, or it is hidden.
5. The PDF has the synthetic/Cloud Assurance boundary on every page and is tagged.
6. The 390 footer shows the complete boundary, not “Guid…”.
7. A viewer can say “Scribe for feature packets; Planner for codebase patches; neither approves” after slides 13–18.
8. The 19 table is never read as 30/28 total patches.

---

## 8. Screenshot index

**Full sets**

- 1440 clean: `screenshots/slides-layman-1/1440/slide-01.png` … `slide-23.png`
- 1440 notes: `screenshots/slides-layman-1/1440/slide-01-notes.png` … `slide-23-notes.png`
- 390 viewport: `screenshots/slides-layman-1/390/slide-01.png` … `slide-23.png`
- 390 notes: `screenshots/slides-layman-1/390/slide-01-notes.png` … `slide-23-notes.png`
- 390 full page: `screenshots/slides-layman-1/390-full/slide-01-full.png` … `slide-23-full.png`
- Capture metrics/text: `deck-1440.json`, `deck-390.json`

**Key details**

- [Slide 3 matrix, no legend](screenshots/slides-layman-1/detail-03-matrix.png)
- [Slide 9 static “scroll” instruction](screenshots/slides-layman-1/detail-09-static-scroll.png)
- [Slide 13 loop/chain caption](screenshots/slides-layman-1/detail-13-loop-caption.png)
- [Slide 11 M5 “6/6 vs 6/8” metric](screenshots/slides-layman-1/detail-11-m5.png)
- [Slide 14 “first 8 of 31” caption](screenshots/slides-layman-1/detail-14-first8.png)
- [Slide 17 Harbor conversion/naming conflict](screenshots/slides-layman-1/detail-17-harbor.png)
- [Slide 17 “APN” boundary typo](screenshots/slides-layman-1/detail-17-apn-typo.png)
- [Slide 18 “Planner compiles”](screenshots/slides-layman-1/detail-18-planner-lede.png)
- [Slide 18 “not a compiler”](screenshots/slides-layman-1/detail-18-not-a-compiler.png)
- [Slide 18 `VehicleRatingQueryQueryService`](screenshots/slides-layman-1/detail-18-queryqueryservice.png)
- [Slide 18 `10/11` title](screenshots/slides-layman-1/detail-18-title.png)
- [Slide 19 390 resume table](screenshots/slides-layman-1/detail-390-19-resume.png)
- [Slide 18 390 code clipping](screenshots/slides-layman-1/detail-390-18-code.png)
- [Slide 17 390 screenshot fragment](screenshots/slides-layman-1/detail-390-17-shot.png)
- [390 footer truncation](screenshots/slides-layman-1/detail-390-footer.png)
- [390 matrix clipping/no cue](screenshots/slides-layman-1/detail-390-matrix.png)
- [PDF page 9](screenshots/slides-layman-1/pdf-page-09.png)
- [PDF page 15 (no boundary)](screenshots/slides-layman-1/pdf-page-15.png)
- [PDF page 17 (cut figure)](screenshots/slides-layman-1/pdf-page-17.png)
- [PDF page 18 (code/SARIF)](screenshots/slides-layman-1/pdf-page-18.png)
- [PDF page 20 (blank bottom)](screenshots/slides-layman-1/pdf-page-20.png)
- [PDF page 21 (blank panel)](screenshots/slides-layman-1/pdf-page-21.png)
- [PDF page 23 (disclaimer)](screenshots/slides-layman-1/pdf-page-23.png)

---

## 9. Limitations of this audit

- I used only the deck and its speaker notes; I did not use external Guidewire/APD/Gosu documentation. Some “jargon” complaints may be acceptable for a specialist audience; the brief was explicitly a layman.
- I did not run a screen-reader session (NVDA/VoiceOver), a color-blind simulation, or a full WCAG contrast scan. The accessibility findings are based on DOM/CSS, keyboard/focus tests, the PDF metadata, and sampled contrast.
- I did not test real touch hardware or iOS Safari; the 390 layout was tested in headless Chromium at 390 × 844.
- I did not edit the deck or app; the screenshots are from the running 8091 deck. The PDF is the packaged `docs/presentation/PreFlight-deck.pdf`.
- The 404 is a favicon request, not a content asset. All 17 slide images load.

**One-line summary:** The deck is honest, coherent, and visually confident; for a first-time lay viewer it is still a 5.8/10 because the fifth agent, the state of the 11 gates, the Harbor APD claim, and the code/SARIF story are not yet self-explanatory, and the mobile/print versions lose the evidence and the boundary.
