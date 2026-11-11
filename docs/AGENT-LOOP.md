# Agent loop contracts

This document defines the two bounded agent loops in PreFlight:

1. the **feature migrator** (`app/services/migrator.py`), a straight-line,
   five-agent handoff over a completed review run; and
2. the **codebase lab** (`app/services/code_migration.py`), a cyclic,
   five-agent refactor loop over synthetic insurer estates.

The contracts below are written against the implementation, not the marketing
copy. Where the UI narrative and the code differ, the difference is called out.
All counts were observed on 11 November 2026 from the seeded run
`R-DEMO-001` and from `run_code_migration()` with two iterations.

| Loop | Agents | Shape | Machine gate | Human outcome |
|---|---|---|---|---|
| Feature migrator | Scout, Architect, Guardian, Critic, Scribe | Linear handoff with a documented but unimplemented rework branch | Critic 7/7 verification; sealing is not gated on it | `completed_with_gates`; 11 open gates |
| Codebase lab | Scout, Architect, Guardian, Critic, Planner | Real two-iteration red→green cycle | Guardian 13 checks + Critic 7 checks | `green_with_human_gates`; 10 or 11 open gates |

Neither loop deploys, edits `_gen` files, approves its own changes, resolves an
assumption, or contacts a Guidewire tenant.

---

## 1. Control flow at a glance

### Feature migrator

```text
Scout ──scope──▶ Architect ──packages──▶ Guardian ──gates──▶ Critic ──verdict──▶ Scribe ──▶ sealed bundle
  │                  │                       │                  │
  └ read-only        └ migration/target/**    └ 3 + 8 gates      └ 7 checks; no model unless live annotation
```

The implementation is a single pass. The UI view publishes a `loop.rework_path`
string saying Guardian or Critic can send the package back to Architect, but
`run_migration()` has no such branch. A failed Critic verdict is recorded and
Scribe still seals the bundle. Rework is an operator action: fix the input
artifact and rerun (CLI `migrate`; API `force: true`).

### Codebase lab

```text
Scout ──inventory──▶ Architect ──draft──▶ Guardian
                         ▲                   │
                         │                   ▼
                         └──fix requests── Critic
                                             │
                              both green ────┴──▶ Planner
```

This is a genuine loop. Iteration 1 is error-first; iteration 2 is full. If the
budget expires, the loop stops red rather than manufacturing a green signal.

---

## 2. Feature migrator contracts

### 2.1 Shared invariants

- **Input gate:** the review run must have `status == "succeeded"`; otherwise
  `run_migration()` raises `ValueError("migration requires a succeeded analysis run")`.
- **Evidence gate:** every work package must carry at least one evidence ID.
- **Path gate:** targets must be relative, must not contain `..`, and must not
  start with `_gen/` or equal `_gen`.
- **Approval gate:** every package is written with `approval: "pending"`.
- **Seal:** plan, report, target files, manifest, and a separate hash-chained
  audit log are written under `migration/`.
- **Determinism:** no model is called on the offline path. Counts, gate groups,
  paths, and check outcomes are deterministic for the same input. Timestamps,
  latency fields, and therefore the plan/report SHA-256 values vary between runs.

### 2.2 Scout — inventory and scope

| Field | Contract |
|---|---|
| **Inputs** | `status.json` (must be `succeeded`), `features.json`, `manifest.json`, `evidence.json`, `findings.json`, `mappings.json`, `assumptions.json`. |
| **Allowed evidence** | All persisted review artifacts; the feature slice is `feature.evidence_ids` from `features.json`. On the demo this is 31 evidence links out of 101 evidence records. |
| **Outputs** | Agent summary, four checks, progress `18`, and summary counts: files, evidence, findings, dispositions, feature evidence. |
| **Checks** | `run succeeded`; `feature resolved`; `feature evidence` (`len(feature_evidence) > 0`); `source snapshot` (`manifest.sha256` present). On the demo: **4/4**. |
| **Failure modes** | Run not succeeded → hard `ValueError`. Feature ID not found → hard `ValueError`. Missing artifact → read helper returns an empty default. Empty feature evidence → the check records `ok: false`, but the run continues; there is no hard refusal in this build. |
| **Determinism** | Fully deterministic counts and check outcomes. Summary text is deterministic for the same artifact set. |
| **Boundary** | Read-only. Does not write source, edit `_gen`, deploy, or approve. |

**Observed summary:** `300 files → 101 evidence records · 24 findings · 12 dispositions · 31 evidence links on PA-VEH-01`.

