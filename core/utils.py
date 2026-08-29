"""core.utils — general-purpose, side-effect-free helpers (defense toolkit)."""
import base64
import binascii
import datetime
import gzip
import hashlib
import html
import ipaddress
import json
import os
import random
import re
import string
import time
import unicodedata
import urllib.parse
import uuid
import zlib


def now_utc():
    return datetime.datetime.now(datetime.timezone.utc)


def now_iso():
    return now_utc().isoformat()


def timestamp():
    return now_utc().strftime("%Y-%m-%dT%H:%M:%SZ")


def epoch():
    return int(time.time())


def from_epoch(e):
    return datetime.datetime.fromtimestamp(e, datetime.timezone.utc)


def duration_fmt(seconds):
    seconds = int(seconds)
    m, s = divmod(seconds, 60)
    h, m = divmod(m, 60)
    d, h = divmod(h, 24)
    return "%dd %dh %dm %ds" % (d, h, m, s)


def sha1(s):
    return hashlib.sha1(s.encode("utf-8", "replace")).hexdigest()


def sha256(s):
    return hashlib.sha256(s.encode("utf-8", "replace")).hexdigest()


def sha512(s):
    return hashlib.sha512(s.encode("utf-8", "replace")).hexdigest()


def sha3_256(s):
    return hashlib.sha3_256(s.encode("utf-8", "replace")).hexdigest()


def blake2b(s):
    return hashlib.blake2b(s.encode("utf-8", "replace")).hexdigest()


def md5(s):
    return hashlib.md5(s.encode("utf-8", "replace")).hexdigest()


def crc32(s):
    return zlib.crc32(s.encode("utf-8", "replace")) & 0xFFFFFFFF


def fingerprint(text):
    return {"sha256": sha256(text), "sha1": sha1(text),
            "md5": md5(text), "len": len(text)}


def b64_encode(s):
    return base64.b64encode(s.encode("utf-8", "replace")).decode("ascii")


def b64_decode(s):
    return base64.b64decode(s).decode("utf-8", "replace")


def b64url_encode(s):
    return base64.urlsafe_b64encode(s.encode("utf-8", "replace")).decode("ascii")


def hex_encode(s):
    return s.encode("utf-8", "replace").hex()


def hex_decode(s):
    return bytes.fromhex(s).decode("utf-8", "replace")


def url_encode(s):
    return urllib.parse.quote_plus(s)


def url_decode(s):
    return urllib.parse.unquote_plus(s)


def html_escape(s):
    return html.escape(s)


def html_unescape(s):
    return html.unescape(s)


def rot13(s):
    return codecs_rot13(s)


def codecs_rot13(s):
    import codecs
    return codecs.encode(s, "rot_13")


def xor_bytes(data, key):
    return bytes(b ^ key[i % len(key)] for i, b in enumerate(data))


def normalize_ws(s):
    return re.sub(r"\s+", " ", s).strip()


def normalize_unicode(s):
    return unicodedata.normalize("NFKC", s)


def to_lower(s):
    return s.lower()


def to_upper(s):
    return s.upper()


def strip(s):
    return s.strip()


def truncate(s, n, suffix="..."):
    return s if len(s) <= n else s[:n - len(suffix)] + suffix


def slugify(s):
    s = normalize_unicode(s).lower()
    s = re.sub(r"[^a-z0-9]+", "_", s).strip("_")
    return s or "na"


def reverse(s):
    return s[::-1]


def is_ascii(s):
    return all(ord(c) < 128 for c in s)


def is_empty(s):
    return s is None or len(str(s).strip()) == 0


def word_count(s):
    return len(re.findall(r"\w+", s or ""))


def line_count(s):
    return len((s or "").splitlines())


def unique_lines(s):
    seen = []
    for ln in (s or "").splitlines():
        if ln not in seen:
            seen.append(ln)
    return "\n".join(seen)


def read_text(p):
    with open(p, "r", encoding="utf-8", errors="replace") as fh:
        return fh.read()


def write_text(p, t):
    os.makedirs(os.path.dirname(p) or ".", exist_ok=True)
    with open(p, "w", encoding="utf-8") as fh:
        fh.write(t)


def read_json(p):
    with open(p, "r", encoding="utf-8") as fh:
        return json.load(fh)


def write_json(p, o):
    os.makedirs(os.path.dirname(p) or ".", exist_ok=True)
    with open(p, "w", encoding="utf-8") as fh:
        json.dump(o, fh, indent=2)


def ensure_dir(p):
    os.makedirs(p, exist_ok=True)


def file_exists(p):
    return os.path.exists(p)


def file_size(p):
    return os.path.getsize(p) if os.path.exists(p) else -1


def list_files(d):
    return [os.path.join(d, f) for f in os.listdir(d)
            if os.path.isfile(os.path.join(d, f))]


def safe_filename(s):
    return re.sub(r"[^A-Za-z0-9._-]", "_", s)[:200]


def random_string(n=12):
    return "".join(random.choices(string.ascii_letters + string.digits, k=n))


def random_hex(n=16):
    return binascii.hexlify(os.urandom(n)).decode()


def uuid4():
    return str(uuid.uuid4())


def jitter(base, frac=0.3):
    return base * (1 + random.uniform(-frac, frac))


def clamp(x, lo, hi):
    return max(lo, min(hi, x))


def chunk(seq, n):
    return [seq[i:i + n] for i in range(0, len(seq), n)]


def flatten(lst):
    out = []
    for x in lst:
        if isinstance(x, list):
            out.extend(flatten(x))
        else:
            out.append(x)
    return out


def dedupe(seq):
    seen, out = set(), []
    for x in seq:
        if x not in seen:
            seen.add(x)
            out.append(x)
    return out


def intersect(a, b):
    return [x for x in a if x in b]


