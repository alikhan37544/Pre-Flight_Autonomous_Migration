"""Contract tests for the five-agent demo experience.

These are deliberately written before the implementation. The tests pin the
information each agent must expose, the handoff narrative, and the safe
configuration of the optional live-reasoning layer.
"""

from __future__ import annotations

import json
from pathlib import Path

import httpx
import pytest

from app.services.migrator import build_migration_view


def _agent(agent_id: str, name: str, status: str = "done") -> dict:
    return {
        "agent_id": agent_id,
        "name": name,
        "role": f"{name} role",
        "description": f"{name} description",
        "status": status,
        "summary": f"{name} summary",
        "checks": [{"name": f"{name} check", "ok": True, "detail": "ok"}],
    }


def _state() -> dict:
    return {
        "schema_version": "1.0",
        "run_id": "R-TEST",
        "feature_id": "PA-VEH-01",
        "feature_name": "Vehicle Information",
        "status": "completed_with_gates",
        "mode": "five specialist agents · deterministic handoffs",
        "boundary": "No deployment.",
        "started_at": "2026-01-01T00:00:00Z",
        "finished_at": "2026-01-01T00:00:05Z",
        "progress": 100,
        "current_agent": None,
        "agents": [
            _agent("scout", "Scout"),
            _agent("architect", "Architect"),
            _agent("guardian", "Guardian"),
            _agent("critic", "Critic"),
            _agent("scribe", "Scribe"),
        ],
        "packages": [
            {
                "package_id": "WP-01",
                "title": "Generate schema",
                "target_path": "config/ext/schema.json",
                "disposition": "mapped_transformed",
                "status": "draft_ready",
                "evidence_ids": ["EV-0001"],
                "gate_ids": ["G-03"],
                "approval": "pending",
                "bytes": 100,
                "sha256": "a" * 64,
            }
        ],
        "gates": [
            {"gate_id": "G-01", "kind": "assumption", "severity": "high",
             "title": "Territory gap", "question": "Which rating source?", "owner": "Product",
             "source_id": "A-01", "status": "open"},
            {"gate_id": "G-02", "kind": "assumption", "severity": "medium",
             "title": "Rating input gap", "question": "Provide export?", "owner": "Data",
             "source_id": "A-02", "status": "open"},
            {"gate_id": "G-03", "kind": "assumption", "severity": "high",
             "title": "Long type", "question": "Who owns the override?", "owner": "APD",
             "source_id": "A-03", "status": "open"},
            {"gate_id": "G-04", "kind": "review", "severity": "medium",
             "title": "Direct SQL (2 findings, PF-GW-SQL-001)", "question": "Remediated?",
             "owner": "delivery team", "source_id": "PF-GW-SQL-001", "status": "open"},
        ],
        "outputs": [],
        "verification": {"status": "passed", "checks": [
            {"name": "packages exist", "ok": True, "detail": "1 work package"},
            {"name": "human approval retained", "ok": True, "detail": "0 auto-approved changes"},
        ]},
        "summary": {"packages": 1, "generated": 1, "gates": 4, "high_gates": 2,
                    "artifacts": 5, "files": 300, "evidence": 101,
                    "feature_evidence": 31, "findings": 24, "dispositions": 12},
        "audit": {"path": "migration/audit.jsonl", "events": 12,
                  "head": "b" * 64, "verified": True},
        "report_path": "migration/MIGRATION-REPORT.md",
        "plan_path": "migration/migration-plan.json",
        "llm": {"status": "off", "mode": "offline", "model": None},
    }


def _evidence() -> list[dict]:
    return [
        {"evidence_id": "EV-0001", "path": "gsrc/acme/Vehicle.gs", "line": 12,
         "excerpt": "class Vehicle {}", "method": "gosu", "confidence": "parsed"},
        {"evidence_id": "EV-0002", "path": "config/entity/PersonalVehicle.eti", "line": 3,
         "excerpt": "<entity name=\"PersonalVehicle\">", "method": "xml", "confidence": "parsed"},
    ]


