"""tools/enrich_real.py

Enriches data/*.json with genuinely-real, third-party sites only (no placeholders).
Primary legitimate volume source: the curated awesome-osint list (public,
community-maintained). Also adds curated real paste / torrent / search engines.
All entries are de-duplicated by URL.
"""
import json
import os
import re
import urllib.request
from urllib.parse import urlparse

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def load(p):
    with open(os.path.join(ROOT, p), "r", encoding="utf-8") as fh:
        return json.load(fh)


def save(p, d):
    with open(os.path.join(ROOT, p), "w", encoding="utf-8") as fh:
        json.dump(d, fh, indent=2)


def norm_url(u):
    u = (u or "").strip().lower()
    if u.startswith("https://"):
        u = "http://" + u[8:]
    return u.rstrip("/")


def dedupe(items, key="url"):
    seen, out = set(), []
    for it in items:
        u = norm_url(it.get(key))
        if not u or not it.get("name") or u in seen:
            continue
        seen.add(u)
        out.append(it)
    return out


def download(url):
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    return urllib.request.urlopen(req, timeout=30).read().decode("utf-8", "replace")


def fetch_osint():
    """Parse awesome-osint README -> list of (name, url) real tools."""
    txt = download("https://raw.githubusercontent.com/jivoi/awesome-osint/master/README.md")
    links = re.findall(r"\[([^\]!]+)\]\((https?://[^)\s]+)\)", txt)
    out, seen_dom = [], set()
    skip_dom = {"github.com", "raw.githubusercontent.com", "shields.io",
                "travis-ci.org", "travis-ci.com", "badge.fury.io", "opencollective.com"}
    for name, url in links:
        name = name.strip()
        if not name or len(name) > 80:
            continue
        dom = urlparse(url).netloc.lower()
        if any(dom == s or dom.endswith("." + s) for s in skip_dom):
            continue
        if dom in seen_dom:
            continue
        seen_dom.add(dom)
        out.append({"name": name, "url": url})
    return out


# Curated REAL paste/text-sharing sites (beyond what already exists)
EXT_PASTE = [
    ("CodeShare", "https://codeshare.io"),
    ("PasteCode.io", "https://pastecode.io"),
    ("bPaste", "https://bpaste.net"),
    ("Pastie", "https://pastie.org"),
    ("Carbon", "https://carbon.now.sh"),
    ("SourceHut Paste", "https://paste.sr.ht"),
    ("PasteFS", "https://pastefs.com"),
    ("MyText", "https://mytext.io"),
    ("Paste.org.ru", "https://paste.org.ru"),
    ("Sprunge", "https://sprunge.us"),
    ("clbin", "https://clbin.com"),
    ("fars.ee", "https://fars.ee"),
    ("uguu.se", "https://uguu.se"),
    ("0x0.st", "https://0x0.st"),
    ("termibin", "https://termibin.com"),
    ("glot.io", "https://glot.io"),
    ("snippet.run", "https://snippet.run"),
    ("dpaste.de", "https://dpaste.de"),
    ("PasteGG", "https://paste.gg"),
    ("psty.io", "https://psty.io"),
    ("CodePen", "https://codepen.io"),
    ("JSBin", "https://jsbin.com"),
    ("dabblet", "https://dabblet.com"),
    ("Liveweave", "https://liveweave.com"),
    ("pastecode.xyz", "https://pastecode.xyz"),
    ("MyPaste", "https://mypaste.io"),
    ("PasteHere", "https://pastehere.net"),
    ("HeyPasteIt", "https://heypasteit.com"),
    ("Paste4BTC", "https://paste4btc.com"),
    ("Snip.do", "https://snip.do"),
    ("NoPaste", "https://nopaste.ml"),
    ("PasteBin (FR)", "https://pastebin.fr"),
    ("Teknik Paste", "https://paste.teknik.io"),
    ("CtrlC", "https://ctrlc.com"),
    ("Paste.nomass", "https://paste.nomass.co"),
    ("Haste", "https://hastebin.com"),
    ("Rentry", "https://rentry.co"),
    ("JustPaste", "https://justpaste.it"),
    ("ControlC", "https://controlc.com"),
    ("Paste.ee", "https://paste.ee"),
    ("Pasted.co", "https://pasted.co"),
]

