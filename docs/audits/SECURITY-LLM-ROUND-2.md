# Security & LLM Audit — Round 2

**Target:** PreFlight Cloud Migration, `v2/`  
**Commit:** `2d766ea` (`main`, `fork/main`)  
**Date:** 2026-11-11  
**Auditor stance:** independent security/LLM reviewer. I did not edit product code or tests. This report is the only repository file created. The live API key is deliberately **not reproduced anywhere in this report**; neither is its fingerprint.  
**Scope:** verification of the Round 1 fixes: credential removal/history, synthetic-only live mode, malformed provider responses, grounding/caps/injection, base-URL/SSRF, migration audit checkpoint, CLI bind guard, and general CSRF/Host/Origin/path-traversal/XSS/CSP controls.

**Method:** read-only review; exact-key scans of `HEAD`, every commit reachable from `HEAD`, the working tree, docs/PDF text and screenshot assets; `git fsck`, reflog and GitHub commit-existence checks; focused and full non-e2e pytest; `httpx.MockTransport` adversarial probes; one authorized real `preflight llm-check`; rendered-page probes. No product or test file was modified.

---

## 1. Verdict

**Conditional pass on the code fixes. Fail on credential remediation.**

Most of the Round 1 code changes are real and verified: uploaded runs receive a fast 409 and zero HTTP calls, malformed provider shapes degrade instead of crashing, grounding fails closed, response/item caps exist, userinfo/private literal endpoints are rejected, `trust_env=False` is set, the migration audit now has a checkpoint, and the CLI refuses non-loopback binds. CSRF, Host/Origin, path confinement, autoescaping, CSP and secret redaction still hold.

However, the live credential is **not remediated**. The current key was removed from the `HEAD` tree but is still present in commit `4527950`, which both configured GitHub repositories still serve by SHA (HTTP 200). The current key is byte-for-byte identical to the old test literal, and the one authorized `llm-check` succeeded — so the publicly retrievable old commit contains a **working** credential. The key was not rotated, old objects were not purged, and `.env` is still mode `0644`.

There is also a new high-impact behavioral gap: the synthetic-only gate trusts a mutable `fixture_id`. `preflight analyze --fixture demo-slice-300 --fixture-path <customer code>` labels customer code as a synthetic fixture, and `run_migration(..., live=True)` sent a customer marker in three prompts with `allow_real_code=False`. The `fixture_id="uploaded"` case is fixed; the broader policy is not.

**Overall security score: 6.8 / 10 — do not enable live mode in a release until the credential is rotated/purged and the synthetic gate is derived from immutable run metadata. The deterministic offline product is not blocked by these findings.**

---

## 2. Scorecard

