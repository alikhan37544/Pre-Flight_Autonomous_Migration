# PreFlight UX Round 1 — Independent No-Context Audit

**Run:** `R-DEMO-001`  
**App:** `http://127.0.0.1:8010`  
**Viewports:** 1440×900, 1280×720, 390×844  
**Method:** Playwright/Chromium, start at Home, then navigate only through visible UI. Full-page and viewport screenshots, console/page-error capture, DOM measurement, and axe-core 4.10.2 (WCAG 2.0/2.1 A/AA) scans. No product code or tests were edited; only this report and the screenshot directory were created. I did not submit any human decision; the decision dialog was opened and cancelled.

**Verdict:** PreFlight is a credible, unusually honest evidence-first demo once the viewer already understands Guidewire and the demo vocabulary. It is not self-explanatory from the home page. The strongest parts are the evidence drawer/assistant, the human-decision dialog, the migration-story counts, and the explicit “green is not approval” prose. The weakest parts are the product framing on Home, the Scribe-versus-Planner split across demos, the `/migrator` mobile tables, and several places where template/debug data leaks into the interface.

## Scorecard

| Category | Score | Why |
|---|---:|---|
| Product purpose | **4/10** | Home’s H1 is “Feature workbench” and its lede is about PCF/entity metadata/Gosu. The clear “what PreFlight is” paragraph exists only on About. A newcomer must already know Guidewire to understand the first screen. |
| Five-agent clarity | **5/10** | `/migrator` explains Scout, Architect, Guardian, Critic, and Scribe very well. But `/codebase` and `/case-studies` replace Scribe with Planner, and no page explains that the crews differ. There is no single canonical five-agent list. |
| Handoff clarity | **6/10** | The Received / Work / Produced columns, numbered handoff list, and “What just happened” paragraph are excellent. The explanatory “read this first” block is below the run controls and stage cards on `/migrator`; stage-card interactivity is not called out. |
| Gate / human-approval clarity | **5/10** | “Sealed means tamper-evident, not approved,” “Human approval required: yes,” and the decision dialog are strong. But case cards say only `green · gated`, Home says `succeeded`, and the 11 `/migrator` gates are not actionable and do not link to where a human records a decision. |
| Migration-story explainability | **6/10** | The two completed rehearsals and their counts are easy to compare. “Completed,” “green · gated,” “loop passes,” “iterations,” and “generation” are not consistently explained. |
| Evidence traceability | **6/10** | Workbench nodes, evidence drawer, assistant citations, and Findings/Reconstruction evidence cards are traceable. `/migrator`’s “Evidence handed to Architect” table has a blank Locator column, shows only 8 of 31 links, and provides no click-through. |
| Codebase-loop explainability | **6/10** | Iteration 1 and 2 are explicitly labelled, with the two Guardian failures and the two Critic fix requests that caused rework. Raw `target {'warning': 7}` / `target {}` data, `2 passs`, and inconsistent “deterministic” / “hybrid” Critic wording reduce trust and clarity. |
| Visual hierarchy | **5/10** | Strong panel/card language overall. Desktop pipeline labels are visibly clipped, 1280 page heads squeeze the lede into a narrow column, mobile panel heads stay two-column, and mobile evidence/package tables collapse into character-by-character wrapping. |
| Terminology / glossary | **4/10** | Good glossaries exist, but omit key terms and conflict with each other. Raw enums (`completed_with_gates`, `green_with_human_gates`, `mapped_transformed`), raw Python dicts, “MiMo,” “SBT,” “APD,” “seal,” “generation,” and “loop passes” remain unexplained on the page where they first appear. |
| Navigation | **5/10** | Sidebar grouping and breadcrumbs are useful. The PreFlight brand is not a link, nav labels do not match page titles, and mobile removes the group labels entirely. |
| Mobile / responsive | **3/10** | Page-level horizontal overflow is contained, but the two primary `/migrator` tables are effectively unreadable at 390px. `/codebase` is ~11,000px tall on a 390px screen. Controls and panel headers are cramped. |
| Accessibility | **5/10** | Skip link, focus rings, landmarks, labelled inputs, and scrollable-table regions are present; axe found no color-contrast failures. But `/migrator` has a critical ARIA violation on all five stage buttons and a serious non-focusable scrollable gate list. |

**Average: 4.9/10.**

## What a First-Time Viewer Can Actually Answer

