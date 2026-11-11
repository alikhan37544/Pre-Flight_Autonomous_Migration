# Upgrade resilience and stale-green handling

A cloud-migration assessment can stay open for weeks while the target release
moves underneath it. `app/services/resilience.py` models that reality explicitly:
a release upgrade names the old and new release, identifies affected patches,
invalidates a prior green signal, and records a resume decision.

The mechanism is deliberately conservative. It never silently reuses a green
signal, never treats a resume choice as an approval, and never restores files on
its own. The sealed bundle is the checkpoint; a “rollback” is a recorded decision
to resume from it, not a filesystem restore.

---

## 1. The five release scenarios

All five are **PreFlight simulations**. `GWCP 2027.04` is not a verified public
Guidewire release note; the scenario IDs and effective values exist to exercise
the logic. Do not cite them as published vendor commitments.

| Scenario ID | Simulated label | Simulated release window | Severity | Affected rules | Effective constraint | Required action | Owner |
|---|---|---|---|---|---|---|---|
| `GWCP-APD-NAMING-2027.04` | APD import limit tightens from 24 to 20 characters | GWCP 2026.10 → 2027.04 | high | `PF-CODE-APD-001` | `apd_name_limit: 20` | Regenerate codegen `nameOverride` entries and endpoint drafts at 20 characters. | APD / product model owner |
| `GWCP-APP-EVENTS-V2-2027.04` | App Events envelope moves to schema v2 | GWCP 2026.10 → 2027.04 | high | `PF-CODE-MSG-001` | `app_events_schema: "2.0"` | Re-run the App Events contract check; add `tenantId`/`eventId` envelope fields. | Integration owner |
| `GWCP-GATEWAY-MTLS-2027.04` | Integration Gateway requires mTLS and scoped service auth | GWCP 2026.10 → 2027.04 | medium | `PF-CODE-SRV-001`, `PF-CODE-MSG-001` | `gateway_auth: mtls+scoped-service` | Add mTLS and scoped service authorization to each route draft. | Platform integration owner |
| `GWCP-GOSU-API-REMOVAL-2027.04` | A deprecated Gosu API is removed from the target runtime | GWCP 2026.10 → 2027.04 | high | `PF-CODE-API-001`, `PF-CODE-API-002` | removed APIs: `java.rmi`, `javax.ejb`, `gw.internal` | Re-run Architect on affected classes and replace the removed API. | Application development owner |
| `GWCP-CLOUD-API-VERSION-2027.04` | Cloud API extension routes move to a new version prefix | GWCP 2026.10 → 2027.04 | medium | `PF-CODE-SRV-001` | `cloud_api_version: "v2"` | Regenerate the route draft with the v2 prefix and update consumers. | API product owner |

Each scenario also declares affected paths:

| Scenario | Affected paths |
|---|---|
| APD naming | `config/codegen/`, `product/template/` |
| App Events v2 | `config/appevents/` |
| Gateway mTLS | `config/cloudapi/`, `config/appevents/` |
| Gosu API removal | `gsrc/`, `java/`, `plugins/` |
| Cloud API version | `config/cloudapi/` |

**Implementation coverage.** Only the APD scenario has an implemented *effective
constraint* that changes refactor generation (`apd_limit=20`). The other four are
impact simulators: their scenario checks run against the existing bundle and
report the affected drafts, but the current generator does not emit the new
envelope, mTLS block, replacement API, or v2 prefix automatically. A re-run of
those four will still be `revalidation_required` until the generator and the
human-owned refactor are updated. This is a feature of the prototype, not a
claim that a one-click re-run fixes a release change.

---

## 2. Generation and checkpoint semantics

### 2.1 Generation is a logical assessment vintage

A codebase result starts with:

```json
{"generation": 1, "status": "green_with_human_gates", "green_signal": {"unified": true}}
```

An upgrade event proposes the next generation:

```json
{
  "event_id": "UP-002",
  "active_assessment_generation": 1,
  "new_generation": 2,
  "from_version": "GWCP 2026.10",
  "to_version": "GWCP 2027.04",
  "invalidates_green": true,
  "status": "revalidation_required"
}
```

`event_id` is `UP-{new_generation:03d}`. A baseline at generation 1 therefore
produces `UP-002`, not `UP-001`. The event is hashed.

A generation is **not** a Git branch, a copied directory, or a physical snapshot.
It is a label that ties an assessment result to the rule pack and effective
constraints it was evaluated against. The sealed bundle remains the artifact of
record for the prior generation.

