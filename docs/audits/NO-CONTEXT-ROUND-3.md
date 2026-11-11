# No-context audit — Round 3

**Auditor stance:** a smart reviewer who knows nothing about Guidewire, Gosu, APD, Cloud Data Access, App Events, Cloud Assurance, or PreFlight.
**App:** `http://127.0.0.1:8000` (run `R-DEMO-001`, `demo-slice-300`, synthetic fixture).
**Date:** 2026-11-11.
**Viewports:** 1440 × 900, 1280 × 720, 1024 × 768, 390 × 844 (Chromium/Playwright, 100% zoom).
**Evidence:** screenshots under `docs/audits/screenshots/no-context-round3/`. Key files are indexed at the end.
**Method:** answers below come from the rendered screens. I consulted source only to name the exact DOM selectors and confirm implementation details cited in the defect log; I did not use source to decide the answers. I did not edit product code, tests, or existing docs. I did not run live reasoning, delete a run, or record a feature-loop decision.
**Disclosure:** while testing the codebase upgrade flow I clicked **Record revalidate** and **Apply and re-run the loop** for Harbor, then **Run fresh** to restore its default green state. Those actions persisted in the codebase audit trail; the feature run `R-DEMO-001` remained pending. `Test connection` was clicked once; it returned `OK · mimo-v2.6-flash · 3369 ms` without exposing a key.

---

## 1. Verdict

PreFlight is unusually self-aware about what it is not. The home page answers “what is this?” in one screen; the feature loop exposes **received/produced** panels for all five agents; the machine-check vs human-gate boundary is repeated; and every run carries a synthetic-estate/reality-boundary warning.

It is still **not no-context**. The largest problems are not missing features but unresolved vocabulary and stopped workflows:

- Counts are stated, but their relationships are not reconciled: **31/101/126 evidence items**, **5 packages / 5 target drafts / 5 changes**, **8 bundle files / 7-of-8 seal matches**, **9 audit events vs 12 agent-log events**.
- “Gate” is used for machine checks, grouped findings, assumption questions, and human decisions. The human decisions have no controls on the pages that announce them.
- The codebase Source-findings table **overflows at every tested width and never shows its scroll cue**, hiding columns at 1440 as well as 390.
- The upgrade story visibly contradicts itself after “Apply and re-run”: **“compatible” + “Green signal invalidated: yes” + “generation 1” + “generation 1 → 2” + a “Retain” option with no Retain button**.
- A no-context reviewer can answer most of the ten questions, but only after reading two or three pages and mentally joining three ID schemes (**A-01… / G-01… / unlabelled gap cards**).

**Overall: 5.8/10. No-context explainability: 5/10.** Deliberately harsh: a 7 means usable, not excellent.

---

## 2. The ten questions, answered from the screen

### Q1. What is PreFlight? What is it not?

**What it is.** The home page says: “PreFlight is a local, read-only review tool for a Guidewire-style insurance codebase before a cloud migration. It reads a snapshot, groups the code into features, and shows what each claim is based on, what is still unknown, and what a safe change would touch.” It runs on the machine, never edits the source, and never deploys.

**What it is not** (home “WHAT IT IS NOT”, About “What it is not”):

- Not an official **Cloud Assurance** result, score, or certification.
- Does not convert products to **APD** and does not replace **Cloud Retrofit**.
- Not a deployment tool or a live tenant connection.
- Not an autonomous approver: every draft, mapping, and patch stays pending.
- Not a generic Gosu linter; SonarQube and Cloud Assurance own generic linting.
- The Migrator is a draft generator: local, non-deployable, no tenant contact.

The About page adds the important qualifier: the Migrator “writes a local, non-deployable bundle and leaves every change pending human approval.” The home page also labels itself an “independent academic research prototype”; no Guidewire affiliation.

### Q2. What are the five agents, and what does each receive/produce?

From `/migrator?run=R-DEMO-001`, stages 1–5 (URLs `?stage=scout`, `?stage=architect`, `?stage=guardian`, `?stage=critic`, `?stage=scribe`):

| Agent | Receives | Produces |
|---|---|---|
| **Scout** | Completed review run and source manifest; feature index and evidence graph; findings and explicit dispositions. | Feature scope **PA-VEH-01 · Vehicle Information**; **31 evidence links**; 101 evidence records across 300 files; 24 findings; 12 dispositions. |
| **Architect** | Scout’s PA-VEH-01 scope; 12 explicit dispositions; evidence IDs for every package. | **5 work packages / 5 target files** (WP-01 schema, WP-02 mapping, WP-03 updater, WP-04 codegen config, WP-05 API contract); every package pending. |
| **Guardian** | Architect’s 5 packages; open assumptions and review findings; Guidewire rule pack and APD constraints. **Deliberately not received:** Scout narrative/opinion, Critic verdict/fixes, any model text. | **11 open gates**: 3 assumption gates + 8 rule groups; 6 high-impact; deployment blocked. |
| **Critic** | Scout’s evidence summary; Architect’s packages/targets; Guardian’s gate register. | **7 independent checks passed**; verdict PASS; 0 auto-approved changes. |
| **Scribe** | Critic’s verification; Guardian’s open gates; package and target hashes. | Plan, report, bundle manifest, and hash-chained agent log; **8 bundle files**; all changes still pending. |

In the codebase loop the same first four roles appear and the fifth is **Planner** instead of Scribe. Planner compiles the executive report, readiness indicator, SARIF summary, and next actions; it still runs only after Guardian and Critic agree.

### Q3. Why 5 packages, 11 human gates, 7 machine checks, 8 bundle files?

The screen gives the **decomposition** but not a single “why these counts” sentence. Reading the stage panels and packet together:

