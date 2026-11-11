# PreFlight — 10-minute demo script

**Deck:** <http://127.0.0.1:8092/compact-10min.html>  
**Deck deep link:** <http://127.0.0.1:8092/compact-10min.html#slide-1>  
**Live app:** <http://127.0.0.1:8000/?run=R-DEMO-001&feature=PA-VEH-01>  
**Run:** `R-DEMO-001` · synthetic `demo-slice-300` · 12 slides · 10:00

**The one sentence to keep repeating:** *On a synthetic Guidewire-style estate, PreFlight produced evidence-linked candidate findings and reviewable draft refactors. Nothing was compiled, deployed, or officially assured.*

---

## Before you start (2 minutes before the clock)

1. **Deck tab (Tab 1):** open `http://127.0.0.1:8092/compact-10min.html#slide-1`.
2. **App tab (Tab 2):** open `http://127.0.0.1:8000/?run=R-DEMO-001&feature=PA-VEH-01`.
3. **Terminal tab (Tab 3):**
   ```bash
   cd /home/understressengineer/programming/Preflight-CloudMigration/v2
   .venv/bin/preflight verify-audit R-DEMO-001
   .venv/bin/preflight verify-packet R-DEMO-001
   .venv/bin/preflight verify-migration R-DEMO-001
   ```
   Read the head from the live output. **Do not read a hash from the deck as if it were live.**
4. Set the deck to 1440 × 900 or 1920 × 1080. Close notifications. Turn off screen sleep.
5. Have `docs/presentation/assets/compact/validation.json` and `docs/presentation/PreFlight-10min.pdf` ready as fallbacks.
6. Say the boundary once, early, then present the evidence. Do not open with a disclaimer speech.

**Keyboard:** `→` next · `←` previous · `Home` / `End` · `n` notes · `?` help · `p` print/PDF.  
**Deep links:** `#slide-1` … `#slide-12`.

---

## Minute-by-minute run sheet

