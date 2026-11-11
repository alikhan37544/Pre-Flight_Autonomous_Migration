"""API contracts for the optional live-reasoning layer and migration views.

These complement ``test_agent_experience.py``: that module pins the service
contracts, while these tests drive the FastAPI routes, the persisted offline
bundle, and the real code-migration result. No test may reach a real endpoint;
the one live check is backed by ``httpx.MockTransport``.
"""

from __future__ import annotations

import hashlib
import json
import re
import subprocess
import time
from pathlib import Path

import httpx
import pytest
from fastapi.testclient import TestClient

from app.config import Settings
from app.main import CodeMigrationRequest, MigrationRequest, create_app
from app.services.code_migration import build_codebase_view, run_code_migration
from app.services.llm import chat_json as real_chat_json

REPO = Path(__file__).resolve().parents[1]
DEMO = REPO / "fixtures" / "demo-slice-300"
REFERENCE = REPO / "ground_truth" / "reference_target" / "pa_veh_01_reference.json"


def _settings(tmp_path: Path, **overrides) -> Settings:
    values = {
        "data_dir": tmp_path / "data",
        "fixtures_dir": REPO / "fixtures",
        "reference_path": REFERENCE,
        "secret_key": "test-secret",
        "sync_runs": True,
        # Never inherit the developer's .env: tests must not reach a real endpoint.
        "llm_mode": "off",
        "llm_base_url": "",
        "llm_api_key": "",
        "llm_model": "mimo-v2.6-flash",
    }
    values.update(overrides)
    return Settings(**values)


def _csrf(client: TestClient) -> str:
    response = client.get("/about")
    match = re.search(r'name="csrf-token" content="([^"]+)"', response.text)
    assert match, "a product page must expose a CSRF token"
    return match.group(1)


def _wait_for_migration(client: TestClient, run_id: str, *, timeout: float = 60.0) -> dict:
    """Wait until the background worker has finished and released the run."""
    deadline = time.monotonic() + timeout
    payload: dict | None = None
    while time.monotonic() < deadline:
        payload = client.get(f"/api/runs/{run_id}/migration").json()
        worker = client.app.state.migration_workers.get(run_id)
        finished = payload.get("status") in {"completed", "completed_with_gates", "failed"}
        if finished and (worker is None or not worker.is_alive()):
            return payload
        time.sleep(0.05)
    pytest.fail(f"migration did not finish within {timeout}s: {payload}")


@pytest.fixture(scope="module")
def offline_migration(tmp_path_factory):
    """Run one real offline migration and keep the sealed files for assertions."""
    app = create_app(_settings(tmp_path_factory.mktemp("offline-migration-data")))
    with TestClient(app) as client:
        token = _csrf(client)
        created = client.post(
            "/api/runs",
            json={"project_id": "demo", "fixture_id": "demo-slice-300", "force": True},
            headers={"X-CSRF-Token": token},
        )
        assert created.status_code == 200, created.text
        run_id = created.json()["run_id"]
        started = client.post(
            f"/api/runs/{run_id}/migration",
            json={"feature_id": "PA-VEH-01", "force": True},
            headers={"X-CSRF-Token": token},
        )
        assert started.status_code == 200, started.text
        _wait_for_migration(client, run_id)

        store = app.state.store
        state = store.read_artifact(run_id, "migration.json")
        run_dir = store.run_dir(run_id)
        plan_path = run_dir / "migration" / "migration-plan.json"
        plan_bytes = plan_path.read_bytes()
        response = client.get(f"/api/runs/{run_id}/migration")
        assert response.status_code == 200, response.text
        payload = response.json()

    return {
        "payload": payload,
        "state": state,
        "run_dir": run_dir,
        "plan_path": plan_path,
        "plan_bytes": plan_bytes,
    }


# -- 1. status endpoint -----------------------------------------------------

def test_llm_status_api_exposes_models_without_the_key(tmp_path: Path) -> None:
    settings = _settings(
        tmp_path,
        llm_mode="live",
        llm_base_url="https://example.test/v1",
        llm_api_key="secret-key-value",
        llm_model="mimo-v2.6-pro",
    )
    with TestClient(create_app(settings)) as client:
        response = client.get("/api/llm/status")

    assert response.status_code == 200
    payload = response.json()
    assert payload["configured"] is True
    assert payload["mode"] == "live"
    assert payload["base_host"] == "example.test"
    assert payload["models"] == ["mimo-v2.6-flash", "mimo-v2.6-pro"]
    assert payload["default_model"] == "mimo-v2.6-pro"
    assert "api_key" not in payload
    assert "secret-key-value" not in response.text