def _findings() -> list[dict]:
    return [
        {"finding_id": "F-01", "rule_id": "PF-GW-SQL-001", "severity": "error",
         "title": "Direct SQL", "decision": "open"},
        {"finding_id": "F-02", "rule_id": "PF-GW-SQL-001", "severity": "error",
         "title": "Direct SQL", "decision": "open"},
    ]


def _assumptions() -> list[dict]:
    return [
        {"assumption_id": "A-01", "statement": "Territory gap", "impact": "high",
         "status": "open", "related_mapping_id": "M-01", "owner": "Product",
         "question_to_ask": "Which rating source?"},
        {"assumption_id": "A-02", "statement": "Rating input gap", "impact": "medium",
         "status": "open", "related_mapping_id": "M-02", "owner": "Data",
         "question_to_ask": "Provide export?"},
        {"assumption_id": "A-03", "statement": "Long type", "impact": "high",
         "status": "open", "related_mapping_id": "M-03", "owner": "APD",
         "question_to_ask": "Who owns the override?"},
    ]


def _sealed_state() -> dict:
    state = _state()
    target_paths = [
        "config/schema.json",
        "config/mapping.json",
        "config/updater.json",
        "config/installedlobs/codegen_config_ext.yaml",
        "config/installedlobs/api_ext-1.0.yaml",
    ]
    state["packages"] = [
        {
            "package_id": f"WP-{index:02d}",
            "title": f"Generate {target_path}",
            "target_path": target_path,
            "status": "draft_ready",
            "evidence_ids": ["EV-0001"],
            "gate_ids": [],
            "approval": "pending",
        }
        for index, target_path in enumerate(target_paths, start=1)
    ]
    state["bundle"] = {
        "path": "migration/bundle-manifest.json",
        "bytes": 2048,
        "sha256": "c" * 64,
        "file_count": 8,
        "sha256_files": {
            "migration/target/config/schema.json": "1" * 64,
            "migration/target/config/mapping.json": "2" * 64,
            "migration/target/config/updater.json": "3" * 64,
            "migration/target/config/installedlobs/codegen_config_ext.yaml": "4" * 64,
            "migration/target/config/installedlobs/api_ext-1.0.yaml": "5" * 64,
            "migration/migration-plan.json": "6" * 64,
            "migration/MIGRATION-REPORT.md": "7" * 64,
            "migration/audit.jsonl": "8" * 64,
        },
    }
    state["summary"]["artifacts"] = 8
    return state


def _codebase_result() -> dict:
    return {
        "case_id": "cascade-mutual",
        "profile": {"name": "Cascade Mutual", "segment": "Monoline Personal Auto"},
        "status": "green_with_human_gates",
        "mode": "five-agent cyclic",
        "generated_at": "2026-01-01T00:00:00Z",
        "agents": [],
        "iterations": [
            {"iteration": 1, "decision": "rework",
             "architect": {"patches": 7, "mode": "error-first"},
             "guardian": {"verdict": "rework", "blocking": ["warning"]},
             "critic": {"verdict": "rework", "fix_requests": [{"request_id": "FR-1"}]},
             "target": {"findings": 7, "by_severity": {"warning": 7}, "score": 65}},
            {"iteration": 2, "decision": "green",
             "architect": {"patches": 9, "mode": "full"},
             "guardian": {"verdict": "green", "blocking": []},
             "critic": {"verdict": "green", "fix_requests": []},
             "target": {"findings": 0, "by_severity": {}, "score": 100}},
        ],
        "findings": [{"finding_id": "F-1"}],
        "patches": [{"patch_id": "CP-001", "approval": "pending"}],
        "target_files": [{"path": "gsrc/a.gs", "sha256": "a" * 64, "bytes": 1,
                          "content": "class A {}"}],
        "guardian": {"verdict": "green", "summary": "green",
                     "checks": [{"name": "guardian check", "ok": True}]},
        "critic": {
            "verdict": "green", "summary": "green",
            "checks": [{"name": "critic check", "ok": True}],
            "residual_risks": [
                {"risk_id": "CR-01", "category": "data_access", "severity": "high",
                 "title": "Data-access rewrite", "owner": "unassigned",
                 "action": "Run the rating regression.", "rule_ids": ["PF-CODE-SQL-001"],
                 "blocking": False, "human_gate": True, "status": "open"},
            ],
        },
        "planner": {
            "executive_summary": "Compiled",
            "readiness": {"score_before": 0, "structural_score_after": 100,
                          "human_gate_adjusted_score": 74},
            "report_markdown": "# Codebase migration report\n",
            "report_sha256": "b" * 64,
            "next_actions": ["Review the patch.", "Run the regression.",
                             "Verify the audit log."],
        },
        "green_signal": {"unified": True, "gates": 1},
        "source_scan": {"files_scanned": 17, "loc": 156, "by_language": {"Gosu": 10}},
        "sarif": {
            "summary": {"results": 2, "errors": 1, "warnings": 1},
            "path": "code-migration/cascade-mutual.sarif",
            "json": {"version": "2.1.0"},
        },
        "audit": [{"seq": 0, "agent": "scout", "action": "completed"}],
        "audit_verified": True,
        "handoffs": [],
        "stale_green": False,
        "stale_green_reason": None,
    }


