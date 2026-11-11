# PreFlight — Evidence & Claims Audit, Round 1

**Audited:** 11 November 2026 · repository `v2` · run `R-DEMO-001`  
**Scope:** `README.md`, `docs/PROJECT-REPORT.md`, `docs/PROJECT-REPORT-CHEATSHEET.md`, `docs/REALITY-BOUNDARY.md`, `docs/presentation/index.html` + `PreFlight-deck.pdf`, and the app UI served by FastAPI.  
**Method:** artifact inspection; CLI re-runs in a temporary copy; full pytest; claims lint; freeze recompute; codebase lab runs for both cases; FastAPI `TestClient` GETs; PDF page/text inspection. No product, test, fixture, or documentation source was edited. This report is the only file added by the audit.

**Overall verdict:** the executable core is real and the headline counts are almost entirely exact. The **claim presentation layer is not clean**: two app-UI statements overstate reality, one report carries hashes from a different run, the boundary document's own open-issue list is stale in five places, one QA score is stale, eight deck asset hashes do not match the files, and a re-run of the migrator does not reproduce the sealed 12-event/hash state. **Overall score: 6.9/10.** This is a strong demo with a documentation and provenance debt, not a fabrication problem.

---

## Scorecard

| Category | Score | Why |
|---|---:|---|
| Counts | **9/10** | Every headline count checked (300/101/31/24/12/5/11/6/7/8/12; Cascade 18/22/2/10; Harbor 20/21/2/11) is exact. Two wording problems: “12 mapping rules” when the pack has 16, and “126 evidence records” on the deck title when the headline elsewhere is 101 discovery evidence. |
| Hashes | **5/10** | Audit, packet, PDF and 18/18 freeze hashes verify. But `PROJECT-REPORT` prints hashes from an older run; the packet's rule-pack hash is not the frozen rule-pack hash; 8 deck asset hashes are stale; the frozen manifest's commit cannot be resolved. |
| Rule IDs | **9/10** | Rule IDs, claim-strength labels, 16 code families and the two `IS-*` bindings are consistent. README's summary table does not distinguish Cloud Standards from Gosu Secure Coding, though the deck does. |
| Code evidence | **7/10** | Source supports the core claims. Three specific `REALITY-BOUNDARY` code citations are stale (CDA draft class, Harbor APD label, servlet wording), and the app's CDA glossary still contradicts the corrected code and docs. |
| SARIF | **9/10** | Exact 2.1.0 documents; 18 results/13 rules for Cascade and 20 results/15 rules for Harbor; `official_cloud_assurance: false`; `synthetic: true`. Full schema validation was not run offline. |
| Test claims | **8/10** | 481 passed; 28 codebase tests pass. 421 and 418 are explicitly historical. `REALITY-BOUNDARY` still says README claims 449, which is false. |
| Reality boundary | **6/10** | The core “not an actual migration / not compiled / not official” position is correct and prominent. But `/case-studies` H1 says “Two completed migrations”, CDA is described in two UI glossaries as a synchronous read path, and the boundary document's open-issue table is stale. |
| Deck consistency | **7/10** | 23 slides, 23 PDF pages, sequential labels 1–23, no stale 16-slide text, 481 tests and 18/18 freeze claims verified. Title slide's 126/101 ambiguity, a stale APD caption on slide 17, and eight stale asset hashes keep it below 8. |
| Docs consistency | **4/10** | `PROJECT-REPORT` has the wrong Scribe hashes; README's QA panel is still Loop 2 7/10; `REALITY-BOUNDARY` has five stale issues; version/date labels disagree across README, deck, changelog and run-summary. |
| Reproducibility | **5/10** | Counts reproduce in a temp copy. Sealed hashes do not; a second `migrate` appends another 12 events; packet and frozen rule-pack hashes use different scopes; the deck regeneration path still enumerates 16 slides; the frozen commit is absent from history. |

**Average: 6.9/10.**

---

## 1. Exact commands and output

```text
$ .venv/bin/python -m app.cli verify-audit R-DEMO-001
R-DEMO-001: OK (9 events, head d3da24fac51f7c6a)

$ .venv/bin/python -m app.cli verify-packet R-DEMO-001
R-DEMO-001: OK - packet hash, content digests, and audit chain verified

$ .venv/bin/python -m app.cli verify-migration R-DEMO-001
R-DEMO-001: OK - 12 events verified

$ .venv/bin/python scripts/claims_lint.py
claims-lint: OK
exit=0

$ .venv/bin/python -m pytest -v -p no:warnings
======================== 481 passed in 88.33s (0:01:28) ========================

$ .venv/bin/python -m pytest tests/test_codebase.py -q -p no:warnings
............................                                             [100%]
28 passed in 3.67s

$ .venv/bin/python -m pytest tests/test_freeze_manifest.py -v -p no:warnings
tests/test_freeze_manifest.py .                                          [100%]
============================== 1 passed in 0.15s ===============================

$ freeze recompute (scripts/freeze.py primitives)
checks 18 pass 18
```

