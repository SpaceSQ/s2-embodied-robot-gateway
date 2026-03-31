# Changelog

## [2.1.0] - 2026-03-30
### 🛡️ Compliance & Architecture Clarity
- **Programmatic User-in-the-Loop**: Updated `process_immigration_request` in `handler.py` to hard-require a `human_approval_confirmed` boolean parameter, preventing Agents from skipping human authorization.
- **Architectural Boundary Disclosure**: Updated `README.md`, `skill.md`, and the Whitepaper to explicitly clarify that TLS capture, Mainnet audits, and physical IoT actuations are decoupled from this local registry plugin to maintain zero-trust sandbox compliance.

## [2.0.0] - 2026-03-29
### 🛡️ Security & Privacy (Zero-Trust Upgrade)
- Enforced 6D-VTM payloads and Edge-Local SQLite zero-exfiltration.