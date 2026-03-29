# Changelog

All notable changes to the `s2-embodied-robot-gateway` plugin will be documented in this file.

## [2.0.0] - 2026-03-29
### 🛡️ Security & Privacy (Zero-Trust Upgrade)
- **6D-VTM Enforcement**: `process_immigration_request` now strictly requires a 6-Dimensional Vendor Transparency Manifesto payload. Hardware failing to provide this is blocked at the edge.
- **Edge-Local Zero-Exfiltration**: Device MAC addresses and Gene Codes are now mathematically isolated in the local SQLite DB. The gateway computes a `vtm_hash` to facilitate anonymized reputation queries against the S2 Mainnet without leaking user topology.
- **User-in-the-Loop Constraint**: Updated Agent `skill.md` directives to legally mandate human Lord approval before permanent E-DID minting.
- **Whitepaper Sync**: Upgraded `S2-ERSAP-Whitepaper-EN.md` to V2.0.0 to reflect the new data topography matrix.

## [1.0.0] - 2026-03-28
### 🚀 Added (Genesis Hardware Release)
- **S2-DID Minting Engine**: Strict 22-character, hyphen-less IDs with the `E` prefix and 2-letter checksums.
- **Dual-Mode Access Protocol**: `generate_temporary_token` and `process_immigration_request`.
- **Hardware-to-Space Synergy (`sync_six_elements_status`)**.