# PreFlight — Accessibility + Visual QA, Round 2

**Audited:** 11 November 2026 · `http://127.0.0.1:8010` · run `R-DEMO-001`  
**Viewports:** 1920×1080, 1440×900, 1280×720, 1024×768, 390×844  
**Method:** Playwright/Chromium (`chromium-1254`), axe-core 4.10.2, DOM measurement, computed-style checks, manual keyboard walks, contrast sampling, reduced-motion emulation, and interaction tests. axe was injected through CDP because the app’s CSP (`script-src 'self'`) correctly blocks injected `<script>` tags.  
**Constraint:** No product code or tests were edited. This report and 166 screenshots under `docs/audits/screenshots/a11y-round2/` are the only additions.  
**Coverage:** 35 page/viewport loads, 25 `/migrator` stage states, 50 `/codebase` tab states (2 cases × 5 tabs × 5 viewports), 5 upgrade-impact states, replay, mobile navigation, and keyboard focus order.

## Verdict

PreFlight is still a visually disciplined prototype with unusually good keyboard fundamentals for its size: all visible controls on every page tested at 1440 are keyboard-reachable (plus the 390px mobile nav), the skip link works, the mobile menu is operable, the old stage-button ARIA conflict is gone, and reduced-motion handling is complete. It also renders with **zero console errors, zero page errors, and zero failed requests** across every base page, tab, stage, upgrade, replay, and navigation state tested.

It is **not** ready to call responsive at the required viewports. At 1024px, `/codebase` overflows by 74–96px and `/case-studies` by 51px; case-study outcome labels visibly collide, and a case-study badge is clipped. The `/codebase` tab strip is operable with Tab + Enter/Space, but it does not implement the ARIA tab keyboard model and its panels are unnamed. The 1280px page-head squeeze, replay controls that change an off-screen detail panel, and mobile findings table remain unfinished. I would not sign off the accessibility or responsive-layout portions yet.

## Scorecard

| Area | Score | Why |
|---|---:|---|
| Accessibility semantics | **6/10** | Strong H1/label/landmark basics and no critical axe violations, but tabs are incomplete, stage-card subheads skip from H2 to H4, four core tables lack captions, and selected case/feature rows are visual-only. |
| Keyboard / focus | **7/10** | Every visible control reached at 1440; mobile nav, skip link, stage buttons, gate list, and tabs all keyboard-operable. Deductions: tabs are five Tab stops with no arrow navigation, replay changes an off-screen panel without scrolling or focusing it, and the home graph’s scroll region is not focusable. |
| Color / contrast | **8/10** | All sampled text meets 4.5:1; the lowest is 4.72:1. Deductions: that margin is only 0.22, and the focus ring on the dark topbar is 1.70:1. |
| Responsive layout | **4/10** | 30/35 base loads are clean, but 1024px breaks three page variants, 1280px adds a 10px overflow on Harbor, 390px adds 2px on Harbor, and outcome labels collide at 1024. |
| Visual hierarchy | **5.5/10** | Good panel/card system and clear “start here” blocks, but the 1280px hero is squeezed into a 387–438px column, “read this first” sits below the migrator controls, and the live action is the strongest CTA. |
| Visual consistency | **6/10** | The design language is coherent, but raw enums (`completed_with_gates`, `green_with_human_gates`) and “loop passes” vs “loop iterations” remain, table captions/scroll hints are inconsistent, and the 1440 agent grid leaves an orphan row. |
| Motion | **8/10** | Reduced-motion CSS zeroes all transitions/animations; JS respects `matchMedia`; replay is pausable and announces via `aria-live`. Deduction: replay does not reveal the detail it changes. |
| Error-free rendering | **10/10** | No console errors/warnings, page errors, failed requests, or HTTP ≥400 responses in any tested state. |

**Average: 6.8/10.** No P0 defects found. Five P1, eight P2, and six P3 items remain, plus the deferred print check.

## Horizontal overflow

Measured as `documentElement.scrollWidth − clientWidth`; the off-canvas skip link (`left: -999px`) is excluded because it is an intentional focus technique.

| Page | 1920 | 1440 | 1280 | 1024 | 390 |
|---|---:|---:|---:|---:|---:|
| `/` | 0 | 0 | 0 | 0 | 0 |
| `/migrator` | 0 | 0 | 0 | 0 | 0 |
| `/codebase?case=cascade-mutual` | 0 | 0 | 0 | **+74** | 0 |
| `/codebase?case=harbor-pc` | 0 | 0 | **+10** | **+96** | **+2** |
| `/case-studies` | 0 | 0 | 0 | **+51** | 0 |
| `/settings` | 0 | 0 | 0 | 0 | 0 |
| `/about` | 0 | 0 | 0 | 0 | 0 |

