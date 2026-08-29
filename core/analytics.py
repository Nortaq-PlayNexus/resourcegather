"""core.analytics — correlation, scoring, and timeline over collected findings."""
import datetime
from collections import Counter


def dedupe(rows):
    seen, out = set(), []
    for r in rows:
        k = (r.get("source"), r.get("matched"), r.get("url"))
        if k not in seen:
            seen.add(k)
            out.append(r)
    return out


def by_source(rows):
    return dict(Counter(r.get("source") for r in rows))


def by_category(rows):
    return dict(Counter(r.get("category") for r in rows))


def by_day(rows):
    out = {}
    for r in rows:
        day = (r.get("timestamp") or "")[:10]
        out[day] = out.get(day, 0) + 1
    return out


def timeline(rows):
    return sorted(rows, key=lambda r: r.get("timestamp", ""))


def top_sources(rows, n=5):
    return Counter(r.get("source") for r in rows).most_common(n)


def rank_findings(rows):
    scored = []
    for r in rows:
        score = 1
        if r.get("category") == "search":
            score += 2
        if r.get("matched"):
            score += 1
        scored.append((score, r))
    return sorted(scored, key=lambda x: x[0], reverse=True)


def correlate(rows, key="matched"):
    out = {}
    for r in rows:
        out.setdefault(r.get(key), []).append(r)
    return out


def unique_matches(rows):
    return sorted({r.get("matched") for r in rows if r.get("matched")})


def count_total(rows):
    return len(rows)


def confidence(rows):
    hits = sum(1 for r in rows if r.get("category") == "search")
    return round(100.0 * hits / len(rows), 1) if rows else 0.0


def merge_identical(rows):
    return dedupe(rows)


def cluster_by_domain(rows):
    out = {}
    for r in rows:
        d = (r.get("url") or "").split("/")[2] if "://" in (r.get("url") or "") else "?"
        out.setdefault(d, []).append(r)
    return out


def recency_weight(rows, half_life_days=7):
    now = datetime.datetime.now(datetime.timezone.utc)
    out = []
    for r in rows:
        try:
            ts = datetime.datetime.fromisoformat(r.get("timestamp"))
        except Exception:
            ts = now
        age = (now - ts).days
        w = 0.5 ** (age / half_life_days)
        out.append((w, r))
    return sorted(out, key=lambda x: x[0], reverse=True)


def extract_entities(rows):
    import itertools
    emails, domains, ips, hashes = [], [], [], []
    for r in rows:
        ind = r.get("indicators") or {}
        emails += ind.get("emails", [])
        domains += ind.get("domains", [])
        ips += ind.get("ips", [])
        hashes += ind.get("hashes", [])
    return {"emails": sorted(set(emails)), "domains": sorted(set(domains)),
            "ips": sorted(set(ips)), "hashes": sorted(set(hashes))}


def severity(rows):
    c = by_category(rows)
    return {"search": c.get("search", 0), "monitor": c.get("monitor", 0),
            "onion": c.get("onion", 0)}


def delta(prev, cur):
    return len(cur) - len(prev)


def coverage(rows, total_sources):
    return round(100.0 * len({r.get("source") for r in rows}) / total_sources, 1) \
        if total_sources else 0.0


def summarize(rows):
    return {
        "total": len(rows),
        "by_source": by_source(rows),
        "by_category": by_category(rows),
        "by_day": by_day(rows),
        "unique_matches": unique_matches(rows),
        "confidence": confidence(rows),
    }


def filter_after(rows, iso_ts):
    return [r for r in rows if (r.get("timestamp") or "") >= iso_ts]


def filter_before(rows, iso_ts):
    return [r for r in rows if (r.get("timestamp") or "") <= iso_ts]


def intersects(a, b, key="matched"):
    return [x for x in a if any(x.get(key) == y.get(key) for y in b)]


def group_consecutive(rows, gap_minutes=60):
    groups, cur, last = [], [], None
    for r in timeline(rows):
        ts = r.get("timestamp")
        if last and (datetime.datetime.fromisoformat(ts) -
                     datetime.datetime.fromisoformat(last)).seconds > gap_minutes * 60:
            groups.append(cur)
            cur = []
        cur.append(r)
        last = ts
    if cur:
        groups.append(cur)
    return groups


def entropy(labels):
    import math
    total = sum(labels.values()) or 1
    return -sum((v / total) * math.log2(v / total)
                for v in labels.values() if v)


def score_source_health(rows):
    return {s: c for s, c in Counter(r.get("source") for r in rows).items()}


def top_matches(rows, n=10):
    return Counter(r.get("matched") for r in rows).most_common(n)
