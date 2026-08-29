"""tools/expand_more.py

Adds 500+ real, third-party sites to EACH type (paste/torrent/inbetween/search)
from legitimate curated lists, while keeping a persistent search-history log
(data/_history.json) so the same source/URL is never re-added (no backtracking).

Run repeatedly; only new sources/URLs are processed.
"""
import json
import os
import re
import urllib.request
from urllib.parse import urlparse

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
HIST = os.path.join(ROOT, "data", "_history.json")

SKIP_DOM = {"github.com", "raw.githubusercontent.com", "twitter.com",
            "reddit.com", "facebook.com", "wikipedia.org", "wikimedia.org",
            "shields.io", "travis-ci.org", "travis-ci.com", "youtube.com",
            "linkedin.com", "instagram.com", "medium.com", "t.me",
            "sourceforge.net", "paypal.com", "amazon.com", "google.com"}


def load_hist():
    if os.path.exists(HIST):
        with open(HIST, "r", encoding="utf-8") as fh:
            return json.load(fh)
    return {"sources": [], "added": {"paste": [], "torrent": [], "search": [], "inbetween": []}}


def save_hist(h):
    os.makedirs(os.path.dirname(HIST), exist_ok=True)
    with open(HIST, "w", encoding="utf-8") as fh:
        json.dump(h, fh, indent=2)


def norm(u):
    u = (u or "").strip().lower()
    if u.startswith("https://"):
        u = "http://" + u[8:]
    return u.rstrip("/")


def download(url):
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    return urllib.request.urlopen(req, timeout=40).read().decode("utf-8", "replace")


def extract_md(txt):
    out = []
    for name, url in re.findall(r"\[([^\]!]+)\]\((https?://[^)\s]+)\)", txt):
        out.append((name.strip(), url.strip()))
    # also udp trackers (for torrent lists)
    for url in re.findall(r"(udp://[^\s)\"']+)", txt):
        out.append(("tracker", url.strip()))
    # plain-text URLs (many curated lists use bare URLs, not markdown)
    seen = {u for _, u in out}
    for url in re.findall(r"https?://[^\s)\"'\s<>]+", txt):
        if url not in seen:
            out.append(("", url.strip()))
            seen.add(url)
    return out


def extract_wiki(html):
    out = []
    for url, name in re.findall(r'<a href="(https?://[^"]+)"[^>]*>([^<]+)</a>', html):
        out.append((name.strip(), url.strip()))
    seen = {u for _, u in out}
    for url in re.findall(r"https?://[^\s)\"'\s<>]+", html):
        if url not in seen:
            out.append(("", url.strip()))
            seen.add(url)
    return out


def extract_json(obj):
    out = []
    if isinstance(obj, dict):
        if isinstance(obj.get("url"), str) and obj["url"].startswith("http"):
            out.append((obj.get("name", obj["url"]), obj["url"]))
        for v in obj.values():
            out += extract_json(v)
    elif isinstance(obj, list):
        for v in obj:
            out += extract_json(v)
    return out


BAD_EXT = (".svg", ".txt", ".png", ".jpg", ".jpeg", ".gif", ".css", ".js",
           ".ico", ".json", ".md", ".pdf", ".zip", ".exe")
JUNK_HOST = ("jsdelivr.net", "ko-fi.com", "cdn.jsdelivr.net", "gstatic.com",
             "googleapis.com", "w3.org", "schema.org")


def legit(url):
    u = (url or "").lower()
    try:
        dom = urlparse(u).netloc
    except ValueError:
        return False
    if any(dom == s or dom.endswith("." + s) for s in SKIP_DOM):
        return False
    if any(dom == s or dom.endswith("." + s) for s in JUNK_HOST):
        return False
    if any(u.endswith(e) for e in BAD_EXT):
        return False
    return True


def load_file(cat):
    p = os.path.join(ROOT, "data",
                     {"paste": "paste_sites.json", "torrent": "torrent_sites.json",
                      "inbetween": "inbetween.json", "search": "search_targets.json"}[cat])
    with open(p, "r", encoding="utf-8") as fh:
        return json.load(fh), p


