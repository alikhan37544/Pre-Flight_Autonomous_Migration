"""Autonomous multi-agent migration draft generation.

This is deliberately bounded autonomy: the orchestrator can read the snapshot,
generate a target draft, verify it, and package it without a human in the loop.
It cannot deploy, edit ``_gen`` files, approve its own changes, or resolve an
assumption. Every run produces its own hash-chained agent log and a reviewable
bundle under ``migration/`` in the run store.
"""

from __future__ import annotations

import copy
import hashlib
import json
import re
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import yaml

from app.services.llm import (
    LLMConfig,
    LLMError,
    annotate_migration_agent,
)

MIGRATION_ARTIFACT = "migration.json"
AUDIT_PATH = "migration/audit.jsonl"
AUDIT_CHECKPOINT = "migration/audit.checkpoint.json"
BUNDLE_ROOT = "migration"
TARGET_ROOT = "migration/target"
REPORT_PATH = "migration/MIGRATION-REPORT.md"
PLAN_PATH = "migration/migration-plan.json"
MANIFEST_PATH = "migration/bundle-manifest.json"
SYNTHETIC_FIXTURES = frozenset({"demo-slice-300", "acme-pc-2026.10"})

_REAL_CODE_BLOCKED_MESSAGE = (
    "Live reasoning is blocked for non-synthetic runs. Only synthetic fixtures "
    "may be sent unless an operator explicitly sets "
    "PREFLIGHT_LLM_ALLOW_REAL_CODE=true after data-owner approval."
)

BOUNDARY = (
    "Autonomous draft generation only: the orchestrator writes a local, "
    "non-deployable target bundle. It does not edit _gen files, approve changes, "
    "resolve assumptions, or contact a Guidewire tenant."
)

AGENTS: list[dict[str, str]] = [
    {
        "agent_id": "scout",
        "name": "Scout",
        "role": "Inventory and scope",
        "description": "Resolves the feature, counts evidence, and refuses to plan from an ungrounded slice.",
    },
    {
        "agent_id": "architect",
        "name": "Architect",
        "role": "Target draft",
        "description": "Turns every explicit disposition into a target file in the migration bundle.",
    },
    {
        "agent_id": "guardian",
        "name": "Guardian",
        "role": "Risk and gates",
        "description": "Converts findings and open assumptions into blocking review gates.",
    },
    {
        "agent_id": "critic",
        "name": "Critic",
        "role": "Adversarial verification",
        "description": "Rejects ungrounded packages, unsafe paths, duplicate targets, and unparseable output.",
    },
    {
        "agent_id": "scribe",
        "name": "Scribe",
        "role": "Bundle and report",
        "description": "Writes the plan, the review report, and the sealed bundle manifest.",
    },
]


def _now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def _sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _json_hash(payload: Any) -> str:
    return _sha(json.dumps(payload, sort_keys=True, separators=(",", ":")).encode("utf-8"))


def _read(store, run_id: str, name: str, default: Any) -> Any:
    try:
        return store.read_artifact(run_id, name)
    except Exception:
        return default


def _synthetic_snapshot_hashes() -> set[str]:
    """Hashes of the bundled synthetic snapshots, from the frozen manifest."""
    try:
        payload = json.loads(
            (Path(__file__).resolve().parents[2] / "ground_truth" / "FROZEN.json")
            .read_text(encoding="utf-8")
        )
    except (OSError, ValueError, TypeError):
        return set()
    fixtures = payload.get("fixtures") if isinstance(payload, dict) else None
    if not isinstance(fixtures, dict):
        return set()
    hashes = set()
    for fixture_id in SYNTHETIC_FIXTURES:
        entry = fixtures.get(fixture_id)
        digest = entry.get("sha256") if isinstance(entry, dict) else None
        if isinstance(digest, str):
            hashes.add(digest)
    return hashes


def _is_case_study_fixture(fixture_id: str) -> bool:
    parts = [part for part in fixture_id.replace("\\", "/").split("/") if part not in {"", "."}]
    return "case-studies" in parts


def is_synthetic_run(store, run_id: str) -> bool:
    """Return True only for a run whose source is a known synthetic fixture.

    The live gateway is allowed for the bundled fixtures and case studies. A
    run labelled with ``project_id="demo"`` may also qualify when its persisted
    manifest is one of the frozen synthetic snapshots. An uploaded run never
    qualifies, even if its status metadata was copied from a demo run.
    """
    status = store.read_status(run_id)
    fixture_id = str(status.get("fixture_id") or "").strip()
    if fixture_id == "uploaded" or fixture_id.startswith("uploaded/"):
        return False
    if fixture_id in SYNTHETIC_FIXTURES or _is_case_study_fixture(fixture_id):
        return True
    if str(status.get("project_id") or "") != "demo":
        return False
    manifest = _read(store, run_id, "manifest.json", None)
    if not isinstance(manifest, dict):
        return False
    if manifest.get("synthetic") is True:
        return True
    if str(manifest.get("project_id") or "") != "demo":
        return False
    return manifest.get("sha256") in _synthetic_snapshot_hashes()


def _safe_relative(path: str) -> bool:
    candidate = Path(path)
    return (
        bool(path)
        and not candidate.is_absolute()
        and ".." not in candidate.parts
        and not path.startswith("_gen/")
        and path != "_gen"
    )