```text
$ .venv/bin/python -m app.cli codebase cascade-mutual --out /tmp/opencode/audit-cascade
cascade-mutual: green_with_human_gates · 18 findings · 22 patches · green=True

$ .venv/bin/python -m app.cli codebase harbor-pc --out /tmp/opencode/audit-harbor
harbor-pc: green_with_human_gates · 20 findings · 21 patches · green=True

cascade-mutual findings 18 patches 22 iterations 2 gates 10 guardian_checks 13 critic_checks 7 sarif 18 13
harbor-pc      findings 20 patches 21 iterations 2 gates 11 guardian_checks 13 critic_checks 7 sarif 20 15

cascade version 2.1.0 results 18 rules 13 official False synthetic True   pending 22 of 22
harbor  version 2.1.0 results 20 rules 15 official False synthetic True   pending 21 of 21
```

```text
$ R-DEMO-001 migration summary
{'files': 300, 'evidence': 101, 'findings': 24, 'dispositions': 12,
 'feature_evidence': 31, 'packages': 5, 'generated': 5, 'blocked': 0,
 'gates': 11, 'high_gates': 6, 'artifacts': 8}
verification: 7 checks, all ok, status passed
package approval: 5/5 pending
bundle file_count: 8 (5 targets + plan + report + audit log; manifest is the wrapper)
migration audit: 12 events, head 5c28ba80c3f75eb6, verified true
```

```text
$ pdfinfo docs/presentation/PreFlight-deck.pdf
Pages:           23
Page size:       1200 x 675.12 pts

$ deck structural check
labels 23 first [('1','23'),('2','23')] last [('22','23'),('23','23')]
sequential True totals {'23'}
pdf pages 23
legacy 16-slide text in HTML: []
legacy 16-slide text in PDF: []
```

---

## 2. Feature migrator claims

| Claim | Source | Verified evidence | Verdict | Fix |
|---|---|---|---|---|
| 300 files | README:122; PROJECT-REPORT:618; deck:1496 | `manifest.json` `file_count=300`; `find fixtures/demo-slice-300 -type f \| wc -l` → `300`; `preflight manifest fixtures/demo-slice-300` → `300 files … hash bd4a8a4b338a…` | **VERIFIED** | None. |
| 101 evidence records | README:139; PROJECT-REPORT:414,622 | `evidence.json` length `101`; Scout handoff reason: `300 files → 101 evidence records` | **VERIFIED** | None. Keep the distinction from the 126 packet-evidence total. |
| 31 PA-VEH-01 evidence links | README:139; deck:1496,1561 | `features.json` PA-VEH-01 `evidence_ids` length `31`; `spine.json` and UI summary both show 31 | **VERIFIED** | None. |
| 24 findings from 8 rules | README:125; PROJECT-REPORT:297,626 | `findings.json` length `24`; rule counter exactly 8 rules × 3 findings | **VERIFIED** | None. |
| 12 explicit dispositions | README:126; PROJECT-REPORT:414,622 | `mappings.json` length `12`; 8 `mapped_transformed` + 4 `mapped_exact` | **VERIFIED** | None. |
| 5 work packages / 5 draft files | PROJECT-REPORT:260,424; deck:1503 | `migration.json` `packages=5`, `generated=5`; WP-01…WP-05 all `draft_ready` | **VERIFIED** | None. |
| 11 open gates = 3 assumptions + 8 rule groups | PROJECT-REPORT:260; deck:1510 | `gates=11`; kinds `Counter({'review': 8, 'assumption': 3})`; G-01…G-03 assumptions, G-04…G-11 rule groups | **VERIFIED** | None. |
| 6 high-impact gates | PROJECT-REPORT:260; deck:1510 | severity `Counter({'high': 6, 'medium': 5})` | **VERIFIED** | None. |
| 7/7 Critic checks passed | PROJECT-REPORT:447; deck:1517 | `verification.checks` length 7, all `ok: true`, `status: passed`; UI shows `7/7` | **VERIFIED** | None. |
| 8 bundle files | PROJECT-REPORT:260; deck:1705 | `bundle.file_count=8`; entries are 5 targets + plan + report + audit log; manifest is not counted | **VERIFIED** | None. |
| 12-event audit log | deck:1706; PROJECT-REPORT:5.2 | `wc -l migration/audit.jsonl` → `12`; `verify-migration` → `12 events verified` | **VERIFIED** | None for the shipped run; see reproducibility for a re-run. |
| `completed_with_gates` | README:62; PROJECT-REPORT:260 | `migration.json.status` = `completed_with_gates`; UI renders the same | **VERIFIED** | None. |
| Migrator runs five agents as a straight handoff chain | README:55,60; deck:1481 | `migration.json.agents` = Scout, Architect, Guardian, Critic, Scribe, all `done`; no cyclic rework stage in the feature migrator | **VERIFIED** | None. |
| Every package still pending | README:62; deck:1703-1706 | `approval` = `pending` for all 5 packages; Critic check “human approval retained: 0 auto-approved” | **VERIFIED** | None. |
| Deck seal hashes: plan `3c307f75205c`, report `8770963bd2fd`, bundle `6c5b7f5a5aec`, log `5c28ba80c3f75eb6` | deck:1703-1706 | `migration.json` / `bundle-manifest.json` exactly match all four prefixes | **VERIFIED** | None. |
| Scribe plan `12c2d3d23446…`, report `ef9bf37eabcd…` | PROJECT-REPORT:459 | Current run is plan `3c307f75205c11e3…`, report `8770963bd2fd45b8…`; the quoted pair matches an earlier `R-20261111-052740-b001` seal log, not the current one | **STALE** | Replace with `3c307f75205c…` / `8770963bd2fd…`, or remove hashes from the prose and point to `bundle-manifest.json`. |

