# No-context audit — Round 2

**Auditor stance:** first-time reviewer with no prior knowledge of Guidewire, Gosu, APD, Cloud Data Access, App Events, or PreFlight.
**App:** `http://127.0.0.1:8010` (local instance, synthetic fixtures)
**Date:** 2026-11-11
**Viewports:** 1440 × 900, 1280 × 720, 390 × 844 (Chromium, Playwright)
**Evidence:** screenshots in `docs/audits/screenshots/no-context-round2/`
**Constraint:** I did not read repository source, tests, or existing product documentation. All answers below are derived from rendered pages, controls, and the product's own visible Artifact/Audit/Download links; the one exception is the unlinked bundle manifest, which I inspected through the product's artifact endpoint and explicitly mark as not screen-visible. I did not edit product code, tests, or existing docs. I did not launch live reasoning or delete/apply anything. I clicked **Record revalidate** once while testing the upgrade flow; that recorded a UI decision (`resume_requested`) and is disclosed here.

**Coverage:** Workbench/Home; Agent loop, all five stage panels, Play/Pause and Replay; Codebase lab for Cascade and Harbor, all five tabs, iteration comparison, finding/patch details, upgrade evaluation and decision controls; Migration stories; Settings; About/glossary; Manifest; Reconstruction; Findings and its decision dialog; Evaluation; Review packet; Runs. Each was captured at 1440 × 900 and 1280 × 720; the main pages were also captured at 390 × 844.

---

## 1. Verdict

This is a thoughtful, unusually self-aware prototype. The home page can explain the product in one sentence, the five-agent page exposes received/produced handoffs, the migration stories have concrete outcomes, and the machine-green vs human-gate safety message is repeated often enough that a newcomer cannot miss it.

It is **not** yet no-context. A first-time viewer has to learn a private vocabulary (many status phrases, two meanings of "gate", "work package", "bundle artefact"), reconcile several incompatible evidence counts, and discover that some important controls do nothing or do something irreversible without confirmation. Several evidence surfaces are visually clipped at desktop size, and the central feature graph is only one-third visible on a phone.

**Overall no-context explainability: 6/10.**

The strongest parts are product purpose (8/10), five-agent clarity (8/10), and migration-story explainability (7/10). The weakest are gate/human-approval clarity (5/10), terminology/glossary (4/10), visual hierarchy (5/10), and mobile/responsive (5/10).

---

## 2. The ten questions, answered from the screen

### Q1. What is PreFlight, in one sentence?

> **PreFlight is a local, read-only review tool for a Guidewire-style insurance codebase before a cloud migration.** It reads a snapshot, groups the code into features, and shows what each claim is based on, what is still unknown, and what a safe change would touch.

Source: Workbench `START HERE / What PreFlight is, in plain language`. The page also says, "It runs on this machine. It never edits the source and never deploys." This is the clearest sentence in the product.

![Workbench start here](screenshots/no-context-round2/home-1440.png)

Caveat: the same header also says **Local-only** while Settings shows live reasoning enabled against `token-plan-sgp.xiaomimimo.com`. I read the purpose as "offline by default / local review", not "no outbound network ever". See H2 in the defect log.

### Q2. What are the five agents, and what does each receive and produce?

The five-agent page (`/migrator?run=R-DEMO-001`) has an explicit **RECEIVED / WORK / PRODUCED** panel for every stage. For the feature loop (PA-VEH-01):

| Agent | Receives | Produces |
|---|---|---|
| **Scout** | Completed review run and source manifest; feature index and evidence graph; findings and explicit dispositions | Feature scope PA-VEH-01; 31 evidence links on the feature; 101 evidence records across 300 files; 24 findings and 12 dispositions |
| **Architect** | Scout's PA-VEH-01 scope; 12 explicit dispositions; evidence IDs for every package | 5 work packages; 5/5 target files; every package remains pending human approval |
| **Guardian** | Architect's 5 packages; open assumptions and review findings; Guidewire rule pack and APD constraints. Deliberately not Scout's narrative, Critic's verdict, or model text | 11 open gates: 3 assumption gates + 8 rule groups; 6 high-impact gates; deployment remains blocked |
| **Critic** | Scout's evidence summary; Architect's packages and target files; Guardian's gate register | 7/7 independent checks passed; verdict PASS; 0 auto-approved changes |
| **Scribe** | Critic's verification result; Guardian's open gates; package and target hashes | 8 bundle files; plan, report, bundle manifest, hash-chained agent log; every change pending human approval |

The **codebase loop** uses the same first four names and replaces Scribe with **Planner** (see Q5). Its Scout produces 17 files / 156 LOC / 18 blockers / 5 custom feature slices for Cascade (15 / 160 / 20 / 6 for Harbor). Its Planner produces `MIGRATION-REPORT.md`, `results.sarif` (SARIF 2.1.0), and a readiness number.

Source screenshots: `migrator-step1-1440.png` through `migrator-step5-1440.png`; `codebase-tab0-fiveagent-1440.png`.

### Q3. Why are there 5 packages, 11 gates, 7 checks, and 8 bundle files in the feature loop?

This is only **partly** screen-answerable.

| Count | Screen explanation | Can a newcomer derive it? |
|---|---|---|
| **5 packages** | Architect lists WP-01 through WP-05: schema, mapping, updater, codegen config, and LOB API config. | The five rows are visible, but the page never states the selection rule ("one per target artefact family"). It just asserts five. |
| **11 gates** | Guardian says explicitly: **3 assumption gates + 8 rule groups = 11 human decisions**; 6 are high impact. | Yes. The 3 assumption cards and the 8 rule rows are visible. |
| **7 checks** | Critic lists exactly seven checks: packages exist, all package files generated, no `_gen` targets, no duplicate targets, generated JSON/YAML parses, every package evidence-linked, human approval retained. | Yes, the seven checks are visible and named. |
| **8 bundle files** | The header says "8 bundle files"; Scribe names plan, report, bundle manifest, and agent log, but only four artifact groups are named. | **No.** The page never shows an eight-item file list. The bundle manifest itself is not linked from the page. I confirmed its composition only through the artifact API: 5 target files + `migration-plan.json` + `MIGRATION-REPORT.md` + `audit.jsonl`. A normal viewer cannot see that breakdown. |

There is an additional handoff that makes the counts harder: the "what just happened" strip says **"Architect → Guardian: 5 work packages and 8 bundle artefacts"**, before Scribe later produces "8 bundle files". The screen never explains whether those eight artefacts are the same eight files. See M1.

### Q4. Why is iteration 1 red and iteration 2 green in the codebase lab?

The screen explains it clearly in the **Iterative patching** section:

- **Iteration 1 — error-first pass, rework:** Architect produced 16 patches. Guardian passed only **11/13 deterministic checks**: it failed "every source finding has a patch" (10/18 covered) and "target has no residual warnings" (7 warnings). Critic passed only **4/7** and issued two targeted fix requests (FR-01, FR-02). The loop continued.
- **Iteration 2 — full pass, green:** Architect produced 22 patches. Guardian passed **13/13** (18/18 findings covered; 0 residual warnings). Critic passed **7/7**. Both gates agreed, so Planner could compile.

In other words, iteration 1 is not "red because the agent was bad"; it is the deliberate first pass that stops at errors and leaves warning-level findings and coverage gaps, which Guardian is designed to catch. Iteration 2 is the full pass that closes them. The UI labels iteration 1 **"rework"**, not literally "red"; the orange/red card is the only red-like state. Source: `codebase-iterations-1440.png`.

