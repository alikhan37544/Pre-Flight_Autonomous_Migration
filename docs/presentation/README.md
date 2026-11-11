# PreFlight presentation package

A self-contained, offline 23-slide deck for judges, academics, and technical reviewers. It explains the migration problem, the evidence model, the live demo, the five-agent feature migrator, the codebase lab, the evaluation, the engineering hardening, the prior art, and the honest viability case.

**Open:** <http://127.0.0.1:8090/index.html> after starting the local server below.

The deck has no external fonts, scripts, styles, CDNs, analytics, or network calls. It loads only local files from this directory, including a small inline data-URI favicon. The application screenshots are in `assets/`.

---

## Run it

From the repository root:

```bash
python -m http.server 8090 -d docs/presentation
```

Then open:

```text
http://127.0.0.1:8090/index.html
```

The deck also works by opening `docs/presentation/index.html` directly in a modern browser, but a local HTTP server is recommended so deep links and asset paths behave consistently.

`python` must be Python 3 on the machine; the repository’s shared venv also works:

```bash
/home/understressengineer/programming/Preflight-CloudMigration/v2/.venv/bin/python \
  -m http.server 8090 -d docs/presentation
```

Stop the server with `Ctrl+C`.

## Controls

| Input | Action |
|---|---|
| `→` `↓` `Space` `PageDown` | Next slide |
| `←` `↑` `PageUp` | Previous slide |
| `Home` / `End` | First / last slide |
| `n` | Toggle substantive speaker notes |
| `?` | Open / close the keyboard help dialog |
| `Esc` | Close help or notes |
| `p` (or the **PDF** button) | Print / save as PDF |
| Swipe left / right | Next / previous on touch screens |

Deep links use `#slide-1` … `#slide-23`, for example:

```text
http://127.0.0.1:8090/index.html#slide-11
```

The current slide is reflected in the address bar; pasting the URL opens that slide.

## Print or save as PDF

The print stylesheet is designed for one 16:9 slide per page.

1. Open the deck.
2. Press `p` or click **PDF**.
3. Choose **Landscape**, **Background graphics: on**, **Margins: none**.
4. Save as PDF.

The stylesheet sets `@page { size: 1600px 900px; margin: 0; }` and prints every slide on its own page. A headless Chromium check produced **23 tagged pages at 1200 × 675 pt** (16:9) with all screenshots, diagrams, and annotations present. Every printed page also carries the boundary line “Synthetic estate · not affiliated with Guidewire · Official Cloud Assurance: not run.” The packaged `PreFlight-deck.pdf` must match `index.html`.

## File map