| # | Category | Score | Rationale |
|---:|---|---:|---|
| 1 | Secret handling | **2/10** | `HEAD`, all commits reachable from `HEAD`, the working tree (excluding `.env`), docs and PDF text are key-free; `.env` is ignored. But the same live key remains in old commit `4527950` (publicly retrievable by SHA on both GitHub remotes), in an unreachable local blob, and in the fork reflog. No rotation. `.env` is `0644`. No secret scanner in CI. |
| 2 | Env config | **8/10** | Timeout parsing is now safe; live/local/real-code flags are parsed from env; malformed timeout no longer crashes. Residual: `PREFLIGHT_PORT` still uses bare `int()`, `.env` permissions are unchecked, and the fallback-model variable remains dead. |
| 3 | API auth / CSRF | **8/10** | CSRF synchronizer token, signed HttpOnly/SameSite=Strict cookie, exact Host/Origin checks still pass, including `/api/llm/check`. `/api/runs/{id}/migration` now 409s for uploaded runs. Residual: no authentication by design, `testserver` remains a production default host, and direct `uvicorn` can bypass the CLI bind guard. |
| 4 | SSRF | **5/10** | Userinfo, non-http(s), and literal private/loopback/link-local addresses are rejected; `trust_env=False`, `follow_redirects=False`, and `base_host` omits credentials. But numeric/octal/hex loopback forms (`2130706433`, `0x7f000001`, `0177.0.0.1`, `127.1`) are accepted and resolve to `127.0.0.1`; DNS names that resolve private (e.g. `*.nip.io`) are accepted; remote plaintext `http://` is accepted. |
| 5 | Prompt injection | **7/10** | System prompts now delimit evidence as untrusted data; instruction-like text is dropped from headline, unknowns, observations, package rationale/test, trade-offs and residual-risk text even with a valid citation. Model has no tools. Residual: regex heuristic is bypassable, and `risk`/`owner` metadata are not filtered. UI still labels annotations “grounded.” |
| 6 | Grounding | **8/10** | Per-list caps, empty package allowlists fail closed, residual risks require an allowed `rule_id`, dropped items are counted. Residual: no quote-substring check; headline and unknowns are uncited by design; “grounded” badge still overstates what was checked. |
| 7 | Synthetic-only enforcement | **4/10** | The exact `fixture_id="uploaded"` case is enforced at API and service boundaries (409, zero transport calls tested). But `is_synthetic_run()` trusts a mutable `fixture_id`; a custom CLI fixture labelled `demo-slice-300` (or `case-studies/...`) is treated as synthetic and its customer marker was sent in 3 prompts. |
| 8 | Error handling | **8/10** | Array/`choices=None`/`content=None`/invalid JSON/non-UTF-8/500/timeout all degrade safely; `/api/llm/check` returns sanitized 502. Residual: 4xx and validation errors are still retried; response-size cap is applied after the full body is read; no total deadline; invalid model still returns 200 then fails in a worker. |
| 9 | Redaction | **7/10** | Pipeline redaction is unchanged and still passes; prompts use persisted redacted evidence, not raw source. Pattern/taxonomy-based only; not a DLP control for arbitrary business text or PII. |
| 10 | Audit integrity | **7/10** | Empty, truncated, and wrong-run migration logs are rejected; `R-DEMO-001` verifies with 12 events. Residual: a fully rewritten log plus a rewritten checkpoint still verifies; the checkpoint is not sealed into or checked against the bundle manifest; the UI calls any seal mismatch “append-only grown,” even if the log shrank. |
| 11 | XSS / CSP | **9/10** | Jinja autoescape, no `|safe`, no `innerHTML`, `tojson` escaping, `textContent` in JS, strict CSP. Path traversal route still sound. |
| 12 | Test coverage | **8/10** | 506 non-e2e tests pass; 118 focused security/LLM tests pass. New tests cover the requested fixes. Gaps: no numeric/encoded-IP or DNS SSRF test, no mislabeled-fixture synthetic-gate test, no `risk`/`owner` injection test, no 401/429 retry-count test, no CI secret scanner, and the source-hygiene test scans only `app/`, not `tests/` or docs. |

**Average: 81 / 12 = 6.75 → 6.8/10.**

---

## 3. Verification of the eight requested fixes

