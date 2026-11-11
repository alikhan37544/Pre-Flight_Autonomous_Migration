# Live agents: configuration, grounding, and operations

Live reasoning is an **optional annotation layer** over PreFlight's deterministic
agents. The product never needs it. When enabled, Scout, Architect, and Critic may
ask an OpenAI-compatible endpoint for a grounded narrative; Guardian never calls a
model, and no model output can create a gate, change a check, approve a patch, or
alter a package.

This document contains **no API key**. Credentials are read from the environment
only and are never written to the run store, the plan, the report, or an API
response.

---

## 1. Where the model is called

| Loop | Agent | Calls per run | What the model receives | What it can change |
|---|---|---|---|---|
| Feature migrator | Scout | 1 | Feature summary, up to 12 evidence records, findings, allowlists | `llm.annotations.scout` only |
| Feature migrator | Architect | 1 | Package metadata and evidence IDs | `llm.annotations.architect` only |
| Feature migrator | Critic | 1 | Packages, gates, deterministic checks, allowlists | `llm.annotations.critic` only |
| Feature migrator | Guardian | **0** | Nothing | Nothing |
| Feature migrator | Scribe | **0** | Nothing | Nothing |
| Codebase lab | Critic | 1 | Patch/package metadata, gates, checks, allowlists | `llm.annotations.critic` only |
| Codebase lab | Scout, Architect, Guardian, Planner | **0** | Nothing | Nothing |

Maximum per feature migration: **3 calls**. Maximum per codebase run: **1 call**.
Failures are independent; a failed Scout annotation does not stop Architect or
Critic from being called.

---

## 2. Environment variables

| Variable | Required | Default | Behavior |
|---|---|---|---|
| `PREFLIGHT_LLM_MODE` | Yes, to enable live | `off` | Only `off` and `live` are accepted; any other value becomes `off`. `--live` alone is not enough — the mode must be `live`. |
| `PREFLIGHT_LLM_BASE_URL` | Yes, when live | empty | Trailing slash is stripped; the client posts to `{base_url}/chat/completions`. The host is shown in status; the full URL is not treated as a secret. |
| `PREFLIGHT_LLM_API_KEY` | Yes, when live | empty | Sent as `Authorization: Bearer …`. Never returned by `LLMConfig.public()`, never written to the plan/report, never logged by the application. |
| `PREFLIGHT_LLM_MODEL` | No | `mimo-v2.6-flash` | Must be `mimo-v2.6-flash` or `mimo-v2.6-pro`. An invalid environment value silently falls back to Flash; an invalid explicit request raises `unsupported_model`. |
| `PREFLIGHT_LLM_TIMEOUT` | No | `45` seconds | Clamped to **5–120** seconds. Applies to each HTTP attempt. |
| `PREFLIGHT_LLM_ALLOW_REAL_CODE` | No | `false` | Operator acknowledgement shown in Settings. It does **not** automatically classify or block real code. See section 7. |
| `PREFLIGHT_LLM_FALLBACK_MODEL` | No | not read by code | Present in `.env.example`, but **no fallback logic uses it**. There is no automatic Flash→Pro fallback. |

`configured` is true only when **all three** are true:

```text
PREFLIGHT_LLM_MODE=live
PREFLIGHT_LLM_BASE_URL is non-empty
PREFLIGHT_LLM_API_KEY is non-empty
```

`GET /api/llm/status` returns `mode`, `configured`, `base_host`, `models`,
`default_model`, `allow_real_code`, `reason`, and `provider` — never the key.

Recommended `.env` shape (values supplied by the operator, not committed):

```dotenv
PREFLIGHT_LLM_MODE=live
PREFLIGHT_LLM_BASE_URL=<operator-supplied OpenAI-compatible base URL>
PREFLIGHT_LLM_API_KEY=<set-in-environment>
PREFLIGHT_LLM_MODEL=mimo-v2.6-flash
PREFLIGHT_LLM_TIMEOUT=45
PREFLIGHT_LLM_ALLOW_REAL_CODE=false
```

`.env` is gitignored. Do not put a key in `.env.example`, a test, a document, a
screenshot, or a shell argument that is captured in history.

---

## 3. Model IDs and request shape

