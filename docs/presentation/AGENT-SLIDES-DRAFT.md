# PreFlight — Agent slides draft

**Status:** draft only. Not integrated into `index.html`.
**Deck math:** 16 existing slides + 7 new slides = **23 slides**.
**New slide numbers:** 13–19. Existing slides 13–16 shift to 20–23.
**Checked:** 2026-11-11 against `R-DEMO-001`, the live MiMo run `R-20261111-052740-b001`, and fresh Cascade/Harbor codebase runs.

This draft adds one narrative block after the packet slide: the feature migrator (four slides), then the codebase lab (three slides). It reuses the run the audience has already seen, so the new material adds no new fixture context.

**Tone guardrails for the writer**

- Use: **synthetic**, **bounded**, **human gates open**, **not an official Cloud Assurance result**.
- Name statuses exactly: `completed_with_gates`, `green_with_human_gates`.
- Attribute every count to a run or artifact. Prefer “the run reports” over “the system proves”.
- Describe outputs as drafts, review artifacts, or bounded checks — not as a completed migration.
- Do not imply certification, deployment, or perfect detection.
- Fit rule: preserve the numbers and the boundary line; drop optional detail before shrinking type.

---

## Placement

| New order | Slide | Section | Insertion point | Replaces |
|---:|---|---|---|---|
| 13 | (a) Five-agent loop overview | Demo · Migrator | After current slide 12 (Packet) | No |
| 14 | (b) Scout → Architect handoff | Demo · Migrator | After new slide 13 | No |
| 15 | (c) Guardian’s 11 gates | Demo · Migrator | After new slide 14 | No |
| 16 | (d) Critic 7/7 and Scribe seal | Demo · Migrator | After new slide 15 | No |
| 17 | (e) Two insurer migration stories | Demo · Codebase lab | After new slide 16 | No |
| 18 | (f) Code-level refactor and SARIF | Demo · Codebase lab | After new slide 17 | No |
| 19 | (g) Upgrade resilience | Demo · Codebase lab | After new slide 18 | No |

Then:

| Old slide | New order | Title |
|---:|---:|---|
| 13 | 20 | Engineering rigor |
| 14 | 21 | Novelty and prior art |
| 15 | 22 | Viability and limitations |
| 16 | 23 | Close and ask |

All seven new slides sit between current slides 12 (Packet) and 13 (Engineering rigor). The per-slide “follows new slide” notes refer to this new block order; none replaces an existing slide.

**Optional live MiMo callout:** place it once inside slide 13. Do not add a separate slide, and do not duplicate it on slide 16.

---

## Source of truth used

| Claim | Artifact |
|---|---|
| Feature migrator counts, status, gates, verification | `data/runs/R-DEMO-001/migration.json` (`summary`, `agents`, `gates`, `verification`) |
| Sealed bundle, 8 listed files, hashes | `data/runs/R-DEMO-001/migration/bundle-manifest.json` |
| 12-event agent log | `data/runs/R-DEMO-001/migration/audit.jsonl`; `preflight verify-migration R-DEMO-001` |
| Live MiMo annotations and usage | `data/runs/R-20261111-052740-b001/migration.json` (`llm.annotations`) |
| Cascade and Harbor counts | `docs/PROJECT-REPORT.md` §7; fresh `.venv/bin/python -m app.cli codebase ...` runs; each case’s `MIGRATION-REPORT.md` |
| Upgrade exposure counts | `app/services/resilience.py`; `evaluate_upgrade` on the current Cascade and Harbor runs |
| 16 code rule families | `rules/codebase_rules.yaml`; `docs/PROJECT-REPORT.md` §6.2 |
| Five upgrade scenarios and resume options | `app/services/resilience.py`; `docs/CODEBASE-MIGRATION.md` §8 |
| Current slide order | `docs/presentation/index.html` |

---

## Slide 13 — Demo · Migrator — (a) Five-agent loop overview

**1. Slide number and section**
New slide **13**, section **Demo · Migrator**. Insert after current slide 12 (Packet). Replaces none.

**2. Headline**
> **Five agents. One evidence chain. No authority to deploy.**