### Product, evaluation and packet claims

| Claim | Source | Verified evidence | Verdict | Fix |
|---|---|---|---|---|
| 8 business features | README:124; PROJECT-REPORT:621 | `features.json` length `8`; PA-VEH-01…PA-POL-02; all `lob=PersonalAuto` | **VERIFIED** | None. |
| 4 excluded files: 2 binary, 1 corrupt, 1 unsupported | README:210; PROJECT-REPORT:620 | `manifest.artifacts` statuses: `binary 2`, `corrupt 1`, `unsupported 1`; paths `dealer-logo.png`, `rate-table.xls`, `BrokenScreen.pcf`, `vehicle_rating_inputs.csv` | **VERIFIED** | None. |
| Source snapshot is unchanged after analysis | README:239; PROJECT-REPORT:619 | `immutability.json`: before = after = `bd4a8a4b338a…`, `unchanged: true` | **VERIFIED** | None. |
| Holdout is pre-computed and not imported | README:144; metrics | `metrics.json` supporting `HOLDOUT-RECALL 4/4`; `evidence.json` holdout `imported: false`; deck labels “not imported” | **VERIFIED** | None. |
| M1 8/8, M2 8/8, M3 101/101, M4 12/12, M5 6/6 (6/8 top-8), M6 48/48 | README:137-142; PROJECT-REPORT:324-329 | `metrics.json` exact numerators/denominators; M5 supporting `6/8`; M6 `24 TP / 0 FP / 0 FN` across 8 rules | **VERIFIED** | None. |
| Review packet has six sections | README:130; PROJECT-REPORT:341 | `packet.json.pages` = Cover, Executive summary, Coverage and confidence, Assumption register, Findings, Evidence and audit appendix | **VERIFIED** | None. |
| Long type is 37 characters against the 24-character APD import limit | README:296-297; deck:1099 | `feature_summary.long_type = 37`; finding F-023 says “37-character product-template type” and “over 24 characters”; labelled synthetic in the finding message | **VERIFIED** | None. |

---

## 3. Codebase lab claims

| Claim | Source | Verified evidence | Verdict | Fix |
|---|---|---|---|---|
| Cascade 18 findings | README:56; PROJECT-REPORT:631; deck:1809 | Re-run: `findings 18`; SARIF results 18 | **VERIFIED** | None. |
| Cascade 22 patches | PROJECT-REPORT:631; deck:1809 | Re-run: `patches 22`; all 22 `pending` | **VERIFIED** | None. |
| Cascade 2 iterations | PROJECT-REPORT:631; deck:1809 | Re-run: `iterations 2`; report shows Iteration 1 rework, Iteration 2 green | **VERIFIED** | None. |
| Cascade 10 human gates | PROJECT-REPORT:631; deck:1809 | Re-run: `gates 10`; report lists CR-01…CR-10 | **VERIFIED** | None. |
| Harbor 20 findings / 21 patches / 2 iterations / 11 gates | PROJECT-REPORT:632; deck:1809 | Re-run: `findings 20 patches 21 iterations 2 gates 11`; all 21 patches pending | **VERIFIED** | None. |
| Codebase lab runs five agents in a cyclic loop | README:56; PROJECT-REPORT:394 | Result: Scout, Architect, Guardian, Critic, Planner; 2 iterations with Guardian/Critic rework, then green | **VERIFIED** | None. |
| Guardian has 13 checks | PROJECT-REPORT:276; CHEATSHEET:76; UI | `_guardian_checks` returns 13 entries; UI reports `Guardian 13/13` | **VERIFIED** | None. |
| Critic has 7 checks | PROJECT-REPORT:5.3; UI | `_critic_checks` returns 7 entries; UI reports `Critic 7/7` | **VERIFIED** | None. |
| SARIF is 2.1.0 | README:23; REALITY-BOUNDARY:70,130 | Both files: `version 2.1.0`, `$schema https://json.schemastore.org/sarif-2.1.0.json` | **VERIFIED** | None. |
| SARIF Cascade 18 results / 13 rules | presentation/README:175; deck:1848; REALITY-BOUNDARY:70 | Re-run: `results 18 rules 13`; run properties `result_count 18`, `rule_count 13` | **VERIFIED** | None. |
| SARIF Harbor 20 results / 15 rules | presentation/README:175; deck:1848 | Re-run: `results 20 rules 15`; run properties `result_count 20`, `rule_count 15` | **VERIFIED** | None. |
| SARIF is advisory and synthetic | README:23; REALITY-BOUNDARY:85,132 | Run properties: `official_cloud_assurance: false`, `synthetic: true` on both cases | **VERIFIED** | None. |
| Every patch remains pending | README:87; deck:1864 | Bundle manifests: Cascade `22/22 pending`; Harbor `21/21 pending` | **VERIFIED** | None. |
| Structural 100/100, gate-adjusted 74/100 Cascade; 100/100, 71/100 Harbor | REALITY-BOUNDARY:221,484 | Both generated `MIGRATION-REPORT.md` files show those exact four scores | **VERIFIED** | None. Keep both numbers together. |
| 16 code rule families | README:279; deck:1809 | `rules/codebase_rules.yaml` has 16 rules across 11 categories | **VERIFIED** | None. |