| Path | Purpose |
|---|---|
| `index.html` | Complete deck: inline CSS/JS, 23 slides, speaker notes, help, print CSS. No external dependencies. |
| `PreFlight-deck.pdf` | Rendered 23-page, 16:9 PDF of the current deck (1200 × 675 pt per page). |
| `README.md` | This file. |
| `DEMO-RUNBOOK.md` | Five-minute live demo script, setup, fallbacks, Q&A, claims to avoid, exact IDs, URLs. |
| `sources.md` | Public sources, access dates, rate-limited/gated notes, prior-art citations. |
| `evidence.json` | Machine-readable slide data, run counts, metrics, capture-time hashes, source list, asset hashes. |
| `ITERATION-LOG.md` | Demo-hardening loop notes and remaining risks. |
| `assets/workbench-1440x900.png` | Workbench viewport at 1440 × 900. |
| `assets/workbench-focus-1440x900.png` | Cropped Workbench summary strip + feature spine used on slide 6. |
| `assets/workbench-1280x900.png`, `workbench-1280x720.png` | Workbench at the 1280 widths. |
| `assets/workbench-full-1440.png` | Full-page Workbench for annotation/reference. |
| `assets/workbench-390x844.png`, `workbench-390x844-full.png` | Mobile Workbench viewport/full page. |
| `assets/workbench-evidence-1440x900.png` | Workbench scrolled to the evidence drawer. |
| `assets/workbench-evidence-drawer.png` | EV-0001 evidence card crop. |
| `assets/manifest-excluded-1440x900.png`, `manifest-focus-1440x900.png` | Manifest filtered to the four excluded files; focus crop on slide 7. |
| `assets/manifest-excluded-1280x900.png` | Same filter at 1280 × 900. |
| `assets/reconstruction-1440x900.png` | Reconstruction in the read-only seed state (12 pending / 3 assumptions / 9 audit events). |
| `assets/reconstruction-after-decision-1440x900.png`, `reconstruction-after-decision-focus-1440x900.png` | Isolated copy after M-01 accept + M-12 reject: A-DEC-04, 4 assumptions, 11 audit events. |
| `assets/reconstruction-m12-row.png` | M-12 row after rejection (reference; slide 8 uses a legible HTML row). |
| `assets/reconstruction-assumptions-1440x900.png` | Assumption register after the reject. |
| `assets/findings-1440x900.png`, `findings-focus-1440x900.png` | Findings with the selected ERR00-G row and SBT flag; source crops. |
| `assets/findings-table-clean-1440x900.png` | Clean crop below the app’s table-scroll hint, used on slide 9; 8 of 24 rows plus the selected F-002 detail. |
| `assets/findings-guard-query-make.png` | Precision-guard reference crop; slide 9 carries the same claim as a text callout. |
| `assets/findings-1280x720.png` | Proof that Findings renders at 1280 without horizontal overflow. |
| `assets/assistant-citation-1440x900.png`, `assistant-citation-panel.png` | Motorcycle_Ext cited answer and crop. |
| `assets/assistant-refusal-1440x900.png`, `assistant-refusal-panel.png` | Territory refusal and crop. |
| `assets/evaluation-1440x900.png`, `evaluation-intervals.png` | Evaluation summary and interval chart. |
| `assets/packet-1440x900.png`, `packet-focus-1440x900.png` | Post-decision packet: 11 events / 4 assumptions. |
| `assets/packet-predecision-1440x900.png`, `packet-predecision-focus-1440x900.png` | Seed packet: 9 events / 3 assumptions. |
| `assets/packet-predecision-full-1440.png` | Full-page seed packet for reference. |
| `assets/agents/migrator-*.png` | Real Migrator captures used on slides 14–16: Scout, Guardian, Critic, and Scribe. |
| `assets/agents/codebase-*.png` | Real Codebase-lab captures used on slides 17 and 19: case studies and upgrade. |
| `assets/agents/case-studies-1440x900.png`, `case-studies-outcomes-focus.png` | Real migration-stories capture and the wider crop. |
| `assets/agents/case-studies-outcome-strips.png` | Clean outcome-strip crop used on slide 17; it excludes the app’s program-label row. |
| `assets/deck-23/` | Validation proofs for all 23 slides at 1440 × 900 and 390 × 844, plus the dense-slide 1280 × 720 / 1024 × 768 / 1920 × 1080 checks. |
| `assets/deck-slide-01-1440x900.png` … `deck-slide-16-1440x900.png` | Legacy validation proofs for the first 16 slides (pre-agent block). |
| `assets/capture-manifest.json` | Capture timestamp, URLs, sizes, SHA-256, and post-decision facts. |
| `assets/deck-validation.json` | Per-viewport navigation/overflow/console/external-request results and PDF facts. |
| `assets/marker-hints.json` | Measured element positions used by the capture script (debug); callouts are text-only and do not overlay evidence. |
| `assets/.gitignore` | Keeps generated `.webm` walkthroughs local. |

All review-workbench screenshots are from run `R-DEMO-001` (`demo-slice-300`) on 2026-11-10. The Migrator and Codebase-lab captures under `assets/agents/` are from the same run on 2026-11-11 (`assets/agents/capture-manifest.json` records the loopback URL, hashes, and counts). The main set is live from a loopback server; the after-decision set uses an isolated temporary copy so the demo run stays at 12 pending dispositions. Post-decision state: **11 audit events, 4 assumptions, A-DEC-04**. Slide 12 deliberately shows no packet or audit-head value: both change with reviewer decisions and packet refresh, so the deck says “read live.” The only visible digest is the stable fixture snapshot hash (`bd4a8a4b338a…`). The main packet hash covers rendered packet HTML; `packet_json` covers canonical JSON; content digests bind findings, mappings, and evidence; the audit head covers the chain.

## Refresh the screenshots