### 2.3 Architect — target draft

| Field | Contract |
|---|---|
| **Inputs** | `changes.json`, `mappings.json`, `evidence.json`, `draft/**`, Scout's feature scope. |
| **Allowed evidence** | For each change, the mapping's `source_ref`; the agent searches evidence excerpts for the leaf token and keeps at most two IDs. If none match, it falls back to the first two feature evidence IDs. This is a lexical link, not a semantic proof. |
| **Outputs** | One work package per change (`WP-01` …), target files under `migration/target/**`, SHA-256 and byte count per output, package status `draft_ready` or `blocked`, `approval: pending`. |
| **Checks** | `explicit dispositions` (mappings exist); `target files generated` (all packages ready); `_gen untouched`. On the demo: **3/3**. |
| **Failure modes** | Unsafe or `_gen` target → package `blocked`, reason `unsafe or _gen target path`. Duplicate target → `blocked`, `duplicate target path`. Missing draft output → `blocked`, `draft output is missing`. No changes → zero packages; missing mappings leave a package without a disposition/source and can still fall back to feature evidence. The run continues and later checks record the gap. |
| **Determinism** | Package order follows `changes.json`; target bytes are copied from the draft; hashes are deterministic. |
| **Boundary** | Draft generation only. Does not compile, deploy, approve, or modify `_gen`. |

**Observed summary:** `5 work packages · 5 draft files generated · 5 target artefacts in migration/target/`. All five packages are `draft_ready`, all `approval: pending`, and the bundle manifest lists **8** hashed files (five targets, plan, report, audit log); the manifest itself is the ninth file.

### 2.4 Guardian — deterministic risk gates

| Field | Contract |
|---|---|
| **Inputs** | Open assumptions from `assumptions.json`; findings from `findings.json` with `decision == "open"`; Architect's package list. |
| **Allowed evidence** | Assumption statements, questions, impacts, owners; finding rule IDs, titles, severities, decisions. Explicitly **not** Scout's narrative, Critic's verdict, or any model text. |
| **Outputs** | Gate register: one gate per open assumption plus one gate per open rule family; gate ID, kind, severity, title, question, owner, source ID, status `open`. |
| **Checks** | `assumption gates`; `finding gates`; `no self-approval`. These are bookkeeping checks and are all hard-coded `ok: true`; the real gate is the gate register itself. On the demo: **3/3**. |
| **Failure modes** | No normal failure path. Missing fields default (`unknown` rule, `medium` severity, `unassigned` owner). A malformed title falls back to a count of 1 in the view layer. |
| **Determinism** | Assumption order follows the artifact; rule groups are sorted by `rule_id`; gate IDs are assigned in that order. No model call. |
| **Boundary** | Opens gates; cannot resolve them, approve a package, or waive a finding. |

**Observed result:** **11 open gates = 3 assumption gates + 8 review-rule groups**; **6 high-impact gates**; deployment remains blocked. Each of the eight rule groups aggregates three findings, so the 24 findings become eight gates, not 24. Gate IDs `G-01`–`G-03` are assumptions; `G-04`–`G-11` are rule groups.

### 2.5 Critic — adversarial verification

| Field | Contract |
|---|---|
| **Inputs** | Architect's packages and outputs; generated files on disk; package evidence IDs and approval state. |
| **Allowed evidence** | Package metadata, target files, generated JSON/YAML. It does not consult the gate register when computing its seven checks. |
| **Outputs** | `verification.status` (`passed` / `failed`), seven checks with detail, Critic summary and verdict text. |
| **Checks** | `packages exist`; `all package files generated`; `no _gen targets`; `no duplicate targets`; `generated JSON/YAML parses`; `every package is evidence-linked`; `human approval retained`. On the demo: **7/7 PASS**. |
| **Failure modes** | Missing output → generation check fails. Unreadable or unparseable JSON/YAML → parse check fails with the path and parser message. Duplicate path → duplicate check fails. Empty evidence list → evidence check fails. An unexpected exception → the orchestrator catches it, marks the run `failed`, and appends `migration.failed`. |
| **Determinism** | Fully deterministic. Optional live annotation is recorded but cannot override the deterministic PASS/FAIL. |
| **Boundary** | Verifies; does not repair, approve, or block Scribe in code. |

### 2.6 Scribe — seal the bundle

