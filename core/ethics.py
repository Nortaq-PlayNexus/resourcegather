"""core.ethics — defensive-only guardrails and PII redaction.

The framework is built strictly for authorized defensive OSINT: breach-exposure
monitoring, threat-actor attribution, academic study, and early-warning. These
functions enforce scope, consent, and safe-handling policy.
"""
import re

PROHIBITED_PATTERNS = [
    r"how to hack", r"exploit.*(target|victim)", r"ddos.*tool",
    r"credential.*crack", r"ransom.*payment", r"buy.*access",
    r"initial access broker", r"carding", r"cashout",
]

DEFENSIVE_SCOPES = ["breach_monitoring", "threat_intel", "attribution",
                    "academic", "early_warning", "brand_protection"]


def is_defensive_scope(scope):
    return scope in DEFENSIVE_SCOPES


def scope_allowed(scope):
    return is_defensive_scope(scope)


def reject_if_prohibited(query):
    q = (query or "").lower()
    for p in PROHIBITED_PATTERNS:
        if re.search(p, q):
            return False, "prohibited_pattern:%s" % p
    return True, None


def policy_check(scope, query):
    ok, reason = reject_if_prohibited(query)
    if not ok:
        return False, reason
    if not scope_allowed(scope):
        return False, "scope_not_defensive:%s" % scope
    return True, None


def redact_email(text):
    return re.sub(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}",
                  "[REDACTED_EMAIL]", text or "")


def redact_ip(text):
    return re.sub(r"\b(?:\d{1,3}\.){3}\d{1,3}\b", "[REDACTED_IP]", text or "")


def redact_phone(text):
    return re.sub(r"\+?[0-9][0-9\s().-]{6,20}", "[REDACTED_PHONE]", text or "")


def redact_ssn(text):
    return re.sub(r"\b\d{3}-\d{2}-\d{4}\b", "[REDACTED_SSN]", text or "")


def redact_wallet(text):
    return re.sub(r"\b[13][a-km-zA-HJ-NP-Z1-9]{25,34}\b", "[REDACTED_BTC]",
                  text or "")


def redact_credentials(text):
    text = re.sub(r"(?i)(password|passwd|pwd)\s*[:=]\s*\S+", "[REDACTED]", text)
    text = re.sub(r"(?i)(api[_-]?key|secret|token)\s*[:=]\s*\S+", "[REDACTED]", text)
    return text


def redact_all(text):
    for fn in (redact_email, redact_ip, redact_phone, redact_ssn,
               redact_wallet, redact_credentials):
        text = fn(text)
    return text


def contains_pii(text):
    return bool(re.search(r"@|(?:\d{1,3}\.){3}\d{1,3}|\+?\d{7,}", text or ""))


def consent_required(text):
    return contains_pii(text)


def log_audit(event, scope, actor="system"):
    import datetime
    return {
        "ts": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "event": event, "scope": scope, "actor": actor,
        "policy": "defensive_only",
    }


def safe_to_store(text, redact=True):
    if contains_pii(text) and not redact:
        return False
    return True


def minimization(text, max_len=2000):
    return text[:max_len]


def purpose_limitation(meta):
    meta["retention"] = "investigation_only"
    return meta


def data_subject_rights_note():
    return "subject to GDPR/CCPA takedown on verified request"


def ethics_stamp():
    return "RG-ETHICS:defensive-osint-v1"


def verify_authorized(scope, query, actor="system"):
    ok, reason = policy_check(scope, query)
    if not ok:
        raise PermissionError("Ethics policy violation: %s" % reason)
    return log_audit("authorized_run", scope, actor)


def anonymize_source(meta):
    meta.pop("collector_ip", None)
    meta.pop("collector_host", None)
    return meta


def is_criminal_solicitation(text):
    return any(re.search(p, text or "", re.I) for p in PROHIBITED_PATTERNS)


def retain_only_necessary(findings, keep_keys=None):
    keep_keys = keep_keys or ["timestamp", "category", "source", "matched", "url"]
    return [{k: f.get(k) for k in keep_keys} for f in findings]


def dual_use_warning(text):
    return "dual_use" if ("exploit" in (text or "").lower()
                          or "payload" in (text or "").lower()) else "ok"
