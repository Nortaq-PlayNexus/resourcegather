import json

res = json.load(open("data/_probe_results.json"))
dead = {u.lower() for u, s in res["results"].items() if s.startswith("dead")}
print("confirmed-dead URLs to remove: %d" % len(dead))


def load(f):
    return json.load(open(f, encoding="utf-8")), f


def save(d, f):
    json.dump(d, open(f, "w", encoding="utf-8"), indent=2)


# paste
d, f = load("data/paste_sites.json")
before = len(d["sites"])
d["sites"] = [s for s in d["sites"] if (s.get("url") or "").lower() not in dead]
save(d, f)
print("paste: %d -> %d" % (before, len(d["sites"])))

# torrent (multiple subcats)
d, f = load("data/torrent_sites.json")
tot_before = sum(len(d.get(k, [])) for k in ("public", "legal", "private_trackers"))
for k in ("public", "legal", "private_trackers"):
    d[k] = [s for s in d.get(k, []) if (s.get("url") or "").lower() not in dead]
save(d, f)
tot_after = sum(len(d.get(k, [])) for k in ("public", "legal", "private_trackers"))
print("torrent: %d -> %d" % (tot_before, tot_after))

# inbetween (subcats)
d, f = load("data/inbetween.json")
tot_before = sum(len(d[k]) for k in d if isinstance(d[k], list))
for k in list(d):
    if isinstance(d[k], list):
        d[k] = [s for s in d[k] if (s.get("url") or "").lower() not in dead]
save(d, f)
tot_after = sum(len(d[k]) for k in d if isinstance(d[k], list))
print("inbetween: %d -> %d" % (tot_before, tot_after))

# search
d, f = load("data/search_targets.json")
before = len(d["targets"])
d["targets"] = [t for t in d["targets"] if (t.get("search_url") or "").lower() not in dead]
save(d, f)
print("search: %d -> %d" % (before, len(d["targets"])))