The requirement is ≤1px. Three page variants fail at 1024, one at 1280, and one at 390. Details are in D‑01/D‑02. All three 1024 failures share a root cause: the 240px sidebar does not collapse until 980px, while the inventory, case grid, and case-card header stay multi-column until 900/980/700px respectively. At 1024 the content column is only 728px wide.

## Severity-ranked defects

### P1 — High

#### D-01 — `/codebase` Scout inventory overflows the page at 1024 and 1280
The three-column inventory keeps desktop layout too far down. Long hotspot paths have no wrapping boundary and expand the grid track beyond the page.

- **Selectors:** `.inventory-grid`, `.inventory-grid > div`, `.inventory-list`, `.inventory-list code`
- **Measured:** Cascade 1024: 1098px document vs 1024px viewport (**+74px**); Harbor 1024: 1120 vs 1024 (**+96px**); Harbor 1280: 1290 vs 1280 (**+10px**); Harbor 390: 392 vs 390 (**+2px**).
- **Example overflowing nodes:** `java/harbor/plugin/LegacyHarborRatingPlugin.java` at `x=773 → 1120` (1024) and `x=944 → 1290` (1280); `gsrc/harbor/integration/ClaimsGatewayServlet.gs` at `x=773 → 1113`.
- **Screenshots:** [1024 Cascade inventory](screenshots/a11y-round2/defect-codebase-inventory-overflow-1024.png), [1280 Harbor inventory](screenshots/a11y-round2/defect-codebase-harbor-inventory-overflow-1280.png), [390 Harbor 2px overflow](screenshots/a11y-round2/defect-codebase-harbor-2px-overflow-390.png)
- **Fix direction:** Add `min-width: 0` to grid children, `overflow-wrap: anywhere` (or truncation with a title) to hotspot paths, and switch the inventory to 2 columns at ≤1180 and 1 column at ≤900. Do not hide page overflow globally.

#### D-02 — `/case-studies` card-header badges overflow and are clipped at 1024
`.case-card-head` stays a non-wrapping flex row until 700px. At 1024 the right card is only ~322px wide, but its badge is 320px wide; it leaves almost no room for the segment/title and runs off the viewport.

- **Selectors:** `article.case-card .case-card-head`, `article.case-card .case-card-head .badge`; second card specifically `article.case-card:nth-child(2) .case-card-head .badge`
- **Measured:** second badge `x=755 → 1075`, width 320; document width 1075 vs viewport 1024 (**+51px**). First badge also consumes 301px of a 322px card, forcing the eyebrow into three lines.
- **Screenshot:** [Case card header at 1024](screenshots/a11y-round2/defect-case-studies-card-header-overflow-1024.png)
- **Fix direction:** Allow `.case-card-head` to wrap at ≤1180, give the badge `max-width: 100%` and normal wrapping, or switch the case grid to one column at ≤1100. The existing 700px stacking rule is too late.

#### D-03 — Case-study outcome labels overlap at 1024
The outcome strip still uses four equal columns plus an auto status column. At 1024 each numeric column is ~27px wide, but labels such as “BLOCKERS FOUND” need 40–56px and have `overflow: visible`, so the text runs into the next cell.

- **Selectors:** `article.case-card .case-outcome`, `.case-outcome > div`, `.case-outcome .outcome-label`
- **Measured:** labels are 27px wide with `scrollWidth` 56px (“blockers found”), 50px (“patches drafted”), 40px (“loop passes”), 40px (“human gates”). Screenshot visibly reads `BLOCKERPATCHESLOOP` / `DRAFTEDPASSES`.
- **Screenshot:** [Outcome label collision at 1024](screenshots/a11y-round2/defect-case-studies-outcome-labels-1024.png)
- **Fix direction:** At ≤1180, use a 2×2 numeric grid plus a full-width status row (the ≤700 rule already does this), or allow each cell to size to its labels.

#### D-04 — Mobile codebase findings table wraps IDs and categories character-by-character
The table is inside a keyboard-focusable scroll region, but the first column collapses to ~40px. `CF-0001` becomes three lines; “messaging” becomes “messagin/g”; the caption (1180px wide) is also clipped until the user scrolls.

