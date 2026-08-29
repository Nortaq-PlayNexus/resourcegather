# Section C — The Inbetween (Tier 3)

Forums, ransomware leak sites, dark-web search engines, aggregators, and file
hosts. This is where signal consolidates and where attribution actually happens.
Many entries are CRIMINAL INFRASTRUCTURE — documented for *monitoring*, not participation.

## 1. Ransomware leak sites (double-extortion "walls of shame")
Tor-hosted, operated by ransomware groups. Richest OSINT feed in cybercrime.
- Active groups (2025–2026): Akira, Play, RansomHub, BlackBasta, Cl0p, Medusa, Lynx, and smaller operators. List shifts constantly.
- **Monitoring projects:** Ransomwatch (ransomwatch.telemetry.ltd + github.com/joshhighet/ransomwatch), RansomLook, DarkFeed.io.
- **Workflow:** scheduled Tor snapshots → log entry changes (removal = possible payment; sample additions = escalation; full dump = worst case) → timestamp every transition.

## 2. Cybercrime forums / marketplaces (awareness + monitoring)
English-language lineage: RaidForums (seized 2022) → BreachForums (multi takedown, DB leaked Jan 2026, ~324k users) → LeakBase (seized Mar 2026).
Current / notable:
- **Exploit** — oldest Russian-language forum (since 2005); data, initial access, MaaS.
- **XSS** — credential/phishing/malware; admin arrested; suspected honeypot risk.
- **DarkForums** — absorbed BreachForums userbase post-Apr 2025.
- **DamageLib** — Tor-only spin-off from XSS, no marketplace.
- **RAMP** — ransomware-friendly Russian forum.
- **Duty Free** — XSS-structured, openly RaaS-friendly.
- **WWH-Club** — carding / financial fraud (mods arrested 2024).
- **HydraForums, Cracking[.]org, DarkNet Army, Altenen, BHF** — creds, combolists, tutorials.
- **Dread** — Reddit-like Tor community hub (often where markets/forums are discussed).
- **Telegram / Discord** channels — increasingly primary distribution; monitor via bots.

## 3. Dark-web / onion search engines
| Engine | Type | Filtering |
|--------|------|-----------|
| Ahmia (ahmia.fi) | Tor crawler | Abuse-filtered (CSAM/terror blocked), safe starting point |
| Torch | Tor crawler | Minimal / none |
| Haystack (Haystak) | Tor crawler | Abuse-only, 1.5B+ pages |
| Not Evil | Tor crawler | Partial / community-moderated |
| Recon | Market-specific search | Vendor/listing search |
| Tor66 / OnionLand / TorDex | Search + directory | Minimal |

Clearnet-on-Tor: **DuckDuckGo .onion** for anonymous surface-web search.
Use **directories** (OnionDir, TorWiki, torGate-legal) for verified .onion links.

## 4. Aggregators / meta-indexes (highest leverage)
- **IntelligenceX** — paste sites, leaks, dark web; search by email/domain/IP/BTC.
- **SOCRadar Threat Hunting** (free tier) — 50+ sources incl. paste, dark web, code repos.
- **Library of Leaks** — meta-index pointing to known leak references (no hosting).
- **Have I Been Pwned** — confirmation source for exposed credentials.
- **Flare / Bitsight / DeXpose / Recorded Future / Mandiant** — commercial continuous monitoring (for orgs).

## 5. File hosts / document leakers (the "inbetween" file layer)
- **Dropbox Transfer / Google Drive / Mega / WeTransfer** — frequently used to ship large leaked archives via share links (often misconfigured / public).
- **SecureDrop** — journalist/whistleblower submissions (legitimate).
- **WikiLeaks / Sony Archives (.onion)** — historical leak archives.
- OSINT tip: search `site:docs.google.com` / `site:dropbox.com` dorks for exposed shared documents.

