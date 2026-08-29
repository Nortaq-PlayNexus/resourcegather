#!/usr/bin/env python3
"""Resource Gather — EXE entry point.

Modes:
  python main.py --selftest            verify config + data + generated functions
  python main.py --count               print total callable functions (>=500)
  python main.py                       one collection pass (monitoring)
  python main.py --search "QUERY"      custom crawl across all indexed sites
  python main.py --search "QUERY" --loop 1800   AUTOMATED repeated search
  python main.py --report              print/export summary
  python main.py --gui                 launch minimal Tkinter UI
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import argparse

from core import sources
from core.config_loader import load_settings, load_json
from core.search import single_pass, automated_search
from core.report import print_report, export_summary


def selftest():
    print("Self-test...")
    try:
        s = load_settings()
        print("  settings OK: keywords=%d" % len(s.get("keywords", [])))
    except Exception as e:
        print("  settings FAILED: %s" % e)
        return 1
    try:
        for f in ("data/paste_sites.json", "data/torrent_sites.json",
                  "data/inbetween.json", "data/search_targets.json"):
            d = load_json(f)
            print("  %s OK (%d keys)" % (f, len(d)))
    except Exception as e:
        print("  data FAILED: %s" % e)
        return 1
    n = sources.build_functions()
    print("  generated functions: %d" % n)
    print("Self-test passed.")
    return 0


def count_functions():
    import inspect
    mods = [__import__("core." + m, fromlist=["_"]) for m in
            ["utils", "validation", "opsec", "ethics", "parsers", "storage",
             "analytics", "scheduler", "search", "report", "tor_client",
             "config_loader", "sources"]]
    total = 0
    for m in mods:
        fns = [n for n, o in inspect.getmembers(m, inspect.isfunction)]
        total += len(fns)
    total += len(sources.GENERATED)
    print("Callable functions:")
    for m in mods:
        print("  core.%-12s %d" % (m.__name__.split(".")[1],
              len([n for n, o in inspect.getmembers(m, inspect.isfunction)])))
    print("  generated (sources) %d" % len(sources.GENERATED))
    print("TOTAL: %d functions" % total)
    return total


def launch_gui():
    try:
        import tkinter as tk
        from tkinter import scrolledtext
    except Exception as e:
        print("GUI unavailable: %s" % e)
        return 1
    sources.build_functions()
    settings = load_settings()
    alert = settings.get("alert_webhook") or None

    root = tk.Tk()
    root.title("Resource Gather")
    root.geometry("760x520")

    tk.Label(root, text="Custom search query:").pack(anchor="w", padx=8, pady=2)
    q = tk.Entry(root, width=90)
    q.pack(fill="x", padx=8)
    tk.Label(root, text="Loop interval (sec, 0 = single):").pack(anchor="w", padx=8, pady=2)
    iv = tk.Entry(root, width=20)
    iv.insert(0, "0")
    iv.pack(anchor="w", padx=8)

    out = scrolledtext.ScrolledText(root, height=22)
    out.pack(fill="both", expand=True, padx=8, pady=8)

    def run():
        query = q.get().strip()
        interval = int(iv.get() or 0)
        out.insert("end", ">> search: %s\n" % query)
        try:
            if interval > 0:
                automated_search(query, interval=interval)
            else:
                single_pass(query=query or None)
            out.insert("end", ">> done. See output/findings.csv\n")
        except Exception as e:
            out.insert("end", "!! %s\n" % e)
        out.see("end")

    tk.Button(root, text="Run", command=run).pack(side="left", padx=8, pady=4)
    tk.Button(root, text="Summary", command=lambda: out.insert("end", str(print_report()) + "\n")).pack(side="left")

    root.mainloop()
    return 0


def main():
    ap = argparse.ArgumentParser(description="Resource Gather framework")
    ap.add_argument("--search", type=str, default=None)
    ap.add_argument("--loop", type=int, default=0)
    ap.add_argument("--selftest", action="store_true")
    ap.add_argument("--count", action="store_true")
    ap.add_argument("--report", action="store_true")
    ap.add_argument("--gui", action="store_true")
    args = ap.parse_args()

    sources.build_functions()

    if args.selftest:
        sys.exit(selftest())
    if args.count:
        sys.exit(0 if count_functions() >= 500 else 1)
    if args.gui:
        sys.exit(launch_gui())
    if args.report:
        print_report()
        export_summary()
        sys.exit(0)
    if args.loop > 0:
        settings = load_settings()
        alert = settings.get("alert_webhook") or None
        query = args.search
        import time
        from core.opsec import safe_delay
        print("Looping every %ds. Ctrl+C to stop. Run under VPN+Tor." % args.loop)
        try:
            while True:
                if query:
                    automated_search(query, interval=args.loop)
                else:
                    single_pass()
                safe_delay(args.loop * 0.5, args.loop * 1.5)
        except KeyboardInterrupt:
            print("\nStopped by user.")
    else:
        single_pass(query=args.search)


if __name__ == "__main__":
    main()