| # | Requested check | Result | Evidence |
|---:|---|---|---|
| 1 | Key absent from tracked files/history reachable from `HEAD`; `.env` ignored; no key in docs/slides/screenshots | **PARTIAL (HEAD clean, remediation failed)** | `git grep` over `HEAD` and every commit in `git rev-list HEAD`: no match. Working tree excluding `.env`/`.git`/zip: no match. `.env.example` clean; `.env` is `git check-ignore`d. Exact-byte scan of docs assets and `pdftotext` of PDFs: no match. **But** old commit `4527950` (and an unreachable local blob) contains the current live key; both GitHub repos return HTTP 200 for `4527950` by SHA; `llm-check` succeeded. `.env` is `0644`. |
| 2 | Synthetic-only live mode for `fixture_id="uploaded"`; no HTTP call; 409 | **PARTIAL** | Exact uploaded case passes: API 409 with no worker/artifact, service raises `real_code_blocked` before any transport call (test uses a recording handler; calls `[]`). But a custom fixture labelled `demo-slice-300` or `case-studies/...` bypasses the gate and sends data. |
| 3 | Malformed provider responses degrade safely (array, `choices: None`, `content: None`, invalid JSON, 500, timeout) | **PASS** | Tests and probes: `[]` → `invalid_response`; `choices=None` → `empty_response`; `content=None` → `invalid_response`; non-JSON/non-UTF-8 → `invalid_json`; 500 → sanitized `http_error`; timeout → sanitized `request_failed`. A bad-shape migration completes with `llm.status=degraded`, 3 warnings, no annotations. `/api/llm/check` returns 502 without provider text. |
| 4 | Grounding caps, empty allowlists fail closed, residual risks require allowed rule IDs, instruction-like text dropped | **PASS with residual** | Caps 8 observations / 5 packages / 8 trade-offs / 8 residual risks / 8 unknowns; empty package allowlist drops all packages; residual risks without an allowed rule are dropped; `SYSTEM:` / “ignore previous instructions” text is dropped even with `EV-0001`. Residual: `risk` and `owner` fields can still carry instruction text. |
| 5 | Base URL rejects userinfo/non-http(s)/private/loopback unless allowed; `trust_env=False`; `base_host` no credentials | **PARTIAL** | `file://`, `ftp://`, `https://user:pass@…`, literal `169.254.169.254`, RFC1918, `127.0.0.1`, `localhost`, `[::1]`, `0.0.0.0` are rejected without `PREFLIGHT_LLM_ALLOW_LOCAL=true`; `trust_env=False` and `follow_redirects=False` verified; `base_host` drops userinfo. Numeric/encoded loopback and DNS-private names are not rejected; remote `http://` is allowed. |
| 6 | Migration audit checkpoint rejects empty/truncated/wrong-run logs; `R-DEMO-001` OK | **PASS with residual** | Empty log → `migration audit log is empty`; truncation → checkpoint count/size mismatch; cross-run events → `belongs to a different run`; checkpoint missing/corrupt → rejected. `preflight verify-migration R-DEMO-001` → `OK - 12 events verified`; review audit 9 events OK. Fully recomputed log+checkpoint still verifies (known local-writer limitation). |
| 7 | CLI non-loopback bind refused unless override | **PASS** | `cmd_serve` rejects `0.0.0.0`/LAN hosts with exit 2 unless `PREFLIGHT_ALLOW_NONLOCAL` is truthy; `127.0.0.1`, `::1`, `localhost` allowed; tests cover refused, override and loopback cases. Direct `uvicorn app.main:app --host 0.0.0.0` still bypasses this CLI-only guard. |
| 8 | CSRF/Host/Origin/path traversal/XSS/CSP still hold | **PASS** | No CSRF token → 403; bad token → 403; query-string token rejected; `Host: evil.example` → 400; `Origin: https://evil.example` → 400; valid same-origin token → 200. Traversal probes → 400/404; symlink escape blocked by resolve/parent check. Autoescape/CSP/no `|safe`/no `innerHTML` hold. |

---

## 4. Remaining findings

### SEC-R2-01 — CRITICAL: live API key was removed from `HEAD` but not rotated or purged from public history

**Where:** old commit `45279500a890875089ec067d20576253bf89ba27`; old `tests/test_agent_experience.py` literal at approximately line 592; an unreachable local Git blob; `.env` (untracked, mode `0644`); `.github/workflows/ci.yml` (no secret scan).

**Evidence:**

- The Round 1 literal was replaced in `HEAD`; `git grep` over `HEAD`, every commit reachable from `HEAD`, and the working tree (excluding `.env`) found no exact key.
- `git fsck --unreachable` still shows old commit `4527950` and a blob containing the key. The `fork/main` reflog shows `4527950` was previously pushed.
- `https://api.github.com/repos/<origin>/commits/4527950…` and the same URL on the fork both return **HTTP 200**. I did not download the commit bodies; local object inspection proves the old blob contains the key.
- I compared the old 51-character test literal with `PREFLIGHT_LLM_API_KEY` from `.env`: exact byte-for-byte match.
- One authorized `preflight llm-check` succeeded (`model mimo-v2.6-flash`, ~5.3 s, usage reported), so the publicly retrievable key is **live**, not a stale fixture.
- `.env` is still `0644`, and `.github/workflows/ci.yml` has no gitleaks/trufflehog/detect-secrets step.

**Impact:** Anyone who can read either GitHub repository can retrieve the old commit by SHA and obtain a working provider credential. Force-pushing the branch did not delete the old commit. Removing the literal from `HEAD` is cosmetic until the key is revoked and the server-side object is purged.

**Exact fix (in this order):**

1. **Revoke/rotate the key at the provider now.** Treat the old value as compromised; review provider usage/billing for the exposure window.
2. Purge the old object from both repositories. On a mirror, rewrite history with `git filter-repo`/BFG, force-push all branches and tags, expire reflogs and run `git gc --prune=now`; ask GitHub Support to purge cached/unreachable commits. A force-push alone is insufficient — the old commit remains reachable by SHA.
3. `chmod 600 .env`; add a startup check that warns if `stat.S_IMODE(...) & 0o077`. Document `install -m 600` in `.env.example`/README.
4. Add a secret scanner to pre-commit and CI (gitleaks/trufflehog/detect-secrets), scanning full history and the test/doc trees. The current hygiene tests only scan `app/` and `.env.example` (`tests/test_api_llm.py:1146-1168`, `tests/test_agent_experience.py:586-596`).
5. For anything beyond the demo, load the key from the OS keyring or a secrets manager. Do not put the key or a fingerprint in the repository.