| Question | Verdict | Where / why |
|---|---|---|
| What is the product? | **Partial** | Home says “Cloud-readiness review” and “Feature workbench.” It never states in one sentence that this is a local, synthetic, evidence-first cloud-readiness review for Guidewire-style legacy estates. About does say it clearly (“An offline, evidence-first cloud-readiness review product for Guidewire-style legacy estates. Independent research prototype.”), but About is not surfaced from the Home content. |
| What are the five agents and what does each do? | **Two different answers** | `/migrator`: Scout resolves feature/evidence, Architect drafts 5 packages, Guardian opens 11 gates, Critic runs 7 checks, Scribe seals 8 bundle files. `/codebase` and `/case-studies`: Scout, Architect, Guardian, Critic, **Planner**. No page says “the migrator uses Scribe; the codebase lab uses Planner.” |
| Can you find the completed dummy migrations and outcomes? | **Yes** | Migration stories → Cascade Mutual and Harbor P&C. Cascade: 18 blockers, 22 patches, 2 loop passes, 10 human gates. Harbor: 20 blockers, 21 patches, 2 loop passes, 11 human gates. Both are labelled synthetic and `green · gated`. Detailed iteration evidence requires “Explore the five-agent run.” |
| Can you distinguish machine-green from human approval? | **Yes with reading; no at a glance** | `/codebase` is explicit: “green · human gates open,” “Every patch remains pending human approval. Human approval required: yes.” `/migrator` says “sealed · gates open” and Scribe says “Sealing is not approval.” The Reconstruction/Findings decision dialog records a named acceptance. But Home says only `succeeded`; case cards say only `green · gated`; `/migrator` gates are labels, not actions. |
| Can you find the evidence behind a claim? | **Yes, but not everywhere** | Workbench: clicking an evidence node shows path, locator, excerpt, method, and excerpt SHA-256. The assistant’s “Long type?” answer cites `REV-0023` and its “Open evidence” link resolves to the evidence drawer. Findings → Inspect shows source file/line and excerpt. Failures: `/migrator`’s handoff table has no usable locators and no links. |
| On `/migrator`, can you follow Scout→Architect→Guardian→Critic→Scribe and understand 5 packages / 11 gates / 7 checks / seal? | **Yes on desktop; no on mobile** | The detail panels contain all four ideas: 5 work packages, 3 assumption gates + 8 rule groups = 11, 7/7 Critic checks, and Scribe’s 8-file sealed bundle. At 390px the Scout evidence table and Architect package table are not legible. |
| On `/codebase`, can you follow the 2 iterations and explain why 1 was red and 2 green? | **Yes, after reading the check lists** | Iteration 1 Guardian: 11/13, failing “every source finding has a patch” (10/18) and “target has no residual warnings” (7 warnings); Critic 4/7 with 2 fix requests. Iteration 2: Guardian 13/13 and Critic 7/7. The labels and check details are there, but raw template data and the `2 passs` typo undermine the explanation. |
| On `/case-studies`, can you compare Cascade and Harbor and find outcome counts? | **Yes** | Counts are in the first `case-outcome` strip of each card: Cascade 18 / 22 / 2 / 10; Harbor 20 / 21 / 2 / 11. Both show `green · gated`. |
| On `/settings`, can you understand how to enable live reasoning without seeing a key? | **Partial** | The page says live is configured, shows the endpoint host and models, explains that the key/base URL are environment-only, and the key never appears in the DOM. But there is no enable/disable control, no restart instruction, and the copy says both “Live mode is configured” and “Set PREFLIGHT_LLM_BASE_URL and PREFLIGHT_LLM_API_KEY in .env.” |

## Detailed Findings

### A. Product framing and Home

**F-01 — Home never says what PreFlight is (P1, `/`)**  
The first fold is brand tagline (“Cloud-readiness review”), H1 “Feature workbench,” and a paragraph beginning “One selected feature, traced across PCF, entity metadata, typelists…” A viewer who does not know Guidewire has no anchor. The clear product statement is only on `/about` (“An offline, evidence-first cloud-readiness review product for Guidewire-style legacy estates”). Add a one-sentence definition directly under the H1, before the evidence graph.  
Evidence: `home-1440x900.png`, `home-390x844.png`, `about-1440x900.png`.

**F-02 — The brand is not a home link (P1, global)**  
`.brand` is a `<div>`; clicking “PF” or “PreFlight” does nothing. On mobile the only route Home is Sections → Workbench. Make the brand a link to `/` (preserving the run query if appropriate).  
Selector: `.topbar .brand` in `app/templates/base.html`.

**F-03 — 1280px page heads squeeze the lede into a narrow column (P1, global)**  
At 1280px, `.head-meta` measures 526–577px while the `.lede` gets only 387–438px of a 1012px content area. The result is a tall, narrow paragraph with a large empty gap before the right-side badges. This reproduces on Home, Codebase, Migrator, Case studies, and Findings.  
Selectors: `.page-head`, `.page-head .head-meta`, `.page-head .lede`. The `@media (max-width: 1319px) { .head-meta { width: 100%; } }` rule is the direct cause in the row layout. Stack `.page-head` at the same breakpoint or remove the full width in row mode.  
Evidence: `home-1280x720-viewport.png`, `migrator-1280x720-viewport.png`, `case-studies-1280x720-viewport.png`.

**F-04 — “succeeded” on Home is not qualified as machine-only (P1, `/`)**  
The status pill and “Succeeded” dot read like final sign-off. There is no “human gates open” on Home, unlike `/codebase`. Add a second status line such as “Machine checks succeeded · human gates open” or link to the gate register.  
Selectors: `.head-meta .status-succeeded`, `.status-dot.status-succeeded`.

**F-05 — The 37 vs 24 stat is loud but unexplained and inert (P2, `/`)**  
`37 vs 24` appears in red under `LONG TYPE VS APD LIMIT`, but APD is not expanded on Home and the stat is not clickable. A first-time viewer sees a red number without knowing that it is a type-name length versus an API limit. The explanation is lower on the page. Link the stat to the `Estimate-moving signal` panel or add a short label such as “37-character type name / 24-character APD limit.”  
Selector: `.summary-strip .summary-signal`.