def union(a, b):
    return dedupe(a + b)


def difference(a, b):
    return [x for x in a if x not in b]


def freq_map(seq):
    d = {}
    for x in seq:
        d[x] = d.get(x, 0) + 1
    return d


def top_n(d, n=5):
    return sorted(d.items(), key=lambda kv: kv[1], reverse=True)[:n]


def most_common(seq):
    fm = freq_map(seq)
    return max(fm.items(), key=lambda kv: kv[1])[0] if fm else None


def avg(nums):
    return sum(nums) / len(nums) if nums else 0.0


def median(nums):
    if not nums:
        return 0.0
    s = sorted(nums)
    m = len(s) // 2
    return s[m] if len(s) % 2 else (s[m - 1] + s[m]) / 2


def contains_any(s, subs):
    return any(sub in s for sub in subs)


def contains_all(s, subs):
    return all(sub in s for sub in subs)


def starts_with_any(s, subs):
    return any(s.startswith(sub) for sub in subs)


def ends_with_any(s, subs):
    return any(s.endswith(sub) for sub in subs)


def mask_middle(s, keep=3):
    if len(s) <= keep * 2:
        return "*" * len(s)
    return s[:keep] + "*" * (len(s) - keep * 2) + s[-keep:]


def is_hex(s):
    return bool(re.fullmatch(r"[0-9a-fA-F]+", s or ""))


def is_base64(s):
    try:
        base64.b64decode(s, validate=True)
        return True
    except Exception:
        return False


def parse_kv(text, sep=":"):
    out = {}
    for ln in (text or "").splitlines():
        if sep in ln:
            k, v = ln.split(sep, 1)
            out[k.strip()] = v.strip()
    return out


def to_bool(s):
    return str(s).strip().lower() in ("1", "true", "yes", "y", "on")


def coalesce(*vals):
    for v in vals:
        if v is not None and v != "":
            return v
    return None


def nth(seq, i, default=None):
    try:
        return seq[i]
    except Exception:
        return default


def group_by(seq, keyfn):
    d = {}
    for x in seq:
        d.setdefault(keyfn(x), []).append(x)
    return d


def sort_by(seq, keyfn, reverse=False):
    return sorted(seq, key=keyfn, reverse=reverse)


def uniq_by(seq, keyfn):
    seen, out = set(), []
    for x in seq:
        k = keyfn(x)
        if k not in seen:
            seen.add(k)
            out.append(x)
    return out


def take(n, seq):
    return seq[:n]


def drop(n, seq):
    return seq[n:]


def enumerate_pairs(seq):
    return [(seq[i], seq[i + 1]) for i in range(len(seq) - 1)]


def merge_dicts(*dicts):
    out = {}
    for d in dicts:
        out.update(d or {})
    return out


def deep_get(d, path, default=None):
    cur = d
    for part in path.split("."):
        if isinstance(cur, dict) and part in cur:
            cur = cur[part]
        else:
            return default
    return cur


def set_nested(d, path, val):
    cur = d
    parts = path.split(".")
    for p in parts[:-1]:
        cur = cur.setdefault(p, {})
    cur[parts[-1]] = val


def env(name, default=None):
    return os.environ.get(name, default)


def bool_env(name, default=False):
    return to_bool(os.environ.get(name, str(default)))


def retry(fn, times=3, delay=1.0):
    last = None
    for i in range(times):
        try:
            return fn()
        except Exception as e:
            last = e
            time.sleep(delay * (i + 1))
    raise last


def memoize(fn):
    cache = {}

    def wrapped(*a):
        if a not in cache:
            cache[a] = fn(*a)
        return cache[a]
    return wrapped


def rate_limit(per_second=1.0):
    interval = 1.0 / per_second
    last = [0.0]

    def tick():
        now = time.time()
        wait = interval - (now - last[0])
        if wait > 0:
            time.sleep(wait)
        last[0] = time.time()
    return tick


def backoff(attempt, base=1.0, cap=60.0):
    return min(cap, base * (2 ** attempt))


def gzip_compress(s):
    return gzip.compress(s.encode("utf-8", "replace"))


def gzip_decompress(b):
    return gzip.decompress(b).decode("utf-8", "replace")


def is_ipv4(s):
    try:
        ipaddress.IPv4Address(s)
        return True
    except Exception:
        return False


def is_ipv6(s):
    try:
        ipaddress.IPv6Address(s)
        return True
    except Exception:
        return False


def is_onion(s):
    return bool(re.search(r"[a-z2-7]{16,56}\.onion", s or "", re.I))


def is_i2p(s):
    return ".i2p" in (s or "").lower()


def strip_scheme(s):
    return re.sub(r"^[a-zA-Z][a-zA-Z0-9+.-]*://", "", s or "")


def domain_of(url):
    return strip_scheme(url).split("/")[0].split("?")[0]


def count_items(seq):
    return len(seq)


def similarity(a, b):
    a, b = set(a or ""), set(b or "")
    if not a and not b:
        return 0.0
    return len(a & b) / len(a | b)


def plural(n, word):
    return "%d %s%s" % (n, word, "" if n == 1 else "s")


def safe_json(obj):
    try:
        return json.dumps(obj, default=str)
    except Exception:
        return "{}"


def is_url(value):
    if not value:
        return False
    return bool(re.match(r'^https?://[^\s/]+', value.strip()))


def is_onion_url(value):
    if not value:
        return False
    return bool(re.search(r'https?://[a-z2-7]{16,56}\.onion', value.strip(), re.I))


def is_i2p_url(value):
    if not value:
        return False
    return bool(re.search(r'https?://[^\s/]+\.i2p', value.strip(), re.I))


def is_clear_url(value):
    return is_url(value) and not is_onion_url(value) and not is_i2p_url(value)