| Model ID | Role in PreFlight | Default |
|---|---|---|
| `mimo-v2.6-flash` | Lower-latency annotation; default for the demo | Yes |
| `mimo-v2.6-pro` | Higher-capability annotation for harder narratives | No |

The allowlist is fixed in `app/services/llm.py`; no arbitrary model string is
accepted.

**Request:**

- `POST {base_url}/chat/completions`
- `Authorization: Bearer <key>`
- JSON body: `model`, `messages`, `temperature: 0.1`, `max_tokens: 1200`,
  `response_format: {"type": "json_object"}`
- prompt size cap: **48,000 characters** of serialized messages
- two attempts per call; a 0.4-second pause between attempts
- no streaming, no tool/function calling, no model-directed URL

**Response handling:** the client reads `choices[0].message.content`, tolerates a
fenced code block, extracts the first `{` through the last `}`, and requires a JSON
object. It records `model`, `usage`, `latency_ms`, `prompt_sha256`,
`response_sha256`, and `generated_at`.

The endpoint is operator-supplied and must be OpenAI-compatible. PreFlight does
not bundle a provider, a base URL, or a credential.

---

## 4. Mode behavior

| Situation | Feature migrator | Codebase lab | UI / API surface |
|---|---|---|---|
| `mode=off` | Deterministic pass; no calls; `llm.status=off` | Deterministic pass; no calls; `llm.status=off` | Live controls hidden; `GET /api/llm/status` says offline. |
| `mode=live`, URL + key set, default model | 3 annotation attempts; `llm.status=active` if any annotation succeeds | 1 Critic annotation; `status=active` on success | Live badge with model ID. |
| `mode=live`, URL or key missing | `run_migration()` raises `LLMError(not_configured)` before writing state | Full deterministic run completes; `llm.status=failed` plus a `not_configured` warning | Feature API returns **409**; codebase API still returns the result. |
| `--live` but mode `off` | Same `not_configured` error | Deterministic result with warning | The mode flag, not the CLI flag, is authoritative. |
| Explicit unsupported model in CLI | `argparse` rejects it (choices) | `argparse` rejects it | — |
| Explicit unsupported model in API/body | `resolve_model()` raises `unsupported_model` | Same | Send only the two allowlisted IDs. |
| All annotations fail | `llm.status=degraded`; warnings and failed calls recorded; deterministic artifacts remain | `llm.status=degraded`; warning recorded | The bundle is still produced. |
| Some annotations fail | `llm.status=degraded` if not all three succeeded | `degraded` | Per-call status is in `llm.calls`. |

**Important:** the feature migrator checks configuration *before* the run; the
codebase lab checks it *after* the deterministic loop and records a warning. This
asymmetry is intentional in the current code and visible in the API behavior.

---

## 5. Grounding validation

Each role has a fixed system prompt in `_SYSTEM_PROMPTS` and a JSON schema in the
prompt. After the call, `validate_migration_annotation()` filters the response
against allowlists derived from the deterministic artifacts.

| Kind | Required grounding | Post-filter behavior |
|---|---|---|
| Scout | Every observation needs at least one `evidence_id` from `allowed_evidence_ids`. | Observations with no allowed ID, no text, or a non-object shape are dropped. IDs are capped at 6 per observation; text at 500 characters. `headline` and `unknowns` are retained without citation checks. |
| Architect | Each package must name a `package_id` from `allowed_package_ids`. | Unknown package IDs are dropped. Rationale is capped at 600 characters, risk at 20, test at 400. The schema does **not** request per-package evidence IDs, so package rationales are package-grounded, not evidence-cited. |
| Critic | Each trade-off needs at least one `rule_id` from `allowed_rule_ids`. | Trade-offs with no allowed rule ID or no text are dropped. Residual risks are free text with an owner (default `human reviewer`). `allowed_package_ids` is supplied, but the Critic branch does not enforce package IDs. |
| Codebase Critic | Same Critic schema; patch IDs act as package IDs, finding IDs as evidence IDs, patch rule IDs as rules. | Same filtering. The annotation is advisory and never changes Guardian/Critic checks. |

Every annotation carries `dropped_ungrounded`, the number of statements removed.
A non-zero count is a quality signal, not a run failure.

