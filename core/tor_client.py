"""core.tor_client — HTTP session helpers with optional Tor (SOCKS5) routing."""
import requests


def make_session(use_tor=False, proxy_addr=("127.0.0.1", 9050), ua=None):
    """Return a requests.Session. If use_tor, route through the Tor SOCKS proxy.

    socks5h:// resolves DNS through Tor (prevents local DNS leaks). Requires the
    requests[socks] extra (bundled by PyInstaller if installed at build time).
    """
    s = requests.Session()
    s.headers.update({"User-Agent": ua or "Mozilla/5.0 (resource-gather/1.0)"})
    if use_tor:
        proxy = "socks5h://%s:%d" % (proxy_addr[0], proxy_addr[1])
        s.proxies.update({"http": proxy, "https": proxy})
    return s