### 2.2 `evaluate_upgrade()` is read-only

`evaluate_upgrade(result, scenario_id)`:

1. resolves the scenario (unknown ID → `KeyError`);
2. matches patches by affected rule ID **or** affected path prefix;
3. runs scenario-specific checks;
4. computes `failed = [check for check in checks if not check["ok"]]`;
5. computes `green = result.green_signal.unified`;
6. sets `status = "revalidation_required"` if any check failed, otherwise
   `"compatible"`;
7. sets `invalidates_green = bool(green and failed)`;
8. returns `green_signal_before`, `green_signal_after`, affected patches/rules,
   checks, required actions, resume options, and the hashed event.

It does **not** mutate the result and does **not** change the persisted generation.
This makes it safe to preview an upgrade before a reviewer chooses a resume path.

### 2.3 `apply_upgrade_policy()` persists the generation change

`apply_upgrade_policy(result, scenario_id)` deep-copies the result and:

- sets `generation = new_generation`;
- replaces `green_signal` with `green_signal_after`;
- sets `status = "revalidation_required"` when the impact requires revalidation;
- stores the full impact under `upgrade`;
- appends a `resilience / upgrade.detected` event to the audit list;
- recomputes `audit_verified` and `audit_detail`.

It still does not regenerate patches or approve anything.

### 2.4 `resume_assessment()` records the human choice

`resume_assessment(result, impact, choice)`:

- accepts only a choice present in `impact.resume_options`;
- sets `generation = impact.new_generation`;
- records `resume.choice`, `resume.label`, `resume.recorded_at`, and
  `resume.requires_human_approval: true`;
- for any choice other than `retain`, clears `green_signal.unified` and writes a
  reason that the affected Architect pass must be re-run;
- maps the status:

| Choice | Resulting status | Green signal |
|---|---|---|
| `revalidate` | `resume_requested` | Cleared |
| `rollback` | `rolled_back_to_checkpoint` | Cleared |
| `defer` | `upgrade_deferred` | Cleared |
| `retain` | unchanged (`compatible` path only) | Retained with revalidation note |

It appends `resilience / upgrade.resume.{choice}` to the audit. It does **not**
run Architect, restore files, or approve the migration.

### 2.5 What “checkpoint” means here

The checkpoint is the sealed bundle plus its audit chain. The code does not copy
a checkpoint directory, and `rollback` does not restore one. It records that the
reviewer chose to keep the sealed bundle and resume after the release stabilizes.
The prior bundle must still exist; PreFlight does not garbage-collect it for you.

A separate source-generation rule applies to scanning: if the source tree hash
changes during a scan, `guarded_scan()` refuses to mix generations and returns
`source_changed`. That is a source-immutability check, not the release-generation
counter.

---

## 3. Stale-green invalidation

### 3.1 The rule

A green signal is **stale** when all of the following hold:

1. the bundle was previously `green_signal.unified == true`;
2. at least one scenario check fails.

The result is:

```json
{
  "status": "revalidation_required",
  "green_signal_before": {
    "unified": true, "guardian": true, "critic": true, "planner": true
  },
  "green_signal_after": {
    "unified": false, "guardian": false, "critic": false, "planner": false,
    "reason": "stale after core release upgrade"
  },
  "event": {"invalidates_green": true}
}
```

`guardian`, `critic`, and `planner` are set false even though the previous
artifacts still say they passed. The after-signal describes the current
release-validity state, not a re-run of the historical agents.

If the bundle was already red, `green_signal_after.unified` remains false; an
upgrade cannot turn a red bundle green merely by being detected.

### 3.2 What is not invalidated

- The sealed plan, report, target files, manifest, and audit log remain on disk.
- Historical check results remain in the result for traceability.
- Human gates remain open and are not auto-resolved.
- The source snapshot is unchanged by an upgrade event.

Invalidation is a validity decision, not a deletion.

### 3.3 Run-time upgrade path

`run_code_migration(..., upgrade_scenario=...)` evaluates the scenario after the
normal loop. On failure it:

- sets `status = "revalidation_required"`;
- sets `green_signal.unified/guardian/critic = false`;
- writes a reason that the upgrade invalidated the green signal;
- appends `resilience / upgrade.invalidated-green` to the audit.

For the APD scenario it also passes `effective_apd_limit=20` into the refactor,
so a fresh run can be genuinely compatible. That is a **new assessment**, not a
reuse of the old green signal.

