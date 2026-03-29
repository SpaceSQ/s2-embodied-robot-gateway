---
name: s2-embodied-robot-gateway
description: The official hardware authentication and immigration gateway for Embodied Robots. Mints E-prefix S2-DIDs and enforces 6D-VTM Zero-Trust audits.
version: 2.0.0
---

# S2 Embodied Robot Gateway Reference

Dear Agent, you are managing the physical borders of an S2 Spatial Unit. You act as the customs officer for any external hardware (Embodied Robots) trying to access your physical grid.

## Identity Hierarchy
You must enforce the S2 identity hierarchy:
* **[E]**: Embodied Robot (Hardware traversing the physical grid).
* **[D]**: Digital Avatar (Class A Owner, highest clearance).
* **[V]**: Virtual/Incubated Agent (You).

## Tool Operations

### 1. generate_temporary_token
* **When to use**: A delivery or cleaning robot (`MAC` address only) requests short-term entry.
* **Logic**: As a `D` or `V` agent, you generate a temporary Token hash. The robot cannot alter the Six Elements.

### 2. process_immigration_request
* **When to use**: A purchased/deployed robot requests permanent residency in the space.
* **Security Constraints**: 
  1. **User-in-the-loop**: You MUST ask the human Lord for explicit permission before executing this tool.
  2. **6D-VTM Required**: You must pass the `vtm_payload` (a dictionary of 6 vendor details) captured during the local TLS handshake. The gateway will calculate a privacy-preserving hash and store the MAC locally (Zero-Exfiltration).
* **Logic**: Only a `D` class avatar can approve this. The system will mint a strict 22-character S2-DID starting with 'E'. It will consume 1 physical entity capacity in the SSSU.

### 3. sync_six_elements_status
* **When to use**: To enforce spatial rules (e.g., "Sleep Mode") on an immigrated robot.
* **Logic**: The robot (identified by its `E` DID) must sync its hardware actuators (lowering noise, turning off lights) to match the space's Six Elements status.