**3. Lede (4 sentences)**
> The feature migrator runs five specialist agents over the completed PA-VEH-01 review: Scout, Architect, Guardian, Critic, and Scribe. Each receives the prior artifact, adds a check or an artifact, and leaves a record. The run ends `completed_with_gates` with 11 gates open; it does not end in approval or deployment. The page calls it a loop; this path is a straight handoff chain, while the codebase lab is the cyclic variant.

**4. Exact content blocks**

**Block A — the handoff in five artifacts**

| # | Agent | Handoff | Exact output |
|---:|---|---|---|
| 1 | **Scout** | review → scope | 300 files · 101 evidence records · 31 links on PA-VEH-01 · 24 findings · 12 dispositions |
| 2 | **Architect** | scope → draft | 5 work packages · 5 target files · all `draft_ready` · all `pending` |
| 3 | **Guardian** | draft → gates | 11 open gates = 3 assumptions + 8 rule groups · 6 high |
| 4 | **Critic** | gates → checks | 7/7 checks passed · verdict PASS · 0 auto-approved |
| 5 | **Scribe** | checks → seal | 8 listed bundle files · 5 targets + plan + report + 12-event log · manifest seals them · `completed_with_gates` |

**Block B — status bar**

> `R-DEMO-001` · `completed_with_gates` · verification passed (7/7) · 11 gates open · no deployment

**Block C — boundary callout**

> **Bounded autonomy.** Read the snapshot, generate local drafts, verify, seal. Never deploy, edit `_gen`, approve a change, resolve an assumption, or contact a tenant.

**Block D — optional live MiMo callout (slide 13 only)**

> **LIVE MIMO REASONING · OPTIONAL** — `mimo-v2.6-flash` adds citation-checked commentary for Scout, Architect, and Critic on synthetic fixture text. Three calls; no ungrounded claim passed validation; Guardian makes zero model calls. Example: Critic 1,706 tokens / 14.5 s. The deterministic 7/7 checks and sealed status are unchanged. Live run `R-20261111-052740-b001`.

**5. Suggested visual and screenshot target path**

| Item | Detail |
|---|---|
| Primary visual | Five-column handoff strip built in HTML/SVG, with the optional MiMo callout in the lower-right. |
| Screenshot target | `docs/presentation/assets/agents/migrator-loop-1440x900.png` |
| Optional focus crop | `docs/presentation/assets/agents/migrator-loop-focus.png` |
| Source URL | `http://127.0.0.1:8000/migrator?run=R-DEMO-001` |
| Capture status | Exists: `docs/presentation/assets/agents/migrator-loop-1440x900.png` (1440 × 900, 0 overflow, no console errors). |

**6. Speaker notes (5 sentences)**

> Start with the chain, not the badge. Scout’s numbers are the same ones on the workbench slides: 300 files, 101 evidence records, 31 links on PA-VEH-01, 24 findings, 12 dispositions. Architect produces five local files, Guardian opens 11 gates, Critic runs seven checks, and Scribe seals the bundle; none of them can approve or deploy. If asked about the “loop” label, say the feature path is a straight handoff chain and the cyclic rework loop is the codebase lab. Say plainly: synthetic fixtures, bounded checks, human gates open, not an official Cloud Assurance result.

**7. Placement**
New slide 13. Follows current slide 12 (Packet); replaces none. Current slide 13 becomes 20.

---

## Slide 14 — Demo · Migrator — (b) Scout → Architect handoff

**1. Slide number and section**
New slide **14**, section **Demo · Migrator**. Follows new slide 13. Replaces none.

**2. Headline**
> **Scout hands over 31 links and 12 dispositions. Architect writes five files.**

**3. Lede (4 sentences)**
> Scout resolves PA-VEH-01 from 300 files and 101 evidence records, keeping 31 links, 24 findings, and 12 dispositions attached to the handoff. Architect turns those dispositions into five local targets: schema, mapping, updater, codegen config, and API contract. The mapping file carries all 12 dispositions, so five files do not mean five trivial changes. Every target is `draft_ready` and `pending`.

**4. Exact content blocks**

**Block A — Scout → Architect strip**

> **Scout → Architect** · 300 files · 101 evidence records · 31 links on PA-VEH-01 · 24 findings · 12 dispositions · snapshot `bd4a8a4b338a`

**Block B — five work packages**

