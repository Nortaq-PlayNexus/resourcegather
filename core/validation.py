"""core.validation — input/format validators used across the pipeline."""
import re
import ipaddress


def is_email(s):
    return bool(re.fullmatch(r"[^@\s]+@[^@\s]+\.[^@\s]+", s or ""))


def is_domain(s):
    return bool(re.fullmatch(r"(?=^.{1,253}$)([A-Za-z0-9](?:[A-Za-z0-9-]{0,61}[A-Za-z0-9])?\.)+[A-Za-z]{2,}$", s or ""))


def is_url(s):
    return bool(re.fullmatch(r"https?://[^\s]+", s or ""))


def is_onion_url(s):
    return bool(re.search(r"https?://[a-z2-7]{16,56}\.onion", s or "", re.I))


def is_i2p_url(s):
    return bool(re.search(r"https?://[^\s]+\.i2p", s or "", re.I))


def is_ip(s):
    try:
        ipaddress.ip_address(s)
        return True
    except Exception:
        return False


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


def is_md5(s):
    return bool(re.fullmatch(r"[0-9a-fA-F]{32}", s or ""))


def is_sha1(s):
    return bool(re.fullmatch(r"[0-9a-fA-F]{40}", s or ""))


def is_sha256(s):
    return bool(re.fullmatch(r"[0-9a-fA-F]{64}", s or ""))


def is_hash(s):
    return is_md5(s) or is_sha1(s) or is_sha256(s)


def is_btc(s):
    return bool(re.fullmatch(r"[13][a-km-zA-HJ-NP-Z1-9]{25,34}", s or ""))


def is_cve(s):
    return bool(re.fullmatch(r"CVE-\d{4}-\d{4,7}", s or "", re.I))


def is_mac(s):
    return bool(re.fullmatch(r"([0-9A-Fa-f]{2}[:-]){5}[0-9A-Fa-f]{2}", s or ""))


def is_cidr(s):
    try:
        ipaddress.ip_network(s, strict=False)
        return True
    except Exception:
        return False


def is_asn(s):
    return bool(re.fullmatch(r"AS\d+", s or "", re.I))


def is_phone(s):
    return bool(re.fullmatch(r"\+?[0-9][0-9\s().-]{6,20}", s or ""))


def is_aws_key(s):
    return bool(re.fullmatch(r"AKIA[0-9A-Z]{16}", s or ""))


def is_private_key(s):
    return "PRIVATE KEY" in (s or "")


def is_jwt(s):
    return bool(re.fullmatch(r"[A-Za-z0-9_-]+\.[A-Za-z0-9_-]+\.[A-Za-z0-9_-]*", s or ""))


def is_base64(s):
    try:
        import base64
        base64.b64decode(s, validate=True)
        return True
    except Exception:
        return False


def is_uuid(s):
    import uuid
    try:
        uuid.UUID(s)
        return True
    except Exception:
        return False


def is_number(s):
    try:
        float(s)
        return True
    except Exception:
        return False


def is_int(s):
    try:
        int(s)
        return True
    except Exception:
        return False


def is_bool_str(s):
    return str(s).strip().lower() in ("true", "false", "0", "1", "yes", "no")


def is_json(s):
    try:
        import json
        json.loads(s)
        return True
    except Exception:
        return False


def is_short(s, n=3):
    return bool(s) and len(s) >= n


def is_valid_port(n):
    return isinstance(n, int) and 1 <= n <= 65535


def has_upper(s):
    return any(c.isupper() for c in s or "")


def has_lower(s):
    return any(c.islower() for c in s or "")


def has_digit(s):
    return any(c.isdigit() for c in s or "")


def has_special(s):
    return any(not c.isalnum() for c in s or "")


def password_strength(s):
    score = sum([has_upper(s), has_lower(s), has_digit(s), has_special(s),
                 len(s or "") >= 12])
    return score


def looks_like_leak(text):
    keys = ["password", "api_key", "token", "secret", "BEGIN RSA", "@gmail.com",
            "database", "leak", "dump", "credentials"]
    return any(k.lower() in (text or "").lower() for k in keys)


def is_fqdn(s):
    return is_domain(s)


def is_subdomain(s, base):
    return (s or "").endswith("." + base) and is_domain(s)


def validate_range(n, lo, hi, default=None):
    return n if lo <= n <= hi else default


def all_valid(items, validator):
    return all(validator(i) for i in items)


def any_valid(items, validator):
    return any(validator(i) for i in items)


def classify_indicator(s):
    s = (s or "").strip()
    for name, fn in (("email", is_email), ("domain", is_domain), ("url", is_url),
                     ("ipv4", is_ipv4), ("ipv6", is_ipv6), ("sha256", is_sha256),
                     ("sha1", is_sha1), ("md5", is_md5), ("btc", is_btc),
                     ("cve", is_cve), ("aws_key", is_aws_key),
                     ("onion", is_onion_url)):
        if fn(s):
            return name
    return "unknown"


def confidence_score(hits, total):
    return round(100.0 * hits / total, 1) if total else 0.0