| Field | Contract |
|---|---|
| **Inputs** | Final state, packages, gates, outputs, plan payload, Critic verification, source snapshot hash. |
| **Allowed evidence** | The state and its hashes. It does not read the model or re-litigate findings. |
| **Outputs** | `migration/migration-plan.json`; `migration/MIGRATION-REPORT.md`; `migration/bundle-manifest.json`; `migration/audit.jsonl`; target files. Plan SHA-256, report SHA-256, bundle SHA-256, per-file hashes, audit head and verification. |
| **Checks** | `plan written`; `report written`; `bundle manifest written`. All three are hard-coded `ok: true` after the writes succeed. On the demo: **3/3**. |
| **Failure modes** | Any write or hash error propagates to the orchestrator's catch-all: state `failed`, current agent `failed`, audit event `migration.failed`. A broken audit chain is reported in `state.audit.verified` and detail; it does not roll back the files. |
| **Determinism** | File inventory, order, and per-file hashes are deterministic for the same bytes. Plan/report bytes include timestamps and therefore differ between runs. |
| **Boundary** | Sealing is tamper-evidence, not approval. Scribe does not resolve gates or deploy. |

**Observed result (seed generation):** plan `3c307f75205c…`, report `8770963bd2fd…`, **8** manifest entries, **12** audit events in the seed log. A rerun appends to the same audit log; it does not truncate it, and the new plan/report/bundle hashes are not expected to match the seed values. The migration directory is not pruned, so a target file from a previous run can remain on disk even when it is absent from the new manifest. Treat the manifest, not the directory listing, as the authoritative bundle inventory.

### 2.7 Observed feature-run totals

| Metric | Value |
|---|---|
| Source files | 300 |
| Evidence records | 101 |
| Evidence links on `PA-VEH-01` | 31 |
| Findings | 24 |
| Explicit dispositions | 12 |
| Work packages | 5 |
| Draft targets generated | 5/5 |
| Blocked packages | 0 |
| Open gates | 11 (3 assumptions + 8 rule groups) |
| High-impact gates | 6 |
| Critic checks | 7/7 passed |
| Manifest entries | 8 |
| Audit events | 12 verified |
| Status | `completed_with_gates` |
| Progress checkpoints | 18 → 42 → 65 → 85 → 100 |

### 2.8 Feature handoff table

| Seq | From → To | Payload | Acceptance |
|---|---|---|---|
| 1 | Scout → Architect | Feature scope, 31 evidence links, 12 dispositions, 24 findings | Feature is resolved and at least one evidence link exists (recorded, not enforced). |
| 2 | Architect → Guardian | 5 packages, 5 target files, 8 bundle artefacts | Paths are safe, unique, non-`_gen`; every package is `draft_ready`. |
| 3 | Guardian → Critic | 11 gates: 3 assumptions + 8 rule groups | Gate register is open; no approval recorded. |
| 4 | Critic → Scribe | 7/7 checks passed, verdict PASS | Packages exist, parse, are evidence-linked, and remain pending. |
| 5 | Scribe → sealed bundle | Plan, report, manifest, audit log, target files | Hashes written; audit chain verified; every change pending. |

### 2.9 Rework path

**Feature migrator, as implemented.** There is no automatic rework edge. The
view exposes `loop.rework_path` as narrative:

> “Guardian or Critic can send the package back to Architect; Scribe only seals
> after verification.”

The orchestrator does not implement that message. If Critic returns a failed
verification, Scribe still writes the bundle and the run can finish as
`completed` or `completed_with_gates` with `verification.status == "failed"`.
The sealed bundle is therefore a record of a failed pass, not a green one.

The actual rework procedure is:

1. resolve or explicitly disposition the failing assumption or finding in the
   review run;
2. correct the source mapping/change/draft artifact;
3. rerun `preflight migrate RUN_ID` or `POST /api/runs/{run_id}/migration` with
   `{"force": true}`;
4. verify the new audit chain with `preflight verify-migration RUN_ID`.

**Codebase lab, as implemented.** The real rework edge is
`Critic → Architect`. It is described in section 3.5.

---

## 3. Codebase lab contracts

### 3.1 Shared invariants

- **Source read-only:** the scanner and refactorer never write the source tree;
  a before/after tree hash must match.
- **Bounded budget:** `max_iterations` defaults to 3 and is capped at 5 by the API.
- **Draft-only:** patches are unified diffs plus target drafts; nothing is
  compiled against a Guidewire runtime, deployed, or auto-approved.