| WP | Target (basename) | Disposition | Evidence | Bytes | Gate / approval |
|---|---|---|---|---|---|
| **WP-01** | `policyperiod_pa_ext-1.0.schema.json` | PAVehicle → PersonalVehicle | EV-0011, EV-0018 | 945 B | — / `pending` |
| **WP-02** | `policyperiod_pa_ext-1.0.mapping.json` | PAVehicle.Year → ModelYear | EV-0002, EV-0006 | 3,046 B | — / `pending` |
| **WP-03** | `policyperiod_pa_ext-1.0.updater.json` | PADriver → VehicleDriver | EV-0057, EV-0061 | 402 B | — / `pending` |
| **WP-04** | `pa_codegen_config_ext-1.0.yaml` | PALine → PersonalAutoLine | EV-0097 | 520 B | — / `pending` |
| **WP-05** | `pa_ext-1.0.yaml` | PersonalAutoRatingFactorConfiguration → same | EV-0036 | 78 B | **G-03** / `pending` |

Full target paths are under `migration/target/config/integration/`. All five are `mapped_transformed`.

**Block C — callout**

> **Five files, twelve dispositions.** WP-02 is a 12-entry mapping file; WP-05 is the only package carrying a gate at handoff (G-03, 37-character APD type). Five target files are not five deployment units.

**Block D — boundary strip**

> `_gen` targets: 0 · duplicate targets: 0 · auto-approved changes: 0 · all five packages `pending`

**Block E — plain-language footnote**

> Work package = one target file generated from one explicit disposition. APD = Advanced Product Designer; a 37-character type name exceeds the 24-character import limit and needs a codegen `nameOverride`.

**5. Suggested visual and screenshot target path**

| Item | Detail |
|---|---|
| Primary visual | Left: Scout handoff strip. Right: five-row package table with the WP-05 gate highlighted. |
| Screenshot target | `docs/presentation/assets/agents/migrator-handoff-1440x900.png` |
| Optional focus crop | `docs/presentation/assets/agents/migrator-packages-focus.png` |
| Source URL | `http://127.0.0.1:8000/migrator?run=R-DEMO-001`, Architect stage |
| Capture status | Scout panel exists: `docs/presentation/assets/agents/migrator-scout-1440x900.png`. Package table still needs capture or HTML reconstruction. |

**6. Speaker notes (4 sentences)**

> Scout’s handoff is deliberately evidence-heavy; the point is that Architect never starts from a prose summary. The five files are schema, mapping, updater, codegen config, and API contract; the mapping file contains all 12 dispositions, while WP-05 carries the APD naming gate. All five are local drafts and none is compiled or deployed. Say plainly: synthetic fixtures, bounded checks, human gates open, not an official Cloud Assurance result.

**7. Placement**
New slide 14. Follows new slide 13; replaces none.

---

## Slide 15 — Demo · Migrator — (c) Guardian’s 11 gates

**1. Slide number and section**
New slide **15**, section **Demo · Migrator**. Follows new slide 14. Replaces none.

**2. Headline**
> **Guardian turns 24 findings and 3 assumptions into 11 human gates.**

**3. Lede (4 sentences)**
> Guardian does not score the draft; it opens a gate for every open assumption and every rule group that still has an unanswered finding. The 24 findings collapse into 8 rule groups of 3, plus 3 assumption gates, for 11 human decisions. Six of the 11 are high impact. The bundle cannot ship while any gate is open.

**4. Exact content blocks**

**Block A — arithmetic strip**

> 24 findings → 8 rule groups × 3 = 24 · 3 assumptions = **11 gates** · **6 high** · **0 resolved**

**Block B — assumption gates (3)**

| Gate | Impact | Open question | Owner |
|---|---|---|---|
| **G-01** | high | Which rating table or service consumes `Territory_Ext`, and is it in scope for this Retrofit? | `unassigned` |
| **G-02** | medium | Can the team provide a supported rating input export before scope is agreed? | `unassigned` |
| **G-03** | high | Who owns the 37-character `PersonalAutoRatingFactorConfiguration` APD change, and can the `nameOverride` be validated on the target release? | `unassigned` |

**Block C — rule groups (8)**

