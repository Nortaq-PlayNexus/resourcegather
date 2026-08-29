"""Count and verify the total callable functions in the framework."""
import inspect
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from core import sources

MODS = ["utils", "validation", "opsec", "ethics", "parsers", "storage",
        "analytics", "scheduler", "search", "report", "tor_client",
        "config_loader", "sources"]

total = 0
sources.build_functions()
for m in MODS:
    mod = __import__("core." + m, fromlist=["_"])
    fns = [n for n, o in inspect.getmembers(mod, inspect.isfunction)]
    total += len(fns)
    print("core.%-12s %d" % (m, len(fns)))
print("generated (sources) %d" % len(sources.GENERATED))
total += len(sources.GENERATED)
print("TOTAL: %d functions" % total)
print(">=500:", total >= 500)