- **Selectors:** `#cb-findings .codebase-table`, `#cb-findings .codebase-table td:first-child`, `#cb-findings .codebase-table td:first-child code`, `#cb-findings caption`, `#cb-findings .table-scroll`
- **Measured:** table 1180px; scroll viewport 332px at 390; first ID cell 40px wide and 71.5px tall for six characters; caption width 1180px.
- **Screenshot:** [Findings ID wrapping at 390](screenshots/a11y-round2/defect-codebase-findings-idwrap-390.png)
- **Fix direction:** `white-space: nowrap` on ID/severity/category columns; consider a sticky ID column; put the caption outside the horizontal scroller; add a text scroll hint (the gradient alone is easy to miss).

#### D-05 — `/codebase` tabs do not implement the ARIA tabs keyboard model and panels are unnamed
The tabs expose `role="tab"` and `aria-selected`, but all five are in the Tab order (`tabIndex=0`), and ArrowRight does nothing. Tabs have no `id`, so the `role="tabpanel"` regions cannot and do not have `aria-labelledby`. Enter/Space activation works, which is why this remains operable while still being non-conformant for AT users.

- **Selectors:** `[data-codebase-tabs] [role="tab"]`, `[data-codebase-tab]`, `#cb-loop`, `#cb-findings`, `#cb-patches`, `#cb-gates`, `#cb-upgrade`
- **Measured:** five tabs with `tabindex` null/0; `aria-labelledby` null on all panels; ArrowRight leaves `document.activeElement` on “Five-agent loop”.
- **Screenshots:** [Tab bar at 1440](screenshots/a11y-round2/codebase-tabbar-focus-1440.png), [codebase at 1440](screenshots/a11y-round2/codebase-cascade-1440x900-viewport.png)
- **Fix direction:** Add roving tabindex (selected 0, others -1), Left/Right/Home/End handling, tab `id`s and panel `aria-labelledby`. Alternatively remove the tab roles and use ordinary buttons with an `aria-live` region.

### P2 — Medium

#### D-06 — Replay controls change a panel 1,576px below the viewport without scrolling or moving focus
Clicking **Next**, **Play**, or **Reset** updates the active stage and `aria-live` status, but does not scroll the detail panel into view. In the top-of-page test the page stayed at `scrollY=0` while the active panel began 1,576px below it; the only visible feedback is the stage-card outline. Keyboard and screen-magnifier users are left with changed content off-screen, and screen-reader users hear the step but are not placed in the newly shown panel.

- **Selectors:** `[data-replay-next]`, `[data-replay-prev]`, `[data-replay-reset]`, `[data-replay-play]`, `[data-agent-stage]:not([hidden])`
- **Measured:** after Reset, `scrollY=0`; after Next, `scrollY=0`, active panel `top=1576px`, status “Step 2 of 5 · Architect”; after 2s of Play, active panel is Guardian while `scrollY` is still 0.
- **Screenshot:** [Replay at top of page](screenshots/a11y-round2/migrator-replay-at-top-1440x900.png)
- **Fix direction:** Call `showStage(..., { scroll: true })` from replay controls, or focus a `tabindex="-1"` heading in the active panel (without stealing focus during the unattended Play loop).

#### D-07 — 1280px page heads compress the lede into a 387–438px column
The page-head does not stack until 1180px, while `.head-meta` becomes full-width at ≤1319px. The result is a five-to-six-line lede with a large empty area beside it on Home, Migrator, Codebase, and Case Studies.

- **Selectors:** `.page-head`, `.page-head > div:first-child`, `.page-head .lede`, `.head-meta`; CSS `@media (max-width: 1319px)` and `@media (max-width: 1180px)`
- **Measured at 1280:** Migrator/Codebase text column 387px and head-meta 577px inside a 984px row; Home/Case Studies text column 438px and head-meta 526px. At 1440 the lede is 659px.
- **Screenshots:** [Migrator at 1280](screenshots/a11y-round2/defect-page-head-squeeze-migrator-1280.png), [Codebase at 1280](screenshots/a11y-round2/defect-page-head-squeeze-codebase-1280.png), [Case Studies at 1280](screenshots/a11y-round2/case-studies-1280x720-full.png)
- **Fix direction:** Stack `.page-head` at 1319px (the same breakpoint that makes `.head-meta` full-width) or cap `.head-meta` to its content width in row mode.