### 3.4 Observed impact on the Cascade baseline

Baseline: `generation=1`, unified green, 22 patches.

| Scenario | Status | Affected patches | First failing check |
|---|---|---|---|
| APD naming | `revalidation_required` | 2 (`CP-015`, `CP-018`) | 1 override exceeds 20 characters |
| App Events v2 | `revalidation_required` | 3 (`CP-001`, `CP-007`, `CP-016`) | 1 publication draft still uses the v1 envelope |
| Gateway mTLS | `revalidation_required` | 7 | 7 route drafts only declare service-user auth |
| Gosu API removal | `revalidation_required` | 14 | 1 target draft depends on a removed API family |
| Cloud API version | `revalidation_required` | 4 | 4 route drafts still advertise the v1 prefix |

All five scenarios have at least one failing check on the baseline, so all five
invalidate green. A fresh APD run at the 20-character limit is the only scenario
that reaches `compatible` in the current implementation.

---

## 4. Resume options

| Option | Label | Safe | Recommended | Status after resume | Meaning |
|---|---|---|---|---|---|
| `revalidate` | Re-run Architect with the new rule pack | yes | yes (failed path) | `resume_requested` | Regenerate the affected drafts, then re-run Guardian/Critic. The resume record itself does not run them. |
| `rollback` | Roll back to the last green checkpoint | yes | no | `rolled_back_to_checkpoint` | Keep the sealed bundle and resume after the release stabilizes. No files are restored. |
| `defer` | Defer the upgrade and pin the assessment release | yes | no | `upgrade_deferred` | Record the risk owner and revisit before go-live. |
| `retain` | Retain the green bundle with a revalidation note | yes | only when compatible | unchanged | Offered only when no check failed. It is not available on the failed path. |

All four record `requires_human_approval: true`. None approves a patch.

---

## 5. Unexpected-input playbook

`resilience_drills()` exposes these to the page and `GET /api/codebase/cases`.
They are named states, not crashes.

| Kind | Detection | Handling | Recovery |
|---|---|---|---|
| `source-changed` | Tree hash before and after the scan differs. | Abort the pass; keep the previous target bundle; status `source_changed`. | Import a fresh snapshot and re-run Scout; never mix evidence from two source generations. |
| `corrupt-file` | UTF-8/read failure or unparseable XML/Gosu. | List the file as quarantined with the parser error; continue scanning the rest. | Fix or explicitly exclude the file, then re-run the affected rule families. |
| `duplicate-target` | Two patches write the same target path. | Guardian path check blocks the bundle; the second patch is marked for review. | Split the change into separate packages or choose one owner. |
| `analyzer-crash` | The guarded scanner catches an unexpected exception. | Return `analyzer_failed` with the error; do not emit green. | Re-run with a smaller file cap or quarantine the triggering file. |
| `empty-snapshot` | Zero supported source files scanned. | Return `insufficient_evidence`; do not fabricate findings or a score. | Confirm the archive layout and re-import. |

The playbook's phrase “last good checkpoint” is conceptual: the code preserves
the last successful result it has, not a separate checkpoint archive. If no good
result exists, the state is explicitly failed or insufficient.

---

## 6. Codebase demo flow

### 6.1 Start the product

```bash
cd /home/understressengineer/programming/Preflight-CloudMigration/v2
make demo
```

This seeds `R-DEMO-001` and starts the local server. Open:

- `http://127.0.0.1:8000/case-studies`
- `http://127.0.0.1:8000/codebase?case=cascade-mutual`
- `http://127.0.0.1:8000/codebase?case=harbor-pc`
- `http://127.0.0.1:8000/migrator?run=R-DEMO-001`

The codebase result is computed on first request and cached in process. The
`upgrade` query parameter previews an impact without persisting it:

```text
http://127.0.0.1:8000/codebase?case=cascade-mutual&upgrade=GWCP-APD-NAMING-2027.04
```

### 6.2 The loop you should see

