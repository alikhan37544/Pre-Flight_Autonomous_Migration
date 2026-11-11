# PreFlight — repository status

**Repository:** <https://github.com/alikhan37544/Pre-Flight_Autonomous_Migration>
**Default branch:** `main`
**Status:** standalone repository (the former upstream is no longer available).

The former cross-repository pull request workflow is retired. All work is committed and
pushed directly to the standalone repository above. The two local archive files
(`*.zip`) are intentionally ignored and are not part of the repository.

## Branches

| Branch | Purpose |
|---|---|
| `main` | Complete five-agent demo, codebase lab, 23-slide reference deck, and 10-minute compact deck. |

## Verify locally

```bash
make test
make e2e
make claims
.venv/bin/python -m app.cli verify-audit R-DEMO-001
.venv/bin/python -m app.cli verify-migration R-DEMO-001
```

The product, fixtures, decks, and audit evidence are synthetic. PreFlight is not an
actual migration, not an official Cloud Assurance result, and every generated change
remains pending human approval.