- **Evidence:** every finding has a path, line, excerpt hash, and fingerprint.
- **Determinism:** rule detection, patch ordering, gate checks, and risk
  templates are deterministic. Live annotation is optional and cannot change
  a verdict.

### 3.2 Scout

**Inputs:** read-only case fixture; code rule pack; guarded scan result.
**Allowed evidence:** scanned source files, findings, language/category counts,
feature slices from the profile.
**Outputs:** summary, four checks, files, LOC, language mix, category mix,
severity mix, feature inventory, hotspots, import edges, skipped files.
**Checks:** source scan completed; supported files found; line evidence complete;
language coverage.
**Failure modes:** analyzer exception → `analyzer_failed`; source tree changes
mid-scan → `source_changed`; zero supported files → `insufficient_evidence`.
Those outcomes return an explicit empty result, not a score.
**Determinism:** deterministic for the same tree and rule pack.
**Boundary:** read-only inventory.

### 3.3 Architect

**Inputs:** Scout's findings; refactor strategies; effective APD limit.
**Allowed evidence:** finding rule IDs, paths, lines, excerpts; source tree.
**Outputs:** unified-diff patches, target tree, added cloud configuration drafts,
deleted files, codegen overrides, per-patch risk/semantic-review/`pending`.
**Checks:** no separate check list; its summary records patch count, target file
count, added/deleted counts, and iteration mode.
**Failure modes:** refactor exception → whole run `failed` with the source scan
preserved; duplicate/unsafe targets → Guardian path checks fail; a target that
does not reproduce its diff → Critic diff check fails.
**Determinism:** patch IDs, target paths, and diff content are deterministic for
the same source and rules.
**Boundary:** local target tree only; no source writes, no `_gen` edits, no
compile, no deploy.

### 3.4 Guardian

**Inputs:** source scan, target re-scan, patches, SARIF, target file contents,
source-hash equality.
**Allowed evidence:** deterministic scans and patch metadata only. Never the
Scout narrative, Critic opinion, or live model text.
**Outputs:** `verdict` (`green` / `rework`), 13 checks, blocking list, summary.
**Checks (13):**

1. source snapshot unchanged;
2. every source finding has a patch;
3. target has no error-severity blockers;
4. target has no residual warnings;
5. APD type names fit the effective import limit;
6. no `_gen` targets;
7. target paths are unique and safe;
8. generated XML/JSON/YAML drafts parse;
9. secret patches redact their displayed diffs;
10. all patches remain pending approval;
11. SARIF 2.1.0 is structurally valid;
12. SARIF results cover every source finding;
13. target draft files exist.

**Failure modes:** any failed check → `rework`; no “warn and continue” path.
**Determinism:** fully deterministic; the only model-adjacent input is the
optional annotation, which is not read by Guardian.
**Boundary:** blocks a green signal; cannot approve, deploy, or waive a check.

### 3.5 Critic and the actual rework path

**Inputs:** source scan, target scan, patches, Guardian verdict, target contents.
**Allowed evidence:** applied diffs, coverage, source hash, target findings.
**Outputs:** `verdict`, seven checks, residual-risk register, fix requests.
**Checks (7):** Guardian is green; patch coverage is complete; displayed diffs
reproduce target drafts; target paths are unique; source snapshot is unchanged;
target re-scan has zero blockers; no automatic approval.
**Risks:** one named gate per finding category, with severity, owner, action,
rule IDs, evidence paths, `blocking: false`, `human_gate: true`, `status: open`.
On Cascade these are `CR-01`–`CR-10`; on Harbor `CR-01`–`CR-11`.
**Failure modes:** a diff that does not reproduce its target → rework; duplicate
targets → rework; residual target blocker → rework; exhausted budget → `blocked`.
**Determinism:** the seven checks and the risk templates are deterministic.
Optional live annotation is advisory.
**Boundary:** records human gates; does not approve.

**Rework path:** if either Guardian or Critic is red, Critic appends
`Critic → Architect` with targeted fix requests. Architect re-enters the loop;
the prior draft is superseded and its temporary tree is cleaned up. On both
synthetic insurers this happens exactly once.

### 3.6 Planner