- **5 packages** = five target artefacts, one per work package: `WP-01` schema, `WP-02` mapping, `WP-03` updater, `WP-04` codegen config, `WP-05` API contract. These correspond to changes `C-01`…`C-05` in the packet. The page never says “one package per target artefact” explicitly.
- **11 human gates** = **3 assumption gates** (`G-01`…`G-03`) + **8 rule groups** (`G-04`…`G-11`, one per rule with 3 findings each). 6 are high-impact. All 5 generated changes remain pending.
- **7 machine checks** = Critic’s checks: packages exist; all package files generated (5/5); no `_gen` targets; no duplicate targets; generated JSON/YAML parses (5 files); every package evidence-linked (5/5); human approval retained (0 auto-approved). This is stated on the Critic stage.
- **8 bundle files** = 5 target drafts + plan + report + agent log. The **bundle manifest is a separate wrapper** and is *not* counted among the 8, even though the page says Scribe seals the bundle manifest. Seal check is **7/8 match · log appended**, because the agent log is append-only and has grown since seal.

**Friction:** Guardian also displays **7/7 deterministic checks passed**, while listing only three work items. The seven listed checks belong to Critic. A no-context reader cannot tell whether Guardian has seven hidden checks, Critic’s seven are being echoed, or there are fourteen.

### Q4. What is the difference between Scribe and Planner?

Same role, different loop:

- **Scribe** is the fifth agent in the **feature loop**. It seals the plan, report, bundle manifest, and hash-chained agent log; the stage says “Sealing is not approval.”
- **Planner** is the fifth agent in the **codebase loop**. It compiles and seals the executive report, readiness indicator, SARIF summary, and next actions after Guardian and Critic agree.

The home page and Case Studies both say this explicitly: “Both loops use the same first four roles. Only the sealer changes name.” That is clear. What is less clear is that Scribe “seals the bundle manifest” while the manifest is then labelled “wrapper · not a sealed content file.”

### Q5. What does machine-green mean, and what must a human do next?

**Machine-green** is a machine result, not approval. On Cascade/Harbor it means Guardian’s 13 deterministic checks and Critic’s 7 independent checks agree: **20/20 passed**, Planner compiled the report, and all patches remain pending. The page repeats: “A machine-green result is not human approval.” It is also not an official Cloud Assurance result.

What a human must do next is explicit:

- **Codebase loop:** review the named gates `CR-01`…`CR-10` (Cascade) or `CR-01`…`CR-11` (Harbor) with their owners; accept, reject, or defer every patch; resolve affected rules; revalidate after a release upgrade. Harbor: 11 gates open, 7 high-impact, 21 patches pending; Cascade: 10 gates, 22 patches pending.
- **Feature loop:** assign owners to 3 unassigned assumption gates; resolve the 3 assumptions; accept/reject the 12 mappings; review the 5 draft packages; verify the 12-event agent log. 11 gates open, 5 changes pending.

**Defect:** these are to-do lists, not actions. The codebase gate cards and patch cards have **no accept/reject/defer controls**, and the Reconstruction **Assumptions** tab has no action control at all. On the feature page, a human can decide mappings/changes/findings, but not assumptions. The page tells a person to do things the UI cannot do.

### Q6. What are Cascade and Harbor, and their outcomes?

They are the two **synthetic codebase migration stories**, not real insurers:

| Story | Outcome shown |
|---|---|
| **Cascade Mutual** — monoline Personal Auto mutual, Cloud Retrofit without APD App | **18 blockers, 22 patches, 2 iterations, 10 human gates**, machine-green · gates open. Codebase page: 17 files, 156 LOC, 18 findings, 22 patches, 24 target files. Readiness 0 before, 100 structural after, 74 after human gates. |
| **Harbor P&C** — multi-line P&C group, Cloud Retrofit + APD naming preparation (type-level codegen draft) | **20 blockers, 21 patches, 2 iterations, 11 human gates**, machine-green · gates open. Codebase page: 15 files, 160 LOC, 20 findings, 21 patches, 23 target files. Readiness 0 before, 100 structural after, 71 after human gates. |

Both codebase pages show **20/20 deterministic checks** (13 Guardian + 7 Critic), 2 iterations, and every patch pending. The Case Studies cards match those outcomes. The immediate contradiction is the page title: **“Two completed migrations you can explore”** followed by the banner “This is a synthetic rehearsal, **not an actual migration**.”

### Q7. Where is the evidence for a claim?

Evidence is present in several forms, but it is not one coherent, clickable trail:

- **Workbench / feature spine:** click an evidence-bearing node and the **Selected node evidence** panel shows an EV ID, file path, line/xpath, excerpt, method, and excerpt SHA-256. Example: `PAVehicleDV` → `EV-0001`, `config/web/pcf/policy/PAVehicleDV.pcf`, xpath `/PCF/Screen/TypeKeyInput[1]:4`, excerpt `<TypeKeyInput id="VehicleType" .../>`, method `xml_xpath`, excerpt SHA `d76bf9908b1f`.
- **Migrator stage 1:** the first eight of 31 links are shown with EV ID, file, locator, and excerpt. Each EV link opens the raw JSON endpoint `/api/runs/R-DEMO-001/evidence/EV-0001`, not a formatted evidence page. There is no “view all 31” control.
- **Findings:** each row has a stable ID (`F-002`…`F-025`), source path:line, severity, claim strength (`verified-id`, `verified-policy`, `verified-doc`, `secondary`, `heuristic`), standard ID, and an excerpt in the detail panel. Example: `F-002` → `gsrc/acme/error/SwallowError.gs:7`, `ERR00-G`, `verified-id`.
- **Codebase lab:** findings show a stable fingerprint, path:line, rule, standard, and cloud target; patches show unified diffs; artifacts show report/SARIF/audit hashes; the SARIF endpoint and audit JSON are downloadable. But codebase finding rows do **not** show an excerpt and are not clickable to a source view.
- **Packet:** hashes for snapshot, rulepack, reference target, ground truth, audit head, findings, mappings, assumptions, evidence, review evidence, gaps, packet. It claims a 126-item evidence appendix and a full audit trail, but the rendered packet does not list those 126 items or the 9 audit events—only the hashes.

**The weakest link:** package evidence IDs are inert. `WP-01` shows `EV-0011 EV-0018` as plain `<code>` text in `#agent-stage-architect .package-table td:nth-child(5)`, not links. To verify the claim you must leave the package table, remember the IDs, and hunt in Workbench or the packet. There is also no source-file viewer anywhere; the evidence is an excerpt and hash, not the file itself.