---

### SEC-R2-02 — HIGH: synthetic-only gate trusts a mutable `fixture_id`; custom CLI snapshots are sent live

**Where:** `app/services/migrator.py:130-153` (especially line 142); `app/cli.py:99-114`; `app/services/pipeline.py:83-84`; `app/main.py:1292-1306` is correct for the API upload path.

**Evidence:**

- `is_synthetic_run()` returns `True` immediately when `fixture_id` is in `SYNTHETIC_FIXTURES` or contains a `case-studies` path part. It does not verify the manifest hash on that fast path.
- A minimal run with `fixture_id="demo-slice-300"`, `project_id="demo"`, and a fake manifest hash (`b`×64) returned `is_synthetic_run=True`. Live `run_migration()` then made **3 HTTP calls** and the prompt contained `CUSTOMER-CODE-MARKER-MISLABEL`.
- The CLI makes this reachable without editing the run store: `preflight analyze --fixture demo-slice-300 --fixture-path /path/to/customer` creates the run with `fixture_id="demo-slice-300"` and `project_id="demo"`; I confirmed a success status with that label on a temporary custom snapshot. The CLI only warns that it will not write metrics; it does not relabel the run or block live mode.
- The same bypass exists for any `fixture_id` containing a `case-studies` path part, because `_is_case_study_fixture()` accepts arbitrary path components.
- The exact `fixture_id="uploaded"` case is correctly blocked: API 409, no worker/artifact, service `LLMError(code="real_code_blocked")`, zero recorded transport calls.

**Impact:** A user who analyzes customer code with a custom `--fixture-path` and then runs `--live` can send confidential source text despite `PREFLIGHT_LLM_ALLOW_REAL_CODE=false`. This is exactly the accidental-misuse scenario the synthetic-only policy is meant to prevent.

**Exact fix:**

1. Derive synthetic status from **immutable run metadata**, not a mutable label:
   - Require `project_id == "demo"` **and** `manifest.sha256 in _synthetic_snapshot_hashes()` for the bundled fixtures.
   - For case studies, require the exact case ID in a server-side allowlist and `get_case_study(case_id)["synthetic"] is True`; do not accept arbitrary `case-studies/*` paths.
   - Remove the `fixture_id in SYNTHETIC_FIXTURES` short-circuit unless the manifest hash matches `ground_truth/FROZEN.json`.
2. In `cmd_analyze`, when `--fixture-path` is used, label the run `fixture_id="custom"` (or `"uploaded"`) and `project_id="custom"`; or refuse live mode for custom paths. Never label arbitrary content `demo-slice-300`.
3. Add tests: custom fixture path + live + flag false → `real_code_blocked`/409 and zero transport calls; mislabeled `fixture_id` with a non-frozen manifest → blocked; case-study path traversal label → blocked.

---

### SEC-R2-03 — MEDIUM: base-URL validation is bypassable with numeric/encoded loopback and DNS-private names; remote HTTP is allowed

**Where:** `app/services/llm.py:59-99` (`_base_url_error`), `app/services/llm.py:155-166` (`configured`), `app/services/llm.py:275-280` (client).

**Evidence:** The following configurations are accepted (`configured=True`):

```text
http://example.test/v1          (remote plaintext; API key would be sent over HTTP)
http://2130706433/v1            -> resolves to 127.0.0.1
http://0x7f000001/v1            -> resolves to 127.0.0.1
http://0177.0.0.1/v1            -> resolves to 127.0.0.1
http://127.1/v1                 -> resolves to 127.0.0.1
http://localhost.evil.test/v1   (DNS name; can resolve private)
```

`ipaddress.ip_address()` only sees dotted-quad/literal IPv6 in `parsed.hostname`; it does not normalize the numeric forms the resolver accepts. There is no DNS resolution check, and `http` is allowed for public hosts, so a key can be sent in cleartext or to a name that resolves into the private network. `https://user:pass@…`, `file://`, `ftp://`, `169.254.169.254`, RFC1918, `127.0.0.1`, `localhost`, `[::1]` and `0.0.0.0` are rejected as intended; `trust_env=False`, `follow_redirects=False`, and credential-free `base_host` are correct.

