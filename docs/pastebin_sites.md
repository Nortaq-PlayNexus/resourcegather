# Section A — Paste / Text-Sharing Sites (Tier 1)

Paste sites are the **first stop** for exfiltrated credentials, config files, and
DB dumps — often hours to weeks before they hit commercial breach databases.
MONITOR these, don't just browse.

## Public / general-purpose
| Site | Notes |
|------|-------|
| pastebin.com | The original; high volume, noisy, API + PasteLert alerting |
| gist.github.com | Versioned git snippets; public + secret gists |
| privatebin.info | E2E encrypted, zero-knowledge server — privacy-focused |
| hastebin.com | Lightweight, syntax highlighting, logs/debug |
| rentry.co | Markdown support |
| paste.ee | Advanced sharing, encryption option |
| paste.rs | Minimal anonymous pastes |
| dpaste | Minimal, API-friendly |
| justpaste.it | Formatted text + media |
| slexy.org | Syntax-highlighting paste |
| ghostbin.com | Anonymous paste |
| yopass | One-time secure secret sharing |
| gistpad.com | Modern GitHub-Gist alternative, API + trending |

## Monitoring tools
- **PasteLert** (andrewmohawk.com/pasteLert) — keyword alerting on Pastebin.
- **Custom scrapers** for Gist / PrivateBin / Ghostbin via their APIs.
- **IntelligenceX** (intelx.io) — indexes paste sites + leaks, searchable by email/domain/IP/BTC.
- **OpenOSINT pastebin guide** — collect → pivot → verify → document.

## Extended inventory (pass 2)
| Site | Notes |
|------|-------|
| controlc.com | Rich formatting, custom URLs, 100KB pastes |
| pastes.io | Developer-focused, REST API, encryption, file upload |
| paste.tc | Local-first, offline-capable |
| jsfiddle.net | Code/HTML/CSS/JS snippets (often abused for skimming) |
| paste.centos.org | Community paste |
| termbin.com | CLI-first (`nc termbin.com 9999`), logs/configs |
| slexy.org | Syntax-highlighting paste (already noted) |
| yopass (already noted) | One-time secret |
| PrivateBin on I2P | E2E encrypted paste reachable inside I2P (`privatebin.i2p`) |
| lorien/awesome-pastebins | GitHub meta-list of scrapeable (unencrypted) pastebins |

## Operational notes
- Most require no account → path of least resistance for threat actors.
- Use expiry-aware monitoring: re-pull before links die.
- Source signal: paste creation time vs. ingestion into HIBP/breach DBs = your early-warning window.
