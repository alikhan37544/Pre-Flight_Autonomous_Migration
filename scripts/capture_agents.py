#!/usr/bin/env python3
"""Capture the agent-loop and codebase-lab presentation screenshots.

The script is read-only against an already-running local PreFlight app. It
opens the demo run, clicks the five Migrator stage buttons and the Codebase lab
tabs, and writes a hash-addressed manifest next to the screenshots.

Typical use from ``v2/``::

    python scripts/capture_agents.py
    python scripts/capture_agents.py --base-url http://127.0.0.1:8010 \
        --out docs/presentation/assets/agents

Safety checks:
  * every request to a host other than 127.0.0.1 is blocked and recorded;
  * any browser console error or uncaught page error fails the run;
  * horizontal overflow on a 390 px viewport above 1 px fails the run;
  * a missing required selector fails the run with the selector and page URL;
  * no live-reasoning screenshot is fabricated. If the run has no live
    annotations, the file is skipped with a reason in the manifest.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import struct
import sys
import traceback
import urllib.request
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import quote, urlparse

from playwright.sync_api import (
    Page,
    TimeoutError as PlaywrightTimeoutError,
    sync_playwright,
)


REPO = Path(__file__).resolve().parents[1]
DEFAULT_BASE_URL = "http://127.0.0.1:8010"
DEFAULT_OUT = REPO / "docs" / "presentation" / "assets" / "agents"
DEFAULT_RUN_ID = "R-DEMO-001"
DEFAULT_CASE_ID = "cascade-mutual"
UPGRADE_SCENARIO = "GWCP-APD-NAMING-2027.04"

DESKTOP = {"width": 1440, "height": 900}
MOBILE = {"width": 390, "height": 844}

TARGET_FILES = (
    "migrator-loop-1440x900.png",
    "migrator-scout-1440x900.png",
    "migrator-architect-1440x900.png",
    "migrator-guardian-1440x900.png",
    "migrator-critic-1440x900.png",
    "migrator-scribe-1440x900.png",
    "migrator-live-1440x900.png",
    "codebase-loop-1440x900.png",
    "codebase-patches-1440x900.png",
    "codebase-upgrade-1440x900.png",
    "case-studies-1440x900.png",
    "migrator-390x844.png",
    "codebase-390x844.png",
    "case-studies-390x844.png",
)

STAGE_SPECS = (
    {
        "index": 0,
        "name": "Scout",
        "count": r"^31 evidence links$",
        "artifact": ".stage-artifact table",
        "focus": "Scout stage panel and evidence table",
    },
    {
        "index": 1,
        "name": "Architect",
        "count": r"^5 packages$",
        "artifact": ".stage-artifact table",
        "focus": "Architect stage panel and package table",
    },
    {
        "index": 2,
        "name": "Guardian",
        "count": r"^11 gates$",
        "artifact": ".stage-artifact .gate-group-grid",
        "focus": "Guardian stage panel and 11-gate story",
    },
    {
        "index": 3,
        "name": "Critic",
        "count": r"^7 checks passed$",
        "artifact": ".stage-artifact .verification-list",
        "focus": "Critic stage panel and seven independent checks",
    },
    {
        "index": 4,
        "name": "Scribe",
        "count": r"^8 bundle files$",
        "artifact": ".stage-artifact .seal-grid",
        "focus": "Scribe stage panel and four seal cards",
    },
)


class CaptureError(RuntimeError):
    """A required page state or capture invariant could not be satisfied."""


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def normalize_base_url(value: str) -> str:
    value = value.strip().rstrip("/")
    if value.isdigit():
        value = f"http://127.0.0.1:{value}"
    elif "://" not in value:
        value = f"http://{value}"
    parsed = urlparse(value)
    if parsed.scheme not in {"http", "https"}:
        raise ValueError(f"base URL must use http or https: {value!r}")
    if parsed.hostname != "127.0.0.1":
        raise ValueError(
            "base URL must point at 127.0.0.1 so the capture cannot reach "
            f"an external host: {value!r}"
        )
    if not parsed.port:
        raise ValueError(f"base URL must include an explicit port: {value!r}")
    return value


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Capture agent-loop and codebase-lab presentation screenshots."
    )
    parser.add_argument(
        "--base-url",
        default=DEFAULT_BASE_URL,
        help=f"Running PreFlight origin on 127.0.0.1 (default: {DEFAULT_BASE_URL})",
    )
    parser.add_argument(
        "--out",
        default=str(DEFAULT_OUT),
        help=f"Output directory (default: {DEFAULT_OUT})",
    )
    parser.add_argument(
        "--run-id",
        default=DEFAULT_RUN_ID,
        help=f"Migrator run id (default: {DEFAULT_RUN_ID})",
    )
    parser.add_argument(
        "--case-id",
        default=DEFAULT_CASE_ID,
        help=f"Codebase case id (default: {DEFAULT_CASE_ID})",
    )
    parser.add_argument(
        "--timeout",
        type=int,
        default=30_000,
        help="Per-action timeout in milliseconds (default: 30000)",
    )
    args = parser.parse_args()
    try:
        args.base_url = normalize_base_url(args.base_url)
    except ValueError as exc:
        parser.error(str(exc))
    return args


def wait_health(base_url: str, timeout: float = 15.0) -> None:
    url = f"{base_url}/api/health"
    try:
        with urllib.request.urlopen(url, timeout=timeout) as response:
            if response.status != 200:
                raise CaptureError(f"health check returned HTTP {response.status}: {url}")
    except Exception as exc:  # noqa: BLE001 - operational error with context
        raise CaptureError(
            f"PreFlight is not reachable at {base_url} ({exc}). "
            "Start the app first or pass a different --base-url."
        ) from exc


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def png_size(path: Path) -> tuple[int, int]:
    with path.open("rb") as handle:
        signature = handle.read(8)
        if signature != b"\x89PNG\r\n\x1a\n":
            raise CaptureError(f"not a PNG file: {path}")
        handle.read(4)  # IHDR chunk length
        if handle.read(4) != b"IHDR":
            raise CaptureError(f"PNG has no IHDR chunk: {path}")
        width, height = struct.unpack(">II", handle.read(8))
    return int(width), int(height)


class AgentCapture:
    def __init__(
        self,
        page: Page,
        base_url: str,
        out: Path,
        run_id: str,
        case_id: str,
        timeout: int,
    ) -> None:
        self.page = page
        self.base_url = base_url
        self.out = out
        self.run_id = run_id
        self.case_id = case_id
        self.timeout = timeout
        self.shots: list[dict] = []
        self.skipped: list[dict] = []
        self.console_errors: list[dict] = []
        self.blocked_requests: list[dict] = []
        self.overflow_checks: list[dict] = []
        self.mobile_overflow_failures: list[dict] = []
        self.counts: dict[str, int] = {}
        self._console_cursor = 0

        self.page.on("console", self._on_console)
        self.page.on("pageerror", self._on_page_error)
        self.page.route("**/*", self._guard_request)

    # -- event handlers -------------------------------------------------
    def _on_console(self, message) -> None:
        if message.type != "error":
            return
        location = message.location or {}
        self.console_errors.append(
            {
                "kind": "console",
                "text": message.text,
                "url": location.get("url") or self.page.url,
                "timestamp": utc_now(),
            }
        )

    def _on_page_error(self, error) -> None:
        self.console_errors.append(
            {
                "kind": "pageerror",
                "text": str(error),
                "url": self.page.url,
                "timestamp": utc_now(),
            }
        )

    def _guard_request(self, route) -> None:
        parsed = urlparse(route.request.url)
        if parsed.scheme in {"http", "https"} and parsed.hostname != "127.0.0.1":
            self.blocked_requests.append(
                {
                    "url": route.request.url,
                    "resource_type": route.request.resource_type,
                    "timestamp": utc_now(),
                }
            )
            route.abort()
        else:
            route.continue_()

    # -- navigation and scrolling --------------------------------------
    def url(self, path: str) -> str:
        if path.startswith(("http://", "https://")):
            return path
        return f"{self.base_url}/{path.lstrip('/')}"

    def open(self, path: str) -> None:
        self.page.goto(self.url(path), wait_until="networkidle", timeout=self.timeout)
        self.page.wait_for_timeout(200)
        self.scroll_to(0)

    def scroll_to(self, value: float) -> None:
        self.page.evaluate(
            "(y) => window.scrollTo(0, Math.max(0, Math.round(y)))", value
        )
        self.page.wait_for_timeout(120)

    def scroll_y(self) -> int:
        return int(round(self.page.evaluate("window.scrollY")))

    def absolute_top(self, selector: str) -> float:
        value = self.page.evaluate(
            """(selector) => {
                const element = document.querySelector(selector);
                return element ? element.getBoundingClientRect().top + window.scrollY : null;
            }""",
            selector,
        )
        if value is None:
            raise CaptureError(
                f"cannot position missing selector {selector!r} on {self.page.url}"
            )
        return float(value)

    def scroll_element_top(self, selector: str, offset: int = 16) -> None:
        locator = self.page.locator(selector).first
        locator.wait_for(state="visible", timeout=self.timeout)
        locator.scroll_into_view_if_needed()
        self.page.wait_for_timeout(80)
        self.scroll_to(self.absolute_top(selector) - offset)

    def click(self, selector: str, description: str) -> None:
        locator = self.page.locator(selector)
        try:
            locator.first.wait_for(state="visible", timeout=self.timeout)
        except PlaywrightTimeoutError as exc:
            raise CaptureError(
                f"missing required selector: {selector!r} ({description}) "
                f"on {self.page.url}"
            ) from exc
        locator.first.scroll_into_view_if_needed()
        locator.first.click()
        self.page.wait_for_timeout(180)

    # -- selector and visibility invariants -----------------------------
    def require_visible(
        self, selector: str, description: str, *, min_count: int = 1
    ):
        locator = self.page.locator(selector)
        try:
            locator.first.wait_for(state="visible", timeout=self.timeout)
        except PlaywrightTimeoutError as exc:
            raise CaptureError(
                f"missing required selector: {selector!r} ({description}) "
                f"on {self.page.url}"
            ) from exc
        count = locator.count()
        if count < min_count:
            raise CaptureError(
                f"expected at least {min_count} match(es) for {selector!r} "
                f"({description}), found {count} on {self.page.url}"
            )
        return locator

    def expect_count(self, selector: str, expected: int, description: str) -> int:
        count = self.page.locator(selector).count()
        if count != expected:
            raise CaptureError(
                f"expected {expected} {description} ({selector!r}), found {count} "
                f"on {self.page.url}"
            )
        return count

    def expect_min_count(self, selector: str, minimum: int, description: str) -> int:
        count = self.page.locator(selector).count()
        if count < minimum:
            raise CaptureError(
                f"expected at least {minimum} {description} ({selector!r}), "
                f"found {count} on {self.page.url}"
            )
        return count

    def require_text(
        self, selector: str, pattern: str, description: str
    ) -> str:
        locator = self.require_visible(selector, description)
        text = locator.first.inner_text().strip()
        if re.search(pattern, text) is None:
            raise CaptureError(
                f"{description} text did not match {pattern!r}: got {text!r} "
                f"from {selector!r} on {self.page.url}"
            )
        return text

    def _metrics(self, selector: str) -> dict | None:
        return self.page.evaluate(
            """(selector) => {
                const element = document.querySelector(selector);
                if (!element) return null;
                const rect = element.getBoundingClientRect();
                const width = Math.max(0, Math.min(rect.right, window.innerWidth)
                    - Math.max(rect.left, 0));
                const height = Math.max(0, Math.min(rect.bottom, window.innerHeight)
                    - Math.max(rect.top, 0));
                return {
                    top: rect.top,
                    right: rect.right,
                    bottom: rect.bottom,
                    left: rect.left,
                    width: rect.width,
                    height: rect.height,
                    visible_width: width,
                    visible_height: height,
                    inner_width: window.innerWidth,
                    inner_height: window.innerHeight,
                };
            }""",
            selector,
        )

    def require_in_viewport(
        self,
        selector: str,
        description: str,
        *,
        full: bool = True,
        min_px: int = 1,
    ) -> dict:
        metrics = self._metrics(selector)
        if metrics is None:
            raise CaptureError(
                f"missing required selector: {selector!r} ({description}) "
                f"on {self.page.url}"
            )
        if full:
            if (
                metrics["top"] < -1
                or metrics["left"] < -1
                or metrics["bottom"] > metrics["inner_height"] + 1
                or metrics["right"] > metrics["inner_width"] + 1
            ):
                raise CaptureError(
                    f"{description} is clipped at {self.page.url}: "
                    f"top={metrics['top']:.0f} bottom={metrics['bottom']:.0f} "
                    f"viewport={metrics['inner_width']}x{metrics['inner_height']}"
                )
        elif (
            metrics["visible_width"] < min_px
            or metrics["visible_height"] < min_px
        ):
            raise CaptureError(
                f"{description} is not visible enough at {self.page.url}: "
                f"visible={metrics['visible_width']:.0f}x"
                f"{metrics['visible_height']:.0f}, need {min_px}px"
            )
        return metrics

    # -- overflow and screenshots ---------------------------------------
    def overflow_px(self) -> int:
        data = self.page.evaluate(
            """() => ({
                innerWidth: window.innerWidth,
                documentWidth: document.documentElement.scrollWidth,
            })"""
        )
        return max(0, int(data["documentWidth"]) - int(data["innerWidth"]))

    def check_overflow(self, state: str, *, mobile: bool = False) -> int:
        data = self.page.evaluate(
            """() => ({
                innerWidth: window.innerWidth,
                documentWidth: document.documentElement.scrollWidth,
            })"""
        )
        overflow = max(0, int(data["documentWidth"]) - int(data["innerWidth"]))
        entry = {
            "state": state,
            "url": self.page.url,
            "viewport": self.page.viewport_size,
            "inner_width": int(data["innerWidth"]),
            "document_width": int(data["documentWidth"]),
            "overflow_px": overflow,
            "ok": overflow <= 1,
            "timestamp": utc_now(),
        }
        self.overflow_checks.append(entry)
        if mobile and overflow > 1:
            self.mobile_overflow_failures.append(entry)
        return overflow

    def screenshot(
        self,
        name: str,
        *,
        focus: str,
        cycle_stages: int,
        tabs: int,
        verified: list[str],
        extra_counts: dict[str, object] | None = None,
    ) -> None:
        self.page.wait_for_timeout(100)
        target = self.out / name
        overflow = self.overflow_px()
        console_start = self._console_cursor
        self.page.screenshot(path=str(target), animations="disabled")
        timestamp = utc_now()
        self._console_cursor = len(self.console_errors)
        width, height = png_size(target)
        viewport = self.page.viewport_size or {}
        expected_width = int(viewport.get("width", 0))
        expected_height = int(viewport.get("height", 0))
        if (width, height) != (expected_width, expected_height):
            raise CaptureError(
                f"{name} has size {width}x{height}, expected "
                f"{expected_width}x{expected_height} for the active viewport"
            )
        entry = {
            "file": name,
            "status": "captured",
            "url": self.page.url,
            "viewport": {"width": width, "height": height},
            "sha256": sha256(target),
            "bytes": target.stat().st_size,
            "timestamp": timestamp,
            "scroll_y": self.scroll_y(),
            "console_errors": [
                dict(item) for item in self.console_errors[console_start:]
            ],
            "overflow_px": overflow,
            "counts": {
                "cycle_stages": cycle_stages,
                "tabs": tabs,
                **(extra_counts or {}),
            },
            "focus": focus,
            "verified_selectors": verified,
        }
        self.shots.append(entry)
        print(
            f"  captured {name} ({width}x{height}, {entry['bytes']:,} bytes, "
            f"overflow={overflow}px)"
        )

    def record_skip(self, name: str, reason: str) -> None:
        target = self.out / name
        if target.exists():
            target.unlink()
        entry = {
            "file": name,
            "status": "skipped",
            "reason": reason,
            "url": self.page.url,
            "viewport": self.page.viewport_size,
            "sha256": None,
            "timestamp": utc_now(),
            "console_errors": [
                dict(item) for item in self.console_errors[self._console_cursor:]
            ],
            "overflow_px": self.overflow_px(),
            "counts": {
                "cycle_stages": self.page.locator("[data-agent-step]").count(),
                "tabs": self.page.locator("[data-codebase-tab]").count(),
            },
        }
        self._console_cursor = len(self.console_errors)
        self.skipped.append(entry)
        print(f"  skipped {name}: {reason}")

    # -- capture groups -------------------------------------------------
    def capture_migrator(self) -> None:
        self.open(f"/migrator?run={quote(self.run_id)}")
        panel = self.require_visible(".agent-loop-panel", "migrator agent loop panel")
        self.expect_count("[data-agent-step]", 5, "Migrator cycle stages")
        self.expect_count("[data-agent-stage]", 5, "Migrator stage panels")
        self.require_visible(".agent-cycle", "Migrator agent cycle")
        self.require_visible(".agent-narrative-panel", "Migrator narrative panel")
        self.counts["migrator_cycle_stages"] = 5
        self.counts["migrator_stage_panels"] = 5
        status = panel.first.get_attribute("data-migration-status") or ""
        if status == "running":
            raise CaptureError(
                f"migrator run {self.run_id!r} is still running; wait for it to "
                "finish before capturing deterministic stage panels"
            )

        # Show the whole agent cycle and the explanatory narrative in one
        # 1440x900 viewport. The page hero is intentionally above the crop;
        # the requested cycle + narrative are both fully readable.
        cycle_top = self.absolute_top(".agent-cycle")
        self.scroll_to(cycle_top - 16)
        self.require_in_viewport(".agent-cycle", "Migrator agent cycle")
        self.require_in_viewport(
            ".agent-narrative-panel .panel-head", "Migrator narrative heading"
        )
        self.require_in_viewport(
            ".agent-narrative", "Migrator narrative paragraph"
        )
        self.screenshot(
            "migrator-loop-1440x900.png",
            focus="Agent cycle and the What-just-happened narrative",
            cycle_stages=5,
            tabs=0,
            verified=[
                ".agent-loop-panel",
                ".agent-cycle",
                "[data-agent-step]",
                ".agent-narrative-panel .panel-head",
                ".agent-narrative",
            ],
        )

        for spec in STAGE_SPECS:
            index = spec["index"]
            name = spec["name"]
            stage_panel = f'[data-agent-stage="{index}"]'
            artifact = f"{stage_panel} {spec['artifact']}"
            self.click(
                f'[data-agent-step="{index}"]', f"{name} stage button"
            )
            self.require_visible(stage_panel, f"{name} stage panel")
            self.scroll_element_top(stage_panel, offset=16)
            self.require_in_viewport(stage_panel, f"{name} stage panel")
            self.require_text(
                f"{stage_panel} .stage-count",
                spec["count"],
                f"{name} stage count",
            )
            self.require_visible(artifact, f"{name} artifact")
            self.require_in_viewport(artifact, f"{name} artifact")

            extra_counts: dict[str, object] = {}
            if name == "Scout":
                rows = self.expect_min_count(
                    f"{stage_panel} .stage-artifact table tbody tr",
                    1,
                    "Scout evidence rows",
                )
                extra_counts["evidence_rows"] = rows
            elif name == "Architect":
                rows = self.expect_min_count(
                    f"{stage_panel} .stage-artifact table tbody tr",
                    1,
                    "Architect package rows",
                )
                if rows != 5:
                    raise CaptureError(
                        f"Architect package table should show 5 packages, found {rows} "
                        f"on {self.page.url}"
                    )
                extra_counts["package_rows"] = rows
            elif name == "Guardian":
                gate_cards = self.expect_min_count(
                    f"{stage_panel} .stage-artifact .gate-card",
                    1,
                    "Guardian assumption gate cards",
                )
                rule_rows = self.expect_min_count(
                    f"{stage_panel} .stage-artifact table tbody tr",
                    1,
                    "Guardian rule-group rows",
                )
                if gate_cards + rule_rows != 11:
                    raise CaptureError(
                        "Guardian gate story should total 11 (3 assumption gates + "
                        f"8 rule groups), found {gate_cards}+{rule_rows} on "
                        f"{self.page.url}"
                    )
                extra_counts["assumption_gates"] = gate_cards
                extra_counts["rule_groups"] = rule_rows
                extra_counts["gates_total"] = gate_cards + rule_rows
            elif name == "Critic":
                checks = self.expect_count(
                    f"{stage_panel} .stage-artifact .verification-list > li",
                    7,
                    "Critic independent checks",
                )
                extra_counts["checks"] = checks
            elif name == "Scribe":
                seals = self.expect_count(
                    f"{stage_panel} .stage-artifact .seal-card",
                    4,
                    "Scribe seal cards",
                )
                extra_counts["seal_cards"] = seals

            self.screenshot(
                f"migrator-{name.lower()}-1440x900.png",
                focus=spec["focus"],
                cycle_stages=5,
                tabs=0,
                verified=[
                    stage_panel,
                    f"{stage_panel} .stage-count",
                    artifact,
                ],
                extra_counts=extra_counts,
            )

    def capture_live(self) -> None:
        self.open(f"/migrator?run={quote(self.run_id)}")
        total = self.page.locator(".reasoning-card").count()
        if total == 0:
            self.record_skip(
                "migrator-live-1440x900.png",
                "No live reasoning card on this run: the migrator LLM mode is "
                "offline, so a live screenshot would be fabricated.",
            )
            return

        for index in range(5):
            stage_panel = f'[data-agent-stage="{index}"]'
            if self.page.locator(f"{stage_panel} .reasoning-card").count() == 0:
                continue
            self.click(
                f'[data-agent-step="{index}"]',
                f"live reasoning stage button {index}",
            )
            self.require_visible(stage_panel, "live reasoning stage panel")
            self.scroll_element_top(f"{stage_panel} .reasoning-card", offset=16)
            self.require_in_viewport(
                f"{stage_panel} .reasoning-card", "live reasoning card"
            )
            self.screenshot(
                "migrator-live-1440x900.png",
                focus="Live grounded reasoning card inside the stage panel",
                cycle_stages=5,
                tabs=0,
                verified=[
                    stage_panel,
                    f"{stage_panel} .reasoning-card",
                ],
            )
            return

        self.record_skip(
            "migrator-live-1440x900.png",
            "Reasoning markup exists on the page but no visible stage panel "
            "contained a capturable live reasoning card.",
        )

    def capture_codebase(self) -> None:
        self.open(f"/codebase?case={quote(self.case_id)}")
        self.expect_count("[data-codebase-tab]", 5, "Codebase tabs")
        self.expect_count("[data-codebase-stage]", 5, "Codebase cycle stages")
        stage_cards = self.expect_count(".stage-card", 5, "Codebase stage cards")
        self.require_visible(".agent-cycle", "Codebase agent cycle")
        self.require_visible(".stage-card-grid", "Codebase stage-card grid")
        self.require_visible(".agent-narrative-panel", "Codebase narrative panel")
        self.counts["codebase_cycle_stages"] = 5
        self.counts["codebase_tabs"] = 5
        self.counts["codebase_stage_cards"] = stage_cards

        self.click('[data-codebase-tab="loop"]', "Five-agent loop tab")
        # Fit the narrative, the full cycle, and the first row of stage-card
        # names into one viewport. The rest of the stage cards continue below
        # the fold by design.
        grid_top = self.absolute_top(".stage-card-grid")
        narrative_top = self.absolute_top(".agent-narrative-panel")
        viewport_height = int((self.page.viewport_size or DESKTOP)["height"])
        self.scroll_to(
            min(
                grid_top - (viewport_height - 42),
                narrative_top + 8,
            )
        )
        self.require_in_viewport(
            ".agent-narrative-panel .panel-head", "Codebase narrative heading"
        )
        self.require_in_viewport(
            ".agent-narrative", "Codebase narrative paragraph"
        )
        self.require_in_viewport(".agent-cycle", "Codebase agent cycle")
        self.require_in_viewport(
            ".stage-card-head", "Codebase stage cards", full=False, min_px=30
        )
        self.require_in_viewport(
            ".stage-card strong", "first stage-card name"
        )
        self.screenshot(
            "codebase-loop-1440x900.png",
            focus="Narrative, cycle, and the first stage-card row",
            cycle_stages=5,
            tabs=5,
            verified=[
                ".agent-narrative-panel .panel-head",
                ".agent-narrative",
                ".agent-cycle",
                ".stage-card-grid",
                ".stage-card strong",
                ".tab-bar",
            ],
            extra_counts={"stage_cards": stage_cards},
        )

        self.click('[data-codebase-tab="patches"]', "Patches tab")
        self.require_visible("#cb-patches", "Patches tab panel")
        patches = self.expect_min_count(".patch-card", 1, "patch cards")
        self.require_text(
            ".tab-button.is-active", r"^Patches \(", "active Patches tab"
        )
        self.scroll_element_top(".tab-bar", offset=16)
        self.require_in_viewport(".tab-bar", "Codebase tab bar")
        self.require_in_viewport(
            ".patch-card", "first patch card", full=False, min_px=20
        )
        self.screenshot(
            "codebase-patches-1440x900.png",
            focus="Active Patches tab and the Architect patch bundle",
            cycle_stages=5,
            tabs=5,
            verified=[".tab-bar", "#cb-patches", ".patch-card"],
            extra_counts={"patch_cards": patches},
        )

        self.click('[data-codebase-tab="upgrade"]', "Upgrade tab")
        self.require_visible("#upgrade-select", "Upgrade scenario select")
        values = self.page.locator("#upgrade-select option").evaluate_all(
            "options => options.map((option) => option.value)"
        )
        if UPGRADE_SCENARIO not in values:
            raise CaptureError(
                f"required upgrade scenario {UPGRADE_SCENARIO!r} is not present "
                f"on {self.page.url}; found {values!r}"
            )
        self.page.locator("#upgrade-select").select_option(UPGRADE_SCENARIO)
        with self.page.expect_navigation(
            wait_until="networkidle", timeout=self.timeout
        ):
            self.page.locator(
                'form.upgrade-form button[type="submit"]'
            ).first.click()
        self.page.wait_for_timeout(200)
        self.click('[data-codebase-tab="upgrade"]', "Upgrade tab after submit")
        self.require_visible(".impact-card", "Upgrade impact card")
        self.require_text(
            ".impact-card", re.escape(UPGRADE_SCENARIO), "upgrade impact scenario"
        )
        selected = self.page.locator("#upgrade-select").input_value()
        if selected != UPGRADE_SCENARIO:
            raise CaptureError(
                f"upgrade scenario selection was lost after submit: {selected!r} "
                f"on {self.page.url}"
            )
        resume_cards = self.expect_count(
            ".impact-card .resume-card", 3, "upgrade resume options"
        )
        impact_status = (
            self.page.locator(".impact-card .pill").first.inner_text().strip()
        )
        self.scroll_element_top(".tab-bar", offset=16)
        self.require_in_viewport(".tab-bar", "Codebase tab bar")
        self.require_in_viewport(".impact-card", "Upgrade impact card")
        self.screenshot(
            "codebase-upgrade-1440x900.png",
            focus=(
                f"Active Upgrade tab with the {UPGRADE_SCENARIO} impact card"
            ),
            cycle_stages=5,
            tabs=5,
            verified=[
                ".tab-bar",
                "#upgrade-select",
                ".impact-card",
                ".impact-card .resume-card",
            ],
            extra_counts={
                "resume_options": resume_cards,
                "impact_status": impact_status,
            },
        )

    def capture_case_studies(self) -> None:
        self.open("/case-studies")
        self.require_visible(".page-head h1", "case-studies heading")
        self.require_visible(".case-grid", "case-study grid")
        cards = self.expect_count(".case-card", 2, "case-study cards")
        self.scroll_to(0)
        self.require_in_viewport(
            ".case-grid", "case-study grid", full=False, min_px=100
        )
        self.screenshot(
            "case-studies-1440x900.png",
            focus="Both migration story cards with their outcome strips",
            cycle_stages=0,
            tabs=0,
            verified=[".page-head h1", ".case-grid", ".case-card"],
            extra_counts={"case_cards": cards},
        )
        self.counts["case_studies"] = cards

    def verify_mobile_overflow(self) -> None:
        self.page.set_viewport_size(MOBILE)

        self.open(f"/migrator?run={quote(self.run_id)}")
        self.check_overflow("migrator: top", mobile=True)
        for index in range(5):
            self.click(
                f'[data-agent-step="{index}"]', f"mobile stage {index} button"
            )
            self.check_overflow(f"migrator: stage {index}", mobile=True)

        self.open(f"/codebase?case={quote(self.case_id)}")
        for tab in ("loop", "findings", "patches", "gates", "upgrade"):
            self.click(
                f'[data-codebase-tab="{tab}"]', f"mobile {tab} tab"
            )
            self.check_overflow(f"codebase: {tab}", mobile=True)

        self.click('[data-codebase-tab="upgrade"]', "mobile upgrade tab")
        self.page.locator("#upgrade-select").select_option(UPGRADE_SCENARIO)
        with self.page.expect_navigation(
            wait_until="networkidle", timeout=self.timeout
        ):
            self.page.locator(
                'form.upgrade-form button[type="submit"]'
            ).first.click()
        self.page.wait_for_timeout(200)
        self.click('[data-codebase-tab="upgrade"]', "mobile upgrade tab after submit")
        self.require_visible(".impact-card", "mobile upgrade impact card")
        self.check_overflow("codebase: upgrade impact", mobile=True)

        self.open("/case-studies")
        self.check_overflow("case-studies: top", mobile=True)

    def capture_mobile(self) -> None:
        self.page.set_viewport_size(MOBILE)

        self.open(f"/migrator?run={quote(self.run_id)}")
        self.require_visible(".agent-loop-panel", "mobile Migrator panel")
        self.scroll_to(0)
        self.screenshot(
            "migrator-390x844.png",
            focus="Mobile Migrator page top",
            cycle_stages=5,
            tabs=0,
            verified=[".agent-hero", ".agent-loop-panel"],
        )

        self.open(f"/codebase?case={quote(self.case_id)}")
        self.click('[data-codebase-tab="loop"]', "mobile loop tab")
        self.scroll_to(0)
        self.require_visible(".agent-hero", "mobile codebase heading")
        self.screenshot(
            "codebase-390x844.png",
            focus="Mobile Codebase lab page top",
            cycle_stages=5,
            tabs=5,
            verified=[".agent-hero", ".tab-bar", ".case-switcher"],
        )

        self.open("/case-studies")
        self.require_visible(".page-head h1", "mobile case-studies heading")
        self.scroll_to(0)
        self.screenshot(
            "case-studies-390x844.png",
            focus="Mobile migration stories page top",
            cycle_stages=0,
            tabs=0,
            verified=[".page-head h1", ".case-grid"],
        )

    # -- orchestration and manifest -------------------------------------
    def capture_all(self) -> None:
        print("Migrator")
        self.capture_migrator()
        self.capture_live()
        print("Codebase lab")
        self.capture_codebase()
        print("Case studies")
        self.capture_case_studies()
        print("Mobile overflow checks")
        self.verify_mobile_overflow()
        print("Mobile screenshots")
        self.capture_mobile()

    def finalize(self) -> None:
        failures: list[str] = []
        if self.console_errors:
            failures.append(f"{len(self.console_errors)} console error(s)")
        if self.blocked_requests:
            failures.append(
                f"{len(self.blocked_requests)} external request(s) blocked"
            )
        if self.mobile_overflow_failures:
            failures.append(
                "horizontal overflow above 1px at 390: "
                + ", ".join(
                    f"{item['state']}={item['overflow_px']}px"
                    for item in self.mobile_overflow_failures
                )
            )
        missing = [
            name
            for name in TARGET_FILES
            if not (self.out / name).exists()
            and name not in {item["file"] for item in self.skipped}
        ]
        if missing:
            failures.append(f"missing output file(s): {', '.join(missing)}")
        if failures:
            raise CaptureError("; ".join(failures))

    def manifest(self, *, ok: bool, error: str | None) -> dict:
        mobile_overs = [
            item["overflow_px"]
            for item in self.overflow_checks
            if (item.get("viewport") or {}).get("width") == MOBILE["width"]
        ]
        return {
            "schema_version": 1,
            "generated_at": utc_now(),
            "base_url": self.base_url,
            "run_id": self.run_id,
            "case_id": self.case_id,
            "out_dir": str(self.out),
            "viewports": {"desktop": DESKTOP, "mobile": MOBILE},
            "counts": self.counts,
            "console_errors": self.console_errors,
            "console_error_count": len(self.console_errors),
            "blocked_external_requests": self.blocked_requests,
            "blocked_external_request_count": len(self.blocked_requests),
            "overflow_checks": self.overflow_checks,
            "max_mobile_overflow_px": max(mobile_overs, default=0),
            "mobile_overflow_failures": self.mobile_overflow_failures,
            "screenshots": self.shots,
            "skipped": self.skipped,
            "screenshots_captured": len(self.shots),
            "screenshots_skipped": len(self.skipped),
            "ok": ok,
            "error": error,
        }

    def write_manifest(self, *, ok: bool, error: str | None) -> Path:
        target = self.out / "capture-manifest.json"
        target.write_text(
            json.dumps(self.manifest(ok=ok, error=error), indent=2) + "\n",
            encoding="utf-8",
        )
        return target


def main() -> int:
    args = parse_args()
    out = Path(args.out).expanduser().resolve()
    out.mkdir(parents=True, exist_ok=True)
    for name in TARGET_FILES:
        target = out / name
        if target.exists():
            target.unlink()

    try:
        wait_health(args.base_url)
    except CaptureError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1

    print(f"Capture source: {args.base_url}")
    print(f"Output: {out}")
    error: str | None = None
    capture: AgentCapture | None = None

    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(headless=True)
        context = browser.new_context(
            viewport=DESKTOP,
            device_scale_factor=1,
            reduced_motion="reduce",
            color_scheme="light",
        )
        page = context.new_page()
        page.set_default_timeout(args.timeout)
        capture = AgentCapture(
            page=page,
            base_url=args.base_url,
            out=out,
            run_id=args.run_id,
            case_id=args.case_id,
            timeout=args.timeout,
        )
        try:
            capture.capture_all()
            capture.finalize()
        except CaptureError as exc:
            error = str(exc)
            print(f"ERROR: {error}", file=sys.stderr)
        except Exception as exc:  # noqa: BLE001 - report and fail clearly
            error = f"{type(exc).__name__}: {exc}"
            print(f"ERROR: {error}", file=sys.stderr)
            traceback.print_exc()
        finally:
            manifest_path = capture.write_manifest(ok=error is None, error=error)
            context.close()
            browser.close()

    if capture is None:
        print("ERROR: no capture object was created", file=sys.stderr)
        return 1

    print("")
    print(f"Captured {len(capture.shots)} screenshot(s) -> {out}")
    print(f"Manifest -> {manifest_path}")
    if capture.skipped:
        for item in capture.skipped:
            print(f"Skipped {item['file']}: {item['reason']}")
    print(
        "Checks: "
        f"console_errors={len(capture.console_errors)} "
        f"blocked_external_requests={len(capture.blocked_requests)} "
        f"mobile_overflow_failures={len(capture.mobile_overflow_failures)}"
    )

    if error:
        print(f"FAILED: {error}", file=sys.stderr)
        return 1
    print("OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