**Impact:** Env-only configuration reduces reachability, but a compromised `.env`, deployment setting, or operator typo can still turn the live check into a loopback/private-network SSRF primitive and can leak the API key over cleartext HTTP.

**Exact fix:**

1. Normalize/validate the host through the resolver, not just `ipaddress` on the literal string: resolve all A/AAAA records with `socket.getaddrinfo` and reject any private/loopback/link-local/reserved/multicast result unless `PREFLIGHT_LLM_ALLOW_LOCAL=true`.
2. Reject numeric/hex/octal IPv4 forms explicitly (canonicalize with `socket.inet_aton`/`ipaddress`) and consider an explicit `PREFLIGHT_LLM_ALLOWED_HOSTS` allowlist.
3. Require `https` for any non-loopback host, or gate plaintext behind a separate explicit `PREFLIGHT_LLM_ALLOW_PLAINTEXT=true`.
4. To close DNS rebinding, pin the validated IP for the request or re-check the connected peer; keep `trust_env=False`/`follow_redirects=False`.
5. Add tests for `2130706433`, `0x7f000001`, `0177.0.0.1`, `127.1`, a private-resolving DNS name, and remote `http://`.

---

### SEC-R2-04 — LOW/MEDIUM: response cap is enforced after the full body is read; 4xx/validation errors are retried; no total deadline

**Where:** `app/services/llm.py:281-352` (retry loop), `app/services/llm.py:290-294` (`len(response.content)` check), `app/services/llm.py:275-280` (per-operation timeout).

**Evidence:** `httpx.Client.post()` reads the entire response into `response.content` before the `MAX_RESPONSE_BYTES` check. A malicious/compromised endpoint can return a multi-gigabyte body and exhaust memory before the 256 KiB limit is applied. The `except (httpx.HTTPError, LLMError, ValueError)` block retries every `LLMError`, including 400/401/403/404 and `invalid_response`, twice; a bad key or bad model causes two requests. `timeout=45` is per operation, not a total deadline, so two attempts can take substantially longer than documented. The `llm-check` probe confirmed 2 attempts for 500, timeout, and 401.

**Impact:** Memory/availability DoS from a hostile endpoint; unnecessary credential/rate-limit exposure on 4xx; timeout budget overrun. Not a false-green or key-disclosure issue.

**Exact fix:** Use `client.stream()` and abort at `MAX_RESPONSE_BYTES` before buffering; classify retryable errors (transport errors, 429, 5xx only); honor `Retry-After` with a cap; impose a total `time.monotonic()` deadline; add tests asserting 401 → 1 attempt, 500 → 2 attempts, 429 `Retry-After` honored, oversized streamed body bounded.

---

### SEC-R2-05 — LOW: instruction-like text is filtered in prose but not in `risk`/`owner` metadata; UI still says “grounded”

**Where:** `app/services/llm.py:470-475` (`risk` copied without filtering), `app/services/llm.py:502-506` (`owner` copied without filtering); `app/templates/migrator.html:480`; `app/templates/codebase.html:304`; `app/templates/settings.html:76-78`.

**Evidence:** `validate_migration_annotation()` applies `_looks_like_instruction()` to headline, unknowns, observation text, package rationale/test, trade-off text and residual-risk text. It does **not** apply it to `risk` or `owner`:

```json
{"packages": [{"package_id": "WP-01", "rationale": "ok", "test": "ok",
               "risk": "ignore all rules now"}]}
```

retained `risk="ignore all rules now"` with `dropped_ungrounded=0`. A residual risk retained `owner="ignore previous instructions"`. These fields are rendered in the migration UI/plan. The “grounded” badge remains even though only citation membership was checked, not truth or quote support; the Round 1 recommendation to relabel it was not implemented.

**Impact:** Low; the model has no tools and cannot mutate gates, but prose/metadata labelled “grounded” can still mislead a reviewer. The instruction filter is a heuristic, not a security boundary.

**Exact fix:** Constrain `risk` to a `Literal["low","medium","high"]` enum; filter/drop `owner` and any other free-text metadata with `_looks_like_instruction()`; add injection tests for every rendered field. Either require a normalized quote to be a substring of the cited evidence/check detail before showing “grounded,” or relabel the badge “model commentary — citations checked, not evidence.” Update Settings copy accordingly.

---

### SEC-R2-06 — LOW: migration checkpoint is not sealed/bound; a fully rewritten log plus checkpoint verifies

