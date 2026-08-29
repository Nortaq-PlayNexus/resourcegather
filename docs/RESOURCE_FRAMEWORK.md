# Investigational Resource-Gathering Framework

**Purpose:** A repeatable OSINT / threat-intel collection setup for mapping and
monitoring public sharing infrastructure — paste sites, torrent indexes, and the
"inbetween" (forums, leak sites, dark-web search engines, file hosts, aggregators).

**Scope & ethics (read first):**
This framework is built for *defensive* research: breach exposure monitoring,
threat-actor attribution, academic study, and early-warning alerting. It does
NOT endorse copyright infringement, unauthorized access, buying/selling stolen
data, or any illegal activity. Several sources below are criminal infrastructure
and are documented only so defenders know what to *monitor*, not how to
*participate*. Law-enforcement infiltration of these spaces is routine — treat
every interaction as potentially attributable.

---

## 0. Operational baseline (OPSEC) — do this before anything else
- Run collection from an isolated VM or dedicated profile. Never from your daily-use environment.
- Route through Tor + VPN. Verify no DNS/WebRTC leaks.
- Use script/ad blockers. Torrent index sites are heavy with malvertising and fake download buttons.
- Never log into personal accounts while researching. Assume query logging everywhere.
- Document everything with timestamps: source URL, capture time, screenshot hash, content summary. This is your chain of custody.

## 1. Collection workflow (the loop)
```
Identify target/keyword
   -> Discover sources (search engines, directories, aggregators)
   -> Collect (crawl / API / snapshot)
   -> Verify (cross-source, reputation, hashes)
   -> Enrich (pivot: domain, email, IP, handle, crypto address)
   -> Document + alert (store, flag matches)
   -> Monitor on schedule (re-snapshot for changes)
```

## 2. Source tiers
- **Tier 1 — Clear-web paste sites** (Section A): earliest landing spot for leaked data.
- **Tier 2 — Torrent / file-distribution indexes** (Section B): bulk distribution.
- **Tier 3 — The inbetween** (Section C): forums, leak sites, dark-web search, aggregators, file hosts.

## 3. Tooling to stand up
- **Paste monitoring:** PasteLert (keyword alerts on Pastebin), custom scraper for Gist/PrivateBin/Ghostbin.
- **Aggregators:** Ransomwatch (github.com/joshhighet/ransomwatch), IntelligenceX, SOCRadar Threat Hunting (free tier), Library of Leaks.
- **Tor access:** Tor Browser + scripted SOCKS proxy for scheduled onion scraping.
- **Frameworks:** Maltego / SpiderFoot / Recon-ng; modular OSINT frameworks (e.g. Kodjocares/osint) for paste-site + breach modules.
- **Tracking lists:** ngosang/trackerslist (public BitTorrent trackers) for magnet resolution.
- **Archiving:** Wayback Machine + local snapshot with hash.

## 4. Verification rules
- Never trust a single source. Cross-reference (Ransomwatch + RansomLook + forum chatter).
- Validate checksums/hashes before treating any file as real.
- Some leak sites are law-enforcement honeypots (Hive, LockBit precedent). Assume that.
- Operators inflate victim counts and recycle listings. Verify claims.

## 5. Output format (per finding)
```
TIMESTAMP | SOURCE (url/onion) | CATEGORY | ENTITY MATCHED | SUMMARY | CONFIDENCE | EVIDENCE HASH
```

See the three companion files for the categorized source inventories:
- `pastebin_sites.md`
- `torrent_sites.md`
- `the_inbetween.md`