Caveat: the badge at the very top says **"generation 1"**, while the body says **2 loop iterations** and the outcome says "2 iterations". A newcomer can easily read "generation 1" as "only one iteration happened", especially because the page never defines "generation". See M11.

### Q5. What is the difference between Scribe and Planner?

- **Scribe** is the fifth agent in the **feature loop**. It seals the plan, human-readable report, bundle manifest, and hash-chained agent log. Its screen says "Sealed means tamper-evident, not approved" and "Sealing is not approval: every change still waits for a human."
- **Planner** is the fifth agent in the **codebase loop**. It compiles the executive report, readiness score, SARIF summary, and next actions. It only runs after Guardian and Critic agree; the report is still a human-review artifact.

The product states the relationship directly: **"Planner is the codebase lab's seal/report agent — the same role Scribe plays in the feature loop."** Home adds: "Both loops use the same first four roles. Only the sealer changes name."

So the difference is the loop and the output format, not authority: neither one approves anything. The practical difference is that Scribe produces a local migration bundle, while Planner produces a code-migration report with SARIF and readiness numbers. A first-time viewer can answer this from Home + Codebase lab; a viewer landing only on the codebase lab will see Planner and the one-line mapping, which is adequate.

### Q6. What does "machine-green" mean, and what remains for a human?

**Machine-green** means the deterministic machine checks agree: Guardian is green, Critic is green, and (in the codebase loop) Planner has compiled. It does **not** mean approved, and it is **not** an official Cloud Assurance result. The stories state: "machine-green · human gates open ... It is not human approval and not an official Cloud Assurance result."

What remains for a human is named in the **Human review gates** tab:

| Gate | Human task |
|---|---|
| CR-01 | APD nameOverride and endpoint regeneration; regenerate endpoints and compile the target product model |
| CR-02 | Public API replacement; compile and regression-test the replaced API path |
| CR-03 | Semantic equivalence of the data-access rewrite; run rating/data regression and compare with legacy output |
| CR-04 | Log redaction verification; confirm redaction and retain the audit trail |
| CR-05 | App Events contract and delivery behaviour; contract, ordering key, delivery guarantee, consumer acknowledgement |
| CR-06 | Tenant isolation after removing shared state |
| CR-07 | Credential rotation and secret binding |
| CR-08 | Cloud API route contract, auth scopes, and consumer cut-over |
| CR-09 | Test coverage after removing database coupling |
| CR-10 | Transaction and failure-path behaviour |

These ten tasks remain open for Cascade. Harbor has eleven. The feature loop's Guardian has eleven gates of its own: three open assumptions (territory source, supported rating export, 37-character APD type name) plus eight rule groups. Every patch/draft stays pending.

Important gap: the gate cards in the codebase UI have owners written as role names ("APD / product model owner", "Application development") and **no action controls**. The feature-loop gates say "Owner: unassigned" for all three. The "human gates" are therefore described, not resolvable, on the pages where they are counted. See H1.

### Q7. What are Cascade and Harbor, and what are their outcomes?

Both are explicitly **dummy insurers** built to exercise the product; the story page says "Invented, not customer data."

| | **Cascade Mutual** | **Harbor P&C** |
|---|---|---|
| Profile | Monoline Personal Auto mutual; "Cloud Retrofit without APD App · single LOB" | Multi-line regional P&C group; "Cloud Retrofit with APD conversion · multi-LOB"; three applications |
| Scale shown | 420,000 policies; TX / OR / WA; 64 custom Gosu; 7 integrations | 2.6M policies; TX / LA / FL / WA; 1,180 custom Gosu; 42 integrations |
| Findings | 18 blockers | 20 blockers |
| Patches | 22 | 21 |
| Iterations | 2 | 2 |
| Human gates | 10 | 11 |
| Outcome | **machine-green · human gates open** | **machine-green · human gates open** |

Cascade is the "narrow, high-value" case: one LOB, a small number of integration surfaces, and a rating path where direct SQL is both a cloud blocker and a latency risk. Harbor is the "hard case": three LOBs, cross-application claims/billing customizations, APD conversion, and a filed-model dependency. Both stories state that the green signal is necessary but not sufficient; Harbor explicitly says "code-level green is necessary but not sufficient."

### Q8. Where can you verify a claim's evidence?

There are four good, screen-visible routes, and one important gap:

1. **Feature workbench graph:** Click a highlighted node (for example `PAVehicleDV`) in **Feature spine**. The **Selected node evidence** panel shows an evidence ID, file, line/xpath, excerpt, and excerpt SHA-256. The assistant's "Open evidence" link scrolls to the same panel. Source: `home-evidence-node-1440.png`, `home-open-evidence-1440.png`.
2. **Agent loop:** The Scout evidence table links `EV-0001` … to the evidence API JSON. The JSON contains evidence ID, path, locator, excerpt, excerpt SHA, method, confidence. The **Audit JSON** header link exposes the hash-chained review log.
3. **Findings page:** Click **Inspect** on a finding to open the side **Finding F-002** panel. It shows remediation, standard/claim strength, and an **EVIDENCE** card with file, line, and code excerpt. The **public reference** links go to documentation. Source: `findings-evidence-1440.png`.
4. **Review packet:** Section 06 is an "Evidence and audit appendix"; it claims 126 evidence items and includes the hash-chained audit trail in the downloadable packet.

The gap: In the **Codebase lab → Source findings** tab, the table gives only a source path and line plus a rule name. Rows are not clickable, there is no excerpt, no fingerprint, and no EV link, even though the section header promises "18 findings · line evidence · stable fingerprints." The Patches tab shows a source path and a diff for each patch, so a determined user can reconstruct a claim from a patch, but cannot inspect a finding directly. This is the weakest of the two loops for evidence traceability.

Another gap: counts do not reconcile. Home says **31 evidence records**; Scout says **31 evidence links** and **101 evidence records across 300 files**; the Review packet says **126 items**; the audit chain has 9 events in the packet, 12 in the migrator, and 15 in the codebase lab. Each may be correct for its own scope, but the screen never provides a reconciliation.

### Q9. How would you enable live reasoning without exposing a key?

From **Settings → Optional live reasoning**:

- The UI displays **enabled**, mode **live**, endpoint `token-plan-sgp.xiaomimimo.com`, models `mimo-v2.6-flash` and `mimo-v2.6-pro`, default `mimo-v2.6-flash`, and "Real code: synthetic only."
- It says the base URL and key are read **only from the environment**; **no key value is displayed or requested in the UI**; no key is written to the repository, logs, screenshots, or API responses.
- To change it, edit `.env` and **restart the app**; "Test connection" is provided.
- How it is used: Scout, Architect, and Critic may receive a grounded narrative prompt; Guardian never calls the model; every returned statement must cite an allowed evidence/rule/package ID, and ungrounded statements are dropped and counted.

So the safe answer is: configure the endpoint/key as environment variables, restart, and never paste a key into the UI. The screen deliberately has no key field.

Two usability gaps: (a) the exact environment variable names are **not shown**, so a user who does not already know them cannot actually configure it from this screen; (b) the header simultaneously says **Local-only** and "No telemetry", while this page says live reasoning is enabled and points at an external host. The page needs a clearer "offline by default; live is opt-in and sends synthetic fixture content" statement. See H2.

### Q10. What happens when a release upgrade lands mid-migration?

I opened **Codebase lab → Upgrade resilience**, left the default scenario, and pressed **Evaluate upgrade**.

The scenario was "APD import limit tightens from 24 to 20 characters (GWCP 2026.10 → GWCP 2027.04)". The screen then showed:

