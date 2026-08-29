"""core.sources — source-driven function generator.

Loads every site from the data/ inventories and materializes live adapter
functions: monitor_<slug>, search_<slug>, snapshot_<slug>, validate_<slug>,
extract_<slug>. This is DRY: one code path per behaviour, instantiated for each
source, so the framework exposes hundreds of callable functions without
hand-writing stubs.
"""
import re
import sys
import urllib.parse
from core.config_loader import load_json
from core.utils import sha256, is_onion_url, is_i2p_url, is_url
from core.tor_client import make_session
from core.storage import log_finding, save_snapshot
from core.parsers import clean_html, extract_all

this_module = sys.modules[__name__]
GENERATED = {}
SOURCES = []


def _slug(name):
    return re.sub(r"[^a-z0-9]+", "_", (name or "x").lower()).strip("_") or "x"


def _session_for(network):
    if network in ("tor", "onion"):
        return make_session(use_tor=True)
    return make_session(use_tor=False)


def _load_sources():
    out = []
    try:
        for s in load_json("data/paste_sites.json").get("sites", []):
            out.append({"name": s["name"], "url": s["url"],
                        "network": "clear", "kind": "paste"})
    except Exception:
        pass
    try:
        tor = load_json("data/torrent_sites.json")
        for sec in ("public", "legal", "private_trackers"):
            for s in tor.get(sec, []):
                out.append({"name": s["name"], "url": s["url"],
                            "network": "clear", "kind": "torrent"})
    except Exception:
        pass
    try:
        inb = load_json("data/inbetween.json")
        for sec, net in (("ransomware_leak_sites", "tor"),
                         ("cybercrime_forums", "tor"),
                         ("darkweb_search", "clear"),
                         ("i2p", "i2p"),
                         ("aggregators", "clear"),
                         ("stealer_logs", "clear"),
                         ("telegram_osint", "clear"),
                         ("frameworks", "clear")):
            for it in inb.get(sec, []):
                out.append({"name": it["name"], "url": it.get("url", ""),
                            "network": net, "kind": sec})
    except Exception:
        pass
    try:
        for t in load_json("data/search_targets.json").get("targets", []):
            out.append({"name": t["name"], "url": t["search_url"],
                        "network": t.get("network", "clear"),
                        "kind": "search", "search_url": t["search_url"]})
    except Exception:
        pass
    return out


def _make_monitor(src):
    def fn(session=None, keywords=None, alert=None):
        session = session or _session_for(src["network"])
        try:
            r = session.get(src["url"],
                            timeout=30 if src["network"] == "clear" else 60)
            if r.status_code != 200:
                return []
            text = clean_html(r.text)
            hits = []
            for kw in (keywords or []):
                if kw.lower() in text.lower():
                    log_finding("monitor", src["name"], kw, text,
                                sha256(text), src["url"], alert_webhook=alert)
                    hits.append(kw)
            return hits
        except Exception as e:
            print("  [warn] monitor %s: %s" % (src["name"], e))
            return []
    fn.__name__ = "monitor_" + _slug(src["name"])
    return fn


def _make_search(src):
    def fn(query, session=None, alert=None):
        session = session or _session_for(src["network"])
        url = src.get("search_url") or src["url"]
        if "{q}" in url:
            url = url.replace("{q}", urllib.parse.quote_plus(query))
        try:
            r = session.get(url,
                            timeout=30 if src["network"] == "clear" else 60)
            if r.status_code != 200:
                return False
            text = clean_html(r.text)
            save_snapshot(src["name"], url, r.text)
            if query.lower() in text.lower():
                log_finding("search", src["name"], query, text,
                            sha256(text), url, alert_webhook=alert)
                return True
            return False
        except Exception as e:
            print("  [warn] search %s: %s" % (src["name"], e))
            return False
    fn.__name__ = "search_" + _slug(src["name"])
    return fn


def _make_snapshot(src):
    def fn(session=None):
        session = session or _session_for(src["network"])
        try:
            r = session.get(src["url"],
                            timeout=30 if src["network"] == "clear" else 60)
            if r.status_code == 200:
                return save_snapshot(src["name"], src["url"], r.text)
        except Exception as e:
            print("  [warn] snapshot %s: %s" % (src["name"], e))
        return None
    fn.__name__ = "snapshot_" + _slug(src["name"])
    return fn


def _make_validate(src):
    def fn():
        from core.validation import classify_indicator
        return {"name": src["name"], "url": src["url"],
                "network": src["network"],
                "classified_as": classify_indicator(src["url"]),
                "valid_url": (is_url(src["url"]) or is_onion_url(src["url"])
                               or is_i2p_url(src["url"]))}
    fn.__name__ = "validate_" + _slug(src["name"])
    return fn


def _make_extract(src):
    def fn(session=None):
        session = session or _session_for(src["network"])
        try:
            r = session.get(src["url"],
                            timeout=30 if src["network"] == "clear" else 60)
            if r.status_code == 200:
                return extract_all(clean_html(r.text))
        except Exception:
            pass
        return {}
    fn.__name__ = "extract_" + _slug(src["name"])
    return fn


def build_functions():
    global SOURCES
    SOURCES = _load_sources()
    makers = (_make_monitor, _make_search, _make_snapshot,
              _make_validate, _make_extract)
    for src in SOURCES:
        if not src.get("url") or "[FILL]" in src["url"]:
            continue
        for maker in makers:
            fn = maker(src)
            GENERATED[fn.__name__] = fn
            setattr(this_module, fn.__name__, fn)
    return len(GENERATED)


def list_sources():
    return [{"name": s["name"], "kind": s["kind"], "network": s["network"]}
            for s in SOURCES]


def dispatch(name, *args, **kw):
    fn = GENERATED.get(name)
    if not fn:
        raise KeyError("no generated function: %s" % name)
    return fn(*args, **kw)


def run_all_monitors(keywords, alert=None):
    out = {}
    for name, fn in GENERATED.items():
        if name.startswith("monitor_"):
            out[name] = fn(keywords=keywords, alert=alert)
    return out


def run_search_all(query, alert=None):
    out = {}
    for name, fn in GENERATED.items():
        if name.startswith("search_"):
            out[name] = fn(query, alert=alert)
    return out