| Pass | Cascade Mutual | Harbor P&C |
|---|---|---|
| Scout | 17 files, 156 LOC, 18 findings, 5 feature slices | 15 files, 160 LOC, 20 findings, 6 feature slices |
| Architect 1 (error-first) | 16 patches, 7 config drafts | 17 patches, 8 config drafts |
| Guardian 1 | `rework`, 11/13 | `rework`, 11/13 |
| Critic 1 | 4/7, 2 fix requests | 4/7, 2 fix requests |
| Architect 2 (full) | 22 patches, 7 config drafts | 21 patches, 8 config drafts |
| Guardian 2 | `green`, 13/13 | `green`, 13/13 |
| Critic 2 | `green`, 7/7 | `green`, 7/7 |
| Human gates | 10 | 11 |
| Status | `green_with_human_gates` | `green_with_human_gates` |

The first pass is intentionally red: it addresses errors only, so warnings remain.
The second pass addresses errors and warnings and reaches green. A one-iteration
run stops `blocked`; it does not fake a green.

### 6.3 CLI: baseline, red stop, and upgrade

```bash
# Green baseline, two iterations
.venv/bin/python -m app.cli codebase cascade-mutual --iterations 2 \
  --out /tmp/preflight-cascade

# Multi-line case
.venv/bin/python -m app.cli codebase harbor-pc --iterations 2 \
  --out /tmp/preflight-harbor

# Red stop: no false green
.venv/bin/python -m app.cli codebase cascade-mutual --iterations 1 \
  --out /tmp/preflight-cascade-red

# Stale-green demo: App Events v2 invalidates the prior green
.venv/bin/python -m app.cli codebase cascade-mutual --iterations 2 \
  --upgrade GWCP-APP-EVENTS-V2-2027.04 \
  --out /tmp/preflight-cascade-appevents

# APD re-run at the effective 20-character limit: compatible
.venv/bin/python -m app.cli codebase cascade-mutual --iterations 2 \
  --upgrade GWCP-APD-NAMING-2027.04 \
  --out /tmp/preflight-cascade-apd20
```

Expected terminal lines:

```text
cascade-mutual: green_with_human_gates · 18 findings · 22 patches · green=True
harbor-pc: green_with_human_gates · 20 findings · 21 patches · green=True
cascade-mutual: blocked · 18 findings · 16 patches · green=False
cascade-mutual: revalidation_required · 18 findings · 22 patches · green=False
cascade-mutual: green_with_human_gates · 18 findings · 22 patches · green=True
```

The CLI exits non-zero whenever `green_signal.unified` is false. The red-stop and
App Events commands therefore return 1; the green baseline and APD command
return 0.

### 6.4 API flow

Start the server and prepare a session/CSRF token as in `LIVE-AGENTS.md`:

```bash
BASE=http://127.0.0.1:8000
JAR=/tmp/preflight-cookies.txt
HTML=$(curl -s -c "$JAR" "$BASE/codebase?case=cascade-mutual")
TOKEN=$(printf '%s' "$HTML" | sed -n 's/.*name="csrf-token" content="\([^"]*\)".*/\1/p')
```

Preview an upgrade (no mutation):

```bash
curl -s -b "$JAR" -H "X-CSRF-Token: $TOKEN" \
  -H 'Content-Type: application/json' \
  -d '{"scenario_id":"GWCP-APD-NAMING-2027.04"}' \
  "$BASE/api/codebase/cases/cascade-mutual/upgrade"
```

Record a resume choice:

```bash
curl -s -b "$JAR" -H "X-CSRF-Token: $TOKEN" \
  -H 'Content-Type: application/json' \
  -d '{"scenario_id":"GWCP-APD-NAMING-2027.04","choice":"rollback"}' \
  "$BASE/api/codebase/cases/cascade-mutual/resume"
```

Expected `result.status`: `rolled_back_to_checkpoint`; `green_signal.unified`
false; `resume.requires_human_approval` true.

Other useful GETs:

```bash
curl -s "$BASE/api/codebase/cases" | jq
curl -s "$BASE/api/codebase/cases/cascade-mutual" | jq '.status, .green_signal'
curl -s "$BASE/api/codebase/cases/cascade-mutual/audit" | jq '.verified, .detail'
curl -s "$BASE/api/codebase/cases/cascade-mutual/sarif" -o /tmp/cascade.sarif
```

All POST routes require the CSRF token. GET routes do not.

### 6.5 Library flow