**F-06 — Home’s “at 1280px” caption is implementation copy (P2, `/`)**  
“Labels wrap so test nodes stay inside the graph at 1280px” is a layout/QA note, not a user-facing explanation. Replace it with “Labels wrap so the Tests column stays visible” or remove the viewport width.  
Selector: `.spine-caption`.

### B. Migrator (`/migrator`)

**F-07 — Pipeline role labels are clipped by the step-number badge (P0 visual)**  
At 1440px the cards visibly read “RESOLVE THE FEATURE AN [1] EVIDENCE,” “OPEN DETERMINISTIC RISI [3],” “VERIFY AND CHALLENGE T [4],” and “SEAL THE PLAN, REPORT, [5].” At 1280px it is worse. `.cycle-index` is absolutely positioned over text that does not reserve space. Reserve 24–28px on `.cycle-role` (or put the index in normal flow).  
Selectors: `.agent-cycle .cycle-stage`, `.agent-cycle .cycle-role`, `.agent-cycle .cycle-index`.  
Evidence: `migrator-pipeline-1440.png`, `migrator-1280x720-viewport.png`, `migrator-1440x900.png`.

**F-08 — Mobile Scout evidence table is unreadable (P0, 390px)**  
The table is 332px wide with no min-width. Every file path (`config/web/pcf/policy/PAVehicleDV.pcf`) and XML excerpt breaks at character boundaries across many lines. The `LOCATOR` column is a dash for every one of the eight rows even though the Workbench has xpath/pointer locators. There is no horizontal scroll hint and no “view all 31” link.  
Selectors: `#agent-stage-scout .table-scroll`, `#agent-stage-scout .table-scroll > table`. Template source uses `{{ item.line or '—' }}` rather than the full locator; the table is not wrapped by the `scroll_region` macro.  
Evidence: `migrator-stage-scout-390.png`; desktop version `migrator-stage-scout-1440.png`.

**F-09 — Mobile Architect package table collapses into vertical fragments (P0, 390px)**  
The package table has 332px of client width and 510px of table width, but the columns are crushed anyway: `WP-01` becomes four one-character lines, `mapped_transformed` splits mid-word, and the Evidence column is clipped at `EV-0…`. There is no table scroll cue. At 1440px, `WP-01` and `mapped_transformed` still wrap unnecessarily.  
Selectors: `#agent-stage-architect .table-scroll`, `#agent-stage-architect .table-scroll > table`. Add a minimum table width and a visible scroll hint, or switch to stacked package cards on narrow screens.  
Evidence: `migrator-stage-architect-390.png`, `migrator-stage-architect-1440.png`.

**F-10 — Evidence handoff is not actually traceable (P1, `/migrator`)**  
“Evidence handed to Architect” lists only the first 8 of 31 links. The Locator column is empty for all eight rows. The EVIDENCE IDs are plain text, not links. A viewer cannot open the evidence or see the remainder. Populate the full locator, make each row open the Workbench evidence drawer, and add “Open all 31 in Workbench.”  
Selector: `#agent-stage-scout .stage-artifact`; template `{{ item.line or '—' }}`. Full locators already exist in the Workbench evidence data (`xpath /PCF/Screen/TypeKeyInput[1]:4`).

**F-11 — “read this first” comes after the thing it explains (P1 hierarchy)**  
The `agent-explain` panel carries a `read this first` badge, but on `/migrator` it appears after the Agent crew controls, the five stage cards, and the stats strip. A newcomer can press Run/Replay before seeing any explanation. Move the explanation above the agent panel, or put a short “Start here” inline summary in the hero.  
Selector: `.agent-explain` following `.agent-loop-panel`.

**F-12 — Gate cards do not lead to a decision (P1)**  
Guardian opens 11 human gates and displays them, but the cards are read-only; owners are “unassigned” and there is no link to Reconstruction, Findings, or Review packet where a decision is actually recorded. The page says “human gates” but does not tell the viewer how to act. Add a primary “Review and decide” link to the gate section and link each gate to the relevant object.  
Selectors: `#agent-stage-guardian .gate-card`, `.gate-list`.

**F-13 — “Run live” is visually primary and has no disclosure in the active state (P1)**  
The current run panel has a teal `Run live · mimo-v2.6-flash` button next to Replay/Run again. Unlike the empty-state `.live-note`, the active state does not say that synthetic fixture text will be sent to the configured external endpoint. `Run live` is also not visually secondary. Add the same privacy note in the active state and/or require a confirmation before sending.  
Selector: `.agent-loop-actions [data-migration-live]`.

**F-14 — The replay controls do not bring the detail panel into view (P2)**  
Clicking a stage card invokes `showStage(..., { scroll: true })` and eventually scrolls to the active panel. Clicking Play/Next/Back/Reset calls `showStage` without scrolling. At the top of the page, the user sees the cards change but not the stage detail. Add `scroll: true` to the replay controls or make the active stage detail sticky.  
Selectors: `[data-replay-play]`, `[data-replay-next]`, `[data-replay-prev]`, `[data-replay-reset]`.

