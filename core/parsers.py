"""core.parsers — extract structured indicators from free text."""
import re

EMAIL_RE = re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}")
DOMAIN_RE = re.compile(r"\b(?:[a-z0-9](?:[a-z0-9-]{0,61}[a-z0-9])?\.)+[a-z]{2,}\b", re.I)
URL_RE = re.compile(r"https?://[^\s'\"]+")
IPV4_RE = re.compile(r"\b(?:\d{1,3}\.){3}\d{1,3}\b")
HASH_RE = re.compile(r"\b(?:[0-9a-fA-F]{32}|[0-9a-fA-F]{40}|[0-9a-fA-F]{64})\b")
BTC_RE = re.compile(r"\b[13][a-km-zA-HJ-NP-Z1-9]{25,34}\b")
CVE_RE = re.compile(r"CVE-\d{4}-\d{4,7}", re.I)
AWS_RE = re.compile(r"AKIA[0-9A-Z]{16}")
ONION_RE = re.compile(r"[a-z2-7]{16,56}\.onion", re.I)


def extract_emails(text):
    return list(set(EMAIL_RE.findall(text or "")))


def extract_domains(text):
    return list(set(DOMAIN_RE.findall(text or "")))


def extract_urls(text):
    return list(set(URL_RE.findall(text or "")))


def extract_ips(text):
    return list(set(IPV4_RE.findall(text or "")))


def extract_hashes(text):
    return list(set(HASH_RE.findall(text or "")))


def extract_btc(text):
    return list(set(BTC_RE.findall(text or "")))


def extract_cves(text):
    return list(set(CVE_RE.findall(text or "")))


def extract_aws_keys(text):
    return list(set(AWS_RE.findall(text or "")))


def extract_onions(text):
    return list(set(ONION_RE.findall(text or "")))


def extract_all(text):
    return {
        "emails": extract_emails(text),
        "domains": extract_domains(text),
        "urls": extract_urls(text),
        "ips": extract_ips(text),
        "hashes": extract_hashes(text),
        "btc": extract_btc(text),
        "cves": extract_cves(text),
        "aws_keys": extract_aws_keys(text),
        "onions": extract_onions(text),
    }


def parse_kv(text, sep=":"):
    out = {}
    for ln in (text or "").splitlines():
        if sep in ln:
            k, v = ln.split(sep, 1)
            out[k.strip()] = v.strip()
    return out


def parse_paste(raw):
    return {
        "length": len(raw or ""),
        "lines": len((raw or "").splitlines()),
        "indicators": extract_all(raw),
    }


def parse_search_results(html):
    from bs4 import BeautifulSoup
    try:
        soup = BeautifulSoup(html or "", "html.parser")
        return [a.get_text(" ", strip=True) for a in soup.find_all("a")][:200]
    except Exception:
        return []


def parse_table(html):
    from bs4 import BeautifulSoup
    out = []
    try:
        soup = BeautifulSoup(html or "", "html.parser")
        for tr in soup.find_all("tr"):
            out.append([td.get_text(" ", strip=True) for td in tr.find_all("td")])
    except Exception:
        pass
    return out


def snippet_around(text, term, width=80):
    idx = (text or "").lower().find(term.lower())
    if idx < 0:
        return ""
    s = max(0, idx - width)
    e = min(len(text), idx + len(term) + width)
    return text[s:e]


def clean_html(html):
    from bs4 import BeautifulSoup
    try:
        return BeautifulSoup(html or "", "html.parser").get_text(" ", strip=True)
    except Exception:
        return html or ""


def extract_code_blocks(text):
    return re.findall(r"```(?:[a-zA-Z]+)?\n(.*?)```", text or "", re.S)


def count_indicators(text):
    return sum(len(v) for v in extract_all(text).values())


def is_config_dump(text):
    return count_indicators(text) > 3


def split_records(text, sep="\n"):
    return [r for r in (text or "").split(sep) if r.strip()]


def pair_lines(text):
    lines = split_records(text)
    return list(zip(lines, lines[1:]))


def grep(text, pattern, flags=re.I):
    return [ln for ln in (text or "").splitlines()
            if re.search(pattern, ln, flags)]


def parse_json_safe(s):
    import json
    try:
        return json.loads(s), None
    except Exception as e:
        return None, str(e)


def extract_mentions(text):
    return list(set(re.findall(r"@[\w]+", text or "")))


def extract_hashes_by_type(text):
    out = {"md5": [], "sha1": [], "sha256": []}
    for h in extract_hashes(text):
        if len(h) == 32:
            out["md5"].append(h)
        elif len(h) == 40:
            out["sha1"].append(h)
        elif len(h) == 64:
            out["sha256"].append(h)
    return out


def normalize_indicators(text):
    a = extract_all(text)
    for k in a:
        a[k] = sorted(set(x.lower() for x in a[k]))
    return a


def parse_headers(raw):
    out = {}
    for ln in (raw or "").splitlines():
        if ":" in ln:
            k, v = ln.split(":", 1)
            out[k.strip()] = v.strip()
    return out


def extract_tokens(text, min_len=8):
    return list(set(re.findall(r"[A-Za-z0-9_\-]{%d,}" % min_len, text or "")))
