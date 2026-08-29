"""core.scheduler — timed, resumable collection loops with jitter."""
import time

from core.opsec import jitter_sleep, safe_delay
from core.utils import now_iso


def loop(interval, task, max_runs=None):
    runs = 0
    while True:
        try:
            task()
        except Exception as e:
            print("  [scheduler error] %s" % e)
        runs += 1
        if max_runs and runs >= max_runs:
            break
        jitter_sleep(interval)
    return runs


def every(interval):
    def decor(fn):
        def wrapped(*a, **k):
            while True:
                fn(*a, **k)
                jitter_sleep(interval)
        return wrapped
    return decor


def cron_like(hour=None, minute=0, task=None):
    while True:
        now = time.localtime()
        if (hour is None or now.tm_hour == hour) and now.tm_min == minute:
            task()
            time.sleep(60)
        else:
            time.sleep(20)


def run_with_timeout(fn, seconds=30):
    import signal

    def handler(signum, frame):
        raise TimeoutError("task exceeded %ss" % seconds)

    try:
        signal.signal(signal.SIGALRM, handler)
        signal.alarm(seconds)
        return fn()
    finally:
        signal.alarm(0)


def staggered(tasks, gap=2.0):
    for t in tasks:
        try:
            t()
        except Exception as e:
            print("  [staggered error] %s" % e)
        safe_delay(gap, gap + 2)


def schedule_sequence(steps):
    for fn, delay in steps:
        try:
            fn()
        except Exception as e:
            print("  [seq error] %s" % e)
        if delay:
            safe_delay(delay, delay + 1)


def heartbeat(tag):
    print("[%s] alive @ %s" % (tag, now_iso()))


def loop_until(condition_fn, task, interval=60, timeout=3600):
    elapsed = 0
    while not condition_fn():
        task()
        if elapsed >= timeout:
            return False
        jitter_sleep(interval)
        elapsed += interval
    return True


def repeat_n(task, n, gap=1.0):
    for i in range(n):
        try:
            task()
        except Exception as e:
            print("  [repeat error] %s" % e)
        if i < n - 1:
            safe_delay(gap, gap + 1)


def pause_until_next(interval, last_ts_holder):
    waited = interval
    time.sleep(waited)
    return waited