- `GWCP-APD-NAMING-2027.04`, **revalidation_required**
- "Generation 1 → 2. 2 patch(es) affected · PF-CODE-APD-001. **Green signal invalidated: yes**."
- **REWORK**: "codegen overrides fit the 20-character limit — 1 override(s) exceed 20 characters."
- **PASS**: "APD patch cohort identified — 2 patch(es) require regeneration."
- Three resume options: **Re-run Architect with the new rule pack** (recommended), **Roll back to the last green checkpoint**, **Defer the upgrade and pin the assessment release**.
- Actions: **Record revalidate**, **Record rollback**, **Record defer**, **Apply and re-run the loop**.

After I clicked **Record revalidate**, the page said "Recorded revalidate: resume_requested. The green signal remains cleared and every patch still needs human approval." The top status showed `revalidation_required` and the banner said "Not green yet." That is the right conceptual behavior: a release change invalidates the previous green state, pinpoints affected patches, and demands a new human decision.

But the page is internally inconsistent after the upgrade: the "No context needed" card still says **"Cascade Mutual: a completed code-migration rehearsal"**, "What just happened" still says the final Guardian/Critic were green and Planner compiled, and the historical iteration cards still show green. Only the banner and outcome strip reflect the invalidation. A viewer cannot tell which narrative is current. See H3.

---

## 3. Scorecard

Scale: **0 = unusable without a guided tour; 10 = a first-time viewer needs no explanation.** These are intentionally harsh.

| # | Category | Score | Why |
|---|---|---:|---|
| 1 | Product purpose | **8** | "What it is / what it is not / three promises" is excellent. Docked for unresolved Local-only vs live reasoning and for jargon in the first sentence ("Guidewire-style"). |
| 2 | Five-agent clarity | **8** | Each agent has explicit received/produced panels; stage cards are clickable and all five were inspectable. Docked for Scribe/Planner split and "same first four roles" hiding different duties. |
| 3 | Handoff clarity | **7** | Handoff strip names the artifact at each transition. Docked for "5 packages and 8 bundle artefacts" appearing before Scribe's 8 files, and for the unexplained 8-file bundle. |
| 4 | Gate / human-approval clarity | **5** | The safety message is strong, but "gate" is used for both deterministic machine checks and human-owned decisions; human gates have no action controls; feature owners are all "unassigned"; counts differ by loop. |
| 5 | Migration-story explainability | **7** | Both insurers have scale, constraints, custom features, outcomes, and a "why this matters" paragraph. Docked for undefined "Cloud Retrofit", "APD App", and "SBT", and for the long repeated onboarding cards before the cards. |
| 6 | Evidence traceability | **6** | The feature graph evidence panel is excellent (file, locator, excerpt, SHA). The evidence table is clipped at 1440 and mobile, the codebase finding rows have no excerpt, and the 8-file bundle is not exposed. |
| 7 | Codebase-loop explainability | **7** | Iteration 1 vs 2, Guardian checks, Critic checks, and human gates are all explicit. Docked for "generation 1" vs 2 iterations, "not a score" vs target scores, and the 11k-pixel mobile page. |
| 8 | Visual hierarchy | **5** | Consistent visual system, but too many stacked explainer cards before the work; duplicated green/status messages; key evidence clipped; the 1280 toolbar wraps "Run live" onto its own line. |
| 9 | Terminology / glossary | **4** | The glossary defines evidence link, feature, disposition, assumption, gate, SARIF, Gosu, APD, Cloud Data Access, and App Events. It does **not** define PCF, GUnit, SBT, Qusar, Cloud Assurance, Cloud Retrofit, APD App, MiMo, or the status lexicon. |
| 10 | Navigation | **6** | Sidebar grouping is clear on desktop. Three names for one page (Agent loop / Migrator / "Watch the migration crew work"), non-clickable breadcrumbs, missing mobile group headings, and an unclear split between "Agent loop" and "Codebase lab". |
| 11 | Mobile / responsive | **5** | No page-wide horizontal overflow in most places, and the mobile menu works. But the feature graph shows only 3 of 6 columns with no affordance; the evidence table hides 1,007 px of content; key tabs sit 2,322 px down an 11,118 px page; touch targets are small. |
| 12 | Accessibility | **5** | Good basics (native dialog focus, Escape, live region, contrast, focusable table scroll regions). Failures: skip link does not move focus, tabs ignore arrow keys, label-content-name mismatches, H4 under H2, tooltip-only paths. |
| — | **No-context explainability (separate)** | **6** | A newcomer can answer Q1, Q2, Q4–Q7, Q9, and Q10 with effort. Q3 and the 8-file bundle, the gate semantics, the status lexicon, and the evidence reconciliation require prior knowledge or reading many pages. |

---

## 4. Where I got lost, page by page