**F-15 — Raw status token and timestamp formatting (P2, `/migrator`)**  
The progress line shows `completed_with_gates · 100%`, and the meta line shows `2026-11-11T07:57:51Z → 2026-11-11T07:57:51Z` (identical start and end). Replace the machine token with “Completed with human gates” and show a readable duration (“completed in under a minute” or omit).  
Selectors: `.migration-progress-meta [data-migration-label]`, `.agent-loop-panel .panel-head .muted`.

**F-16 — Stage cards waste vertical space on mobile (P2, 390px)**  
Each card is 160px tall with a large empty gap between the agent name and the count/status. Five cards consume ~800px before the first detail panel. Reduce `min-height`/remove `margin-top: auto` for the count on narrow screens.  
Selector: `.agent-cycle .cycle-stage`.

### C. Codebase lab (`/codebase`)

**F-17 — Scribe and Planner are different “fifth agents” with no explanation (P0 cross-product)**  
Home’s demo path: “Scout → Architect → Guardian → Critic → **Scribe**.”  
`/migrator`: “Scout → Architect → Guardian → Critic → **Scribe**.”  
`/codebase` and `/case-studies`: “Scout → Architect → Guardian → Critic → **Planner**.”  
This is the single biggest vocabulary failure. If the difference is intentional (migration sealing versus codebase report compilation), say it explicitly and keep a canonical agent table. If not, unify the fifth role.  
Selectors: `.demo-path` on `/`; `.agent-hero .lede` and `.agent-cycle` on `/migrator`; `.agent-hero .lede` and `.agent-cycle` on `/codebase`; `.page-head .lede` on `/case-studies`.

**F-18 — `2 passs` typo (P1, `/codebase`)**  
The “Iterative patching” header renders “2 passs · the first pass is intentionally error-first.” This is a visible pluralization bug from `pluralize(result.iterations|length, 'pass')`. Use “passes” or a human label such as “2 loops.”  
Selector: the `.panel-head` containing `#iterations-heading`.

**F-19 — Raw Python dict in the iteration header (P1, `/codebase`)**  
Iteration 1 shows `target {'warning': 7}` and Iteration 2 shows `target {}`. This is raw template data, not user copy. Replace with “target severity: 7 warnings” / “no warning targets.”  
Selector: `.iteration-card header .muted` (renders `iteration.target.by_severity`).

**F-20 — “Critic 7/7 deterministic checks” conflicts with “Critic hybrid review” (P2, `/codebase`)**  
Iteration 2 says “Critic 7/7 deterministic checks passed,” but the lower panel is titled “Critic hybrid review,” and the page intro says Critic applies diffs and records risks. Clarify whether these are deterministic checks or hybrid review checks, and use one term consistently.  
Selectors: `.iteration-card .iteration-agent h3`, `.codebase-lower` panel headings.

**F-21 — Mobile source-findings table has no scroll cue and breaks IDs (P1, 390px)**  
`#cb-findings .table-scroll` is 332px wide against a 1180px table. IDs such as `CF-CODE-MSG-0001` wrap into four lines, `messaging` breaks, and the visible columns stop before Location/Message/Cloud target. There is no `.scroll-hint` because the table does not use the `scroll_region` macro and has no `data-table-scroll` hint. Add a visible hint and `white-space: nowrap` on IDs, or use cards.  
Selector: `#cb-findings .table-scroll`, `.codebase-table`.  
Evidence: `codebase-findings-table-390.png`.

**F-22 — “Live Critic” checkbox does not control the live run (P1)**  
The checkbox is labelled “Live Critic,” but the Run live handler sends `codebasePayload(true)` regardless of the checkbox state; the checkbox is not read. The separate model select also remains active when the checkbox is unchecked. A user can reasonably expect unchecked = offline, but gets a live run. Wire the checkbox to the payload or remove it and rename the button.  
Selectors: `.case-switcher [data-codebase-live]`, `.case-switcher [data-codebase-live-run]`.

**F-23 — The codebase live path has no external-data disclosure (P1)**  
Unlike the empty-state launch panel on `/migrator`, the `/codebase` top controls provide no note that live mode sends synthetic fixture text to an external endpoint. Add a compact `.live-note` beside “Run live” and make it part of the confirmation.  
Selector: `.case-switcher` near `[data-codebase-live-run]`.

**F-24 — `green_with_human_gates` is a raw enum in the outcome (P2)**  
The explain block shows `green_with_human_gates · 18 findings · 22 patches · 2 iterations · 10 human gates`. The first token is internal data. Use “Machine green; human gates open” and keep the human gate count prominent.  
Selector: `.agent-explain .explain-grid strong`.

**F-25 — “generation” and “loop passes/iterations” are undefined (P2)**  
The hero shows `generation 1`; the summary uses “loop iterations”; the case cards use “loop passes”; the iteration heading says “passs.” Add these to the glossary or remove the distinction.  
Selectors: `.head-meta`, `.summary-strip`, `.iteration-card`, `article.case-card .case-outcome`.

**F-26 — Codebase page is 11,058px tall at 390px (P2 mobile)**  
The page stacks hero, narrative, summary, cyclic crew, agent cards, inventory, iterations, Guardian/Critic panels, findings, patches, gates, upgrade resilience, and decision dialog. Tabs only control some of that; scrolling to the right section is laborious. Add a sticky tab/section jump bar on mobile or collapse secondary sections.

### D. Case studies (`/case-studies`)

