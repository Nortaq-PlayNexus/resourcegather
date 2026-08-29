# Section B — Torrent & File-Distribution Indexes (Tier 2)

Bulk-distribution layer. Public indexes are ad-/malware-heavy — treat as hostile
web pages even when only browsing. LEGAL alternatives listed first.

## Legal / safe-first sources
| Site | Notes |
|------|-------|
| archive.org (Internet Archive) | Public-domain media, software preservation, research data |
| gutenberg.org | Public-domain ebooks |
| academic.torrents.me | Datasets / research materials |
| publicdomaintorrents | Pre-1928 films |
| Creative Commons ecosystems | License-clear creator releases |

## Major public torrent indexes (monitoring/inventory only)
| Site | Focus |
|------|-------|
| The Pirate Bay | Resilient, magnet-only, mirrors |
| 1337x | Structured, moderated categories |
| YTS | Movies (compressed) |
| TorrentGalaxy | General, troubled but active |
| LimeTorrents | General |
| EZTV | TV / complete seasons |
| Nyaa | Anime / East-Asian media |
| Torlock | "Verified-only" claims (aggressive ads) |
| iDope | Magnet-focused, clean UI |
| FitGirl Repacks | Trusted PC-game repacker (official: fitgirl-repacks.site ONLY) |
| IGG-GAMES | Gaming-focused |
| Demonoid | Semi-private, niche/older |
| Kickass (KAT mirrors) | Variable legitimacy |

## Private trackers (higher quality, invite-only — listed for awareness)
BTN (Broadcasthe.net), PassThePopcorn, RED (Redacted), IPTorrents, TorrentLeech.
Note: private ≠ legal. Account bans/data leaks occur.

## Infrastructure references
- **ngosang/trackerslist** (GitHub) — curated public BitTorrent tracker list (UDP/HTTP/I2P/WS).
  Use for magnet resolution in automated collection.

## Extended inventory — private trackers (pass 2)
Source: r/Piracy private-trackers wiki, hdvinnie/Private-Trackers-Spreadsheet, bttrackers.com.
High-tier (stringent join rules): **BTN** (BroadcastheNet, TV), **PTP** (PassThePopcorn, movies), **HDBits** (HDB, general/scene), **RED** (Redacted, music).
Mid/specialized: **GGn** (GazelleGames), **MAM** (MyAnonaMouse, books/audio), **SecretCinema**, **SceneHD**, **PrivateHD**, **Retroflix**, **RevolutionTT**, **SeedPool**, **BTSCHOOL** (Chinese), **Nebulance**, **C411** (French), **PolishTracker**, **PixelCove** (games), **BrokenStones**, **Phoenix Project**.
Pay/invite markets (awareness only): IPTorrents ($20), HD-Torrents (€40); invite brokering via InviteScene (note: account-trading ecosystems exist — relevant to monitoring, not participation).
Tracker recruitment chain: MAM/RED → PTP/BTN/HDB invites (networking model).

## Public tracker list feeds (automation)
- **ngosang/trackerslist** — already noted.
- **shadowcovering/BitTorrentTrackersList** — auto-updated every 10 min.
- **lucky95270/BitTorrent-trackerslist** — daily-updated.

## Safety non-negotiables
- VPN + hardened browser + script blocker before opening any index.
- Inspect torrent files / trackers before opening. Avoid freshly uploaded executables.
- Magnet links reduce (not eliminate) exposure. Verify release groups.
- Bookmark known-good domains; ignore email invites and clone sites.