### Rule IDs and claim strength

| Claim | Source | Verified evidence | Verdict | Fix |
|---|---|---|---|---|
| Review pack has 11 rules; 8 produce the demo's scored findings | REALITY-BOUNDARY:116; README:264-275 | `review_rules.yaml` has 11 rules; `findings.json` uses exactly 8 rule IDs × 3; `PF-GW-LOG-001/002` and `PF-GW-SBT-001` are separate from the 8 scored rules | **VERIFIED** | None. |
| Only two `IS-*` IDs are bound; `SEC00-G` and `ERR00-G` are Gosu secure-coding IDs, not Cloud Standards | REALITY-BOUNDARY:114; README:266-273 | `review_rules.yaml` and `codebase_rules.yaml`: `IS-TLS-1238` and `IS-TLS-1191` are `cloud-standard`; `SEC00-G`/`ERR00-G` are `gosu-secure-coding` | **VERIFIED** | None. Keep the standard-family column visible in the UI/README. |

---

## 4. Audit integrity and hashes

| Claim | Source | Verified evidence | Verdict | Fix |
|---|---|---|---|---|
| `verify-audit R-DEMO-001` passes with 9 events, head `d3da24…` | README:334; REALITY-BOUNDARY:71 | Exact output: `R-DEMO-001: OK (9 events, head d3da24fac51f7c6a)` | **VERIFIED** | None. |
| `verify-packet R-DEMO-001` passes | README:332; REALITY-BOUNDARY:72 | Exact output: `R-DEMO-001: OK - packet hash, content digests, and audit chain verified` | **VERIFIED** | None. |
| `verify-migration R-DEMO-001` passes | task; deck:1706 | Exact output: `R-DEMO-001: OK - 12 events verified` | **VERIFIED** | None. |
| Claims lint passes | README:332 | Exact output: `claims-lint: OK` | **VERIFIED** | None, but note the linter only scans templates, static assets and rule YAML; it does not scan README/docs. |
| Freeze hashes recompute 18/18 | README:332-333; deck:1939 | Recomputed 3 fixtures + reference + annotation guide + annotation concordance + rule pack + pre-registration + claims ledger + 9 gold files = 18; all pass | **VERIFIED** | None. |
| Packet audit head equals the audit-log head | REALITY-BOUNDARY:225; packet | Packet `audit_head` `d3da24fac51f7c6a689993154a6f30f3f469262071573adafb971ce539ed2bd5` equals last `audit.jsonl` hash; 9 events | **VERIFIED** | None. |
| Packet `hashes.rulepack` and `FROZEN.rulepack_sha256` identify the same pack | packet `hashes.rulepack`; `FROZEN.json` `rulepack_sha256` | `packet` = `f0733d19d4bb…` (all four YAML packs); `FROZEN` = `d84a4b7e7446…` (excludes `codebase_rules.yaml`). Both recompute, but they bind different scopes. | **STALE** (scope mismatch) | Align the scopes or document “review rule pack, excludes codebase pack” next to the packet hash. |
| FROZEN records the build commit | `ground_truth/FROZEN.json` | `commit: 95d179e1494de1f0d1ba1e0ee1a4eb97c31433ab`; `git cat-file -t` → `fatal: could not get object info`; not an ancestor of HEAD `4527950` | **UNVERIFIABLE** | Record a commit that exists, or mark the field historical/unknown and validate it in the freeze test. |
| Deck evidence asset hashes match | `docs/presentation/evidence.json` | 8 of 173 entries mismatch current files: `deck-slide-15-1440x900.png`, `-15-1920x1080.png`, `-15-390x844.png`, `-17-1024x768.png`, `-17-1280x720.png`, `-17-1440x900.png`, `-17-1920x1080.png`, `-17-390x844.png` | **STALE** | Re-sync `evidence.json` from the current `assets/deck-23/` files, or drop the hash field from the asset list. |
| A second migrator run keeps the 12-event state | task; deck:1694-1702 | Temp-copy re-run: counts identical, but plan `ce388d82…` vs sealed `3c307f75…`, report `30b02641…` vs sealed `8770963…`, and `verify-migration` reports `24 events verified` because `audit.jsonl` is append-only | **STALE** (reproducibility; shipped run itself is correct) | Reset the migration bundle before a re-run, or document that re-runs append and the sealed 12-event count applies only to the seeded run. |