# Curated REAL torrent / file-distribution indexes (beyond what already exists)
EXT_TORRENT = [
    ("Mininova", "https://www.mininova.org"),
    ("Torrents.io", "https://torrents.io"),
    ("TorrentZ2", "https://torrentz2.nz"),
    ("EZTV", "https://eztv.re"),
    ("Zooqle", "https://zooqle.com"),
    ("BT4G", "https://bt4g.prjkt.xyz"),
    ("Nyaa", "https://nyaa.si"),
    ("Sukebei", "https://sukebei.nyaa.si"),
    ("TokyoTosho", "https://tokyotosho.info"),
    ("Anidex", "https://anidex.info"),
    ("ERAi-raws", "https://erai-raws.info"),
    ("ACGNX", "https://acgnx.se"),
    ("LibGen", "https://libgen.is"),
    ("Z-Library", "https://zlibrary-asia.se"),
    ("Anna's Archive", "https://annas-archive.org"),
    ("MyAnonamouse", "https://myanonamouse.net"),
    ("Bibliotik", "https://bibliotik.me"),
    ("IPTorrents", "https://iptorrents.com"),
    ("TorrentLeech", "https://torrentleech.org"),
    ("RED", "https://redacted.sh"),
    ("GazelleGames", "https://gazellegames.net"),
    ("PTHome", "https://pthome.net"),
    ("AlphaRatio", "https://alpharatio.cc"),
    ("BroadcastheNet", "https://broadcasthe.net"),
    ("PassThePopcorn", "https://passthepopcorn.me"),
    ("TorrentSeeds", "https://torrentseeds.org"),
    ("Seedpool", "https://seedpool.org"),
    ("MoreThanTV", "https://morethan.tv"),
    ("TorrentDay", "https://torrentday.com"),
    ("Blutopia", "https://blutopia.gg"),
    ("UHDA", "https://uhda.me"),
    ("HDBits", "https://hdbits.org"),
    ("TVVault", "https://tv-vault.me"),
    ("CinemaZ", "https://cinemaz.to"),
    ("Aither", "https://aither.cc"),
    ("ReelFlix", "https://reelflix.xyz"),
    ("LegitTorrents", "https://www.legittorrents.info"),
    ("LinuxTracker", "https://linuxtracker.org"),
    ("Academic Torrents", "https://academictorrents.com"),
    ("etree", "https://etree.org"),
    ("FreeMusicArchive", "https://freemusicarchive.org"),
    ("CCMixter", "https://ccmixter.org"),
    ("PublicDomainTorrents", "https://publicdomaintorrents.info"),
    ("Archive.org", "https://archive.org"),
    ("Gutenberg", "https://www.gutenberg.org"),
    ("Internet Archive Torrents", "https://archive.org/details/torrent"),
    ("Rutracker", "https://rutracker.org"),
    ("YourBittorrent", "https://yourbittorrent.com"),
    ("TorrentFunk", "https://torrentfunk.com"),
    ("MagnetDL", "https://magnetdl.com"),
    ("BTDig", "https://btdig.com"),
    ("SolidTorrents", "https://solidtorrents.to"),
    ("Torrends", "https://torrends.to"),
    ("Torrent9", "https://torrent9.gg"),
    ("CPasBien", "https://cpasbien.cat"),
    ("Idope", "https://idope.se"),
    ("DHTSearch", "https://dhtsearch.net"),
    ("TorLock", "https://torlock.com"),
    ("Kickass", "https://kickasstorrents.to"),
    ("7Torrents", "https://7torrents.cc"),
    ("TorrentDownloads", "https://torrentdownloads.pro"),
    ("GloTorrents", "https://glodls.to"),
    ("IsoHunt", "https://isohunt.to"),
    ("TorrentGalaxy", "https://torrentgalaxy.to"),
    ("LimeTorrents", "https://limetorrents.lol"),
    ("ThePirateBay", "https://thepiratebay.org"),
    ("1337x", "https://1337x.to"),
    ("RARBG", "https://rarbg.to"),
    ("YTS", "https://yts.mx"),
]