**What grounding does not prove.** ID allowlisting prevents invented identifiers;
it does not prove that a sentence is true, complete, or semantically entailed by
the cited record. A model can cite a valid evidence ID and still misdescribe it.
`headline`, `unknowns`, Architect rationales, and Critic residual risks are not
fully citation-gated. Treat the narrative as a reading aid, never as evidence.

**Deterministic isolation.** Guardian and Critic checks are computed before or
independently of the annotation. The annotation cannot:

- add, remove, or reorder packages;
- add, remove, or resolve gates;
- change a check from PASS to FAIL or FAIL to PASS;
- change `approval` from `pending`;
- change the green signal or the deterministic package/gate/check payload.

The plan records annotations when live, so an annotation changes the plan bytes
and therefore the plan/bundle SHA-256 values. It does not change the
deterministic sections that a reviewer must rely on.

---

## 6. Prompt injection and security

| Asset / threat | Control | Residual risk |
|---|---|---|
| Source excerpt contains instructions (“ignore previous instructions…”) | Model has no tools; the request contains no function calling; output is parsed as JSON and filtered by allowlists. Guardian never reads model text. | The narrative can still be misleading within valid IDs. A human must not treat it as evidence. |
| Model output tries to act as an instruction | Output is data only. No shell, filesystem, network, or deployment capability is exposed to the model. | None beyond misleading prose. |
| Secrets in prompts | Excerpts are redacted at capture (`[REDACTED:<fingerprint>]`); secret values are not persisted. The codebase annotation sends IDs, paths, statuses, and summaries, not raw source text. | Redaction is pattern-based; do not send real code without approval. |
| API key disclosure | Environment-only; `public()` omits it; no key in plan/report/logs; tests assert no hardcoded key or base URL in `app/`. | Operator must protect `.env`, shell history, and process environment. |
| Arbitrary endpoint / SSRF | Only the operator-configured `base_url` is called; the model cannot choose a URL. | A malicious operator-supplied endpoint can receive the prompt. |
| Cross-origin mutation / CSRF | Local host/origin allowlist; signed session cookie; synchronizer CSRF token on POST; `SameSite=Strict`; CSP. | The product is single-user and unauthenticated by design. Do not expose it to a network. |
| Prompt/cost exhaustion | 48k-character prompt cap; 1,200 completion tokens; 45s default timeout; two attempts; no streaming. | A slow endpoint can still consume the configured timeout budget. |
| Model error causing a false green | Live errors only degrade the annotation status; deterministic gates are unaffected. | None for the machine verdict; the run may be less informative. |

The app binds to `127.0.0.1`, has no authentication, and is a local single-user
workstation. Live mode adds one outbound HTTPS call per annotation (up to three
per feature run, one per codebase run) to the configured endpoint; there is no
telemetry, tenant connection, or other egress.

---

## 7. Synthetic-only policy

PreFlight's fixtures, case studies, and demo run are synthetic. The live path is
designed for that material.

- **Default:** `PREFLIGHT_LLM_ALLOW_REAL_CODE=false`. The Settings page displays
  `synthetic only`.
- **Policy:** do not enable live mode for customer source, tenant data,
  credentials, personal data, or anything covered by a confidentiality agreement
  unless the data owner, security, and legal have approved the endpoint and the
  data flow.
- **What the flag is:** an operator acknowledgement. It is read and displayed,
  but it does not inspect content, redact files, or block a run. It is not a
  data-loss-prevention control.
- **What is sent:** the feature migrator sends up to 12 evidence excerpts
  (300 characters each), finding metadata, package metadata, gates, and checks.
  The codebase lab sends patch IDs, target paths, approval states, finding IDs,
  rule IDs, gates, and checks — not Gosu/Java source text.
- **What is never sent by PreFlight:** API keys, tenant credentials, the review
  packet, raw secret values, or files outside the selected fixture.

If real-code review is ever approved, treat the endpoint as a data processor and
document retention, residency, and access controls outside this repository.

---

## 8. Failure and fallback