| Rule group | Findings | Impact | Gate |
|---|---:|---|---|
| `PF-GW-EXC-001` | 3 | medium | G-04 |
| `PF-GW-GUNIT-001` | 3 | medium | G-05 |
| `PF-GW-NAM-001` | 3 | high | G-06 |
| `PF-GW-PKG-001` | 3 | high | G-07 |
| `PF-GW-SEC-001` | 3 | high | G-08 |
| `PF-GW-SQL-001` | 3 | high | G-09 |
| `PF-GW-SRV-001` | 3 | medium | G-10 |
| `PF-GW-TX-001` | 3 | medium | G-11 |

**Block D — independence callout**

> Guardian receives the 5 packages, open assumptions and findings, and the rule pack. It deliberately does **not** receive Scout’s narrative, Critic’s verdict, or any model-generated text.

**Block E — plain-language footnote**

> A gate is a named human decision with an owner; “open” is a status, not a scoring failure.

**5. Suggested visual and screenshot target path**

| Item | Detail |
|---|---|
| Primary visual | 3 assumption cards above an 8-row rule-group table, with a 6-high / 5-medium severity split. |
| Screenshot target | `docs/presentation/assets/agents/migrator-guardian-gates-1440x900.png` |
| Optional focus crop | `docs/presentation/assets/agents/migrator-guardian-rules-focus.png` |
| Source URL | `http://127.0.0.1:8000/migrator?run=R-DEMO-001`, Guardian stage |
| Existing raw capture | `docs/audits/screenshots/ux-round1/migrator-1440x900.png` (full-page; recapture or crop) |

**6. Speaker notes (5 sentences)**

> The arithmetic is the story: 24 findings collapse to eight rule groups of three, and three assumptions stand alone. Six gates are high impact: two assumptions and four rule groups. Guardian’s independence is deliberate; it never sees the narrative or the Critic’s verdict. The gates are not failures, but they are not resolved either; assumption owners are unassigned and the rule groups sit with the delivery team. Say plainly: synthetic fixtures, bounded checks, human gates open, not an official Cloud Assurance result.

**7. Placement**
New slide 15. Follows new slide 14; replaces none.

---

## Slide 16 — Demo · Migrator — (d) Critic 7/7 and Scribe seal

**1. Slide number and section**
New slide **16**, section **Demo · Migrator**. Follows new slide 15. Replaces none.

**2. Headline**
> **Critic passes 7/7. Scribe seals 8 listed files. Neither approves.**

**3. Lede (4 sentences)**
> Critic re-checks the handoff independently: packages exist, paths are safe and unique, generated JSON/YAML parses, every package is evidence-linked, and nothing was auto-approved. Scribe writes the plan, report, manifest, and 12-event log; the manifest hashes the bundle and the log records the handoffs. Sealed means tamper-evident, not approved. The status remains `completed_with_gates`, with all five changes pending.

**4. Exact content blocks**

**Block A — Critic checks**

| # | Check | Result |
|---:|---|---|
| 1 | packages exist | 5 work packages |
| 2 | all package files generated | 5/5 |
| 3 | no `_gen` targets | bundle is `_ext` / codegen / updater only |
| 4 | no duplicate targets | 5 unique |
| 5 | generated JSON/YAML parses | 5 files parsed |
| 6 | every package is evidence-linked | 5/5 linked |
| 7 | human approval retained | 0 auto-approved changes |

**Block B — Scribe seal cards**

| Seal | Hash (display) | Artifact |
|---|---|---|
| **Plan** | `3c307f75205c` | `migration-plan.json` |
| **Report** | `8770963bd2fd` | `MIGRATION-REPORT.md` |
| **Bundle** | `6c5b7f5a5aec` | 8 listed files |
| **Agent log** | `5c28ba80c3f75eb6` | 12 events, verified |

**Block C — precision footnote**

> 8 listed bundle files = 5 target drafts + plan + report + 12-event log. `bundle-manifest.json` is the seal wrapper. Sealed ≠ approved.

**Block D — separate chains**

> Review packet audit: **9 seed events** (**11** after the two runbook decisions). Migrator log: **12 events**, separate hash chain.

**Block E — status strip**

> `R-DEMO-001` · `completed_with_gates` · 11 gates open · 0 auto-approved · verification passed (7/7)

**5. Suggested visual and screenshot target path**