# -- 2. check endpoint ------------------------------------------------------

def test_llm_check_returns_409_when_unconfigured(tmp_path: Path) -> None:
    settings = _settings(
        tmp_path,
        llm_mode="live",
        llm_base_url="https://example.test/v1",
        llm_api_key="",
    )
    with TestClient(create_app(settings)) as client:
        token = _csrf(client)
        response = client.post(
            "/api/llm/check",
            headers={"X-CSRF-Token": token},
        )

    assert response.status_code == 409
    assert "PREFLIGHT_LLM_API_KEY" in response.json()["detail"]


def test_llm_check_uses_the_mocked_transport_and_returns_metadata(
    tmp_path: Path, monkeypatch
) -> None:
    settings = _settings(
        tmp_path,
        llm_mode="live",
        llm_base_url="https://example.test/v1",
        llm_api_key="secret-key-value",
        llm_model="mimo-v2.6-pro",
    )
    seen: dict[str, str] = {}

    def handler(request: httpx.Request) -> httpx.Response:
        seen["url"] = str(request.url)
        seen["auth"] = request.headers.get("authorization", "")
        seen["model"] = json.loads(request.content)["model"]
        return httpx.Response(
            200,
            json={
                "id": "cmpl-check",
                "model": "mimo-v2.6-pro",
                "choices": [{"message": {"content": '{"ok": true}'}}],
                "usage": {"prompt_tokens": 8, "completion_tokens": 2, "total_tokens": 10},
            },
        )

    def mocked_chat_json(messages, *, config, **kwargs):
        return real_chat_json(
            messages,
            config=config,
            transport=httpx.MockTransport(handler),
            **kwargs,
        )

    monkeypatch.setattr("app.main.chat_json", mocked_chat_json)

    with TestClient(create_app(settings)) as client:
        token = _csrf(client)
        response = client.post(
            "/api/llm/check",
            headers={"X-CSRF-Token": token},
        )

    assert response.status_code == 200, response.text
    payload = response.json()
    assert payload["ok"] is True
    assert payload["model"] == "mimo-v2.6-pro"
    assert isinstance(payload["latency_ms"], int)
    assert payload["latency_ms"] >= 0
    assert payload["usage"]["total_tokens"] == 10
    assert payload["provider"] == "OpenAI-compatible"
    assert seen["url"] == "https://example.test/v1/chat/completions"
    assert seen["auth"] == "Bearer secret-key-value"
    assert seen["model"] == "mimo-v2.6-pro"
    assert "secret-key-value" not in response.text


# -- 3. live migration guard ------------------------------------------------

def test_live_migration_refuses_unconfigured_without_starting_a_worker(
    tmp_path: Path,
) -> None:
    app = create_app(_settings(tmp_path))
    assert app.state.settings.llm_config().configured is False
    run_id = "R-LIVE-UNCONFIG"
    with TestClient(app) as client:
        store = app.state.store
        store.create_run(
            run_id,
            project_id="demo",
            snapshot_id="S-LIVE-UNCONFIG",
            fixture_id="demo-slice-300",
        )
        store.update_status(run_id, status="succeeded", stage="complete", percent=100.0)
        token = _csrf(client)

        response = client.post(
            f"/api/runs/{run_id}/migration",
            json={"feature_id": "PA-VEH-01", "force": True, "live": True,
                  "model": "mimo-v2.6-pro"},
            headers={"X-CSRF-Token": token},
        )

        assert response.status_code == 409, response.text
        detail = response.json()["detail"]
        assert "Live reasoning is not configured" in detail
        assert "PREFLIGHT_LLM_BASE_URL" in detail
        assert not store.exists(run_id, "migration.json")
        assert app.state.migration_workers == {}
        state = client.get(f"/api/runs/{run_id}/migration").json()
        assert state["status"] == "not_started"


# -- 4. completed offline migration API ------------------------------------

