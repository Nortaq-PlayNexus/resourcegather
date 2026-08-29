# Changelog

All notable changes to this project are documented here. The format is based on
[Keep a Changelog](https://keepachangelog.com/), and this project adheres to
[Semantic Versioning](https://semver.org/).

## [1.0.0] - 2026-08-29

### Added
- Defense-grade OSINT resource-gathering framework (`Resource Gather`).
- Four tiered inventories in `data/`:
  - **Tier 1 — paste sites** (`paste_sites.json`): 900+ verified public paste
    services.
  - **Tier 2 — torrent / file distribution** (`torrent_sites.json`): 860+
    public / legal / private trackers + indexes.
  - **Tier 3 — the inbetween** (`inbetween.json`): 2,980+ forums, ransomware
    leak sites, dark-web + I2P search, stealer-log markets, and aggregators.
  - **Custom search** (`search_targets.json`): 650+ search endpoints
    (clear / Tor / I2P).
- `core/` engine: config loader, ethics + PII redaction, OPSEC, validators,
  parsers, storage (chain-of-custody; CSV/JSON/STIX/MISP export), analytics,
  scheduler, Tor client, code generator (`core.sources`), search, and report.
- Materializes **37,000+** callable functions from the inventories
  (`monitor_/search_/snapshot_/validate_/extract_<source>`).
- CLI: `--search`, `--loop`, `--selftest`, `--count`, `--report`, `--gui`
  (Tkinter) and a `build.spec` producing `ResourceGather.exe`.
- Maintenance tooling in `tools/`: source expansion, reachability probing,
  cross-type de-duplication, and dead-site pruning.
- Standard repo scaffolding: `SECURITY.md`, `CODE_OF_CONDUCT.md`,
  `CONTRIBUTING.md`, `CHANGELOG.md`, `.github/` (issue templates + CI),
  `docs/` (building guide + screenshots), and `tests/`.

### Ethics
- Strictly defensive scope enforced in `core.ethics`; PII redaction on export;
  criminal infrastructure included for *monitoring only*.
