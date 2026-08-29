import json

def urls(f):
    d = json.load(open(f, encoding="utf-8"))
    if f.endswith("search_targets.json"):
        return [t["search_url"] for t in d["targets"]]
    if f.endswith("paste_sites.json"):
        return [s["url"] for s in d["sites"]]
    if f.endswith("torrent_sites.json"):
        out = []
        for k in ("public", "legal", "private_trackers"):
            out += [s["url"] for s in d.get(k, [])]
        return out
    out = []
    for k in d:
        if isinstance(d[k], list):
            out += [s["url"] for s in d[k]]
    return out

files = {"paste": "data/paste_sites.json", "torrent": "data/torrent_sites.json",
         "inbetween": "data/inbetween.json", "search": "data/search_targets.json"}
base = {"paste": 95, "torrent": 95, "inbetween": 1422, "search": 144}
allu = {}
for t, f in files.items():
    u = urls(f)
    fill = sum("[FILL]" in x for x in u)
    dup = len(u) - len(set(x.lower() for x in u))
    print("%s: total=%d  +%d vs baseline  FILL=%d  dupes=%d" % (t, len(u), len(u) - base[t], fill, dup))
    allu[t] = set(x.lower() for x in u)
cross = set()
ks = list(allu)
for i in range(len(ks)):
    for j in range(i + 1, len(ks)):
        cross |= allu[ks[i]] & allu[ks[j]]
print("cross-type duplicate URLs:", len(cross))
