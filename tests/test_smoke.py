import os
import sys
import subprocess

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def test_selftest_passes():
    """The framework self-test must pass (config + data + generated functions)."""
    r = subprocess.run(
        [sys.executable, "main.py", "--selftest"],
        cwd=ROOT,
    )
    assert r.returncode == 0, "python main.py --selftest failed"


def test_function_count_gate():
    """Materialized function count must clear the >=500 gate."""
    r = subprocess.run(
        [sys.executable, "main.py", "--count"],
        cwd=ROOT,
    )
    assert r.returncode == 0, "python main.py --count failed"
