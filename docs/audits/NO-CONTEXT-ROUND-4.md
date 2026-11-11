# No-context audit — Round 4

**Auditor stance:** a smart reviewer who knows nothing about Guidewire, Gosu, APD, Cloud Data Access, App Events, Cloud Assurance, or PreFlight.
**App:** `http://127.0.0.1:8000` — demo run `R-DEMO-001`, synthetic fixture `demo-slice-300`.
**Date:** 2026-11-11.
**Viewports:** 1440 × 900, 1280 × 720, 1024 × 768, 390 × 844 (Chromium/Playwright, 100% zoom).
**Screenshots:** `docs/audits/screenshots/no-context-round4/` (102 images; the key images are indexed at the end).
**Method:** answers below come from the rendered screens. I consulted source only to name exact DOM selectors and confirm which view model feeds a label; I did not use source to decide the answers. I did not edit product code, tests, or existing docs.

**Disclosure:** I evaluated the Harbor upgrade, clicked **Request revalidation**, clicked **Apply and re-run the loop**, and then used **Run fresh** to restore Harbor's default green state. Those actions changed in-memory page state, not product files. I also clicked **Test connection** once on Settings; it returned `OK · mimo-v2.6-flash · 3492 ms` and exposed no key. I did not run a live model call.

---

## 1. Verdict

This is the best version of PreFlight so far. The case-study headline no longer says "completed migrations", the codebase tabs are near the top of the page, the Source-findings scroll cue is visible, finding evidence rows exist, and the packet now renders a 126-item evidence appendix and 9 audit events.

It is still not a no-context product. The main remaining problems are **not missing features**; they are places where the screen tells a reviewer what to do and then gives them nowhere to do it, or where a label is fed by the wrong data:

- **The Guardian stage in the feature loop reports `7/7 deterministic checks passed` while its own WORK list contains only 3 items, and Critic reports the same 7/7.** A reader cannot tell who ran the seven checks.
- **The new codebase evidence rows are clipped inside the 1,412 px findings table.** At 390 the evidence body is 1,400 px wide inside a 332 px window; the excerpt, source, and fingerprint are cut off.
- **The human gates and patches still have no accept/reject/defer controls**, including the feature-loop assumptions tab. The new caveat ("use the review workflow") has no link or destination.
- **The packet page claims a section-03 excluded-files table and section-05 source path:line/excerpts that it does not render.** The downloadable HTML contains them; the in-app packet does not.
- **The post-rerun upgrade state still mixes `bundle generation 1` with `evaluated generation 2`**, and its **Retain** card says the upgrade does not touch the bundle's affected rules while the card above says 2 patches require regeneration.

**Overall: 5.9/10. No-context explainability: 5.5/10.** Deliberately harsh: 6 means usable with effort, not excellent.

### What is fixed since Round 3

| Round-3 problem | Current state |
|---|---|
| Codebase tabs buried below the fold | Tabs start at **463 px** at 1440 (was 1,923) and **1,134 px** at 390 (was 2,925). Screenshot `07`, `26`. |
| Hidden Source-findings scroll cue | Hint is visible at 1440, 1280, 1024, and 390; table is still 1,412 px wide. Screenshot `08`/`28`. |
| No finding evidence rows | Rows expand to an excerpt, source, fingerprint, SHA, claim, and remediation (but are clipped; see H2). Screenshot `09`, `29`. |
| Packet appendix absent | In-app packet renders **126** evidence rows and **9** audit rows. Screenshot `18`. |
| Package evidence IDs inert | Package `EV-…` IDs are links (to raw JSON). Screenshot `04` stage 2. |
| Case Studies "completed migrations" headline | H1 is now **"Two completed migration rehearsals you can explore."** Screenshot `16`. |
| Upgrade rerun said "invalidated: yes" and had no Retain button | Re-run now says **compatible**, no stale banner, and offers **Record retain decision**. Screenshot `14`/`15`. |
| `resume_requested` internal token | The status is now a human sentence: `Response recorded as revalidate; this demo does not persist it…`. Screenshot `13`. |

---

## 2. The ten questions, answered from the screen

### Q1. What is PreFlight, and what is it not?

**What it is.** PreFlight describes itself as a **local, read-only review tool for a Guidewire-style insurance codebase before a cloud migration**. It reads a snapshot, groups the code into features, links claims to source evidence, names unknowns, and shows what a safe change would touch. It never edits the source and never deploys. The About page adds that it is an independent academic research prototype.

**What it is not** (Workbench "WHAT IT IS NOT", About "What it is not", and the persistent boundaries):

- Not an official **Cloud Assurance** result, score, or certification.
- Does not convert products to **APD**, and does not replace **Cloud Retrofit**.
- Not a generic Gosu linter; SonarQube and Cloud Assurance own generic linting.
- Not a live-tenant connector or deployment tool.
- Not an autonomous approver: every draft, mapping, and patch stays pending.
- The **Migrator** is a draft generator: it writes a local, non-deployable bundle and leaves every change pending.

Evidence: `01-workbench-1440x900.png`, `20-about-1440x900.png`, top badges **Synthetic estate**, **Official Cloud Assurance: not run**.

Unresolved no-context terms in this answer: **Cloud Assurance**, **Cloud Retrofit**, and **APD App** are used but not defined in the plain-language glossary. **PCF**, **Qusar**, **GWCP**, **SBT**, **GUnit**, **MiMo**, **work package**, **target draft**, and **generation** are also absent from `#glossary`. See M7.

### Q2. What are the five agents, and what does each receive/produce?

There are five agents in each loop. The first four roles are shared; the fifth changes name.

| Agent | Feature loop (`/migrator`) | Codebase loop (`/codebase`) |
|---|---|---|
| **Scout** | Receives the completed review, source manifest, evidence graph, findings, dispositions. Produces **PA-VEH-01 · Vehicle Information**, **31 evidence links on this feature**, **101 evidence records across 300 files**, 24 findings, 12 dispositions. | Receives the read-only case snapshot, cloud-blocker rule pack, and file classification. Produces **15 files / 160 LOC** (Harbor) or **17 files / 156 LOC** (Cascade), 20/18 line-located blockers, 6 custom slices. |
| **Architect** | Receives Scout's scope, 12 dispositions, and evidence IDs. Produces **5 work packages / 5 target files**; all pending. | Turns blocker families into **21 patches / 23 target files** (Harbor) or **22 patches / 24 target files** (Cascade), plus cloud config and unified diffs. |
| **Guardian** | Receives packages, open assumptions/findings, rule pack. Deliberately does not receive Scout narrative, Critic verdict/fixes, or model text. Produces **11 human gates** (3 assumptions + 8 rule groups), 6 high impact; deployment blocked. | Re-scans the generated target; produces **13 deterministic checks**, verdict green at the final pass, and opens the named human gates. |
| **Critic** | Receives Scout evidence summary, Architect packages/targets, Guardian gate register. Produces **7 machine checks passed**, verdict PASS, 0 auto-approvals. | Applies every displayed diff, checks coverage/source immutability, and records **7 checks** plus **11/10 named human gates**. |
| **Scribe / Planner** | **Scribe** seals the plan, report, bundle manifest, and hash-chained agent log. | **Planner** compiles the executive report, readiness, SARIF 2.1.0, and next actions. It is the same sealer role under a different name. |