| Code | Trigger | Behavior |
|---|---|---|
| `not_configured` | Mode not live, or base URL/key missing | Feature migrator raises before the run; codebase records a warning and returns the deterministic result. |
| `unsupported_model` | Explicit model is not in the allowlist | `LLMError`; no call is made. |
| `prompt_too_large` | Serialized messages exceed 48,000 characters | `LLMError`; no call is made. |
| `http_error` | Endpoint returns HTTP ≥ 400 | Retried once; then `LLMError` with status. |
| `empty_response` | No `choices` array | Retried once; then `LLMError`. |
| `invalid_json` | Content has no JSON object or is not parseable | Retried once; then `LLMError`. |
| `request_failed` | Network/timeout exception after retries | `LLMError` with a sanitized message. |
| `unknown_kind` | Internal annotation kind is not Scout/Architect/Critic | `LLMError`; programming error. |

**Fallback policy:** there is **no automatic model fallback**. The
`PREFLIGHT_LLM_FALLBACK_MODEL` line in `.env.example` is currently unused. To use
Pro after a Flash failure, rerun explicitly:

```bash
.venv/bin/python -m app.cli migrate R-DEMO-001 --live --model mimo-v2.6-pro
```

The deterministic path remains available during any live outage. A degraded
annotation never blocks the offline bundle, and an ungrounded citation is dropped
rather than treated as a fatal error.

---

## 9. CLI and API

### CLI

| Command | Purpose |
|---|---|
| `.venv/bin/python -m app.cli llm-check` | Read status; if configured, make one tiny JSON call and print model/latency/tokens. |
| `.venv/bin/python -m app.cli llm-check --model mimo-v2.6-pro` | Same with Pro. |
| `.venv/bin/python -m app.cli migrate R-DEMO-001 --live` | Run the feature migrator with the default model. |
| `.venv/bin/python -m app.cli migrate R-DEMO-001 --live --model mimo-v2.6-flash` | Explicit Flash. |
| `.venv/bin/python -m app.cli codebase cascade-mutual --iterations 2 --live --model mimo-v2.6-flash --out ./codebase/cascade-live` | Run the lab with one Critic annotation. |

`llm-check` exits 1 when not configured or when the live check fails. The
`codebase` command exits non-zero only when the green signal is not unified.

### API

| Method | Path | Notes |
|---|---|---|
| `GET` | `/api/llm/status` | Public, no CSRF; returns configuration without the key. |
| `POST` | `/api/llm/check` | CSRF required; **409** if not configured, **502** on `LLMError`. |
| `GET` | `/api/runs/{run_id}/migration` | Current state, including the `llm` block. |
| `POST` | `/api/runs/{run_id}/migration` | Body `{"feature_id": "...", "live": true, "model": "mimo-v2.6-flash", "force": true}`; **409** if live is requested but not configured. |
| `POST` | `/api/codebase/cases/{case_id}/run` | Body `{"max_iterations": 2, "live": true, "model": "mimo-v2.6-flash"}`; returns a result with `llm.status=failed` if not configured, rather than 409. |

POSTs need the session cookie and the CSRF token from the page's
`<meta name="csrf-token">`. A safe local sequence:

```bash
BASE=http://127.0.0.1:8000
JAR=/tmp/preflight-cookies.txt
HTML=$(curl -s -c "$JAR" "$BASE/migrator?run=R-DEMO-001")
TOKEN=$(printf '%s' "$HTML" | sed -n 's/.*name="csrf-token" content="\([^"]*\)".*/\1/p')

curl -s -b "$JAR" -H "X-CSRF-Token: $TOKEN" \
  -H 'Content-Type: application/json' \
  -d '{"feature_id":"PA-VEH-01","live":true,"model":"mimo-v2.6-flash","force":true}' \
  "$BASE/api/runs/R-DEMO-001/migration"
```

Never put the CSRF token or API key in a query string.

---

## 10. Cost and latency expectations

PreFlight does not bundle pricing. Cost is the provider's price for the tokens in
`usage`; the application records `prompt_tokens`, `completion_tokens`,
`total_tokens` when the endpoint returns them.