| Page | Exact place | What happened |
|---|---|---|
| `/` Workbench | `.stat-grid`, label "EVIDENCE RECORDS" | It says **31 EVIDENCE RECORDS** beside the feature. The agent loop calls the same 31 **evidence links** and separately reports **101 evidence records** across the estate. I could not tell whether "record" and "link" meant the same thing. |
| `/` Workbench | `.spine-scroll`, Feature spine | At 390 px only PCF/ENTITY/TYPELIST are visible. The copy says there are six columns, but there is no visible scroll hint and the scroll container is not focusable. I initially assumed the other three columns were missing. |
| `/` Workbench | `Unknowns and gaps` | All three cards say **Owner: unassigned**. The start-here promise says missing sources become "gaps and assumptions with an owner and impact"; this screen contradicts the "with an owner" part. |
| `/` Workbench | Assistant "Open evidence" | The link goes to `#evidence-drawer` and scrolls to the existing evidence panel, but it is not a modal/drawer; I initially expected an overlay and did not notice the page had moved. |
| `/migrator?run=R-DEMO-001` | Sidebar vs breadcrumb vs H1 | The nav says **Agent loop**, the breadcrumb says **Migrator**, and the H1 says **Watch the migration crew work**. I initially thought these might be three different pages. |
| `/migrator?run=R-DEMO-001` | `data-agent-replay` "Replay loop" | At Step 3 of 5, clicking **Replay loop** produced no visible change after 3 seconds, no toast, no URL change, and no network request. I could not tell whether replay had failed or had already finished. |
| `/migrator?run=R-DEMO-001` | `.scout-evidence-table` | At 1440 the last column (EXCERPT) is visibly cut at the right edge; at 390 only EVIDENCE and FILE are visible. There is no "scroll horizontally" note (unlike Settings/About/Manifest). |
| `/migrator?run=R-DEMO-001` | Guardian gates | The 3 assumption gates all show **Owner: unassigned**, and none of the 11 gate cards has an action. The page says "human decisions" but I cannot make one here. |
| `/migrator?run=R-DEMO-001` | Scribe / Sealed bundle | It says **8 bundle files**, but names only plan, report, bundle manifest, and agent log; only three links are offered (Plan JSON, Migration report, Review audit JSON). The bundle manifest itself is not exposed. |
| `/codebase?case=cascade-mutual` | `.status-badge` / `.no-context card` | "green · human gates open" and "generation 1" are simultaneously visible with "2 iterations" and "Iteration 1 rework / Iteration 2 green". "Generation" is never defined. |
| `/codebase?case=cascade-mutual` | No-context card vs iteration/readiness cards | The card says **"The value is not a score."** The iteration cards say **"Target score 65/100"** and **"Target score 100/100"**, and Planner shows **100 structural / 74 after human gates**. The qualifier "not a Cloud Assurance score" appears below one of them, but the contradiction is immediate. |
| `/codebase?case=cascade-mutual` | `#cb-findings` Source findings | The table header promises "stable fingerprints" but the table has no fingerprint column, rows cannot be expanded, and there is no evidence excerpt or Inspect control. |
| `/codebase?case=cascade-mutual` | `#cb-gates` Human review gates | The gates have owner roles but no Accept/Reject/Defer/Record action. Clicking a gate card does nothing. The only decision controls I found for findings were on the separate **Findings** page. |
| `/codebase?case=cascade-mutual` | `#cb-upgrade` | After **Evaluate upgrade**, the banner and outcome correctly become `revalidation_required` / "Not green yet", but the title still says "a completed code-migration rehearsal" and "What just happened" still says Planner compiled a green report. |
| `/codebase?case=cascade-mutual` | `#cb-upgrade` Record revalidate | The button records immediately (`resume_requested`) without the confirmation/reason dialog used by other decisions. I did not intend to make a state change; there is no undo in the screen. |
| `/codebase?case=harbor-pc` | 1280 / 390 layout | The document is 10 px wider than the 1280 viewport and 2 px wider than 390; a long `<code>` path in the inventory is not contained. |
| `/case-studies` | Card CTA | "Explore the five-agent run" goes to `/codebase` (the codebase loop with Planner), not `/migrator` (the feature loop with Scribe). The page is describing the codebase loop in its CTA, but the nav calls the other page "Agent loop". |
| `/case-studies` | Card tags | "Cloud Retrofit without APD App · single LOB" and "Cloud Retrofit with APD conversion · multi-LOB" use terms that are not in the glossary. |
| `/settings` | Optional live reasoning | "enabled" and "live" are consistent internally, but the exact env var names are absent, and the top-of-page **Local-only** badge is not reconciled with the external endpoint. |
| `/about` | Plain-language glossary | The glossary is useful but stops at 8 terms. PCF, GUnit, SBT, Qusar, Cloud Assurance, Cloud Retrofit, and APD App are all used elsewhere and missing. "Gate" is defined here as human-owned, which conflicts with the codebase lab's machine gates. |
| `/findings?run=R-DEMO-001` | `.findings-table` | At 1440 the STATE column and part of ACTIONS are clipped by the fixed detail panel; at 390 only the leftmost columns are visible. The "scroll horizontally" hint is present, but this is a key table. |
| `/findings?run=R-DEMO-001` | SOURCE column | Source paths are truncated (`gsrc/acme/err...`) with the full path only in a title tooltip. On a phone, a tooltip cannot be opened; the selected finding detail gives the full path, but scanning is impossible. |
| `/findings?run=R-DEMO-001` | SBT readiness flag | "SBT", "Olos SBT", and `standardsBasedTemplate` appear without definition. I could not tell whether this is a finding, a certification, or a conversion check. |
| `/reconstruction?run=R-DEMO-001` | `.mapping-table` | `mapped_transformed`, `guidewire-doc`, `source`, and `pending` are raw tokens; target names wrap mid-word ("PersonalAutoRatingFac torConfiguration"). The page never tells me whether accepting a mapping is safe or what "mapped_transformed" means. |
| `/reconstruction?run=R-DEMO-001` | Draft & diff / Assumptions / Comparison tabs | "macro-F1 1.00", "reference target", TP/FP/FN, and the decision semantics for "Accept change" are not defined. The tabs are usable but require metric knowledge. |
| `/packet?run=R-DEMO-001` | Assumption register | "unassigned" wraps as **"unassig ned"** in the 1440 table; the packet also introduces "126 items", which I cannot reconcile with the 101 evidence records on the migrator. |
| `/manifest?run=R-DEMO-001` | SHA-256 column | Hashes wrap at arbitrary characters into 2–3 lines; the table is hard to scan, and there is no copy button per hash. |
| `/evaluation?run=R-DEMO-001` | Headline metrics | "6/6 estimate-moving issues", "4/4 holdout recall", "6/8 top-8 allowance", and six 100% cards are presented before the limitations. The page says "not a benchmark", but the visual emphasis is entirely on 100%. |
| `/runs` | Run list | Only feature runs are listed; Cascade and Harbor codebase rehearsals are not. A newcomer who explored the codebase lab will not find those runs in Runs. |
| Nav (all pages) | Breadcrumbs | "Workspace / Findings / R-DEMO-001" is plain text (all `<span>`), not links. It looks clickable; it is not. |
| Nav (mobile) | Open "Sections" menu | The group labels **AGENT DEMO / REVIEW / WORKSPACE** disappear; the 12 links become a two-column grid, so "Migration stories" sits next to "Workbench" as if they were peers. |

---

## 5. Defect log

### High

#### H1. "Gate" means two different things, and human gates are not actionable
**Seen at:** `/about#glossary`, `/codebase` Five-agent loop + Gates tab, `/migrator` Guardian stage.
**Observed:**
- About: "**Gate:** A checkpoint that stays with a named human owner. A green machine check does not close a human gate."
- Codebase: "The loop repeats until **both gates agree**" and "Guardian deterministic **gate**" (both machine checks), then "Human review gates" (human decisions).
- Guardian gates in the feature loop have **Owner: unassigned**; the codebase gates have role owners but no action controls. Clicking `CR-01` produces no dialog or state change.
- The only actionable *finding* decisions I found were on `/findings` (Accept / Reject / Defer), and those are for the other loop's 24 findings, not the codebase lab's 18 findings. `/reconstruction` has mapping decisions, but no gate decisions.

**Reproduction:**
1. Open `/about#glossary`; read the Gate definition.
2. Open `/codebase`; read "both gates agree" and "Guardian deterministic gate".
3. Open the **Gates, report & SARIF** tab; click `CR-01`, `CR-02`, or any gate row.
4. Open `/migrator?run=R-DEMO-001`; click stage 3 (Guardian); read "Owner: unassigned" on G-01..G-03.
**Expected:** Two distinct labels ("machine check" vs "human gate"), and an explicit way to assign/resolve a gate (or a clear note that assignment happens outside this demo).
**Evidence:** `about-1440.png`, `codebase-tab3-gates-1440.png`, `migrator-step3-full-1440.png`.

#### H2. "Local-only" and "Offline deterministic" conflict with live reasoning
**Seen at:** global header, `/settings` Optional live reasoning, `/migrator` and `/codebase` action bars.
**Observed:**
- Header on every page: **"Local-only"** and sidebar "No tenant, no telemetry."
- Settings: live reasoning **enabled**, mode **live**, endpoint `token-plan-sgp.xiaomimimo.com`; "Scout, Architect, and Critic may receive a grounded narrative prompt"; "Every returned statement must cite ... ungrounded statements are dropped."
- Migrator/codebase: badge **"Offline deterministic"** next to primary buttons **"Run live · mimo-v2.6-flash"** / **"Run live"**, and a "Live Critic" checkbox.
- There is no confirmation or data-boundary note at the live controls, and no link from the live controls to Settings.

**Reproduction:**
1. Open `/settings`; read the Optional live reasoning section.
2. Open `/migrator?run=R-DEMO-001`; compare the header "Local-only" and "Offline deterministic" badge with "Run live".
3. Open `/codebase`; compare "Offline deterministic" with the "Live Critic" checkbox and "Run live".
**Expected:** "Offline by default; live reasoning is opt-in and sends synthetic fixture content to <endpoint>" next to the live control, and a status that distinguishes the current run from available modes.
**Evidence:** `settings-1440.png`, `migrator-1440.png`, `codebase-cascade-1440.png`.