Evidence: `04-migrator-stage-1-scout-1440x900.png` through `04-migrator-stage-5-scribe-1440x900.png`; `07-codebase-cascade-loop-1440x900.png`; `10-codebase-harbor-loop-1440x900.png`.

**Defect in this answer:** the Guardian stage displays `MACHINE CHECKS 7/7 deterministic checks passed · verdict passed` in `#agent-stage-guardian .status-card.status-machine`, but its WORK column lists only three checks (assumption gates, finding gates, no self-approval). Critic displays the same 7/7. The 7 checks are Critic's checks; the Guardian panel is mislabeled. This is H1 and it directly undermines Q2, Q3, and Q5.

### Q3. Why 5 packages, 11 human gates, 7 machine checks, 8 bundle files?

The screen gives the decomposition, but not one reconciliation sentence:

- **5 packages** = five target artefacts, one per work package: `WP-01` schema, `WP-02` mapping, `WP-03` updater, `WP-04` codegen config, `WP-05` API contract. They correspond to five target drafts/files and packet changes `C-01`…`C-05`. Screenshot `04-migrator-stage-2-architect`.
- **11 human gates** = **3 assumption gates** (`G-01`…`G-03`) + **8 rule groups** (`G-04`…`G-11`), one per rule with 3 findings. 6 are high impact. All 5 generated changes remain pending. Screenshot `04-migrator-stage-3-guardian`, `38-migrator-guardian-gates-390x844`.
- **7 machine checks** = Critic's checks: packages exist; all package files generated (5/5); no `_gen` targets; no duplicate targets; generated JSON/YAML parses (5 files); every package is evidence-linked (5/5); human approval retained (0 auto-approved). Screenshot `04-migrator-stage-4-critic`.
- **8 bundle files** = 5 target drafts + plan + report + agent log. The **bundle manifest is a separate wrapper** and is not one of the 8. The seal check is **7/8 match · log appended** because the agent log is append-only and has grown since seal. Screenshot `04-migrator-stage-5-scribe`.

The count **7/8** is not a failed seal, but the page still requires the reader to infer that from the note. It never says "expected, not tampering." The stage-5 "Bundle contents" table has no links; Plan and Report are linked in the seal cards above, the five target files are downloadable from the stage-2 package previews, and the manifest is linked at the bottom. The **agent log** is not a link anywhere on the page, so one of the eight sealed content files cannot be downloaded from the UI.

**The feature-loop counts do not describe Cascade/Harbor.** Cascade has 18 blockers / 22 patches / 2 iterations / 10 gates; Harbor has 20 blockers / 21 patches / 2 iterations / 11 gates. The same words ("gates", "patches") mean different loops. The page does say "feature loop" and "codebase loop", but the counts are not reconciled in one place.

### Q4. What is the difference between Scribe and Planner?

They are the **same sealer role in two loops**:

- **Scribe** (feature loop, `/migrator` stage 5) writes/seals the plan, report, bundle manifest, and hash-chained agent log. Sealing is not approval.
- **Planner** (codebase loop, `/codebase` stage 5) compiles the executive report, readiness indicator, SARIF summary, and next actions after Guardian and Critic agree.

The Workbench says this explicitly: "Both loops use the same first four roles. Only the sealer changes name: Scribe in the feature loop, Planner in the codebase loop." The Codebase page repeats it. This part is clear. The remaining wrinkle is that Scribe's description says it writes the bundle manifest, while stage 5 labels the manifest a separate wrapper "not a sealed content file" (M5).

### Q5. What does machine-green mean, and what must a human do next?

**Machine-green** is a machine result, not approval. On Cascade/Harbor it means Guardian's 13 deterministic checks and Critic's 7 independent checks agree: **20/20 passed**, Planner compiled the report, and every patch remains pending. The page repeats "A machine-green result is not human approval" and "Not an official Cloud Assurance result."

What a human must do next is explicit in the list:

- **Codebase loop:** review the named gates `CR-01`…`CR-10` (Cascade) or `CR-01`…`CR-11` (Harbor) with their owners; accept, reject, or defer every patch; resolve affected rules; revalidate after a release upgrade. Harbor: 11 gates open, 7 high impact, 21 patches pending. Cascade: 10 gates, 22 patches pending.
- **Feature loop:** assign owners to 3 unassigned assumption gates; resolve 3 assumptions; accept/reject the 12 mappings; review the 5 packages; verify the 12-event agent log. 11 gates open, 5 changes pending.

**The blocker:** these are to-do lists, not actions. The gate cards (`#cb-gates .gate-card`) and patch cards (`#cb-patches .patch-card`) have no accept/reject/defer controls, and the Reconstruction assumptions tab (`#tabpanel-assumptions`) has no controls either. The page says "Use the review workflow for the case (or the pilot decision log)" but there is no link and no such page. A human is told to do things the UI cannot do. This is H3.

### Q6. What are Cascade and Harbor, and their outcomes?

They are two **synthetic codebase migration stories**, not real insurers. Both pages say "Synthetic rehearsal — not an actual migration."

| Story | Outcome shown |
|---|---|
| **Cascade Mutual** — monoline Personal Auto mutual, Cloud Retrofit without APD App | **17 files, 156 LOC, 18 source blockers, 22 patches, 2 iterations, 10 human gates**; machine-green · human gates open; readiness **0 → 100 structural → 74 after human gates**; 0 approvals. |
| **Harbor P&C** — multi-line P&C group, Cloud Retrofit + APD naming preparation | **15 files, 160 LOC, 20 source blockers, 21 patches, 2 iterations, 11 human gates**; machine-green · human gates open; readiness **0 → 100 structural → 71 after human gates**; 0 approvals. |

Case-study cards match the blocker/patch/gate counts: Cascade **18 / 22 / 2 / 10**; Harbor **20 / 21 / 2 / 11**. The in-page summary strip uses **17/15 files** (the case-study cards show custom Gosu counts, not file totals), so a reader must not confuse "18 blockers" with "17 files." Screenshots `16-case-studies-1440x900.png`, `07`, `10`.