| Time | Slide | Exact clicks / URLs | What to say | Fallback |
|---:|---|---|---|---|
| **0:00–0:35** | 1 · Title | `#slide-1` | “This is PreFlight: an offline, evidence-first review of a Guidewire-style estate. The thesis is simple — a migration estimate is only as good as the inventory underneath it.” Point at the packet card. “Three promises: every claim has evidence, every unknown has a name, every change waits for a human.” Say the boundary: “Synthetic rehearsal, not an actual migration. No tenant, no compile, not official Cloud Assurance.” | If the title feels long, stop after the three promises and the boundary. |
| **0:35–1:20** | 2 · Problem | `#slide-2` | “The estimate is the promise; the inventory is the proof.” Walk three questions: what exists, which feature it serves, what is still unknown. Then the cost: hidden scope becomes a change order because nobody could show the inventory behind the number. | Use the three promise cards only. Do not read every row. |
| **1:20–2:35** | 3 · Five-agent chain | `#slide-3`; optional Tab 2: `http://127.0.0.1:8000/migrator?run=R-DEMO-001` | Name the chain: Scout → Architect → Guardian → Critic → Scribe. Read the counts: **300 files, 101 evidence records, 31 links**; **5 packages**; **11 human gates = 3 assumptions + 8 rule groups, 6 high**; **7/7 machine checks**; **8 sealed files**. “The feature path is a straight handoff chain. The codebase lab is the cyclic variant and ends in Planner.” “No agent can approve, resolve an assumption, compile, or deploy.” | If the app is slow, stay on slide 3; every count is on the slide. Do **not** say “loop” for the feature path. |
| **2:35–3:50** | 4 · Feature demo | Tab 2: `http://127.0.0.1:8000/migrator?run=R-DEMO-001` · click the **03 Guardian** stage card, then **05 Scribe** | “Scout turns the snapshot into evidence. Architect turns dispositions into five local files. Guardian opens the eleven gates. Critic checks package integrity. Scribe seals the bundle.” “Every change is still pending because approval is a human action.” Point at **Scribe vs Planner**: Scribe seals the feature packet; Planner assembles the codebase patch plan and SARIF; neither compiles. | If stage clicks do not respond, go back to `#slide-4`; the ledger has received/produced/why-pending for all five agents. |
| **3:50–4:50** | 5 · Codebase lab | Tab 2: `http://127.0.0.1:8000/codebase?case=cascade-mutual` · click **Gates, report & SARIF** · then open `http://127.0.0.1:8000/codebase?case=harbor-pc` · click **Gates, report & SARIF** | “Cascade: 18 findings, 22 patches, 2 iterations, 10 human gates. Harbor: 20 findings, 21 patches, 2 iterations, 11 gates. Same crew, different estate.” “Both are machine-green — `green_with_human_gates`. Structural 100/100, human-gate-adjusted 74 and 71. The gap is the point.” | Stay on `#slide-5`; the cards show both estates. Do not call Harbor a customer reference. |
| **4:50–5:55** | 6 · Code-level refactor | Tab 2: `http://127.0.0.1:8000/codebase?case=cascade-mutual` · click **Patches (22)** · open the first patch · open `http://127.0.0.1:8000/api/codebase/cases/cascade-mutual/sarif` in a tab | “Two examples, both drafts. Left: direct JDBC and concatenated SQL becomes a candidate Gosu Query service. Right: a legacy JMS transport and custom servlet become an App Events publication and Cloud API route shape.” “The class name is corrected to `VehicleRatingQueryService`; the generator’s doubled `QueryService` is an artifact.” “Nothing is compiled. App Events is asynchronous and at-least-once, not a JMS drop-in. SARIF 2.1.0 is advisory.” | If the patch UI is slow, show `#slide-6`; the two before/after pairs and the corrected class name are on the slide. Never imply the draft is deployable. |
| **5:55–6:45** | 7 · Upgrade resilience | Tab 2: `http://127.0.0.1:8000/codebase?case=cascade-mutual` · click **Upgrade resilience** · select the APD naming scenario `GWCP-APD-NAMING-2027.04` | “A green signal is release-bound. The simulated APD scenario moves the type-name limit from 24 to 20 characters. Detection bumps the assessment from generation 1 to 2 and invalidates the stale green.” “Cascade has 30 patch-exposures across 22 patches; Harbor 28 across 21. The rows are not cumulative.” “Revalidate, roll back, or defer. The tool records the choice; a human still decides.” | Stay on `#slide-7`. The timeline, the three resume choices, and the non-cumulative arithmetic are on the slide. |
| **6:45–7:30** | 8 · Evidence & audit | Tab 2: `http://127.0.0.1:8000/packet?run=R-DEMO-001` · scroll to the hash/audit block. Tab 3: run the three `preflight verify-*` commands. | “The evidence card has a path, a locator, an excerpt hash, a method, and a claim-strength label. 101 of 101 links passed the locator-support audit.” “The packet hash binds the rendered packet; content digests bind findings, mappings, and evidence.” “The audit chain has 9 seed events, 11 after two reviewer decisions. The migrator log is a separate 12-event chain.” “Tamper-evident, not non-repudiation.” | Show `#slide-8` and read the commands. If a live command fails, say so: “The local run store does not verify in this session; I will not present it as evidence.” Do not read a stored head as live. |
| **7:30–8:15** | 9 · Demo visualization | `#slide-9` · click **Open full visualization ↗** to `docs/presentation/demo-visual.html` | “Here is the whole story on one map. Top lane: the feature chain — 300 files, 101 evidence, 31 links, 5 packages, 11 gates with 6 high, 7/7 checks, 8 sealed files. Bottom lane: the same five roles in the codebase lab — Scout found 18 Cascade / 20 Harbor; Architect drafted 22 / 21 patches in 2 passes; Guardian ran 13 deterministic machine checks; Critic ran 7 checks with 10/11 human gates open; Planner produced the report and SARIF 2.1.0 with no compile. Zero deployments.” “Agents can read, draft, gate, check, and seal. A human decides.” | **If the companion page is not published with the handout, stay on slide 9.** The full map and all counts are on the slide. |
| **8:15–8:50** | 10 · Engineering rigor | `#slide-10`; optional Tab 3: `python3 -m json.tool docs/presentation/assets/compact/validation.json | head` | “The demo is the surface; the checks are the work. The **current pytest suite** has 520 passing tests at this snapshot. 18/18 freeze hashes recompute. 101/101 evidence links pass. Eight adversarial flaws were found, fixed, and regression-tested.” “No external calls, no telemetry, no live tenant. Live reasoning is gated to synthetic fixtures.” | If the suite count changes, re-run pytest and read the result live; do not guess. |
| **8:50–9:35** | 11 · Reality boundary | `#slide-11` | “Real software. Synthetic estate. Unproven migration.” Name what is real, what is not, and what would make it real: a real read-only snapshot, compile/test, official Cloud Assurance, SME sign-off, production cutover with rollback. “We are at Stage 1 of 5. The next step is Stage 2 — one real snapshot and a blind SME sample, not another synthetic metric.” | If time is short, read only the five proof-ladder labels and the official badge. Do not skip this slide. |
| **9:35–10:00** | 12 · Close | `#slide-12` | “Every claim has evidence. Every unknown has a name. Every change waits for a human.” “The ask: one authorised read-only estate, two blind SME annotators, hard feedback. The next experiment is a real inventory, not another synthetic fixture.” | Stop after the ask and the boundary. Do not add a feature list. |