def existing_urls(cat, d):
    if cat == "paste":
        return {norm(s.get("url", "")) for s in d["sites"]}
    if cat == "torrent":
        return {norm(s.get("url", "")) for k in ("public", "legal", "private_trackers") for s in d.get(k, [])}
    if cat == "inbetween":
        return {norm(s.get("url", "")) for k in d if isinstance(d[k], list) for s in d[k]}
    if cat == "search":
        return {norm(t.get("search_url", "")) for t in d["targets"]}
    return set()


def append_entry(cat, d, name, url):
    if cat == "paste":
        d["sites"].append({"name": name, "url": url})
    elif cat == "torrent":
        d["public"].append({"name": name, "url": url})
    elif cat == "inbetween":
        d["aggregators"].append({"name": name, "url": url})
    elif cat == "search":
        d["targets"].append({"name": name, "search_url": url, "network": "clear"})


SOURCES = [
    ("paste", "https://raw.githubusercontent.com/lorien/awesome-pastebins/master/README.md", "md"),
    ("paste", "https://raw.githubusercontent.com/psapy/awesome-pastebin/master/README.md", "md"),
    ("paste", "https://pasterbox.net/blog/best-pastebin-sites-2026/", "md"),
    ("paste", "https://pastes.io/pages/pastebin-sites", "md"),
    ("paste", "https://s.ee/blog/best-pastebin-alternatives/", "md"),
    ("paste", "https://gistpad.com/pages/top-pastebin-alternatives-in-2026", "md"),
    ("torrent", "https://raw.githubusercontent.com/ngosang/trackerslist/master/README.md", "md"),
    ("torrent", "https://www.rapidseedbox.com/blog/safe-torrent-sites", "md"),
    ("torrent", "https://www.justdailytrackers.com/guides/best-torrent-trackers-2026", "md"),
    ("torrent", "https://www.startupopinions.com/torrent-tracker/", "md"),
    ("inbetween", "https://raw.githubusercontent.com/hslatman/awesome-threat-intelligence/master/README.md", "md"),
    ("inbetween", "https://raw.githubusercontent.com/rshipp/awesome-malware-analysis/master/README.md", "md"),
    ("inbetween", "https://raw.githubusercontent.com/meirwah/awesome-incident-response/master/README.md", "md"),
    ("inbetween", "https://raw.githubusercontent.com/InQuest/awesome-yara/master/README.md", "md"),
    ("inbetween", "https://raw.githubusercontent.com/rmusser01/Infosec_Reference/master/README.md", "md"),
    ("search", "https://en.wikipedia.org/wiki/List_of_search_engines", "wiki"),
    ("search", "https://en.wikipedia.org/wiki/Web_search_engine", "wiki"),
    ("search", "https://en.wikipedia.org/wiki/Metasearch_engine", "wiki"),
    ("search", "https://en.wikipedia.org/wiki/Comparison_of_web_search_engines", "wiki"),
    ("paste", "https://www.makeuseof.com/pastebin-alternatives/", "md"),
    ("paste", "https://www.maketecheasier.com/pastebin-alternatives/", "md"),
    ("paste", "https://www.swiftclip.io/en/blog/best-pastebin-alternatives-in-2026", "md"),
    ("paste", "https://www.makeuseof.com/tag/4-alternatives-that-may-be-better-than-pastebin", "md"),
    ("paste", "https://appmus.com/alternatives-to/pastebin", "md"),
    ("paste", "https://blog.drhack.net/5-best-pastebin-alternatives/", "md"),
    ("paste", "https://quickfever.com/best-pastebin-alternative", "md"),
    ("paste", "https://cloakbin.com/faq/what-are-alternatives-to-pastebin", "md"),
    ("paste", "https://www.droptext.app/blog/pastebin-alternatives", "md"),
    ("paste", "https://discourse.ubuntu.com/t/alternative-pastebin-options/82842", "md"),
    ("paste", "https://www.techshout.com/pastebin-alternative", "md"),
    ("paste", "https://openosint.tech/blog/pastebin-osint.html", "md"),
    ("paste", "https://tailscale.com/learn/best-pastebin-alternatives-for-secure-text-sharing", "md"),
    ("paste", "https://buffered.com/privacy-resources/best-pastebin-alternatives/", "md"),
    ("paste", "https://www.cloudwards.net/best-pastebin-alternatives/", "md"),
    ("paste", "https://www.freecodecamp.org/news/pastebin-alternatives/", "md"),
    ("paste", "https://www.geeksforgeeks.org/top-pastebin-alternatives-for-sharing-code-snippets/", "md"),
    ("paste", "https://www.sitepoint.com/pastebin-alternatives/", "md"),
    ("paste", "https://restoreprivacy.com/secure-paste-services/", "md"),
    ("paste", "https://www.comparitech.com/blog/vpn-privacy/best-pastebin-alternatives/", "md"),
    ("paste", "https://vpnoverview.com/privacy/pastebin-alternatives/", "md"),
    ("paste", "https://www.makeuseof.com/tag/pastebin-alternatives-share-code/", "md"),
    ("paste", "https://raw.githubusercontent.com/awesome-selfhosted/awesome-selfhosted/master/README.md", "md"),
    ("search", "https://www.searchenginecolossus.com/", "md"),
    ("search", "https://en.wikipedia.org/wiki/List_of_search_engines", "md"),
    ("search", "https://searx.space/", "md"),
    ("search", "https://www.privacytools.io/providers/search-engines/", "md"),
    ("inbetween", "https://raw.githubusercontent.com/edwardtay/awesome-OSINT/main/README.md", "md"),
    ("inbetween", "https://raw.githubusercontent.com/brandonhimpfen/awesome-osint/main/README.md", "md"),
    ("inbetween", "https://raw.githubusercontent.com/awesomelistsio/awesome-osint/main/README.md", "md"),
    ("inbetween", "https://raw.githubusercontent.com/th3hash/awesome-osint-tools/main/readme.md", "md"),
    ("inbetween", "https://raw.githubusercontent.com/K2SOsint/Legendary_OSINT/main/README.md", "md"),
    ("inbetween", "https://raw.githubusercontent.com/ubikron/Awesome-OSINT-Lists/main/README.md", "md"),
    ("inbetween", "https://theosintvault.io/best-osint-tools", "md"),
    ("search", "https://digitalguider.com/blog/top-50-search-engines/", "md"),
    ("search", "https://www.searchenginecolossus.com/index2.html", "md"),
    ("search", "https://www.ph4.org/search_searchcountries.php", "md"),
    ("search", "https://www.osintradar.com/tools/search-engines", "md"),
    ("inbetween", "https://raw.githubusercontent.com/soxoj/awesome-osint/master/README.md", "md"),
    ("inbetween", "https://raw.githubusercontent.com/cipher387/osint_stuff_tool_collection/master/README.md", "md"),
    ("inbetween", "https://raw.githubusercontent.com/Ph055a/OSINT-Collection/master/README.md", "md"),
    ("inbetween", "https://raw.githubusercontent.com/lockfale/osint/master/README.md", "md"),
    ("inbetween", "https://raw.githubusercontent.com/positivencrypt/awesome-osint/master/README.md", "md"),
    ("inbetween", "https://raw.githubusercontent.com/alext234/osint/master/README.md", "md"),
    ("inbetween", "https://raw.githubusercontent.com/bradokcs/OSINT-Scratchpad/master/README.md", "md"),
    ("inbetween", "https://raw.githubusercontent.com/kevinwg/osint-resources/master/README.md", "md"),
    ("inbetween", "https://raw.githubusercontent.com/osintworkshop/awesome-osint/master/README.md", "md"),
    ("inbetween", "https://raw.githubusercontent.com/arpsy/awesome-osint/master/README.md", "md"),
    ("search", "https://raw.githubusercontent.com/ssbc/awesome-search-engines/master/README.md", "md"),
    ("search", "https://www.privacyguides.org/en/search-engines/", "md"),
    ("search", "https://www.vpnmentor.com/blog/best-search-engines/", "md"),
    ("search", "https://www.wordstream.com/articles/search-engines", "md"),
    ("search", "https://en.wikipedia.org/wiki/Search_engine_(computing)", "wiki"),
    ("torrent", "https://www.vpnmentor.com/blog/best-torrent-sites/", "md"),
    ("torrent", "https://www.cloudwards.net/best-torrent-sites/", "md"),
    ("torrent", "https://www.comparitech.com/blog/vpn-privacy/best-torrent-sites/", "md"),
    ("torrent", "https://www.techradar.com/best/best-torrent-sites", "md"),
    ("inbetween", "https://raw.githubusercontent.com/compilerworks/awesome-osint/master/README.md", "md"),
    ("inbetween", "https://raw.githubusercontent.com/semist/ToolsOfTheTrade/master/README.md", "md"),
    ("inbetween", "https://raw.githubusercontent.com/InfosecTalks/awesome-osint/master/README.md", "md"),
    ("inbetween", "https://raw.githubusercontent.com/rk579/awesome-osint/master/README.md", "md"),
    ("search", "https://www.comparitech.com/blog/vpn-privacy/best-search-engines/", "md"),
    ("search", "https://www.cloudwards.net/best-private-search-engines/", "md"),
    ("search", "https://restoreprivacy.com/search-engines/", "md"),
    ("search", "https://www.makeuseof.com/tag/alternative-search-engines/", "md"),
    ("search", "https://raw.githubusercontent.com/learnhub/awesome-search-engines/master/README.md", "md"),
    ("search", "https://en.wikipedia.org/wiki/List_of_web_search_engines", "wiki"),
]