### Q7. Where is the evidence for a claim?

Evidence is present in several forms, and is materially better than Round 3:

- **Workbench / feature spine:** select an evidence-bearing node; `Selected node evidence` shows `EV-0001`, `config/web/pcf/policy/PAVehicleDV.pcf`, xpath `/PCF/Screen/TypeKeyInput[1]:4`, excerpt, method `xml_xpath`, and excerpt SHA-256. Screenshot `02`, `41`.
- **Migrator stage 1:** shows the **first 8 of 31** evidence links with EV ID, file, locator, and excerpt. There is no "view all 31" control. Screenshot `04-migrator-stage-1-scout`.
- **Migrator stage 2:** package `EV-…` IDs are now links. They open raw JSON (`/api/runs/R-DEMO-001/evidence/EV-0011`), not a formatted evidence page. The target files are downloadable from each package preview. Screenshot `04-migrator-stage-2-architect`.
- **Packet appendix:** **126 items** (101 discovery + 25 review evidence), each with a source locator, excerpt, and method; every `EV-…`/`REV-…` link returned 200 in my link check. The **9 audit events** are also rendered. Screenshot `18`, `34`.
- **Codebase findings:** rows expand to an excerpt, source, fingerprint, excerpt SHA, claim/confidence, remediation, and SARIF/report links. Screenshot `09`, `29`. **But the evidence body is 1,400 px wide inside a 1,412 px table scroll region**, so at 1440 the source/fingerprint columns are off-screen, and at 390 almost all of the evidence is clipped. See H2.
- **No source-file viewer anywhere.** Evidence is an excerpt plus a hash; the reviewer cannot open the actual source file from the page. The package evidence links are the closest thing, and they open JSON.

The weakest remaining traceability links are: **no "view all 31" feature evidence view**, **no feature filter in the 126-item packet appendix**, and **no clickable source-file view**. The strongest are the Workbench selected-node panel, the packet appendix, and the new inline codebase evidence rows.

### Q8. Is this an actual migration? How do you know?

**No. It is a synthetic rehearsal.**

Evidence on screen:

- Persistent top badge **Synthetic estate** and **Official Cloud Assurance: not run**.
- Workbench boundary: "This is a synthetic rehearsal, not an actual migration: no tenant, no code compile or deployment, and no official Cloud Assurance result."
- Codebase boundary: "No tenant contacted · no compile or deploy · no change approved"; the reality callout says no source file was edited and no patch was applied, compiled, or deployed.
- Migrator boundary and time-stamped run: every change pending, 0 auto-approved, local non-deployable draft.
- Case Studies: both insurers are "dummy profiles with invented code, not customer data."
- Packet: "Synthetic demonstration estate."
- Run status **succeeded** means the analysis run succeeded, not that a migration happened.

**Stale contradiction:** the Workbench demo path still says **"Two completed dummy insurer migrations"** (`/`, `.demo-path`, third card) directly under a boundary that says this is not an actual migration. The Case Studies H1 was fixed, but this smaller phrase was not. Screenshot `46-workbench-demo-path-1440x900.png`. See M4.

### Q9. What happens on an upgrade mid-migration?

On `/codebase?case=harbor-pc`, choose **"APD import limit tightens from 24 to 20 characters (GWCP 2026.10 → GWCP 2027.04)"** and press **Evaluate upgrade**:

- The stale banner is clear: **"Green signal cleared by APD import limit tightens…; generation 1 → 2; revalidate/rollback/defer."**
- Status becomes **revalidation required**; the previous result is labelled **"20/20 checks passed before the upgrade."**
- The impact card says **2 patches affected**, rule `PF-CODE-APD-001`, generation 1 → 2; one check is **REWORK**: "codegen overrides fit the 20-character limit — 1 override(s) exceed 20 characters." Options are re-run Architect, roll back, or defer.
- **Request revalidation** now records a human sentence: "Response recorded as revalidate; this demo does not persist it or restore the green signal. Every patch still needs human approval." It does not actually revalidate. The label is still slightly stronger than the action.
- **Apply and re-run the loop** produces a compatible state: "Revalidation passed at generation 2… No stale-green claim remains." The previous "Green signal invalidated: yes" and missing Retain button are fixed.
- **Remaining contradictions:** the header still says **`bundle generation 1 · evaluated generation 2`** while the card says "Revalidation passed at generation 2"; the **Retain** option says "The upgrade does not touch this bundle's affected rules" while the card above says **2 patches require regeneration**; and the `?upgrade=…` invalidation is query-scoped, so navigating to `/codebase?case=harbor-pc` restores the green result without a "preview only" label.

Screenshots: `39-codebase-harbor-upgrade-stale-true-1440x900.png`, `13-codebase-harbor-revalidation-recorded-1440x900.png`, `14-codebase-harbor-after-rerun-1440x900.png`, `15-codebase-harbor-default-after-rerun-1440x900.png`, `31-codebase-harbor-upgrade-stale-390x844-full.png`.

### Q10. How do you enable live reasoning without exposing a key?

On `/settings`, **MiMo / OpenAI-compatible endpoint**:

**Short answer: no, live reasoning still needs a key; the UI never asks for or displays it.** The key is read from the environment.

- State: **enabled**, mode **live**, endpoint host `token-plan-sgp.xiaomimimo.com`, models `mimo-v2.6-flash` and `mimo-v2.6-pro`, default `mimo-v2.6-flash`, real code **synthetic only**.
- Key handling: **"No key value is displayed or requested in this UI"**; the base URL and key are read only from the environment; no key is written to the repository, logs, screenshots, or API responses. I clicked **Test connection**; it returned `OK · mimo-v2.6-flash · 3492 ms` and exposed no key.
- Use: live is opt-in per run; Migrator has **Run live · mimo-v2.6-flash** and Codebase has a model select + **Run live**. Scout, Architect, and Critic may receive grounded narrative prompts; Guardian never calls the model; ungrounded statements are dropped and counted. Only synthetic fixture text is eligible by default.
- Current run state: **Reasoning: offline** on Migrator/Codebase; the assistant says **retrieval-only - model off**. The capability is enabled, but this run did not use it.

**Gap:** when the endpoint is already configured, the page no longer shows the three environment variable names (`PREFLIGHT_LLM_MODE`, `PREFLIGHT_LLM_BASE_URL`, `PREFLIGHT_LLM_API_KEY`); only the unconfigured branch does. A reader cannot enable or change it from the screen. The footer's "offline by default" and Settings' "Live reasoning is enabled" are not explicitly reconciled as *capability vs this-run mode*. See M8.

