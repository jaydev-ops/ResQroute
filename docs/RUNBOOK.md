# resQroute Operational Runbook & Incident Response Guide

## Emergency Operational Protocols
This document specifies step-by-step procedures for sysadmins, DevOps engineers, and disaster command center operators when system anomalies occur during active operations.

---

## 1. Incident Runbooks

### Runbook 01: Weather Feed & Map Sync Outage
- **Symptom**: External weather or government map feeds stop responding; `freshness_ts` exceeds 15 minutes.
- **Automated Mitigation**: System automatically activates **Degraded Freshness Warning Banner** on all client UIs (`"Warning: Data stale by 15 mins"`).
- **Operator Steps**:
  1. Check Redis pub/sub queue status: `redis-cli ping`.
  2. Inspect ingestion daemon logs: `docker-compose logs --tail=100 ingestion_service`.
  3. If external API is down, switch source mode to `MANUAL_AUTHORITY_OVERRIDE` via command panel.

---

### Runbook 02: Community Report Moderation Surge
- **Symptom**: Incoming unverified citizen hazard reports exceed 500 reports/minute during flash flood.
- **Automated Mitigation**: System auto-enforces spatial clustering (`ST_ClusterDBSCAN` with 100m radius) to merge duplicate points.
- **Operator Steps**:
  1. Open Authority Command Dashboard → Filter by `Cluster Size >= 5`.
  2. Perform bulk verification for clustered points to elevate status from `REPORTED` to `PROBABLE`.
  3. Issue official district closure for verified cluster centers.

---

### Runbook 03: Database Failover & State Rollback
- **Symptom**: Primary PostgreSQL container experiences disk full or crash during disaster event.
- **Operator Steps**:
  1. Docker health check auto-restarts container.
  2. If primary node fails, promote read-replica using `pg_promote`.
  3. Verify materialized view state: `REFRESH MATERIALIZED VIEW current_shelter_capacity;`.
  4. Review `audit_events` to verify zero data loss during failover window.