### Q8. Is this an actual migration? How do you know?

**No.** It is a synthetic rehearsal.

Evidence on screen:

- Persistent top badge **“Synthetic estate”** and **“Official Cloud Assurance: not run.”**
- Home boundary: “This is a synthetic rehearsal, not an actual migration: no tenant, no code compile or deployment, and no official Cloud Assurance result.”
- Codebase boundary: “No Guidewire tenant was contacted, no source file was edited, no patch was applied, compiled, or deployed.”
- Migrator: “No tenant contacted · No compile or deploy · No change approved · No official Cloud Assurance”; every change is a “non-deployable draft.”
- Reconstruction: `_gen writes: 0 · draft is local / non-deployable`.
- Case Studies: both insurers are “dummy profiles with invented code, not customer data.”
- The global disclaimer says the packet is generated from a synthetic fixture and contains no customer data or confidential Guidewire information.

The word **“succeeded”** in the run status therefore means the analysis run succeeded, not that a migration happened. The Case Studies title “completed migrations” works against this.

### Q9. What happens on an upgrade mid-migration?

On `/codebase?case=harbor-pc`, open **Upgrade resilience**, choose **“APD import limit tightens from 24 to 20 characters (GWCP 2026.10 → GWCP 2027.04)”**, and press **Evaluate upgrade**:

- A warning banner appears: **“Stale green signal — revalidation required. Upgrade GWCP 2026.10 to GWCP 2027.04 invalidated the green signal; revalidate the affected patches before approval.”**
- Status becomes **revalidation required**; the previous 20/20 check result is labelled **“checks passed before the upgrade.”**
- Generation goes **1 → 2**; 2 patches are affected (`CP-013`, `CP-016`), rule `PF-CODE-APD-001`.
- One check fails: **“codegen overrides fit the 20-character limit — 1 override(s) exceed 20 characters.”**
- Options: re-run Architect with the new rule pack (recommended), roll back to the last green checkpoint, or defer/pin the release. Buttons: **Record revalidate / Record rollback / Record defer** and **Apply and re-run the loop**.

That is a good story. The implementation then breaks it:

- **Record revalidate** reports `Recorded revalidate: resume_requested. The green signal remains cleared …`—an internal token as user-facing text. It does not revalidate anything; it only records a request. The primary button label overpromises.
- After **Apply and re-run the loop**, the same Upgrade card changes to status **“compatible”**, checks **PASS**, yet still says **“Green signal invalidated: yes”**, **“2 patch(es) affected”**, and offers **“Retain the green bundle with a revalidation note”** with no Retain button. The header still says **“bundle generation 1”** while the card says **“Bundle generation 1 → 2.”**
- Navigating away to `/codebase?case=harbor-pc` or `/case-studies` shows **machine-green · human gates open** again; the stale state exists only while the `?upgrade=…` query is present. The product says it “will invalidate stale green state,” but the invalidation is not persistent.

### Q10. How do you enable live reasoning without exposing a key?

On `/settings`, section **“MiMo / OpenAI-compatible endpoint”**:

- Current state: **enabled**, mode **live**, endpoint host `token-plan-sgp.xiaomimimo.com`, models `mimo-v2.6-flash` and `mimo-v2.6-pro`, default `mimo-v2.6-flash`, real code **synthetic only**.
- Instructions: set `PREFLIGHT_LLM_MODE=live`, `PREFLIGHT_LLM_BASE_URL`, and `PREFLIGHT_LLM_API_KEY` in `.env`, then restart the app. The base URL and key are read only from the environment.
- Key handling: “No key value is displayed or requested in this UI”; “No key is written to the repository, logs, screenshots, or API responses.” The page shows the endpoint host and model names, never a key.
- Use: live is opt-in per run; Scout, Architect, and Critic may receive grounded narrative prompts; Guardian never calls the model; every returned statement must cite an allowed evidence/rule/package ID, and ungrounded statements are dropped and counted. Only synthetic fixture text is eligible by default.
- I clicked **Test connection** once: `OK · mimo-v2.6-flash · 3369 ms`. No key was shown.

The caveat: the same product shows **“Reasoning: offline”** badges on Migrator and Codebase, **“retrieval-only - model off”** on the assistant, and **“Reasoning: offline by default”** in the footer, while Settings says “Live reasoning is enabled.” A first-time reader cannot tell “enabled capability” from “this run used live reasoning.”

---

## 3. Scorecard

Scale: **0 = unusable without a guided tour; 10 = a first-time viewer needs no explanation.** Deliberately harsh.