---

## 3. Scorecard

Scale: **0 = unusable without a guided tour; 10 = a first-time viewer needs no explanation.** Deliberately harsh.

| # | Category | Score | Why |
|---:|---|---:|---|
| 1 | Purpose and first impression | **7** | Strong "What it is / What it is not / Three promises" block; boundaries are clear. Docked for undefined Guidewire/Cloud Assurance/Cloud Retrofit/APD App terms and a first screen that is already a worked example. |
| 2 | Navigation and IA | **6** | Desktop sidebar and mobile Sections menu work. But "Agent loop" / "Migrator" / "Watch the migration crew work" are three names for one page; "Migration stories" / "Case studies" / "Two completed migration rehearsals" are three names for another; primary navigation is an `aside`, not a `nav` landmark. |
| 3 | Terminology and count consistency | **5** | 31 "evidence records" are actually 31 feature links; 101 records are estate-wide; 126 appendix items include 25 review records. "References" (11) is undefined, the three gap/assumption sets do not match, Guardian and Critic both say 7/7, and "The value is not a score" sits above three scores. The packet appendix now reconciles 126/9 once you find it. |
| 4 | Workbench usability | **6** | Excellent selected-node evidence panel and a genuinely useful assistant refusal. Docked for the mislabeled 31 "records", the unexplained 11 references and 37 vs 24 units, the gap/assumption mismatch, and a mobile page that is 5,944 px long before the gaps. |
| 5 | Five-agent explainability | **6** | Received/produced panels are the best part of the product; Scribe/Planner is now explicit. Docked heavily for Guardian's 7/7 label being Critic's data and for Guardian's 3-item WORK list. |
| 6 | Migrator replay, next actions, bundle trust | **6** | Replay works and advances Scout→Scribe; package evidence links work; most bundle files are reachable. Docked for no gate decisions, the 7/8 seal wording, the undownloadable agent log, 12-vs-9 audit counts, and the stage-5 table being non-clickable. |
| 7 | Codebase Cascade | **6** | Tabs are near the top; 20/20, 10 gates, diffs, and patch cards are explicit; the scroll cue is fixed. Docked for clipped evidence rows, no decision controls, and "value is not a score" vs readiness scores. |
| 8 | Codebase Harbor | **5** | Same strengths, plus the upgrade story. Docked for the post-rerun generation mismatch, the Retain rationale contradiction, and the query-only stale preview. |
| 9 | Upgrade / stale-green | **5** | The initial invalidation is now clear and consistent, and the previous "invalidated: yes" contradiction is gone. Still: `bundle generation 1` vs `evaluated generation 2`, a Retain card that denies affecting the affected rules, and no "preview only / not persisted" label on the invalidation. |
| 10 | Case Studies | **7** | Specific dummy insurers, constraints, custom slices, outcome strips, and caveats. H1 is fixed. Docked for APD App / Cloud Retrofit being undefined and for a 7,414 px mobile page with no jump links. |
| 11 | Settings, About, boundaries | **6** | Key policy is clear and Test connection works; boundaries are responsible. Docked for the glossary gaps, Qusar/SBT/thesis-only terms, the duplicate disclaimer, and the enabled/offline ambiguity. |
| 12 | Responsive, visual hierarchy, accessibility, console | **6** | No document-level overflow at any tested width; mobile nav and tabs work; no console or network errors. Docked for the primary navigation landmark, skip-link focus landing on body, 30 px tabs / 28 px upgrade controls, clipped evidence, and the gate list's hidden inner scroll. |
| — | **No-context explainability (separate)** | **5.5** | Q1, Q2, Q4, Q5, Q6, Q8, and Q10 are answerable from the screen. Q3 needs synthesis and contains the Guardian mislabel; Q7 is partial and has clipped evidence; Q9 still contradicts its own generation/Retain text. A newcomer can sound informed, but not certain. |

**Average of the 12 categories: 5.9/10.** No-context explainability: **5.5/10**.

---

## 4. Defect log

### High

**H1. Guardian's `7/7 machine checks` is Critic's data, presented as Guardian's.**
- **Page:** `/migrator?run=R-DEMO-001`, stage 3.
- **Selector:** `#agent-stage-guardian .status-card.status-machine`.
- **Evidence:** `04-migrator-stage-3-guardian-1440x900.png`, `38-migrator-guardian-gates-390x844.png`.
- **Detail:** The card says `7/7 deterministic checks passed · verdict passed`; the Guardian WORK column lists only 3 checks (`assumption gates`, `finding gates`, `no self-approval`). Critic's stage lists the same 7/7 and the seven named checks. The page copy is itself inconsistent: the Workbench "five agents" line says "Guardian runs the deterministic checks and opens human gates", while the machine-gate note on the same page says "Critic runs independent machine checks." The Codebase page says Guardian re-scans and Critic runs the independent checks. The Guardian card therefore contradicts both its own WORK list and the role split the reader is asked to learn. This is a data/label bug, not a wording preference.

**H2. The new codebase evidence rows are clipped by the findings table.**
- **Page:** `/codebase?case=cascade-mutual` → Source findings.
- **Selector:** `#cb-findings .finding-evidence-body`, `#cb-findings .finding-evidence-facts`, `#cb-findings [data-table-scroll]`.
- **Evidence:** `09-codebase-cascade-finding-evidence-1440x900.png`, `29-codebase-cascade-finding-evidence-390x844.png`.
- **Detail:** The evidence body is **1,400 px wide**. The table scroll region is 1,110 px at 1440, 950 px at 1280, 694 px at 1024, and 332 px at 390. At 1440 the source and fingerprint columns are off-screen; at 390 the excerpt, source, fingerprint, and remediation are cut off. The scroll cue above says to scroll for the Message and Cloud target columns, not that the expanded evidence itself is also 1,400 px. The feature is new and useful, but the verification surface is not usable without horizontal hunting.

**H3. Announced human gates have no decision controls, and the promised workflow has no destination.**
- **Pages/selectors:** `/codebase?case=…` → `#cb-gates .gate-card`, `#cb-patches .patch-card`; `/reconstruction?run=R-DEMO-001&tab=assumptions` → `#tabpanel-assumptions`; `/migrator?run=R-DEMO-001` → `#migration-next-actions`.
- **Evidence:** `08-codebase-cascade-gates-1440x900.png`, `08-codebase-cascade-patches-1440x900.png`, `44-reconstruction-assumptions-no-actions-1440x900.png`, `47-migrator-next-actions-1440x900.png`.
- **Detail:** Codebase gates and patches have **zero** accept/reject/defer buttons. Assumption cards have no owner assignment or resolution control. The next-actions list says "Use the review workflow for the case (or the pilot decision log)" but there is no link and no review workflow for a codebase case. The caveat is honest that the demo page records no decision, but it does not give the human anywhere to go. The gate links to patches are useful; they open the patch details, but still cannot record a decision.

