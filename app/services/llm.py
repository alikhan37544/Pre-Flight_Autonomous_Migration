"""Optional live reasoning through an OpenAI-compatible model endpoint.

The deterministic product never needs this module. When live mode is explicitly
enabled, Scout, Architect, and Critic may ask a model for a grounded narrative;
Guardian remains deterministic and never calls the model. Configuration is read
only from the environment so no endpoint or credential is compiled into the app.
"""

from __future__ import annotations

import hashlib
import json
import os
import time
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Iterable, Mapping
from urllib.parse import urlparse

import httpx

MODEL_FLASH = "mimo-v2.6-flash"
MODEL_PRO = "mimo-v2.6-pro"
MODELS: tuple[str, ...] = (MODEL_FLASH, MODEL_PRO)
DEFAULT_MODEL = MODEL_FLASH
MAX_PROMPT_CHARS = 48_000


def _now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def _sha(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


class LLMError(RuntimeError):
    """A sanitized live-model failure safe to show in an API response."""

    def __init__(self, message: str, *, code: str = "llm_error", status: int | None = None):
        super().__init__(message)
        self.code = code
        self.status = status


@dataclass(frozen=True)
class LLMConfig:
    mode: str = "off"
    base_url: str = ""
    api_key: str = field(default="", repr=False)
    model: str = DEFAULT_MODEL
    timeout: float = 45.0
    allow_real_code: bool = False

    @classmethod
    def from_env(cls, env: Mapping[str, str] | None = None) -> "LLMConfig":
        source = os.environ if env is None else env
        mode = (source.get("PREFLIGHT_LLM_MODE") or "off").strip().lower()
        base_url = (source.get("PREFLIGHT_LLM_BASE_URL") or "").strip().rstrip("/")
        api_key = (source.get("PREFLIGHT_LLM_API_KEY") or "").strip()
        model = (source.get("PREFLIGHT_LLM_MODEL") or DEFAULT_MODEL).strip()
        if model not in MODELS:
            model = DEFAULT_MODEL
        try:
            timeout = float(source.get("PREFLIGHT_LLM_TIMEOUT", "45"))
        except ValueError:
            timeout = 45.0
        allow_real_code = (source.get("PREFLIGHT_LLM_ALLOW_REAL_CODE") or "").strip().lower() in {
            "1", "true", "yes", "on"
        }
        return cls(
            mode=mode if mode in {"off", "live"} else "off",
            base_url=base_url,
            api_key=api_key,
            model=model,
            timeout=max(5.0, min(timeout, 120.0)),
            allow_real_code=allow_real_code,
        )

    @property
    def configured(self) -> bool:
        return self.mode == "live" and bool(self.base_url) and bool(self.api_key)

    @property
    def base_host(self) -> str:
        return urlparse(self.base_url).netloc if self.base_url else ""

    def public(self) -> dict[str, Any]:
        reason = ""
        if self.mode != "live":
            reason = "Live reasoning is off. The deterministic offline path is active."
        elif not self.base_url:
            reason = "PREFLIGHT_LLM_BASE_URL is not set."
        elif not self.api_key:
            reason = "PREFLIGHT_LLM_API_KEY is not set."
        return {
            "mode": self.mode,
            "configured": self.configured,
            "base_host": self.base_host,
            "models": list(MODELS),
            "default_model": self.model,
            "allow_real_code": self.allow_real_code,
            "reason": reason,
            "provider": "OpenAI-compatible",
        }

    def resolve_model(self, requested: str | None = None) -> str:
        model = (requested or self.model).strip()
        if model not in MODELS:
            raise LLMError(
                f"Unsupported live model. Choose one of: {', '.join(MODELS)}.",
                code="unsupported_model",
            )
        return model


def _extract_json(text: str) -> dict[str, Any]:
    value = text.strip()
    if value.startswith("```"):
        value = value.strip("`")
        if value.lower().startswith("json"):
            value = value[4:]
    start = value.find("{")
    end = value.rfind("}")
    if start < 0 or end <= start:
        raise LLMError("Model response did not contain a JSON object.", code="invalid_json")
    try:
        payload = json.loads(value[start:end + 1])
    except json.JSONDecodeError as exc:
        raise LLMError(f"Model response was not valid JSON: {exc.msg}.", code="invalid_json") from exc
    if not isinstance(payload, dict):
        raise LLMError("Model response JSON must be an object.", code="invalid_json")
    return payload


def chat_json(
    messages: list[dict[str, str]],
    *,
    config: LLMConfig,
    model: str | None = None,
    transport: httpx.BaseTransport | None = None,
    max_tokens: int = 1200,
    temperature: float = 0.1,
) -> dict[str, Any]:
    """Call a chat-completions endpoint and return parsed JSON plus audit metadata."""
    if not config.configured:
        raise LLMError(
            "Live reasoning is not configured. Set PREFLIGHT_LLM_BASE_URL and "
            "PREFLIGHT_LLM_API_KEY, or use the offline path.",
            code="not_configured",
        )
    selected = config.resolve_model(model)
    url = f"{config.base_url}/chat/completions"
    body = {
        "model": selected,
        "messages": messages,
        "temperature": temperature,
        "max_tokens": max_tokens,
        "response_format": {"type": "json_object"},
    }
    prompt_text = json.dumps(messages, ensure_ascii=False, sort_keys=True)
    if len(prompt_text) > MAX_PROMPT_CHARS:
        raise LLMError("Prompt exceeds the live-reasoning size limit.", code="prompt_too_large")
    headers = {
        "Authorization": f"Bearer {config.api_key}",
        "Content-Type": "application/json",
    }
    started = time.monotonic()
    last_error: Exception | None = None
    with httpx.Client(timeout=config.timeout, transport=transport) as client:
        for attempt in range(2):
            try:
                response = client.post(url, headers=headers, json=body)
                if response.status_code >= 400:
                    raise LLMError(
                        f"Live model returned HTTP {response.status_code}.",
                        code="http_error",
                        status=response.status_code,
                    )
                payload = response.json()
                choices = payload.get("choices") or []
                if not choices:
                    raise LLMError("Live model returned no choices.", code="empty_response")
                content = (choices[0].get("message") or {}).get("content") or ""
                parsed = _extract_json(content)
                return {
                    "data": parsed,
                    "model": payload.get("model") or selected,
                    "usage": payload.get("usage") or {},
                    "latency_ms": int((time.monotonic() - started) * 1000),
                    "prompt_sha256": _sha(prompt_text),
                    "response_sha256": _sha(content),
                    "generated_at": _now(),
                }
            except (httpx.HTTPError, LLMError, ValueError) as exc:
                last_error = exc
                if attempt == 0:
                    time.sleep(0.4)
                    continue
    if isinstance(last_error, LLMError):
        raise last_error
    raise LLMError(
        "Live model request failed. The deterministic offline result is still available.",
        code="request_failed",
    ) from last_error


_SYSTEM_PROMPTS = {
    "scout": (
        "You are Scout in a Guidewire cloud-migration review. Use only the supplied "
        "evidence. Every observation must cite at least one evidence_id from the allowlist. "
        "Never invent files, evidence IDs, findings, rules, or customer facts. Return JSON: "
        '{"headline": "...", "observations": [{"text": "...", "evidence_ids": ["EV-..."]}], '
        '"unknowns": ["..."]}. Keep it under 120 words.'
    ),
    "architect": (
        "You are Architect in a Guidewire cloud-migration review. Explain the supplied "
        "work packages, not new ones. Every package rationale may cite only the supplied "
        "package_id and evidence_ids. Return JSON: "
        '{"headline": "...", "packages": [{"package_id": "WP-01", "rationale": "...", '
        '"risk": "low|medium|high", "test": "..."}], "unknowns": ["..."]}. '
        "Keep it under 160 words."
    ),
    "critic": (
        "You are Critic in a Guidewire cloud-migration review. Review the supplied "
        "deterministic checks and packages. Identify trade-offs and residual human risks. "
        "Cite only supplied rule_ids and package_ids. Do not override a deterministic PASS. "
        'Return JSON: {"headline": "...", "tradeoffs": [{"text": "...", "rule_ids": ["..."]}], '
        '"residual_risks": [{"text": "...", "owner": "..."}], "unknowns": ["..."]}. '
        "Keep it under 160 words."
    ),
}


def validate_migration_annotation(
    kind: str,
    payload: Mapping[str, Any],
    *,
    allowed_evidence: Iterable[str],
    allowed_rules: Iterable[str],
    allowed_packages: Iterable[str] | None = None,
) -> dict[str, Any]:
    """Drop any model statement that cites an unknown evidence/rule/package id."""
    evidence = set(allowed_evidence)
    rules = set(allowed_rules)
    packages = set(allowed_packages or [])
    dropped = 0
    cleaned: dict[str, Any] = {
        "headline": str(payload.get("headline") or "").strip()[:500],
        "observations": [],
        "packages": [],
        "tradeoffs": [],
        "residual_risks": [],
        "unknowns": [str(item)[:300] for item in (payload.get("unknowns") or [])][:8],
        "dropped_ungrounded": 0,
    }

    if kind == "scout":
        for item in payload.get("observations") or []:
            if not isinstance(item, dict):
                dropped += 1
                continue
            ids = [str(value) for value in (item.get("evidence_ids") or []) if str(value) in evidence]
            text = str(item.get("text") or "").strip()
            if not ids or not text:
                dropped += 1
                continue
            cleaned["observations"].append({"text": text[:500], "evidence_ids": ids[:6]})
    elif kind == "architect":
        for item in payload.get("packages") or []:
            if not isinstance(item, dict):
                dropped += 1
                continue
            package_id = str(item.get("package_id") or "")
            if packages and package_id not in packages:
                dropped += 1
                continue
            cleaned["packages"].append({
                "package_id": package_id,
                "rationale": str(item.get("rationale") or "").strip()[:600],
                "risk": str(item.get("risk") or "medium")[:20],
                "test": str(item.get("test") or "").strip()[:400],
            })
    elif kind == "critic":
        for item in payload.get("tradeoffs") or []:
            if not isinstance(item, dict):
                dropped += 1
                continue
            rule_ids = [str(value) for value in (item.get("rule_ids") or []) if str(value) in rules]
            text = str(item.get("text") or "").strip()
            if not rule_ids or not text:
                dropped += 1
                continue
            cleaned["tradeoffs"].append({"text": text[:500], "rule_ids": rule_ids[:6]})
        for item in payload.get("residual_risks") or []:
            if not isinstance(item, dict):
                dropped += 1
                continue
            text = str(item.get("text") or "").strip()
            if not text:
                dropped += 1
                continue
            cleaned["residual_risks"].append({
                "text": text[:500],
                "owner": str(item.get("owner") or "human reviewer")[:120],
            })

    cleaned["dropped_ungrounded"] = dropped
    return cleaned


def annotate_migration_agent(
    kind: str,
    payload: Mapping[str, Any],
    *,
    config: LLMConfig,
    model: str | None = None,
    transport: httpx.BaseTransport | None = None,
) -> dict[str, Any]:
    """Ask a model for a grounded annotation and validate every citation."""
    if kind not in _SYSTEM_PROMPTS:
        raise LLMError(f"Unknown annotation kind: {kind}", code="unknown_kind")
    allowed_evidence = [str(value) for value in payload.get("allowed_evidence_ids", [])]
    allowed_rules = [str(value) for value in payload.get("allowed_rule_ids", [])]
    allowed_packages = [str(value) for value in payload.get("allowed_package_ids", [])]
    request_payload = {
        "feature_id": payload.get("feature_id"),
        "feature_name": payload.get("feature_name"),
        "summary": payload.get("summary"),
        "evidence": payload.get("evidence", []),
        "findings": payload.get("findings", []),
        "packages": payload.get("packages", []),
        "gates": payload.get("gates", []),
        "checks": payload.get("checks", []),
        "allowed_evidence_ids": allowed_evidence,
        "allowed_rule_ids": allowed_rules,
        "allowed_package_ids": allowed_packages,
    }
    messages = [
        {"role": "system", "content": _SYSTEM_PROMPTS[kind]},
        {"role": "user", "content": json.dumps(request_payload, ensure_ascii=False)},
    ]
    raw = chat_json(messages, config=config, model=model, transport=transport)
    cleaned = validate_migration_annotation(
        kind,
        raw["data"],
        allowed_evidence=allowed_evidence,
        allowed_rules=allowed_rules,
        allowed_packages=allowed_packages,
    )
    return {
        "status": "ok",
        "kind": kind,
        **cleaned,
        "model": raw["model"],
        "usage": raw["usage"],
        "latency_ms": raw["latency_ms"],
        "prompt_sha256": raw["prompt_sha256"],
        "response_sha256": raw["response_sha256"],
        "generated_at": raw["generated_at"],
    }