#### H3. Upgrade invalidation leaves contradictory stale narratives
**Seen at:** `/codebase` → **Upgrade resilience** → **Evaluate upgrade** (default scenario).
**Observed:** The banner and outcome correctly become "Not green yet ... stale after core release upgrade" and `revalidation_required`. At the same time:
- the title still says **"Cascade Mutual: a completed code-migration rehearsal"**;
- "What just happened" still says the final Guardian verdict is green, the final Critic verdict is green, and Planner compiled the report;
- the iteration 2 card still shows green and "Planner compiled";
- the "No context needed" card still advertises a completed rehearsal.
There is also a grammar/casing defect in the banner: "stale after core release upgrade Human approval required: yes."

**Reproduction:**
1. Open `/codebase?case=cascade-mutual`.
2. Click **Upgrade resilience**.
3. Press **Evaluate upgrade** with the default APD scenario.
4. Scroll to the top and read the banner, title, no-context card, and "What just happened" together.
**Expected:** Either mark the historical content "pre-upgrade / superseded by revalidation" or update all summaries to the not-green state.
**Evidence:** `codebase-upgrade-top-1440.png`, `codebase-upgrade-evaluated-1440.png`.

#### H4. Feature-loop "Replay loop" does nothing and gives no feedback
**Seen at:** `/migrator?run=R-DEMO-001` agent crew toolbar.
**Observed:** I clicked a stage (Guardian), noted "Step 3 of 5 · Guardian", and clicked **Replay loop**. After 3 seconds the step was still 3, the body text was byte-identical, there was no toast, no URL change, and no new network request. On `/codebase`, the same button at least shows a toast: "Loop replay complete. Green signal still requires human approval," although the visible stage does not change.
**Reproduction:**
1. Open `/migrator?run=R-DEMO-001`.
2. Click the Guardian stage card (`[data-agent=guardian]`).
3. Click **Replay loop** (`[data-agent-replay]`).
4. Wait 3 seconds; observe no change. Compare with **Play**, which advances the stages and changes the button label to **Pause**.
**Expected:** Replay should reset to Scout and visibly animate through the five stages, or explain what was replayed.
**Evidence:** `replay-before-1440.png`, `replay-after-1440.png` (same stage; after screenshot differs only because the button received focus).

#### H5. Evidence table is clipped with no scroll affordance
**Seen at:** `/migrator` → stage 1 → **Evidence handed to Architect** → `.scout-evidence-table`.
**Observed:**
- At 1440: table scroll width **1,339 px** vs **1,110 px** visible; the EXCERPT column is cut at the right edge (`label="V...`).
- At 390: table scroll width **1,339 px** vs **332 px** visible; only EVIDENCE and FILE are visible; the locator and excerpt are hidden.
- The wrapper is `.table-scroll` (not `.table-scroll.is-scrollable`), has no visible scrollbar, and has no "scroll horizontally" hint. It does have `tabindex="0"` and an aria-label, so keyboard users can pan, but sighted mouse/touch users get no cue. Unlike Settings, About, and Manifest, which do show a scroll hint, this critical evidence table does not.
**Reproduction:**
1. Open `/migrator?run=R-DEMO-001`.
2. Scroll to "Evidence handed to Architect."
3. Look at the right edge of the table at 1440; repeat at 390.
**Expected:** A visible horizontal-scroll affordance and/or a sticky first column, plus a hint like the one used on the Manifest page.
**Evidence:** `migrator-evidence-1440.png`, `migrator-390-evidence.png`.

#### H6. Mobile feature graph hides half its columns with no affordance
**Seen at:** `/` at 390 → **Feature spine** → `.spine-scroll`.
**Observed:** The graph is 672 px wide inside a 330 px viewport. Only PCF, ENTITY, and TYPELIST are visible; TEMPLATE/GOSU, API DRAFT, and TESTS are off-screen to the right. There is no "scroll horizontally" hint; the scroll container has no `tabindex`/role/label. The copy says "Six columns read left to right," which tells the user they exist but not that the region scrolls. Selecting a node requires horizontal panning first.
**Reproduction:**
1. Open `/` at 390 × 844.
2. Scroll to "Feature spine."
3. Observe only three columns; swipe horizontally; the other columns appear.
**Expected:** A visible pan/zoom control or scroll hint, or a responsive reflow of the graph (e.g., per-column stacked cards) on narrow screens.
**Evidence:** `home-390-spine.png`, `home-390-full.png`.

### Medium

#### M1. Five packages and eight bundle files are asserted, not explained
**Seen at:** `/migrator` stages 2, 3, 5.
**Observed:** Stage 2 lists five target rows, the "What just happened" handoff strip says Guardian received "5 work packages and 8 bundle artefacts" before Scribe exists, and Stage 5 says "8 bundle files" while naming only four outputs. The eight-file breakdown (5 targets + plan + report + audit log) is only in the unlinked bundle manifest. The screen never states why five packages is the right number, or why eight files is the right count.
**Reproduction:**
1. Open `/migrator?run=R-DEMO-001`.
2. Click Architect; read the five packages.
3. Click Guardian; read the "8 bundle artefacts" handoff.
4. Click Scribe; read "8 bundle files" and the four named artifact groups.
**Expected:** A one-line rationale and an expandable eight-item file list on Scribe.
**Evidence:** `migrator-step2-1440.png`, `migrator-step3-full-1440.png`, `migrator-step5-1440.png`.

#### M2. Evidence counts do not reconcile
**Seen at:** `/` (31 evidence records), `/migrator` (31 evidence links and 101 evidence records), `/packet` (126 evidence items), `/codebase` (15 audit events), `/migrator` (12 events), `/packet` (9 events).
**Observed:** Four different "evidence" totals and three different "audit" totals. Each is probably scoped correctly, but the screen never says so.
**Reproduction:** Open the four pages in the order above; compare the labels in the stat grids, Scout's PRODUCED panel, packet section 06, and the audit labels.
**Expected:** A scope line ("31 links for this feature; 101 estate records; 126 packet items") and a matching scope on each audit count.
**Evidence:** `home-evidence-node-1440.png`, `migrator-evidence-1440.png`, `packet-1440.png`.

#### M3. "Record revalidate" commits immediately with no confirmation or reason
**Seen at:** `/codebase` → Upgrade resilience → after Evaluate upgrade.
**Observed:** The resume-option area has one-click **Record revalidate / rollback / defer** buttons. Clicking **Record revalidate** immediately displays a toast ("Upgrade response recorded: resume_requested") and adds `upgrade=...` to the URL. There is no confirmation dialog, no required reason, and no visible undo. By contrast, `/findings` and `/reconstruction` use a proper "Record decision" dialog requiring a reason.
**Reproduction:**
1. Open `/codebase`.
2. Open **Upgrade resilience**, press **Evaluate upgrade**.
3. Click **Record revalidate**.
4. Observe the immediate toast and changed URL.
**Expected:** Reuse the decision dialog (reason required, cancel/confirm) or label it "Preview revalidate" until a separate commit.
**Evidence:** `codebase-upgrade-recorded-1440.png`.