**Inputs:** profile, source scan, target scan, patches, Guardian result, Critic
result, iteration history, green signal, SARIF, optional upgrade impact.
**Allowed evidence:** the compiled results only.
**Outputs:** executive summary, readiness (`score_before`,
`structural_score_after`, `human_gate_adjusted_score`), risk register, next
actions, `MIGRATION-REPORT.md`, report SHA-256, SARIF summary.
**Checks:** no pass/fail checks; it compiles.
**Failure modes:** report assembly error → run `failed`.
**Determinism:** report content is deterministic except timestamps; score is a
weighted structural indicator, not a Cloud Assurance score.
**Boundary:** the report is a human-review artifact. `green_signal.planner` is
set to `true` whenever the report compiles, including a blocked run; it does not
mean the migration is green. The authoritative gate is
`green_signal.unified`.

### 3.7 Observed codebase runs

| Metric | Cascade Mutual | Harbor P&C |
|---|---|---|
| Source files | 17 | 15 |
| LOC | 156 | 160 |
| Languages | Gosu 10, GUnit 1, Java 1, product template 1, XML 4 | Gosu 9, GUnit 1, Java 1, product template 1, XML 3 |
| Findings | 18 (10 error, 8 warning) | 20 (11 error, 9 warning) |
| Iteration 1 patches | 16 (error-first) | 17 (error-first) |
| Iteration 1 Guardian | 11/13 | 11/13 |
| Iteration 1 Critic | 4/7, 2 fix requests | 4/7, 2 fix requests |
| Iteration 2 patches | 22 (full) | 21 (full) |
| Iteration 2 Guardian | 13/13 green | 13/13 green |
| Iteration 2 Critic | 7/7 green | 7/7 green |
| Target files | 24 | 23 |
| Added files (config, Gosu, Java) | 7 | 8 |
| Human gates | 10 | 11 |
| Readiness | 0 → 100 structural → 74 adjusted | 0 → 100 structural → 71 adjusted |
| SARIF | 18 results / 13 rules | 20 results / 15 rules |
| Audit events | 15 verified | 15 verified |
| Status | `green_with_human_gates` | `green_with_human_gates` |

A one-iteration run of Cascade stops at `blocked` with Guardian `rework`,
Critic `rework`, two fix requests, and no false green.

### 3.8 Codebase handoff table

| Seq | From → To | Cascade payload | Harbor payload |
|---|---|---|---|
| 1 | Scout → Architect | 17 files, 18 blockers, 5 feature slices | 15 files, 20 blockers, 6 feature slices |
| 2 | Architect → Guardian (pass 1) | 16 patches, 7 added files | 17 patches, 8 added files |
| 3 | Guardian → Critic (pass 1) | `rework`, 11/13; blocking coverage and residual warnings | same check pattern, 11/13 |
| 4 | Critic → Architect | 2 targeted fix requests | 2 targeted fix requests |
| 5 | Architect → Guardian (pass 2) | 22 patches, 7 added files | 21 patches, 8 added files |
| 6 | Guardian → Critic (pass 2) | `green`, 13/13 | `green`, 13/13 |
| 7 | Critic → Planner | both green; 10 human gates remain | both green; 11 human gates remain |

### 3.9 Codebase rework path

```text
Guardian rework or Critic rework
        │
        ▼
Critic emits fix requests (reason, instruction, affected check names or rule IDs)
        │
        ▼
Architect re-runs with a wider severity set (iteration 1: errors only;
iteration 2+: errors + warnings)
        │
        ▼
Prior draft is superseded; temporary target tree is cleaned up
        │
        ├── both green → Planner compiles
        └── budget exhausted → blocked, no green
```

---

## 4. Cross-loop comparison

| Dimension | Feature migrator | Codebase lab |
|---|---|---|
| Unit of work | Explicit source→target disposition from a completed review | Code finding and refactor family |
| Evidence | Evidence IDs linked to a feature slice | Path, line, excerpt hash, fingerprint |
| Guardian | 11 gates; 3 bookkeeping checks | 13 deterministic checks |
| Critic | 7 package checks | 7 patch checks + risk register |
| Rework | Operator rerun; no implemented auto-loop | Implemented `Critic → Architect` loop |
| Seal | Plan/report/manifest/audit | Report/SARIF/bundle manifest; in-memory audit |
| Green meaning | Verification passed; human gates remain | Machine gates agree; human gates remain |
| Deployment | None | None |

---

## 5. Boundary

Both loops are **bounded autonomy**. The feature migrator writes a local,
non-deployable target bundle. The codebase lab writes local refactor drafts.
Neither edits `_gen` files, writes source, approves a change, resolves an
assumption, compiles against a Guidewire runtime, or contacts a tenant. A sealed
bundle is tamper-evident, not approved. Official Cloud Assurance was not run.