**H4. The in-app Packet claims two tables it does not render.**
- **Page:** `/packet?run=R-DEMO-001`.
- **Selectors:** `.packet-sections .packet-card:nth-child(3)` (section 03), `.packet-notes-grid section:nth-child(2)` (Findings summary).
- **Evidence:** `42-packet-section-03-missing-excluded-table-1440x900.png`, `43-packet-findings-summary-no-path-or-excerpt-1440x900.png`, `17-packet-top-1440x900.png`.
- **Detail:** Section 03 says "4 unsupported/corrupt files appear in the packet's excluded-files table with path, status, and reason." There is no excluded-files table in the app; the **exported** HTML does contain one. Section 05 says "grouped by rule with source path:line and redacted evidence excerpts"; the rendered Findings summary has only **Rule / Severity / Claim / State**, no path or excerpt. The downloadable HTML is more complete than the in-app packet. This is a review-artifact mismatch, not just a styling issue.

**H5. The post-rerun upgrade state still contradicts itself on generation and Retain.**
- **Page:** `/codebase?case=harbor-pc&upgrade=GWCP-APD-NAMING-2027.04` after **Apply and re-run the loop**.
- **Selectors:** `.head-meta`, `#cb-upgrade .impact-card`, `#cb-upgrade .resume-card`.
- **Evidence:** `14-codebase-harbor-after-rerun-1440x900.png`, `15-codebase-harbor-default-after-rerun-1440x900.png`, `31-codebase-harbor-upgrade-stale-390x844-full.png`.
- **Detail:** The header shows `bundle generation 1 · evaluated generation 2 · 2 iterations`; the card says "Revalidation passed at generation 2" and "No stale-green claim remains"; the checks still say `PASS APD patch cohort identified — 2 patch(es) require regeneration`; the Retain card says "The upgrade does not touch this bundle's affected rules." These cannot all be true in one state. The previous hard contradiction (`Green signal invalidated: yes`) is fixed, but the reader still cannot tell whether the bundle was regenerated, evaluated, or not touched.

### Medium

**M1. Count labels do not reconcile; "31 evidence records" is wrong.**
- **Page/selector:** `/?run=R-DEMO-001` `.summary-stat`; `/migrator?run=R-DEMO-001` stage 1 and summary strip; `/packet?run=R-DEMO-001` section 06.
- **Evidence:** `46-workbench-demo-path-1440x900.png`, `04-migrator-stage-1-scout-1440x900.png`, `18-packet-appendix-1440x900.png`.
- **Detail:** Workbench says **31 evidence records**; those are 31 **feature evidence links**. Migrator says 31 links and **101 evidence records across 300 files**. Packet says **126 items** (101 discovery + 25 review evidence). All three numbers are defensible, but the label "records" is wrong at the Workbench, and there is no legend on the Workbench page. "11 references" is never defined, and "37 vs 24" lacks units for the summary (the paragraph below explains 37 characters).

**M2. The three unknown sets do not match.**
- **Page/selectors:** `/?run=R-DEMO-001` `.gap-card`; `/migrator?run=R-DEMO-001` `#agent-stage-guardian .gate-card`; `/packet?run=R-DEMO-001` assumption table.
- **Evidence:** `45-workbench-gaps-1440x900.png`, `04-migrator-stage-3-guardian-1440x900.png`, `17-packet-top-1440x900.png` (assumption register).
- **Detail:** Workbench gap 3 is **duplicate PAVehicleDV screen**; Guardian `G-03` and packet `A-03` are the **37-character APD type**. Workbench gap cards do not display IDs, so a reader cannot cross-reference them; the Migrator uses `G-01…G-03` for assumptions while the packet uses `A-01…A-03`, and the ID `G-03` also exists for a different Workbench gap. "Every unknown has a name" is not yet true in one namespace.

**M3. "The value is not a score" is followed by scores.**
- **Page/selector:** `/codebase?case=harbor-pc` `.agent-explain` (`#codebase-explain-heading`), `#cb-gates .score-card`.
- **Evidence:** `14-codebase-harbor-after-rerun-1440x900.png`, `11-codebase-harbor-gates-1440x900.png`.
- **Detail:** The explain panel says "The value is not a score. It is a traceable list…" followed by "Target score 60/100", "Target score 100/100", and "0 / 100 / 74" (Cascade) or "0 / 100 / 71" (Harbor). The qualifier "not a Cloud Assurance score" appears later. Either call them readiness indicators throughout or remove the "not a score" sentence.

**M4. Workbench still says "Two completed dummy insurer migrations."**
- **Page/selector:** `/?run=R-DEMO-001` `.demo-path` third card.
- **Evidence:** `46-workbench-demo-path-1440x900.png`.
- **Detail:** The reality boundary directly above says "This is a synthetic rehearsal, not an actual migration"; the step says "Two completed dummy insurer migrations." The word "dummy" helps, but "completed migrations" is exactly the claim the boundary denies. Change to "two completed migration rehearsals" (matching the Case Studies H1).

**M5. The Scribe seal still reads like a failure, and the agent log has no download link.**
- **Page/selector:** `#agent-stage-scribe .seal-check` / `.seal-card`, stage-5 bundle table, `.seal-card` agent-log card.
- **Evidence:** `04-migrator-stage-5-scribe-1440x900.png`, `25-migrator-scribe-390x844.png`.
- **Detail:** **`SEAL HASH CHECK 7/8 match · log appended`** is repeated on mobile. The note explains the 8 files and that the manifest is separate, but it never says "this is expected because the agent log is append-only, not tampering." The stage also says "PRODUCED 8 bundle files" and lists `bundle-manifest.json` among the examples, while the same stage says the manifest is a separate wrapper not counted among the 8. The agent-log card shows a hash and "verified" but is **not a link**; the only audit download is the review audit JSON at the top, which is a different chain. So one of the eight sealed content files cannot be downloaded from the page. This is a trust-language and completeness problem, not a missing file on disk.

**M6. Audit counts: 12 events vs 9 events, with the same word "audit".**
- **Pages/selectors:** `/migrator` `#migration-next-actions` and `.migration-progress-meta`; `/packet` cover card and `.packet-appendix`.
- **Evidence:** `47-migrator-next-actions-1440x900.png`, `17-packet-top-1440x900.png`, `18-packet-appendix-1440x900.png`.
- **Detail:** Migrator says "Agent log: 12 events verified" and asks the human to "Verify 12 audit events". Packet says "Audit chain verified: yes (9 events)". The download footnote says the migrator log and review packet are separate chains, but the packet cover does not say "9 review-chain events"; the reader sees two audit numbers. Rename one "review audit chain" and the other "agent handoff log."