#### M4. "The value is not a score" contradicts visible target/readiness scores
**Seen at:** `/codebase` no-context card, Iterative patching, Gates/report tab.
**Observed:** "The value is not a score. It is a traceable list..." is immediately followed lower in the page by "Target score 65/100", "Target score 100/100", "0 BEFORE / 100 STRUCTURAL AFTER / 74 AFTER HUMAN GATES", and a Planner "readiness score."
**Reproduction:** Open `/codebase`; read the no-context card, then scroll to Iterative patching and the Planner report.
**Expected:** Either consistently call these "readiness indicators" with the qualifier adjacent to every number, or remove the absolute "not a score" sentence.
**Evidence:** `codebase-1440.png`, `codebase-iterations-1440.png`, `codebase-tab3-gates-1440.png`.

#### M5. Codebase findings cannot be inspected
**Seen at:** `/codebase` → **Source findings (18)**.
**Observed:** The section header promises "18 findings · line evidence · stable fingerprints", but the table has no fingerprint column, no `Inspect` link, no expandable row, and no evidence excerpt. Only a path:line and a MESSAGE/CLOUD TARGET. This is inconsistent with `/findings`, where the same design allows inspection, excerpt, and decisions.
**Reproduction:**
1. Open `/codebase`.
2. Click **Source findings (18)**.
3. Click any `CF-xxxx` row.
4. Observe that nothing expands or navigates; there is no action control.
**Expected:** Row expansion with the source excerpt and evidence fingerprint, or a direct "Inspect" link.
**Evidence:** `codebase-tab1-source-1440.png`, `codebase-finding-detail-1440.png`.

#### M6. 1280 layout detaches the primary live action
**Seen at:** `/codebase` at 1280 × 720.
**Observed:** The toolbar wraps: "Migrator story / Cascade / Harbor / All stories / Replay / Run fresh / Live Critic / model" fills the first row, then **Run live** sits alone on a second row at the far left. At 1440 it is one row. It looks like a stray control rather than the primary action.
**Reproduction:** Open `/codebase` at 1280 × 720; inspect the action bar.
**Expected:** Keep the primary action with its related live controls in a single visually coherent group, or use an overflow menu.
**Evidence:** `codebase-cascade-1280.png`.

#### M7. Page depth and repeated explainers bury the actual work
**Observed heights:**
- Codebase at 1440: **5,108 px**; at 390: **11,118 px**.
- Home at 1440: 2,505 px; at 390: 5,652 px.
- Stories at 1440: 2,880 px; at 390: 6,941 px.
- Migrator at 1440: 2,594 px; at 390: 5,611 px.
- Mobile codebase tabs are at **y≈2,322**; the iteration comparison is at **y≈7,104**. The first H1 on mobile home starts at **y≈350**, after header + context bar + menu (≈41% of the viewport).
**Observed repetition:** `/codebase` has the hero paragraph, the "Unified green signal" callout, the "No context needed" card, "What just happened", and the glossary all before the actual tab content. Home repeats "what it is" in the hero and again in the start-here card.
**Reproduction:** Open `/codebase` at 390; count the screens before the tab strip; scroll to Iterative patching.
**Expected:** A compact "read this first" disclosure and a sticky tab jump bar; move the long narratives to one expandable "Learn" drawer.
**Evidence:** `codebase-cascade-390.png`, `codebase-390-tabs.png`, `home-390-full.png`.

#### M8. Navigation labels do not describe the same page consistently
**Seen at:** All pages.
**Observed:**
- Sidebar: **Agent loop** → breadcrumb: **Migrator** → H1: **Watch the migration crew work**.
- Sidebar **Findings** (24 feature findings) vs codebase tab **Source findings (18)** — same phrase, different sets, no cross-link.
- Stories CTA **Explore the five-agent run** → `/codebase` (Planner loop), while the sidebar **Agent loop** → `/migrator` (Scribe loop).
- Runs lists only feature runs; Cascade/Harbor codebase rehearsals are absent.
- Breadcrumbs are plain `<span>`s and cannot be clicked.
**Reproduction:** Use the sidebar and breadcrumbs across `/`, `/migrator`, `/codebase`, `/findings`, `/runs`; click the stories CTA.
**Expected:** One name per concept; explicit "Feature loop / Codebase loop" badges next to the nav items; clickable breadcrumbs; a codebase run entry or a note that stories are not runs.
**Evidence:** `migrator-1440.png`, `findings-1440.png`, `stories-1440.png`, `runs-1440.png`.

#### M9. Mobile menu loses the information architecture
**Seen at:** `/` at 390 → **Sections** menu.
**Observed:** Opening the menu yields a two-column grid of 12 links with no **AGENT DEMO / REVIEW / WORKSPACE** labels. "Migration stories" is adjacent to "Workbench"; "Runs" is adjacent to "Settings". The desktop grouping is the only clue that these belong to different workflows. Link heights are 39.5 px, below the 44 px touch-target guideline.
**Reproduction:** Open `/` at 390, tap **Sections**, inspect the grid.
**Expected:** Preserve group headings in the mobile panel or use a single-column accordion.
**Evidence:** `home-390-nav-open.png`.

#### M10. Status vocabulary is overloaded
**Seen at:** All pages.
**Observed phrases for essentially two states:**
`SUCCEEDED`, `completed_with_gates · 100%`, `sealed · gates open`, `non-deployable draft`, `DONE`, `green · human gates open`, `Unified green signal`, `green_with_human_gates`, `machine-green`, `revalidation_required`, `rework`, `PASS`, `open by design`, `pending`.
There is no single status legend that says which are run states, which are machine-check states, which are human-review states, and which are artifact states.
**Reproduction:** Compare `/`, `/migrator`, `/codebase`, `/case-studies`; list every status phrase.
**Expected:** A status legend with three axes: run lifecycle, machine verification, human approval.
**Evidence:** `home-1440.png`, `migrator-1440.png`, `codebase-1440.png`, `stories-1440.png`.

#### M11. "Generation 1" vs "2 iterations"
**Seen at:** `/codebase`.
**Observed:** The top-right badge says **generation 1**; the body and outcome say **2 iterations** and show Iteration 1/Iteration 2. The upgrade result says "Generation 1 → 2" after evaluation. "Generation" is never defined; a reader can plausibly infer only one iteration happened.
**Reproduction:** Open `/codebase`; compare `.status-badge` "generation 1" with "2 LOOP ITERATIONS" and the iteration cards.
**Expected:** Label it "bundle generation 1" or show "iteration 2 / generation 1".
**Evidence:** `codebase-1440.png`, `codebase-iterations-1440.png`.

#### M12. Table text wraps mid-token and is hard to scan
**Seen at:** `/codebase` Source findings; `/reconstruction` mapping table; `/packet` assumption table; `/manifest` hash column.
**Observed:** In `/codebase` Source findings at 1440, the ID column is only about 40 px wide, so `CF-0001` breaks into "CF-/000/1"; the CLOUD TARGET column is clipped at the right edge (table 1,180 px inside a 1,110 px wrapper) with no scroll hint. On `/findings` at 1440, the side detail panel leaves the table about 800 px, so the STATE and ACTIONS columns are partly hidden in the table's own horizontal scroller even though the page says "Scroll horizontally"; at 390 only the leftmost columns are visible. Elsewhere, `PersonalAutoRatingFactorConfiguration` splits as "PersonalAutoRatingFac torConfiguration"; `unassigned` splits as "unassig ned"; SHA-256 values wrap into 2–3 lines; action buttons in Reconstruction wrap onto two rows. These are 1440 sightings, not only mobile.
**Reproduction:** Open `/codebase` → Source findings; look at the ID and last columns. Open `/reconstruction`; look at M-05. Open `/packet`; look at OWNER. Open `/manifest`; look at SHA-256.
**Expected:** `overflow-wrap: anywhere` only for hashes, no mid-word breaks for ordinary words, and wider columns or a detail drawer for long values.
**Evidence:** `codebase-finding-detail-1440.png`, `findings-1440.png`, `reconstruction-1440.png`, `packet-1440.png`, `manifest-1440.png`.