| Item | Detail |
|---|---|
| Primary visual | Split panel: seven checks on the left, four seal cards on the right. Hash values in mono; status pills for PASS and verified. |
| Screenshot target | `docs/presentation/assets/agents/migrator-critic-scribe-1440x900.png` |
| Optional focus crop | `docs/presentation/assets/agents/migrator-seal-focus.png` |
| Source URL | `http://127.0.0.1:8000/migrator?run=R-DEMO-001`, Critic then Scribe stage |
| Existing raw capture | `docs/audits/screenshots/ux-round1/migrator-1440x900.png` (full-page; recapture or crop) |

**6. Speaker notes (5 sentences)**

> Critic’s 7/7 is not a quality score; it is a package-integrity check. It proves the files exist, parse, are unique, are evidence-linked, and are still pending. Scribe’s seal is tamper-evident, not an approval; the 8 listed files exclude the manifest itself, which is the wrapper. Keep the two audit chains separate: the review packet has 9 seed events (11 after the runbook decisions); the migrator log has 12. Say plainly: synthetic fixtures, bounded checks, human gates open, not an official Cloud Assurance result.

**7. Placement**
New slide 16. Follows new slide 15; replaces none. This completes the feature-migrator block.

---

## Slide 17 — Demo · Codebase lab — (e) Two insurer migration stories

**1. Slide number and section**
New slide **17**, section **Demo · Codebase lab**. Follows new slide 16. Replaces none.

**2. Headline**
> **Two synthetic insurers, two migration shapes, one bounded crew.**

**3. Lede (4 sentences)**
> Cascade Mutual is a monoline Personal Auto mutual; Harbor P&C is a multi-line carrier spanning Personal Auto, Homeowners, and Workers’ Comp. Both run the same five-agent codebase loop — Scout, Architect, Guardian, Critic, Planner — against synthetic Qusar 2026.08 snapshots with a simulated GWCP 2027.04 target (not a published release). The numbers differ because the estates differ, not because the method changes. Both end `green_with_human_gates`, with every patch pending.

**4. Exact content blocks**

**Block A — shared baseline strip**

> Qusar 2026.08 pre-cloud snapshot → simulated GWCP 2027.04 (Guidewire Cloud Platform) target · same 16-family rule pack · SARIF 2.1.0 · every patch `pending` · no deployment

**Block B — Cascade Mutual card**

> **Cascade Mutual** · Monoline Personal Auto
>
> *Illustrative synthetic footprint:* 420,000 policies · 38 PCF screens · 64 custom Gosu files · 7 integrations
>
> Narrow surface: telematics rating, dealer feed, commission publication.
>
> **18 findings** (10 error / 8 warning) · **22 patches** · **2 iterations** · **10 human gates**
>
> `green_with_human_gates` · human gates open

**Block C — Harbor P&C card**

> **Harbor P&C** · Personal Auto / Homeowners / Workers’ Comp
>
> *Illustrative synthetic footprint:* 2.6M policies · 214 PCF screens · 1,180 custom Gosu files · 42 integrations
>
> Cross-application: coastal eligibility, claims gateway, vendor MQ, billing batch.
>
> **20 findings** (11 error / 9 warning) · **21 patches** · **2 iterations** · **11 human gates**
>
> `green_with_human_gates` · human gates open

**Block D — evidence strip**

> 16 rule families in the pack · 13 rules fired on Cascade, 15 on Harbor · 18 vs 20 SARIF results · both cases 2 passes

**Block E — boundary callout**

> Synthetic profiles, not customer references. Footprint figures are illustrative synthetic values, not measured customer data. No customer data, no tenant connection, no Guidewire affiliation. A code-level green is bounded; human gates remain open.

**5. Suggested visual and screenshot target path**

| Item | Detail |
|---|---|
| Primary visual | Two case cards side by side; outcome strip across the bottom with findings / patches / iterations / gates. |
| Screenshot target | `docs/presentation/assets/agents/case-studies-1440x900.png` |
| Optional focus crop | `docs/presentation/assets/agents/case-studies-outcomes-focus.png` |
| Source URL | `http://127.0.0.1:8000/case-studies` |
| Existing raw capture | `docs/audits/screenshots/ux-round1/case-studies-1440x900.png` (full-page; recapture or crop) |

**6. Speaker notes (5 sentences)**