---

## 5. Deck claims

| Claim | Source | Verified evidence | Verdict | Fix |
|---|---|---|---|---|
| 23 slides | deck:README:72; `index.html` | 23 `<section class="slide">`; 23 `aria-label="Slide X of 23"` labels | **VERIFIED** | None. |
| PDF has 23 pages at 1200 × 675 pt | deck:README:137,190; `evidence.json` | `pdfinfo` → `Pages: 23`, `Page size: 1200 x 675.12 pts`; PDF SHA-256 matches `evidence.json` (`ddb97057…`) | **VERIFIED** | None. |
| Slide numbers are the new 1–23 sequence | deck | Labels sequential 1…23; all totals `23`; footer `01 / 23`; no `of 16` | **VERIFIED** | None. |
| No stale 16-slide text | task | No `of 16`, `/ 16`, `16 slides`, `16-page`, `16 pages` in HTML or PDF text; legacy 16-slide proof paths are explicitly labelled legacy in `docs/presentation/README.md` | **VERIFIED** | None. |
| 481 tests and 18/18 freeze hashes | deck:1939,1944; README:13 | `pytest` → `481 passed`; freeze recompute → `18/18` | **VERIFIED** | None. |
| “Evidence records 126” on the title slide | deck:784 | Packet `counts.evidence=126` = `discovery_evidence=101` + `review_evidence=25`; slide 13 and the README headline use 101 discovery records | **VERIFIED** (different denominator) | Label it “126 packet evidence items (101 discovery + 25 review)” to avoid reading it as the 101 discovery count. |
| Slide 17: “Harbor’s visible ‘APD conversion’ label is the app’s program label” | deck:1783 | Current app label is `Cloud Retrofit + APD naming preparation (type-level codegen draft) · multi-LOB` (`case_studies.py:141`); there is no visible “APD conversion” label | **STALE** | Remove the sentence or replace it with “the app now labels this APD naming preparation; the deliverable is type-level only.” |
| 8 deck asset hashes | `evidence.json` | See §4: 8 stale hashes, 165 match | **STALE** | Re-sync. |
| The documented `--deck` capture path covers all 23 slides | deck:README:137; `scripts/capture_demo.py` | `scripts/capture_demo.py` still documents and loops over the original 16 slides (`range(1, 17)`); README explicitly discloses this and says a separate Playwright run produced the 23-slide proofs | **STALE** (tooling) | Extend the capture script to 23 before calling the deck reproducible from the repo tooling. |

---

## 6. Reality boundary and app UI