def test_migration_view_lists_the_eight_sealed_files_and_manifest_separately() -> None:
    state = _sealed_state()
    before = json.dumps(state, sort_keys=True)
    view = build_migration_view(state)
    assert json.dumps(state, sort_keys=True) == before

    assert len(view["bundle_files"]) == state["bundle"]["file_count"] == 8
    roles = [item["role"] for item in view["bundle_files"]]
    assert roles == [
        "schema", "mapping", "updater", "codegen config", "API contract",
        "plan", "report", "agent log",
    ]
    for item in view["bundle_files"]:
        assert item["sha256"] == state["bundle"]["sha256_files"][item["path"]]
    assert all(
        item["path"] != state["bundle"]["path"] for item in view["bundle_files"]
    )
    assert view["bundle_manifest"]["path"] == state["bundle"]["path"]
    assert view["bundle_manifest"]["sha256"] == state["bundle"]["sha256"]
    assert view["bundle_manifest"]["file_count"] == 8


def test_migration_view_explains_human_gates_and_machine_checks() -> None:
    view = build_migration_view(
        _state(), evidence=_evidence(), findings=_findings(), assumptions=_assumptions()
    )

    summary = view["human_gate_summary"]
    assert summary["assumption_gates"] == 3
    assert summary["rule_groups"] == 1
    assert summary["total"] == 4
    assert summary["high"] == 2
    assert summary["pending_changes"] == 1
    assert summary["approved_changes"] == 0
    assert summary["all_changes_pending"] is True
    assert "3 assumptions + 1 rule groups = 4 human review decisions" in summary["plain_language"]
    assert "2 high impact" in summary["plain_language"]

    assert view["machine_checks"]["total"] == 2
    assert view["machine_checks"]["passed"] == 2
    assert view["machine_checks"]["failed"] == 0

    actions = view["next_actions"]
    assert 3 <= len(actions) <= 5
    joined = " ".join(actions).lower()
    assert "owner" in joined
    assert "assumption" in joined
    assert "approve or reject" in joined
    assert "audit" in joined

    boundary = view["reality_boundary"]
    assert boundary["synthetic"] is True
    assert boundary["actual_migration"] is False
    assert boundary["tenant_contacted"] is False
    assert boundary["compiled"] is False
    assert boundary["official_assurance"] is False
    assert boundary["what_is_real"]
    assert boundary["what_is_not_real"]


def test_migration_view_marks_unassigned_owners_without_inventing_a_person() -> None:
    state = _state()
    state["gates"][0]["owner"] = "unassigned"
    state["gates"][1]["owner"] = ""
    view = build_migration_view(
        state, evidence=_evidence(), findings=_findings(), assumptions=_assumptions()
    )

    unassigned = view["gate_groups"]["assumptions"][0]
    assert unassigned["owner"] == "unassigned"
    assert unassigned["owner_assigned"] is False
    assert unassigned["owner_display"] == "Unassigned — assign before approval"
    assert "Assign an owner" in unassigned["resolution_hint"]

    empty_owner = view["gate_groups"]["assumptions"][1]
    assert empty_owner["owner"] == "unassigned"
    assert empty_owner["owner_assigned"] is False
    assert empty_owner["owner_display"] == "Unassigned — assign before approval"

    assigned = view["gate_groups"]["assumptions"][2]
    assert assigned["owner"] == "APD"
    assert assigned["owner_assigned"] is True
    assert assigned["owner_display"] == "APD"
    assert assigned["resolution_hint"]

    rule_group = view["gate_groups"]["rules"][0]
    assert rule_group["owner_assigned"] is True
    assert rule_group["owner_display"] == "delivery team"
    assert rule_group["resolution_hint"]