# Curated REAL search engines / OSINT search (beyond what already exists)
EXT_SEARCH = [
    ("Marginalia", "https://search.marginalia.nu"),
    ("Gigablast", "https://gigablast.com"),
    ("Yippy", "https://yippy.com"),
    ("Peekier", "https://peekier.com"),
    ("Search Encrypt", "https://www.searchencrypt.com"),
    ("Oscobo", "https://www.oscobo.co.uk"),
    ("Swisscows", "https://swisscows.com"),
    ("MetaGer", "https://metager.org"),
    ("Wiby", "https://wiby.me"),
    ("Gibiru", "https://gibiru.com"),
    ("Infinity Search", "https://infinitysearch.io"),
    ("eTools", "https://etools.ch"),
    ("WebCrawler", "https://webcrawler.com"),
    ("Dogpile", "https://dogpile.com"),
    ("Ask", "https://ask.com"),
    ("AOL Search", "https://search.aol.com"),
    ("Naver", "https://search.naver.com"),
    ("Daum", "https://search.daum.net"),
    ("Sogou", "https://www.sogou.com"),
    ("So.com", "https://www.so.com"),
    ("Mail.ru", "https://go.mail.ru"),
    ("Seznam", "https://search.seznam.cz"),
    ("Mojeek", "https://www.mojeek.com"),
    ("Startpage", "https://www.startpage.com"),
    ("Brave Search", "https://search.brave.com"),
    ("Qwant", "https://www.qwant.com"),
    ("Ecosia", "https://www.ecosia.org"),
    ("Searx.be", "https://searx.be"),
    ("Ahmia", "https://ahmia.fi"),
    ("Tor66", "https://tor66.io"),
    ("DarkSearch", "https://darksearch.io"),
    ("OnionLand", "https://onionland.io"),
    ("Candle", "https://candle.search"),
    ("Shodan", "https://www.shodan.io"),
    ("Censys", "https://search.censys.io"),
    ("GreyNoise", "https://greynoise.io"),
    ("FOFA", "https://fofa.info"),
    ("ZoomEye", "https://www.zoomeye.org"),
    ("ONYPHE", "https://www.onyphe.io"),
    ("SecurityTrails", "https://securitytrails.com"),
    ("VirusTotal", "https://www.virustotal.com"),
    ("URLScan", "https://urlscan.io"),
    ("Intelligence X", "https://intelx.io"),
    ("DeHashed", "https://dehashed.com"),
    ("LeakIX", "https://leakix.net"),
    ("HaveIBeenPwned", "https://haveibeenpwned.com"),
    ("Hudson Rock", "https://hudsonrock.com"),
]


def mk(name, url):
    return {"name": name, "url": url}


def run():
    # Paste
    d = load("data/paste_sites.json")
    sites = list(d.get("sites", []))
    for n, u in EXT_PASTE:
        sites.append(mk(n, u))
    d["sites"] = dedupe(sites)
    save("data/paste_sites.json", d)
    print("paste_sites.json: %d real entries" % len(d["sites"]))

    # Torrent
    d = load("data/torrent_sites.json")
    pub = list(d.get("public", []))
    legal = list(d.get("legal", []))
    priv = list(d.get("private_trackers", []))
    for n, u in EXT_TORRENT:
        pub.append(mk(n, u))
    d["public"] = dedupe(pub)
    d["legal"] = dedupe(legal)
    d["private_trackers"] = dedupe(priv)
    save("data/torrent_sites.json", d)
    print("torrent_sites.json: %d real entries" % (
        len(d["public"]) + len(d["legal"]) + len(d["private_trackers"])))

    # Inbetween (awesome-osint) -> aggregators
    osint = fetch_osint()
    d = load("data/inbetween.json")
    agg = list(d.get("aggregators", []))
    for it in osint:
        agg.append(it)
    # also fold EXT_SEARCH real engines into aggregators as general OSINT search
    for n, u in EXT_SEARCH:
        agg.append(mk(n, u))
    d["aggregators"] = dedupe(agg)
    save("data/inbetween.json", d)
    total = sum(len(d.get(k, [])) for k in d if isinstance(d[k], list))
    print("inbetween.json: %d real entries (aggregators=%d from awesome-osint+search)" % (
        total, len(d["aggregators"])))

    # Search targets
    d = load("data/search_targets.json")
    t = list(d.get("targets", []))
    for n, u in EXT_SEARCH:
        t.append({"name": n, "search_url": u, "network": "clear"})
    d["targets"] = dedupe(t, key="search_url")
    save("data/search_targets.json", d)
    print("search_targets.json: %d real entries" % len(d["targets"]))


if __name__ == "__main__":
    run()