| Dimension | Bound |
|---|---|
| Calls per feature migration | 3 (Scout, Architect, Critic) |
| Calls per codebase run | 1 (Critic) |
| Prompt ceiling | 48,000 characters per call (roughly 12k tokens at 4 characters/token; this is an approximation, not a tokenizer result) |
| Completion ceiling | 1,200 tokens per call |
| Feature-run ceiling | ~36k prompt tokens + 3.6k completion tokens in the absolute worst case |
| Timeout | 45s default per attempt; 5–120s configurable |
| Retries | One retry after 0.4s; worst case two attempts per call |
| Worst-case wall clock | ~270s for 3 calls at the 45s default, ~90s for 1 call; scales with the configured timeout |
| Streaming | None |
| Cache | None; each rerun calls again |

The deterministic work itself is local and takes seconds. Live latency is
dominated by the endpoint. Measure it rather than guessing:

```bash
.venv/bin/python -m app.cli llm-check --model mimo-v2.6-flash
```

The command prints `latency_ms` and `total_tokens`. Per-call latency and usage
are also stored in `llm.calls` inside the migration result.

---

## 11. How to test

### Offline contract tests

```bash
.venv/bin/python -m pytest tests/test_agent_experience.py -q
.venv/bin/python -m pytest tests/test_codebase.py -q
```

`tests/test_agent_experience.py` covers:

- environment-only configuration and key non-disclosure;
- `configured == false` when URL/key are missing;
- OpenAI-compatible URL, Bearer header, usage parsing, and response hash via
  `httpx.MockTransport`;
- dropping an invented evidence ID (`dropped_ungrounded == 1`);
- no hardcoded MiMo key or base URL in `app/`;
- `.env.example` contains the variable names but no secret.

### Live smoke test (synthetic fixtures only)

```bash
set -a
. ./.env
set +a

.venv/bin/python -m app.cli llm-check --model mimo-v2.6-flash
.venv/bin/python -m app.cli migrate R-DEMO-001 --live --model mimo-v2.6-flash
.venv/bin/python -m app.cli codebase cascade-mutual --iterations 2 \
  --live --model mimo-v2.6-flash --out /tmp/preflight-cascade-live
```

Then verify the deterministic chain is intact:

```bash
.venv/bin/python -m app.cli verify-migration R-DEMO-001
.venv/bin/python - <<'PY'
import json
state = json.load(open("data/runs/R-DEMO-001/migration.json"))
print(state["llm"]["status"], state["llm"]["model"])
print("warnings:", state["llm"].get("warnings", []))
print("annotations:", sorted(state["llm"].get("annotations", {})))
PY
```

Expected live result: `llm.status` is `active` when all three annotations succeed,
`degraded` when at least one fails. The deterministic verdict is unchanged in
either case.

### Negative checks

- Unset `PREFLIGHT_LLM_API_KEY` and run `llm-check`: expects exit 1 and a
  `PREFLIGHT_LLM_API_KEY is not set` reason.
- Set `PREFLIGHT_LLM_MODE=off` and run `migrate --live`: expects
  `not_configured`.
- Return an invented evidence ID from a mock model: the observation is dropped
  and `dropped_ungrounded` increments.
- Return malformed JSON: two attempts, then `invalid_json`; the deterministic
  bundle still exists.

---

## 12. Operational checklist

- [ ] `PREFLIGHT_LLM_MODE=live` is set intentionally.
- [ ] Base URL and key come from the environment, not a file in the repo.
- [ ] Model is `mimo-v2.6-flash` or `mimo-v2.6-pro`.
- [ ] Inputs are synthetic or explicitly approved for this endpoint.
- [ ] `PREFLIGHT_LLM_ALLOW_REAL_CODE` reflects the approval, not a guess.
- [ ] Timeout fits the provider and the review budget.
- [ ] `llm-check` succeeds before a demo.
- [ ] `llm.status`, `warnings`, `calls`, and `dropped_ungrounded` are reviewed.
- [ ] `verify-migration` passes; the deterministic bundle is authoritative.
- [ ] No key appears in logs, screenshots, plans, reports, or chat.

---

## 13. Boundary

Live reasoning is **commentary, not control**. It does not make PreFlight an LLM
product, an autonomous approver, or a tenant connector. Guardian is deterministic.
The green signal is a bounded machine verdict with open human gates. The sealed
bundle remains pending human approval. Official Cloud Assurance was not run.