**F-27 — `green · gated` is the only status badge and looks like approval (P1)**  
Cascade and Harbor each show `green · gated` in the outcome strip. The explanatory text says “human gates that remain after the machine gates are green,” but the badge itself gives no “machine” or “10/11 human gates” cue. Change it to “Machine green · 10 human gates open” or add the gate count to the badge.  
Selector: `article.case-card .case-outcome .pill`.

**F-28 — Outcome labels are inconsistent with the codebase lab (P1)**  
Case studies: “loop passes”; `/codebase`: “loop iterations”; `/migrator`: “five-agent loop”; `/codebase` hero: “generation 1.” A newcomer cannot tell whether these are the same unit. Pick one (recommended: “iterations”) and use it everywhere.

**F-29 — “Completed” reads as approved (P2)**  
H1 “Two completed migrations you can explore” plus `green · gated` can imply done and signed off. The lede says “completed five-agent rehearsal,” which is better, but the H1 should include “rehearsal” or “drafts complete; human gates open.”  
Selector: `.page-head h1`.

**F-30 — Large blank column under the shorter Cascade card (P2 visual, 1440px)**  
The two case cards share a CSS grid row, so Cascade’s shorter content leaves a large empty region under it while Harbor continues. This is not a functional bug, but it weakens comparison. Consider independent column flow/masonry or aligning outcome/facts and letting the narrative follow.

### E. Settings and live reasoning (`/settings`)

**F-31 — “Live mode is configured” and “Set … in .env” are contradictory (P1)**  
The page says `Mode live`, `configured`, “Live mode is configured. The key and base URL are read only from the environment,” then immediately instructs “Set PREFLIGHT_LLM_BASE_URL and PREFLIGHT_LLM_API_KEY in .env.” A newcomer cannot tell whether they still need to do something, whether a restart is required, or whether live is currently active. Rewrite as a status plus instructions for changing it:
- “Live reasoning is enabled via environment variables in `.env`. No key is shown here.”
- “To enable: set … and restart the local server. To disable: remove/unset …. ”
- Show a clear `Enabled/Disabled` status separate from “Optional live reasoning.”
Selector: `section[aria-labelledby='reasoning-settings']`.

**F-32 — There is no enable/disable control despite the instruction framing (P1)**  
The only control is “Test connection.” A user cannot enable or disable live reasoning from Settings. If env-only is deliberate, label the section “Configuration (environment only)” and remove any implication of an interactive toggle.  
Selector: `[data-llm-check]`.

**F-33 — “MiMo” and model names are unexplained (P2)**  
“MiMo / OpenAI-compatible endpoint,” `mimo-v2.6-flash`, and `mimo-v2.6-pro` are technical names with no expansion or one-line explanation. Add “MiMo is the configured model provider” and explain the default choice.  
Selector: `section[aria-labelledby='reasoning-settings'] h2`.

**F-34 — Test-connection result is low-prominence and wraps on mobile (P3)**  
The result is a small inline string to the right of the button (`OK · mimo-v2.6-flash · 2948 ms`); on 390px “ms” wraps to a second line. It is a `role=status` (good), but the success/failure state should be more visible and include the checked host.  
Selector: `[data-llm-check-status]`.

**Strength — no key exposed (not a finding)**  
The Settings DOM contains no populated secret inputs and no key literal; the endpoint host and model names are visible, but the key is not. I did not reproduce any key in this report or screenshots. This directly satisfies the “without seeing a key” constraint.

### F. Workbench / evidence / findings / reconstruction

**F-35 — Evidence traceability is strong on Workbench (strength)**  
Clicking `EV-0001` in the spine produces a drawer with path, xpath locator, exact excerpt, method, and excerpt SHA-256. The assistant’s Long-type answer cites `REV-0023`; “Open evidence” navigates to a valid Workbench evidence drawer with the source `product/template/LongTypeA.xml` and excerpt. This is the best evidence flow in the product.  
Evidence: `workbench-drawer-1440.png`, `workbench-assistant-1440.png`, `workbench-REV0023-drawer-1440.png`.

**F-36 — Evidence table on `/migrator` undercuts that strength (P1)**  
See F-10. The blank Locator column is especially damaging because the adjacent Workbench demonstrates that the locator exists.

**F-37 — Active feature/case states are visual only (P2 accessibility)**  
`.feature-row.selected` and `.case-chip.active` use classes without `aria-current`. A screen-reader user cannot tell which feature or migration story is selected. Add `aria-current="page"` (case chip) / `aria-current="true"` or `aria-selected` with an appropriate group role (feature list).  
Selectors: `a.feature-row.selected`, `a.case-chip.active`.

**F-38 — Mapping table source/target identifiers break mid-word at 1440 (P2 readability)**  
`PersonalAutoRatingFactorConfiguration` becomes `PersonalAutoRatingFac` / `torConfiguration`; `PersonalVehicle.VehicleType` becomes `PersonalVehicle.Vehic` / `leType`. The table is readable but forces the eye to reconstruct identifiers. Allow horizontal overflow for the source/target columns or use a stacked detail row.  
Selector: `.mapping-table td code`.