def test_completed_offline_migration_api_enriches_without_changing_the_plan(
    tmp_path: Path,
) -> None:
    app = create_app(_settings(tmp_path))
    assert app.state.settings.llm_config().configured is False
    with TestClient(app) as client:
        token = _csrf(client)
        created = client.post(
            "/api/runs",
            json={"project_id": "demo", "fixture_id": "demo-slice-300", "force": True},
            headers={"X-CSRF-Token": token},
        )
        assert created.status_code == 200, created.text
        run_id = created.json()["run_id"]

        started = client.post(
            f"/api/runs/{run_id}/migration",
            json={"feature_id": "PA-VEH-01", "force": True},
            headers={"X-CSRF-Token": token},
        )
        assert started.status_code == 200, started.text
        _wait_for_migration(client, run_id)

        store = app.state.store
        state_before = store.read_artifact(run_id, "migration.json")
        plan_path = store.run_dir(run_id) / "migration" / "migration-plan.json"
        plan_bytes_before = plan_path.read_bytes()
        plan_sha_before = hashlib.sha256(plan_bytes_before).hexdigest()
        assert state_before["plan_sha256"] == plan_sha_before

        response = client.get(f"/api/runs/{run_id}/migration")
        assert response.status_code == 200
        payload = response.json()

        state_after = store.read_artifact(run_id, "migration.json")
        assert state_after["plan_sha256"] == plan_sha_before
        assert payload["plan_sha256"] == plan_sha_before
        assert plan_path.read_bytes() == plan_bytes_before
        assert hashlib.sha256(plan_path.read_bytes()).hexdigest() == plan_sha_before

    assert payload["status"] == "completed_with_gates"
    assert [stage["agent_id"] for stage in payload["stages"]] == [
        "scout", "architect", "guardian", "critic", "scribe",
    ]
    assert len(payload["stages"]) == 5
    assert len(payload["handoffs"]) == 5
    assert payload["handoffs"][0]["from"] == "scout"
    assert payload["handoffs"][0]["to"] == "architect"
    assert payload["handoffs"][-1]["to"] == "sealed bundle"
    assert "Scout resolved PA-VEH-01" in payload["narrative"]
    assert "Scribe sealed" in payload["narrative"]
    assert payload["explain"]["headline"]
    assert payload["explain"]["plain_language"]
    assert payload["explain"]["why_it_matters"]
    assert payload["explain"]["what_to_look_at"]
    assert len(payload["glossary"]) >= 5
    assert all(item["term"] and item["definition"] for item in payload["glossary"])

    gate_groups = payload["gate_groups"]
    assert gate_groups["assumptions"]
    assert gate_groups["rules"]
    grouped_gates = len(gate_groups["assumptions"]) + sum(
        len(group["gates"]) for group in gate_groups["rules"]
    )
    assert grouped_gates == len(payload["gates"])


# -- 4b. sealed bundle and reviewer fields --------------------------------

def test_migration_api_exposes_sealed_files_and_reviewer_fields(
    offline_migration,
) -> None:
    payload = offline_migration["payload"]
    state = offline_migration["state"]
    run_dir = offline_migration["run_dir"]

    files = payload["bundle_files"]
    assert len(files) == state["bundle"]["file_count"] == 8
    roles = [item["role"] for item in files]
    assert roles == [
        "schema", "mapping", "updater", "codegen config", "API contract",
        "plan", "report", "agent log",
    ]
    assert sum(1 for role in roles if role in {
        "schema", "mapping", "updater", "codegen config", "API contract",
    }) == 5
    assert payload["bundle_manifest"]["path"] == "migration/bundle-manifest.json"
    assert payload["bundle_manifest"]["path"] not in {
        item["path"] for item in files
    }
    for item in files:
        assert item["sha256"] == state["bundle"]["sha256_files"][item["path"]]
        sealed = run_dir / item["path"]
        current = hashlib.sha256(sealed.read_bytes()).hexdigest()
        assert item["current_sha256"] == current
        if item["role"] == "agent log":
            # The chain is append-only: sealing records its digest before the
            # final orchestrator events. The view exposes both values rather
            # than pretending the sealed digest covers later appends.
            assert item["append_only"] is True
            assert item["note"]
        else:
            assert item["hash_matches_seal"] is True
            assert current == item["sha256"]

    summary = payload["human_gate_summary"]
    assert summary["assumption_gates"] == 3
    assert summary["rule_groups"] == 8
    assert summary["total"] == 11
    assert summary["high"] == 6
    assert summary["all_changes_pending"] is True
    assert summary["pending_changes"] == 5
    assert "3 assumptions + 8 rule groups = 11 human review decisions" in (
        summary["plain_language"]
    )
    assert "6 high" in summary["plain_language"]
    assert summary["machine_checks"]["total"] == 7
    assert summary["machine_checks"]["passed"] == 7
    assert payload["machine_checks"]["total"] == 7
    assert payload["machine_checks"]["passed"] == 7

    assert 3 <= len(payload["next_actions"]) <= 5
    joined = " ".join(payload["next_actions"]).lower()
    assert "owner" in joined
    assert "assumption" in joined
    assert "approve or reject" in joined
    assert "audit" in joined

    assumptions = payload["gate_groups"]["assumptions"]
    assert assumptions
    for gate in assumptions:
        assert gate["owner"] == "unassigned"
        assert gate["owner_assigned"] is False
        assert gate["owner_display"] == "Unassigned — assign before approval"
        assert gate["resolution_hint"]
    assert all(
        group["resolution_hint"] for group in payload["gate_groups"]["rules"]
    )

    assert payload["evidence_preview"]
    assert all(item.get("locator") for item in payload["evidence_preview"])

    boundary = payload["reality_boundary"]
    assert boundary == {
        "synthetic": True,
        "actual_migration": False,
        "tenant_contacted": False,
        "compiled": False,
        "official_assurance": False,
        "what_is_real": boundary["what_is_real"],
        "what_is_not_real": boundary["what_is_not_real"],
    }
    assert boundary["what_is_real"]
    assert boundary["what_is_not_real"]

    # Reading the enriched view must not touch the sealed plan or its hash.
    plan_path = offline_migration["plan_path"]
    assert plan_path.read_bytes() == offline_migration["plan_bytes"]
    assert hashlib.sha256(plan_path.read_bytes()).hexdigest() == state["plan_sha256"]
    assert payload["plan_sha256"] == state["plan_sha256"]