Start the application server first (see `docs/DEMO-SCRIPT.md` or `Makefile`):

```bash
make demo
curl -s http://127.0.0.1:8000/api/health
```

From the repository root, with the shared venv:

```bash
/home/understressengineer/programming/Preflight-CloudMigration/v2/.venv/bin/python \
  scripts/capture_demo.py \
  --base-url http://127.0.0.1:8000 \
  --run-id R-DEMO-001 \
  --out docs/presentation/assets \
  --data-source /home/understressengineer/programming/Preflight-CloudMigration/v2/data \
  --with-decisions \
  --deck
```

This single command captures the 1440 × 900 set and focus crops, the 1280 × 900 / 1280 × 720 set, the full-page and mobile views, the assistant crops, the evaluation chart, and the pre-decision packet. It copies `R-DEMO-001` to a temporary data directory and starts a **second loopback Uvicorn** for the post-decision set: Accept M-01, Reject M-12, then capture the 11-event / 4-assumption reconstruction, assumption register, and packet. The live demo run is never mutated.

The legacy `--deck` path in `scripts/capture_demo.py` still enumerates the original 16 slides. The current 23-slide package was validated with a separate Playwright run: all 23 slides at **1920 × 1080, 1440 × 900, 1280 × 720, 1024 × 768, and 390 × 844**, with **0** console errors, **0** external requests, **0** desktop layout overflow/clipping, and **0** horizontal overflow at 390. The 390 footer shows the complete boundary line including “Official Cloud Assurance: not run.” That run wrote the proofs under `assets/deck-23/` and regenerated `PreFlight-deck.pdf` (**23 pages, 1200 × 675 pt**, boundary line on every page). The app-page captures under `assets/agents/` come from `scripts/capture_agents.py` and the separate agent runs described below. Keep `capture_demo.py --deck` in sync with the slide count before using it as the deck regenerator again.

The script is read-only against the live application: it does not upload, accept/reject, or restart the live run. The isolated server is terminated and its temporary copy deleted at the end.

**Agent captures (slides 13–19).** `assets/agents/` was captured on 2026-11-11 from a loopback app at `http://127.0.0.1:8010` with run `R-DEMO-001` (Cascade for the codebase captures). The capture manifest records 13 captured images, 0 console errors, 0 blocked external requests, and 0 mobile horizontal overflow. One optional capture (`migrator-live-1440x900.png`) was deliberately skipped because the migrator was in offline mode; no live reasoning card was fabricated. Slides 13–19 use the real captures where they exist and HTML for the package and gate detail so the numbers stay legible at projector size. The `case-studies-outcomes-focus.png` file is a crop of the real `case-studies-1440x900.png`, not a synthetic image.

Optional short walkthrough:

```bash
/home/understressengineer/programming/Preflight-CloudMigration/v2/.venv/bin/python \
  scripts/capture_demo.py --video
```

This writes `docs/presentation/assets/preflight-walkthrough.webm`; it is git-ignored and should not be committed by default.

If the live data directory is elsewhere, pass its parent as `--data-source` (the directory that contains `runs/`). If the app fixes are not merged, do not recapture; update the text/CSS and leave the current assets in place, then run the command again after the merge.

## Slide map

