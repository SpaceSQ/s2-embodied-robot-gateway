# Changelog

All notable changes to the `s2-embodied-robot-gateway` plugin will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/), and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2026-03-28

### 🚀 Added (Genesis Hardware Release)
- **S2-DID Minting Engine**: Implemented the ultimate statutory identity generation for silicon hardware. Generates strict 22-character, hyphen-less IDs with the `E` prefix (Embodied). Features a highly secure 2-letter checksum strategically placed *before* the final personalized 5-digit tail to prevent MAC spoofing.
- **Dual-Mode Access Protocol**:
  - `generate_temporary_token`: Enables local `D` or `V` class agents to dynamically issue time-limited, read-only transit hashes for third-party logistics/cleaning robots.
  - `process_immigration_request`: Empowers Class `A` Digital Avatars to approve permanent hardware residency, allocating a physical entity capacity within the 6-segment millimeter SSSU grid.
- **Hardware-to-Space Synergy (`sync_six_elements_status`)**: Enforces spatial obedience. Immigrated hardware must sync its physical actuators (e.g., lowering acoustic/optical footprint) when the local OS triggers "Sleep Mode" or "Private Negotiation".
- **ERSAP Whitepaper Integration**: Officially bundled the *S2 Embodied Robot Spatial Authentication Protocol (ERSAP)* English Whitepaper as a standard Markdown annex for third-party hardware vendors.

### 🔒 Security & OpenClaw Compliance
- Out-of-the-box compliance with OpenClaw v1.0+ strict registry validations.
- Explicitly defined `compat.pluginApi` and an empty `configSchema` to ensure seamless, headless execution without UI rendering blocks.
- 100% localized SQLite architecture (`s2_embodied_gateway.db`) to sandbox hardware logs and prevent cross-plugin data leakage.