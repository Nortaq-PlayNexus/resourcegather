import urllib.request, re
from urllib.parse import urlparse

pages = [
    ("paste", "https://sourceforge.net/software/product/Pastebin/alternatives/"),
    ("paste", "https://pasterbox.net/blog/best-pastebin-sites-2026/"),
    ("torrent", "https://www.rapidseedbox.com/blog/safe-torrent-sites"),
    ("torrent", "https://www.justdailytrackers.com/guides/best-torrent-trackers-2026"),
    ("search", "https://en.wikipedia.org/wiki/Metasearch_engine"),
]
SKIP = {"github.com", "twitter.com", "reddit.com", "facebook.com",
        "youtube.com", "wikipedia.org", "wikimedia.org", "linkedin.com"}
BAD = (".svg", ".png", ".jpg", ".css", ".js", ".ico", ".gif")
for cat, u in pages:
    try:
        h = urllib.request.urlopen(
            urllib.request.Request(u, headers={"User-Agent": "Mozilla/5.0"}),
            timeout=20).read().decode("utf-8", "replace")
        links = re.findall(r"https?://[^\s\"'<>]+", h)
        ext = [l for l in links
               if urlparse(l).netloc not in SKIP
               and not l.lower().endswith(BAD)]
        print(cat, u, "total", len(links), "ext", len(ext))
    except Exception as e:
        print("ERR", u, str(e)[:60])