def test_migration_view_exposes_evidence_locators_without_client_hydration() -> None:
    evidence = _evidence()
    evidence[0].pop("line", None)
    evidence[0]["locator"] = {
        "kind": "xpath", "value": "/PCF/Screen/TypeKeyInput[1]", "line": 12,
    }
    view = build_migration_view(
        _state(), evidence=evidence, findings=_findings(), assumptions=_assumptions()
    )

    preview = view["evidence_preview"][0]
    assert preview["locator"]["kind"] == "xpath"
    assert preview["locator"]["value"] == "/PCF/Screen/TypeKeyInput[1]"
    assert preview["locator_kind"] == "xpath"
    assert preview["locator_value"] == "/PCF/Screen/TypeKeyInput[1]"
    assert preview["line"] == 12


def test_codebase_view_exposes_report_bundle_and_reviewer_summary() -> None:
    from app.services.code_migration import build_codebase_view

    result = _codebase_result()
    before = json.dumps(result, sort_keys=True, default=str)
    view = build_codebase_view(result)
    assert json.dumps(result, sort_keys=True, default=str) == before

    roles = [item["role"] for item in view["bundle_files"]]
    assert roles == ["report", "SARIF", "patches", "target", "audit log"]
    assert view["report_artifacts"] == view["bundle_files"]

    report = next(item for item in view["bundle_files"] if item["role"] == "report")
    assert report["sha256"] == "b" * 64
    patches = next(item for item in view["bundle_files"] if item["role"] == "patches")
    assert patches["count"] == 1
    assert patches["pending"] == 1
    target = next(item for item in view["bundle_files"] if item["role"] == "target")
    assert target["count"] == 1
    audit = next(item for item in view["bundle_files"] if item["role"] == "audit log")
    assert audit["events"] == 1
    assert audit["verified"] is True

    summary = view["human_gate_summary"]
    assert summary["total"] == 1
    assert summary["high"] == 1
    assert summary["pending_patches"] == 1
    assert summary["all_patches_pending"] is True
    assert summary["unassigned_owners"] == 1

    machine = view["machine_check_summary"]
    assert machine["guardian"]["total"] == 1
    assert machine["critic"]["total"] == 1
    assert machine["total"] == 2
    assert machine["passed"] == 2

    assert len(view["next_actions"]) >= 3
    assert "Assign an owner" in view["next_actions"][0]

    boundary = view["reality_boundary"]
    assert boundary["synthetic"] is True
    assert boundary["actual_migration"] is False
    assert boundary["tenant_contacted"] is False
    assert boundary["compiled"] is False
    assert boundary["official_assurance"] is False

    story = view["iteration_story"]
    assert story[0]["target_label"] == "warning: 7 · error: 0"
    assert story[1]["target_label"] == "warning: 0 · error: 0"
    assert all(isinstance(item["target_label"], str) for item in story)

    fallback = view["gate_owner_fallback"]
    assert len(fallback) == 1
    assert fallback[0]["risk_id"] == "CR-01"
    assert fallback[0]["owner_display"] == "Unassigned — assign before approval"
    assert fallback[0]["owner_assigned"] is False
    assert view["critic"]["residual_risks"][0]["owner_assigned"] is False
    assert view["critic"]["residual_risks"][0]["resolution_hint"]


def test_migration_view_exposes_five_stages_and_handoffs() -> None:
    view = build_migration_view(
        _state(), evidence=_evidence(), findings=_findings(), assumptions=_assumptions()
    )

    assert [stage["agent_id"] for stage in view["stages"]] == [
        "scout", "architect", "guardian", "critic", "scribe"
    ]
    assert view["stages"][0]["name"] == "Scout"
    assert "received" in view["stages"][0]
    assert "produced" in view["stages"][0]
    assert "handoff" in view["stages"][0]
    assert view["stages"][1]["received"]
    assert "Scout" in " ".join(view["stages"][1]["received"])
    assert len(view["handoffs"]) == 5
    assert view["handoffs"][0]["from"] == "scout"
    assert view["handoffs"][0]["to"] == "architect"
    assert view["handoffs"][-1]["to"] == "sealed bundle"