#### D-08 — Codebase stage cards skip from H2 to H4
`Agent-by-agent: what each one received and produced` is an H2, but each stage card’s “Received”/“Produced” labels are H4s. axe reports `heading-order` (moderate) in all ten codebase states.

- **Selectors:** `.stage-card .stage-card-grid-inner h4` (first representative: `.stage-card:nth-child(1) .stage-card-grid-inner > div:nth-child(1) > h4`)
- **Screenshot:** [Stage cards at 1440](screenshots/a11y-round2/defect-codebase-heading-order-h4-1440.png)
- **Fix direction:** Use H3 for the stage-card subheads, or demote them to non-heading labels if they are only visual column labels.

#### D-09 — Core tables lack captions
The migrator’s three evidence/package/rule tables and the codebase upgrade drill table have no `<caption>`; only their scroll regions have `aria-label`. A screen reader entering table mode gets columns without a table name, and the visible panel heading is not programmatically associated with the table.

- **Selectors:** `.scout-evidence-table`, `.package-table`, `#agent-stage-guardian table.data-table.compact`, `#cb-upgrade .drill-details table.data-table.compact`
- **Screenshots:** [Scout table](screenshots/a11y-round2/defect-migrator-scout-table-caption-1440.png), [Upgrade full page](screenshots/a11y-round2/codebase-upgrade-1440x900-full.png)
- **Fix direction:** Add a visible or `visually-hidden` `<caption>` to each table. Keep the region label as a secondary cue, not a replacement.

#### D-10 — Selected case and feature are visual-only
The active case chip and selected feature row use only `.active`/`.selected`. Screen-reader users cannot tell which story or feature is current, even though the surrounding navigation is otherwise well-labelled.

- **Selectors:** `a.case-chip.active`, `a.feature-row.selected`
- **Screenshot:** [Codebase at 390 showing active Cascade Mutual chip](screenshots/a11y-round2/codebase-cascade-390x844-viewport.png)
- **Fix direction:** Add `aria-current="page"` to the active case chip and `aria-current="true"` (or an appropriate selected-state role) to the active feature row. Keep the visual class as-is.

#### D-11 — Focus ring on the dark topbar is only 1.70:1
The global focus outline is `#075166`. On the light page it is excellent (8.83:1), but on the `#1b2833` topbar it nearly disappears. The brand is the second Tab stop, before any page content.

- **Selector:** `.topbar .brand:focus-visible` (also applies to any future control placed on the dark chrome)
- **Measured:** outline `rgb(7,81,102)` against topbar `rgb(27,40,51)` = **1.70:1**; all other sampled focus rings are a 3px solid dark-teal outline on light surfaces.
- **Screenshot:** [Focused brand in topbar](screenshots/a11y-round2/focus-brand-topbar-1440x900.png)
- **Fix direction:** Use a light focus ring (`#ffffff` or a light teal) on dark surfaces, e.g. `.topbar :focus-visible { outline-color: #d9f1f7; }`.

#### D-12 — Home evidence-graph scroller is not focusable or named
`.spine-scroll` is a horizontal scroll region at 1280, 1024, and 390, and even has a `.spine-scroll:focus-visible` CSS rule, but it has no `tabindex`, `role`, or accessible name. Keyboard users can tab through the 12 graph nodes and the browser scrolls them into view, but they cannot focus and pan the region directly. The “Scroll horizontally…” hint is visible at 390.

- **Selector:** `.spine-scroll` / `[data-spine-scroll]`
- **Measured:** 672px content vs 662px client at 1280, 406px at 1024, 330px at 390; `tabindex=null`.
- **Screenshot:** [Evidence graph at 390](screenshots/a11y-round2/defect-spine-scroll-region-390.png)
- **Fix direction:** Add `tabindex="0"`, `role="region"`, and an `aria-label` to `.spine-scroll`, or remove the unused `:focus-visible` rule and rely solely on the table fallback.

#### D-13 — “Live Critic” checkbox does not control the live run, and active live controls lack a disclosure
The checkbox at `[data-codebase-live]` is never read by JavaScript; `[data-codebase-live-run]` always posts `codebasePayload(true)` (`app/static/js/preflight.js:1181`). The unchecked state therefore does not mean “offline.” The migrator’s active `Run live` button also remains the primary teal action with no visible external-data note, unlike its empty-state launch panel.