## 6. Extended — stealer-log economy (pass 2)
After the May 2025 LummaC2 takedown, trade re-consolidated around:
- **Russian Market** — dominant stealer-log storefront (180k+ logs H1 2025).
- **2Easy Shop, Genesis Market (seized), Exodus** — historical marketplaces.
- **Telegram "log clouds"** — Moon Cloud, Daisy Cloud, Observer Cloud, ALIEN TXTBASE (284M accounts added to HIBP), Hawklog (breached by rival Mooncloud, 1.7GB leak).
- Stealers: RedLine, Vidar, RisePro, Stealc, LummaC2, Banshee (macOS), Acreed (2025).
- Channels move fast: logs appear <48h post-infection; priced ~$1–$100, RDP/initial access $500–$2,700.
- **Monitoring angle (defensive):** tgstat.com, telegramchannels.me, Telemetr.io for channel discovery; OSINTLeak / OSINT Industries / commercial TI for aggregated log search. Never buy/access criminal sources directly — use reputable intermediaries (per OSINT Combine guidance).

## 7. Extended — Telegram / Discord OSINT (pass 2)
- **Discovery:** TGStat, Telemetr.io, t.me/s/<channel> previews, telegramchannels.me, Telegram Directory (tdirectory.me).
- **Tooling:** Awesome-Telegram-OSINT, The-Osint-Toolbox/Telegram-OSINT, TelegramOSINT (Telethon scrapers), TG Collector, Bellingcat phone-number checker, Geogramint.
- **Discord:** bot-based monitoring only (ToS restricts scraping); DSH / Discord Server Hunter.
- **X/Twitter:** API now ~$5k/mo; unofficial scrapers (Nitter/snscrape) unreliable. Mastodon/ActivityPub federation increasingly targeted.

## 8. Extended — I2P eepsite discovery (pass 2)
I2P (Invisible Internet Project) is a separate darknet (`.i2p` / `.b32.i2p`), strong for P2P.
- **Search:** Legwork (eepsites-only), I2PSearch, Bandura, duckduckgo.i2p, ahmia.i2p, torch.i2p, raklet.i2p.
- **Directories:** reg.i2p (curated, 4h refresh), identiguy.i2p (live/uncurated), Notbob, hopjoy.i2p, stats.i2p/newhosts.txt.
- **Registries:** inr.i2p, dns.chudo.i2p, isitup.i2p.
- **Services:** Susimail/Postman (email), PrivateBin.i2p (encrypted paste), Chudo's Torrents, Teddit.i2p, Ramble.i2p, Syndie (distributed forums).
- Note: I2P suffered a volumetric attack Feb 2026 (tunnel-build degradation) — factor into uptime monitoring.

## 9. Extended — breach/leak aggregators & frameworks (pass 2)
- **Breach search:** DeHashed, Snusbase, LeakCheck, IntelX (already), OSINTLeak, Library of Leaks (already).
- **Commercial TI:** Recorded Future, Flashpoint, KELA, Cybrvault, NexusXplore (OSINT Combine), VanishID, SpyCloud, SOCRadar (already).
- **Doxbin** — doxxing site; its DB leaked Mar 2026 ("Spring Cleaning" wave after LeakBase takedown). Tier-1 harassment risk.
- **OSINT frameworks:** Maltego, SpiderFoot, Recon-ng (already); plus **VoidAccess** (self-hosted dark-web TI, Docker, STIX/MISP/Sigma export), **focal-harvest** (multi-engine research + Telegram/Discord alerts), **Kodjocares/osint**, **OpenOSINT**.
- **Dork collections:** cipher387/Dorks-collections-list (Google/Bing/Shodan/Censys/Yandex/Onion/GitHub dorks), Awesome-Yandex-Dorks, pagodo/go-dork/Katana for automation.
- **Infra pivots:** Shodan, Censys, SecurityTrails, crt.sh, VirusTotal, Netlas; reverse-image: Yandex, PimEyes, FaceCheck.ID, TinEye, InVID.

## 10. Framework & tooling stack (consolidated)
- **SpiderFoot / Maltego / Recon-ng** — graph-based collection.
- **Modular OSINT frameworks** (e.g. Kodjocares/osint) — paste-monitor, breach-check, threat-IOC, GitHub-recon modules.
- **Google/DuckDuckGo dorks** — `filetype:`, `intitle:`, `inurl:`, `site:`.
- **Wayback Machine** — historical capture when sources go dark.
- **StatusCake / UptimeRobot** — monitor liveness of target onion/index.