| # | Category | Score | Why |
|---:|---|---:|---|
| 1 | Purpose and first impression | **7** | Strong “What it is / What it is not / Three promises” block and repeated reality boundary. Docked for undefined “Guidewire-style,” “Cloud Assurance,” “Cloud Retrofit,” and “APD App,” and for a first screen that is already a dense worked example. |
| 2 | Navigation and IA | **6** | Clear desktop sidebar grouping; mobile Sections menu works. But one page has three names (“Agent loop” / “Migrator” / “Watch the migration crew work”), “Migration stories” becomes “Case studies,” and the primary navigation is an `aside`, not a `nav` landmark. |
| 3 | Terminology and count consistency | **4** | “Disposition,” “package,” “target draft,” “change,” “evidence record,” “reference,” and “gate” all shift meaning. There are unresolved 31/101/126, 9/12, 5/8, and 7/7 counts. The A/G ID schemes do not cross-reference. |
| 4 | Workbench usability | **6** | Excellent selected-node evidence panel, useful assistant refusal, clear excluded-file story. Docked for “37 vs 24” with no units, 11 unexplained “references,” no way to browse the 31 evidence records, and gap cards without IDs or owners’ actions. |
| 5 | Five-agent explainability | **7** | The received/produced panels are the best part of the product. Docked for Guardian also showing 7/7 with only 3 listed work items, and for Scribe/Planner being the same role under two names while the sealer’s artifacts vary. |
| 6 | Migrator replay, next actions, bundle trust | **5** | Replay works and next actions are explicit. Docked for “7/8 match · log appended” reading like a failed seal, “Scribe seals the bundle manifest” vs “manifest is a separate wrapper,” 8 files vs 4 download links, 9 vs 12 audit events, and no action controls for the 11 gates. |
| 7 | Codebase Cascade | **6** | Iteration 1/2, Guardian 13 checks, Critic 7, human gates, and patch diffs are explicit. Docked for the key tabs starting 1,923 px down the page, “The value is not a score” followed by target/readiness scores, no patch decisions, and an overflowed findings table with no cue. |
| 8 | Codebase Harbor | **6** | Same strengths and defects as Cascade, plus the upgrade story. Docked for the upgrade-state contradictions and for “generation 1” vs “2 iterations” with no explanation. |
| 9 | Upgrade / stale-green | **5** | The first invalidation is clear and concrete. Docked heavily for the post-rerun “compatible + invalidated: yes” card, absent Retain control, unchanged generation badge, `resume_requested` token, and non-persistent stale state. |
| 10 | Case studies | **6** | Specific insurers, constraints, custom slices, outcome strips, and caveats. Docked for the headline “Two completed migrations” directly contradicting “not an actual migration,” and for missing definitions of Cloud Retrofit / APD App. |
| 11 | Settings, About, boundaries | **7** | Data policy and live-key instructions are clear; the boundaries are responsible and well written. Docked for a glossary that omits PCF, Qusar, GWCP, Cloud Assurance, Cloud Retrofit, APD App, SBT, Olos, GUnit, and MiMo; for duplicate disclaimer copy; and for the offline/live status ambiguity. |
| 12 | Responsive, visual hierarchy, accessibility, console | **5** | No document-level overflow at the four widths; mobile nav, tab arrow keys, dialogs, and skip-link visibility work. But the codebase findings table overflows at 1440 and 390 with **no cue**, the mobile findings detail is above the table, key work sits 2–4 screens down, touch targets are small, skip-link focus falls to body, and the primary nav has no navigation landmark. No console or network errors. |
| — | **No-context explainability (separate)** | **5** | Q1, Q2, Q4, Q5, Q6, Q8, and Q10 are answerable with effort. Q3 needs synthesis across three stage panels, Q7 needs hunting and has dead ends, and Q9 is contradicted by its own post-rerun state. A newcomer can sound informed, but not certain. |

**Average of the 12 categories: 5.8/10.**

---

## 4. Page-by-page stumbles