# -- 5. real codebase view --------------------------------------------------

@pytest.fixture(scope="module")
def cascade_result(tmp_path_factory):
    settings = _settings(tmp_path_factory.mktemp("cascade-data"))
    return run_code_migration("cascade-mutual", settings, max_iterations=3)


def test_codebase_view_over_a_real_run_adds_a_story_without_mutating(
    cascade_result,
) -> None:
    before = json.dumps(cascade_result, sort_keys=True, default=str)
    view = build_codebase_view(cascade_result)

    assert json.dumps(cascade_result, sort_keys=True, default=str) == before
    assert view is not cascade_result
    assert view["case_id"] == "cascade-mutual"
    assert [stage["agent_id"] for stage in view["stages"]] == [
        "scout", "architect", "guardian", "critic", "planner",
    ]
    assert len(view["stages"]) == 5
    assert view["narrative"]
    assert "Scout scanned" in view["narrative"]
    assert "Planner compiled the report" in view["narrative"]
    assert view["explain"]["headline"]
    assert view["explain"]["what_to_look_at"]
    assert len(view["glossary"]) >= 5

    inventory = view["scout_inventory"]
    source = view["source_scan"]
    assert inventory["files"] == source["files_scanned"] > 0
    assert inventory["loc"] == source["loc"] > 0
    assert inventory["by_language"] == source["by_language"]
    assert "features" in inventory
    assert "hotspots" in inventory
    assert "imports" in inventory
    assert "skipped" in inventory
    # The added experience must not leak back into the persisted-shaped result.
    assert "stages" not in cascade_result
    assert "narrative" not in cascade_result
    assert "scout_inventory" not in cascade_result