**F-39 — Mobile Reconstruction hides target/provenance while showing pinned decisions (P2)**  
At 390px, the mapping table shows ID, Source, and a sticky Decision column; Target, Disposition, Rule, and Provenance are offscreen. A user can press Accept/Reject without seeing the target. The modal does show `PAVehicle → PersonalVehicle`, which partly rescues this, but the table should not present decisions without visible context.  
Selectors: `.mapping-table .actions-col`, `.mapping-table`, `[data-decision]`.

**F-40 — Decision dialog is clear and accessible (strength)**  
“Accept mapping M-01” shows the source→target, consequence (“This records acceptance in the audit trail. No assumption is created.”), a required reason, and “Record acceptance.” The buttons have specific aria-labels (e.g. “Accept mapping M-01 PAVehicle to PersonalVehicle”). I opened and cancelled the dialog; no decision was recorded.  
Evidence: `reconstruction-decision-dialog-390.png`.

### G. Other review pages

**F-41 — Manifest SIZE has no unit and hashes wrap heavily (P2, `/manifest`)**  
The table header says `SIZE` with values like 267, 19, 213; it is presumably bytes but not stated. SHA-256 values break across two/three lines. Add “Size (bytes)” and consider a monospace/nowrap hash column or copy-on-click.  
Selector: `.manifest-table`.

**F-42 — Evaluation is full of undefined metric abbreviations (P2, `/evaluation`)**  
`M1`–`M6`, `F1`, `TP/FP/FN`, “micro-F1,” “top-8 allowance,” “hard negatives silent,” and “SBT” are not explained on the page. The page is rigorous but assumes a metrics-literate reader. Add a collapsible metric legend or link to the evaluation doc.  
Selectors: `.summary-strip`, `.metric-card`, `.margin-table`.

**F-43 — About page does the product-definition job well (strength)**  
“What it is / What it is not,” claim legend, claim strength, and the full disclaimer are clear. It is just not discoverable enough from Home. Link “What is PreFlight?” from the Home hero to About.  
Evidence: `about-1440x900.png`.

### H. Accessibility and console

**F-44 — Critical ARIA violation on all five `/migrator` stage buttons (P0 accessibility)**  
axe: `aria-allowed-attr` (critical), 5 nodes `.cycle-scout`, `.cycle-architect`, `.cycle-guardian`, `.cycle-critic`, `.cycle-scribe`. The elements are `<button role="listitem" aria-pressed="...">`; `aria-pressed` is not allowed on `listitem`, and the button role is effectively overridden. Screen-reader users will not hear these as the interactive stage controls they visually are.  
Fix: use `<div role="listitem"><button aria-current="step">…</button></div>` or remove `role="listitem"` and use `aria-current` on a real button. Keep the button name/state specific.  
Selector: `.agent-cycle .cycle-stage`.

**F-45 — Serious non-focusable scrollable gate list (P1 accessibility)**  
axe: `scrollable-region-focusable` (serious), one node `.gate-list` when Guardian is active. `.gate-list.compact` has `max-height: 360px; overflow: auto` but no `tabindex`. Keyboard-only users cannot scroll the assumption cards. Add `tabindex="0"`, an accessible label, and a focus-visible ring; or remove the fixed height.  
Selector: `#agent-stage-guardian .gate-list.compact`.

**F-46 — Codebase tabs do not implement the expected tab keyboard pattern (P2 accessibility)**  
`role="tablist"` with five `role="tab"` buttons; all five have `tabIndex=0`, and there is no arrow-key roving focus (unlike the generic tab handler used elsewhere). Use roving tabindex (selected `0`, others `-1`) and Left/Right/Home/End handlers, or use ordinary navigation buttons without tab roles.  
Selector: `[data-codebase-tabs] [role="tab"]`.

**F-47 — Small chip targets and 10px labels (P2 accessibility/readability)**  
Assistant prompt chips measure ~23px high; `.eyebrow`, `.summary-label`, `.outcome-label`, `.cycle-role`, and `.seal-label` are 10px uppercase with letter spacing. This is hard to read on 390px and below the 24px target-size recommendation for chips. Increase body/label scale and chip height slightly.

**F-48 — No console errors or page errors observed (strength)**  
Across `/`, `/migrator`, `/codebase`, `/case-studies`, `/settings`, `/manifest`, `/reconstruction`, `/findings`, `/evaluation`, `/packet`, `/runs`, `/about` at all three viewports, browser console had no errors/warnings and no unhandled page errors. No page-level horizontal scrollbar appeared; wide tables/SVG were contained in scroll regions.  
In the pages and states scanned with axe (`/`, `/migrator`, `/codebase`, `/case-studies`, `/settings`, `/reconstruction`, `/findings`, plus the codebase tabs and reconstruction dialog), the only violations were F-44 and F-45. Color contrast passed the axe WCAG A/AA checks.

## Prioritized Fix List

### P0 — fix before calling this demo self-explanatory

1. **Make `/migrator` evidence and package tables usable on 390px.**  
   Pages: `/migrator`. Selectors: `#agent-stage-scout .table-scroll > table`, `#agent-stage-architect .table-scroll > table`, `.table-scroll`. Add a minimum table width (`min-width: 760px` for the scout table, `min-width: 720px` for packages), add `data-table-scroll` + a visible scroll hint, and prefer stacked rows under 600px. Do not rely on `overflow-wrap: anywhere` for file paths and XML.  
   Why: this is the core evidence/work-package story, and at 390px it is effectively unreadable.