> Both insurers are invented; the point is the contrast in migration shape, not a benchmark. Cascade is a monoline auto mutual with a small integration surface and a rating path where direct SQL is both a cloud blocker and a latency risk. Harbor is multi-line, with claims, billing, and coastal underwriting crossing application boundaries; that is why it has more findings and gates despite fewer patches. The internal structural score reads 100/100 for both, but the human-gate-adjusted scores are 74 and 71; that gap is the point. Say plainly: synthetic fixtures, bounded checks, human gates open, not an official Cloud Assurance result.

**7. Placement**
New slide 17. Follows new slide 16; replaces none. Section changes from Demo · Migrator to Demo · Codebase lab.

---

## Slide 18 — Demo · Codebase lab — (f) Code-level refactor and SARIF

**1. Slide number and section**
New slide **18**, section **Demo · Codebase lab**. Follows new slide 17. Replaces none.

**2. Headline**
> **The code lab closes the loop — and still leaves 10/11 human gates.**

**3. Lede (4 sentences)**
> The codebase lab starts from raw Gosu, Java, XML, and GUnit rather than a completed review. Architect drafts patches, Guardian re-scans the target, Critic applies every displayed diff, and Planner compiles only after both gates agree. Cascade and Harbor each need two passes and still exit with human gates open. The output is a review bundle and SARIF, not a deployed change.

**4. Exact content blocks**

**Block A — run strip**

> 16 code rule families · 2 cases · 2 iterations each · **Cascade 18 findings / 22 patches / 10 gates** · **Harbor 20 findings / 21 patches / 11 gates** · 13 / 15 SARIF rules fired

**Block B — loop strip**

> Iteration 1: error-first → Guardian / Critic rework · Iteration 2: full pass → green · both cases 2 passes

**Block C — before → draft → remaining gate**

| Blocker family | Example patch | Draft target | Gate still open |
|---|---|---|---|
| Direct + dynamic SQL | Cascade CP-010 · Harbor CP-007 | Gosu Query / application API + generated service | semantic equivalence |
| Legacy JMS/MQ | Cascade CP-001 · Harbor CP-005 | App Events publication + Gateway route | event contract and ordering |
| Servlet | Cascade CP-005 · Harbor CP-004 | Cloud API endpoint + JAX-RS resource | route auth and consumer cut-over |
| Hard-coded secret | Cascade CP-011 · Harbor CP-008 | secret binding + redacted diff | credential rotation |
| APD long type | Cascade CP-015 · Harbor CP-013 | `nameOverride` mapping | endpoint regeneration |

Examples, not exhaustive; each family covers more patches in the bundle.

**Block D — SARIF card**

> **SARIF 2.1.0** (static-analysis report format) · tool driver `PreFlight CodeGuard`
>
> Cascade: 18 results / 13 rules · Harbor: 20 results / 15 rules
>
> Per result: `ruleId` · `level` · artifact URI · start line/column · `partialFingerprints.primaryLocationLineHash` · claim strength · remediation · redacted flag
>
> Run properties: `official_cloud_assurance: false` · `synthetic: true`
>
> No source excerpts or secret values; works with `upload-sarif`.

**Block E — boundary callout**

> A structural scanner, not a compiler or data-flow engine. Drafts are not compiled; every patch remains `pending`.

**Block F — plain-language footnote**

> Gosu is Guidewire’s JVM language; Cloud Data Access is Guidewire’s export/streaming service to S3, not a synchronous in-app read path. Synchronous reads use Gosu Query or an application API. A patch is a reviewable diff, not a deployment.

**5. Suggested visual and screenshot target path**

| Item | Detail |
|---|---|
| Primary visual | Left: source excerpt from `VehicleRatingQuery.gs` showing `DriverManager` and concatenated SQL. Right: “draft shape” box (`Query` / application API + semantic-equivalence gate) beside a SARIF JSON inset. Do not present the draft as compiled code. |
| Screenshot target | `docs/presentation/assets/agents/codebase-refactor-sarif-1440x900.png` |
| Optional focus crop | `docs/presentation/assets/agents/codebase-sarif-focus.png` |
| Source URL | `http://127.0.0.1:8000/codebase?case=cascade-mutual`; SARIF at `/api/codebase/cases/cascade-mutual/sarif` |
| Existing raw capture | None in the deck assets. Raw full-page case screenshot: `docs/audits/screenshots/ux-round1/codebase-1440x900.png`. |

