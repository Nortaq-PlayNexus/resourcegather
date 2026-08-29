"""tools/final_dedupe.py — global cross-subcategory dedupe, keeps first copy."""
import json
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def n(u):
    u = (u or "").strip().lower()
    if u.startswith("https://"):
        u = "http://" + u[8:]
    return u.rstrip("/")


def load(p):
    with open(os.path.join(ROOT, p), "r", encoding="utf-8") as fh:
        return json.load(fh)


def save(p, d):
    with open(os.path.join(ROOT, p), "w", encoding="utf-8") as fh:
        json.dump(d, fh, indent=2)


def run():
    # Torrent: dedupe across public/legal/private_trackers
    d = load("data/torrent_sites.json")
    seen = set()
    for k in ("public", "legal", "private_trackers"):
        kept = []
        for it in d.get(k, []):
            u = n(it.get("url"))
            if u and u not in seen:
                seen.add(u)
                kept.append(it)
        d[k] = kept
    save("data/torrent_sites.json", d)
    print("torrent_sites.json: %d entries" % sum(len(d[k]) for k in
          ("public", "legal", "private_trackers")))

    # Inbetween: dedupe across all subcategories
    d = load("data/inbetween.json")
    seen = set()
    total = 0
    for k in list(d.keys()):
        if not isinstance(d[k], list):
            continue
        kept = []
        for it in d[k]:
            u = n(it.get("url"))
            if u and u not in seen:
                seen.add(u)
                kept.append(it)
        d[k] = kept
        total += len(kept)
    save("data/inbetween.json", d)
    print("inbetween.json: %d entries" % total)


if __name__ == "__main__":
    run()