| Route | What a no-context reviewer hits | Exact evidence |
|---|---|---|
| `/` (no query) | Auto-loads `R-DEMO-001`; no empty state or run chooser, so the first screen is already a completed worked example. “37 vs 24” has no units. | `.summary-stat` “37 vs 24 / LONG TYPE VS APD LIMIT”; `Run R-DEMO-001` appears without a run selector. |
| `/` | Evidence counts disagree across pages: 31 records here, 101 records on Migrator, 126 items in the packet. “11 references” is never defined. | Home summary strip; `#agent-stage-scout`; `/packet?run=R-DEMO-001`. |
| `/` | “Unknowns and gaps” has three cards but no IDs, while Migrator calls its three assumptions `G-01`…`G-03` and the packet calls them `A-01`…`A-03`. The third item is different: Workbench gap 3 is **duplicate PAVehicleDV screen**; Migrator/Reconstruction assumption 3 is the **37-character APD type**. | `.gap-card` × 3; `#agent-stage-guardian` assumption gates; `/reconstruction?tab=assumptions`. |
| `/manifest` | The “Excluded (4)” checkbox is a 13 × 13 px input inside a 19.5 px label. The checkbox alone does not apply; Apply reloads. | `input[name="excluded"]`, `label.check-inline`; at 390 label is 106.7 × 19.5. |
| `/reconstruction` | At 1280 the mapping table is 1,040 px wide inside a 950 px viewport; the **STATE** column (`pending`) sits underneath the sticky **DECISION** actions at the default scroll position. At 390 only the first two data columns plus pinned actions are visible. | `.mapping-table`; `.mapping-table .actions-col`; table scroll 1040/950 at 1280, 1040/332 at 390. |
| `/reconstruction?tab=assumptions` | The 3 assumptions are listed but there is no action, owner assignment, or decision control. The page’s own next-actions list says to resolve them. | `#tabpanel-assumptions`; no `button[data-decision]` in the visible assumptions tab. |
| `/findings` | Header says “24 findings,” but the first table row is `F-002`; `F-001` exists only in the packet as the SBT readiness flag. No explanation of the gap. | Findings table; packet “Readiness flags (1)” → `F-001`. |
| `/findings` | Source paths are truncated to 104 px with only a `title` tooltip. On touch, the full path is unavailable until the row is selected and the detail panel is read. | `.findings-table code`; caption says “full path in the tooltip.” |
| `/findings` at 390 | The detail panel sits **above** the 24-row table, and only the far-right `Inspect` link changes it; the row itself is not clickable. A first-time viewer who taps a row (the first row is styled `selected`) gets no change. `Inspect` does correctly scroll to and focus the detail. | `.finding-layout`; `tbody tr` has `cursor: auto`; `Inspect` → `#finding-detail-heading` focused and detail scrolled to top (`scrollY 1158`). |
| `/packet` | The page promises a 6-section packet with a “full hash-chained audit trail” and “Complete evidence set (126 items),” but the rendered page shows summary tables and hashes, not the 126-item evidence list or the 9-event audit list. | `/packet?run=R-DEMO-001` section 06 and “Hashes and audit”; `Audit events: 9`. |
| `/migrator` | Actual five-agent stage panel starts at **2,109 px** at 1440 and **4,078 px** at 390—after hero, boundary, bounded-autonomy, “what am I looking at,” human to-do, approval cards, progress, and cycle. The page is titled “Watch the migration crew work.” | `#agent-stage-scout` top: 2109 at 1440, 4078 at 390. |
| `/migrator` | Guardian displays “7/7 deterministic checks passed” but its WORK panel lists only 3 checks; Critic later lists the same 7. | `#agent-stage-guardian` machine-check card. |
| `/migrator` stage 5 | “SEAL HASH CHECK **7/8 match** · log appended” with a page titled “Sealed bundle.” The one non-match is the append-only agent log. No explicit “this is expected, not tampering” sentence; the note only explains the 8 files. | `#agent-stage-scribe` seal check; agent-log row “append-only · grown since seal.” |
| `/migrator` | The 8 bundle files are not all downloadable; only Plan JSON, Migration report, Bundle manifest, and Review audit JSON appear. Target drafts are visible as paths but not individually downloadable. | `.bundle-downloads`; stage 5 table. |
| `/migrator` | “Scribe seals the plan, report, bundle manifest, and hash-chained agent log” conflicts with “Bundle manifest … wrapper · not a sealed content file.” | Hero lede vs stage 5 “BUNDLE MANIFEST — SEPARATE WRAPPER.” |
| `/migrator` | Next actions say verify **12** audit events; packet says audit chain **9 events**. The footnote says the packet has its own chain, but the packet does not repeat that distinction. | `/migrator` “Agent log: 12 events”; `/packet` cover “Audit chain verified: yes (9 events).” |
| `/migrator` | The first 8 of 31 evidence links are shown; there is no “view all” control. EV links open raw JSON (`/api/runs/R-DEMO-001/evidence/EV-0001`) rather than a readable evidence view. | `#agent-stage-scout`; `.evidence-link`. |
| `/codebase?case=cascade-mutual` / `harbor-pc` | Key tabs start **1,923 px** down at 1440 and **2,925 px** at 390; the work is behind hero, boundary, two banners, approval cards, case switcher, explanation, narrative, next actions, summary strip. | `[data-codebase-tabs]` top: 1923 / 2925. |
| `/codebase` → Source findings | The table is **1,412 px** wide in a **1,110 px** container at 1440; **1,412 / 332** at 390. The hint is always hidden, so the Message tail and Cloud target column are invisible with no affordance. | `#cb-findings [data-table-scroll]`; `#cb-findings [data-scroll-hint][hidden]`. The hint is separated from the table by `.table-caption`, so the generic `syncScrollRegion()` never finds it. |
| `/codebase` → Patches | 21 patches, all pending, but the only actions are Download patch / bundle / report / SARIF / audit. There is no Accept, Reject, or Defer control, despite the approval language. | `#cb-patches .patch-card`; no `[data-decision]`. |
| `/codebase` → Gates | “11 gates open · 21 patches pending” but no gate/patched decision controls. The page tells a human to accept/reject/defer every change and provides none of those controls. | `#cb-gates .gate-card`; no action button. |
| `/codebase` | “The value is not a score” is followed by “Target score 60/100,” “Target score 100/100,” and “0 before / 100 structural after / 71 after human gates.” | Codebase explain panel; iteration cards; Planner report. |
| `/codebase` | “bundle generation 1 · 2 iterations” is unexplained; “generation” is never defined. | `.head-meta` badge. |
| `/codebase?upgrade=…` | After **Apply and re-run**, the card says “compatible,” all checks PASS, and yet “Green signal invalidated: yes” and “2 patch(es) affected.” The header still says generation 1 while the card says 1 → 2. | `#cb-upgrade .impact-card`; `.head-meta`. |
| `/codebase?upgrade=…` | “Record revalidate” reports `resume_requested` (internal token) and leaves the signal cleared. The primary-looking action records a request; it does not revalidate. | `[data-upgrade-resume][data-choice="revalidate"]`; `[data-upgrade-resume-status]`. |
| `/codebase?upgrade=…` | The “compatible” state offers “Retain the green bundle with a revalidation note” but the buttons are only Record revalidate/rollback/defer. There is no Retain button. | `#cb-upgrade .resume-card`; button row. |
| `/codebase?upgrade=…` | Navigating away to `/codebase?case=harbor-pc` or `/case-studies` shows machine-green again; the invalidation is query-only. | Default codebase head; Case Studies outcome cards. |
| `/case-studies` | “Two completed migrations you can explore” directly conflicts with the reality boundary “not an actual migration.” | H1 vs `.banner-boundary`. |
| `/settings` | “Qusar 2026.08 (review context)” is unexplained; “8 scored demo rules, 2 thesis-only rules” is unexplained; “SBT” is undefined. | `.migration-facts`; review-context table. |
| `/settings` | Live is **enabled**, but every run page says **“Reasoning: offline”** and the assistant says **“model off.”** No label distinguishes capability from this-run mode. | Settings status `enabled`; `.badge-offline`; `.assistant` status. |
| `/about` | Glossary defines 10 terms but omits PCF, Qusar, GWCP, Cloud Assurance, Cloud Retrofit, APD App, SBT, Olos, GUnit, MiMo, work package, target draft. | `#glossary`; page text. |
| `/about` | The full disclaimer paragraph is repeated in the page body and the global footer. | “Full disclaimer” section vs `.footer-line`. |
| `/runs` | “succeeded” is displayed without saying the analysis run succeeded, not a migration. | Runs table. |
| `/evaluation` | “24 findings / MICRO-F1 1.00” and “M6 Finding micro-F1 (2TP / (2TP+FP+FN))” mix findings count with a generic F1 formula; “6/8 top-8 allowance” is not self-explanatory. | Evaluation summary strip and M6 card. |
| Every page | Primary navigation is an `<aside aria-label="Primary navigation">`, not a `<nav>`/`role="navigation"` landmark. | `aside.sidebar`. |
| Every page | Skip link becomes visible on Tab but activating it moves focus to `BODY`, not `#main`; `main#main` lacks `tabindex="-1"`. | `.skip-link` → `#main`; after Enter `document.activeElement.tagName === "BODY"`. |

---

## 5. Defect log

### High