- **Selectors:** `[data-codebase-live]`, `[data-codebase-live-run]`, `.agent-loop-actions [data-migration-live]`
- **Screenshot:** [Codebase live controls at 390](screenshots/a11y-round2/codebase-cascade-390x844-viewport.png)
- **Fix direction:** Either wire the checkbox into the payload or remove it; add the synthetic-fixture disclosure next to every live action and make live a secondary button. This is a trust/control-state issue rather than a WCAG failure. No live request was sent during this audit.

### P3 — Low / polish

#### D-14 — Codebase card layout wastes space
At 1440 the five agent cards form a 4 + 1 grid with three empty columns beside Planner; at 390 each cycle card is 160px tall with ~60px of blank space between agent name and count, and the loop page is 11,118px (Cascade) / 11,212px (Harbor) tall.

- **Selectors:** `.stage-card-grid`, `.agent-cycle .cycle-stage`, `.cycle-count { margin-top: auto }`
- **Screenshots:** [4+1 stage-card grid](screenshots/a11y-round2/defect-codebase-heading-order-h4-1440.png), [mobile cycle card whitespace](screenshots/a11y-round2/defect-codebase-cycle-whitespace-390.png)
- **Fix direction:** Use an explicit 5/3/2/1 column policy or center the orphan row; remove the fixed `min-height`/`margin-top: auto` on narrow screens.

#### D-15 — Mobile navigation loses its group labels, and primary navigation is an `aside`, not a `nav`
At ≤980px `.side-label` is hidden, so twelve links appear in a flat two-column grid with no “Agent demo / Review / Workspace” grouping. The sidebar is also `<aside aria-label="Primary navigation">`; there is no primary navigation landmark on any of the seven pages (Codebase’s only `<nav>` is reassigned to `role="tablist"`).

- **Selectors:** `.sidebar`, `.side-label`, `.side-groups`, `.side-link`
- **Screenshot:** [Mobile nav open](screenshots/a11y-round2/mobile-nav-open-about-390x844.png)
- **Fix direction:** Keep group labels (or `aria-label` the groups) on mobile and use `<nav aria-label="Primary navigation">` for the sidebar. The `aria-expanded`, Escape, and focus-restore behavior themselves pass.

#### D-16 — Raw enums and unit-name drift
`completed_with_gates` remains in the migrator progress line; `green_with_human_gates` remains in the Codebase explain outcome; Case Studies says “loop passes” while Codebase says “loop iterations” and Migrator says “stages.”

- **Selectors:** `.migration-progress-meta [data-migration-label]`, `.agent-explain .explain-grid strong`, `article.case-card .outcome-label`
- **Screenshots:** [Migrator raw status](screenshots/a11y-round2/migrator-1440x900-viewport.png), [Codebase raw enum](screenshots/a11y-round2/codebase-cascade-1920x1080-viewport.png), [Case Studies outcome](screenshots/a11y-round2/case-studies-1280x720-full.png)
- **Fix direction:** Humanize the status tokens and standardize on “iterations” across the product.

#### D-17 — Micro-labels and prompt chips are below comfortable reading/target size
`.eyebrow`, `.summary-label`, `.outcome-label`, `.cycle-role`, and `.seal-label` are 10–10.5px uppercase with letter spacing; the three assistant prompt chips are 108×23, 81×23, and 109×23px. The chips likely satisfy WCAG 2.2 target-size only through the spacing exception, not by size.

- **Selectors:** `.eyebrow`, `.summary-label`, `.outcome-label`, `.cycle-role`, `.chip`
- **Measured:** chips 23px high at both 1440 and 390; all pass contrast but are the least legible text in the UI.
- **Screenshot:** [Home at 390](screenshots/a11y-round2/home-390x844-viewport.png)
- **Fix direction:** Raise micro-label size to 11–12px and chip height to 28–32px; keep the uppercase tracking only where space allows.

#### D-18 — “Read this first” still appears after the migrator controls
The `.agent-explain` panel with the `read this first` badge is below the agent-loop controls, five stage cards, replay bar, and summary strip. A first-time viewer can start a run before seeing the explanation that says what the run means.

- **Selectors:** `.agent-loop-panel + .agent-explain`, `.agent-explain .badge-neutral`
- **Screenshot:** [Migrator controls and lower explain panel](screenshots/a11y-round2/defect-migrator-readthisfirst-below-controls-1440.png)
- **Fix direction:** Move the explain panel above the agent-loop controls, or put a one-paragraph “Start here” summary in the hero.

