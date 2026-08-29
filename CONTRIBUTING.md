# Contributing

Contributions are welcome. This project follows the standards used across the
maintainer's other repositories (see `aether-facility`, `hexstrike-ai`).

## Development setup

```bash
pip install -r requirements.txt
python main.py --selftest      # config + data + generated functions
python main.py --gui           # optional Tkinter UI
```

## Project layout

- `core/` — the engine (config, ethics, opsec, parsers, storage, analytics,
  scheduler, sources, search, report, tor_client).
- `data/` — machine-readable inventories that *drive code generation*. Editing
  these changes behaviour without touching `core`.
- `config/settings.json` — scope, keywords, proxy, alert, auto-search.
- `tools/` — data-acquisition / maintenance scripts (expand sources, probe,
  dedupe, prune dead).

## Adding data

- **A site:** add an entry to the relevant `data/*.json`. No code change needed.
- **Behaviour:** edit a maker in `core/sources.py`; it propagates to every
  source automatically.
- **Search endpoints:** edit `data/search_targets.json` (overridable at runtime
  via `output/config/search_targets.json` — no rebuild).

## Quality gates

- `python main.py --selftest` must pass.
- `python main.py --count` must report `>=500` (currently 37,000+ functions are
  materialized at runtime).
- Run `ruff` if available; keep imports clean and avoid committing secrets.

## Pull requests

1. Fork and branch from `main`.
2. Keep PRs focused; describe the *why*.
3. Ensure the self-test passes in CI.
4. By contributing you agree your contributions are licensed under the MIT
   License.