```python
from app.config import Settings
from app.services.code_migration import run_code_migration, verify_code_audit
from app.services.resilience import (
    evaluate_upgrade,
    apply_upgrade_policy,
    resume_assessment,
)

result = run_code_migration("cascade-mutual", Settings(), max_iterations=2)
impact = evaluate_upgrade(result, "GWCP-APD-NAMING-2027.04")

print(result["generation"])                 # 1
print(impact["new_generation"])             # 2
print(impact["status"])                     # revalidation_required
print(impact["green_signal_after"]["unified"])  # False

updated = apply_upgrade_policy(result, "GWCP-APD-NAMING-2027.04")
print(updated["generation"])                # 2
print(updated["green_signal"]["unified"])   # False

resumed = resume_assessment(result, impact, "revalidate")
print(resumed["status"])                    # resume_requested
print(resumed["resume"]["requires_human_approval"])  # True

print(verify_code_audit(resumed["audit"]))  # (True, "16 events verified")
```

`apply_upgrade_policy` and `resume_assessment` append audit events. The lab's
`verify_code_audit()` reports the chain correctly; see the caveat in section 7.

### 6.6 Commands to verify behavior

```bash
.venv/bin/python -m pytest tests/test_codebase.py -q
.venv/bin/python -m pytest tests/test_agent_experience.py -q
```

The codebase tests cover the two-pass loop, one-iteration red stop, APD effective
limit, every scenario invalidation, resume status mapping, audit tamper detection,
SARIF, and the unexpected-scenario playbook.

---

## 7. Known implementation caveats

These are current behaviors, not design intent. They matter when you demo or
extend the lab.

1. **The CLI’s `--upgrade` run keeps `generation: 1` in the returned artifact.**
   `run_code_migration()` stores the impact event (`new_generation: 2`) but does
   not assign `result["generation"] = 2`. `apply_upgrade_policy()` and
   `resume_assessment()` do assign it. Treat the event as the proposed next
   generation and the result field as the generation of the artifact that was
   evaluated.

2. **The API preview is not persisted.** `POST /upgrade` returns a computed
   impact against the cached result; it does not mutate the cache. `POST /resume`
   returns an updated copy; it also does not replace the cached result. A
   subsequent `GET` can show the baseline again. For a durable state, persist the
   returned object or re-run with the scenario.

3. **`resume_assessment()` and `apply_upgrade_policy()` report
   `audit_verified: false` even when the chain is valid.** The lab’s
   `verify_code_audit()` canonicalizes JSON with `ensure_ascii=False`, while
   `resilience._verify_chain()` uses the default `ensure_ascii=True`. Existing
   audit reasons contain `·` and `→`, so the two hashes differ.
   `verify_code_audit(resumed["audit"])` returns `True` and “16 events verified.”
   Use that verifier, and do not present the resilience boolean as proof of
   tampering.

4. **`rollback` is a state label, not a restore.** No checkpoint directory is
   copied and no target file is rewritten. The sealed bundle must already exist.

5. **Only APD has an effective constraint.** The other four scenarios detect and
   report impact but do not auto-generate the new contract. Re-running them is
   expected to remain `revalidation_required`.

6. **`affected_rules` is derived from matched patches, not simply copied from the
   scenario declaration.** A patch can match by path without carrying the
   scenario’s rule ID; read `affected_patches` and `affected_rules` together.

7. **`retain` is unavailable on the failed path.** The option list contains only
   `revalidate`, `rollback`, and `defer`; `retain` appears only when the impact is
   `compatible`.

8. **A generation bump does not re-run anything.** It changes validity metadata.
   Only a new Architect/Guardian/Critic pass can produce a new green signal.

---

## 8. Operational checklist

- [ ] Freeze the source snapshot; confirm the tree hash before and after the scan.
- [ ] Confirm the scenario ID and effective constraint.
- [ ] Preview with `evaluate_upgrade()`; do not assume a green survives.
- [ ] Record the previous green signal and generation.
- [ ] Confirm the affected patches and rules, not just the scenario label.
- [ ] Choose `revalidate`, `rollback`, or `defer`; record an owner.
- [ ] Re-run the affected Architect pass; do not claim green from a resume record.
- [ ] Re-run Guardian and Critic; keep every patch `pending`.
- [ ] Verify the audit chain with `verify_code_audit()`.
- [ ] Re-check the sealed bundle and human gates before go-live.

---

## 9. Boundary

Upgrade resilience is a **release-change simulation over a synthetic estate**. It
does not monitor a live Guidewire release, contact a tenant, regenerate production
endpoints, restore a checkpoint, or approve a migration. The five scenarios are
modelled, not published release commitments. A green signal is a bounded machine
verdict with open human gates; a resumed assessment is a recorded decision, not a
deployment. Official Cloud Assurance was not run.