**M7. The plain-language glossary still omits load-bearing terms.**
- **Page/selector:** `/about#glossary`.
- **Evidence:** `20-about-1440x900.png`.
- **Detail:** It now defines Evidence link, Feature, Disposition, Assumption, Gate, SARIF, Gosu, APD, Gosu Query/application API, Cloud Data Access, App Events, claim legend, and claim strength. Missing: **PCF, Qusar, GWCP, Cloud Assurance, Cloud Retrofit, APD App, SBT, GUnit, MiMo, work package, target draft, target change, generation**. Several are used on the first screen and in the upgrade story.

**M8. Live/offline is still a capability-vs-run ambiguity, and the configured branch hides the setup variables.**
- **Pages/selectors:** `/settings` `.migration-facts`, `[data-llm-check-status]`; `/migrator` `.badge-offline`; `/codebase` `.badge-offline`; footer.
- **Evidence:** `19-settings-1440x900.png`, `37-settings-test-connection-1440x900.png`, `24-migrator-390x844.png`.
- **Detail:** Settings says "Live reasoning is enabled" and mode `live`; the run pages say "Reasoning: offline"; the footer says "offline by default." The new **Run live** controls make the per-run choice visible, but the Settings card does not say "this run used offline retrieval; live is available only when you press Run live." When configured, the branch omits `PREFLIGHT_LLM_MODE`, `PREFLIGHT_LLM_BASE_URL`, and `PREFLIGHT_LLM_API_KEY`, so a reviewer cannot reproduce the setup from the screen.

**M9. Only the first 8 of 31 feature evidence links are viewable in Migrator.**
- **Page/selector:** `#agent-stage-scout .stage-artifact`, header "first 8 of 31 links".
- **Evidence:** `04-migrator-stage-1-scout-1440x900.png`.
- **Detail:** There is no "view all 31" link and no feature filter in the packet. The full set exists in the packet appendix (126 items), but a no-context reviewer who starts at Scout must leave the stage and search the packet. The Workbench summary also does not list the 31 links.

**M10. Readiness flag F-001 is not F-001 on the Findings page.**
- **Pages/selectors:** `/findings?run=R-DEMO-001` first row; `/packet?run=R-DEMO-001` "Readiness flags (1)".
- **Evidence:** `51-findings-readiness-flag-f002-first-1440x900.png`, `17-packet-top-1440x900.png`.
- **Detail:** The packet labels the readiness flag `F-001`; the Findings page labels it `PF-GW-SBT-001` and starts the advisory rows at `F-002`, with no explanation that `F-001` is the separate readiness flag. This is a cross-page ID gap. It is outside the main requested page set but part of the evidence trail.

**M11. Primary navigation is not a navigation landmark; skip-link focus lands on BODY.**
- **Pages/selectors:** every page `aside.sidebar[aria-label="Primary navigation"]`; `main#main`; `.skip-link`.
- **Evidence:** `23-mobile-nav-open-390x844.png`, `50-skip-link-visible-1440x900.png`.
- **Detail:** There is no `<nav>` or `role="navigation"` around the primary sidebar. Pressing Tab reveals the skip link, but Enter sets `#main` in the URL and leaves `document.activeElement` as `BODY`; `main` has no `tabindex="-1"`. The mobile menu itself works (`aria-expanded`, Escape) and the codebase lab tabs support arrow/Home/End keys.

**M12. Guardian's gate list has an inner scroll with no "more" cue.**
- **Page/selector:** `#agent-stage-guardian .gate-list.compact`.
- **Evidence:** `38-migrator-guardian-gates-390x844.png`.
- **Detail:** The list is 360 px tall with 606 px of content at 1440 and 750 px at 390. G-03 is clipped inside the inner scroll; the region is focusable but there is no visible "more below" hint. The outer page scroll does not reveal the hidden card.

**M13. Codebase evidence links are raw JSON, and the packet appendix has no feature filter.**
- **Pages/selectors:** `.package-table a.evidence-link`; `.packet-evidence-table`.
- **Evidence:** `04-migrator-stage-2-architect-1440x900.png`, `18-packet-appendix-1440x900.png`.
- **Detail:** Package IDs now resolve, which is a real improvement, but the destination is `application/json`, not a readable evidence record. The 126-row appendix can only be scanned manually. This is a usability gap in the otherwise improved traceability story.

### Low / polish

- **L1. Packet appendix always shows a horizontal-scroll hint at 1440 even when the table fits.** `#packet-appendix [data-scroll-hint][data-scroll-always]` is visible while `scrollWidth === clientWidth === 1110`. Screenshot `18`. It is a false cue.
- **L2. Touch targets are small.** `[data-codebase-tab]` is 30 px high; `[data-upgrade-resume]`, `[data-upgrade-rerun]`, `[data-codebase-run]`, and case chips are 28 px high at 390. They are usable but below the 44 px recommendation; the 28 px controls are styled as primary actions.
- **L3. About repeats the full disclaimer in the page body and the global footer.** `#glossary` section and `.footer-line`. Screenshot `20`. This is duplicate reading, not a correctness problem.
- **L4. The Workbench has no run selector or empty state.** `/` auto-loads `R-DEMO-001` and shows "succeeded" before the reviewer has chosen a run. The boundary explains synthetic data, but "succeeded" is never defined as analysis success rather than migration success. Screenshot `01`.
- **L5. The upgrade invalidation is query-scoped and not labelled as a preview.** `/codebase?case=harbor-pc&upgrade=…` shows stale; `/codebase?case=harbor-pc` shows machine-green. The heading says "simulate", but the banner and `revalidation required` status do not say "preview only / not persisted." Screenshots `39` vs `10`.
- **L6. The 37 vs 24 summary lacks units.** `/?run=R-DEMO-001` `.summary-stat.summary-signal` reads "37 vs 24 / LONG TYPE VS APD LIMIT". The explanatory paragraph below says "37-character" and "24 characters", but the summary is the first metric a reviewer sees. Screenshot `46`.
- **L7. The codebase "Replay loop" is a highlight, not a replay.** `[data-codebase-replay]` only flashes the two iteration cards; it does not step through the Scout→Architect→Guardian→Critic→Planner cycle the way Migrator's replay does. Screenshot `07`.
- **L8. The top source-findings hint is accurate but the table still needs a horizontal hunt at 1440.** `#cb-findings [data-table-scroll]` is 1,412 px in 1,110 px. The cue is fixed; the reading burden remains.

