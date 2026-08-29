"""tools/pad_to_500.py

Brings each top-level source type to >=500 entries:
  - data/paste_sites.json      -> 500 (sites)
  - data/torrent_sites.json    -> 500 (public+legal+private)
  - data/inbetween.json        -> 500 (across all subcategories)
  - data/search_targets.json   -> 500 (targets)

Real services already present are kept. The remaining slots are filled with
clearly-marked [FILL] placeholders (unique url so they survive dedupe and are
skipped by the runtime generator until you populate them).
"""
import json
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TARGET = 500


def load(p):
    fp = os.path.join(ROOT, p)
    with open(fp, "r", encoding="utf-8") as fh:
        return json.load(fh)


def save(p, d):
    fp = os.path.join(ROOT, p)
    with open(fp, "w", encoding="utf-8") as fh:
        json.dump(d, fh, indent=2)


def dedupe(items, key="url"):
    seen, out = set(), []
    for it in items:
        k = (it.get(key) or "").lower()
        if k in seen or not it.get("name"):
            continue
        seen.add(k)
        out.append(it)
    return out


def pad(items, prefix, network="clear", key="url"):
    i = 1
    while len(items) < TARGET:
        items.append({"name": "%s [FILL] #%d" % (prefix, i),
                      key: "[FILL]-%s-%d" % (prefix.lower().replace(" ", ""), i),
                      "network": network})
        i += 1
    return items


def run():
    # --- Paste ---
    d = load("data/paste_sites.json")
    sites = dedupe(list(d.get("sites", [])))
    if len(sites) < TARGET:
        sites = pad(sites, "Paste Site")
    d["sites"] = sites
    save("data/paste_sites.json", d)
    print("paste_sites.json: %d entries (real=%d, fill=%d)" % (
        len(sites), sum(1 for s in sites if "[FILL]" not in s["url"]),
        sum(1 for s in sites if "[FILL]" in s["url"])))

    # --- Torrent (total across subcats) ---
    d = load("data/torrent_sites.json")
    pub = dedupe(list(d.get("public", [])))
    legal = dedupe(list(d.get("legal", [])))
    priv = dedupe(list(d.get("private_trackers", [])))
    total = len(pub) + len(legal) + len(priv)
    i = 1
    while total < TARGET:
        pub.append({"name": "Torrent Index [FILL] #%d" % i,
                    "url": "[FILL]-torrent-%d" % i})
        pub = dedupe(pub)
        total = len(pub) + len(legal) + len(priv)
        i += 1
    d["public"], d["legal"], d["private_trackers"] = pub, legal, priv
    save("data/torrent_sites.json", d)
    real = sum(1 for s in pub + legal + priv if "[FILL]" not in s.get("url", ""))
    print("torrent_sites.json: %d entries (real=%d, fill=%d)" % (
        total, real, total - real))

    # --- Inbetween (total across subcats) ---
    d = load("data/inbetween.json")
    keys = ["ransomware_leak_sites", "cybercrime_forums", "darkweb_search",
            "i2p", "aggregators", "stealer_logs", "telegram_osint",
            "frameworks"]
    allitems = []
    for k in keys:
        d[k] = dedupe(list(d.get(k, [])))
        allitems += d[k]
    total = len(allitems)
    i = 1
    # pad mostly into aggregators (the generic bucket)
    while total < TARGET:
        d["aggregators"].append(
            {"name": "OSINT Source [FILL] #%d" % i,
             "url": "[FILL]-inbetween-%d" % i})
        d["aggregators"] = dedupe(d["aggregators"])
        total = sum(len(d[k]) for k in keys)
        i += 1
    save("data/inbetween.json", d)
    real = sum(1 for k in keys for s in d[k] if "[FILL]" not in s.get("url", ""))
    print("inbetween.json: %d entries (real=%d, fill=%d)" % (total, real, total - real))

    # --- Search targets ---
    d = load("data/search_targets.json")
    t = dedupe(list(d.get("targets", [])), key="search_url")
    if len(t) < TARGET:
        i = 1
        while len(t) < TARGET:
            t.append({"name": "Search Target [FILL] #%d" % i,
                      "search_url": "[FILL]-search-%d" % i, "network": "clear"})
            t = dedupe(t, key="search_url")
            i += 1
    d["targets"] = t
    save("data/search_targets.json", d)
    real = sum(1 for x in t if "[FILL]" not in x["search_url"])
    print("search_targets.json: %d entries (real=%d, fill=%d)" % (
        len(t), real, len(t) - real))


if __name__ == "__main__":
    run()
