# Production Readiness

The local implementation is deliberately inspectable. Before real autonomous writes, add enterprise identity, repository ACLs, migrations, persisted transitions, event workers, leases/fencing/idempotency, reconciliation, approval/resume, hardened sandbox service, Git/CI/MCP/model adapters, persistent memory/artifacts, OpenTelemetry, hardened Kubernetes and tested disaster recovery.