**H1. The codebase Source-findings table is clipped at every width and never shows its scroll cue.**
`#cb-findings [data-table-scroll]` is 1,412 px wide vs 1,110 px at 1440, 950 px at 1280, 694 px at 1024, and 332 px at 390. `#cb-findings [data-scroll-hint]` stays `hidden` at all four widths. The hint element is followed by `.table-caption`; the table is not its immediate next sibling, so the shared `syncScrollRegion()` never finds it. At 1440 the Message tail and Cloud target column are invisible; at 390 the table is mostly off-screen. This is both an overflow and an accessibility failure because touch users get no cue.

**H2. The announced human gates are not actionable.**
`/migrator` says “11 review gates remain open,” “every change waits for a human,” and “Resolve 3 open assumptions.” `/codebase` says “10/11 gates open” and “22/21 patches pending,” with “A person must still accept, reject, or defer every change.” But:
- `#agent-stage-guardian` gate cards have no controls.
- `#cb-patches .patch-card` has no accept/reject/defer controls.
- `#tabpanel-assumptions` has no controls.
- Reconstruction mapping/change/finding dialogs do have controls, but not assumptions.
This is a claim/action mismatch, not just a missing label.

**H3. Upgrade invalidation contradicts itself and does not persist.**
The initial stale state is clear, but after **Apply and re-run the loop** (`[data-upgrade-rerun]`) the card says **compatible**, all checks PASS, and still says **“Green signal invalidated: yes”**; the header badge still says **bundle generation 1** while the card says **1 → 2**; the “Retain” resume option has no corresponding button. Navigating away to the default codebase page shows machine-green again. The `?upgrade=…` query is a preview, not a persisted invalidation. This makes Q9 look correct in one state and wrong in the next.

**H4. Package evidence is inert and the packet does not render its evidence appendix.**
`#agent-stage-architect .package-table td:nth-child(5)` shows `EV-0011 EV-0018` as plain code, not links. The packet claims 126 evidence items and a full audit trail, but `/packet?run=R-DEMO-001` renders hashes and summary tables, not the 126 items or 9 events. A reviewer can see evidence IDs, but cannot follow the claimed chain from package to source from the page.

### Medium

**M1. One page, three names.**
- “Agent loop” (sidebar) → “Migrator” (breadcrumb) → “Watch the migration crew work” (H1).
- “Migration stories” (sidebar) → “Case studies” (title) → “Two completed migrations you can explore” (H1).
- “Review packet” (sidebar) → “Packet” (breadcrumb) → “Review packet” (H1).
A no-context reviewer looking for “Migrator” or “Case studies” has to infer the mapping.

**M2. “Disposition” has two incompatible meanings.**
Reconstruction says “12 explicit dispositions” and labels the table column **Disposition** with values `mapped_transformed` / `mapped_exact`, while **State** says `pending`. About’s glossary says a disposition is “the recorded decision about a finding or mapping: accept, reject, edit, or defer, with a written reason.” The reviewer cannot tell whether the 12 mappings are decided (dispositions) or undecided (pending), and Migrator calls the same set “12 dispositions.”

**M3. The three-unknown sets do not match.**
- Workbench `.gap-card`: territory; rating inputs; **duplicate PAVehicleDV screen** (no IDs).
- Migrator Guardian: `G-01` territory; `G-02` rating inputs; **`G-03` 37-character APD type**.
- Reconstruction/Packet: `A-01` territory; `A-02` rating inputs; **`A-03` 37-character APD type**.
The third item differs between Workbench and the other pages, and the A/G IDs are never cross-referenced. “Every unknown has a name” is undermined by the three naming schemes.

**M4. Counts do not reconcile without private knowledge.**
- `31 evidence records` (Workbench) vs `31 evidence links` (Migrator) vs `101 evidence records` (Migrator estate) vs `126 items` (Packet).
- `5 work packages` vs `5 target drafts` vs `5 target changes` vs `5 target files`.
- `8 bundle files` vs 4 download links vs “8 sealed content files” vs “7/8 match”; stage 2 already tells Guardian “5 work packages and 8 bundle artefacts” before Scribe has produced them.
- `9 audit events` (packet) vs `12` (migrator agent log).
The product has explanations scattered across stages, but no single reconciliation table.

**M5. Guardian and Critic both claim 7/7.**
`#agent-stage-guardian` says “MACHINE CHECKS 7/7 deterministic checks passed · verdict passed,” but its WORK list has 3 items: assumption gates, finding gates, no self-approval. `#agent-stage-critic` then lists seven named checks. The page does not say whether these are the same seven or two different sets.

**M6. “Scribe seals” vs “manifest is a wrapper.”**
The hero says Scribe seals the bundle manifest; stage 5 says the manifest is a separate wrapper and “not a sealed content file.” The stage 5 seal check also reads **7/8 match**, not 8/8. It is transparent, but the terminology makes the seal sound broken.

**M7. “The value is not a score” is immediately contradicted by scores.**
Codebase explain: “The value is not a score. It is a traceable list…”. Same page: “Target score 60/100,” “Target score 100/100,” “0 BEFORE / 100 STRUCTURAL AFTER / 71 AFTER HUMAN GATES.” The qualifier “not a Cloud Assurance score” is below one of them. Pick one framing.

**M8. Findings start at F-002.**
`/findings` says “24 findings”; the first row is `F-002`. `F-001` exists only in the packet (`F-001 Standards Based Template readiness flag`); the Findings page calls it `PF-GW-SBT-001` with no F-001 label. A reader cannot map 24 findings to 24 IDs.

**M9. Only the far-right “Inspect” link selects a finding; the row is not a control.**
At 390 the detail panel is above the table, and `Inspect` correctly scrolls to it and focuses `#finding-detail-heading`. But the row itself has `cursor: auto`, does nothing when tapped, and the first row is already styled `selected`. A reviewer who taps the highlighted row will see no change. The `View detail` anchor is a separate upward jump. Make the row a link/button or make the Inspect affordance unmistakable in every row.

**M10. Primary navigation has no navigation landmark; skip link does not focus main.**
`<aside class="sidebar" aria-label="Primary navigation">` is a complementary landmark, not `nav`. Pressing Tab reveals `.skip-link`, Enter sets `#main` in the URL but active element becomes `BODY`; `main#main` has no `tabindex="-1"`. Screen-reader and keyboard users do not get the promised skip behavior.