def test_migration_view_groups_the_eleven_gate_story() -> None:
    view = build_migration_view(
        _state(), evidence=_evidence(), findings=_findings(), assumptions=_assumptions()
    )

    assert len(view["gate_groups"]["assumptions"]) == 3
    assert len(view["gate_groups"]["rules"]) == 1
    assert view["gate_groups"]["rules"][0]["rule_id"] == "PF-GW-SQL-001"
    assert view["gate_groups"]["rules"][0]["count"] == 2
    assert "3 assumption gates" in view["narrative"]
    assert "Scribe sealed" in view["narrative"]


def test_migration_view_is_explainable_without_context() -> None:
    view = build_migration_view(
        _state(), evidence=_evidence(), findings=_findings(), assumptions=_assumptions()
    )

    explain = view["explain"]
    assert explain["headline"]
    assert explain["plain_language"]
    assert explain["why_it_matters"]
    assert explain["what_to_look_at"]
    assert len(view["glossary"]) >= 5
    assert view["stages"][0]["plain_language"]


def test_migration_view_does_not_mutate_source_state() -> None:
    state = _state()
    before = json.dumps(state, sort_keys=True)
    build_migration_view(
        state, evidence=_evidence(), findings=_findings(), assumptions=_assumptions()
    )
    assert json.dumps(state, sort_keys=True) == before


def test_llm_config_is_env_only_and_never_exposes_the_key(monkeypatch) -> None:
    from app.services.llm import LLMConfig

    config = LLMConfig.from_env({
        "PREFLIGHT_LLM_MODE": "live",
        "PREFLIGHT_LLM_BASE_URL": "https://example.test/v1",
        "PREFLIGHT_LLM_API_KEY": "secret-key-value",
        "PREFLIGHT_LLM_MODEL": "mimo-v2.6-flash",
    })
    assert config.configured is True
    assert config.public()["configured"] is True
    assert config.public()["base_host"] == "example.test"
    assert "secret-key-value" not in json.dumps(config.public())
    assert "api_key" not in config.public()
    assert config.public()["models"] == ["mimo-v2.6-flash", "mimo-v2.6-pro"]


def test_llm_config_requires_base_url_and_key() -> None:
    from app.services.llm import LLMConfig

    config = LLMConfig.from_env({"PREFLIGHT_LLM_MODE": "live"})
    assert config.configured is False
    assert config.public()["configured"] is False


def test_llm_chat_json_uses_openai_protocol_and_returns_usage() -> None:
    from app.services.llm import LLMConfig, chat_json

    seen: dict[str, str] = {}

    def handler(request: httpx.Request) -> httpx.Response:
        seen["url"] = str(request.url)
        seen["auth"] = request.headers.get("authorization", "")
        return httpx.Response(
            200,
            json={
                "id": "cmpl-1",
                "model": "mimo-v2.6-pro",
                "choices": [{"message": {"content": '{"headline": "ok"}'}}],
                "usage": {"prompt_tokens": 10, "completion_tokens": 4, "total_tokens": 14},
            },
        )

    config = LLMConfig.from_env({
        "PREFLIGHT_LLM_MODE": "live",
        "PREFLIGHT_LLM_BASE_URL": "https://example.test/v1",
        "PREFLIGHT_LLM_API_KEY": "secret-key-value",
        "PREFLIGHT_LLM_MODEL": "mimo-v2.6-pro",
    })
    result = chat_json(
        [{"role": "user", "content": "return json"}],
        config=config,
        transport=httpx.MockTransport(handler),
    )
    assert seen["url"].endswith("/chat/completions")
    assert seen["auth"].startswith("Bearer ")
    assert result["data"]["headline"] == "ok"
    assert result["model"] == "mimo-v2.6-pro"
    assert result["usage"]["total_tokens"] == 14
    assert result["response_sha256"]
    assert "secret-key-value" not in json.dumps(result)