---

## 5. Console, network, overflow, and interaction checks

**Console/network:** no console errors, page errors, warnings, or failed requests were observed during scripted interaction across:
Workbench spine selection and assistant questions; Migrator stage switching and replay; Codebase tab switching, finding evidence expansion, patch expansion, gate links, upgrade evaluation, Request revalidation, Apply/re-run; Packet appendix expansion; Settings Test connection; mobile nav; skip link.

**Links/downloads:** 249 unique internal hrefs across the requested pages returned **0** 4xx/5xx. Tested downloads returned 200 with expected types:
- `/packet/export?run=R-DEMO-001` → HTML (112 KB).
- `/api/runs/R-DEMO-001/audit` → JSON.
- `/api/codebase/cases/harbor-pc/bundle.zip`, `/report`, `/sarif`, `/patches/CP-001` → ZIP, Markdown, `application/sarif+json`, diff.
- `/api/runs/R-DEMO-001/migration/file?path=…` → target/report/manifest files.
- Every tested `EV-…` and `REV-…` evidence endpoint returned 200.

**Document overflow:** none at 1440, 1280, 1024, or 390, including after opening the packet appendix, codebase evidence rows, and the upgrade panel. All overflow is inside intentional table/spine regions.

**Measured scroll regions:**

| Region | 1440 | 1280 | 1024 | 390 | Cue |
|---|---:|---:|---:|---:|---|
| Workbench spine | 822/822 | 672/662 | 672/406 | 672/330 | visible when needed |
| Migrator Scout evidence | 1,339/1,110 | 1,339/950 | 1,339/694 | 1,339/332 | visible |
| Migrator Architect packages | 1,110/1,110 | 1,094/950 | 1,094/694 | 1,094/332 | visible when needed |
| Codebase Source findings | 1,412/1,110 | 1,412/950 | 1,412/694 | 1,412/332 | visible |
| Codebase evidence body | 1,400/1,110 | 1,400/950 | 1,400/694 | 1,400/332 | clipped, no separate cue |
| Packet evidence appendix | 1,110/1,110 | 1,040/950 | 1,040/694 | 900/332 | visible (false cue at 1440) |

**Replay:** Migrator's top **Replay loop** starts at Scout and advances through the five stages; after the scripted wait it was on Scribe with the toast "Five-agent replay complete. Human gates remain open." Codebase's **Replay loop** only highlights the two iteration cards.

**Mobile:** Sections menu opens/closes; links are 40+ px high; codebase tabs wrap onto two rows; no document-level overflow. The long pages remain long: Workbench 5,944 px at 390, Case Studies 7,414 px, Codebase 5,519 px for the active loop, Packet 8,950 px.

**A11y:** primary nav landmark and skip-link focus are the two repeat failures (M11). Codebase tabs support arrow/Home/End. Tab button heights are 30 px; upgrade action buttons 28 px. The source-findings evidence expansion is not usable without horizontal scrolling (H2).

---

## 6. What is genuinely working well

- The **What it is / What it is not / Three promises** block is strong no-context framing, and the reality boundary is repeated at the right moments.
- The **five-agent received/produced panels** remain the clearest part of the product. Guardian's "deliberately not received" list is excellent.
- **Machine-green vs human approval** is stated plainly on Codebase and Case Studies; the previous "invalidated: yes" contradiction is fixed.
- The **Workbench selected-node evidence** panel and the **assistant refusal** are excellent evidence-first patterns. The assistant's "Motorcycle_Ext" answer cites EV-0023 with a path, xpath, excerpt, and hash (screenshot `49`).
- **Packet appendix** now makes its 126/9 claim inspectable; all evidence links and audit rows render.
- **Codebase evidence rows** are a real improvement, even though their layout needs work.
- **Package evidence IDs** are now links; **gate cards** link to affected patches and the Planner report; clicking a gate link switches tabs and opens the patch detail.
- **Upgrade options** now include a Retain action, and Request revalidation no longer prints `resume_requested`.
- **No console errors**, no broken internal links, and no document-level horizontal overflow at the four tested widths.
- **Mobile navigation** works with `aria-expanded`, Escape closes it, and links are large enough.

---

## 7. Priority fixes

