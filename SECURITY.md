# Security Policy

`resourcegather` is a **defensive** Open-Source Intelligence (OSINT) framework.
It is built for breach-exposure monitoring, threat-actor attribution, academic
study, and early-warning. It is **not** a tool for unauthorized access, copyright
circumvention, or participation in criminal marketplaces.

## Authorized use

- Monitoring for *your own* credentials, domains, and assets in public leaks.
- Defensive threat-intel: tracking ransomware leak sites, stealer-log markets,
  and paste dumps to protect an organization.
- Academic / journalistic research on publicly available information.

## Prohibited use

- Targeting individuals outside a sanctioned defensive engagement.
- Unauthorized access, credential stuffing, or phishing.
- Harassment, doxxing, or surveillance of protected classes.
- Any violation of the laws of the operator's jurisdiction.

`core.ethics` enforces a scope + prohibited-pattern policy and performs PII
redaction before any finding is exported. Operators are responsible for
complying with applicable law and platform terms.

## OPSEC

- Route network activity through Tor and/or a VPN. Configure `use_tor`,
  `tor_proxy`, and `i2p_proxy` in `config/settings.json`.
- Do not embed real credentials or webhooks in committed files. Use `.env`
  (see `.env.example`) and keep secrets out of version control.
- Several Tier-3 targets are criminal infrastructure and are included only so
  defenders can *monitor* them. Never interact with them beyond read-only
  observation.

## Reporting a vulnerability

If you discover a security vulnerability in this tool itself (e.g. unsafe
default, leaked secret, RCE in a parser), please report it responsibly:

- Open a private security advisory on GitHub, **or**
- Email the maintainer via a GitHub Security Advisory.

Do **not** open a public issue for vulnerabilities. We will acknowledge and
coordinate a fix. This policy covers the *tool*; it is not an invitation to
report the activities of the third-party sites it indexes.
