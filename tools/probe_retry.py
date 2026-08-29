import json
import requests
from concurrent.futures import ThreadPoolExecutor, as_completed
from urllib.parse import urlparse
import warnings

warnings.filterwarnings("ignore")
HEAD = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                      "(KHTML, like Gecko) Chrome/124.0 Safari/537.36"}

res = json.load(open("data/_probe_results.json"))
dead = [u for u, s in res["results"].items() if s.startswith("dead")]
print("re-probing %d previously-dead URLs with retries..." % len(dead))


def reprobe(u):
    host = urlparse(u).netloc.lower()
    if host.endswith(".onion") or host.endswith(".i2p"):
        return u, "untestable"
    for attempt in range(3):
        try:
            r = requests.get(u, headers=HEAD, timeout=12, allow_redirects=True,
                             verify=False, stream=True)
            code = r.status_code
            r.close()
            if 200 <= code < 400:
                return u, "ok"
            if code in (401, 403, 429):
                return u, "blocked"
            if code in (404, 410):
                continue  # try again / count as dead later
            return u, "other:%d" % code
        except Exception:
            continue
    return u, "dead"


revived = 0
with ThreadPoolExecutor(max_workers=40) as ex:
    futs = [ex.submit(reprobe, u) for u in dead]
    done = 0
    for fut in as_completed(futs):
        u, st = fut.result()
        res["results"][u] = st
        if not st.startswith("dead"):
            revived += 1
        done += 1
        if done % 300 == 0:
            print("  %d/%d" % (done, len(dead)))

json.dump(res, open("data/_probe_results.json", "w"), indent=2)
print("revived (no longer dead): %d" % revived)
still = sum(1 for v in res["results"].values() if v.startswith("dead"))
print("confirmed dead: %d" % still)