#### D-19 — Mobile panel heads stay two-column and cramp titles
At 390 the upgrade panel head puts “Mid-migration upgrade resilience” in a three-line left column and “simulate a core release change…” in a four-line right column. The content remains readable but the hierarchy is strained; this pattern repeats on several panel heads.

- **Selector:** `.panel-head` at ≤700px, especially `.upgrade-panel .panel-head`
- **Screenshot:** [Upgrade panel head at 390](screenshots/a11y-round2/defect-upgrade-panelhead-390.png)
- **Fix direction:** Stack panel heads at ≤700px or move the side note below the title.

### Deferred — print/PDF

#### D-20 — Print/PDF deck readiness is deferred
There is no deck implementation in this branch (only markdown runbooks and screenshot assets), so a full print audit would test the browser’s default output rather than a product surface. The product CSS has **no `@page` and no `@media print` rules**; the baseline print render includes the topbar, sidebar, and interactive controls.

- **Baseline screenshot:** [Print emulation of Case Studies](screenshots/a11y-round2/print-baseline-case-studies-1440.png)
- **Status:** Deferred until a deck changes the presentation layer. When that happens, add a print stylesheet with page breaks, hidden chrome, expanded tab panels, and controlled table/screenshot sizing.

## Detailed check results

### Keyboard and focus

| Check | Result |
|---|---|
| Skip link | Passes. First Tab reveals “Skip to content” with a 3px outline and jumps to `#main`. [Screenshot](screenshots/a11y-round2/focus-skip-home-1440.png) |
| Visible focusable coverage at 1440 | Migrator 41/41, Codebase 28/28, Case Studies 19/19, Settings 21/21, About 16/16. Home reached 51/52; the remaining counted item is a scroll region inside a closed `<details>` and is reachable after opening its summary. |
| Mobile nav | Passes. `aria-expanded` flips; all 12 links reachable; Escape closes and restores focus to the toggle. [Screenshot](screenshots/a11y-round2/mobile-nav-open-about-390x844.png) |
| Stage buttons | Pass. Five real buttons, exactly one `aria-pressed="true"`; Enter/Space activates; no `role="listitem"` conflict. [Focused Guardian](screenshots/a11y-round2/focus-stage-guardian-1440x900.png) |
| Tab strip | Operable with Tab + Enter/Space, but fails the arrow/roving-tabindex pattern and panel naming; see D‑05. |
| Scrollable regions | Table scroll regions and the Guardian gate list have `tabindex="0"` and labels. Home `.spine-scroll` does not; see D‑12. |
| Focus indicator | 3px `#075166` outline on light surfaces. Dark-topbar contrast is only 1.70:1; see D‑11. |
| Replay | Play becomes Pause; the step status is `aria-live="polite"`; the active stage detail is not brought into view; see D‑06. |

### ARIA, headings, labels, and landmarks

- **H1:** exactly one per audited page.
- **Heading order:** only the Codebase H2→H4 issue. axe reports `heading-order` (moderate) once per state at 1920/1440/1280/1024/390 for both cases. All other pages have a clean hierarchy.
- **Landmarks:** header, main, footer, and a named sidebar are present. The primary sidebar is an `aside`, not a `nav`; the codebase tab strip is a `nav` whose `role="tablist"` overrides navigation semantics.
- **Labels:** no unlabelled visible inputs/selects/textareas. Home’s search/assistant fields, Codebase’s Live Critic/model controls, and the upgrade scenario select all have names.
- **Alt text:** no `<img>` elements on the audited pages. The home evidence graph is an SVG with a group label and keyboard-selectable nodes; decorative arrows are `aria-hidden`.
- **Tables:** captions are present in Settings, About, and Codebase findings, and in the home fallback. They are missing in the four tables listed in D‑09.
- **Selected state:** nav links use `aria-current="page"` correctly, but case chips and feature rows do not; see D‑10.
- **Duplicates/empty controls:** no duplicate IDs and no empty link/button names found.

### axe-core 4.10.2

Ran against 115 states: 35 base page/viewport loads, 25 migrator stage states, 50 codebase tab states, and 5 upgrade-impact states.

- **Only rule returned:** `heading-order` (moderate), 1 node per Codebase state (10 states total).
- **No `aria-allowed-attr`, `color-contrast` failure, `scrollable-region-focusable`, `label`, `button-name`, `link-name`, `image-alt`, or `landmark` violation.**
- **Incomplete `color-contrast`:** SVG text on the home graph and decorative arrows/handoff routes could not be auto-resolved because of complex backgrounds or non-text characters. Manual sampling found no text contrast failure. The 1024 Case Studies eyebrow was reported incomplete because the overflowing badge overlaps it; that is a layout defect (D‑02/D‑03), not a contrast-ratio defect.