| Claim | Source | Verified evidence | Verdict | Fix |
|---|---|---|---|---|
| The demo is not an actual migration | README:21; PROJECT-REPORT:40; REALITY-BOUNDARY:7,19; deck:1534 | All core docs say so; no tenant/deployment artifacts; `REALITY-BOUNDARY` answers “No” explicitly | **VERIFIED** | None. |
| No compilation or deployment | README:26,359-361; REALITY-BOUNDARY:173-181; deck:1534 | `code_migration.py:313` “source code is not compiled”; no compiler/deploy invocation; codebase report says “No source writes, no _gen edits, no deployment” | **VERIFIED** | None. |
| Official Cloud Assurance was not run | README:9,29,277,371; deck; UI banner | No TeamCity/Cloud Assurance artifacts; README, deck, SARIF and UI all state `not run`; SARIF properties false | **VERIFIED** | None. |
| 2027.04 / 24→20-character scenario is simulated | README:362; REALITY-BOUNDARY:162,462; deck:1883,1895,1925 | Every deck occurrence says “simulated” or “not a published release”; `resilience.py` scenario IDs are models | **VERIFIED** | None. |
| Harbor APD deliverable is type-level naming preparation, not full APD conversion | README §2.3; PROJECT-REPORT:360; REALITY-BOUNDARY:209,477 | `case_studies.py:141` says `APD naming preparation (type-level codegen draft)`; codegen draft has a type-level `nameOverride`; docs say field mapping/APD import not modeled | **VERIFIED** | None in docs. See the stale deck caption row. |
| Cloud Data Access is streaming/export to S3 Parquet, not a synchronous in-app read path | PROJECT-REPORT:686; REALITY-BOUNDARY:193-197; `code_migration.py:1485` | Code glossary: `cloud data export/streaming service (S3 Parquet); synchronous in-app reads use Gosu Query or application APIs`; `CODEBASE-MIGRATION.md:95` says the same | **VERIFIED** (code/docs) | The app UI contradicts this — see next row. |
| App `/case-studies` glossary: CDA is “the supported cloud read path that replaces direct SQL/JDBC” | `app/templates/case_studies.html:64` | Page text exactly says that; same wrong definition in `app/templates/about.html:38` (“supported cloud way to read Guidewire data, replacing direct database or JDBC queries”) | **OVERSTATED** | Replace both with: “Cloud Data Access is a streaming/export service to S3 Parquet; synchronous in-app reads use Gosu Query or an application API.” |
| App `/case-studies` H1: “Two completed migrations you can explore” | `app/templates/case_studies.html:8` | Page's own boundary banner (line 20) says “synthetic rehearsal, not an actual migration”; outcome aria-label (line 86) says “Completed migration outcome”; workbench link (line 77) says “Explore two completed migration stories” | **OVERSTATED** | Change H1 to “Two completed synthetic migration rehearsals you can explore”; change aria-label to “Synthetic migration rehearsal outcome”; change link to “Explore two synthetic migration rehearsals.” |
| App UI exposes the correct status and counts | `/`, `/manifest`, `/reconstruction`, `/findings`, `/evaluation`, `/packet`, `/migrator`, `/codebase` | GET all return 200; Workbench summary 31/12/4/2/11; Manifest 300/4 excluded; Reconstruction 12; Findings 24; Evaluation 101/101; Migrator 101/31/5/11/7/7/8/12; Codebase 13/13 Guardian, 7/7 Critic, 10/11 gates, 22/21 pending | **VERIFIED** | None. |
| `100/100` structural score is not cloud readiness | REALITY-BOUNDARY:221,265,484; deck:1763,1778 | Both generated reports show 100/100 structural and 74/100 or 71/100 human-gate-adjusted; docs say the 100 is structural consistency | **VERIFIED** | None; keep both numbers adjacent. |

---

## 7. Tests, dates, and stale counts

| Claim | Source | Verified evidence | Verdict | Fix |
|---|---|---|---|---|
| Current suite is 481 passed (2026-11-11) | README:13,128,302; PROJECT-REPORT:630; CHEATSHEET:96; deck:1939 | `pytest -v -p no:warnings` → `481 passed in 88.33s (0:01:28)` | **VERIFIED** | None. |
| Codebase tests 28 passed | REALITY-BOUNDARY:69 | `pytest tests/test_codebase.py` → `28 passed in 3.67s` | **VERIFIED** | None. |
| 421 tests at the 8 November build | `docs/VERIFICATION.md:44,56`; `CHANGELOG.md:34` | Explicitly labelled historical; current line says 481 | **VERIFIED** (historical) | None; keep the qualifier. |
| 418 tests at an earlier iteration | `docs/presentation/ITERATION-LOG.md:132,142` | Explicitly labelled “at that iteration”; line 142 adds “Current pytest suite: 481 passed (2026-11-11)” | **VERIFIED** (historical) | None. |
| “README says 449 tests” | `docs/REALITY-BOUNDARY.md:483` | README says 481 at lines 13, 128, 302; no 449 in README | **STALE** | Replace with “README says 481; VERIFICATION/ITERATION-LOG cite 421/418 as historical builds.” |
| Panel score is 7/10 (Loop 2), hardening continues | README:330 | `docs/VERIFICATION.md:71-80` records Loop 4 final scores: Judge 8.0, UX 8.2, Guidewire 8.5, Engineering 8.0, and “no remaining demo blockers” | **STALE** | Update to the Loop 4 final scores, or explicitly say “historical Loop 2 score; final Loop 4 was 8.0–8.5.” |
| Snapshot version/date is `v1.0.0` / 2026-11-08 | README:119-120; deck:772; `run-summary.json`; `CHANGELOG.md:20` | README says v1.0.0/2026-11-08; deck says v1.0.0/2026-11-09; run-summary says `v1.1.0-demo`/2026-11-10; CHANGELOG puts migrator/codebase/23-slide deck in “Unreleased” | **STALE / inconsistent** | Use one current label: either `v1.1.0-demo (unreleased)` for the current run or keep `v1.0.0` only for the frozen release. |
| “12 mapping rules” | README:227; PROJECT-REPORT:149 | `rules/mapping_rules.yaml` has 16 rules (8 transformed, 4 exact, 2 not_applicable, 1 unresolved_gap, 1 unsupported); the run applies 12 dispositions | **STALE wording** | Say “16-rule mapping pack, 12 applied dispositions” or “12 explicit dispositions.” |