2. **Fix the clipped `.cycle-role` labels on `/migrator`.**  
   Selectors: `.agent-cycle .cycle-role`, `.agent-cycle .cycle-index`. Reserve horizontal space for the index (or put it in flow). Verify at 1280 and 1440 widths.

3. **Fix the invalid stage-button ARIA.**  
   Selector: `.agent-cycle .cycle-stage` in `app/templates/migrator.html`. Remove `role="listitem"` from the button or restructure as list items containing buttons; replace `aria-pressed` with an appropriate step state such as `aria-current="step"`. Add a regression axe check.

4. **State the canonical five-agent model everywhere.**  
   Pages: `/`, `/migrator`, `/codebase`, `/case-studies`. Selectors: `.demo-path`, `.agent-hero .lede`, `.agent-cycle`, `.page-head .lede`. Either unify Scribe/Planner or add a visible “Two crews” note and a shared agent glossary. This directly answers the product’s central question.

5. **Add the one-sentence product definition to Home and make the brand a Home link.**  
   Pages: `/`; selectors: `.page-head h1`/`.lede` and `.topbar .brand`. Suggested copy: “PreFlight is an offline, evidence-first cloud-readiness review for Guidewire-style legacy estates. It traces every claim to evidence, drafts cloud targets, and leaves every change for human approval.”

### P1 — high-impact clarity, trust, and responsive fixes

6. **Populate the `/migrator` evidence locators and add a way to open all 31 links.**  
   Selector: `#agent-stage-scout .stage-artifact`; replace `{{ item.line or '—' }}` with the full locator and add a Workbench link. This fixes the sharpest evidence-traceability gap.

7. **Fix the 1280px page-head squeeze.**  
   Selector: `.page-head .head-meta` (global). At 1280px, it takes 526–577px and leaves the lede 387–438px. Stack `.page-head` at the same breakpoint or remove `width: 100%` in row mode. Verify Home, Codebase, Migrator, Case studies, Findings.

8. **Remove raw template/debug output from `/codebase`.**  
   Selectors: `.iteration-card header .muted` (`target {'warning': 7}` / `target {}`) and the `#iterations-heading` `.panel-head` (“2 passs”). Also humanize `green_with_human_gates`. This affects trust more than aesthetics; a research prototype that leaks a Python dict looks unfinished.

9. **Fix the `/codebase` live-run semantics and disclosure.**  
   Selectors: `.case-switcher [data-codebase-live]`, `[data-codebase-live-run]`, `.agent-loop-actions [data-migration-live]`. Wire the checkbox to the run payload or remove it; add a concise external-data note beside every live button; label the action “Send synthetic fixture text to the configured model.” Consider making live a secondary action.

10. **Add scroll cues and ID nowrap to the codebase source-findings table.**  
    Selectors: `#cb-findings .table-scroll`, `.codebase-table`. At 390px the table is 1180px wide with no hint and IDs wrap into four lines. Add `data-table-scroll`/`.scroll-hint` and `white-space: nowrap` for `code` IDs, or card-stack the rows.

11. **Make the case-study status badge say “machine green.”**  
    Selector: `article.case-card .case-outcome .pill`. Current `green · gated` reads as an approval badge. Use `Machine green · 10 human gates open` (and 11 for Harbor) or add that count to the badge.

12. **Clarify Settings’ enable/disable story.**  
    Selector: `section[aria-labelledby='reasoning-settings']`. Separate status from instructions, state that the key is environment-only, state that a server restart is required after changing `.env`, and add a visible Enabled/Disabled status. Remove the contradiction between “configured” and “Set … in .env.”

13. **Keep mobile navigation grouping.**  
    Selectors: `.side-label` (hidden by `.side-label, .side-foot { display:none; }` under 980px), `.nav-toggle`. The two-column mobile menu flattens Agent demo, Review, and Workspace into one undifferentiated block. Retain group labels or insert visible separators; keep the close state discoverable (it currently changes the hint to “Close,” which is good).

14. **Stack `.panel-head` on narrow screens.**  
    Selectors: `.panel-head` (global), especially the “What just happened” panel and `#iterations-heading` panel. At 390px the title and right-side note share a cramped row; “What just happened” wraps into two lines while “the whole handoff in one paragraph” occupies the side column. Use `flex-wrap: wrap` or `flex-direction: column; align-items: flex-start`.

15. **Reduce the mobile stage-card blank space and replay disconnection.**  
    Selectors: `.agent-cycle .cycle-stage`; `[data-replay-play]`, `[data-replay-next]`, `[data-replay-prev]`. Remove the fixed 132px min-height on small screens, and make replay controls scroll/focus the active `.agent-stage-detail`.

### P2 — polish, terminology, and accessibility follow-up

16. **Add missing glossary terms and use one unit of progress.**  
    Add: generation, iteration/loop pass, package, gate, Scribe, Planner, machine green, human gate, live reasoning, SBT, claim strength, SARIF. Use “iterations” everywhere instead of “loop passes.”

17. **Fix active-state semantics.**  
    Add `aria-current` to `.case-chip.active` and decide the right `aria-current`/`aria-selected` model for `a.feature-row.selected`; the visual selection currently has no accessible equivalent.