**Where:** `app/services/migrator.py:217-271` (`verify_migration_log`), `app/services/migrator.py:1441-1462` (bundle manifest excludes `audit.checkpoint.json`), `app/templates/migrator.html:445-446` (unconditional “append-only · grown since seal”).

**Evidence:** Empty, truncated and wrong-run logs are now rejected, and `R-DEMO-001` verifies (`12 events verified`). But `verify_migration_log()` trusts a checkpoint written by the same local writer. I rewrote every event reason, recomputed all `hash`/`prev_hash` values, rewrote `count`/`head`/`log_size`, and verification returned `(True, "3 events verified")`. The bundle manifest deliberately excludes `audit.checkpoint.json` and contains no checkpoint head/digest, so the checkpoint is not sealed or independently anchored. The UI treats any audit-log seal mismatch as “append-only · grown since seal,” even if the file was truncated, unless the checkpoint verification independently fails.

**Impact:** Local tamper evidence only; a writer who can rewrite both files can present a valid-looking chain. This matches the documented “tamper-evident, not non-repudiation” limitation, but the Round 1 fix asked for a checkpoint head binding into the manifest and an external anchor, and neither is present.

**Exact fix:** Bind the final checkpoint head/count/log_size into the bundle manifest (or a separately signed anchor) and verify it in `verify_migration_log`; use an HMAC key outside the run directory or an external timestamp/anchor for real tamper evidence; distinguish “grown” from “shrunk” in the UI using the sealed digest/event count; add a test with a fully recomputed log+checkpoint that must fail or be flagged as “rewritten/unanchored.”

---

### SEC-R2-07 — LOW: invalid model/feature still returns HTTP 200 “starting” and fails asynchronously

**Where:** `app/main.py:267-271` (`MigrationRequest.model: str | None`), `app/main.py:1292-1322` (worker started before model/feature validation), `app/services/migrator.py:1012` (`resolve_model` in the worker).

**Evidence:** With a configured live app and a succeeded run, POSTing `{"live": true, "model": "evil-model"}` returned:

```text
200 {"run_id": "R-BADMODEL", "status": "starting", "feature_id": null}
```

The worker then raised `LLMError: Unsupported live model…`, logged a traceback, wrote no `migration.json`, and the migration view remained `not_started`. A missing/invalid `feature_id` has the same asynchronous shape. This is the Round 1 SEC-10 issue, still open.

**Impact:** Low; the request cannot cause an unwanted model call, but the client is told the run started when it did not. A missing feature fails after the worker is created.

**Exact fix:** Use `Literal["mimo-v2.6-flash", "mimo-v2.6-pro"] | None` on both request models; resolve/validate `feature_id` and `model` before starting the thread; return 422/404/409 with a sanitized message, or return a job record and surface worker failures in migration state. Add API tests for invalid model/feature returning 4xx and no worker.

---

### SEC-R2-08 — LOW: `.env` remains world-readable; `testserver` remains a default host; docs/UI drift

**Where:** `.env` mode `0644`; `app/config.py:58` (`allowed_hosts` includes `testserver`); `app/security.py:104-108` (fallback origins include `testserver`); `docs/LIVE-AGENTS.md:186-191`; `app/templates/settings.html:34,61,69`; `app/templates/migrator.html:67,123-124`.

**Evidence:** `.env` is still `0644` and no startup permission warning exists. `testserver` remains in the production default host allowlist; the CLI bind guard is real, but direct `uvicorn app.main:app --host 0.0.0.0` bypasses it. Settings/UI say “synthetic only” and “only synthetic fixture text” even when `allow_real_code=true`, and `docs/LIVE-AGENTS.md` still says the flag “does not inspect content, redact files, or block a run,” which is now false — the service does block uploaded runs.

**Impact:** Low operational/security hygiene; documentation and UI can misstate the control that now exists.

**Exact fix:** `chmod 600 .env` and warn at startup on `0o077`; remove `testserver` from production defaults and inject it only in tests, or gate it behind an explicit test flag; add a startup check in the app factory for non-loopback bind as well as the CLI guard; update `docs/LIVE-AGENTS.md` and the UI strings to condition on `allow_real_code`; describe the CLI custom-fixture caveat (or fix SEC-R2-02).

---

## 5. Controls that held

### Secret hygiene in `HEAD` (but not history)