---

## If you have 60 seconds less

Cut in this order:

1. Slide 4 live app clicks — stay on the slide ledger.
2. Slide 6 patch/SARIF tab — stay on the two before/after examples.
3. Slide 10 audits detail — keep the current-suite count and “no external calls”.
4. Never cut slide 11 or the official-assurance line.

## If a live page fails

- **Migrator down:** stay on slides 3–4. The counts and the Scribe/Planner comparison are in HTML.
- **Codebase lab down:** stay on slides 5–7. The Cascade/Harbor counts and the simulated scenario are in HTML.
- **Packet or verify command fails:** say so plainly and stay on slide 8. Do not substitute a screenshot or a stale hash.
- **Companion visualization unavailable:** stay on slide 9; the full map and all counts are there.
- **Projector is 1024 × 768:** the deck is validated there; use `→` and `n` only.
- **Phone/390:** the deck scrolls vertically, hides the decorative evidence screenshot, and has no horizontal overflow. Use swipe or `→`.

## Reality boundary — say this if challenged

> PreFlight is a synthetic, offline cloud-readiness review and refactor-drafting prototype. The scanner, evidence links, unified diffs, SARIF 2.1.0 exporter, hash chain, and tests are real and executable. The estate, insurer names, code, APD release scenarios, and evaluation slice are synthetic. Nothing was compiled against Guidewire, deployed to a tenant, migrated, or officially assured. **Official Cloud Assurance: not run.**

**Say this, not that**

| Say | Do not say |
|---|---|
| “PreFlight is a synthetic rehearsal of the assessment layer.” | “PreFlight migrates insurers to Guidewire Cloud.” |
| “The review produced 24 candidate findings; the codebase lab drafted 22 patches on Cascade.” | “PreFlight fixed Cascade’s cloud blockers.” |
| “SARIF 2.1.0 is advisory CI input; official Cloud Assurance was not run.” | “PreFlight passed Cloud Assurance.” |
| “The local audit chain verifies the run log.” | “The results are certified or non-repudiable.” |
| “The 2027.04 20-character APD limit is a simulation.” | “Guidewire is tightening the limit in 2027.04.” |
| “Both estates are synthetic archetypes.” | “Cascade and Harbor are customer case studies.” |
| “The green signal is structural, with human gates open.” | “100/100 means the estate is cloud-ready.” |
| “The next step is a real snapshot and blind SME validation.” | “The demo proves the migration works.” |

## Likely questions

**“Is this real?”**  
“The software is real; the estate is synthetic. The honest claim is on slide 11: evidence-linked candidate findings and reviewable drafts on a synthetic estate. No compile, no tenant, no official assurance.”

**“Why 11 gates if you have 5 packages?”**  
“Gates live at the finding and assumption level, not the package level. Three assumption gates plus eight rule groups of three findings each. The package table shows the one package-level gate, G-03.”

**“Why does the fifth agent change?”**  
“Scribe is the feature-packet sealer. Planner is the codebase-patch planner and SARIF assembler. They are alternative fifth steps for two different paths, not the same role.”

**“Did you compile it?”**  
“No. The drafts are syntax-shaped and reviewable, not compiled. Compile and runtime validation are Stage 3 evidence.”

**“How many tests?”**  
“The current pytest suite has 520 passing at this snapshot. I will re-run pytest before quoting any other number.”

**“What would you do with a real estate?”**  
“Stage 2: an authorised read-only snapshot, chain of custody, a blind SME sample with adjudication, and a decision log showing which findings changed a backlog item or assumption. Then one feature slice into a Guidewire developer environment.”