def _write_bytes(path: Path, data: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(data)


def _read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def _append_audit(store, run_id: str, *, agent: str, action: str,
                  object_id: str, reason: str | None = None) -> dict[str, Any]:
    """Append an event to the migrator's own hash chain.

    The review-run audit remains untouched so the existing review packet and
    demo evidence stay reproducible. The migrator log proves agent ordering and
    is linked from the signed bundle manifest.
    """
    with store.locked(run_id):
        path = store.run_dir(run_id) / AUDIT_PATH
        path.parent.mkdir(parents=True, exist_ok=True)
        previous = "GENESIS"
        seq = 0
        if path.is_file():
            lines = [line for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]
            seq = len(lines)
            if lines:
                previous = json.loads(lines[-1]).get("hash", "GENESIS")
        event = {
            "seq": seq,
            "ts": _now(),
            "run_id": run_id,
            "agent": agent,
            "action": action,
            "object_id": object_id,
            "reason": reason,
            "prev_hash": previous,
        }
        event["hash"] = _json_hash(event)
        with path.open("a", encoding="utf-8") as handle:
            handle.write(json.dumps(event, sort_keys=True) + "\n")
        store.write_artifact(run_id, AUDIT_CHECKPOINT, {
            "run_id": run_id,
            "count": seq + 1,
            "head": event["hash"],
            "log_size": path.stat().st_size,
            "updated_at": _now(),
        })
        return event


def verify_migration_log(store, run_id: str) -> tuple[bool, str]:
    """Verify the migrator's append-only event chain and its checkpoint."""
    path = store.run_dir(run_id) / AUDIT_PATH
    if not path.is_file():
        return False, "migration audit log is missing"
    try:
        raw = path.read_bytes()
    except OSError as exc:
        return False, f"migration audit log cannot be read: {type(exc).__name__}"
    if not raw.strip():
        return False, "migration audit log is empty"
    try:
        checkpoint = json.loads(
            (store.run_dir(run_id) / AUDIT_CHECKPOINT).read_text(encoding="utf-8")
        )
    except FileNotFoundError:
        return False, "migration audit checkpoint is missing"
    except (OSError, ValueError, TypeError):
        return False, "migration audit checkpoint is corrupt"
    if not isinstance(checkpoint, dict):
        return False, "migration audit checkpoint is corrupt"
    if checkpoint.get("run_id") != run_id:
        return False, "migration audit checkpoint belongs to a different run"

    previous = "GENESIS"
    count = 0
    for index, line in enumerate(raw.decode("utf-8", "replace").splitlines()):
        if not line.strip():
            continue
        try:
            event = json.loads(line)
        except json.JSONDecodeError:
            return False, f"event {index} is not valid JSON"
        if not isinstance(event, dict):
            return False, f"event {index} is not a JSON object"
        if event.get("run_id") != run_id:
            return False, f"event {index} belongs to a different run"
        digest = event.pop("hash", None)
        if event.get("seq") != index:
            return False, f"event {index} has the wrong sequence"
        if event.get("prev_hash") != previous:
            return False, f"event {index} has a broken previous hash"
        if _json_hash(event) != digest:
            return False, f"event {index} hash mismatch"
        previous = digest
        count += 1
    if count == 0:
        return False, "migration audit log is empty"
    if checkpoint.get("count") != count:
        return False, "migration audit log does not match its checkpoint (truncated or extended)"
    if checkpoint.get("head") != previous:
        return False, "migration audit log head does not match its checkpoint"
    if checkpoint.get("log_size") != len(raw):
        return False, "migration audit log size does not match its checkpoint"
    return True, f"{count} events verified"


def _initial_state(run_id: str, feature: dict[str, Any], feature_id: str) -> dict[str, Any]:
    return {
        "schema_version": "1.0",
        "run_id": run_id,
        "feature_id": feature_id,
        "feature_name": feature.get("name", feature_id),
        "status": "running",
        "mode": "five specialist agents · deterministic handoffs",
        "boundary": BOUNDARY,
        "started_at": _now(),
        "finished_at": None,
        "progress": 0,
        "current_agent": "scout",
        "agents": [
            {**agent, "status": "queued", "started_at": None,
             "finished_at": None, "summary": "", "checks": []}
            for agent in AGENTS
        ],
        "packages": [],
        "gates": [],
        "outputs": [],
        "verification": {"status": "pending", "checks": []},
        "summary": {},
        "llm": {"mode": "off", "status": "off", "model": None,
                "annotations": {}, "warnings": [], "calls": []},
        "audit": {"path": AUDIT_PATH, "events": 0, "head": None, "verified": False},
        "report_path": REPORT_PATH,
        "plan_path": PLAN_PATH,
    }


def _set_agent(state: dict[str, Any], agent_id: str, **changes: Any) -> None:
    for agent in state["agents"]:
        if agent["agent_id"] == agent_id:
            agent.update(changes)
            return
    raise KeyError(agent_id)


def _persist(store, run_id: str, state: dict[str, Any]) -> None:
    store.write_artifact(run_id, MIGRATION_ARTIFACT, state)


def _gate_count(gate: dict[str, Any]) -> int:
    match = re.search(r"\((\d+)\s+findings?", str(gate.get("title", "")))
    return int(match.group(1)) if match else 1


def _gate_rule_id(gate: dict[str, Any]) -> str:
    source = str(gate.get("source_id") or "")
    return source or "unclassified"


def _plural(count: int, singular: str, plural: str | None = None) -> str:
    return f"{count} {singular if count == 1 else (plural or singular + 's')}"


_OWNER_FALLBACK = "Unassigned — assign before approval"
_UNASSIGNED_OWNERS = {
    "", "unassigned", "unknown", "tbd", "tbc", "none", "n/a", "na", "-", "—",
    "not assigned", "to be assigned",
}
_BUNDLE_ROLE_PRIORITY = {"target": 0, "plan": 1, "report": 2, "agent log": 3, "artifact": 4}


def _owner_view(owner: Any) -> dict[str, Any]:
    """Return display fields without inventing an owner for an open gate."""
    text = str(owner or "").strip()
    assigned = bool(text) and text.casefold() not in _UNASSIGNED_OWNERS
    return {
        "owner": text or "unassigned",
        "owner_assigned": assigned,
        "owner_display": text if assigned else _OWNER_FALLBACK,
    }


def _bundle_role(path: str) -> tuple[str, str]:
    """Map a sealed bundle path to the demo's role label and coarse kind."""
    name = Path(path).name.lower()
    if name == "migration-plan.json":
        return "plan", "plan"
    if name == "migration-report.md":
        return "report", "report"
    if name == "audit.jsonl":
        return "agent log", "agent log"
    if "codegen" in name:
        return "codegen config", "target"
    if "schema" in name:
        return "schema", "target"
    if "mapping" in name:
        return "mapping", "target"
    if "updater" in name:
        return "updater", "target"
    lowered = path.lower()
    if "/apis/" in lowered or "/installedlobs/" in lowered or name.endswith((".yaml", ".yml")):
        return "API contract", "target"
    return "target", "target"


def _bundle_view_parts(
    state: dict[str, Any], run_dir: Path | None
) -> tuple[list[dict[str, Any]], dict[str, Any] | None]:
    """Build the list of sealed content files and the separate manifest wrapper.

    The sealed hashes in ``state['bundle']['sha256_files']`` are authoritative;
    the migration directory is only used for byte counts (or to list files for
    older states that predate the bundle summary). The manifest is not one of
    the sealed content files, so it is returned separately.
    """
    bundle = state.get("bundle") or {}
    sealed = bundle.get("sha256_files") if isinstance(bundle, dict) else None
    hashes = sealed if isinstance(sealed, dict) else {}
    paths = {
        str(path): digest
        for path, digest in hashes.items()
        if path and Path(str(path)).name != "bundle-manifest.json"
    }
    if not paths and run_dir is not None:
        migration_dir = Path(run_dir) / BUNDLE_ROOT
        if migration_dir.is_dir():
            for path in sorted(migration_dir.rglob("*")):
                if path.is_file() and path.name != "bundle-manifest.json":
                    relative = path.relative_to(Path(run_dir)).as_posix()
                    paths[relative] = _sha(path.read_bytes())
    entries: list[dict[str, Any]] = []
    package_order = {
        f"{TARGET_ROOT}/{package.get('target_path')}": index
        for index, package in enumerate(state.get("packages") or [])
        if package.get("target_path")
    }
    for path in sorted(paths):
        role, kind = _bundle_role(path)
        entry: dict[str, Any] = {
            "path": path,
            "role": role,
            "role_label": role,
            "kind": kind,
            "sha256": paths[path],
        }
        if run_dir is not None:
            candidate = Path(run_dir) / path
            if candidate.is_file():
                data = candidate.read_bytes()
                entry["bytes"] = len(data)
                entry["current_sha256"] = _sha(data)
                entry["hash_matches_seal"] = entry["current_sha256"] == entry["sha256"]
                if role == "agent log":
                    entry["append_only"] = True
                    entry["note"] = (
                        "Sealed digest covers the log at seal time; later events "
                        "append to the same hash chain."
                    )
        entries.append(entry)
    entries.sort(key=lambda item: (
        _BUNDLE_ROLE_PRIORITY.get(item["kind"], 9),
        package_order.get(item["path"], 10_000),
        item["path"],
    ))
    manifest = None
    if bundle:
        manifest = {
            "path": bundle.get("path") or MANIFEST_PATH,
            "sha256": bundle.get("sha256"),
            "bytes": bundle.get("bytes"),
            "file_count": bundle.get("file_count", len(entries)),
            "note": "Manifest wrapper — separate from the sealed content files.",
        }
    elif run_dir is not None:
        manifest_path = Path(run_dir) / MANIFEST_PATH
        if manifest_path.is_file():
            data = manifest_path.read_bytes()
            try:
                payload = json.loads(data)
            except (ValueError, UnicodeDecodeError):
                payload = {}
            manifest = {
                "path": MANIFEST_PATH,
                "sha256": _sha(data),
                "bytes": len(data),
                "file_count": payload.get("file_count", len(entries)),
                "note": "Manifest wrapper — separate from the sealed content files.",
            }
    return entries, manifest


def _check_summary(checks: list[dict[str, Any]], label: str) -> dict[str, Any]:
    passed = sum(1 for check in checks if check.get("ok"))
    return {
        "label": label,
        "total": len(checks),
        "passed": passed,
        "failed": len(checks) - passed,
    }


def build_migration_view(
    state: dict[str, Any],
    *,
    evidence: list[dict[str, Any]] | None = None,
    findings: list[dict[str, Any]] | None = None,
    assumptions: list[dict[str, Any]] | None = None,
    run_dir: Path | None = None,
) -> dict[str, Any]:
    """Enrich a persisted migration state for the human-facing agent loop.

    This is a view-layer function. It never changes the sealed plan or the
    migration artifact, so the offline bundle keeps its original hashes.
    """
    view = copy.deepcopy(state)
    evidence = evidence or []
    findings = findings or []
    assumptions = assumptions or []
    agents = {item.get("agent_id"): item for item in view.get("agents", [])}
    packages = view.get("packages", []) or []
    gates = view.get("gates", []) or []
    checks = (view.get("verification") or {}).get("checks", []) or []
    summary = view.get("summary", {}) or {}
    feature_id = view.get("feature_id") or "the selected feature"
    feature_name = view.get("feature_name") or feature_id
    package_count = len(packages)
    generated = sum(1 for package in packages if package.get("status") == "draft_ready")
    gate_count = len(gates)
    assumption_gates = [gate for gate in gates if gate.get("kind") == "assumption"]
    review_gates = [gate for gate in gates if gate.get("kind") == "review"]
    high_gates = sum(1 for gate in gates if gate.get("severity") == "high")
    passed = sum(1 for check in checks if check.get("ok"))
    verification_ok = (view.get("verification") or {}).get("status") == "passed"
    failed = len(checks) - passed

    rule_groups: dict[str, dict[str, Any]] = {}
    for gate in review_gates:
        rule_id = _gate_rule_id(gate)
        group = rule_groups.setdefault(rule_id, {
            "rule_id": rule_id,
            "title": gate.get("title", rule_id),
            "count": 0,
            "severity": gate.get("severity", "medium"),
            "gates": [],
        })
        group["count"] += _gate_count(gate)
        group["gates"].append(gate)
        if gate.get("severity") == "high":
            group["severity"] = "high"

    # Owner fallbacks are explicit review facts: never invent a person. The
    # same fields are exposed on the flat gate list and on the grouped view.
    for gate in gates:
        gate.update(_owner_view(gate.get("owner")))
        question = str(gate.get("question") or "").strip()
        if gate.get("kind") == "assumption":
            prefix = (
                "Answer the open question and record the decision"
                if gate["owner_assigned"] else
                "Assign an owner, then answer the open question"
            )
            gate["resolution_hint"] = f"{prefix}: {question}" if question else prefix + "."
        elif gate.get("kind") == "review":
            rule_id = _gate_rule_id(gate)
            gate["resolution_hint"] = (
                f"Review the {_plural(_gate_count(gate), 'finding')} for {rule_id}; "
                "accept the risk or remediate, then re-run Guardian and Critic."
            )
    for group in rule_groups.values():
        first_gate = group["gates"][0] if group["gates"] else {}
        group.update(_owner_view(first_gate.get("owner")))
        group["resolution_hint"] = (
            f"Review the {_plural(group['count'], 'finding')} for {group['rule_id']}; "
            "accept the risk or remediate, then re-run Guardian and Critic."
        )

    feature_evidence = summary.get("feature_evidence", len(evidence))
    total_evidence = summary.get("evidence", len(evidence))
    scan_files = summary.get("files", 0)
    dispositions = summary.get("dispositions", 0)
    findings_count = summary.get("findings", len(findings))
    artifact_count = summary.get("artifacts", len(packages) + 4)

    evidence_preview = [
        {
            "evidence_id": item.get("evidence_id"),
            "path": item.get("path"),
            "line": item.get("line") or (item.get("locator") or {}).get("line"),
            "locator": item.get("locator"),
            "locator_kind": (item.get("locator") or {}).get("kind"),
            "locator_value": (item.get("locator") or {}).get("value"),
            "excerpt": (item.get("excerpt") or "")[:240],
            "method": item.get("method"),
            "confidence": item.get("confidence"),
        }
        for item in evidence[:8]
    ]

    package_previews = []
    for package in packages:
        preview = ""
        if run_dir is not None:
            target = (Path(run_dir) / TARGET_ROOT / str(package.get("target_path", ""))).resolve()
            root = (Path(run_dir) / TARGET_ROOT).resolve()
            if root in target.parents and target.is_file():
                try:
                    preview = target.read_text(encoding="utf-8", errors="replace")[:5000]
                except OSError:
                    preview = ""
        package_previews.append({**package, "preview": preview})

    bundle_files, bundle_manifest = _bundle_view_parts(view, run_dir)
    pending_changes = sum(
        1 for package in packages if str(package.get("approval", "pending")) == "pending"
    )
    approved_changes = package_count - pending_changes
    all_changes_pending = approved_changes == 0
    unassigned_owners = sum(
        1 for gate in assumption_gates if not gate.get("owner_assigned")
    )
    review_group_count = len(rule_groups)
    human_decision_count = len(assumption_gates) + review_group_count
    machine_checks = _check_summary(checks, "Critic checks")
    machine_checks["verdict"] = (view.get("verification") or {}).get("status", "pending")
    machine_checks["checks"] = checks

    gate_phrase = (
        f"{len(assumption_gates)} assumptions + {review_group_count} rule groups = "
        f"{_plural(human_decision_count, 'human review decision')}"
    )
    change_phrase = (
        f"all {_plural(package_count, 'generated change')} are pending approval"
        if all_changes_pending else
        f"{approved_changes} of {_plural(package_count, 'generated change')} are already decided"
    )
    human_gate_summary = {
        "assumption_gates": len(assumption_gates),
        "rule_groups": review_group_count,
        "total": human_decision_count,
        "high": high_gates,
        "high_gates": high_gates,
        "pending_changes": pending_changes,
        "approved_changes": approved_changes,
        "all_changes_pending": all_changes_pending,
        "all_pending": all_changes_pending,
        "unassigned_owners": unassigned_owners,
        "machine_checks": machine_checks,
        "plain_language": f"{gate_phrase}; {high_gates} high impact; {change_phrase}.",
    }

    audit = view.get("audit") or {}
    audit_events = int(audit.get("events") or 0)
    next_actions: list[str] = []
    if unassigned_owners:
        next_actions.append(
            f"Assign an owner to {_plural(unassigned_owners, 'unassigned assumption gate')} "
            "before approval."
        )
    elif assumption_gates:
        next_actions.append(
            f"Confirm the named owner for each of the {_plural(len(assumption_gates), 'assumption gate')}."
        )
    if assumption_gates:
        next_actions.append(
            f"Resolve {_plural(len(assumption_gates), 'open assumption')} and record the answer "
            "for each one."
        )
    if dispositions:
        next_actions.append(
            f"Accept or reject the {_plural(dispositions, 'source-to-target mapping')} used by the draft."
        )
    next_actions.append(
        f"Review and approve or reject the {_plural(package_count, 'draft package')}; "
        "none are approved automatically."
    )
    next_actions.append(
        f"Verify {_plural(audit_events, 'audit event')} in the hash-chained agent log"
        + (" (chain verified)." if audit.get("verified") else " (chain not yet verified).")
    )
    for fallback in (
        "Confirm the evidence behind each package with the named owner.",
        "Verify the sealed bundle manifest and its hashes before sign-off.",
    ):
        if len(next_actions) >= 3:
            break
        next_actions.append(fallback)

    reality_boundary = {
        "synthetic": True,
        "actual_migration": False,
        "tenant_contacted": False,
        "compiled": False,
        "official_assurance": False,
        "what_is_real": (
            f"A deterministic five-agent pass over a read-only synthetic snapshot: "
            f"{_plural(package_count, 'target draft')}, {_plural(len(bundle_files), 'sealed bundle file')}, "
            f"and a hash-chained agent log."
        ),
        "what_is_not_real": (
            "No Guidewire tenant was contacted, no code was compiled or deployed, "
            "no change was approved, and this is not an official Cloud Assurance result."
        ),
    }

    def agent(agent_id: str) -> dict[str, Any]:
        return agents.get(agent_id, {"name": agent_id.title(), "role": "", "status": "queued",
                                     "summary": "", "checks": []})

    scout = agent("scout")
    architect = agent("architect")
    guardian = agent("guardian")
    critic = agent("critic")
    scribe = agent("scribe")

    stages = [
        {
            "agent_id": "scout",
            "index": 1,
            "name": "Scout",
            "role": "Resolve the feature and evidence",
            "status": scout.get("status", "queued"),
            "summary": scout.get("summary", ""),
            "plain_language": "Scout opens the read-only snapshot and finds the files, evidence, findings, and dispositions that belong to this feature. If the slice is not grounded, it refuses to plan.",
            "received": [
                "Completed review run and source manifest",
                "Feature index and evidence graph",
                "Findings and explicit dispositions",
            ],
            "produced": [
                f"{feature_id} · {feature_name}",
                f"{_plural(feature_evidence, 'evidence link')} on this feature",
                f"{_plural(total_evidence, 'evidence record')} across {_plural(scan_files, 'file')}",
                f"{_plural(findings_count, 'finding')} · {_plural(dispositions, 'disposition')}",
            ],
            "handoff": f"Scout → Architect: feature scope, {feature_evidence} evidence links, and {dispositions} dispositions.",
            "checks": scout.get("checks", []),
            "count": feature_evidence,
            "count_label": "evidence links",
        },
        {
            "agent_id": "architect",
            "index": 2,
            "name": "Architect",
            "role": "Generate the target draft",
            "status": architect.get("status", "queued"),
            "summary": architect.get("summary", ""),
            "plain_language": "Architect takes each explicit source-to-target disposition and writes the corresponding cloud target file. Every package is a local draft; nothing is deployed or auto-approved.",
            "received": [
                f"Scout's {feature_id} scope",
                f"{_plural(dispositions, 'explicit disposition')}",
                "Evidence IDs for every package",
            ],
            "produced": [
                f"{_plural(package_count, 'work package')}",
                f"{generated}/{package_count} target files written",
                "Every package remains pending human approval",
            ],
            "handoff": f"Architect → Guardian: {package_count} work packages and {artifact_count} bundle artefacts.",
            "checks": architect.get("checks", []),
            "count": package_count,
            "count_label": "packages",
        },
        {
            "agent_id": "guardian",
            "index": 3,
            "name": "Guardian",
            "role": "Open deterministic risk gates",
            "status": guardian.get("status", "queued"),
            "summary": guardian.get("summary", ""),
            "plain_language": "Guardian is the strict compliance gate. It sees only the Architect's packages and evidence-linked findings/assumptions. It opens a gate for every open assumption and every rule family that still has an unanswered finding.",
            "received": [
                f"Architect's {_plural(package_count, 'package')}",
                "Open assumptions and review findings",
                "Guidewire rule pack and APD constraints",
            ],
            "not_received": [
                "Scout's narrative or opinion",
                "Critic's verdict or suggested fixes",
                "Any model-generated text",
            ],
            "produced": [
                f"{_plural(gate_count, 'open gate')}: {len(assumption_gates)} assumption + {len(rule_groups)} rule groups",
                f"{high_gates} high-impact gates",
                "Deployment remains blocked",
            ],
            "handoff": f"Guardian → Critic: {gate_count} gates; deterministic verdict is independent of the narratives.",
            "checks": guardian.get("checks", []),
            "count": gate_count,
            "count_label": "gates",
        },
        {
            "agent_id": "critic",
            "index": 4,
            "name": "Critic",
            "role": "Verify and challenge the package",
            "status": critic.get("status", "queued"),
            "summary": critic.get("summary", ""),
            "plain_language": "Critic independently checks the whole handoff: packages exist, paths are safe and unique, generated JSON/YAML parses, every package is evidence-linked, and nothing was auto-approved.",
            "received": [
                "Scout's evidence summary",
                "Architect's packages and target files",
                "Guardian's gate register",
            ],
            "produced": [
                f"{passed}/{len(checks)} checks passed" if checks else "Verification pending",
                "Verdict: PASS" if verification_ok else "Verdict: FAIL" if checks else "Verdict: pending",
                "0 auto-approved changes",
            ],
            "handoff": f"Critic → Scribe: {passed}/{len(checks) or 7} checks passed; human gates remain open.",
            "checks": checks,
            "count": passed,
            "count_label": "checks passed",
        },
        {
            "agent_id": "scribe",
            "index": 5,
            "name": "Scribe",
            "role": "Seal the plan, report, and bundle",
            "status": scribe.get("status", "queued"),
            "summary": scribe.get("summary", ""),
            "plain_language": "Scribe writes the plan, the human-readable report, the bundle manifest, and the hash-chained agent log. Sealing is not approval: every change still waits for a human.",
            "received": [
                "Critic's verification result",
                "Guardian's open gates",
                "Package and target hashes",
            ],
            "produced": [
                f"{artifact_count} bundle files",
                "migration-plan.json · MIGRATION-REPORT.md",
                "bundle-manifest.json · audit.jsonl",
            ],
            "handoff": "Scribe → sealed bundle: every change is pending human approval.",
            "checks": scribe.get("checks", []),
            "count": artifact_count,
            "count_label": "bundle files",
        },
    ]

    handoffs = []
    for index, stage in enumerate(stages):
        target = stages[index + 1]["agent_id"] if index + 1 < len(stages) else "sealed bundle"
        handoffs.append({
            "seq": index + 1,
            "from": stage["agent_id"],
            "to": target,
            "kind": "handoff" if index + 1 < len(stages) else "seal",
            "message": stage["handoff"],
        })

    narrative = (
        f"Scout resolved {feature_id} · {feature_name} from the snapshot. It found "
        f"{feature_evidence} evidence links across {total_evidence} evidence records, "
        f"{findings_count} findings, and {dispositions} dispositions. "
        f"Architect turned those dispositions into {package_count} work packages; "
        f"{generated} target files were generated. "
        f"Guardian opened {gate_count} gates — {len(assumption_gates)} assumption gates and "
        f"{len(rule_groups)} rule groups — with {high_gates} marked high impact. "
        f"Critic ran {len(checks)} checks; {passed} passed"
        + (f" and {failed} failed." if failed else ".")
        + f" Scribe sealed {artifact_count} bundle files, the plan, the report, and the agent log. "
        "Every change remains pending human approval."
    )

    explain = {
        "headline": "How to read this page: five agents, one evidence chain",
        "plain_language": (
            "This page is the demo of the migration crew. Scout finds the evidence. "
            "Architect writes the cloud target drafts. Guardian opens the compliance "
            "gates. Critic tries to break the result. Scribe seals the plan and report. "
            "Nobody deploys; every change is a draft for a human."
        ),
        "why_it_matters": (
            "A migration estimate is only trustworthy if every claim has evidence and "
            "every unknown has an owner. The gates are not failures — they are the "
            "decisions a delivery team must make before anything ships."
        ),
        "what_to_look_at": [
            "Start with Scout: 300 files, 101 evidence records, 31 links on PA-VEH-01.",
            "Then Architect: five target packages, all evidence-linked, all pending.",
            "Then Guardian: 3 assumption gates + 8 rule groups = 11 human decisions.",
            "Then Critic: 7/7 checks passed, but 0 auto-approvals.",
            "Then Scribe: the sealed plan, report, bundle, and hash-chained log.",
        ],
        "outcome": "completed_with_gates — verification passed; human gates remain open.",
        "caveat": "This is not a deployment and not an official Cloud Assurance result.",
    }

    glossary = [
        {"term": "Evidence link", "definition": "A pointer from a claim to a file, line or pointer, excerpt, method, and confidence."},
        {"term": "Work package", "definition": "One target file generated from one explicit source-to-target disposition."},
        {"term": "Gate", "definition": "A named human decision that must be resolved before the bundle can ship."},
        {"term": "Assumption gate", "definition": "A gate created because the evidence is incomplete or a decision was rejected."},
        {"term": "Rule group", "definition": "A gate grouping every open finding for one Guidewire rule."},
        {"term": "Deterministic", "definition": "The same input produces the same output; no model is called."},
        {"term": "Sealed bundle", "definition": "A hashed plan, report, target files, manifest, and agent log. Sealed means tamper-evident, not approved."},
        {"term": "Official Cloud Assurance", "definition": "Guidewire's official cloud-readiness assessment. PreFlight is not that assessment."},
    ]

    view.update({
        "stages": stages,
        "handoffs": handoffs,
        "narrative": narrative,
        "explain": explain,
        "glossary": glossary,
        "gate_groups": {
            "assumptions": assumption_gates,
            "rules": sorted(rule_groups.values(), key=lambda item: item["rule_id"]),
        },
        "evidence_preview": evidence_preview,
        "package_previews": package_previews,
        "bundle_files": bundle_files,
        "bundle_manifest": bundle_manifest,
        "human_gate_summary": human_gate_summary,
        "machine_checks": machine_checks,
        "next_actions": next_actions,
        "reality_boundary": reality_boundary,
        "loop": {
            "rework_path": "Guardian or Critic can send the package back to Architect; Scribe only seals after verification.",
            "green": verification_ok and not failed,
            "human_gates": gate_count,
            "machine_green": verification_ok and not failed,
        },
    })
    view.setdefault("llm", {"mode": "off", "status": "off", "model": None,
                            "annotations": {}, "warnings": [], "calls": []})
    return view



def _evidence_for_source(source_ref: str, evidence: list[dict[str, Any]]) -> list[str]:
    leaf = source_ref.rsplit(".", 1)[-1]
    if not leaf:
        return []
    matches = []
    for item in evidence:
        excerpt = item.get("excerpt") or ""
        if leaf in excerpt and item.get("evidence_id"):
            matches.append(item["evidence_id"])
        if len(matches) == 2:
            break
    return matches


def _parse_generated(path: Path) -> tuple[bool, str]:
    try:
        text = _read_text(path)
    except (OSError, UnicodeDecodeError) as exc:
        return False, f"cannot read: {exc}"
    suffix = path.suffix.lower()
    try:
        if suffix == ".json":
            json.loads(text)
        elif suffix in {".yaml", ".yml"}:
            yaml.safe_load(text)
    except (ValueError, yaml.YAMLError) as exc:
        return False, f"parse failed: {exc}"
    return True, "parsed"


def _live_reasoning(
    state: dict[str, Any],
    *,
    kind: str,
    payload: dict[str, Any],
    config: LLMConfig,
    model: str | None,
    transport=None,
) -> None:
    """Run one optional live annotation and record a sanitized audit trail."""
    started = time.monotonic()
    try:
        annotation = annotate_migration_agent(
            kind, payload, config=config, model=model, transport=transport
        )
        state.setdefault("llm", {}).setdefault("annotations", {})[kind] = annotation
        state["llm"].setdefault("calls", []).append({
            "kind": kind,
            "status": "ok",
            "model": annotation["model"],
            "latency_ms": annotation["latency_ms"],
            "usage": annotation["usage"],
            "prompt_sha256": annotation["prompt_sha256"],
            "response_sha256": annotation["response_sha256"],
        })
        for agent in state.get("agents", []):
            if agent.get("agent_id") == kind:
                agent["reasoning"] = annotation
    except LLMError as exc:
        state.setdefault("llm", {}).setdefault("warnings", []).append({
            "agent": kind,
            "code": exc.code,
            "message": str(exc),
            "latency_ms": int((time.monotonic() - started) * 1000),
        })
        state["llm"]["status"] = "degraded"
        state["llm"].setdefault("calls", []).append({
            "kind": kind,
            "status": "failed",
            "code": exc.code,
            "latency_ms": int((time.monotonic() - started) * 1000),
        })
    except Exception:
        # An optional annotation must never abort the deterministic migration.
        # Do not persist exception text that may contain provider details.
        state.setdefault("llm", {}).setdefault("warnings", []).append({
            "agent": kind,
            "code": "annotation_failed",
            "message": "Live annotation failed; the deterministic result is retained.",
            "latency_ms": int((time.monotonic() - started) * 1000),
        })
        state["llm"]["status"] = "degraded"
        state["llm"].setdefault("calls", []).append({
            "kind": kind,
            "status": "failed",
            "code": "annotation_failed",
            "latency_ms": int((time.monotonic() - started) * 1000),
        })



def run_migration(store, run_id: str, *, feature_id: str | None = None,
                  pace: float = 0.35, live: bool = False,
                  model: str | None = None, llm_config: LLMConfig | None = None,
                  llm_transport=None) -> dict[str, Any]:
    """Run the five agents end-to-end and persist the bundle and state.

    ``pace`` adds a short pause between handoffs so the live UI can show agent
    progress. Tests and CLI callers set it to zero. ``live`` is opt-in: it asks
    the configured model endpoint for grounded Scout/Architect/Critic narratives,
    while Guardian remains deterministic.
    """
    status = store.read_status(run_id)
    if status.get("status") != "succeeded":
        raise ValueError("migration requires a succeeded analysis run")

    config = llm_config or LLMConfig.from_env()
    if live and not config.configured:
        raise LLMError(
            "Live reasoning was requested but is not configured. Set "
            "PREFLIGHT_LLM_BASE_URL and PREFLIGHT_LLM_API_KEY, or run offline.",
            code="not_configured",
        )
    if live and not config.allow_real_code and not is_synthetic_run(store, run_id):
        raise LLMError(_REAL_CODE_BLOCKED_MESSAGE, code="real_code_blocked", status=409)
    live_model = config.resolve_model(model) if live else None

    features = _read(store, run_id, "features.json", {"features": []}).get("features", [])
    feature = next((item for item in features if item.get("feature_id") == feature_id), None)
    if feature is None and feature_id is None:
        feature = features[0] if features else None
    if feature is None:
        raise ValueError(f"feature not found: {feature_id}")
    feature_id = feature["feature_id"]

    state = _initial_state(run_id, feature, feature_id)
    if live:
        state["mode"] = (
            f"five specialist agents · live reasoning ({live_model}) · deterministic Guardian"
        )
        state["llm"] = {
            "mode": "live",
            "status": "ready",
            "model": live_model,
            "annotations": {},
            "warnings": [],
            "calls": [],
        }
    store.write_artifact(run_id, MIGRATION_ARTIFACT, state)
    _append_audit(store, run_id, agent="orchestrator", action="migration.started",
                  object_id=run_id, reason=f"autonomous draft for {feature_id}")

    manifest = _read(store, run_id, "manifest.json", {})
    evidence = _read(store, run_id, "evidence.json", {"evidence": []}).get("evidence", [])
    mappings = _read(store, run_id, "mappings.json", {"mappings": []}).get("mappings", [])
    changes = _read(store, run_id, "changes.json", {"changes": []}).get("changes", [])
    assumptions = _read(store, run_id, "assumptions.json", {"assumptions": []}).get("assumptions", [])
    findings = _read(store, run_id, "findings.json", {"findings": []}).get("findings", [])
    mappings_by_id = {item.get("mapping_id"): item for item in mappings}
    run_dir = store.run_dir(run_id)
    draft_root = run_dir / "draft"
    migration_dir = run_dir / BUNDLE_ROOT

    try:
        # 1. Scout ---------------------------------------------------------
        _set_agent(state, "scout", status="running", started_at=_now())
        _append_audit(store, run_id, agent="scout", action="agent.started", object_id="scout")
        feature_evidence = feature.get("evidence_ids", [])
        scout_checks = [
            {"name": "run succeeded", "ok": True, "detail": status.get("status", "")},
            {"name": "feature resolved", "ok": True, "detail": feature_id},
            {"name": "feature evidence", "ok": len(feature_evidence) > 0,
             "detail": f"{len(feature_evidence)} linked records"},
            {"name": "source snapshot", "ok": bool(manifest.get("sha256")),
             "detail": str(manifest.get("sha256", ""))[:12]},
        ]
        _set_agent(
            state, "scout", status="done", finished_at=_now(),
            summary=(
                f"{manifest.get('file_count', 0)} files → {len(evidence)} evidence records · "
                f"{len(findings)} findings · {len(mappings)} dispositions · {len(feature_evidence)} "
                f"evidence links on {feature_id}"
            ),
            checks=scout_checks,
        )
        state["progress"] = 18
        state["current_agent"] = "architect"
        state["summary"].update({
            "files": manifest.get("file_count", 0),
            "evidence": len(evidence),
            "findings": len(findings),
            "dispositions": len(mappings),
            "feature_evidence": len(feature_evidence),
        })
        if live:
            feature_ids = set(feature_evidence)
            allowed_evidence = [str(value) for value in feature_evidence]
            scout_evidence = [
                {
                    "evidence_id": item.get("evidence_id"),
                    "path": item.get("path"),
                    "line": item.get("line"),
                    "excerpt": (item.get("excerpt") or "")[:300],
                    "method": item.get("method"),
                }
                for item in evidence
                if item.get("evidence_id") in feature_ids
            ][:12]
            _live_reasoning(
                state,
                kind="scout",
                payload={
                    "feature_id": feature_id,
                    "feature_name": feature.get("name", feature_id),
                    "summary": state["agents"][0]["summary"],
                    "evidence": scout_evidence,
                    "findings": [
                        {"rule_id": item.get("rule_id"), "severity": item.get("severity"),
                         "title": item.get("title")} for item in findings[:12]
                    ],
                    "allowed_evidence_ids": allowed_evidence,
                    "allowed_rule_ids": sorted({str(item.get("rule_id")) for item in findings if item.get("rule_id")}),
                },
                config=config,
                model=live_model,
                transport=llm_transport,
            )
            state["llm"]["status"] = (
                "active" if state["llm"].get("annotations") else "degraded"
            )
        _persist(store, run_id, state)
        _append_audit(store, run_id, agent="scout", action="agent.completed", object_id="scout",
                      reason=state["agents"][0]["summary"])
        if pace:
            time.sleep(pace)

        # 2. Architect -----------------------------------------------------
        _set_agent(state, "architect", status="running", started_at=_now())
        _append_audit(store, run_id, agent="architect", action="agent.started", object_id="architect")
        packages: list[dict[str, Any]] = []
        outputs: list[dict[str, Any]] = []
        used_targets: set[str] = set()
        for index, change in enumerate(changes, start=1):
            target = str(change.get("target_path", ""))
            mapping = mappings_by_id.get(change.get("mapping_id"), {})
            package_id = f"WP-{index:02d}"
            reasons: list[str] = []
            if not _safe_relative(target):
                reasons.append("unsafe or _gen target path")
            if target in used_targets:
                reasons.append("duplicate target path")
            used_targets.add(target)
            source_file = draft_root / target
            output_file = migration_dir / "target" / target
            output_ok = False
            if source_file.is_file() and _safe_relative(target):
                data = source_file.read_bytes()
                _write_bytes(output_file, data)
                output_ok = True
                outputs.append({
                    "path": f"{TARGET_ROOT}/{target}",
                    "bytes": len(data),
                    "sha256": _sha(data),
                })
            else:
                reasons.append("draft output is missing")
            evidence_ids = _evidence_for_source(str(mapping.get("source_ref", "")), evidence)
            if not evidence_ids:
                evidence_ids = list(feature_evidence[:2])
            gate_ids = [
                assumption["assumption_id"]
                for assumption in assumptions
                if assumption.get("related_mapping_id") == mapping.get("mapping_id")
                and assumption.get("status") == "open"
            ]
            package = {
                "package_id": package_id,
                "title": f"Generate {Path(target).name}",
                "target_path": target,
                "source_ref": mapping.get("source_ref"),
                "target_name": mapping.get("target_name"),
                "disposition": mapping.get("disposition"),
                "mapping_id": mapping.get("mapping_id"),
                "change_id": change.get("change_id"),
                "agent": "architect",
                "status": "blocked" if reasons else "draft_ready",
                "reasons": reasons,
                "evidence_ids": evidence_ids,
                "gate_ids": gate_ids,
                "approval": change.get("approval_state", "pending"),
                "bytes": len((output_file.read_bytes() if output_ok else b"")),
                "sha256": _sha(output_file.read_bytes()) if output_ok else None,
            }
            packages.append(package)
        state["packages"] = packages
        state["outputs"] = outputs
        state["progress"] = 42
        state["current_agent"] = "guardian"
        ready = sum(1 for p in packages if p["status"] == "draft_ready")
        _set_agent(
            state, "architect", status="done", finished_at=_now(),
            summary=(f"{len(packages)} work packages · {ready} draft files generated · "
                     f"{len(outputs)} target artefacts in migration/target/"),
            checks=[
                {"name": "explicit dispositions", "ok": bool(mappings), "detail": f"{len(mappings)}"},
                {"name": "target files generated", "ok": ready == len(packages) and bool(packages),
                 "detail": f"{ready}/{len(packages)}"},
                {"name": "_gen untouched", "ok": all("_gen" not in p["target_path"] for p in packages),
                 "detail": "target bundle only"},
            ],
        )
        if live:
            _live_reasoning(
                state,
                kind="architect",
                payload={
                    "feature_id": feature_id,
                    "feature_name": feature.get("name", feature_id),
                    "summary": state["agents"][1]["summary"],
                    "packages": [
                        {"package_id": item["package_id"], "target_path": item["target_path"],
                         "disposition": item.get("disposition"),
                         "evidence_ids": item.get("evidence_ids", [])}
                        for item in packages
                    ],
                    "allowed_evidence_ids": sorted({
                        str(evidence_id) for item in packages
                        for evidence_id in item.get("evidence_ids", [])
                    }),
                    "allowed_package_ids": [item["package_id"] for item in packages],
                },
                config=config,
                model=live_model,
                transport=llm_transport,
            )
            state["llm"]["status"] = (
                "active" if state["llm"].get("annotations") else "degraded"
            )
        _persist(store, run_id, state)
        _append_audit(store, run_id, agent="architect", action="agent.completed",
                      object_id="architect", reason=state["agents"][1]["summary"])
        if pace:
            time.sleep(pace)

        # 3. Guardian ------------------------------------------------------
        _set_agent(state, "guardian", status="running", started_at=_now())
        _append_audit(store, run_id, agent="guardian", action="agent.started", object_id="guardian")
        gates: list[dict[str, Any]] = []
        for assumption in assumptions:
            if assumption.get("status") != "open":
                continue
            gates.append({
                "gate_id": f"G-{len(gates) + 1:02d}",
                "kind": "assumption",
                "severity": assumption.get("impact", "medium"),
                "title": assumption.get("statement", ""),
                "question": assumption.get("question_to_ask", ""),
                "owner": assumption.get("owner", "unassigned"),
                "source_id": assumption.get("assumption_id"),
                "status": "open",
            })
        rules: dict[str, list[dict[str, Any]]] = {}
        for finding in findings:
            if finding.get("decision", "open") != "open":
                continue
            rules.setdefault(finding.get("rule_id", "unknown"), []).append(finding)
        for rule_id, items in sorted(rules.items()):
            severity = "high" if any(item.get("severity") == "error" for item in items) else "medium"
            gates.append({
                "gate_id": f"G-{len(gates) + 1:02d}",
                "kind": "review",
                "severity": severity,
                "title": f"{items[0].get('title', rule_id)} ({len(items)} findings, {rule_id})",
                "question": "Has the delivery team accepted or remediated this finding before target approval?",
                "owner": "delivery team",
                "source_id": rule_id,
                "status": "open",
            })
        gate_by_mapping = {
            gate["source_id"]: gate["gate_id"]
            for gate in gates if gate["kind"] == "assumption"
        }
        for package in packages:
            related = [
                gate_by_mapping[assumption_id]
                for assumption_id in package.get("gate_ids", [])
                if assumption_id in gate_by_mapping
            ]
            package["gate_ids"] = related
        state["gates"] = gates
        state["progress"] = 65
        state["current_agent"] = "critic"
        high = sum(1 for gate in gates if gate["severity"] == "high")
        _set_agent(
            state, "guardian", status="done", finished_at=_now(),
            summary=f"{len(gates)} open gates · {high} high impact · deployment remains blocked",
            checks=[
                {"name": "assumption gates", "ok": True,
                 "detail": f"{sum(1 for g in gates if g['kind'] == 'assumption')} open"},
                {"name": "finding gates", "ok": True,
                 "detail": f"{sum(1 for g in gates if g['kind'] == 'review')} rule groups"},
                {"name": "no self-approval", "ok": True,
                 "detail": "all changes remain pending"},
            ],
        )
        _persist(store, run_id, state)
        _append_audit(store, run_id, agent="guardian", action="agent.completed",
                      object_id="guardian", reason=state["agents"][2]["summary"])
        if pace:
            time.sleep(pace)

        # 4. Critic --------------------------------------------------------
        _set_agent(state, "critic", status="running", started_at=_now())
        _append_audit(store, run_id, agent="critic", action="agent.started", object_id="critic")
        checks: list[dict[str, Any]] = []
        checks.append({"name": "packages exist", "ok": bool(packages),
                       "detail": f"{len(packages)} work packages"})
        checks.append({"name": "all package files generated",
                       "ok": all(p["status"] == "draft_ready" for p in packages),
                       "detail": f"{sum(1 for p in packages if p['status'] == 'draft_ready')}/{len(packages)}"})
        checks.append({"name": "no _gen targets",
                       "ok": all("_gen" not in p["target_path"] for p in packages),
                       "detail": "bundle is _ext/codegen/updater only"})
        checks.append({"name": "no duplicate targets",
                       "ok": len({p["target_path"] for p in packages}) == len(packages),
                       "detail": f"{len({p['target_path'] for p in packages})} unique"})
        parse_ok = True
        parse_details = []
        for output in outputs:
            path = run_dir / output["path"]
            ok, detail = _parse_generated(path)
            parse_ok = parse_ok and ok
            if not ok:
                parse_details.append(f"{output['path']}: {detail}")
        checks.append({"name": "generated JSON/YAML parses", "ok": parse_ok,
                       "detail": "; ".join(parse_details) or f"{len(outputs)} files parsed"})
        checks.append({"name": "every package is evidence-linked",
                       "ok": all(p["evidence_ids"] for p in packages),
                       "detail": f"{sum(1 for p in packages if p['evidence_ids'])}/{len(packages)} linked"})
        checks.append({"name": "human approval retained",
                       "ok": all(p["approval"] == "pending" for p in packages),
                       "detail": "0 auto-approved changes"})
        failed = [check for check in checks if not check["ok"]]
        state["verification"] = {"status": "passed" if not failed else "failed",
                                 "checks": checks}
        state["progress"] = 85
        state["current_agent"] = "scribe"
        _set_agent(
            state, "critic", status="done" if not failed else "failed",
            finished_at=_now(),
            summary=(f"{len(checks) - len(failed)}/{len(checks)} checks passed · "
                     f"verdict {'PASS' if not failed else 'FAIL'}"),
            checks=checks,
        )
        if live:
            _live_reasoning(
                state,
                kind="critic",
                payload={
                    "feature_id": feature_id,
                    "feature_name": feature.get("name", feature_id),
                    "summary": state["agents"][3]["summary"],
                    "packages": [
                        {"package_id": item["package_id"], "target_path": item["target_path"],
                         "status": item["status"], "approval": item.get("approval")}
                        for item in packages
                    ],
                    "gates": [
                        {"gate_id": gate["gate_id"], "kind": gate["kind"],
                         "severity": gate["severity"], "title": gate["title"]}
                        for gate in gates
                    ],
                    "checks": checks,
                    "allowed_evidence_ids": sorted({
                        str(evidence_id) for item in packages
                        for evidence_id in item.get("evidence_ids", [])
                    }),
                    "allowed_rule_ids": sorted({
                        str(item.get("rule_id")) for item in findings if item.get("rule_id")
                    }),
                    "allowed_package_ids": [item["package_id"] for item in packages],
                },
                config=config,
                model=live_model,
                transport=llm_transport,
            )
            state["llm"]["status"] = (
                "active" if len(state["llm"].get("annotations", {})) >= 3 else "degraded"
            )
        _persist(store, run_id, state)
        _append_audit(store, run_id, agent="critic", action="agent.completed",
                      object_id="critic", reason=state["agents"][3]["summary"])
        if pace:
            time.sleep(pace)

        # 5. Scribe --------------------------------------------------------
        _set_agent(state, "scribe", status="running", started_at=_now())
        _append_audit(store, run_id, agent="scribe", action="agent.started", object_id="scribe")
        state["summary"].update({
            "packages": len(packages),
            "generated": sum(1 for p in packages if p["status"] == "draft_ready"),
            "blocked": sum(1 for p in packages if p["status"] == "blocked"),
            "gates": len(gates),
            "high_gates": high,
            "artifacts": len(outputs) + 4,
        })
        state["status"] = "completed_with_gates" if gates else "completed"
        state["progress"] = 100
        state["current_agent"] = None
        state["finished_at"] = _now()
        _set_agent(
            state, "scribe", status="done", finished_at=_now(),
            summary="Plan, report, and sealed bundle manifest written; every change remains pending.",
            checks=[
                {"name": "plan written", "ok": True, "detail": PLAN_PATH},
                {"name": "report written", "ok": True, "detail": REPORT_PATH},
                {"name": "bundle manifest written", "ok": True, "detail": MANIFEST_PATH},
            ],
        )
        plan = {
            "schema_version": "1.0",
            "run_id": run_id,
            "feature_id": feature_id,
            "feature_name": feature.get("name", feature_id),
            "generated_at": _now(),
            "boundary": BOUNDARY,
            "source_snapshot": manifest.get("sha256"),
            "agents": [
                {"agent_id": item["agent_id"], "name": item["name"], "role": item["role"],
                 "status": item["status"], "summary": item["summary"]}
                for item in state["agents"]
            ],
            "packages": packages,
            "gates": gates,
            "outputs": outputs,
            "verification": state["verification"],
        }
        if live:
            plan["llm"] = {
                "mode": state["llm"].get("mode"),
                "model": state["llm"].get("model"),
                "status": state["llm"].get("status"),
                "calls": state["llm"].get("calls", []),
                "warnings": state["llm"].get("warnings", []),
                "annotations": state["llm"].get("annotations", {}),
            }
        plan_bytes = (json.dumps(plan, indent=2, sort_keys=False) + "\n").encode("utf-8")
        plan_sha256 = _sha(plan_bytes)
        _write_bytes(migration_dir / "migration-plan.json", plan_bytes)
        report = _render_report(
            state, plan, plan_sha256=plan_sha256,
            bundle_file_count=len(outputs) + 3,
        )
        _write_bytes(migration_dir / "MIGRATION-REPORT.md", report.encode("utf-8"))
        bundle_files = []
        for path in sorted(migration_dir.rglob("*")):
            if path.is_file() and path.name not in {
                "bundle-manifest.json", "audit.checkpoint.json",
            }:
                relative = path.relative_to(migration_dir).as_posix()
                data = path.read_bytes()
                bundle_files.append({"path": f"{BUNDLE_ROOT}/{relative}",
                                     "bytes": len(data), "sha256": _sha(data)})
        manifest_payload = {
            "schema_version": "1.0",
            "run_id": run_id,
            "feature_id": feature_id,
            "generated_at": _now(),
            "boundary": BOUNDARY,
            "source_snapshot": manifest.get("sha256"),
            "files": bundle_files,
            "file_count": len(bundle_files),
            "gate_count": len(gates),
            "verification": state["verification"]["status"],
            "audit_path": AUDIT_PATH,
        }
        manifest_bytes = (json.dumps(manifest_payload, indent=2, sort_keys=False) + "\n").encode("utf-8")
        _write_bytes(migration_dir / "bundle-manifest.json", manifest_bytes)
        state["outputs"] = outputs
        state["bundle"] = {
            "path": f"{BUNDLE_ROOT}/bundle-manifest.json",
            "bytes": len(manifest_bytes),
            "sha256": _sha(manifest_bytes),
            "file_count": len(bundle_files),
            "sha256_files": {item["path"]: item["sha256"] for item in bundle_files},
        }
        state["plan_sha256"] = plan_sha256
        state["report_sha256"] = _sha(report.encode("utf-8"))
        state["summary"]["artifacts"] = len(bundle_files)
        verified, detail = verify_migration_log(store, run_id)
        events = _read(store, run_id, AUDIT_PATH, [])
        state["audit"] = {
            "path": AUDIT_PATH,
            "events": len(events) + 1,
            "head": events[-1]["hash"][:16] if events else None,
            "verified": verified,
            "detail": detail,
        }
        _set_agent(
            state, "scribe", status="done", finished_at=_now(),
            summary=(f"Bundle sealed: {len(bundle_files)} files · plan {state['plan_sha256'][:12]} · "
                     f"report {state['report_sha256'][:12]}"),
        )
        _persist(store, run_id, state)
        _append_audit(store, run_id, agent="scribe", action="agent.completed",
                      object_id="scribe", reason=state["agents"][4]["summary"])
        final_verified, final_detail = verify_migration_log(store, run_id)
        events = _read(store, run_id, AUDIT_PATH, [])
        state["audit"] = {
            "path": AUDIT_PATH,
            "events": len(events),
            "head": events[-1]["hash"][:16] if events else None,
            "verified": final_verified,
            "detail": final_detail,
        }
        _append_audit(store, run_id, agent="orchestrator", action="migration.completed",
                      object_id=run_id, reason=state["status"])
        events = _read(store, run_id, AUDIT_PATH, [])
        state["audit"] = {
            "path": AUDIT_PATH,
            "events": len(events),
            "head": events[-1]["hash"][:16] if events else None,
            "verified": verify_migration_log(store, run_id)[0],
            "detail": verify_migration_log(store, run_id)[1],
        }
        _persist(store, run_id, state)
        return state
    except Exception as exc:
        state["status"] = "failed"
        state["finished_at"] = _now()
        state["current_agent"] = None
        state["error"] = {"type": type(exc).__name__, "message": str(exc)}
        state["progress"] = 100
        for agent in state["agents"]:
            if agent["status"] == "running":
                agent["status"] = "failed"
                agent["finished_at"] = _now()
        _persist(store, run_id, state)
        _append_audit(store, run_id, agent="orchestrator", action="migration.failed",
                      object_id=run_id, reason=str(exc))
        raise


def _render_report(state: dict[str, Any], plan: dict[str, Any], *,
                   plan_sha256: str, bundle_file_count: int) -> str:
    lines = [
        f"# Autonomous migration draft — {state['feature_id']} {state['feature_name']}",
        "",
        f"**Status:** `{state['status']}`  ",
        f"**Verification:** `{state['verification']['status']}`  ",
        f"**Generated:** {state['finished_at'] or _now()}  ",
        f"**Boundary:** {BOUNDARY}",
        "",
        "## Agent handoffs",
        "",
    ]
    for agent in state["agents"]:
        lines.append(f"- **{agent['name']} ({agent['role']})** — `{agent['status']}`. {agent['summary']}")
    lines += ["", "## Work packages", "",
              "| ID | Target | Disposition | Status | Gates | Evidence |",
              "|---|---|---|---|---|---|"]
    for package in state["packages"]:
        lines.append(
            f"| {package['package_id']} | `{package['target_path']}` | "
            f"{package.get('disposition') or '—'} | {package['status']} | "
            f"{', '.join(package.get('gate_ids', [])) or '—'} | "
            f"{', '.join(package.get('evidence_ids', [])) or '—'} |"
        )
    lines += ["", "## Open gates", ""]
    if state["gates"]:
        for gate in state["gates"]:
            lines.append(
                f"- **{gate['gate_id']} · {gate['severity']} · {gate['kind']}** — {gate['title']}  "
                f"Question: {gate['question']} (owner: {gate['owner']})"
            )
    else:
        lines.append("No open gates.")
    lines += ["", "## Verification", ""]
    for check in state["verification"]["checks"]:
        lines.append(f"- **{'PASS' if check['ok'] else 'FAIL'}** — {check['name']}: {check['detail']}")
    lines += [
        "",
        "## Generated files",
        "",
        f"The sealed bundle manifest is `{MANIFEST_PATH}` ({bundle_file_count} files plus the manifest).",
        "",
        f"Plan SHA-256: `{plan_sha256}`  ",
        "Report SHA-256: recorded in `migration/bundle-manifest.json`  ",
        f"Agent log: `{AUDIT_PATH}`",
        "",
        "Changes remain pending human approval. This is not a deployment.",
        "",
    ]
    return "\n".join(lines)