**Source excerpt to use (exact):**

```gosu
uses java.sql.Connection
uses java.sql.DriverManager

var conn = DriverManager.getConnection("jdbc:cascade:rating")
var stmt = conn.createStatement()
stmt.executeQuery("SELECT factor FROM cascade_rating WHERE vin = '" + vin + "'")
```

**6. Speaker notes (5 sentences)**

> The lab is a structural pre-check, not a compiler; that is why the slide says “draft” and keeps semantic equivalence visible. The same 16-family pack fires differently: 13 rules on Cascade, 15 on Harbor, producing 18 and 20 SARIF results. Each result carries a line hash and a claim-strength label, and the SARIF run marks Cloud Assurance as not run and the fixture as synthetic. The refactor examples show intent, not compiled equivalence; a human owner still has to validate semantics. Say plainly: synthetic fixtures, bounded checks, human gates open, not an official Cloud Assurance result.

**7. Placement**
New slide 18. Follows new slide 17; replaces none.

---

## Slide 19 — Demo · Codebase lab — (g) Upgrade resilience

**1. Slide number and section**
New slide **19**, section **Demo · Codebase lab**. Follows new slide 18. Replaces none.

**2. Headline**
> **A green signal is release-bound, not permanent.**

**3. Lede (4 sentences)**
> A migration assessment can outlive the release it was written against. PreFlight simulates five GWCP release changes and invalidates the prior green signal rather than silently reusing it. It identifies affected patches, runs scenario checks, and records one of three resume choices: revalidate, rollback, or defer. The APD scenario reruns at its simulated 20-character limit; the other four remain `revalidation_required` until their drafts are fixed.

**4. Exact content blocks**

**Block A — five simulated GWCP release changes**

| Release change | Effective change | Affected rules | Cascade patches matched | Harbor patches matched |
|---|---|---|---:|---:|
| **APD naming** (simulated) | 24 → 20 characters | `PF-CODE-APD-001` | 2 | 2 |
| **App Events v2** | envelope adds `tenantId` / `eventId` | `PF-CODE-MSG-001` | 3 | 3 |
| **Gateway mTLS** | mTLS (mutual TLS) + scoped service identity | `PF-CODE-SRV-001`, `PF-CODE-MSG-001` | 7 | 6 |
| **Removed Gosu API** | deprecated runtime API family removed | `PF-CODE-API-001`, `PF-CODE-API-002` | 14 | 14 |
| **Cloud API version** | v1 → v2 route prefix | `PF-CODE-SRV-001` | 4 | 3 |

Scenario IDs: `GWCP-APD-NAMING-2027.04` · `GWCP-APP-EVENTS-V2-2027.04` · `GWCP-GATEWAY-MTLS-2027.04` · `GWCP-GOSU-API-REMOVAL-2027.04` · `GWCP-CLOUD-API-VERSION-2027.04`. All five simulate GWCP 2026.10 → 2027.04.

**Block B — APD control callout**

> Same bundle, two outcomes: regenerated at the scenario's 20-character limit → `compatible`; the 24-character bundle → `revalidation_required`.

**Block C — resume options: revalidate / rollback / defer**

| Option | What it does | Status recorded |
|---|---|---|
| **Revalidate** (recommended) | Re-run Architect with the new rule pack | `resume_requested` |
| **Rollback** | Return to the last green checkpoint; keep the sealed bundle | `rolled_back_to_checkpoint` |
| **Defer** | Pin the assessment release; record the risk owner | `upgrade_deferred` |

All three clear the green signal and keep human approval required.

**Block D — unexpected-scenario playbook**

> Named states, not an unchecked green signal: **source changed** · **corrupt file** · **duplicate target** · **analyzer crash** · **empty snapshot**.

**Block E — boundary strip**

> Conservative match by affected rule or path. Counts are exposure, not effort. A human still approves every patch.

**5. Suggested visual and screenshot target path**

| Item | Detail |
|---|---|
| Primary visual | Scenario table with the APD row highlighted; three resume cards beneath; five playbook chips across the bottom. |
| Screenshot target | `docs/presentation/assets/agents/codebase-upgrade-1440x900.png` |
| Optional focus crop | `docs/presentation/assets/agents/codebase-upgrade-focus.png` |
| Source URL | `http://127.0.0.1:8000/codebase?case=cascade-mutual&upgrade=GWCP-APD-NAMING-2027.04` (select the Upgrade resilience tab before capture) |
| Existing raw capture | None. Capture new from the current UI. |