def test_llm_annotation_drops_ungrounded_citations() -> None:
    from app.services.llm import validate_migration_annotation

    payload = {
        "headline": "Scout found a scope",
        "observations": [
            {"text": "Vehicle class exists", "evidence_ids": ["EV-0001"]},
            {"text": "Invented claim", "evidence_ids": ["EV-9999"]},
        ],
        "unknowns": ["No rating table"],
    }
    cleaned = validate_migration_annotation(
        "scout", payload, allowed_evidence={"EV-0001"}, allowed_rules=set()
    )
    assert len(cleaned["observations"]) == 1
    assert cleaned["observations"][0]["evidence_ids"] == ["EV-0001"]
    assert cleaned["dropped_ungrounded"] == 1


def test_codebase_view_has_plain_language_narrative() -> None:
    from app.services.code_migration import build_codebase_view

    result = {
        "case_id": "cascade-mutual",
        "profile": {"name": "Cascade Mutual", "segment": "Monoline Personal Auto"},
        "status": "green_with_human_gates",
        "mode": "five-agent cyclic",
        "generated_at": "2026-01-01T00:00:00Z",
        "agents": [
            {"agent": "scout", "name": "Scout", "role": "Inventory", "status": "done",
             "summary": "17 files"},
            {"agent": "architect", "name": "Architect", "role": "Draft", "status": "done",
             "summary": "22 patches"},
            {"agent": "guardian", "name": "Guardian", "role": "Gate", "status": "done",
             "summary": "13 checks"},
            {"agent": "critic", "name": "Critic", "role": "Review", "status": "done",
             "summary": "7 checks"},
            {"agent": "planner", "name": "Planner", "role": "Report", "status": "done",
             "summary": "compiled"},
        ],
        "iterations": [
            {"iteration": 1, "decision": "rework",
             "architect": {"patches": 18, "mode": "error-first"},
             "guardian": {"verdict": "rework", "blocking": ["warning"]},
             "critic": {"verdict": "rework", "fix_requests": [{"request_id": "FR-1"}]}},
            {"iteration": 2, "decision": "green",
             "architect": {"patches": 22, "mode": "full"},
             "guardian": {"verdict": "green", "blocking": []},
             "critic": {"verdict": "green", "fix_requests": []}},
        ],
        "findings": [{"finding_id": "F-1"}],
        "patches": [{"patch_id": "CP-001"}],
        "guardian": {"verdict": "green", "checks": [], "summary": "green"},
        "critic": {"verdict": "green", "checks": [], "residual_risks": [], "summary": "green"},
        "planner": {"executive_summary": "Compiled", "readiness": {"score_before": 0,
                    "structural_score_after": 100, "human_gate_adjusted_score": 74}},
        "green_signal": {"unified": True, "gates": 10},
        "source_scan": {"files_scanned": 17, "loc": 156, "by_language": {"Gosu": 10}},
        "handoffs": [],
        "audit_verified": True,
        "audit": [],
    }
    view = build_codebase_view(result)
    assert len(view["stages"]) == 5
    assert "Scout" in view["narrative"]
    assert "iteration 1" in view["narrative"].lower()
    assert view["explain"]["headline"]
    assert view["explain"]["what_to_look_at"]


def test_source_has_no_hardcoded_mimo_key_or_base_url() -> None:
    root = Path(__file__).resolve().parents[1] / "app"
    text = "\n".join(
        path.read_text(encoding="utf-8", errors="ignore")
        for path in root.rglob("*.py")
    )
    assert "tp-sg26" not in text
    assert "token-plan-sgp" not in text
    assert "xiaomimimo.com" not in text
    assert "token-plan-sgp.xiaomimimo.com" not in text


def test_env_example_exists_without_secrets() -> None:
    root = Path(__file__).resolve().parents[1]
    example = root / ".env.example"
    assert example.is_file()
    text = example.read_text(encoding="utf-8")
    assert "PREFLIGHT_LLM_BASE_URL" in text
    assert "PREFLIGHT_LLM_API_KEY" in text
    assert "tp-sg26" not in text
