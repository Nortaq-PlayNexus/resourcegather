"""core.report — summary/export builders for operators."""
import json
import os
from collections import Counter

from core.config_loader import output_path
from core.storage import load_findings, export_json, export_csv
from core.analytics import summarize, top_sources, by_day
from core.ethics import ethics_stamp, redact_all


def build_summary():
    rows = load_findings()
    return {
        "stamp": ethics_stamp(),
        "summary": summarize(rows),
        "top_sources": top_sources(rows, 10),
        "by_day": by_day(rows),
        "total_findings": len(rows),
    }


def print_report():
    s = build_summary()
    print("=" * 60)
    print("RESOURCE GATHER — SUMMARY (%s)" % s["stamp"])
    print("Total findings : %d" % s["total_findings"])
    print("By category    : %s" % s["summary"].get("by_category"))
    print("Top sources    : %s" % s["top_sources"])
    print("By day         : %s" % s["by_day"])
    print("=" * 60)
    return s


def export_summary():
    s = build_summary()
    path = output_path("output/summary.json")
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(s, fh, indent=2)
    return path


def redacted_copy():
    rows = load_findings()
    for r in rows:
        r["snippet"] = redact_all(r.get("snippet", ""))
    return rows


def findings_to_text(rows):
    return "\n".join("[%s] %s | %s | %s" % (r.get("category"), r.get("source"),
                        r.get("matched"), r.get("url")) for r in rows)


def top_matches(rows, n=10):
    return Counter(r.get("matched") for r in rows).most_common(n)


def coverage_stats(rows, total_sources):
    return {
        "covered": len({r.get("source") for r in rows}),
        "total": total_sources,
        "pct": round(100.0 * len({r.get("source") for r in rows}) / total_sources, 1)
        if total_sources else 0.0,
    }


def write_markdown_report(rows, path=None):
    path = path or output_path("output/report.md")
    lines = ["# Investigation Report", "",
             "Generated: %s" % __import__("core.utils", fromlist=["now_iso"]).now_iso(),
             "Ethics: %s" % ethics_stamp(), "", "## Findings", ""]
    for r in rows:
        lines.append("- [%s] %s — `%s` (%s)" % (r.get("category"), r.get("source"),
                                                r.get("matched"), r.get("url")))
    with open(path, "w", encoding="utf-8") as fh:
        fh.write("\n".join(lines))
    return path


def json_bundle(rows):
    return {"stamp": ethics_stamp(), "count": len(rows), "rows": rows}


def daily_rollup(rows):
    out = {}
    for r in rows:
        d = (r.get("timestamp") or "")[:10]
        out.setdefault(d, 0)
        out[d] += 1
    return out


def severity_breakdown(rows):
    c = Counter(r.get("category") for r in rows)
    return dict(c)


def source_leaderboard(rows, n=10):
    return Counter(r.get("source") for r in rows).most_common(n)


def consolidate_export():
    rows = load_findings()
    export_json(rows, "consolidated.json")
    export_csv(rows, "consolidated.csv")
    return output_path("output/consolidated.json")


def audit_trail(rows):
    return [{"ts": r.get("timestamp"), "src": r.get("source"),
             "hash": r.get("content_sha256")} for r in rows]