def test_codebase_view_over_a_real_run_exposes_report_bundle_and_summaries(
    cascade_result,
) -> None:
    before = json.dumps(cascade_result, sort_keys=True, default=str)
    view = build_codebase_view(cascade_result)
    assert json.dumps(cascade_result, sort_keys=True, default=str) == before

    files = view["bundle_files"]
    assert [item["role"] for item in files] == [
        "report", "SARIF", "patches", "target", "audit log",
    ]
    assert view["report_artifacts"] == files
    patches = next(item for item in files if item["role"] == "patches")
    assert patches["count"] == len(cascade_result["patches"]) > 0
    assert patches["pending"] == len(cascade_result["patches"])
    target = next(item for item in files if item["role"] == "target")
    assert target["count"] == len(cascade_result["target_files"]) > 0
    audit = next(item for item in files if item["role"] == "audit log")
    assert audit["events"] == len(cascade_result["audit"]) > 0
    assert audit["verified"] is True
    report = next(item for item in files if item["role"] == "report")
    assert report["sha256"] == cascade_result["planner"]["report_sha256"]

    summary = view["human_gate_summary"]
    assert summary["total"] == len(cascade_result["critic"]["residual_risks"])
    assert summary["all_patches_pending"] is True
    assert summary["approved_patches"] == 0

    machine = view["machine_check_summary"]
    assert machine["guardian"]["total"] == len(cascade_result["guardian"]["checks"])
    assert machine["critic"]["total"] == len(cascade_result["critic"]["checks"]) == 7
    assert machine["failed"] == 0
    assert machine["passed"] == machine["total"]

    assert len(view["next_actions"]) >= 3
    boundary = view["reality_boundary"]
    assert boundary["synthetic"] is True
    assert boundary["actual_migration"] is False
    assert boundary["tenant_contacted"] is False
    assert boundary["compiled"] is False
    assert boundary["official_assurance"] is False
    assert boundary["what_is_real"]
    assert boundary["what_is_not_real"]

    assert view["iteration_story"]
    for item in view["iteration_story"]:
        assert isinstance(item["target_label"], str)
        assert item["target_label"].startswith("warning: ")
        assert " · error: " in item["target_label"]
    assert view["gate_owner_fallback"] == []
    assert view["stale_green"] is False
    assert view["stale_green_reason"] is None


def test_upgrade_run_marks_the_previous_green_as_stale(
    cascade_result, tmp_path: Path
) -> None:
    assert cascade_result["stale_green"] is False
    assert cascade_result["stale_green_reason"] is None

    result = run_code_migration(
        "cascade-mutual",
        _settings(tmp_path),
        max_iterations=2,
        upgrade_scenario="GWCP-APP-EVENTS-V2-2027.04",
    )
    assert result["status"] == "revalidation_required"
    assert result["stale_green"] is True
    assert "revalidated" in result["stale_green_reason"]
    assert "GWCP" in result["stale_green_reason"]

    view = build_codebase_view(result)
    assert view["stale_green"] is True
    assert view["stale_green_reason"] == result["stale_green_reason"]


# -- 6. request models ------------------------------------------------------

def test_request_models_accept_live_and_model_fields() -> None:
    migration = MigrationRequest(
        feature_id="PA-VEH-01", force=True, live=True, model="mimo-v2.6-pro",
    )
    assert migration.live is True
    assert migration.model == "mimo-v2.6-pro"
    assert migration.feature_id == "PA-VEH-01"
    assert migration.force is True

    code = CodeMigrationRequest(
        max_iterations=2, live=True, model="mimo-v2.6-flash",
    )
    assert code.live is True
    assert code.model == "mimo-v2.6-flash"
    assert code.max_iterations == 2

    assert MigrationRequest().live is False
    assert MigrationRequest().model is None
    assert CodeMigrationRequest().live is False
    assert CodeMigrationRequest().model is None


# -- 7. source hygiene ------------------------------------------------------

def test_app_and_env_example_contain_no_real_credentials() -> None:
    app_text = "\n".join(
        path.read_text(encoding="utf-8", errors="ignore")
        for path in (REPO / "app").rglob("*")
        if path.is_file() and "__pycache__" not in path.parts
    ).lower()
    example = (REPO / ".env.example").read_text(encoding="utf-8")
    example_lower = example.lower()

    for marker in ("tp-sg26", "token-plan-sgp", "xiaomimimo.com"):
        assert marker not in app_text, marker
        assert marker not in example_lower, marker

    values = {
        key.strip(): value.strip()
        for line in example.splitlines()
        if "=" in line and not line.lstrip().startswith("#")
        for key, value in (line.split("=", 1),)
    }
    assert values["PREFLIGHT_LLM_MODE"] == "off"
    assert values["PREFLIGHT_LLM_BASE_URL"] == ""
    assert values["PREFLIGHT_LLM_API_KEY"] == ""
    assert values["PREFLIGHT_LLM_MODEL"] == "mimo-v2.6-flash"


def test_dot_env_is_gitignored_but_env_example_is_not() -> None:
    root = REPO
    ignored = {
        line.strip()
        for line in (root / ".gitignore").read_text(encoding="utf-8").splitlines()
        if line.strip() and not line.lstrip().startswith("#")
    }
    assert ".env" in ignored
    assert ".env.example" not in ignored
    assert ".env.local" in ignored

    if (root / ".git").exists():
        result = subprocess.run(
            ["git", "check-ignore", "--quiet", ".env"],
            cwd=root,
            check=False,
        )
        assert result.returncode == 0, ".env must be ignored by git"