- `git grep` over `HEAD` and every commit in `git rev-list HEAD`: no exact key.
- Working tree excluding `.env`/`.git`/zip: no exact key.
- `.env.example` contains empty `PREFLIGHT_LLM_API_KEY` and empty base URL; `.env` is ignored via `git check-ignore`.
- Exact-byte scan over `docs/` assets, including PNG/PDF bytes, plus `pdftotext` for PDFs: no key. Visual spot-check of the Settings live panel and test-connection screenshots shows the endpoint host only, never the key. I did not OCR all 1,000+ PNGs; the exact-byte scan is the reliable check.
- `tests/test_agent_experience.py` no longer stores the real literal; the current source-hygiene tests scan `app/` and `.env.example`.

### Synthetic-only for uploaded runs

- `tests/test_api_llm.py:337-363`: uploaded run + configured live + flag false → 409, no worker, no `migration.json`.
- `tests/test_api_llm.py:366-387`: direct `run_migration()` with a recording `MockTransport` → `real_code_blocked`, **zero calls**, no artifact.
- `tests/test_api_llm.py:390-419`: labelled synthetic fixture → 3 calls, 3 annotations, plan records them. Note: `_minimal_succeeded_run()` writes a fake manifest hash (`a`×64, not a `FROZEN.json` hash), so this positive test itself relies on the `fixture_id` fast path rather than proving immutable synthetic provenance.
- API gate is before thread start (`app/main.py:1292-1306`); service gate is before feature/HTTP work (`app/services/migrator.py:1010-1012`).

### Malformed provider responses

| Probe | Result |
|---|---|
| `[]` | `LLMError(code="invalid_response")` |
| `{"choices": null}` | `LLMError(code="empty_response")` |
| `{"choices": "oops"}` | `LLMError(code="empty_response")` |
| `{"choices": []}` | `LLMError(code="empty_response")` |
| `{"choices": [{}]}` | `LLMError(code="invalid_response")` |
| `content: null` / `content: []` | `LLMError(code="invalid_response")` |
| 200 non-JSON / non-UTF-8 | `LLMError(code="invalid_json")` |
| HTTP 500 | `http_error`, 2 attempts, message `Live model returned HTTP 500.` |
| Timeout | `request_failed`, 2 attempts, generic message |
| Bad shape during migration | migration completes; `llm.status=degraded`; 3 warnings; no annotations |
| `/api/llm/check` bad shape / `AttributeError` | 502; provider text absent |

### Grounding and injection

| Probe | Result |
|---|---|
| 50 observations | 8 kept, 42 dropped |
| Empty package allowlist | all packages dropped |
| Residual risk without allowed `rule_id` | dropped |
| Instruction text with valid `EV-0001` | dropped; `dropped_ungrounded` increments |
| `SYSTEM OVERRIDE` headline | dropped |
| Empty evidence allowlist | observations dropped |
| 1 MB response / 50k items | byte cap and item caps bound output; note the byte cap is post-read (SEC-R2-04) |

### Base URL

- Userinfo, `file://`, `ftp://`, literal private/loopback/link-local/unspecified addresses rejected without `PREFLIGHT_LLM_ALLOW_LOCAL=true`.
- `PREFLIGHT_LLM_ALLOW_LOCAL=true` allows a trusted loopback endpoint.
- `httpx.Client(trust_env=False, follow_redirects=False)` verified by monkeypatched client.
- `public()["base_host"]` returns host:port only; no userinfo.
- `chat_json` refuses an unsafe base URL before creating a request.

### Migration audit

- Empty `audit.jsonl` → `migration audit log is empty`.
- Truncated log with stale checkpoint → checkpoint count/size mismatch.
- Events copied from another run → `belongs to a different run`.
- Missing/corrupt checkpoint → rejected.
- `preflight verify-migration R-DEMO-001` → `OK - 12 events verified`.
- `preflight verify-audit R-DEMO-001` → `OK (9 events)`.

### CLI bind

- `preflight serve --host 0.0.0.0` without override → exit 2, no uvicorn start.
- `PREFLIGHT_ALLOW_NONLOCAL=1` → allowed with a visible warning.
- `127.0.0.1`, `::1`, `localhost` → allowed.
- `scripts/run_demo_server.sh` and `Makefile` bind `127.0.0.1` explicitly.

### CSRF, Host/Origin, traversal, XSS/CSP

