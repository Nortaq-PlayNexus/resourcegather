"""core.storage — chain-of-custody logging, integrity, and export."""
import csv
import json
import os
from datetime import datetime, timezone

from core.config_loader import output_path
from core.utils import sha256


def _utc():
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def log_finding(category, source, matched, snippet, content_hash, url="",
                alert_webhook=None, meta=None):
    path = output_path("output/findings.csv")
    os.makedirs(os.path.dirname(path), exist_ok=True)
    write_header = not os.path.exists(path)
    with open(path, "a", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh)
        if write_header:
            w.writerow(["timestamp", "category", "source", "matched",
                        "snippet", "content_sha256", "url", "meta"])
        w.writerow([_utc(), category, source, matched, (snippet or "")[:280],
                    content_hash, url, json.dumps(meta or {})])
    if alert_webhook:
        try:
            import requests
            requests.post(alert_webhook, json={"text": "[%s] %s matched '%s' @ %s"
                          % (category, source, matched, url)}, timeout=10)
        except Exception:
            pass
    print("  [FINDING] %s | %s | %s | %s" %
          (category, source, matched, content_hash[:12]))
    return content_hash


def save_snapshot(name, url, html, subdir="snapshots"):
    d = output_path("output/%s" % subdir)
    os.makedirs(d, exist_ok=True)
    fn = os.path.join(d, "%s_%d.html" % (sha256(url)[:16], int(
        datetime.now(timezone.utc).timestamp())))
    with open(fn, "w", encoding="utf-8", errors="replace") as fh:
        fh.write(html or "")
    return fn


def load_findings():
    path = output_path("output/findings.csv")
    if not os.path.exists(path):
        return []
    with open(path, "r", encoding="utf-8") as fh:
        return list(csv.DictReader(fh))


def dedupe_findings(rows):
    seen, out = set(), []
    for r in rows:
        key = (r.get("source"), r.get("matched"), r.get("content_sha256"))
        if key not in seen:
            seen.add(key)
            out.append(r)
    return out


def verify_integrity(rows):
    bad = []
    for r in rows:
        if not r.get("content_sha256"):
            bad.append(r)
    return {"total": len(rows), "invalid": len(bad)}


def export_json(rows, name="findings.json"):
    path = output_path("output/%s" % name)
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(rows, fh, indent=2)
    return path


def export_stix(rows):
    objects = []
    for r in rows:
        objects.append({
            "type": "indicator",
            "spec_version": "2.1",
            "id": "indicator--%s" % r.get("content_sha256", "")[:32],
            "pattern": "[email:value = '%s']" % r.get("matched", ""),
            "valid_from": r.get("timestamp"),
        })
    return {"type": "bundle", "objects": objects}


def export_misp(rows):
    events = []
    for r in rows:
        events.append({
            "Event": {"info": r.get("matched", ""),
                      "Attribute": [{"type": "text", "value": r.get("source")}]}})
    return events


def export_csv(rows, name="export.csv"):
    path = output_path("output/%s" % name)
    with open(path, "w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh)
        w.writerow(["timestamp", "category", "source", "matched", "url"])
        for r in rows:
            w.writerow([r.get("timestamp"), r.get("category"),
                        r.get("source"), r.get("matched"), r.get("url")])
    return path


def write_report(summary, name="report.json"):
    path = output_path("output/%s" % name)
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(summary, fh, indent=2)
    return path


def archive_session():
    return output_path("output")


def custody_record(category, source, url, content_hash):
    return {"ts": _utc(), "category": category, "source": source,
            "url": url, "hash": content_hash}


def count_by(rows, key):
    out = {}
    for r in rows:
        out[r.get(key)] = out.get(r.get(key), 0) + 1
    return out


def latest(rows, n=10):
    return rows[-n:]


def filter_rows(rows, **kw):
    out = []
    for r in rows:
        if all(r.get(k) == v for k, v in kw.items()):
            out.append(r)
    return out


def to_dict(rows):
    return rows


def merge_sessions(paths):
    rows = []
    for p in paths:
        if os.path.exists(p):
            with open(p, "r", encoding="utf-8") as fh:
                rows.extend(list(csv.DictReader(fh)))
    return rows


def integrity_manifest(rows):
    return {r.get("url"): r.get("content_sha256") for r in rows}


def redacted_export(rows):
    from core.ethics import redact_all
    for r in rows:
        r["snippet"] = redact_all(r.get("snippet", ""))
    return rows
