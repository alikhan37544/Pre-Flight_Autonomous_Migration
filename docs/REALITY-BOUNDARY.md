# The Reality Boundary: Is the Demo an Actual Migration?

**Status:** Decision memo / evidence review  
**Date:** 2026-11-11  
**Scope:** PreFlight v2, synthetic Guidewire-style cloud-readiness review and refactor-drafting prototype  
**Audience:** demo presenters, judges, prospective design partners, engineering, and anyone preparing a claim about the demo  
**Verdict:** **No. The demo is not an actual migration.** It is a real, working review prototype exercised on a synthetic estate. It does not contact a tenant, compile Gosu (Guidewire's JVM language) or Java against Guidewire, generate real Cloud API endpoints, deploy, or run official Cloud Assurance.

---

## 0. The one-paragraph answer

The demo is **real software on synthetic inputs**. The scanner, rule pack, evidence links, unified diffs, Static Analysis Results Interchange Format (SARIF) 2.1.0 exporter, hash-chained audit log, and two migration archetypes are genuinely implemented and executable. But the estate, insurer names, code, Advanced Product Designer (APD) release scenarios, and evaluation slice are synthetic; and the things that would make a migration real — compilation in a Guidewire environment, runtime behavior, tenant compatibility, official Cloud Assurance, data migration, production cutover, rollback, and customer outcomes — have not happened. PreFlight is a **pre-migration review and drafting tool**, not a migration. The correct claim is narrow: *on a synthetic Guidewire-style estate, PreFlight found evidence-linked candidate blockers and produced reviewable draft refactors. Nothing was compiled, deployed, or officially assured.*

### At a glance

| Question | Honest answer |
|---|---|
| Is the demo an actual migration? | **No.** It is a synthetic rehearsal of the assessment and drafting layer. |
| Is the software real? | **Yes.** The scanner, diffs, SARIF, hash chain, and review workflows execute and are tested. |
| Is the estate real? | **No.** Fixtures, insurer names, code, numbers, APD scenarios, and evaluation slice are synthetic. |
| Is the use case real? | **The problem is real and publicly documented; the demo's instance is not validated with a real insurer.** |
| Does it compile Gosu/Java against Guidewire? | **No.** No compiler, SDK, runtime, or codegen build is invoked. |
| Does it run in a tenant? | **No.** No tenant, data model, permissions, integrations, or production data are contacted. |
| Is it official Cloud Assurance? | **No.** No TeamCity build, Studio inspection, Cloud Assurance Plugin, threshold, or official report. |
| Can it deploy or migrate data? | **No.** No deployment, data migration, cutover, or rollback. |
| What is the strongest true claim? | **On a synthetic Guidewire-style estate, PreFlight produced evidence-linked candidate findings and reviewable draft refactors; nothing was compiled, deployed, or officially assured.** |

---

## 1. What a real migration means

Guidewire's own public migration guide describes a nine-stage program: Cloud Upgrade Estimate (CUE), Pre-Project, Technical Upgrade, Delivery Inception, Delivery Development, Delivery Stabilization, Deployment Preparation, Post-Deployment Support, and Cloud Updates [S9]. A real migration is not a scan or a diff; it is the whole chain from a formal estimate through a production cutover and post-go-live support.

| Guidewire stage | What the public guide says happens | PreFlight today |
|---|---|---|
| 1. Cloud Upgrade Estimate (CUE) | A formal assessment of effort from a self-managed environment to Guidewire Cloud, based on pre-work reviews and internal tooling [S9] | **Not a CUE.** PreFlight is a pre-estimate evidence pack that could feed CUE preparation; it has no formal estimate, no Guidewire tooling, and no customer inputs. |
| 2. Pre-Project | Kick-off, environment setup, optimization backlog, integration inventory, Cloud Data Access (CDA) review [S9] | Synthetic inventory and drafting only. No real backlog, integration inventory, or CDA review. |
| 3. Technical Upgrade | Merge the self-managed codebase into the latest Guidewire Cloud version, resolve errors, launch core services [S9] | **Not performed.** No code merge, no Guidewire build, no core services. |
| 4. Delivery: Inception | Review technical-upgrade output, create the formal development backlog, finalize release plan [S9] | Synthetic findings can look like a backlog, but no real release plan or owner commitments exist. |
| 5. Delivery: Development | Address cloud-suitability issues, refactor technical debt, develop and run automated tests [S9] | **Drafts only.** Unified diffs and candidate files; no compilation, no tests against a Guidewire runtime, no deployment. |
| 6. Delivery: Stabilization | End-to-end testing, performance validation, dress rehearsals for database upgrade readiness [S9] | **Not performed.** No E2E, performance, or data-rehearsal evidence. |
| 7. Deployment Preparation | Final dry runs, code confirmed stable, environment prepared for production [S9] | **Not performed.** |
| 8. Post-Deployment Support | Dedicated support for 4–6 weeks to resolve post-go-live issues [S9] | **Not performed.** |
| 9. Cloud Updates | Test new Guidewire Cloud releases during and after migration and stay aligned [S9] | **Not performed.** PreFlight models simulated release scenarios, not live release monitoring. |

**Where PreFlight actually sits:** it is a **pre-CUE / pre-project assessment and draft-remediation aid**. It can help a team inventory a codebase, surface candidate blockers, assemble evidence, and prepare questions before a formal CUE, Cloud Retrofit, or Cloud Assurance effort. It is not a migration program and cannot substitute for one.

The distinction matters because Guidewire's own docs separate the **formal assessment** (CUE), the **code inspection gate** (Automated Cloud Assurance), the **product-model conversion** (Advanced Product Designer (APD) conversion / Cloud Retrofit), the **data path** (Cloud Data Access and database migration), and the **deployment path** (development, pre-production, and production planets) [S1][S9][S10]. PreFlight touches a small, early part of that chain.

### 1.1 Is the use case real?

**The problem is real.** Guidewire's public docs describe Cloud Standards compliance, Automated Cloud Assurance, CUE, APD/Cloud Retrofit, Cloud Data Access, migration-stage planning, production deployment, and post-go-live support [S1][S4][S9][S10][S13]. Insurers with self-managed InsuranceSuite estates do need to inventory customizations, find cloud blockers, estimate remediation, and prove the result. A pre-migration evidence pack is a coherent product idea in that context.

**The demo's instance of the use case is not yet real.** The repository contains no real insurer snapshot and no pilot record; there is no evidence that an owner has used the output in a real decision, and no measured time or estimate impact exists. The two synthetic archetypes show that the method can be exercised on different migration shapes; they do not show that the method works for a real insurer.

**What would prove the use case:** a signed pilot with a real read-only snapshot, a blind subject-matter expert (SME) validation sample, a decision log showing which findings changed a backlog item or assumption, and a measured reviewer-time or estimate-variance baseline. That is **Stage 2** below. It proves the assessment use case; it still does not prove the migration.

---

## 2. What the demo actually is — reproduced evidence

This review re-ran the codebase lab and the verification commands on 2026-11-11 from the repository. These are real outputs of the prototype, not screenshots.

| Check | Command / artifact | Result | What it proves |
|---|---|---|---|
| Cascade lab run | `python -m app.cli codebase cascade-mutual --out /tmp/...` | Exit 0; 18 findings; 22 patches; `green_with_human_gates` | The five-agent loop and refactor generator execute end-to-end on the synthetic Cascade fixture. |
| Harbor lab run | `python -m app.cli codebase harbor-pc --out /tmp/...` | Exit 0; 20 findings; 21 patches; `green_with_human_gates` | The multi-line synthetic fixture exercises a different blocker mix. |
| Codebase tests | `pytest tests/test_codebase.py -q` | 28 passed | The codebase contracts, SARIF, refactor, and boundary tests pass for this build. |
| SARIF | Cascade `results.sarif` | `version: 2.1.0`; 18 results; 13 rules; `official_cloud_assurance: false`; `synthetic: true` | The exporter emits a real SARIF 2.1.0 document, explicitly marked advisory and synthetic. |
| Review audit | `python -m app.cli verify-audit R-DEMO-001` | `OK (9 events, head d3da24fac51f7c6a)` | The local review log's hash chain verifies. |
| Packet | `python -m app.cli verify-packet R-DEMO-001` | `OK - packet hash, content digests, and audit chain verified` | The packet's own hashes and content bindings verify. |
| Generated JMS patch | `/tmp/opencode/pf-cascade/patches/CP-001.diff` | Replaces the legacy JMS (Java Message Service) transport with `<preflightMigrationPlaceholder>` | The patch is a reviewable draft marker, **not** a deployable configuration. |
| Generated Harbor codegen draft | `/tmp/opencode/pf-harbor/target/config/codegen/...yaml` | Type-level `nameOverride` for the long APD type | The draft illustrates the documented type-name mechanism; it is not a full APD-conversion or field-mapping artifact. |

Representative repository evidence:

| Claim | Repository evidence | What it proves | What it does **not** prove |
|---|---|---|---|
| Fixtures are synthetic | `scripts/generate_fixture.py` begins “Everything here is synthetic”; `fixtures/demo-slice-300/README.md`; `fixtures/case-studies/*/README.md` | The demo estate is generated/invented and declares no customer data. | Nothing about a real insurer's estate. |
| The scanner is not a compiler | `app/services/codeanalyzer.py` docstring: “deliberately a *scanner*, not a compiler” | The analysis is structural and evidence-linked. | Compilation, type checking, AST correctness, or data-flow behavior. |
| Source code is not compiled | `app/services/code_migration.py:313` — “source code is not compiled” | Target drafts are syntax-parsed (XML/JSON/YAML), not compiled as Gosu/Java. | Buildability or runtime correctness. |
| Nothing is deployed | `app/services/code_migration.py` — “Nothing is compiled or deployed” and “nothing was deployed, and every patch is pending” | The lab stops before deployment. | Tenant compatibility, cutover, or production behavior. |
| Unified diffs are real | `app/services/refactor.py:573-581` uses `difflib.unified_diff`; `:769-787` records source/target SHA-256 and `approval: "pending"` | The diff and patch contract is genuine. | That the patch is correct, compilable, or approved. |
| SARIF is real | `app/services/sarif.py:18` sets `SARIF_SCHEMA` to the 2.1.0 schema; `:110-145` emits `official_cloud_assurance: False` and `synthetic: True` | The output is a valid-format advisory SARIF document. | An official Cloud Assurance result or a compliance pass. |
| The audit chain is real | `app/services/code_migration.py:163-240` implements SHA-256 canonical JSON, `prev_hash`, and verification | The log is tamper-evident against local edits/reorders/truncation when the checkpoint is intact. | Non-repudiation, external timestamping, or truth of the content. |
| Patches stay pending | `app/services/refactor.py:787`, `:807`, `:833` set `approval: "pending"` | No self-approval. | Human review or business acceptance. |
| The demo is explicitly bounded | `README.md:103-113`, `:338-363`; `docs/CODEBASE-MIGRATION.md:304-313`; `docs/EVALUATION-SCOPE.md:37-52` | The project already states the limitations in its own words. | That the limitations are unimportant. |

**Key point:** these artifacts are real, but they are real **about a synthetic input**. The generated JMS patch is a particularly useful honesty test: it replaces a legacy transport with a placeholder, not with a working App Events or Gateway configuration. That is appropriate for a draft, and it should be shown as a draft.

---

## 3. The three-way split

### 3.1 What is genuinely real

#### Cloud-breaking patterns

The patterns are real migration concerns, not invented theater. Guidewire's public hardening guidance identifies direct SQL/database modification, custom servlets, hidden/internal packages, hard-coded secrets, and custom encryption as cloud concerns [S3][S13][S14]. Guidewire's APD documentation identifies type-name truncation as a real cause of endpoint compile errors [S4]. The App Events and Integration Gateway docs describe the supported direction for legacy messaging integrations [S7][S8].

But “the pattern is real” is not the same as “this finding is a confirmed violation.” A regex match on a synthetic file is a **candidate**. Real code can use JDBC in a test harness, a servlet in an approved edge case, or an internal package with a documented exception. The rule pack is not the Cloud Standards corpus.

#### Public rule references

The claim-strength system is real and unusually disciplined:

- `verified-id` — a public Guidewire page lists the standard ID and exact title; the body may be gated.
- `verified-policy` — an exact public policy statement supports the pattern; no standard ID is bound.
- `verified-doc` — an exact public product-documentation behavior is reproduced.
- `secondary` — a public secondary source describes the pattern.
- `heuristic` — PreFlight's own detector; no vendor rule claimed.

Only two `IS-*` IDs are bound anywhere in the packs: `IS-TLS-1238` (Use of Direct SQL Calls to Access a Database) and `IS-TLS-1191` (Hidden Package Reference) [S14]. `SEC00-G` and `ERR00-G` are Gosu secure-coding IDs, not Cloud Standards [S3][S14]. The APD rule is `verified-doc` [S4]; the servlet and removed-runtime-API rules are `verified-policy` [S14]; the remaining rules are `secondary` or `heuristic`.

This is real, inspectable labeling. The codebase pack has 16 rules across 11 categories; the review pack has 11 rules, of which 8 produce the demo's gate groups. That coverage is real but bounded: it is not the Cloud Standards corpus. A public title is not the full rule text, and a link is not an endorsement.

#### Deterministic static analysis

The scanner is real Python code. It masks comments and string literals before structural matching, keeps separate value-preserving views for secret/weak-crypto checks, redacts secret excerpts to a fingerprint, never writes to the source snapshot, and emits a path, line, excerpt hash, and stable fingerprint for each finding. On a fixed input and fixed rule pack, it is deterministic.

It is **not** a compiler, AST, type checker, data-flow engine, or semantic analyzer. It does not resolve inheritance, generics, framework dispatch, generated code, or runtime configuration. False-positive and false-negative rates on a real estate are unmeasured. “Deterministic” means “same input, same output,” not “correct output.”

#### Unified diffs

The diffs are real `difflib.unified_diff` output with `a/...` and `b/...` paths, source/target SHA-256, a patch ID, rule/finding IDs, risk level, semantic-review flag, and `approval: "pending"`. The Critic applies the displayed diff to the original and compares it with the target draft; a patch that does not reproduce its target fails the gate.

This is a genuine review artifact. It is not a merge request, a compiled change, or an approval. Some patches are placeholders or structural rewrites; the JMS patch is the clearest example.

#### SARIF 2.1.0

The SARIF output is a real 2.1.0 document: `$schema`, `version`, tool driver, rule metadata, results, locations, `partialFingerprints`, and run properties. It carries `official_cloud_assurance: false` and `synthetic: true`. It is suitable for CI ingestion as **advisory** findings.

Uploading it to GitHub Code Scanning does not make it an official Cloud Assurance result. SARIF is a transport format, not a compliance verdict. The project says this correctly: “SARIF results describe source findings and their evidence; they do not assert that a patch has been compiled or approved” [README:363].

#### Hash chain

The audit log is a real SHA-256 hash chain over canonical JSON, with `prev_hash`, sequence checks, and an atomically written checkpoint that detects tail truncation. `verify-audit` and `verify-packet` both passed on 2026-11-11.

It is **tamper-evident**, not **non-repudiation**. An attacker with write access to the run store can recompute the chain; there is no external timestamp, signature, or notary. The project labels it correctly as “tamper-evident local log, not non-repudiation” [docs/security.md:33]. It proves internal consistency of a run, not that the run's claims are true or that the source estate is real.

#### Case-study archetypes

The two archetypes are real **migration shapes**:

- **Cascade Mutual** — monoline Personal Auto, narrow integration surface, Cloud Retrofit without APD App, a rating path with direct SQL, and a small set of high-risk integrations.
- **Harbor P&C** — multi-line regional carrier spanning Personal Auto, Homeowners, and Workers' Comp, with claims, billing, and coastal underwriting crossing application boundaries, Cloud Retrofit with APD conversion, and a mid-migration release-change scenario.

Those dimensions — LOB count, application spread, integration mix, regulatory constraints, product-model path, and release cadence — are genuine variables in a real migration. The profiles are deliberately constructed to exercise them. But the companies, policy counts, states, screen counts, rating-call volumes, and code are invented. Two synthetic archetypes are not a representative sample and cannot support a generalization claim.

#### The honesty machinery

The claim-strength labels, synthetic badges, `official_cloud_assurance: false` flags, claims ledger, freeze hashes, and “pending” approval states are genuinely implemented. They are the strongest evidence that the prototype is not trying to pass itself off as a migration. They should be preserved and made more prominent, not buried.

### 3.2 What is synthetic

| Item | Evidence | Why it matters |
|---|---|---|
| Fixtures | `demo-slice-300` (300 files), `acme-pc-2026.10` (650 files), `northstar-pc-2026.10` (150 files); `ground_truth/FROZEN.json`; `scripts/generate_fixture.py` | No real insurer estate. File counts and hashes are deterministic, but the content is generated. |
| Insurer names and profiles | Cascade Mutual and Harbor P&C; Acme Personal Auto; Northstar Auto; `app/services/case_studies.py:1-4`; fixture READMEs | The names, footprints, states, policy counts, and rating volumes are invented. No customer data. |
| Code | Fixture snippets such as `VehicleRatingQuery.gs` and `DealerFeedServlet.gs` | The snippets are legible pattern examples, not production Guidewire code. They are intentionally small and do not exercise framework complexity, inheritance, generated code, or real data models. |
| APD release scenarios | `app/services/resilience.py:27-42`; `docs/CODEBASE-MIGRATION.md:239-245`; `docs/RULES-RESEARCH.md:149-166` | `GWCP 2027.04`, the 24→20-character limit, and the other five scenarios are PreFlight simulations. No public 2027.04 release note or 20-character APD limit was found in the sources reviewed. |
| Evaluation slice | `docs/EVALUATION-SCOPE.md:7-18`, `:37-52`; `ground_truth/PRE_REGISTRATION.md` | The 300-file slice is in-sample; the gold files were generated by the same fixture build; the reference target is internally authored and AI-assisted; the holdout is naming-shift only, pre-computed, and not imported. The current demo reports M1–M6 at 1.0 and reference macro-F1 1.00 on this slice; these are rule-pack consistency results, not an independent benchmark. |
| Case-study numbers | `docs/CASE-STUDIES.md:13`, `:61-63`; `app/services/case_studies.py:17-38`, `:122-143` | 420,000 policies, 2.6 million policies, 38/214 PCF (page configuration file) screens, 1.8M/11.4M rating calls per day, and similar figures are invented illustrations. |
| Impact ranges | Packet/demo assumption ranges (for example, 7–9 engineer-days) | Heuristic planning ranges, not quotes, benchmarks, or customer data. |

**A note on “Qusar 2026.08.”** Qusar is a real public release label used as review context [S18]. The snapshot contents are still synthetic. Do not let a real release label make the estate look real.

### 3.3 What is not proven

| Claim | Status | Why it is not proven | Minimum evidence to close |
|---|---|---|---|
| Compilation | **Not proven** | No Gosu compiler, Java compiler, Guidewire SDK/runtime, or codegen build is invoked. `_parse_target_files` only parses XML/JSON/YAML. | A real build in a Guidewire developer environment with compiler logs and zero in-scope errors. |
| Runtime behavior | **Not proven** | No refactored Gosu/Java is executed; no GUnit (Guidewire unit test), integration, or end-to-end test is run against the refactors. | Unit/integration/E2E test results in a Guidewire environment, including failure-path tests. |
| Tenant compatibility | **Not proven** | No tenant, metadata, data model, permissions, plugins, integrations, or production data are contacted. | A real tenant or authorized sandbox with the target release and data model; deployment and smoke tests. |
| Official Cloud Assurance | **Not proven / not run** | No TeamCity Automated Cloud Assurance build, Studio inspection, Cloud Assurance Plugin, threshold, or official report. The threshold and full standards corpus are gated. | An official Cloud Assurance report for a real branch/commit/release, with violation triage and sign-off. |
| Migration execution | **Not proven** | No data migration, code deployment, integration cutover, production planet, or rollback. | Cutover runbook, deployment records, data reconciliation, rollback test, hypercare. |
| Customer outcomes | **Not proven** | No customer, no production metrics, no time/cost/defect baseline or post-migration measurement. | A real pilot with before/after outcomes and customer acceptance. |
| APD conversion / endpoint generation | **Not proven** | The lab drafts a type-level `nameOverride` and custom configuration descriptors; it does not import a product into APD, generate endpoints, or regenerate `_gen` files. | Real APD import/conversion, codegen, endpoint generation, and endpoint smoke tests. |
| Data migration / CDA | **Not proven** | No database snapshot, CDA configuration, ETL, reconciliation, or read-model test. | A data migration rehearsal with row counts, reconciliation, latency, and rollback. |
| Security / compliance | **Not proven** | No threat model review for the target, pen test, secret rotation, access review, or regulatory sign-off. | Security review, pen test, data-handling approval, and compliance sign-off for the scope. |
| Performance | **Not proven** | No latency, throughput, or load test. The 200 ms p95 dealer-feed constraint in Cascade is invented. | Performance test against the target architecture and release. |
| Generalisation | **Not proven** | One synthetic 300-file slice, a filler-heavy 650-file variant, and a naming-shift holdout that is pre-computed and not imported. No real anonymised estate, blind SME annotation, or reviewer-time study. | A real anonymised estate, independent blind annotation, and measured precision/recall with confidence intervals. |

---

## 4. Technical accuracy caveats

These are not reasons to discard the prototype. They are reasons to phrase its claims carefully, and they are concrete items to fix before a real pilot.

### 4.1 Cloud Data Access is not a synchronous replacement for JDBC

**Status: resolved in the current build.** The code glossary now says: “Guidewire's cloud data export/streaming service (S3 Parquet); synchronous in-app reads use Gosu Query or application APIs” (`app/services/code_migration.py:1485`), and `docs/CODEBASE-MIGRATION.md:70` reserves Cloud Data Access for analytics/export. The generated draft is a Gosu Query service named `VehicleRatingQueryQueryService` (`app/services/refactor.py:532-546`) and uses `Query.make(...).select()`; the old `VehicleRatingQueryCloudDataAccess` class name is gone.

Guidewire's public CDA material describes CDA as a **data streaming/export service** that lands InsuranceSuite data in Amazon S3 as Parquet files for analytics and downstream systems [S15][S16]. It is not a synchronous in-application query API. For synchronous reads inside extension code, the documented direction is a supported Gosu Query or an application/Cloud API; the data-access architecture must be decided explicitly.

This still matters for the invented Cascade 200 ms p95 constraint: a CDA/S3 export path is not designed as a synchronous 200 ms rating path. Keep the synchronous path labelled “Gosu Query / application API,” reserve “CDA” for analytics/export, and record a data-access architecture decision with latency and consistency requirements. The app-template glossaries are a separate copy surface and must use the same wording.

### 4.2 App Events is asynchronous and at-least-once

The App Events draft replaces a legacy JMS transport with an App Events publication plus an Integration Gateway route. That is a real supported direction: Guidewire describes App Events as the new outbound asynchronous integration approach, with at-least-once delivery and safe ordering [S7]. It is not a drop-in for every JMS request/reply or exactly-once pattern.

The lab's own human gate CR-05 says: “Verify event contract, ordering key, delivery guarantee, and consumer acknowledgement” (`MIGRATION-REPORT.md`, CR-05). That is the right gate. The “green” signal must not be read as proof that the event semantics are correct. A real pilot needs an event-contract test, idempotency/consumer-ack evidence, and a latency measurement against the consumer's requirements.

### 4.3 APD path: type-level `nameOverride` is not the whole APD-conversion story

The public docs say type names are limited to 24 characters and truncation can cause endpoint compile errors; the correction is a codegen `nameOverride` plus endpoint regeneration [S4]. The docs' field-level guidance says `nameOverride` should be used only for Cloud Retrofit without APD App; for APD App or APD conversion, use `schemaPropertyName` [S6]. The project interprets this as a field-level restriction and says it models the non-APD path [docs/RULES-RESEARCH.md:165,232-235].

**Status: resolved in the current build.** Cascade is explicitly “Cloud Retrofit without APD App,” so the type-level `nameOverride` draft is in scope. Harbor is now labelled “Cloud Retrofit + APD naming preparation (type-level codegen draft) · multi-LOB” (`app/services/case_studies.py:141`), and the case-study copy says the deliverable is a type-level `nameOverride`, not a full APD conversion (`:251-253`). The draft still does not model the APD App import, field-level `schemaPropertyName`, product-model synchronization, or endpoint regeneration [S4][S6][S11][S12]. Do not present Harbor as proof that PreFlight covers APD conversion. Keep the label “type-name codegen override only; APD conversion and field mapping not modeled.”

### 4.4 Servlet wording matches the public policy

**Status: resolved in the current build.** The public hardening guidance says: “The use of custom servlets is not a recommended practice. All integrations should be implemented using the approved REST API framework” [S14]. PreFlight labels the rule `verified-policy`, which is correct. The case-study summary now says “custom servlets are not a recommended practice; use the approved REST API framework” (`app/services/case_studies.py:116`). The stronger “not supported” wording is gone. Keep the public wording and the claim-strength label visible.

### 4.5 The 24-character limit is a type-name limit, not a universal name limit

The public page says “type names are limited to 24 characters” and gives the `WCRetroRatingLetterOfCredit` → `WCRetroRatingLetterOfCre` truncation example [S4]. It does not say every field or label is limited to 24 characters; other APD name limits vary by type/field. PreFlight's `PF-CODE-APD-001` scans XML product-template type names, which is the right scope. Do not generalize the 24-character rule to all names, and keep the synthetic 37-character example labeled as synthetic (`docs/claims-ledger.md` C-029).

### 4.6 “Green” and “100/100” are structural, not production readiness

The generated Cascade report (`MIGRATION-REPORT.md`) shows a structural score of 100/100 after the loop, a human-gate-adjusted score of 74/100, and ten open human gates; Harbor shows 100/100 structural and 71/100 human-gate-adjusted. The 100 is a **structural consistency score**, not cloud readiness, not Cloud Assurance, and not deployment approval. The project says the green signal is “a bounded agent verdict with open human gates; it is never deployment approval” [README:113; docs/CODEBASE-MIGRATION.md:319]. Put the human-gate score and the boundary next to any 100/100 slide.

### 4.7 The hash chain and the static snapshot are different artifacts

The local audit chain verifies, but `docs/demo/run-summary.json` is a capture-time snapshot. Its own README says it is “a historical snapshot, not a live verifiable run” [docs/demo/README.md:3]. On 2026-11-11 the live `verify-audit` head was `d3da24fac51f7c6a`; the packaged summary records a different head. Do not present the packaged snapshot's hash as live proof. Present it as a historical artifact and re-run the verification on the live run store.

### 4.8 SARIF is advisory by construction

The SARIF exporter is real, but it is not an official Cloud Assurance result. It marks `official_cloud_assurance: false` and `synthetic: true` [app/services/sarif.py:132-145]. GitHub Code Scanning can display it, but display is not approval. Keep the advisory label in the PR check name, the SARIF rule metadata, and the talk track.

---

## 5. The five-stage proof ladder

The ladder answers a different question at each stage. Do not skip stages: a later-stage artifact cannot repair a missing earlier-stage proof.

| Stage | Question it answers | Minimum evidence | Maximum claim | Still not proven |
|---|---|---|---|---|
| 1. Synthetic rehearsal (current) | “Does the method work on controlled inputs?” | Frozen synthetic fixtures, deterministic run, evidence links, diffs, SARIF, hash chain, tests | “The method is reproducible and evidence-linked on a synthetic estate.” | Everything about a real estate, compilation, runtime, tenant, official assurance, migration. |
| 2. Real read-only snapshot with evidence | “Does the method find real, relevant issues?” | Authorized real snapshot, chain-of-custody, hash manifest, parser coverage, SME-validated sample, decision log | “On this real snapshot, we found X candidate issues; Y% of a sample were confirmed; the evidence changed Z decisions.” | Compilation, runtime, tenant compatibility, official assurance, migration, outcomes. |
| 3. Compile/test in a Guidewire developer environment | “Does the code build and run in the target environment?” | Guidewire dev planet, target release, real code/config, compiler logs, codegen output, GUnit/integration tests, dev deployment, smoke tests | “In-scope drafts compile and pass defined tests in a Guidewire developer environment on release X.” | Official Cloud Assurance, production data compatibility, performance, security, cutover. |
| 4. Official Cloud Assurance + SME sign-off | “Does the official gate pass, and do the owners accept the residual risk?” | Official Automated Cloud Assurance report, threshold, violation triage, Cloud Standards mapping, named SME sign-offs, residual-risk register | “Official Cloud Assurance ran on date X for commit Y/release Z; result R; named owners signed off.” | Production cutover, customer outcomes, long-term stability. |
| 5. Production cutover with rollback | “Did the migration actually work in production?” | Deployment records, data reconciliation, cutover runbook, go/no-go, rollback test, hypercare, production smoke/performance, business acceptance, measured outcomes | “The migration was executed on date X; production verification passed; rollback was tested; outcomes were measured over period P.” | Generalization to other insurers; long-term ROI beyond the measured window; absence of future risk. |

### Stage 1 — Synthetic rehearsal (current)

**Purpose:** prove the method is repeatable, evidence-linked, and honest about its boundaries.

**Evidence required (already present):**
- Frozen synthetic fixtures with SHA-256 manifests (`ground_truth/FROZEN.json`).
- A fixed rule pack and a deterministic scanner.
- Evidence links with path, line/pointer, excerpt, excerpt hash, and claim strength.
- Unified diffs with source/target hashes and `pending` approval.
- SARIF 2.1.0 with `official_cloud_assurance: false` and `synthetic: true`.
- Hash-chained audit log and packet verification.
- A test suite covering the codebase contracts and boundaries.

**What PreFlight can claim:**
- “On a synthetic Guidewire-style estate, PreFlight produced evidence-linked candidate findings and reviewable draft refactors.”
- “The scanner is deterministic and read-only; the audit chain and packet hashes verify.”
- “The rule citations are labeled by strength; only two `IS-*` IDs are bound, and their bodies are gated.”

**What PreFlight cannot claim:**
- Any real-estate finding, compile, runtime, tenant, official assurance, migration, or customer outcome.
- That a “green” lab signal is deployment approval.
- That the 100/100 structural score is cloud readiness.

**What the demo should show:**
- A persistent “Synthetic rehearsal” badge from the first screen.
- Fixture hash and file count.
- Rule claim strength on every finding.
- `Official Cloud Assurance: not run` and `synthetic: true` in the SARIF panel.
- A placeholder patch (for example CP-001) shown as a draft marker, not a deployable config.
- The human-gate-adjusted score next to any structural score.
- The exact sentence: “This is a rehearsal on a synthetic estate; nothing is compiled, deployed, or officially assured.”

**Exit criteria:** a reproducible run, all artifacts hashed, and no slide or UI text that implies a real migration. This is the current stage.

### Stage 2 — Real read-only snapshot with evidence

**Purpose:** prove the method finds relevant issues on a real estate and that the use case is real.

**Evidence required:**
- Written authorization / data-processing agreement for a real snapshot.
- A read-only snapshot or repository export, with chain-of-custody and a SHA-256 manifest.
- Data classification/minimization; no unnecessary PII; redaction rules.
- Scope agreement: applications, LOBs, products, integrations, custom code, configuration, exclusions.
- Parser coverage: files parsed, unsupported/binary/corrupt files, LOC, languages, generated code.
- A blind SME validation sample: findings confirmed, rejected, or uncertain, with adjudication.
- A decision log: which findings changed a backlog item, assumption, estimate, or design decision.
- A measured reviewer-time or estimate-variance baseline, if the use-case claim is about efficiency.

**What PreFlight can claim:**
- “On this authorized real snapshot, PreFlight found X candidate issues across Y categories; a blind SME sample confirmed Z% (with confidence interval).”
- “The evidence pack changed N decisions and surfaced M named assumptions.”
- “The source snapshot hash was unchanged; no source files were written.”

**What PreFlight cannot claim:**
- Compilation, runtime, tenant compatibility, official Cloud Assurance, migration execution, or customer outcomes.
- That the findings are the full Cloud Standards set or that a candidate is a confirmed violation without SME adjudication.

**What the demo should show:**
- A redacted real evidence card with a custody ID, path, line, excerpt hash, and SME disposition.
- Parser coverage and an explicit unsupported/corrupt file list.
- A “candidate, pending SME triage” label on every finding.
- The decision log and the measured time/estimate impact.
- A clear statement: “This proves the assessment use case on a real estate; it does not prove the migration.”

**Exit criteria:** source hash unchanged, data-handling sign-off, a blind SME sample with a confidence interval, and at least one real decision influenced. This is the first stage that can honestly say the **use case** is real.

### Stage 3 — Compile/test in a Guidewire developer environment

**Purpose:** prove the refactors are buildable and testable in the target environment.

**Evidence required:**
- A Guidewire developer environment or development planet, with the target release pinned.
- Real code/config imported into the environment; a commit hash for the source and target.
- Gosu/Java compilation logs, including warnings and errors.
- Real Cloud API codegen / endpoint generation, with `_gen` and `_ext` outputs.
- APD/product-model import or synchronization for the in-scope product.
- GUnit/unit/integration tests, including failure-path and tenant-isolation tests.
- A dev-planet deployment and smoke test.
- A list of what was **not** compiled or tested and why.

**What PreFlight can claim:**
- “In-scope drafts compile and pass defined tests in a Guidewire developer environment on release X.”
- “The generated Cloud API/APD artifacts parse and the endpoint smoke test passed in dev.”
- “The source snapshot remained unchanged; the target commit is Y.”

**What PreFlight cannot claim:**
- Official Cloud Assurance, production data compatibility, performance, security, or cutover.
- That a successful dev build proves production readiness.

**What the demo should show:**
- A compiler/test transcript, not just a diff.
- Codegen output and a dev endpoint smoke test.
- A “Compiled in Guidewire dev” badge with build ID, target release, and commit hash.
- A still-visible “Official Cloud Assurance: not run” badge.
- A list of uncompiled/out-of-scope items.

**Exit criteria:** zero compile errors for in-scope artifacts, defined tests passing, code review, reproducible build. This is the first stage where the **code** is real in the target sense, but it is still not a migration.

**Important prerequisite:** PreFlight's Cloud API and App Events outputs are currently custom local descriptors, not Guidewire schema/mapping/updater syntax [docs/EVALUATION-SCOPE.md:47-48]. Stage 3 requires converting them into the actual Guidewire formats, or replacing them with real generated artifacts. A “compiled” claim cannot be made from the current custom YAML.

### Stage 4 — Official Cloud Assurance + SME sign-off

**Purpose:** prove the code passes the official standards gate and that accountable owners accept the residual risk.

**Evidence required:**
- A real branch/commit in the customer's source control.
- The official TeamCity Automated Cloud Assurance build, with Studio inspections and the Cloud Assurance Plugin [S1].
- The official inspection report, threshold result, and all violations (errors and warnings).
- A Cloud Standards mapping/triage for every open violation; accepted deviations with rationale.
- Named SME sign-offs: product/APD, rating/actuarial, integrations, security, data, operations, and compliance as applicable.
- A residual-risk register with owners and dates.
- If used, the customer's CUE or Cloud Assurance assessment report; do not conflate it with the automated build.
- APD/product-model validation and endpoint regeneration evidence.
- Security review and performance test evidence for the release candidate.

**What PreFlight can claim:**
- “Official Cloud Assurance ran on date X for commit Y against release Z; the result was R.”
- “Named owners signed off on the residual risks; the register is attached.”
- “The official report is linked to the PreFlight packet as evidence.”

**What PreFlight cannot claim:**
- Production cutover, customer outcomes, or regulatory approval unless separately evidenced.
- That PreFlight itself produced the official result. PreFlight can prepare evidence and attach the report; it cannot substitute for the official gate.

**What the demo should show:**
- The official report ID, date, commit, release, threshold, and open violations.
- A sign-off register with names/roles and residual risks.
- The “Official Cloud Assurance: not run” badge replaced only by a real “run on date X” badge.
- A clear distinction between PreFlight advisory findings and official violations.

**Exit criteria:** official result plus sign-offs plus no untriaged blockers; a release candidate. This is the first stage where “official Cloud Assurance” may be said — and only with the actual report.

### Stage 5 — Production cutover with rollback

**Purpose:** prove the migration actually worked in production and can be reversed if it did not.

**Evidence required:**
- A signed go/no-go decision and cutover runbook.
- Data migration: database snapshot, CDA/ETL path, row counts, reconciliation, and exception handling.
- Production deployment records for code, configuration, integrations, and product model.
- A tested rollback plan, including the rollback trigger, data rollback procedure, and communication plan.
- Production smoke tests, performance tests, error-rate/availability monitoring, and business-process validation.
- Hypercare for the agreed window (Guidewire's guide describes 4–6 weeks of post-deployment support [S9]).
- Business/customer acceptance and a post-implementation review.
- Outcome measurements against a pre-migration baseline: cycle time, defect rate, reviewer effort, cost, availability, or other agreed metrics.

**What PreFlight can claim:**
- “The migration was executed on date X; production verification passed; rollback was tested; outcomes were measured over period P.”
- “The customer accepted the result; the evidence pack contains the deployment, reconciliation, rollback, and hypercare records.”

**What PreFlight cannot claim:**
- Generalization to other insurers, long-term ROI beyond the measured window, or absence of future risk.
- That a successful cutover proves the assessment method generalizes.

**What the demo should show:**
- A cutover timeline with deployment IDs, data reconciliation, rollback checkpoint, hypercare metrics, and signed acceptance.
- If the evidence is not real, show an **empty evidence template** with named slots — do not simulate a production dashboard. A fake green production screen is worse than an honest blank.

**Exit criteria:** production stable for the agreed window, rollback not needed or successfully exercised, outcomes measured, and business acceptance signed. This is the only stage that proves a **migration**, not just a review or a build.

---

## 6. Slide-ready “Reality boundary” box

> ### Reality boundary — read before the demo
>
> **PreFlight is not a migration.** It is a synthetic, offline cloud-readiness review and refactor-drafting prototype.
>
> **It does not:** contact a tenant, compile Gosu/Java against Guidewire, generate real Cloud API endpoints, deploy to a planet, migrate data, or run official Cloud Assurance.
>
> **What is real:** the scanner, the rule citations where labeled, deterministic static analysis, evidence links, unified diffs, SARIF 2.1.0, a tamper-evident hash chain, and the two migration archetypes (monoline auto vs multi-line P&C).
>
> **What is synthetic:** the fixtures, insurer names, code, APD release scenarios, case-study numbers, and evaluation slice.
>
> **What is not proven:** compilation, runtime behavior, tenant compatibility, official Cloud Assurance, migration execution, rollback, and customer outcomes.
>
> **Use it for:** pre-migration triage, evidence assembly, assumption discovery, and reviewable draft refactors.
>
> **Do not use it for:** an actual-migration claim, a pass/fail, a certification, deployment approval, a savings claim, or a customer reference.
>
> **Official Cloud Assurance: NOT RUN.**

A shorter variant for a dense slide:

> **Real software. Synthetic estate. Unproven migration.**  
> PreFlight reviews and drafts; it does not compile, deploy, contact a tenant, or run official Cloud Assurance. The demo is a rehearsal, not a migration.

---

## 7. What would make this real

| Gap | Minimum evidence | Who owns it | Claim unlocked | Still not proven |
|---|---|---|---|---|
| Real estate input | Authorized read-only snapshot, chain-of-custody, SHA-256 manifest, data classification, parser coverage | Insurer + PreFlight team | “On this real snapshot, we found X candidates; Y% of a blind SME sample were confirmed.” | Compilation, runtime, tenant compatibility, official assurance. |
| Compilation | Guidewire developer environment, target release, real code/config, compiler logs, codegen output | Insurer/SI + Guidewire environment owner | “In-scope drafts compile in a Guidewire developer environment.” | Runtime, official assurance, production. |
| Runtime / integration tests | GUnit/unit/integration/E2E tests, failure-path tests, dev deployment, smoke tests | Insurer/SI engineering | “In-scope drafts pass defined tests in the target environment.” | Official assurance, production data, performance. |
| Real Cloud API/APD artifacts | Actual schema/mapping/updater/codegen files, APD import/conversion, endpoint generation, endpoint smoke test | Guidewire/SI + product model owner | “Endpoints and product model were generated and exercised in dev.” | Production, tenant data compatibility. |
| Official Cloud Assurance | TeamCity Automated Cloud Assurance report, Studio + Plugin inspections, threshold, violation triage | Guidewire/customer Cloud Assurance owner | “Official Cloud Assurance ran on date X; result R.” | Production cutover, outcomes. |
| SME sign-off | Named sign-offs for product/APD, rating, integration, security, data, operations; residual-risk register | Customer business/IT owners | “Accountable owners accepted the residual risks.” | Production behavior, long-term outcomes. |
| Data migration / cutover rehearsal | Database snapshot, CDA/ETL path, reconciliation, dry runs, rollback test, performance | Data migration lead + Guidewire Go-Live Management | “Cutover was rehearsed with reconciliation and rollback.” | Production success. |
| Production cutover | Deployment records, go/no-go, production smoke/performance, hypercare, business acceptance | Customer operations + Guidewire/SI | “The migration was executed and verified in production.” | Generalization, long-term ROI. |
| Security/compliance sign-off | Threat model, pen test, secret rotation, access review, data-handling/regulatory approval | Customer security/compliance | “Security and compliance review passed for the scope.” | The insurer's overall compliance. |
| Measured outcomes | Pre/post baseline: cycle time, defect rate, reviewer effort, cost, availability | Customer + independent evaluator | “Measured outcome over period P.” | Generalization to other insurers. |
| Independent evaluation | Blind SME annotation, inter-annotator agreement, real-estate precision/recall, reviewer-time study | Independent research/SME panel | “The method's accuracy and effort impact are measured independently.” | Migration execution. |

**Sequencing advice:** the cheapest credible next step is **Stage 2**, not more synthetic metrics. One real read-only snapshot with a blind SME validation sample would do more for credibility than another 100 synthetic files. Then take one feature slice through **Stage 3** in a Guidewire developer environment. Do not claim Stage 4 or 5 until Stages 2 and 3 are done.

---

## 8. Claim language: say this, not that

| Say this | Do not say this | Why |
|---|---|---|
| “PreFlight is a synthetic, offline cloud-readiness review and refactor-drafting prototype.” | “PreFlight migrates insurers to Guidewire Cloud.” | It does not perform a migration. |
| “On the synthetic demo estate, the review layer produced 24 candidate findings; on the synthetic Cascade estate, the lab produced 22 draft patches.” | “PreFlight fixed Cascade Mutual's cloud blockers.” | The fixes are drafts; the insurer is invented, and the two counts come from different layers. |
| “PreFlight emits SARIF 2.1.0 for advisory CI ingestion; official Cloud Assurance has not been run.” | “PreFlight passed Cloud Assurance.” | No official build, threshold, or report. |
| “The local audit chain verifies the run log.” | “The results are immutable, certified, or non-repudiable.” | It is tamper-evident, not non-repudiation. |
| “The 24-character APD type-name limit is documented; the 2027.04 20-character scenario is a simulation.” | “Guidewire is tightening the APD limit to 20 characters in 2027.04.” | No public 2027.04 release note or 20-character limit was found in the sources reviewed. |
| “The two case studies are synthetic archetypes: monoline auto vs multi-line P&C.” | “Cascade Mutual and Harbor P&C are customer case studies.” | The companies and numbers are invented. |
| “The codebase lab is a structural scanner and refactor drafter.” | “The code is compiled, tested, and deployable.” | No compiler, runtime, tenant, or deployment. |
| “The green signal is an internal structural verdict with human gates open.” | “100/100 means the estate is cloud-ready.” | The 100 is structural consistency; the human-gate-adjusted score is lower. |
| “The next step is a real read-only snapshot and blind SME validation.” | “The demo proves the migration works.” | Only Stage 3–5 evidence can prove migration. |

---

## 9. Unverifiable claims and status of previously open issues

Rows marked **RESOLVED** record issues found in the 2026-11-11 review that have since been fixed. They stay in the memo as evidence of what was wrong and what the current wording is.

| Location | Claim / issue | Why it is not verifiable or not yet supported | Recommended handling |
|---|---|---|---|
| Cloud Standards corpus and threshold | The full Cloud Standards rules and the exact Cloud Assurance threshold are not public. Standard pages redirect to `/gw-login`; the public Cloud Assurance page refers to “the threshold” without a number [S1][S2]. | Only public IDs/titles and process descriptions can be cited. The rule bodies and numeric threshold are gated. | Say “public ID/title verified; body gated; threshold not public.” Do not infer or invent a threshold. |
| **RESOLVED** · 2027.04 / 20-character APD scenario | `app/services/resilience.py:27-42` and `docs/RULES-RESEARCH.md:149-166,236-238` label the 20-character limit a simulation. `docs/presentation/AGENT-SLIDES-DRAFT.md:518` now says “The 24-character limit is documented; the 20-character 2027.04 scenario is a simulation.” | No public 2027.04 release note or 20-character APD limit was found in the sources reviewed. The deck and research note now agree. | Keep saying “documented 24-character type-name limit; 2027.04 20-character scenario is a simulation.” |
| **RESOLVED** · CDA as a read path | `app/services/code_migration.py:1485` defines CDA as the cloud data export/streaming service (S3 Parquet) and says synchronous in-app reads use Gosu Query or application APIs; `docs/CODEBASE-MIGRATION.md:70` reserves Cloud Data Access for analytics/export. The generated draft is `VehicleRatingQueryQueryService` (`app/services/refactor.py:532-546`). | CDA is a streaming/export service to S3, not a synchronous in-app query API [S15][S16]. The previous `VehicleRatingQueryCloudDataAccess` label and “supported cloud read path” glossary wording are gone. | Keep the “Gosu Query / application API” label for synchronous reads; reserve CDA for analytics/export. App-template glossaries must use the same wording. |
| **RESOLVED** · Harbor APD conversion coverage | `app/services/case_studies.py:141` labels Harbor “Cloud Retrofit + APD naming preparation (type-level codegen draft) · multi-LOB”; `:251-253` says the deliverable is a type-level `nameOverride`, not a full APD conversion. | The draft is still type-level only. A full APD conversion also involves APD import, field-level `schemaPropertyName`, product-model synchronization, and endpoint regeneration [S6]. | Keep the type-name-only label; do not present Harbor as APD-conversion coverage. |
| **RESOLVED** · Servlet wording | `app/services/case_studies.py:116` says “custom servlets are not a recommended practice; use the approved REST API framework.” | This matches the public policy [S14]; the stronger “not supported” wording is gone. | Keep “not recommended; use the approved REST API framework” and the `verified-policy` label. |
| Case-study footprint numbers | `docs/CASE-STUDIES.md:13`, `:61-63`; `app/services/case_studies.py:17-38`, `:122-143` give policy counts, states, screen counts, and rating volumes. | The profiles are invented; no customer data. The numbers are illustrative. | Put “invented” on the same slide as the numbers; do not use them in a benchmark or ROI claim. |
| “Over 90% of CAA findings resolved” | The 2026 Guidewire guest blog says Lighthouse resolves “over 90% of CAA findings” [S17]. | This is a vendor/guest-post claim; no independent data or methodology is provided. | Do not use it as evidence. If mentioned, label it “vendor claim, not independently verified.” |
| Demo snapshot hashes | `docs/demo/run-summary.json` records an audit head; the live `verify-audit` head on 2026-11-11 was different. | The packaged summary is a capture-time snapshot; the README says it is “not a live verifiable run” [docs/demo/README.md:3]. | Present it as historical; re-run `verify-audit`/`verify-packet` on the live run store for live proof. |
| “CAA” terminology | Some partner/guest material uses “Cloud Assurance Assessment (CAA)” alongside “CUE” and the automated build without a public definition. | The public Guidewire docs verified for this review describe the Automated Cloud Assurance build and the CUE; no public self-service “CAA” artifact or published threshold was found in the sources reviewed. | Use “CUE” for the formal assessment and “Automated Cloud Assurance” for the build gate. Do not treat the terms as interchangeable. |
| **RESOLVED** · Test counts | README says 481 (`pytest`, 2026-11-11); `docs/VERIFICATION.md` keeps 421 as an explicitly historical 8 November build and cites 481 as the current suite. | Test counts are build-specific and change with the suite. | Cite the current count and command; do not cite a stale count. |
| “100/100” structural score | The generated Cascade report shows 100/100 after the loop and 74/100 human-gate-adjusted; Harbor shows 100/100 and 71/100. | The 100 is structural consistency, not cloud readiness. | Show both numbers and the boundary; never show 100/100 alone. |

---

## 10. Sources and verification

All sources were accessed on **2026-11-11**. Status meanings: **200** = fetched successfully; **GATED** = redirected to Guidewire login; **429** = direct fetch rate-limited, search-indexed excerpt used; **PDF** = downloaded and text-extracted.

| ID | Source | URL | Access / status |
|---|---|---|---|
| S1 | Guidewire, “Automated cloud assurance and code compliance” | https://docs.guidewire.com/cloud/gcc-guide/insurer-developer/latest/automated-cloud-assurance | 200. Verified process, threshold language, `NEEDS WORK`, Studio + Cloud Assurance Plugin, 120-minute timeout. |
| S2 | Guidewire, “Guidewire Cloud Standards” overview | https://docs.guidewire.com/cloud/standards/latest/Overview/overview.html | GATED. Redirects to `/gw-login`; full corpus not public. |
| S3 | Guidewire, “INJ00-G: Prevent SQL Injection” | https://docs.guidewire.com/security/gosu-secure-coding-guidelines/INJ00-G | 200. “JDBC is not supported on Guidewire Cloud”; cloud execute calls prohibited. |
| S4 | Guidewire, “Correcting Cloud API LOB endpoint compile errors” | https://docs.guidewire.com/cloud/is/202607/cloudapica/cloudAPI/LOBEndpoints/generating-LOB-endpoints/c_correcting_compile_errors.html | 200. “type names are limited to 24 characters”; truncation, `nameOverride`, endpoint regeneration. Published 2026-10-22. |
| S5 | Guidewire, “Files that define LOB-specific endpoints” | https://docs.guidewire.com/cloud/pc/202603/cloudapica/cloudAPI/topics/508-LOBEndpoints/01-generating-LOB-endpoints/c_files_that_define_lob_specific_endpoints.html | 200. `_gen` vs `_ext`; “Do not modify codegen output files directly”; product access file. |
| S6 | Guidewire, “Codegen config file syntax” | https://docs.guidewire.com/cloud/pc/202603/cloudapica/cloudAPI/topics/508-LOBEndpoints/03-codegen-config-files/c_codegen_config_file_syntax.html | 200. `nameOverride`; field-level guidance limits it to Cloud Retrofit without APD App; `schemaPropertyName` for APD App/APD conversion. |
| S7 | Guidewire, “App Events” | https://docs.guidewire.com/education/cloud-integration-basics/latest/docs/integration_cloud_basics/appevents_overview | 200. New outbound asynchronous approach; describes custom message-transport plugins as the traditional approach; at-least-once; safe-ordered. |
| S8 | Guidewire, “Integration Gateway” | https://docs.guidewire.com/education/cloud-integration-basics/latest/docs/integration_cloud_basics/integration_gateway_overview | 200. Cloud-managed service; integration logic moves out of Gosu; Apache Camel. |
| S9 | Guidewire, “Migrating from Guidewire On-Premises to Guidewire Cloud: Clear Steps and Proven Results” | https://success.guidewire.com/rs/140-LHX-683/images/WP_Moving-to-the-Cloud-with-Confidence_EN_0525.pdf | PDF. Nine stages; CUE formal assessment; dress rehearsals; final dry runs; 4–6 weeks post-deployment support. |
| S10 | Guidewire, “Deploy Guidewire applications” | https://docs.guidewire.com/cloud/gcc-guide/insurer-developer/latest/deploy/ | 200. Development, pre-production, production planets; pre-production real user data; production live. |
| S11 | Guidewire, “Generating LOB-specific endpoints for non-APD-native products” | https://docs.guidewire.com/cloud/pc/202603/cloudapica/cloudAPI/topics/508-LOBEndpoints/01-generating-LOB-endpoints/c_generating_lob_specific_endpoints_for_non_apd_native_products.html | 200. Cloud Retrofit without APD App “is not the recommended Cloud Retrofit process.” |
| S12 | Guidewire, “What's new in Cloud Platform for Olos” | https://docs.guidewire.com/cloud/olos/whatsnew/topics/gwcp-release_highlights.html | 200. APD conversion; Standards Based Template (SBT) lines cannot be converted to APD-managed lines “at this time.” |
| S13 | Guidewire, “Data Security and Governance” | https://docs.guidewire.com/security/hardening-guidance-for-insurancesuite/data-security-and-governance | 200. Direct database modification via SQL “strictly prohibited”; secrets not in plaintext; platform-managed FIPS encryption; ad-hoc queries against read-only replicas. |
| S14 | Guidewire, “Application and Development Security” | https://docs.guidewire.com/security/hardening-guidance-for-insurancesuite/application-and-development-security | 200. Servlet quote; public `IS-*` titles/links; N−2 support. |
| S15 | Guidewire, `cda-client` (Open Source Reader for Cloud Data Access) | https://github.com/Guidewire/cda-client | 200. CDA populates an S3 bucket; reader downloads Parquet table data; repo archived 2026-07-22. |
| S16 | Guidewire developer blog, “Get to Know Cloud Data Access (CDA)” | https://www.guidewire.com/resources/blog/developers/get-to-know-cloud-data-access-webinar-guide-and-highlights | 429. Search-indexed excerpt: CDA is a data streaming service, near-real-time/historical changes, recommended for most cloud customers. Secondary/vendor source. |
| S17 | Guidewire developer blog, “Lessons from Guidewire Cloud Migrations” | https://www.guidewire.com/resources/blog/developers/lessons-from-guidewire-cloud-migrations-de-risking-the-move-to-saas-via-guidewire-cloud | 429. Published 2026-11-03. Search-indexed excerpt: database snapshot and cutover rehearsals; dry runs/fallback; full Cloud Assurance report in Lighthouse; “over 90% of CAA findings” vendor/guest claim. Secondary source. |
| S18 | Guidewire, “Guidewire Cloud Platform releases” | https://www.guidewire.com/products/technology/guidewire-cloud-platform-releases | 429. Search-indexed release context: Qusar (Aug 2026), Palisades (Apr 2026), Olos (Dec 2025). Secondary/vendor source. |

**Gated or rate-limited material:**
- Full Cloud Standards bodies, the complete standards corpus, and the Cloud Assurance numeric threshold are gated. Only public IDs/titles and process descriptions were verified.
- CDA guide pages redirect to login; public CDA evidence here is the official GitHub reader and the Guidewire blog.
- Several Guidewire marketing pages returned 429 to direct fetch; their search-indexed excerpts are labeled secondary and are not treated as standards.
- No tenant, customer data, credentials, or confidential Guidewire content was accessed.

**Repository evidence:** all repository paths and line references in this document were inspected on 2026-11-11. Commands were run from `/tmp/opencode` against the repository's `.venv`; the only file added by this review is `docs/REALITY-BOUNDARY.md`.

---

## 11. Bottom line

**Real software, synthetic estate, unproven migration.**

The demo is an **actual rehearsal**, not an **actual migration**. The use case — finding cloud-migration blockers early, linking them to evidence, and drafting reviewable refactors — is a real, documented problem aligned with Guidewire's public migration stages. But the demo's instance of that use case is synthetic and has not been used by a real insurer; the proof stops at the synthetic boundary. There is no compilation, no runtime, no tenant, no official Cloud Assurance, no data migration, no cutover, no rollback, and no customer outcome.

The fastest path to a stronger claim is not more synthetic metrics. It is:

1. One authorized, real, read-only snapshot with a blind SME validation sample.
2. One feature slice compiled and tested in a Guidewire developer environment.
3. One official Cloud Assurance run with named SME sign-off.
4. One production cutover with a tested rollback and measured outcomes.

Until then, say the narrow true thing:

> **PreFlight is a working, offline, evidence-first review prototype tested on synthetic Guidewire-style estates. It produces evidence-linked candidate findings, reviewable draft refactors, SARIF 2.1.0, and a tamper-evident audit trail. It does not compile, deploy, contact a tenant, or run official Cloud Assurance. The demo is a rehearsal, not a migration.**

---

*Independent review. Guidewire, InsuranceSuite, PolicyCenter, ClaimCenter, BillingCenter, Gosu, Advanced Product Designer, Cloud Assurance, Integration Gateway, and Cloud Data Access are trademarks or registered trademarks of Guidewire Software, Inc. This document is not affiliated with, endorsed by, or certified by Guidewire.*

[S1]: https://docs.guidewire.com/cloud/gcc-guide/insurer-developer/latest/automated-cloud-assurance
[S2]: https://docs.guidewire.com/cloud/standards/latest/Overview/overview.html
[S3]: https://docs.guidewire.com/security/gosu-secure-coding-guidelines/INJ00-G
[S4]: https://docs.guidewire.com/cloud/is/202607/cloudapica/cloudAPI/LOBEndpoints/generating-LOB-endpoints/c_correcting_compile_errors.html
[S5]: https://docs.guidewire.com/cloud/pc/202603/cloudapica/cloudAPI/topics/508-LOBEndpoints/01-generating-LOB-endpoints/c_files_that_define_lob_specific_endpoints.html
[S6]: https://docs.guidewire.com/cloud/pc/202603/cloudapica/cloudAPI/topics/508-LOBEndpoints/03-codegen-config-files/c_codegen_config_file_syntax.html
[S7]: https://docs.guidewire.com/education/cloud-integration-basics/latest/docs/integration_cloud_basics/appevents_overview
[S8]: https://docs.guidewire.com/education/cloud-integration-basics/latest/docs/integration_cloud_basics/integration_gateway_overview
[S9]: https://success.guidewire.com/rs/140-LHX-683/images/WP_Moving-to-the-Cloud-with-Confidence_EN_0525.pdf
[S10]: https://docs.guidewire.com/cloud/gcc-guide/insurer-developer/latest/deploy/
[S11]: https://docs.guidewire.com/cloud/pc/202603/cloudapica/cloudAPI/topics/508-LOBEndpoints/01-generating-LOB-endpoints/c_generating_lob_specific_endpoints_for_non_apd_native_products.html
[S12]: https://docs.guidewire.com/cloud/olos/whatsnew/topics/gwcp-release_highlights.html
[S13]: https://docs.guidewire.com/security/hardening-guidance-for-insurancesuite/data-security-and-governance
[S14]: https://docs.guidewire.com/security/hardening-guidance-for-insurancesuite/application-and-development-security
[S15]: https://github.com/Guidewire/cda-client
[S16]: https://www.guidewire.com/resources/blog/developers/get-to-know-cloud-data-access-webinar-guide-and-highlights
[S17]: https://www.guidewire.com/resources/blog/developers/lessons-from-guidewire-cloud-migrations-de-risking-the-move-to-saas-via-guidewire-cloud
[S18]: https://www.guidewire.com/products/technology/guidewire-cloud-platform-releases