### Color and contrast

Manual sampling covered body/lede/muted, all badge/pill variants, buttons, tabs, primary nav, case chips, summary/outcome/cycle labels, table headers, banners, code, and diff text. All text samples passed 4.5:1.

| Sample | Ratio |
|---|---:|
| `.muted` / `.badge-neutral` / `.data-table th` `#5b6f80` on `#f1f4f7` | **4.72:1** (lowest) |
| Success pill `#267a45` on `#eaf4ee` | 4.72:1 |
| `.lede` / inactive tab `#5b6f80` on `#f6f8fa` | 4.89:1 |
| `.summary-label` / `.context-meta` `#5b6f80` on white | 5.21:1 |
| Link/brand `#0b6b85` on white | 6.08:1 |
| Primary button white on `#0b6b85` | 6.08:1 |
| Danger summary `#b3261e` on white | 6.54:1 |
| Dark-topbar focus ring `#075166` on `#1b2833` | **1.70:1** (D‑11) |
| Decorative `.cycle-arrow` `#b9c7d3` on white | 1.70:1 (aria-hidden; exempt) |

The 4.72:1 labels pass, but the margin is thin. Any tint or opacity change to `--surface-2` will break the 10px labels that use it.

### Motion / reduced motion

- Under `prefers-reduced-motion: reduce`, computed transitions drop to **0** and animations to **0**; the global CSS rule zeroes both. Normal state had 1 transition on the Migrator.
- `motionBehavior()` switches smooth scrolling to `auto` when reduced motion is requested.
- Replay is user-initiated, has a Play/Pause toggle, and announces steps through `aria-live="polite"`. It does not auto-start on load.
- Remaining behavioral issue: replay changes the detail panel off-screen; see D‑06.

### Text fit, clipping, and mobile

- **Cycle cards:** the old `.cycle-role` clipping is fixed at 1440/1280/1024; role text is fully visible. At 390 the cards are 160px tall with large blank gaps (D‑14).
- **Outcome strips:** pass at 1920/1440/1280/390; fail at 1024 with overlapping labels (D‑03).
- **Long paths:** contained in table scroll regions on `/migrator`, but inventory hotspot paths break the page at 1024/1280 and codebase findings IDs/categories break character-by-character at 390 (D‑01/D‑04).
- **Score labels:** pass. At 390 the three `.score-card`s lay out 2 + 1 (162/162/332px), with no clipping; labels are 140px wide and 15px high. [Screenshot](screenshots/a11y-round2/score-cards-390x844.png)
- **Mobile page lengths:** Codebase loop is 11,118px (Cascade) and 11,212px (Harbor) at 390; the five 160px agent cards alone consume ~800px before detail.

### Console, network, and runtime

- **35/35 base page loads:** zero console errors/warnings, zero `pageerror`, zero failed requests, zero HTTP ≥400 responses.
- **Interaction passes:** stage clicks, replay Play/Pause/Reset, all five codebase tabs, patch expansions, mobile nav toggle/Escape, and upgrade impact loading also produced zero errors or failed requests.
- The CSP correctly blocks inline script injection; axe was run through CDP without weakening the policy.

## Round-1 follow-up (same run)

| Round-1 item | Current status |
|---|---|
| Brand as home link | **Fixed.** `.brand` is an `<a href="/">` with `aria-label="PreFlight home"`. |
| Product definition on Home | **Fixed.** “What PreFlight is, in plain language” is the first content panel. |
| Clipped cycle-role labels | **Fixed.** `.cycle-index` is static; roles fit at 1440/1280/1024. |
| Stage `role="listitem"` + `aria-pressed` conflict | **Fixed.** Stage buttons are plain buttons with valid `aria-pressed`. |
| Non-focusable Guardian gate list | **Fixed.** `.gate-list.compact` has `tabindex="0"`, a label, and a focus ring. |
| “2 passs” and raw `target {'warning': 7}` | **Fixed.** Copy now reads “2 passes” and “warning: 7”. |
| Case-study `green · gated` badge | **Improved.** Now “machine-green / human gates open” with a caveat. |
| Two loops / Scribe vs Planner | **Fixed/explained.** Home, Codebase, and Case Studies now state the role difference. |
| 1280 page-head squeeze | **Still present.** See D‑07. |
| Replay does not bring detail into view | **Still present.** See D‑06. |
| Active case/feature is visual-only | **Still present.** See D‑10. |
| Codebase tab keyboard pattern | **Still present.** See D‑05. |
| Mobile stage-card whitespace | **Still present.** See D‑14. |
| Mobile findings table | **Partially fixed.** Scroll region exists; ID/category wrapping and caption clipping remain. See D‑04. |
| “loop passes” vs “loop iterations” | **Still present in Case Studies.** See D‑16. |