18. **Fix the gate list keyboard trap.**  
    Selectors: `#agent-stage-guardian .gate-list.compact`; add `tabindex="0"` and an accessible label, or remove the internal scroll. This is a serious axe finding.

19. **Fix the codebase tab pattern.**  
    Selector: `[data-codebase-tabs] [role="tab"]`; implement roving tabindex and arrow keys, or use normal buttons without tab roles.

20. **Increase target/label size.**  
    Selectors: `.chip` (23px high), `.eyebrow`, `.summary-label`, `.outcome-label`, `.cycle-role`, `.seal-label` (10px). Improve readability on 390px; 24px is the WCAG 2.2 target-size baseline.

21. **Make the 37 vs 24 stat self-explanatory and link it to the explanation.**  
    Selector: `.summary-strip .summary-signal` on `/`. Add “37-char type vs 24-char APD limit” and link to the long-type signal/Reconstruction section.

22. **Replace the 1280px caption with user copy.**  
    Selector: `.spine-caption` on `/`: remove “at 1280px.”

23. **Make the test-connection result more prominent.**  
    Selector: `[data-llm-check-status]` on `/settings`: include host and state (“Connected to host · 1.8s”) and expose failure guidance. Keep the `role=status` success announcement.

24. **Clarify the Manifest SIZE column.**  
    Selector: `.manifest-table`: use “Size (bytes)” and prevent hash values from becoming unreadable multi-line strings.

25. **Add an Evaluation metric legend.**  
    Selector: `/evaluation` `.summary-strip` and metric cards: define M1–M6, F1, TP/FP/FN, recall/precision, and “top-8 allowance.”

## Strengths Worth Preserving

- **Honesty is designed into the chrome.** “Synthetic estate,” “Local-only,” and “Official Cloud Assurance: not run” are persistent and visible at every viewport.
- **Human approval is stated repeatedly and specifically.** The `/codebase` banner (“Every patch remains pending human approval. Human approval required: yes.”), Scribe’s “Sealing is not approval,” and the Reconstruction decision dialog are strong.
- **The evidence graph is genuinely interactive.** Keyboard activation works, the selected node is outlined, the evidence drawer contains a real source excerpt and hash, and there is a table fallback.
- **The assistant is grounded and refuses unsupported claims.** The Long-type answer cites `REV-0023` and the “Open evidence” link resolves.
- **The five `/migrator` stage panels use a consistent Received / Work / Produced structure.** Guardian’s “Deliberately not received” box is a particularly good way to explain bounded autonomy.
- **Case-study counts are prominent and directly comparable.**
- **No console or page errors were observed.** The app is stable across the tested flows.

## Screenshot Index

All screenshots are in `docs/audits/screenshots/ux-round1/`. Key evidence:

| File | What it shows |
|---|---|
| `home-1440x900.png`, `home-1280x720-viewport.png`, `home-390x844.png` | Product framing, 1280 squeeze, mobile fold |
| `home-mobile-nav-open-390.png` | Mobile navigation without group labels |
| `migrator-1440x900.png`, `migrator-1280x720-viewport.png`, `migrator-390x844-viewport.png` | Migrator hero and pipeline |
| `migrator-pipeline-1440.png` | Clipped `.cycle-role` labels |
| `migrator-stage-scout-390.png` | Unreadable mobile evidence table |
| `migrator-stage-architect-390.png` | Crushed mobile package table |
| `migrator-stage-guardian-1440.png`, `migrator-stage-critic-1440.png`, `migrator-stage-scribe-1440.png` | 11 gates, 7 checks, seal |
| `codebase-1440x900.png`, `codebase-1280x720-viewport.png`, `codebase-390x844-viewport.png` | Codebase hero/controls |
| `codebase-iterations-1440.png`, `codebase-iterations-390.png` | Iteration 1/2 story and raw data |
| `codebase-findings-table-390.png` | Mobile source-findings table failure |
| `case-studies-1440x900.png`, `case-cascade-outcome-1440.png`, `case-harbor-outcome-1440.png` | Story comparison and counts |
| `settings-1440x900.png`, `settings-live-panel-390.png`, `settings-test-connection-after.png` | Live reasoning, no visible key, test result |
| `workbench-drawer-1440.png`, `workbench-assistant-1440.png`, `workbench-REV0023-drawer-1440.png` | Evidence traceability strengths |
| `reconstruction-table-390.png`, `reconstruction-decision-dialog-390.png` | Mobile mapping context and human decision dialog |
| `findings-1440x900.png`, `findings-table-390.png`, `findings-detail-390.png` | Findings density and mobile detail |

## Method and Limitations

- The app was already running on `127.0.0.1:8010`; the server was restarted once after it stopped during the audit. No product source or data was edited, and no human decision was recorded.
- I did not run live model reasoning. Settings reports it as configured; I verified that the key is not present in the Settings DOM or screenshots and that “Test connection” returns an OK status with model and latency.
- axe-core results are automated; they do not replace a full screen-reader walkthrough. The manual checks covered keyboard focus, aria labels, scroll regions, and visible content order.
- The report intentionally omits any API key or secret; no key value is present in the screenshots or in this file.
- This is a harsh first-time/no-context score. It is not a statement that the prototype is low quality; the evidence model and human-approval discipline are strong. The score reflects how much explanation a new viewer needs before those strengths become visible.