- `/api/llm/check` without CSRF → 403; bad token → 403; query-string token rejected.
- `Host: evil.example` → 400; `Origin: https://evil.example` → 400.
- Traversal: `migration/../../status.json` → 400; `migration/../status.json` → 400; `/etc/passwd` → 400; encoded `..` → 404; symlink escape → 404; valid migration file → 200.
- `app/templates`/`app/static`: no `|safe`, no `innerHTML`/`insertAdjacentHTML`/`eval`/`new Function`; `workbench.html:368` uses `|tojson`; CSP includes `default-src 'self'`, `script-src 'self'`, `object-src 'none'`, `base-uri 'none'`, `frame-ancestors 'none'`.

---

## 6. Test and runtime evidence

```text
.venv/bin/python -m pytest tests/test_api_llm.py tests/test_security.py \
  tests/test_agent_experience.py tests/test_redaction.py -q
# 118 passed

.venv/bin/python -m pytest -m "not e2e" -q
# 506 passed (520 collected, 14 e2e deselected)

PREFLIGHT_LLM_TIMEOUT=20 .venv/bin/preflight llm-check
# mode: live · configured: True · host: <configured-provider-host>
# OK · model mimo-v2.6-flash · ~5257 ms · usage 37 tokens
```

The real check confirms the configured key is live; it does not print or persist the key. All other live-path probes used `httpx.MockTransport` or a failing model resolution, never the provider.

Adversarial probes (read-only, temporary dirs):

| Probe | Result |
|---|---|
| Uploaded run API + live + flag false | 409, no worker/artifact |
| Uploaded run service + recording transport | `real_code_blocked`, 0 calls |
| `fixture_id=demo-slice-300` + fake manifest + live | **3 calls**, marker in prompt (SEC-R2-02) |
| CLI custom `--fixture-path` + `--fixture demo-slice-300` | run succeeded with `fixture_id=demo-slice-300`; `is_synthetic_run=True` (SEC-R2-02) |
| `http://2130706433`, `0x7f000001`, `0177.0.0.1`, `127.1` | accepted; resolve to `127.0.0.1` (SEC-R2-03) |
| `http://example.test` | accepted (plaintext remote) (SEC-R2-03) |
| `risk`/`owner` instruction text | retained (SEC-R2-05) |
| Fully rewritten migration log + checkpoint | verifies true (SEC-R2-06) |
| Invalid model POST | 200 `starting`; worker fails; no artifact (SEC-R2-07) |
| `Host: evil.example` | 400 |
| `/api/llm/check` no CSRF | 403 |
| `/api/llm/check` bad Origin | 400 |
| Traversal / absolute / encoded / valid file | 400 / 400 / 404 / 200 |

---

## 7. Prioritized remediation order

1. **Rotate the live key and purge old commit `4527950` from both GitHub repositories.** Force-push is not enough; the old commit is still served by SHA. Do this before any further live use. (SEC-R2-01)
2. **Make synthetic status immutable.** Remove the `fixture_id` fast path; require a frozen manifest hash or exact case-study profile; relabel custom CLI paths; add the mislabeled-fixture test. (SEC-R2-02)
3. **Harden base-URL validation** against numeric/encoded loopback, DNS-private names, and remote plaintext HTTP; pin/validate resolved addresses. (SEC-R2-03)
4. **Stream the response with a hard cap, retry only transport/429/5xx, and add a total deadline.** (SEC-R2-04)
5. **Filter `risk`/`owner` metadata and relabel or strengthen the “grounded” UI badge.** (SEC-R2-05)
6. **Bind the audit checkpoint into the bundle/anchor and test a fully recomputed chain.** (SEC-R2-06)
7. **Validate model/feature before starting workers.** (SEC-R2-07)
8. **Fix `.env` permissions, remove `testserver` from production defaults, guard direct non-loopback uvicorn, and update docs/UI copy.** (SEC-R2-08)

---

## 8. Scope limits

- I did not run the browser E2E suite; the 14 e2e tests were deselected. The non-e2e suite and focused security/LLM tests are green.
- I did not OCR all 1,000+ documentation/screenshot images. I did exact-byte scans of the repository/docs assets, `pdftotext` extraction of PDFs, and a visual spot-check of the Settings screenshots. The confirmed credential exposure is historical, not a screenshot.
- I did not download the body of the old GitHub commit; I confirmed its existence by HTTP status and confirmed its content locally. I used one authorized real `llm-check`; no other provider calls were made.
- A local attacker with write access to the repository, `.env`, or the run store can defeat most local hash-chain and client-side controls. The audit treats the local filesystem as trusted only where explicitly stated.