**6. Speaker notes (5 sentences)**

> The 24-character limit is documented; the 20-character 2027.04 scenario is a simulation. It moves from 24 to 20 characters in this model and invalidates any bundle built against the older limit. The table shows how many patches each scenario touches, but those are conservative matches, not defect counts or effort estimates; the removed-API row scans `gsrc/`, `java/`, and `plugins/` broadly. The three resume choices all clear the green signal and keep a human in the loop; the tool records the choice, it does not approve it. Source changes, corrupt files, duplicate targets, analyzer crashes, and empty snapshots become named states instead of an unchecked green signal. Say plainly: synthetic fixtures, bounded checks, human gates open, not an official Cloud Assurance result.

**7. Placement**
New slide 19. Follows new slide 18; replaces none. Current slide 13 (Engineering rigor) becomes 20 and follows this slide.

---

## Final count

| Item | Count |
|---|---:|
| Existing slides | 16 |
| New slides | **7** |
| Total after insertion | **23** |
| New slide range | 13–19 |
| Shifted existing slides | 13–16 → 20–23 |
| Optional live MiMo callout | 1, inside slide 13; no separate slide |

---

## Gaps and open items

1. **Not integrated.** This file is a draft only. `index.html`, `evidence.json`, `README.md`, `PreFlight-deck.pdf`, and app code were not edited.
2. **Deck metadata is still “16”.** The HTML hard-codes `aria-label="Slide X of 16"`, the help text says `#slide-1 … #slide-16`, and `README.md` describes 16 slides and 16 PDF pages. All must change to 23 after insertion.
3. **`evidence.json` has 16 slide entries.** The seven new slides, their asset hashes, the 23-page PDF fact, and the new validation run need to be added. `asset_count` and `validation` fields will change.
4. **The new screenshot set is incomplete.** Two 1440 × 900 captures exist under `docs/presentation/assets/agents/` (`migrator-loop`, `migrator-scout`); the capture manifest reports `ok: false` because the Architect artifact selector was not found. Slide 13 is captured; slide 14 has the Scout panel but still needs the package table; slides 15–19 need captures, plus 1280 × 720 / 1024 × 768 / 390 × 844 variants for dense slides. Older full-page audit captures under `docs/audits/screenshots/ux-round1/` are reference only.
5. **The main capture script does not cover the new routes.** `scripts/capture_demo.py` has no `/migrator` or `/codebase` deck capture path. A separate agent capture run has started under `assets/agents/` but is incomplete; extend that path or capture the new slides manually, then validate overflow and console errors.
6. **The feature path is not the cyclic loop.** The UI calls it a “five-agent loop,” but `R-DEMO-001` is a straight Scout → Architect → Guardian → Critic → Scribe handoff chain. The cyclic Architect ↔ Guardian/Critic rework belongs to the codebase lab. Keep this distinction in the slide copy.
7. **“8 bundle files” excludes the manifest.** The manifest lists 5 target drafts + plan + report + 12-event log. `bundle-manifest.json` is the ninth file in the directory and the seal wrapper. Keep “8 listed files” wording.
8. **Do not mix the two migrator runs.** `R-DEMO-001` is the canonical 12-event offline run. The live MiMo run `R-20261111-052740-b001` has a 24-event log. Use the live run only for the optional MiMo callout, not for bundle/log counts.
9. **The code-level drafts are not compiled.** The refactor patches are structural drafts; semantic equivalence, compilation, and tenant validation remain human gates. The slide copy must not imply otherwise.
10. **Upgrade exposure counts are conservative.** They are matched by affected rule or path, not by proving each patch is broken. The removed-Gosu-API row is especially broad (14 patches in both cases). Label them as exposure, not effort or defect count.
11. **Status labels need consistent treatment.** `completed_with_gates` and `green_with_human_gates` mean bounded checks finished with open human gates; neither means approval or deployment.
12. **Tone check remains manual.** The tone guardrails above still apply. Re-run the deck’s claims lint after integration, and keep the “not an official Cloud Assurance result” caveat in slide notes and the code-lab footer.