---

## 8. Documentation consistency and provenance

| Claim | Source | Verified evidence | Verdict | Fix |
|---|---|---|---|---|
| Scribe hashes in the project report | `PROJECT-REPORT.md:459` | See §2: `12c2d3d23446…` / `ef9bf37eabcd…` are not the current sealed values (`3c307f75…` / `8770963b…`) and do not match the current `R-20261111-052740-b001` plan/report hashes either | **STALE** | Replace with current values or remove. |
| REVIEW boundary §4.1 cites a `VehicleRatingQueryCloudDataAccess` draft class | `REALITY-BOUNDARY.md:197` | Current refactor function `_gosu_query_service_draft` generates a class named `VehicleRatingQueryQueryService`; no `CloudDataAccess` class exists in `refactor.py` | **STALE** | Re-point the evidence to the still-wrong UI glossary (`case_studies.html:64`, `about.html:38`) and delete the old class-name claim. |
| Boundary §4.3 cites Harbor “Cloud Retrofit with APD conversion” at `case_studies.py:125` | `REALITY-BOUNDARY.md:209` | Current `case_studies.py:141` says `Cloud Retrofit + APD naming preparation (type-level codegen draft) · multi-LOB`; the line number is also stale | **STALE** | Rewrite the issue as fixed, or point to the deck caption that still calls it “APD conversion.” |
| Boundary §4.4 cites a “not a supported cloud extension point” servlet summary | `REALITY-BOUNDARY.md:213,478` | Current `case_studies.py:116` says “custom servlets are not a recommended practice; use the approved REST API framework.” The stronger wording is gone. | **STALE** | Remove the open issue; keep the `verified-policy` label. |
| Boundary §9 says `AGENT-SLIDES-DRAFT.md:518` calls 2027.04 “not a hypothetical” | `REALITY-BOUNDARY.md:475` | Current line 518 says “The 24-character limit is documented; the 20-character 2027.04 scenario is a simulation.” | **STALE** | Remove the contradiction; the deck/research note now agree. |
| Boundary §9 says README claims 449 tests | `REALITY-BOUNDARY.md:483` | README says 481 (lines 13, 128, 302) | **STALE** | Update to 481. |
| Run summary represents the live R-DEMO-001 state | README:131; `docs/demo/run-summary.json` | `run-summary.json`: `snapshot v1.1.0-demo`, `audit_head 75b4b39d…`, `packet aea3c6e4…`; live at audit time: `d3da24fa…`, packet `589fe13d…`; `docs/demo/README.md:3` calls it “a historical snapshot, not a live verifiable run” | **STALE** (historical) | Regenerate or label the README row “historical capture” with the date. |
| `docs/demo/preflight-review-packet.html` represents the live packet | README:130 | Historical packet: 9 events, audit head `75b4…`, packet hash `aea3…`; live at audit time: 9 events, audit head `d3da…`, packet hash `589f…` | **STALE** (historical) | Keep as a downloaded example but label it “capture-time, not live.” |
| `docs/VERIFICATION.md` final status says only “Loop 2 7/10” | `VERIFICATION.md:56` | Same document later records Loop 4 final scores and “no remaining demo blockers” (lines 71-80) | **STALE internally** | Remove the older sentence or move it to a clearly historical section. |

---

## 9. Reproducibility detail

| Check | Result |
|---|---|
| Temp-copy migrator re-run counts | Identical: 300 files, 101 evidence, 24 findings, 12 dispositions, 31 PA-VEH-01 links, 5 packages, 11 gates, 6 high, 8 bundle files |
| Temp-copy migrator re-run hashes | Different: plan `ce388d82115a…` vs sealed `3c307f75205c…`; report `30b026413c5d…` vs sealed `8770963bd2fd…`; bundle `b7a8ccc1e97a…` vs sealed `6c5b7f5a5aec…` |
| Temp-copy migrator audit log | `verify-migration` → `24 events verified` because the migration log is append-only; the shipped run remains 12 |
| Freeze manifest commit | `95d179e…` is not present in this repository; `git cat-file` fails |
| Packet vs frozen rule pack | Packet `f0733d19…` includes `codebase_rules.yaml`; FROZEN `d84a4b7e…` excludes it |
| Deck asset hashes | 8 of 173 `evidence.json` entries stale |
| Deck regeneration tooling | `scripts/capture_demo.py --deck` still documents/enumerates 16 slides; README discloses and says the 23-slide run was separate |

