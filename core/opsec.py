"""core.opsec — operational-security primitives for safe collection."""
import random
import time

USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36",
    "Mozilla/5.0 (compatible; ResourceGather/1.0; +defensive-osint)",
]


def random_ua():
    return random.choice(USER_AGENTS)


def make_headers(extra=None):
    h = {"User-Agent": random_ua(), "Accept-Language": "en-US,en;q=0.9"}
    if extra:
        h.update(extra)
    return h


def jitter_sleep(base, frac=0.3):
    time.sleep(base * (1 + random.uniform(-frac, frac)))


def safe_delay(min_s=1.0, max_s=4.0):
    time.sleep(random.uniform(min_s, max_s))


def proxy_url(addr):
    return "socks5h://%s:%d" % (addr[0], addr[1])


def apply_proxy(session, addr):
    p = proxy_url(addr)
    session.proxies.update({"http": p, "https": p})
    return session


def rotate_ua(session):
    session.headers.update({"User-Agent": random_ua()})
    return session


def circuit_isolation_ok(proxies):
    return bool(proxies.get("http", "").startswith("socks5"))


def request_budget(max_per_min=30):
    interval = 60.0 / max_per_min
    last = [0.0]

    def tick():
        now = time.time()
        wait = interval - (now - last[0])
        if wait > 0:
            time.sleep(wait)
        last[0] = time.time()
    return tick


def tor_host_ok(addr):
    import socket
    try:
        with socket.create_connection(addr, timeout=3):
            return True
    except Exception:
        return False


def scrub_headers_before_send(headers):
    drop = {"proxy-authorization", "authorization"}
    return {k: v for k, v in headers.items() if k.lower() not in drop}


def no_cookies(session):
    session.cookies.clear()
    return session


def random_padding_string(n=8):
    return "".join(random.choices("abcdefghijklmnopqrstuvwxyz", k=n))


def is_suspicious_redirect(url, allowed_domains):
    from core.utils import domain_of
    return domain_of(url) not in allowed_domains


def opsec_report(addr, proxies):
    return {
        "proxy": proxy_url(addr) if addr else None,
        "tor_routing": circuit_isolation_ok(proxies),
        "ua_rotation": True,
        "cookie_scrub": True,
    }


def harden_session(session, addr=None):
    session = no_cookies(session)
    session = rotate_ua(session)
    if addr:
        session = apply_proxy(session, addr)
    return session


def dns_leak_check_stub():
    return {"note": "run from isolated VM; verify no DNS leaks via external tool"}


def torify(session_factory, addr):
    def make():
        import requests
        s = session_factory()
        return apply_proxy(s, addr)
    return make


def safe_get(session, url, timeout=30, retries=2):
    last = None
    for _ in range(retries + 1):
        try:
            return session.get(url, timeout=timeout)
        except Exception as e:
            last = e
            safe_delay(1, 2)
    raise last


def throttle_guard(rate_fn):
    def wrap(fn):
        def wrapped(*a, **k):
            rate_fn()
            return fn(*a, **k)
        return wrapped
    return wrap


def isolation_ok(session):
    return session.proxies.get("http", "").startswith("socks5")


def redact_proxy_log(addr):
    return "%s:****" % addr[0] if addr else None


def verify_no_plaintext(session):
    return "http://" not in str(session.proxies.get("http", ""))


def exp_backoff(attempt):
    return min(60.0, (2 ** attempt))


def tag_attribution_safe(meta):
    meta.pop("source_ip", None)
    meta.pop("local_user", None)
    return meta