#### M13. Raw internal tokens are exposed as user-facing labels
**Seen at:** `/reconstruction`, `/codebase` patch detail, `/codebase` upgrade result.
**Observed:** `mapped_transformed`, `guidewire-doc`, `revalidation_required`, `resume_requested`, "semantic review: True", "secret-redacted diff: False". The last two are Python booleans in a human review panel; the rest are snake_case internal state.
**Reproduction:** Open `/reconstruction`; open `/codebase` → Patches → CP-001; open Upgrade resilience → Evaluate.
**Expected:** Human labels ("Mapped and transformed", "Guidewire documentation", "Revalidation required") with technical values available in a details view.
**Evidence:** `reconstruction-1440.png`, `codebase-patch-detail-1440.png`, `codebase-upgrade-evaluated-1440.png`.

#### M14. Essential glossary terms are missing
**Seen at:** `/about#glossary` and throughout.
**Observed missing:** **PCF**, **GUnit**, **SBT**, **Qusar**, **Cloud Assurance**, **Cloud Retrofit**, **APD App**, **MiMo**, **work package**, **target draft**, **bundle artefact**, **generation**, **readiness**, **macro-F1**, **reference target**, and the **TP/FP/FN** metric abbreviations.
The glossary does define evidence link, feature, disposition, assumption, gate, SARIF, Gosu, APD, Cloud Data Access, and App Events, which is a good start. But the first sentence of the product ("PCF, entity metadata, typelists...") already uses an undefined acronym.
**Reproduction:** Open `/about#glossary`; then search the product pages for each missing term.
**Expected:** Add the missing terms, especially "Cloud Assurance" (used as the key disclaimer) and "PCF/GUnit" (used in the first and codebase views).
**Evidence:** `about-1440.png`, `codebase-1440.png`, `findings-1440.png`.

#### M15. "Live reasoning" configuration is not actionable from the screen
**Seen at:** `/settings`.
**Observed:** The page says to change `.env` and restart, but it never names the environment variables, shows no sample, and offers only a **Test connection** button whose result is not described. A newcomer cannot perform the task from this page alone.
**Reproduction:** Open `/settings`; read the Optional live reasoning section; look for variable names or a copyable snippet.
**Expected:** Show `PREFLIGHT_LIVE_BASE_URL` / `PREFLIGHT_LIVE_API_KEY` (or the actual names) and the exact restart command, without displaying values.
**Evidence:** `settings-1440.png`.

### Low / polish

| ID | Page / selector | Defect | Reproduction | Screenshot |
|---|---|---|---|---|
| L1 | `/migrator` skip link | Skip link scrolls to `#main`, but `document.activeElement` remains `BODY`; next Tab jumps into main at "Replay loop" rather than moving focus/announcing the main region. | Press Tab, Enter on "Skip to content"; inspect focus. | `migrator-skip-focus-1440.png` |
| L2 | `/codebase` tabs | `role="tab"` buttons do not support ArrowLeft/ArrowRight and do not use roving tabindex; ArrowRight on the focused "Five-agent loop" tab does nothing. | Focus "Five-agent loop"; press ArrowRight; observe no change; Tab moves to "Source findings." | `codebase-390-tabs.png` |
| L3 | `/` and all pages | Axe: `label-content-name-mismatch` on `.brand` (aria-label "PreFlight home" does not include visible "Cloud-readiness review") and on three SVG nodes; accessible names do not contain the visible node text exactly. | Run axe-core on `/`; inspect the four nodes. | `home-1440.png` |
| L4 | `/codebase` agent cards | Heading order skips a level: H4 "RECEIVED"/"PRODUCED" under H2 "Agent-by-agent" (axe heading-order). | Run axe-core on `/codebase`. | `codebase-tab0-fiveagent-1440.png` |
| L5 | Mobile controls | Primary toolbar buttons are 28 px high; nav links 39.5 px; checkbox 13 px. Usable, but below the 44 px touch guideline and easy to miss. | Measure at 390; use touch emulation. | `migrator-390-crew.png`, `home-390-nav-open.png` |
| L6 | `/codebase?case=harbor-pc` | Document horizontal overflow: 1,290 px at 1280 viewport; 392 px at 390. A long `<code>` path in the inventory is not contained. | Open Harbor at 1280 and 390; measure `documentElement.scrollWidth`. | `codebase-harbor-1280.png`, `codebase-harbor-390.png` |
| L7 | `/codebase` Agent-by-agent grid | Five agent cards are laid out in a four-column grid; Planner sits alone on a second row with a large empty area at 1440. | Open `/codebase`; scroll to Agent-by-agent. | `codebase-tab0-fiveagent-full-1440.png` |
| L8 | `/findings` source column | Full source path exists only in a `title` tooltip; not available to touch users, and truncated to `gsrc/acme/err...` in the table. | Open `/findings` at 390; inspect SOURCE column. | `findings-390.png` |
| L9 | `/migrator` | The H1/title block uses a two-line uppercase eyebrow and a two-line H1 at 1280; the date/time line breaks in the middle of the timestamp. Minor hierarchy/typography. | Open `/migrator` at 1280. | `migrator-1280.png` |
| L10 | `/` evidence panel | Assistant "Open evidence" scrolls to the evidence panel at `#evidence-drawer` rather than opening an overlay; the page movement is easy to miss on a long page. | Ask "Long type?", click "Open evidence." | `home-open-evidence-1440.png` |
| L11 | `/migrator` | Scribe's four artifact cards show truncated hashes as the only identifiers; there is no copy button on each. | Open stage 5; inspect PLAN/REPORT/BUNDLE/AGENT LOG. | `migrator-step5-1440.png` |
| L12 | `/evaluation` | "Top-8 allowance", TP/FP/FN and Wilson intervals are shown without definitions; "6/6" and "6/8" are both prominent and easy to misread. | Open `/evaluation`. | `evaluation-1440.png` |
| L13 | `/packet` | "unassigned" breaks as "unassig ned" in the 1440 assumption table. | Open `/packet`; inspect OWNER column. | `packet-1440.png` |
| L14 | Nav / mobile | Breadcrumbs are non-interactive spans; mobile menu loses group labels. | Click "Workspace" in the breadcrumb; open mobile menu. | `home-390-nav-open.png` |
| L15 | `/runs` | Codebase case studies are absent from Runs; no indication that they are static demos rather than persisted runs. | Open `/runs`; compare with `/codebase` case chips. | `runs-1440.png` |
| L16 | `/codebase` upgrade banner | "stale after core release upgrade Human approval required: yes." lacks punctuation/capitalization and reads like concatenated template strings. | Evaluate upgrade; read banner. | `codebase-upgrade-top-1440.png` |
| L17 | `/` | "Spine table fallback" is developer language for the accessible table; a newcomer will not know to open it. | Open `/`; scroll below graph; expand "Spine table fallback". | `home-spine-table-1440.png` |

### Console / network / overflow checks

- **Console errors:** none across all 13 pages at 1440, 1280, and 390, and across the interactions I exercised. No page errors.
- **Failed requests:** none observed for the reviewed pages.
- **Document horizontal overflow:** clean except Harbor P&C (10 px at 1280, 2 px at 390). All other pages had `scrollWidth === clientWidth` at the document level.
- **Intentional inner overflow:** migrator evidence table (1,339/1,110 at 1440; 1,339/332 at 390), home feature graph (672/330 at 390), findings table (800/332 at 390), codebase diff blocks (627/308 at 390). Most have a hint; the migrator evidence table and home graph do not.
- **Page heights:** home 2,505/5,652; migrator 2,594/5,611; codebase 5,108/11,118; stories 2,880/6,941 (1440/390). These are not functional bugs, but they are why the work feels buried.

