"""Runtime configuration for the PreFlight product."""

from __future__ import annotations

import os
import secrets
from dataclasses import dataclass, field
from pathlib import Path

from dotenv import load_dotenv

REPO = Path(__file__).resolve().parents[1]
load_dotenv(REPO / ".env")

_FALLBACK_SECRET = secrets.token_urlsafe(32)


def _default_secret_key() -> str:
    return os.environ.get("PREFLIGHT_SECRET_KEY") or _FALLBACK_SECRET


def _llm_timeout_from_env() -> float:
    try:
        value = float(os.environ.get("PREFLIGHT_LLM_TIMEOUT", "45"))
    except (TypeError, ValueError):
        return 45.0
    return max(5.0, min(value, 120.0))


@dataclass
class Settings:
    data_dir: Path = field(default_factory=lambda: Path(os.environ.get("PREFLIGHT_DATA_DIR", REPO / "data")))
    fixtures_dir: Path = field(default_factory=lambda: Path(os.environ.get("PREFLIGHT_FIXTURES_DIR", REPO / "fixtures")))
    ground_truth_dir: Path = field(default_factory=lambda: REPO / "ground_truth")
    reference_path: Path | None = field(
        default_factory=lambda: Path(os.environ.get(
            "PREFLIGHT_REFERENCE_PATH",
            REPO / "ground_truth" / "reference_target" / "pa_veh_01_reference.json",
        ))
    )
    secret_key: str = field(default_factory=_default_secret_key)
    sync_runs: bool = False
    tier: str = "demo"
    release_context: str = "Qusar 2026.08 (review context)"
    host: str = field(default_factory=lambda: os.environ.get("PREFLIGHT_HOST", "127.0.0.1"))
    port: int = field(default_factory=lambda: int(os.environ.get("PREFLIGHT_PORT", "8000")))
    llm_mode: str = field(default_factory=lambda: (os.environ.get("PREFLIGHT_LLM_MODE") or "off").strip().lower())
    llm_base_url: str = field(default_factory=lambda: (os.environ.get("PREFLIGHT_LLM_BASE_URL") or "").strip().rstrip("/"))
    llm_api_key: str = field(
        default_factory=lambda: (os.environ.get("PREFLIGHT_LLM_API_KEY") or "").strip(),
        repr=False,
    )
    llm_model: str = field(default_factory=lambda: (os.environ.get("PREFLIGHT_LLM_MODEL") or "mimo-v2.6-flash").strip())
    llm_timeout: float = field(default_factory=lambda: _llm_timeout_from_env())
    llm_allow_real_code: bool = field(default_factory=lambda: (os.environ.get("PREFLIGHT_LLM_ALLOW_REAL_CODE") or "").strip().lower() in {"1", "true", "yes", "on"})
    llm_allow_local: bool = field(default_factory=lambda: (os.environ.get("PREFLIGHT_LLM_ALLOW_LOCAL") or "").strip().lower() in {"1", "true", "yes", "on"})

    allowed_hosts: tuple[str, ...] = ("127.0.0.1", "localhost", "testserver")
    allowed_origins: tuple[str, ...] = ()
    allowed_fixtures: tuple[str, ...] = (
        "demo-slice-300", "acme-pc-2026.10",
    )
    max_upload_bytes: int = 500 * 1024 * 1024

    def __post_init__(self) -> None:
        if not self.allowed_origins:
            configured = f"http://{self.host}:{self.port}"
            self.allowed_origins = tuple(dict.fromkeys((
                "http://127.0.0.1:8000",
                "http://localhost:8000",
                "http://testserver",
                configured,
            )))

    def llm_config(self):
        from app.services.llm import LLMConfig

        return LLMConfig(
            mode=self.llm_mode,
            base_url=self.llm_base_url,
            api_key=self.llm_api_key,
            model=self.llm_model,
            timeout=self.llm_timeout,
            allow_real_code=self.llm_allow_real_code,
            allow_local=self.llm_allow_local,
        )
