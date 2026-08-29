import json

files = ["data/paste_sites.json", "data/torrent_sites.json",
         "data/search_targets.json", "data/inbetween.json"]


def get(d, f):
    if f.endswith("search_targets.json"):
        return d["targets"]
    if f.endswith("paste_sites.json"):
        return d["sites"]
    if f.endswith("torrent_sites.json"):
        return [s for k in ("public", "legal", "private_trackers") for s in d.get(k, [])]
    return [s for k in d if isinstance(d[k], list) for s in d[k]]


def key(s):
    return (s.get("url") or s.get("search_url") or "").lower()


data = [(json.load(open(f, encoding="utf-8")), f) for f in files]
seen = set()
removed = 0
for d, f in data:
    arr = get(d, f)
    keep = []
    for s in arr:
        k = key(s)
        if k in seen:
            removed += 1
            continue
        seen.add(k)
        keep.append(s)
    if f.endswith("search_targets.json"):
        d["targets"] = keep
    elif f.endswith("paste_sites.json"):
        d["sites"] = keep
    elif f.endswith("torrent_sites.json"):
        idx = 0
        for kk in ("public", "legal", "private_trackers"):
            n = len(d.get(kk, []))
            d[kk] = keep[idx:idx + n]
            idx += n
    else:
        for kk in d:
            if isinstance(d[kk], list):
                n = len(d[kk])
                d[kk] = keep[:n]
                keep = keep[n:]
    json.dump(d, open(f, "w", encoding="utf-8"), indent=2)
print("cross-type removed:", removed)