---

## 6. Accessibility test details

Automated axe-core scan (WCAG 2 A/AA + best practice) across nine pages at both 1440 and 390 — Home, Migrator, Codebase, Stories, Settings, About, Findings, Reconstruction, and Manifest — found exactly two rule types:

1. **`label-content-name-mismatch` (serious):**
   - `.brand` on every page: accessible name "PreFlight home" excludes visible "Cloud-readiness review".
   - Three SVG nodes on `/`: visible "Vehicle Validation" vs accessible names that do not contain that exact text.
2. **`heading-order` (moderate):**
   - `/codebase` stage/agent cards place H4 "RECEIVED"/"PRODUCED" under an H2 "Agent-by-agent" with no H3.

Manual accessibility checks:

- **Positive:** Native `<dialog>` receives focus in the reason textarea; Escape closes it. `aria-live="polite"` is present on the assistant transcript and evidence regions. Table scroll wrappers have `tabindex="0"`, `role="region"`, and descriptive labels. SVG nodes respond to Enter and Space. No color-contrast failures found by axe; the only sub-4.5 contrast elements I found were decorative separators/arrows.
- **Negative:** Skip link does not move active focus to `#main`. Tabs lack ArrowLeft/ArrowRight handling. Source paths depend on a title tooltip. Mobile graph scroll container is not focusable. Primary controls are below the 44 px touch target guideline.

---

## 7. What is genuinely working well

- The **What it is / What it is not / Three promises** section is excellent no-context framing.
- The **five-agent stage panels** are the strongest product idea: every role has explicit `RECEIVED`, `WORK`, and `PRODUCED`, and the stage cards are clickable.
- The **machine-green vs human approval** boundary is stated in plain language on multiple pages. The repeated "Official Cloud Assurance: not run" is a responsible safety choice.
- The **feature evidence panel** and **assistant refusal** are good examples of evidence-first behavior: file, locator, excerpt, hash; "Cannot determine" when evidence is absent.
- The **upgrade simulation** is concrete and understandable; it identifies affected patches and offers revalidate/rollback/defer.
- The **migration stories** have real specificity (policies, states, custom Gosu, integrations, constraints) rather than generic marketing copy.
- The **decision dialogs** on Findings and Reconstruction are well-designed: confirmation, required reason, and audit-trail language.
- There are **no console errors**, and the app is fast enough at all three viewports.

---

## 8. Priority fixes

1. **Fix the gate vocabulary and gate actions.** Rename machine checks to "machine checks" and reserve "gate" for human-owned decisions. Either make every human gate actionable (assign owner, accept/reject/defer with reason) or explicitly say "assignment happens outside this demo." Resolve the "Owner: unassigned" contradiction on Home.
2. **Make live/offline status truthful and local to the run.** Replace the global "Local-only"/"Offline deterministic" ambiguity with `This run: offline deterministic` and `Live reasoning: available (opt-in; sends synthetic content to ...)`. Add a visible data-boundary statement at every live action.
3. **Fix the feature-loop Replay loop.** It should reset to Scout and visibly replay, or be removed. Keep the codebase toast behavior.
4. **Fix the evidence table and mobile graph affordances.** Add a visible horizontal-scroll hint and sticky identifiers to the evidence table; add a pan/zoom/reflow affordance to the feature graph.
5. **Clean up the status/evidence counts.** Add a reconciliation legend: feature link vs estate record vs packet item; bundle artefact vs bundle file; run audit events vs packet audit events. Add an eight-item bundle list to Scribe.
6. **Make upgrade invalidation consistent.** Update or label every summary when `revalidation_required`; preserve history as "pre-upgrade" instead of leaving it green. Require a reason/confirmation for `Record revalidate` like every other decision.
7. **Remove the score contradiction.** Use "readiness indicator" consistently and place the "not a Cloud Assurance score" qualifier next to every numeric score.
8. **Tighten mobile hierarchy.** Add a sticky jump bar for codebase tabs; collapse the repeated "read this first" content; preserve mobile nav group headings; raise touch targets to at least 44 px.
9. **Expand the glossary.** Add PCF, GUnit, SBT, Qusar, Cloud Assurance, Cloud Retrofit, APD App, MiMo, work package, target draft, bundle artefact.
10. **Fix accessibility details.** Make skip link focus `main`; implement arrow-key navigation for tabs; align visible and accessible names; fix the H4/H2 sequence; make source paths available without hover.

---

## 9. Screenshot index

All paths are relative to `docs/audits/screenshots/no-context-round2/`.

- **Home/Workbench:** `home-1440.png`, `home-1280.png`, `home-390.png`, `home-390-full.png`, `home-390-nav-open.png`, `home-390-spine.png`, `home-evidence-node-1440.png`, `home-node-focus-1440.png`, `home-spine-table-1440.png`, `home-assistant-1440.png`, `home-open-evidence-1440.png`, `home-unknowns-1440.png`
- **Agent loop:** `migrator-1440.png`, `migrator-1280.png`, `migrator-390.png`, `migrator-390-crew.png`, `migrator-390-evidence.png`, `migrator-step1-1440.png` through `migrator-step5-1440.png`, `migrator-step1-full-1440.png` through `migrator-step5-full-1440.png`, `migrator-evidence-1440.png`, `migrator-replay-start-1440.png`, `migrator-replay-mid-1440.png`, `replay-before-1440.png`, `replay-after-1440.png`, `migrator-skip-focus-1440.png`
- **Codebase lab:** `codebase-cascade-1440.png`, `codebase-cascade-1280.png`, `codebase-cascade-390.png`, `codebase-cascade-390-full.png`, `codebase-harbor-1440.png`, `codebase-harbor-1280.png`, `codebase-harbor-390.png`, `codebase-tab0-fiveagent-1440.png`, `codebase-tab1-source-1440.png`, `codebase-tab2-patches-1440.png`, `codebase-tab3-gates-1440.png`, `codebase-tab4-upgrade-1440.png`, `codebase-iterations-1440.png`, `codebase-patch-detail-1440.png`, `codebase-finding-detail-1440.png`, `codebase-390-tabs.png`, `codebase-390-patch.png`, `codebase-upgrade-evaluated-1440.png`, `codebase-upgrade-top-1440.png`, `codebase-upgrade-recorded-1440.png`
- **Stories:** `stories-1440.png`, `stories-1280.png`, `stories-390.png`, `stories-390-full.png`
- **Settings/About:** `settings-1440.png`, `settings-1280.png`, `settings-390.png`, `settings-390-full.png`, `about-1440.png`, `about-1280.png`, `about-390.png`, `about-390-full.png`
- **Review pages:** `manifest-1440.png`, `manifest-390.png`, `manifest-390-table.png`, `reconstruction-1440.png`, `reconstruction-390.png`, `reconstruction-draft-1440.png`, `reconstruction-assumptions-1440.png`, `reconstruction-comparison-1440.png`, `findings-1440.png`, `findings-390.png`, `findings-evidence-1440.png`, `findings-accept-modal-1440.png`, `evaluation-1440.png`, `evaluation-390.png`, `packet-1440.png`, `packet-390.png`, `runs-1440.png`, `runs-390.png`