**Assessment:** the *counts* and *reasoning* reproduce; the *sealed bytes* do not. That is acceptable for a demo if the claim is “deterministic counts on a fixed seed,” but not if the claim is “the sealed hash is reproducible.” The latter should be dropped or the re-run should reset the bundle.

---

## 10. What I could not verify

- **Official Cloud Assurance:** no official report, TeamCity build, Studio inspection or threshold artifact exists; the claim “not run” is consistent with the absence of evidence, but I cannot prove a negative beyond that.
- **Compilation / runtime / tenant compatibility:** no compiler, SDK, tenant or deployment was available; the docs correctly say so.
- **Guidewire public-source claims:** I did not re-fetch the external Guidewire pages; source citations in `REALITY-BOUNDARY` and the claims ledger are taken as recorded, not independently re-verified here.
- **Full SARIF schema conformance:** I checked version, schema URI, results, rules, locations, fingerprints and the advisory flags, but did not run a full JSON-Schema validation against the 2.1.0 schema offline.
- **11-event post-decision packet state:** the deck labels it as an isolated after-decision capture; I verified the seed state (9 events) and the documented counts, but did not re-execute the accept/reject actions to reproduce 11 events.
- **Playwright deck validation:** the recorded `assets/deck-23/validation.json` reports 23 slides at five viewports, zero console errors and zero external requests; I verified the static HTML/PDF facts but did not re-run that browser matrix.
- **GitHub release tag `v1.0.0`:** no network check; the local repository has no tag.

---

## 11. Fix list, in priority order

**P0 — fix before the next demo or claim review**

1. Change `/case-studies` H1, outcome `aria-label`, and the Workbench link from “completed migrations/stories” to “synthetic migration rehearsals.”
2. Fix the two UI CDA definitions (`case_studies.html:64`, `about.html:38`) to the streaming/export definition.
3. Replace the stale Scribe hashes in `PROJECT-REPORT.md:459` with the current `3c307f75…` / `8770963b…`, or remove them.

**P1 — fix before calling the claim set audited**

4. Update the README QA panel to the Loop 4 final scores (8.0–8.5) or explicitly label 7/10 as a historical Loop 2 score.
5. Refresh `REALITY-BOUNDARY.md` §4.1/§4.3/§4.4 and §9: five entries describe code that has already been fixed or a README test count that has changed.
6. Re-sync the 8 stale `deck-23` hashes in `docs/presentation/evidence.json`.
7. Align the packet and frozen rule-pack hash scopes, or document the difference next to the packet hash.
8. Record a resolvable commit in `FROZEN.json`, or remove/qualify the field.
9. Reset the migration bundle on a re-run, or document that a second run appends to the 12-event log and changes the sealed hashes.

**P2 — polish**

10. Align the version/date labels across README, deck, `run-summary.json`, and CHANGELOG.
11. Change “12 mapping rules” to “16-rule pack, 12 applied dispositions.”
12. Label the deck title's 126 as “126 packet evidence items (101 discovery + 25 review).”
13. Remove the stale “Harbor visible APD conversion label” sentence from slide 17.
14. Regenerate or clearly label the historical demo packet and run summary.

---

## 12. Bottom line

The demo's numbers are real. I found no evidence of invented counts, a fake Cloud Assurance result, a hidden compile/deploy, or a claim that the synthetic estate is a real insurer. The central execution claims — 300 files, 101 discovery evidence, 31 PA-VEH-01 links, 24 findings, 12 dispositions, 5 packages, 11 gates (3 + 8, 6 high), 7/7 Critic checks, 8 bundle files, 12-event migrator log, `completed_with_gates`, Cascade 18/22/2/10, Harbor 20/21/2/11, Guardian 13, Critic 7, SARIF 2.1.0 18/13 and 20/15, all patches pending, 481 tests, 23 slides and 23 PDF pages — are **verified**.

What is not clean is the claim surface: the `/case-studies` page still sells “two completed migrations,” two UI glossaries still describe CDA as a synchronous read path, `PROJECT-REPORT` prints another run's hashes, `README` cites a superseded QA score, `REALITY-BOUNDARY` keeps five already-fixed issues in its open-issues table, and eight deck asset hashes are stale. Those are fixable documentation and label defects, not a collapse of the project's evidence. Fix the P0/P1 list before using this package as an evidence-grade claim set.

**Score: 6.9/10 — strong executable evidence, weak claim hygiene.**

---

### Method note

No product, test, fixture, or documentation source was edited. The only file added by this audit is this report. One read-only `GET /packet?run=R-DEMO-001` through the app refreshed the capture-time `packet.json` / `packet.html` in the run store (the route rebuilds the packet on view); `verify-packet` still passes. That side effect is itself a minor product concern: a GET should not rewrite a sealed run artifact, or it should be explicit that `/packet` is a refresh action.