**M11. The live/offline status is ambiguous.**
`/settings` says **enabled** and **mode: live**; `/migrator` and `/codebase` badges say **Reasoning: offline**; the Workbench assistant says **retrieval-only - model off**; the footer says **offline by default**. A no-context reviewer cannot tell whether live reasoning is on, off, or only available.

**M12. Essential terms are missing from the glossary.**
Defined: evidence link, feature, disposition, assumption, gate, SARIF, Gosu, APD, Cloud Data Access, App Events. Missing in actual UI copy: **PCF, Qusar, GWCP, Cloud Assurance, Cloud Retrofit, APD App, SBT, Olos, GUnit, MiMo, work package, target draft, target change, generation**. Several are load-bearing for Q1, Q3, Q9, and Q10.

**M13. “37 vs 24” is a riddle, not a metric.**
The home summary strip says “37 vs 24 / LONG TYPE VS APD LIMIT.” The units are characters; the meaning is explained only in a paragraph lower on the page. A first-time viewer can read it as 37 findings vs 24 findings.

### Low / polish

- `#manifest` checkbox `input[name="excluded"]` is 13 × 13 px; its `label.check-inline` is 19.5 px high. Below the 24 × 24 WCAG 2.5.8 target minimum.
- `.evidence-link` in `#agent-stage-scout` is 51 × 15 px; inline-link exception may apply, but table-cell links are easier to hit at a larger size.
- `.mapping-table a` repeated “source” links are 43 × 15 px and share identical accessible names; a screen-reader link list shows five “source” items with no mapping ID.
- `.rule-summary-item` on `/findings` looks like filter chips but is a `<span>` with `cursor: auto`; nothing happens when clicked. Add “summary” label or make them filters.
- `progress[data-migration-bar]` has no accessible name; the adjacent `[data-migration-label]` is not associated via `aria-labelledby`.
- `#agent-stage-guardian .gate-list.compact` is 360 px tall with 529 px of content (673 px at 390); G-03 is clipped below the fold inside the inner scroll. It is focusable (`tabindex="0"`), but there is no visible “more below” cue.
- `#cb-loop` “bundle generation 1 · 2 iterations” uses “generation” with no definition; a reader may read it as “one bundle generation, two attempts.”
- `Replay loop` on `/codebase` briefly marks both iteration cards `is-active` at once, then clears them; it is a visual highlight, not a step-by-step replay. Label or sequence it more clearly.
- `/case-studies` has no jump links for the two long cards; the page is 7,393 px at 390. Not a correctness issue, but the first card’s details are far from its title.
- `/about` repeats the entire disclaimer in the body and the footer.
- The Case Studies H1 and the Workbench “Run … succeeded” phrasing both imply a completed real-world event that the reality boundary then denies.
- The Workbench “31 evidence records” and Migrator “31 evidence links” should say “feature evidence links” and “estate evidence records,” or show a legend.

---

## 6. Console, network, overflow, and interaction checks

**No console errors, page errors, or failed requests** were observed in scripted interaction across:
Workbench spine selection; assistant questions; Manifest filter/Apply; Reconstruction accept dialog (opened, cancelled); Findings row selection and Accept dialog (opened, cancelled); Migrator stage switching, replay, and stage panel; Codebase tab switching, iteration replay, patch expansion, upgrade evaluation, Record revalidate, Apply/re-run; Settings Test connection; mobile nav open/Escape; feature filter; skip link.

**Downloads:** all tested endpoints returned 200 with the expected type:

- `/packet/export?run=R-DEMO-001` → HTML attachment.
- `/api/runs/R-DEMO-001/audit` → JSON.
- `/api/codebase/cases/harbor-pc/bundle.zip` → ZIP attachment (31 KB).
- `/api/codebase/cases/harbor-pc/report` → Markdown.
- `/api/codebase/cases/harbor-pc/sarif` → `application/sarif+json`.
- `/api/codebase/cases/harbor-pc/patches/CP-001` → `text/x-diff` attachment.
- `/api/runs/R-DEMO-001/migration/file?path=migration/...` → JSON/Markdown attachments.

**No document-level horizontal overflow** was observed at 1440, 1280, 1024, or 390. All overflow is inside scroll regions. Observed intentional/contained scrolls:

- Feature spine graph: 672/662 at 1280, 672/406 at 1024, 672/330 at 390; the graph hint is visible at all three widths.
- Migrator stage 1 evidence table: 1,339/1,110 at 1440 and 1,339/332 at 390; hint visible.
- Migrator stage 2 package table: 1,094/332 at 390; hint visible; only ID and part of Target are visible without scrolling.
- Reconstruction mapping table: 1,040/950 at 1280, 1,040/694 at 1024, 1,040/332 at 390; hint visible, but State can be hidden under the sticky Decision column.
- Codebase Source-findings table: 1,412/1,110 at 1440, 1,412/950 at 1280, 1,412/694 at 1024, 1,412/332 at 390; **hint hidden at all four widths** (H1).
- Codebase artifact table: 820/332 at 390; hint visible.
- Findings table: 800/764 at 1440 and 800/332 at 390; hint visible.
- Packet tables: up to 820/332 at 390; hints visible where needed.

The two real defects are the hidden cue on the codebase findings table (H1) and the State column hidden under the pinned decision column on the reconstruction table.

**Performance:** initial page loads were about 0.55–0.67 s on the local instance; HTML transfer 12–111 KB; DOM 182–1,654 nodes. Nothing blocked or timed out.

---

## 7. What is genuinely working well