| # | Slide | Purpose |
|---:|---|---|
| 1 | Title | Evidence before the estimate; boundaries and packet preview. |
| 2 | The problem | Estimate vs inventory, four questions, four sourced pain points. |
| 3 | Why tools leave a gap | Capability map across CUE, Cloud Assurance Services, Lighthouse, SurePath, Developer Assistants, GoQu, CAST/ADDI (portfolio/code discovery), Syntra ETL (data migration/extraction), SIs; positioning footnote. |
| 4 | Solution | Nine-stage pipeline, invariants, run facts, artifact writes. |
| 5 | Evidence model | Claim anatomy, claim-strength ladder, assumption register, hash chain. |
| 6 | Demo: Workbench | 31/12/4/2/11 for PA-VEH-01; 37 vs 24 long type in two files, PA-VEH-02 dependency; 3 estate gaps; click node → evidence; synthetic-fixture note. |
| 7 | Demo: Manifest | 4 excluded files named with reasons; source hash unchanged; fixture-realism note. |
| 8 | Demo: Reconstruction | **Post-decision** state: 4 assumptions; 12 dispositions; M-01 accept; M-12 reject → A-DEC-04; `_gen` writes 0; Cloud Retrofit scope note. |
| 9 | Demo: Findings | 24 findings / 8 rules; two standard families; clean crop shows 8 of 24 rows; precision guard (`Query.make`) as a text callout; 24 hard negatives silent. |
| 10 | Demo: Assistant | Territory refusal; Motorcycle_Ext citation; retrieval-only, model off. |
| 11 | Demo: Evaluation | Six metrics M1–M6; M6 F1 1.00 (24 TP / 0 FP / 0 FN); 24/24 guard count separate; intervals, baselines, holdout, limitations. |
| 12 | Demo: Packet | **Post-decision** state: 126 evidence, 11 audit events / 4 assumptions; packet/audit hashes labelled read live; snapshot hash stable; two-step verify-packet + verify-audit. |
| 13 | Demo: Migrator handoff chain | Five-agent feature pass: Scout → Architect → Guardian → Critic → Scribe; **seeded state: 3 assumptions / 11 gates**; visible Scribe-vs-Planner line; 4-term glossary; `completed_with_gates`; reality-boundary callout; optional live MiMo run noted in speaker notes. |
| 14 | Demo: Scout → Architect | Scout’s 300 files / 101 evidence / 31 links / 24 findings / 12 dispositions; five work packages with bytes, evidence IDs, WP-05’s G-03 gate, and all `pending`. |
| 15 | Demo: Guardian | **Seeded state: 3 assumptions**; 24 findings → 8 rule groups × 3 + 3 assumptions = 11 human gates / 6 high; all 8 rule groups visible; gate-level check; Guardian independence. |
| 16 | Demo: Critic + Scribe | Critic 7/7 package-integrity checks; four seal cards (plan, report, bundle, 12-event log); 8 listed files; separate review-packet and migrator audit chains. |
| 17 | Demo: Codebase stories | Cascade 18 findings / 22 patches / 2 iterations / 10 gates; Harbor 20 / 21 / 2 / 11; 13 vs 15 rules fired; illustrative synthetic footprints; **type-level APD naming preparation only, not conversion**; clean outcome-strip crop; visible Scribe-vs-Planner line. |
| 18 | Demo: Refactor + SARIF | 16 rule families; JDBC source and corrected `VehicleRatingQueryService` draft (generator naming artifact noted); SARIF 2.1.0 explainer (18 / 13 Cascade, 20 / 15 Harbor); Planner assembles and seals, nothing compiled; 5-term glossary. |
| 19 | Demo: Upgrade resilience | Five simulated GWCP 2026.10 → 2027.04 scenarios; generation 1 → 2; **per-scenario exposure, not additive** (30/28 across 22/21 patches); revalidate / rollback / defer; APD 24 → 20 simulation; five named failure states. |
| 20 | Engineering rigor | 481 passed with the current pytest suite, Playwright, 18/18 freeze hashes, 9 seed audit events, security, flaws found and fixed. |
| 21 | Novelty & prior art | Feature location, traceability, Reversa, GSN, honest scorecard. |
| 22 | Viability | Kill risks, vendor-independent wedge (not independently validated), acceptance tests, roadmap. |
| 23 | Close | The three-line standard, pilot ask, Saundarya Singh / repository / MIT. |

## Accessibility and quality notes