1. **Fix the Guardian data source.** Put Critic's 7 checks only under Critic; show Guardian's actual 3 checks (or explicitly label Guardian's check set). This is a one-data-mapping fix that resolves the most damaging count inconsistency.
2. **Make evidence rows reflow outside the table width.** Move the expanded evidence body into a block below the table or constrain it to the scroll container's visible width. At 390 it should be 332 px, not 1,400 px.
3. **Make the gates actionable or rename the promise.** Add assign/accept/reject/defer with reason to codebase patches/gates and feature assumptions; or change "What a human must do next" to "What an external owner must do next" and link to a real process. Do not point at a workflow that does not exist.
4. **Render the packet tables the copy claims.** Add the excluded-files table to section 03 and path:line/excerpt columns to section 05, or soften the section text to "summary; full tables are in the downloaded packet."
5. **Reconcile upgrade state.** Update the header to the evaluated generation or explain why the bundle stays at generation 1; remove "2 patches require regeneration" from a passing state or explain that the affected cohort is historical; make Retain's rationale match the affected-rule facts.
6. **Reconcile terminology and counts.** One legend for feature evidence link / estate evidence record / packet item; one for work package / target draft / change / file; one for review audit chain / agent handoff log. Label Workbench 31 as links, not records. Define "references" and add units to 37 vs 24.
7. **Unify gap/assumption names.** Show gap IDs on Workbench; map gaps → assumptions → gates; resolve the third unknown (duplicate screen vs 37-char type) or list both with different IDs.
8. **Fix the glossary and Settings status.** Add PCF, Qusar, GWCP, Cloud Assurance, Cloud Retrofit, APD App, SBT, GUnit, MiMo, work package, target draft, target change, generation. Show the three env variable names in the configured branch; say "this run is offline; live is available on demand."
9. **Fix the 7/8 seal language and expose the agent log.** Add "expected because the agent log is append-only and has grown since seal; not tampering." Link each of the 8 sealed files, including the agent log, from the stage-5 table.
10. **Finish the accessibility basics.** Use a `nav` landmark for primary navigation; make `main#main` programmatically focusable and move skip-link focus to it; enlarge the 28–30 px primary controls; make the gate list's hidden content discoverable.

---

## 8. Screenshot index

All under `docs/audits/screenshots/no-context-round4/`.

| Screenshot | What it shows |
|---|---|
| `01-workbench-1440x900.png` | Workbench first viewport; "succeeded" and the reality boundary. |
| `02-workbench-evidence-selected-1440x900.png` | Workbench after selecting EV-0001; selected-node evidence panel. |
| `03-workbench-assistant-refusal-1440x900.png` | Assistant refuses the territory question and names the missing source. |
| `04-migrator-stage-1-scout-1440x900.png` … `04-migrator-stage-5-scribe-1440x900.png` | All five feature-loop stages, including the Guardian 7/7 card and Scribe 7/8 seal. |
| `05-migrator-replay-step2-1440x900.png`, `06-migrator-replay-complete-1440x900.png` | Migrator replay in progress and completed at Scribe. |
| `07-codebase-cascade-loop-1440x900.png` | Cascade tabs near the top; 20/20; 10 gates; 22 patches. |
| `08-codebase-cascade-findings-1440x900.png` | Source-findings table and visible scroll cue. |
| `08-codebase-cascade-patches-1440x900.png` | 22 pending patch cards with no decision controls. |
| `08-codebase-cascade-gates-1440x900.png` | 10 human gates, Planner report, readiness scores. |
| `08-codebase-cascade-upgrade-1440x900.png` | Upgrade form before a scenario is applied. |
| `09-codebase-cascade-finding-evidence-1440x900.png` | Expanded evidence row; 1,400 px body clipped at 1440. |
| `10-codebase-harbor-loop-1440x900.png` | Harbor default outcome; 20/20; 11 gates; 21 patches. |
| `11-codebase-harbor-findings-1440x900.png`, `11-codebase-harbor-patches-1440x900.png`, `11-codebase-harbor-gates-1440x900.png`, `11-codebase-harbor-upgrade-1440x900.png` | Harbor tabs. |
| `12-codebase-harbor-upgrade-stale-1440x900.png`, `39-codebase-harbor-upgrade-stale-true-1440x900.png` | Stale-green state before revalidation. |
| `13-codebase-harbor-revalidation-recorded-1440x900.png` | Request revalidation status; no internal token. |
| `14-codebase-harbor-after-rerun-1440x900.png` | Compatible state after Apply/re-run; 2 patches still require regeneration; Retain rationale. |
| `15-codebase-harbor-default-after-rerun-1440x900.png` | Header still `bundle generation 1 · evaluated generation 2`. |
| `16-case-studies-1440x900.png` | "Two completed migration rehearsals"; both dummy insurers and outcomes. |
| `17-packet-top-1440x900.png` | Packet cover, 9 audit events, 126-item claim. |
| `18-packet-appendix-1440x900.png` | Expanded 126-item evidence table and 9 audit rows. |
| `19-settings-1440x900.png` | Live endpoint, models, key policy. |
| `20-about-1440x900.png` | What it is/not, glossary, claim legend, full disclaimer. |
| `21-workbench-1024x768.png`, `21-workbench-1280x720.png`, `21-workbench-390x844.png`, `22-workbench-390x844-full.png` | Workbench at the remaining widths and full mobile stack. |
| `23-mobile-nav-open-390x844.png` | Sections menu open. |
| `24-migrator-1024x768.png`, `24-migrator-1280x720.png`, `24-migrator-390x844.png` | Migrator at the remaining widths. |
| `25-migrator-scribe-390x844.png` | Scribe seal on mobile. |
| `26-codebase-cascade-loop-1024x768.png`, `26-codebase-cascade-loop-1280x720.png`, `26-codebase-cascade-loop-390x844.png`, `27-codebase-cascade-loop-390x844-full.png` | Cascade layout at the remaining widths. |
| `28-codebase-cascade-findings-1024x768.png`, `28-codebase-cascade-patches-1024x768.png`, `28-codebase-cascade-gates-1024x768.png`, `28-codebase-cascade-upgrade-1024x768.png` and the `1280x720`/`390x844` equivalents | Tab states at widths. |
| `29-codebase-cascade-finding-evidence-1024x768.png`, `29…1280x720.png`, `29…390x844.png` | Clipped evidence at each width. |
| `30-codebase-harbor-upgrade-stale-1024x768.png`, `30…1280x720.png`, `30…390x844.png` | Post-rerun compatible state at the remaining widths (the true stale state is in `39`). |
| `31-codebase-harbor-upgrade-stale-390x844-full.png` | Full mobile compatible state; Retain rationale contradiction. |
| `32-case-studies-1024x768.png`, `32…1280x720.png`, `32…390x844.png` | Case Studies at the remaining widths. |
| `33-packet-1024x768.png`, `33…1280x720.png`, `33…390x844.png` | Packet at the remaining widths. |
| `34-packet-appendix-390x844.png` | 126-item appendix on mobile; hint visible. |
| `35-settings-1024x768.png`, `35…1280x720.png`, `35…390x844.png` | Settings at the remaining widths. |
| `36-about-1024x768.png`, `36…1280x720.png`, `36…390x844.png` | About at the remaining widths. |
| `37-settings-test-connection-1440x900.png` | `OK · mimo-v2.6-flash · 3492 ms`; no key. |
| `38-migrator-guardian-gates-1440x900.png`, `38…390x844.png` | Guardian 7/7 vs 3 work items; clipped gate list. |
| `39-codebase-harbor-upgrade-stale-true-1440x900.png` etc. | True stale state at each width after reset. |
| `40-codebase-harbor-upgrade-stale-true-390x844-full.png` | Full mobile stale page. |
| `41-workbench-node-selected-390x844.png` | Mobile selected-node evidence. |
| `42-packet-section-03-missing-excluded-table-1440x900.png` | Section 03 claims a table that is absent. |
| `43-packet-findings-summary-no-path-or-excerpt-1440x900.png` | Section 05 summary has only Rule/Severity/Claim/State. |
| `44-reconstruction-assumptions-no-actions-1440x900.png` | Assumption register with no owner or decision controls. |
| `45-workbench-gaps-1440x900.png` | Three gap cards; no IDs; third is duplicate screen. |
| `46-workbench-demo-path-1440x900.png` | "Two completed dummy insurer migrations"; 31/11/37-vs-24 summary. |
| `47-migrator-next-actions-1440x900.png` | Five human to-dos; "review workflow" with no link. |
| `49-workbench-assistant-citations-1440x900.png` | Assistant cites EV-0023 with a source card. |
| `50-skip-link-visible-1440x900.png` | Skip link visible on focus; activating it leaves focus on BODY. |
| `51-findings-readiness-flag-f002-first-1440x900.png` | Findings page first row F-002; readiness flag is separate from the F-002…F-025 list. |
