# Threat Model

Trust boundaries include user input, repository contents, dependencies/build scripts, model output, MCP servers, sandboxes, Git providers and artifact stores.

Primary threats: prompt injection, malicious build execution, secret exfiltration, SSRF, sandbox escape, cross-tenant leakage, dependency confusion, tool poisoning, approval substitution and stale-worker writes.

Controls: repository authorization, content-as-data treatment, deny-by-default egress, hardened sandboxing, short-lived credentials, tool policy, leases/fencing, idempotency, immutable patch hashes, secret scanning and append-only audit.
