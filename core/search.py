"""core.search — orchestrates custom user search + automated monitoring."""
import os

from core.config_loader import load_settings, output_path
from core.tor_client import make_session
from core.opsec import harden_session, safe_delay
from core.ethics import policy_check, verify_authorized, redact_all
from core.storage import log_finding, save_snapshot
from core.sources import run_search_all, run_all_monitors, build_functions
from core.utils import sha256, url_encode


def _auth(scope, query):
    verify_authorized(scope, query)


def custom_search(query, settings=None, alert=None, i2p_proxy=None):
    """Crawl every search endpoint in data/search_targets.json for `query`."""
    settings = settings or load_settings()
    ok, reason = policy_check(settings.get("scope", "breach_monitoring"), query)
    if not ok:
        print("  [ethics block] %s" % reason)
        return {}
    print("[search] query=%r" % query)
    return run_search_all(query, alert=alert)


def monitor_pass(settings, alert=None):
    """Run configured keyword monitoring across all generated monitors."""
    kw = settings.get("keywords", [])
    if not kw:
        return {}
    return run_all_monitors(kw, alert=alert)


def single_pass(query=None):
    settings = load_settings()
    alert = settings.get("alert_webhook") or None
    _auth(settings.get("scope", "breach_monitoring"),
          query or " ".join(settings.get("keywords", [])))
    if query:
        custom_search(query, settings, alert=alert)
    elif settings.get("auto_search_keywords", False):
        for kw in settings.get("keywords", []):
            custom_search(kw, settings, alert=alert)
    else:
        monitor_pass(settings, alert=alert)
    print("[pass] complete")


def automated_search(query, interval=1800, max_runs=None):
    settings = load_settings()
    alert = settings.get("alert_webhook") or None
    runs = 0
    while True:
        custom_search(query, settings, alert=alert)
        runs += 1
        if max_runs and runs >= max_runs:
            break
        safe_delay(interval * 0.5, interval * 1.5)


def search_site_by_name(name, query):
    from core.sources import dispatch
    return dispatch("search_%s" % name, query) if "search_%s" % name in \
        __import__("core.sources", fromlist=["GENERATED"]).GENERATED else None


def export_query_results(query, rows):
    path = output_path("output/search_%s.json" % sha256(query)[:12])
    import json
    with open(path, "w", encoding="utf-8") as fh:
        json.dump({"query": query, "results": rows}, fh, indent=2)
    return path


def safe_query_log(query, hits):
    path = output_path("output/queries.log")
    with open(path, "a", encoding="utf-8") as fh:
        fh.write("%s\t%s\t%d\n" % (__import__("core.utils", fromlist=["now_iso"]).now_iso(), query, hits))


def build_and_run(query=None):
    build_functions()
    single_pass(query=query)
