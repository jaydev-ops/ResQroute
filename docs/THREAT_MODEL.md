# resQroute Threat Model & Cybersecurity Assessment

## Threat Modeling Framework (STRIDE)
Disaster management applications are prime targets for malicious actors seeking to cause panic, divert emergency responders, or intercept vulnerable citizen locations. 

`resQroute` applies the **STRIDE Model** to identify and mitigate security risks across system boundaries.

---

## 1. Threat Identification & Mitigation Matrix

| Threat Category | Disaster Attack Vector | System Vulnerability | resQroute Security Mitigation |
| :--- | :--- | :--- | :--- |
| **Spoofing** | Attacker spoofs an Authority JWT token to trigger fake evacuation orders | Compromised credentials or weak token validation | RS256 asymmetric signed JWTs; MFA required for Authority logins |
| **Tampering** | Malicious injection of fake SMS coordinates to declare safe roads closed | Untrusted SMS input channel | SMS parsing treats input as `UNTRUSTED_CITIZEN`; hard closures require authority verification |
| **Repudiation** | An operator falsely denies triggering an unauthorized road closure | Lack of actor auditing | Immutable, append-only `audit_events` logging actor ID, timestamp, and policy version |
| **Information Disclosure** | Interception of vulnerable users' medical/disability data | Storing sensitive medical records in database | Minimal flag architecture (`wheelchair_required = true`); no medical diagnosis history stored |
| **Denial of Service** | DDoS attack flooding API during active hurricane | Unthrottled API endpoints | Redis rate limiting (100 req/min/IP); Cloudflare edge DDoS mitigation |
| **Elevation of Privilege** | Citizen account escalating role to create official hazards | Missing RBAC check on POST endpoints | Strict FastAPI dependency injection verifying `user_role == AUTHORITY` |

---

## 2. Privacy Boundaries & Data Minimization
1. **Zero Location Retention Policy**: Exact raw citizen coordinates are processed ephemerally in RAM during route calculation. Only aggregated route snapshot geometries are retained for post-disaster audit.
2. **Minimal Profile Flags**: The application collects binary flags (`wheelchair_required`, `electricity_required`) rather than granular medical conditions.
3. **SMS Anonymization**: Parsed incoming SMS payloads strip sender phone numbers immediately after extracting coordinate data, assigning a transient hash.