- Semantic `h1`/`h2` headings, labelled slide regions, skip link, visible focus rings, `aria-live` slide announcements, and reduced-motion support.
- Keyboard navigation works without a mouse; the help dialog traps focus while open and returns focus on close. The closed speaker-notes panel is `inert` and not tabbable.
- Screenshots have descriptive `alt` text; numbered callouts are supplemented by a text legend, not colour alone. Markers on slides 6, 7, 8, 9, and 12 sit in the image margin (or a known gutter) at the measured row, so they do not cover the text they explain. The capture script validates each crop against the live DOM and records the proof in `assets/capture-manifest.json`.
- Supporting text uses a **10.5px CSS floor** at 1440 and 390; 1280 × 720 and 1024 × 768 keep dense slides on one screen with a 0.96 fit scale (≈10.1px effective). Title metadata, dot labels, pipeline numbers, and slide-12 dark labels meet 4.5:1 against their backgrounds. Dense slides compact at short projector heights; secondary detail moves to speaker notes rather than clipping.
- At 390 px the capability matrix is a labelled, keyboard-focusable scroll region (`tabindex="0"`, `role="region"`). Desktop UI captures are hidden below 640px because they would render at ~3–5px; the HTML tables, cards, and captions carry the data, except the near-1:1 assistant panels on slide 10. The slide 18 code panes are keyboard-focusable scroll regions. At 1920 px the stage-label column sizes to content so “RECONSTRUCT” cannot collide with the mapped text.
- Charts are inline SVG with a text caption and equivalent numbers in the surrounding slide.
- Validation was run with Playwright at **1920 × 1080, 1440 × 900, 1280 × 720, 1024 × 768, and 390 × 844**: all 23 slides navigated, zero console errors, zero external requests, zero layout overflow/clipping at desktop viewports, zero horizontal overflow at 390, zero stage-label overlaps at 1920, and a focusable mobile matrix. The 390 footer is unclipped and includes “Official Cloud Assurance: not run.” Print produced a **tagged 23-page PDF at 1200 × 675 pt** with the boundary line on every page. A subtle slide-enter fade/translate and a gentle agent-loop pulse honour `prefers-reduced-motion`. See `assets/deck-23/validation.json`, `assets/agents/capture-manifest.json`, and `evidence.json`.
- New agent and codebase slides use real application captures where they remain legible and HTML for exact numbers, package rows, gates, seals, and code snippets. Scout is used on slide 14; Guardian on 15; Critic and Scribe on 16; the clean outcome strips on 17; the upgrade tab on 19. Slides 13 and 18 use HTML diagrams and code instead of unreadable thumbnails. The 2027.04 release scenarios are simulations, not published release notes.
- The deck keeps the explicit **Reality boundary** callout on slide 13 and repeats the boundary on slides 17 and 19: synthetic rehearsal, not an actual migration; no tenant; no Gosu/Java compile against Guidewire; no official Cloud Assurance. Slide 18’s glossary defines CDA as streaming/export to S3 Parquet, with synchronous reads using Gosu Query or an application API; the servlet wording correction lives in the speaker notes. Custom servlets are “not a recommended practice,” not “unsupported.”
- Repository checks on 2026-11-11: `pytest` — **481 passed**; `scripts/claims_lint.py` — **OK**; `preflight verify-packet R-DEMO-001` — **OK (packet hash, content digests, audit head)**; `preflight verify-audit R-DEMO-001` — **OK (9 seed events; 11 after the two runbook actions; audit chain only)**; freeze manifest — **18/18 recorded hashes recompute**.

## Boundaries

This is an independent academic research prototype. It is not affiliated with, endorsed by, sponsored by, or certified by Guidewire Software, Inc. “Independent” means vendor-independent, not independently validated. The demo is a synthetic rehearsal, not an actual migration. Fixtures are synthetic; the 300 files include generated filler, and the PCF/product-model/Gosu shapes are synthetic sketches, not production Guidewire formats. Official Cloud Assurance was not run. Findings are pattern-based heuristics, not official Cloud Standards checks, and are not legal, security, or compliance advice. The Cloud API extension draft targets Cloud Retrofit **without APD App** and is local and non-deployable; the `_ext` draft is a local JSON contract, not official Guidewire schema, mapping, or updater syntax. It is not compiled or tenant-validated. Impact ranges are heuristic planning ranges, not quotes.

The two codebase case studies are synthetic archetypes, not customer references. Their policy counts, PCF screen counts, Gosu file counts, integration counts, and rating volumes are **illustrative synthetic values**, not measured customer data. Harbor’s APD deliverable is type-level naming preparation (a codegen `nameOverride` draft) only; it is not a full APD conversion and does not model field-level mapping or endpoint regeneration. Cloud Data Access is a streaming/export service that lands InsuranceSuite data in S3 as Parquet, not a synchronous in-app read path; synchronous reads use Gosu Query or an application API. Public guidance describes custom servlets as “not a recommended practice,” not “unsupported.” The 2027.04 release scenarios and the 20-character APD limit are PreFlight simulations, not published Guidewire release notes.
