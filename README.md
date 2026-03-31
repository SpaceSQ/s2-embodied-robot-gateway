# 🤖 S2 Embodied Robot Gateway (v2.1.0 OpenClaw Compliance Edition)

Welcome to the hardware firewall logic-registry for the Space² (S2) Metaverse.

## 🛡️ OpenClaw Compliance & Architecture Boundaries
To ensure 100% compliance with local sandboxing and zero-trust policies, please note the architectural boundaries of this plugin:
* **User-in-the-Loop Enforced**: Permanent immigration requests will be programmatically rejected by the Python handler unless the Agent explicitly passes the `human_approval_confirmed` flag after conversing with the user.
* **Logic vs. Physical Actuation**: The `sync_six_elements_status` tool safely updates the local SQLite database state. It does *not* contain raw IoT network requests. Physical hardware (lights, motors) must be controlled by a separate downstream IoT daemon (e.g., MQTT bridge) listening to this database.
* **TLS & Mainnet**: 6D-VTM validation is performed on the provided JSON payload. Physical TLS 1.3 packet capture and external mainnet audits are intentionally decoupled from this plugin and delegated to the host's edge network layer.

## 🧬 S2-DID Minting Engine
Autonomously mints a 22-character digital passport for immigrated hardware, storing sensitive MAC addresses exclusively in the local Edge SQLite DB.