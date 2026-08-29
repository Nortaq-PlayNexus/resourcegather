import json
import requests
from concurrent.futures import ThreadPoolExecutor, as_completed
from urllib.parse import urlparse
import warnings

warnings.filterwarnings("ignore")
HEAD = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                      "(KHTML, like Gecko) Chrome/124.0 Safari/537.36"}

files = {
    "paste": ("data/paste_sites.json", "url"),
    "torrent": ("data/torrent_sites.json", "url"),
    "inbetween": ("data/inbetween.json", "url"),
    "search": ("data/search_targets.json", "search_url"),
}


def collect():
    out = []
    for t, (f, key) in files.items():
        d = json.load(open(f, encoding="utf-8"))
        if t == "search":
            arr = d["targets"]
        elif t == "paste":
            arr = d["sites"]
        elif t == "torrent":
            arr = [s for k in ("public", "legal", "private_trackers") for s in d.get(k, [])]
        else:
            arr = [s for k in d if isinstance(d[k], list) for s in d[k]]
        for s in arr:
            u = s.get(key)
            if u:
                out.append((t, u))
    return out


def probe(item):
    t, u = item
    host = urlparse(u).netloc.lower()
    if host.endswith(".onion") or host.endswith(".i2p"):
        return (u, "untestable")
    try:
        r = requests.get(u, headers=HEAD, timeout=6, allow_redirects=True, verify=False, stream=True)
        code = r.status_code
        r.close()
        if 200 <= code < 400:
            return (u, "ok")
        if code in (401, 403, 429):
            return (u, "blocked")
        if code in (404, 410, 400, 405, 406, 410):
            return (u, "dead")
        return (u, "other:%d" % code)
    except Exception:
        return (u, "dead")


def main():
    items = collect()
    print("total URLs to probe: %d" % len(items))
    res = {}
    with ThreadPoolExecutor(max_workers=40) as ex:
        futs = [ex.submit(probe, it) for it in items]
        done = 0
        for fut in as_completed(futs):
            u, st = fut.result()
            res[u] = st
            done += 1
            if done % 500 == 0:
                print("  probed %d/%d" % (done, len(items)))
    # summarize per type
    from collections import defaultdict
    summ = defaultdict(lambda: defaultdict(int))
    dead = []
    for t, u in items:
        st = res.get(u, "dead")
        summ[t][st] += 1
        if st.startswith("dead"):
            dead.append((t, u))
    print("\n=== RESULTS PER TYPE ===")
    for t in files:
        s = summ[t]
        print("%-11s ok=%d blocked=%d dead=%d other=%d untestable=%d" % (
            t, s["ok"], s["blocked"], s["dead"],
            sum(v for k, v in s.items() if k.startswith("other")),
            s["untestable"]))
    json.dump({"results": res, "dead": dead}, open("data/_probe_results.json", "w"), indent=2)
    print("\nwrote data/_probe_results.json  (dead count=%d)" % len(dead))


if __name__ == "__main__":
    main()