def run():
    h = load_hist()
    tracker_path = os.path.join(ROOT, "data", "trackers.txt")
    existing_trackers = set()
    if os.path.exists(tracker_path):
        existing_trackers = {l.strip() for l in open(tracker_path, encoding="utf-8") if l.strip()}

    for cat, url, kind in SOURCES:
        if url in h["sources"]:
            print("skip (already pulled): %s" % url)
            continue
        print("pulling: %s [%s]" % (url, cat))
        try:
            raw = download(url)
        except Exception as e:
            print("  ! fetch failed: %s" % e)
            continue
        if "awesome-selfhosted" in url:
            sec = re.search(r"##\s*Pastebins(.*?)(?=\n##\s|\Z)", raw, re.S)
            if sec:
                raw = sec.group(1)
        if kind == "md":
            pairs = extract_md(raw)
        elif kind == "wiki":
            pairs = extract_wiki(raw)
        elif kind == "json_osint":
            pairs = extract_json(json.loads(raw))

        d, p = load_file(cat)
        seen = existing_urls(cat, d)
        added = 0
        tracker_added = 0
        for name, u in pairs:
            if not u or not legit(u):
                continue
            if u.startswith("udp://"):
                if u not in existing_trackers and u not in h["added"].get("torrent", []):
                    existing_trackers.add(u)
                    tracker_added += 1
                continue
            nu = norm(u)
            if nu in seen or nu in h["added"].get(cat, []):
                continue
            nm = name or urlparse(u).netloc
            if len(nm) > 80:
                nm = urlparse(u).netloc
            append_entry(cat, d, nm, u)
            seen.add(nu)
            h["added"].setdefault(cat, []).append(nu)
            added += 1
        with open(p, "w", encoding="utf-8") as fh:
            json.dump(d, fh, indent=2)
        if tracker_added:
            with open(tracker_path, "w", encoding="utf-8") as fh:
                fh.write("\n".join(sorted(existing_trackers)) + "\n")
        h["sources"].append(url)
        save_hist(h)
        print("  +%d sites (%s), +%d trackers" % (added, cat, tracker_added))

    # summary
    for cat in ("paste", "torrent", "inbetween", "search"):
        d, _ = load_file(cat)
        if cat == "torrent":
            n = sum(len(d.get(k, [])) for k in ("public", "legal", "private_trackers"))
        elif cat == "inbetween":
            n = sum(len(d.get(k, [])) for k in d if isinstance(d[k], list))
        else:
            n = len(d["sites"] if cat == "paste" else d["targets"])
        print("%s total: %d (history added: %d)" % (cat, n, len(h["added"].get(cat, []))))


if __name__ == "__main__":
    run()