## What passed cleanly

- Skip link, one H1 per page, unique page titles, and no duplicate IDs.
- All visible buttons/links have accessible names; all audited form controls are labelled.
- No raster images; the SVG evidence graph has a group name and named keyboard nodes.
- Mobile navigation: toggle state, Escape close, focus restoration, and every link reachable.
- Table scroll regions and Guardian gate list: focusable, labelled, visible focus ring.
- Reduced-motion: no transitions/animations under the preference; replay remains pausable.
- Zero console/page/network errors across every tested state.
- axe: no serious/critical violations; the only rule returned is the moderate heading-order issue.

## Recommended fix order

1. **Make 1024 safe.** Fix the case-card header/outcome and codebase inventory at 1024 first; then re-check 1280 Harbor (+10px) and 390 Harbor (+2px). A single breakpoint pass that collapses the sidebar/case grid/inventory at ≤1180 will remove most of the responsive score loss.
2. **Fix the codebase tabs.** Roving tabindex + arrow keys + tab/panel IDs and `aria-labelledby`; or remove the tab roles. This is the largest remaining AT-semantic gap.
3. **Make replay reveal its result.** Scroll/focus the active stage panel from Next/Play/Reset; keep the live region announcement.
4. **Repair the mobile findings table.** `nowrap` on IDs/severity/category, caption outside the scroller, and a visible scroll cue.
5. **Stack the 1280 page head.** Move the existing 1180px rule to 1319px, or stop `.head-meta` from taking 100% in row mode.
6. **Batch the semantics fixes.** H4→H3, table captions, `aria-current` on case/feature, `.spine-scroll` tabindex/name, and a light focus ring on the dark topbar.
7. **Polish mobile hierarchy.** Remove the 160px stage-card blank space, stack panel heads, keep nav group labels, raise micro-labels/chips slightly.
8. **Add a print stylesheet only when the deck exists.** Deferred for now; current print output includes app chrome and interactive controls.

## Artifact index

All screenshots are under `docs/audits/screenshots/a11y-round2/`. The most useful evidence files:

- Responsive/overflow: `defect-codebase-inventory-overflow-1024.png`, `defect-codebase-harbor-inventory-overflow-1280.png`, `defect-codebase-harbor-2px-overflow-390.png`, `defect-case-studies-card-header-overflow-1024.png`, `defect-case-studies-outcome-labels-1024.png`
- Mobile findings/cycle: `defect-codebase-findings-idwrap-390.png`, `defect-codebase-cycle-whitespace-390.png`, `defect-spine-scroll-region-390.png`
- 1280 hierarchy: `defect-page-head-squeeze-migrator-1280.png`, `defect-page-head-squeeze-codebase-1280.png`
- Keyboard/focus: `focus-skip-home-1440.png`, `focus-brand-topbar-1440x900.png`, `focus-stage-guardian-1440x900.png`, `mobile-nav-open-about-390x844.png`, `codebase-tabbar-focus-1440.png`
- Structure/layout: `defect-codebase-heading-order-h4-1440.png`, `defect-migrator-scout-table-caption-1440.png`, `defect-migrator-readthisfirst-below-controls-1440.png`, `defect-upgrade-panelhead-390.png`
- Replay: `migrator-replay-at-top-1440x900.png`
- Print baseline: `print-baseline-case-studies-1440.png`
- Full-page references for every page/viewport: `<page>-<viewport>-full.png` and `<page>-<viewport>-viewport.png`.

**Bottom line:** the fundamentals are good, and the runtime/accessibility baseline is clean. The remaining failures are concentrated and fixable: one breakpoint pass, one tab component, one replay behavior, one mobile table, and a short semantics batch. Until those land, the product is pleasant at 1440/1920 but not dependable at 1024 or fully conformant for Assistive Technology.