- The **What it is / What it is not / Three promises** panel is strong no-context framing.
- The **five-agent received/produced panels** are the clearest part of the product; Guardian’s “deliberately not received” list is excellent.
- **Machine-green vs human approval** is stated plainly in several places; the repeated Cloud Assurance boundary is responsible, not marketing.
- **Selected node evidence** (file, locator, excerpt, method, excerpt SHA) and the **assistant refusal** are excellent evidence-first patterns.
- **Replay** works: top Replay starts at Scout and advances every 1.6 s; Play/Next/Back/Reset work; status is announced.
- **Mobile navigation** works with `aria-expanded`, Escape closes it, and links are 39.5 px high.
- **Tabs** support ArrowLeft/ArrowRight/Home/End and roving `tabindex`.
- **Dialogs** focus the reason textarea, use native `<dialog>`, and require a reason.
- **No console errors**; downloads and the Test connection work.
- The **reality boundary** is repeated at the right moments, even if the Case Studies title undermines it.

---

## 8. Priority fixes

1. **Make human gates actionable or say they are external.** Add assign/accept/reject/defer (with reason) to assumption gates, codebase patches, and codebase gates; otherwise change “what a human must do next” to “what an external owner must do next” and point to where.
2. **Fix the codebase findings scroll cue.** Move `[data-scroll-hint]` directly before `[data-table-scroll]` or make `syncScrollRegion()` find it through the caption. This is a one-line class of bug with a serious desktop and mobile impact.
3. **Make upgrade invalidation consistent and persistent.** Reconcile `compatible` vs `invalidated: yes`; update the generation badge; add the missing Retain action; persist or clearly label the `?upgrade=…` preview; replace `resume_requested` with a human phrase.
4. **Reconcile vocabulary and counts.** Add a single legend for feature evidence link / estate evidence record / packet item; work package / target draft / target change / target file; bundle file / sealed content / manifest wrapper; review audit event / agent log event.
5. **Fix the three unknown sets.** Give the Workbench gaps IDs; map gaps to assumptions to gates; use one prefix or show an explicit crosswalk. Add “duplicate PAVehicleDV screen” to the assumption register or remove it from the estate-gap count.
6. **Make evidence reachable.** Link package `EV-…` IDs to `/api/runs/.../evidence/...`; show the 126-item packet appendix and the 9 audit events; add a source-file view or at least a “copy evidence record” action.
7. **Move the work above the fold.** Collapse the repeated “read this first” / boundary / approval blocks or add a sticky section jump (“Loop / Findings / Patches / Gates / Upgrade”) so the tabs are reachable before 2,000 px.
8. **Fix the mobile Findings relationship.** When a row is selected, scroll to or focus the detail panel (or put the detail below the selected row on narrow screens).
9. **Fix accessibility basics.** Make `main#main` focusable and move skip-link focus; add a `nav` landmark for primary navigation; enlarge the 13 px excluded checkbox; add an accessible name to the progress bar; give repeated “source” links context.
10. **Tighten no-context terms.** Add PCF, Qusar, GWCP, Cloud Assurance, Cloud Retrofit, APD App, SBT, Olos, GUnit, MiMo, and generation to the glossary; add F-001 to the Findings page; clarify “the value is not a score” vs visible readiness numbers.

---

## 9. Screenshot index

All under `docs/audits/screenshots/no-context-round3/`.

| Screenshot | What it shows |
|---|---|
| `01-workbench-1440-viewport.png`, `07-workbench-390x844-full.png` | Home/Workbench at desktop and the full mobile stack. |
| `03-migrator-stage-1-1440.png` … `03-migrator-stage-5-1440.png` | All five feature-loop stage panels, including Guardian 7/7 and Scribe 7/8. |
| `04-migrator-top-replay-complete-1440.png` | Replay at Scribe after the top Replay control advanced through five steps. |
| `03-migrator-stage-3-1440.png`, `18-migrator-guardian-1440x900.png` | Guardian gates and the 7/7 claim with only three listed work items. |
| `03-migrator-stage-5-1440.png` | 8 bundle files, manifest wrapper, 7/8 seal check, append-only agent log. |
| `05-codebase-cascade-mutual-findings-1440.png` | Cascade findings tab: table clipped at 1440 with no hint. |
| `05-codebase-harbor-pc-findings-1440.png`, `26-findings-390x844.png` | Harbor findings at desktop; 390 findings page with detail above table. |
| `05-codebase-harbor-pc-patches-1440.png` | 21 pending patches with no accept/reject/defer controls. |
| `05-codebase-harbor-pc-gates-1440.png` | 11 human gates, 21 pending patches, Planner report. |
| `06-codebase-harbor-upgrade-stale-1440.png`, `16-codebase-upgrade-stale-390x844.png` | Stale-green banner and revalidation-required upgrade before re-run. |
| `31-codebase-upgrade-compatible-1440.png` | Post-rerun “compatible” card that still says “Green signal invalidated: yes.” |
| `29-codebase-upgrade-revalidate-recorded-1440.png` | `Recorded revalidate: resume_requested` status. |
| `27-reconstruction-scrolled-1280.png`, `12-reconstruction-table-1280x720.png` | Reconstruction table at 1280; state column hidden under sticky actions. |
| `19-reconstruction-reject-dialog-1440.png`, `13-reconstruction-accept-dialog-1440.png` | Decision dialogs with required reason and rejection-creates-assumption copy. |
| `22-manifest-excluded-1440.png` | Excluded-file filter and “4 matching” state. |
| `23-evaluation-390x844.png` | Evaluation at 390; dense metric stack and holdout label. |
| `02-packet-1440.png` | Packet hashes and summary; no rendered 126-item appendix or 9-event list. |
| `07-case-studies-390x844-viewport.png` | “Two completed migrations” directly above “not an actual migration.” |
| `02-settings-1440.png`, `17-settings-test-connection-1440.png` | Live endpoint/key instructions; Test connection success. |
| `07-about-390x844-viewport.png` | About/“what it is not” and glossary entry point at mobile. |
| `11-mobile-nav-open-390x844.png` | Mobile Sections menu expanded. |
| `33-skip-link-focus-1440.png` | Skip link visible on focus. |
| `36-findings-inspect-390x844.png` | Mobile Inspect action: detail panel scrolled into view and heading focused. |
| `35-workbench-filter-zzz-1440.png` | Feature filter empty state. |

**Total screenshots:** 164 images in the folder, covering the requested 1440 × 900, 1280 × 720, 1024 × 768, and 390 × 844 widths plus interaction states.
