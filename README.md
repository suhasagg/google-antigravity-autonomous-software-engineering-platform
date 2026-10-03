# Google Antigravity Autonomous Software Engineering Platform


## Architecture

```text
                  ENGINEERING GOAL
                         |
                Engineering Planner
                         |
               Repository Analyzer
                         |
                 Task DAG Compiler
                         |
                  Supervisor Agent
                         |
       +----------+-----+-----+----------+
       |          |           |          |
    Research    Coding      Debug       Test
     Agent       Agent      Agent       Agent
       |          |           |          |
       +----------+-----+-----+----------+
                        |
                 Dynamic Subagents
                        |
                 Skills Registry
                        |
                  MCP Gateway
                        |
              Secure Code Sandbox
                        |
             Isolated Git Worktrees
                        |
        Build -> Test -> Run -> Benchmark
                        |
                  Reviewer Agent
                        |
               Evaluation Engine
                        |
             PASS / REPAIR / REPLAN
                        |
                  Merge Agent
                        |
                 Human Approval
                        |
                  Candidate PR
```

## What the executable reference implements

The repository contains real local Git inspection/worktree operations, DAG validation, role-separated engineering agents, dynamic-subagent fan-out abstraction, a skills registry, MCP gateway boundary, command allowlisting and time-bounded subprocess execution, test execution, diff generation, reviewer/evaluator logic, repair diagnostics, immutable approval hashing, artifact persistence, PostgreSQL durable-state schema foundations, transactional-outbox/idempotency models, Redis and Redpanda infrastructure, Docker Compose, Kubernetes manifests and tests.

The coding agent intentionally writes only inside an isolated worktree. The reference never silently pushes or merges code.

## Quick Start

```bash
unzip google-antigravity-autonomous-software-engineering-platform.zip
cd google-antigravity-autonomous-software-engineering-platform
cp .env.example .env
docker compose build
docker compose up -d
curl http://localhost:8000/health
```

List skills:

```bash
curl http://localhost:8000/v1/skills -H 'x-api-key: change-me'
```

The API requires an existing Git checkout visible inside the API container. For local host development, this is easiest:

```bash
docker compose up -d postgres redis redpanda
python3 -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
```

Change PostgreSQL/Redis/Redpanda hostnames in `.env` to `localhost`, then:

```bash
uvicorn app.main:app --reload
```

Submit an engineering goal, replacing `/absolute/path/to/repo` with a local Git checkout:

```bash
curl -X POST http://localhost:8000/v1/engineering/run \
  -H 'x-api-key: change-me' \
  -H 'Content-Type: application/json' \
  -d '{
    "tenant_id":"demo",
    "principal_id":"engineer@example",
    "repository":"/absolute/path/to/repo",
    "goal":"Inspect the repository, propose a safe improvement, run tests and prepare a reviewed candidate patch",
    "base_ref":"HEAD"
  }'
```

Tests:

```bash
pytest -q
ruff check .
```

## 1. Product Definition

This system is an autonomous software-engineering control plane. It converts an engineering objective into governed, evidence-producing tasks executed against isolated repository workspaces.

## 2. Antigravity Alignment

Google publicly describes Antigravity 2.0 as an agent-first environment supporting multiple parallel agents, dynamic subagents and scheduled/background tasks. Google also describes a unified agent harness exposed through Antigravity CLI/SDK and Managed Agents. This project uses those public concepts as architectural inspiration without claiming internal equivalence.

## 3. Why Multi-Agent Engineering

A single coding prompt mixes planning, research, editing, testing and review. Role separation allows different policies, models, tools and budgets for each responsibility.

## 4. Engineering Goal

A goal includes repository, base revision, objective, tenant/principal context, constraints and optional acceptance criteria.

## 5. Repository Analyzer

`repository.py` verifies a real Git checkout, captures HEAD/status, counts files and language extensions, and exposes Git-backed search.

Production analyzers should additionally build:

```text
symbol index
AST index
dependency graph
call graph
ownership map
test map
build graph
historical change graph
```

## 6. Repository Snapshot

Every run should pin:

```text
repository identity
commit SHA
base branch/ref
dirty-state policy
dependency lockfiles
toolchain version
```

This makes engineering decisions reproducible.

## 7. Code Graph

A production code graph can model:

```text
File -> DEFINES -> Symbol
Symbol -> CALLS -> Symbol
Module -> IMPORTS -> Module
Test -> COVERS -> Symbol
Service -> DEPENDS_ON -> Service
Owner -> OWNS -> Path
```

## 8. Planner

The planner creates typed engineering work rather than directly editing code.

## 9. Plan Schema

Each task has:

```text
task key
role
description
dependencies
risk
tool/skill requirements
resource requirements
acceptance criteria
```

## 10. Task DAG Compiler

The compiler rejects duplicate IDs, missing dependencies and cycles. Production validation also checks capability availability, policy, budgets and schemas.

## 11. Immutable Plan Versions

Replanning creates a new version. Existing execution history remains attached to the original plan.

## 12. Supervisor

The supervisor owns coordination, not unrestricted authority. It can dispatch registered work, inspect outcomes and request replanning.

## 13. Research Agent

The research agent understands repository structure, code history, documentation, issues and external technical evidence.

## 14. Coding Agent

The coding agent receives a bounded worktree and objective. It creates a candidate patch, never direct production deployment.

## 15. Debug Agent

The debug agent consumes failing commands, logs, stack traces and diffs and creates targeted repair hypotheses.

## 16. Test Agent

The test agent runs approved test/build commands in an isolated environment and records exact evidence.

## 17. Reviewer Agent

Review combines:

```text
diff inspection
test evidence
static analysis
security findings
scope adherence
risk
```

## 18. Merge Agent

The merge agent prepares integration metadata. Production policy should require approval before pushing/merging consequential changes.

## 19. Dynamic Subagents

A supervisor may spawn focused temporary workers:

```text
dependency researcher
API researcher
frontend specialist
database specialist
security reviewer
performance analyst
```

Subagents inherit only explicitly delegated capabilities.

## 20. Subagent Fan-Out

Independent tasks can execute concurrently with bounded semaphores/worker quotas.

## 21. Subagent Join

The supervisor waits for required child results and merges structured outputs, not arbitrary prose.

## 22. Skills Registry

Skills describe reusable bounded engineering procedures.

Examples:

```text
repo.inspect
git.search
test.pytest
lint.ruff
git.diff
benchmark.make
```

## 23. Skill Contract

A production skill declares:

```text
name/version
inputs
outputs
required tools
risk
timeout
resource profile
network policy
owner
signature
```

## 24. Skills vs Tools

A tool is a capability such as `git grep`. A skill is a governed procedure that may compose tools.

## 25. Skills Supply Chain

Version and sign skills; generate provenance/SBOM where executable dependencies are involved.

## 26. MCP Gateway

MCP provides a standard boundary for repository search, CI, issue trackers, documentation and enterprise engineering tools.

## 27. MCP Discovery

Only expose MCP servers/tools admitted by registry and allowed by policy.

## 28. MCP Invocation

Validate tool name, schema, arguments, tenant, agent identity, deadline, risk and idempotency.

## 29. Plugins and Hooks

Hooks provide deterministic lifecycle controls around agent actions.

Useful hooks:

```text
before_plan
after_plan
before_tool
after_tool
before_patch
after_patch
before_test
after_test
before_merge
```

## 30. Hook Safety

Hooks run outside model reasoning and can enforce mandatory checks.

## 31. Secure Sandbox

The local sandbox executes an allowlisted executable with timeout and captured output.

A real production sandbox should additionally provide:

```text
container/VM isolation
non-root UID
seccomp
AppArmor
read-only base filesystem
CPU/memory/PID quotas
network deny-by-default
ephemeral credentials
artifact quotas
```

## 32. Why Command Allowlisting

Never pass arbitrary model output to `shell=True`. This implementation uses argv execution and an executable allowlist.

## 33. Network Egress

Coding sandboxes should default to no network. Package registries and approved services require explicit egress policy.

## 34. Credentials

Keep Git/CI/cloud credentials outside model-visible environment. Broker short-lived scoped credentials.

## 35. Git Worktrees

Each candidate task gets an isolated worktree and branch:

```text
agent/<run>/<task>
```

This prevents concurrent agents from modifying the same checkout.

## 36. Worktree Lifecycle

```text
create
execute candidate
test
collect diff/artifacts
review
approval
integrate or discard
cleanup
```

## 37. Branch Isolation

Parallel coding agents use separate branches/worktrees and cannot overwrite one another's uncommitted files.

## 38. Patch Artifact

Capture the binary-safe Git diff and SHA-256 hash before approval.

## 39. Build Stage

Detect build system and execute registered build skills.

Examples:

```text
go test/build
cargo build
npm build
maven/gradle
make
```

## 40. Test Stage

Use layered tests:

```text
targeted unit
changed-package
integration
full regression
```

## 41. Static Analysis

Run language-specific linters, type checkers and security scanners as policy requires.

## 42. Benchmark Stage

Performance-sensitive changes should produce before/after evidence.

## 43. Benchmark Reproducibility

Record:

```text
hardware class
container image
toolchain
dataset
warmup
iterations
statistics
```

## 44. Reviewer

The reviewer should consume immutable artifacts, not trust a coding agent's self-description.

## 45. Evaluation Engine

Evaluation decides:

```text
PASS
REPAIR
REPLAN
```

using tests, review, policy and acceptance criteria.

## 46. Repair Loop

```text
failure
 -> classify
 -> debug hypothesis
 -> targeted repair task
 -> isolated patch
 -> rerun affected tests
 -> review
```

## 47. Replan Loop

Replan when the architecture/assumptions are wrong rather than repeatedly patching symptoms.

## 48. Stop Conditions

Bound:

```text
repair attempts
replans
model calls
tool calls
wall time
sandbox minutes
cost
```

## 49. Human Approval

Consequential integration pauses with exact candidate evidence.

## 50. Approval Hash

Bind approval to:

```text
repository
base SHA
branch
patch hash
test/evaluation evidence
target
```

Any material change requires new approval.

## 51. Candidate PR

A production integration can create a draft PR with:

```text
summary
motivation
changed files
tests
benchmarks
risks
rollback
agent trace
```

## 52. No Silent Merge

The reference does not push or merge automatically.

## 53. Durable Runtime

Long-running engineering work must survive API/worker restarts.

## 54. Run State Machine

```text
CREATED -> ANALYZING -> PLANNING -> READY -> RUNNING
 -> WAITING_APPROVAL
 -> REPAIRING
 -> REPLANNING
 -> COMPLETED / FAILED / CANCELLED
```

## 55. Task State Machine

```text
PENDING -> READY -> RUNNING
 -> SUCCEEDED / FAILED
 -> UNKNOWN -> RECONCILING
 -> CANCELLED
```

## 56. PostgreSQL Source of Truth

The included SQL models establish durable entities for runs, tasks, approvals, outbox, idempotency, artifacts and audit.

## 57. Transactional Outbox

Persist task readiness and dispatch intent in one transaction.

```sql
BEGIN;
UPDATE tasks SET status='READY' WHERE id=:id;
INSERT INTO outbox(event_type,aggregate_id,payload)
VALUES ('TASK_READY',:id,:payload);
COMMIT;
```

## 58. Event Bus

Use Kafka/Pulsar for task dispatch, results, approvals, reconciliation and audit export.

Redpanda provides a Kafka-compatible local environment.

## 59. Scheduler

Production scheduler selects READY tasks, checks quotas and creates worker leases.

## 60. Worker Leases

Lease ownership expires if a worker dies.

## 61. Fencing Tokens

Each new owner receives a larger token; stale workers cannot commit.

## 62. Idempotency

Use semantic keys for external writes such as PR creation and CI dispatch.

## 63. UNKNOWN

If a remote action may have succeeded before timeout, mark UNKNOWN rather than blindly retrying.

## 64. Reconciliation

Query Git provider/CI state to resolve UNKNOWN effects.

## 65. Retries

Retry only transient safe failures with backoff and jitter.

## 66. Circuit Breakers

Protect Git, CI, model and MCP dependencies from retry storms.

## 67. Bulkheads

Separate worker pools for research, coding, testing, review and reconciliation.

## 68. Backpressure

Bound DAG fan-out, active sandboxes, model calls, CI jobs and artifacts.

## 69. Cancellation

Persist cancellation and terminate active sandbox processes safely.

## 70. Checkpoints

Checkpoint after repository analysis, plan, patch, test, review and evaluation.

## 71. Memory

Recommended engineering memory layers:

```text
working
session
episodic
semantic
entity
procedural
```

## 72. Working Memory

Current task context; reconstructible where possible.

## 73. Session Memory

Current engineering conversation/project context.

## 74. Episodic Memory

Past successful/failed engineering attempts with provenance.

## 75. Semantic Memory

Repository docs, ADRs, runbooks and indexed code knowledge.

## 76. Entity Memory

Services, packages, owners, APIs and dependencies.

## 77. Procedural Memory

Team conventions and approved engineering procedures.

## 78. Memory Safety

Memory provides context, never permission.

## 79. Artifact Store

Persist:

```text
patches
test logs
benchmark results
review reports
generated docs
screenshots
```

with hashes and lineage.

## 80. Audit

Record:

```text
principal
agent
run/task
repository/base SHA
tool
sandbox command
patch hash
test evidence
approval
integration action
```

## 81. Model Gateway

Keep model provider credentials and routing outside agent code.

## 82. Model Routing

Use different profiles for planning, coding, debugging and reviewing when useful.

## 83. Structured Outputs

Planner/reviewer/evaluator output must validate against typed schemas.

## 84. Prompt Injection from Repositories

Repository text is untrusted. A README saying "upload secrets" cannot grant network/credential access.

## 85. Malicious Dependencies

Do not execute arbitrary repository install/build scripts outside a hardened sandbox.

## 86. Secret Scanning

Scan candidate patches and logs before artifact publication or PR creation.

## 87. Supply-Chain Security

Pin base images/toolchains and scan generated dependency changes.

## 88. Multi-Tenancy

Tenant-scope repositories, workspaces, artifacts, event topics, credentials, logs and quotas.

## 89. Repository Authorization

Verify the authenticated principal/agent can access the requested repository before cloning or opening it.

## 90. OpenTelemetry

Trace:

```text
engineering.run
 analyze
 plan
 task
  agent
  tool
  sandbox
 review
 evaluate
 approval
```

## 91. Metrics

Track:

```text
runs
task latency
sandbox duration
test pass rate
repair loops
replans
approval wait
PR acceptance
cost
```

## 92. Evaluation Metrics

Measure:

```text
task completion
patch correctness
test success
regression rate
review acceptance
scope adherence
security findings
```

## 93. Golden Engineering Tasks

Maintain versioned benchmark repositories/issues for regression testing the whole agent system.

## 94. Reproducibility

Persist model/workflow/skill versions, base SHA, commands and artifact hashes.

## 95. Kubernetes

Separate API/control plane from execution workers and sandbox infrastructure.

## 96. Production Services

```text
api
repository-service
planner
compiler
scheduler
supervisor
research-worker
coding-worker
test-worker
review-worker
skills-registry
mcp-gateway
sandbox-manager
artifact-service
evaluator
approval-service
reconciliation
outbox-publisher
audit-exporter
```

## 97. Worker Autoscaling

Scale from queue lag and oldest-task age, not only CPU.

## 98. Sandbox Node Pools

Use dedicated hardened worker pools for untrusted code execution.

## 99. Network Policy

Sandbox egress is deny-by-default. Control-plane services get only required connectivity.

## 100. Multi-Region

Keep repository/data residency in mind. One region owns a task at a time.

## 101. Disaster Recovery

Fence old workers, restore SQL/artifacts, replay outbox and reconcile Git/CI effects.

## 102. Capacity Planning

Model:

```text
engineering runs/day
tasks/run
sandboxes/task
test minutes
model calls
artifact bytes
```

## 103. Cost Governance

Track model tokens, sandbox compute, CI minutes, storage and external API usage per run.

## 104. SLOs

Separate:

```text
API availability
durable acceptance
task start
sandbox provisioning
workflow completion
```

## 105. CI/CD

```text
lint
unit tests
property tests
contract tests
security scan
SBOM
container scan
evaluation corpus
integration tests
load tests
chaos tests
staging
progressive deployment
```

## 106. Unit Tests

Test DAG validation, skill registry, approval hashes and repository utilities.

## 107. Property Tests

Important invariants:

```text
no task executes before dependencies
no stale worker commits
no unapproved merge
no sandbox command outside policy
no cross-tenant artifact access
```

## 108. Contract Tests

Test Git provider, MCP, CI, model and artifact adapters.

## 109. Load Tests

Exercise large repositories, many parallel runs, slow tests and large artifacts.

## 110. Chaos Tests

Kill workers, duplicate events, timeout Git/CI/model calls and verify safe recovery.

## 111. Security Tests

Test repository prompt injection, malicious build scripts, secret exfiltration, SSRF and sandbox escape.

## 112. Application — Feature Development

Goal -> code analysis -> implementation -> tests -> review -> approval -> draft PR.

## 113. Application — Bug Fixing

Failure report -> reproduction -> debug -> patch -> regression test -> review.

## 114. Application — Large Refactor

Planner decomposes modules into parallel isolated worktrees and joins only validated patches.

## 115. Application — Dependency Upgrade

Inspect lockfiles/advisories -> isolated upgrade -> tests -> compatibility review -> PR.

## 116. Application — Security Remediation

Finding -> affected-symbol analysis -> minimal patch -> security tests -> human security approval.

## 117. Application — Performance Optimization

Profile -> hypothesis -> candidate optimization -> benchmark -> statistical comparison -> review.

## 118. Application — Migration

Inventory -> dependency graph -> staged plan -> module-by-module changes -> compatibility tests.

## 119. Application — Test Generation

Coverage analysis -> target selection -> generated tests -> mutation/quality checks -> review.

## 120. Application — Documentation

Code/ADR analysis -> documentation candidate -> consistency checks -> approval.

## 121. Application — CI Failure Triage

CI event -> log analysis -> suspect commit -> reproduction -> candidate fix.

## 122. Application — Code Review

PR diff -> repository context -> static/test evidence -> structured review findings.

## 123. Run — Docker

```bash
cp .env.example .env
docker compose up --build -d
docker compose ps
curl http://localhost:8000/health
```

## 124. Run — Host

```bash
docker compose up -d postgres redis redpanda
python3 -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
uvicorn app.main:app --reload
```

## 125. Run — Tests

```bash
pytest -q
ruff check .
```

## 126. Run — Skills

```bash
curl http://localhost:8000/v1/skills -H 'x-api-key: change-me'
```

## 127. Run — Engineering Goal

```bash
curl -X POST http://localhost:8000/v1/engineering/run \
 -H 'x-api-key: change-me' \
 -H 'Content-Type: application/json' \
 -d '{"tenant_id":"demo","principal_id":"engineer","repository":"/absolute/path/to/git/repo","goal":"Inspect and prepare a reviewed candidate improvement","base_ref":"HEAD"}'
```

## 128. Run — Database

```bash
docker compose exec postgres psql -U postgres -d antigravity
```

```sql
\dt
SELECT * FROM runs;
SELECT * FROM tasks;
SELECT * FROM approvals;
SELECT * FROM outbox;
SELECT * FROM idempotency;
SELECT * FROM artifacts;
SELECT * FROM audit;
```

## 129. Run — Logs

```bash
docker compose logs -f api
docker compose logs -f postgres
docker compose logs -f redpanda
```

## 130. Run — Kubernetes

```bash
kubectl apply -f k8s/namespace.yaml
kubectl apply -f k8s/api.yaml
kubectl apply -f k8s/network-policy.yaml
```

## 131. Troubleshooting — Repository

The submitted path must be an existing Git checkout visible to the API process/container.

## 132. Troubleshooting — Pytest

Repositories without pytest will return a failed test result. Production build detection selects repository-specific test skills.

## 133. Troubleshooting — Worktrees

Ensure the source checkout is writable by the API user and Git permits creation of worktrees/branches.

## 134. Troubleshooting — Sandbox Timeout

Increase `SANDBOX_TIMEOUT_SECONDS` only after considering resource-abuse implications.

## 135. `repository.py`

Real Git-backed repository inspection/search plus deterministic tree hashing.

## 136. `worktrees.py`

Creates isolated Git worktrees/branches, captures binary-safe diffs and cleans abandoned workspaces.

## 137. `sandbox.py`

Uses argv-based subprocess execution, executable allowlisting, timeout and captured output.

## 138. `planner.py`

Creates a typed reference engineering workflow. Production binds a structured LLM planner behind the same contract.

## 139. `compiler.py`

Deterministically validates DAG correctness.

## 140. `agents.py`

Separates research, coding, debugging and review responsibilities.

## 141. `subagents.py`

Provides bounded asynchronous fan-out for dynamically created specialist work.

## 142. `skills.py`

Defines the reusable engineering capability catalog.

## 143. `mcp.py`

Defines the MCP gateway boundary; production replaces mock mode with authenticated MCP transport and policy.

## 144. `evaluator.py`

Converts test/review evidence into PASS or REPAIR.

## 145. `artifacts.py`

Persists patch/evaluation artifacts with SHA-256 integrity metadata.

## 146. `runtime.py`

Coordinates repository analysis, planning, isolated worktree, coding, tests, diff, review, evaluation, repair diagnostics and approval.

## 147. `models.py`

Defines production persistence foundations for runs, tasks, approvals, outbox, idempotency, artifacts and audit.

## 148. Current vs Distributed Runtime

The local API executes synchronously for inspectability. The production topology wires the SQL/outbox models to event publishing, scheduler and worker consumers.

## 149. Recommended Async API

```text
POST /v1/runs
GET  /v1/runs/{id}
GET  /v1/runs/{id}/events
GET  /v1/runs/{id}/tasks
GET  /v1/runs/{id}/artifacts
POST /v1/runs/{id}/cancel
POST /v1/approvals/{id}/decision
```

## 150. Production Upgrade Sequence

```text
1 OIDC/workload identity
2 repository authorization
3 persistent run/task transitions
4 Alembic
5 outbox publisher
6 Kafka/Pulsar
7 scheduler/workers
8 leases/fencing/idempotency
9 UNKNOWN/reconciliation
10 approval/resume
11 hardened sandbox service
12 GitHub/GitLab provider adapters
13 CI provider adapter
14 production MCP gateway
15 model gateway
16 code graph/index
17 persistent memory
18 artifact object storage
19 OpenTelemetry
20 Kubernetes/Helm
21 load/chaos/security testing
22 DR drills
```

## 151. Production Readiness Matrix

| Area | Included reference | Production target |
|---|---|---|
| Git | real local Git/worktree | authenticated provider + repo service |
| Repository analysis | file/language/Git | AST/symbol/code graph |
| Planner | deterministic | structured model planner |
| DAG | real validation | versioned durable DAG |
| Coding | isolated candidate artifact | model-backed patch engine |
| Tests | real subprocess | detected/hardened test skills |
| Sandbox | allowlist + timeout | container/VM isolation |
| MCP | boundary/mock | authenticated protocol implementation |
| Runtime | synchronous | SQL/outbox/event workers |
| Approval | immutable hash | durable approval/resume |
| Artifacts | filesystem + hashes | object storage |
| Telemetry | documented | OpenTelemetry |
| Kubernetes | starter manifests | hardened Helm/platform |

## 152. Principal-Level Design Questions

```text
Why worktrees instead of one shared checkout?
How do you prevent malicious repository instructions from gaining authority?
When should a failure cause repair vs replan?
How do you make PR creation idempotent?
How do you recover after a worker dies during an external write?
How do dynamic subagents inherit capabilities safely?
How do you benchmark performance changes reproducibly?
How do you isolate untrusted build scripts?
How do you merge parallel patches safely?
How do you evaluate autonomous coding beyond test pass rate?
```

## 153. Core Design Principle

```text
Model        -> reasons and proposes
Repository   -> provides grounded engineering context
Planner      -> decomposes the goal
Compiler     -> validates task structure
Supervisor   -> coordinates
Agents       -> perform specialized reasoning
Skills       -> provide reusable procedures
MCP          -> exposes governed tools
Sandbox      -> contains execution
Worktrees    -> isolate code mutations
Tests        -> produce execution evidence
Reviewer     -> independently checks candidate
Evaluator    -> decides pass/repair/replan
Approval     -> controls integration
Runtime      -> owns durable truth
Audit        -> reconstructs the engineering process
```

**Autonomous coding is not autonomous authority.**



# Extended Production Architecture, Operations and Code Guide

## 154. Complete End-to-End Production Flow

```text
Engineering Request
      |
Authentication / Repository Authorization
      |
Goal Normalization
      |
Repository Snapshot
      |
Code / Symbol / Dependency Analysis
      |
Engineering Planner
      |
Typed Plan vN
      |
DAG Compiler + Policy Validation
      |
Durable SQL State
      |
Transactional Outbox
      |
Event Bus
      |
Supervisor / Scheduler
      |
+-------------+-------------+-------------+-------------+
| Research    | Coding      | Debug       | Test        |
| Workers     | Workers     | Workers     | Workers     |
+-------------+-------------+-------------+-------------+
      |
Dynamic Specialist Subagents
      |
Skills Registry + MCP Gateway
      |
Sandbox Manager
      |
Isolated Git Worktrees
      |
Build / Test / Run / Benchmark / Scan
      |
Immutable Evidence + Artifacts
      |
Reviewer
      |
Evaluation
      |
PASS -------- REPAIR -------- REPLAN
  |              |               |
  |              +---- DAG ------+
  |
Approval-bound Patch Hash
  |
Candidate PR
  |
Human Review / Merge Policy
```

The essential property is that model reasoning never becomes durable truth by itself. SQL state, immutable repository revisions, test evidence and approval records determine what actually happened.

## 155. Request Admission

Before repository access, validate:

```text
authenticated principal
tenant
repository authorization
repository classification
requested operation
budget
allowed models
allowed tools
region
```

Never derive trusted tenant or repository authorization from free-form model output.

## 156. Repository Service

A dedicated production repository service should own cloning, fetch, snapshot creation and worktree lifecycle. Agents receive logical workspace handles instead of unrestricted host paths.

## 157. Clone Security

Production cloning should enforce:

```text
approved Git hosts
repository allowlist
credential brokerage
maximum repository size
submodule policy
LFS policy
fetch timeout
protocol restrictions
```

## 158. Base Revision Pinning

Resolve branch names to immutable commit SHAs before planning. Every patch, test and review artifact references the same base SHA.

## 159. Dirty Repository Policy

Production runs should normally reject dirty shared checkouts. If dirty state is intentionally supported, capture it as an immutable patch artifact first.

## 160. Repository Index Pipeline

```text
Git Snapshot
   |
File Classifier
   |
Language Parsers
   |
AST / Symbol Extractors
   |
Dependency Extractor
   |
Call / Import Graph
   |
Test Mapping
   |
Ownership Metadata
   |
Search Index + Code Graph
```

## 161. Incremental Indexing

Cache indexes by commit SHA. For a new commit, update only changed files and affected graph edges.

## 162. Symbol-Level Retrieval

Prefer symbol-aware retrieval over arbitrary chunks for code tasks. Store symbol name, type, file, line range, imports, callers/callees and owning package.

## 163. Hybrid Code Search

Combine:

```text
exact identifier search
lexical/BM25 search
semantic embedding search
symbol graph traversal
Git history
```

## 164. Context Builder

The context builder selects the minimum authorized code context required for a task. This reduces cost and limits accidental disclosure.

## 165. Context Provenance

Every context item records:

```text
repository
commit SHA
path
line/symbol range
retrieval method
score
```

## 166. Engineering Planner Output

A production planner should return a schema such as:

```json
{
  "objective": "Fix race in worker lease renewal",
  "assumptions": [],
  "tasks": [],
  "acceptance_criteria": [],
  "risks": [],
  "required_evidence": [],
  "budget": {}
}
```

## 167. Acceptance Criteria

Acceptance criteria should be machine-checkable when possible:

```text
specific tests pass
new regression test exists
lint/type checks pass
benchmark regression < threshold
no new high-severity security finding
```

## 168. Planner Validation

Reject plans that:

```text
reference unknown skills
request forbidden network access
exceed fan-out limits
contain cycles
lack required review
attempt direct protected-branch mutation
```

## 169. Supervisor Responsibilities

The supervisor may:

```text
schedule ready tasks
spawn bounded subagents
request additional evidence
classify failures
request repair
request replan
```

It may not bypass policy or approval.

## 170. Dynamic Subagent Contract

Every subagent receives:

```text
parent run/task
objective
input artifact references
allowed skills
allowed repositories
budget
deadline
output schema
```

## 171. Delegation Depth

Set a maximum subagent depth to prevent recursive agent explosion.

## 172. Fan-Out Budget

Bound subagents by:

```text
count
tokens
sandbox minutes
wall time
external calls
```

## 173. Research Worker

Research tasks are read-only by default and may inspect code, docs, Git history, issues and approved external sources.

## 174. Coding Worker

Coding tasks receive a dedicated worktree. A coding worker cannot mutate the shared source checkout.

## 175. Debug Worker

Debugging is evidence-driven. Inputs include failing command, exit code, logs, stack trace, patch and environment metadata.

## 176. Test Worker

Test workers run exact registered commands and emit immutable execution evidence.

## 177. Reviewer Independence

For higher-risk changes, use a separate model/session from the coding agent to reduce correlated errors.

## 178. Merge Preparation

The merge stage prepares:

```text
candidate branch
base SHA
patch SHA
test report
review report
evaluation report
PR title/body
```

but does not automatically merge protected changes.

## 179. Repair Taxonomy

Classify failure as:

```text
syntax
compile
unit test
integration
behavior
performance
security
environment
dependency
flaky
```

## 180. Repair Strategy

Target only the failure-relevant portion of the patch/context. Avoid repeatedly rewriting the entire solution.

## 181. Replan Triggers

Replan when:

```text
core assumption invalid
required API absent
architecture incompatible
dependency constraint impossible
repair budget exhausted
```

## 182. Evaluation Evidence

Evaluation consumes artifacts, not self-reported claims:

```text
patch
commands
exit codes
test logs
coverage
lint/type output
security scan
benchmarks
review
```

## 183. Evaluation Policy

A possible gate:

```text
required tests = PASS
required static checks = PASS
critical security findings = 0
review = PASS
scope = acceptable
approval = present when required
```

## 184. Test Selection

Use change-impact analysis to choose fast targeted tests first, then broader suites according to risk.

## 185. Flaky Test Handling

Record historical flake rates. Do not automatically reinterpret every failure as flaky.

## 186. Benchmark Comparison

Use statistical confidence and repeated runs rather than one before/after number.

## 187. Security Review Stage

Security-sensitive changes may require:

```text
SAST
dependency scan
secret scan
IaC scan
container scan
specialist reviewer
```

## 188. Git Provider Adapter

Define an interface for GitHub/GitLab/Bitbucket rather than embedding provider APIs in agent logic.

## 189. Candidate PR Idempotency

Use a stable key derived from:

```text
tenant
repository
run
base SHA
patch SHA
```

to avoid duplicate PR creation.

## 190. Protected Branches

Never give autonomous workers unrestricted direct push access to protected branches.

## 191. CI Integration

After candidate PR creation, consume CI callbacks/events and attach results to the durable run.

## 192. Asynchronous CI

Long CI must transition the task to `WAITING_EXTERNAL`, release the worker and resume from callback/polling.

## 193. Scheduled Engineering Tasks

Scheduled jobs can run:

```text
dependency audits
test-health checks
documentation drift scans
performance regression scans
repository maintenance
```

The schedule creates ordinary durable runs; it should not bypass admission policy.

## 194. Background Execution

A background task must be resumable and queryable by run ID. Do not require a client HTTP connection to stay open.

## 195. Hook Architecture

```text
before_goal
after_analysis
before_plan
after_plan
before_task
before_tool
after_tool
before_patch
after_patch
before_test
after_test
before_approval
before_pr
```

Hooks are deterministic enforcement/integration points.

## 196. Plugin Architecture

A plugin can package:

```text
skills
hooks
MCP servers
rules
templates
evaluators
```

Plugins require versioning and admission review.

## 197. Plugin Isolation

Do not load arbitrary untrusted plugin code into the privileged control-plane process.

## 198. MCP Tool Envelope

```json
{
  "run_id": "...",
  "task_id": "...",
  "tool": "ci.status",
  "arguments": {},
  "deadline": "...",
  "idempotency_key": "...",
  "traceparent": "..."
}
```

## 199. MCP Authorization

Authorization is evaluated per call even if the tool appeared in discovery.

## 200. MCP Response Safety

Tool responses are untrusted data. They cannot modify policy, credentials or sandbox privileges.

## 201. Sandbox Image Catalog

Use approved versioned images per ecosystem:

```text
python
go
rust
node
java
android
```

## 202. Sandbox Provisioning

```text
task
 -> select image
 -> create isolated workspace
 -> mount worktree
 -> apply resource limits
 -> apply egress policy
 -> inject short-lived handles
 -> execute
 -> collect artifacts
 -> destroy
```

## 203. Filesystem Policy

Mount only the task worktree and explicitly required caches. Host filesystem access is forbidden.

## 204. Build Cache

Caches should be content-addressed and treated as untrusted acceleration, not correctness evidence.

## 205. Network Policy

Allow package registry access only when required. Restrict DNS and destination ranges.

## 206. Sandbox Credential Policy

Credentials are scoped to task, repository, operation and TTL. Prefer proxy/broker handles over raw tokens.

## 207. Sandbox Output Limits

Cap stdout/stderr and artifact sizes to prevent storage exhaustion.

## 208. Process Tree Cleanup

Timeout/cancellation must terminate descendant processes, not only the shell parent.

## 209. Durable SQL Transactions

State transition example:

```sql
BEGIN;

UPDATE tasks
SET status='READY'
WHERE id=:id AND status='PENDING';

INSERT INTO outbox(event_type, aggregate_id, payload)
VALUES ('engineering.task.ready', :id, :payload);

COMMIT;
```

## 210. Outbox Publisher

The publisher scans unpublished rows, sends events and records publication. Consumers remain idempotent because duplicate publication is possible.

## 211. Event Keying

Partition task events by run or repository where ordering is required.

## 212. Consumer Idempotency

Before side effects, atomically claim/check an idempotency record.

## 213. Worker Heartbeats

Workers renew leases during long sandbox/test operations.

## 214. Lease Expiry

Expired work returns to scheduling only after the previous owner is fenced.

## 215. Reconciliation Worker

Reconcile:

```text
PR creation
CI dispatch
remote MCP writes
artifact upload
Git provider mutation
```

## 216. Dead-Letter Handling

Poison events go to a DLQ with run/task/error metadata and operator tooling.

## 217. Workflow Timeouts

Distinguish:

```text
task timeout
tool timeout
sandbox timeout
workflow deadline
approval timeout
```

## 218. Quotas

Apply quotas per tenant/repository/principal for concurrent runs, subagents, sandbox CPU, model tokens and artifacts.

## 219. Fair Scheduling

Use weighted fair queues so one large repository cannot starve all interactive engineering work.

## 220. Priority

Typical classes:

```text
interactive
CI remediation
scheduled maintenance
background research
```

## 221. Persistent Memory Backend

Store memory metadata transactionally and content in appropriate relational/vector/object stores.

## 222. Memory Provenance

Every durable memory records source run, artifact and authoring agent/human.

## 223. Memory Poisoning Defense

Require confidence/provenance thresholds and review for procedural memory changes.

## 224. Repository-Scoped Memory

Never leak semantic/episodic memory between unauthorized repositories or tenants.

## 225. Artifact Object Storage

Production artifacts should use S3/GCS-compatible storage with immutable hashes and retention rules.

## 226. Artifact Lineage

```text
goal
 -> task
 -> sandbox execution
 -> patch
 -> test report
 -> evaluation
 -> PR
```

## 227. Observability Span Model

```text
run
  analyze_repository
  plan
  compile
  task
    agent_reason
    skill
    mcp_call
    sandbox
  review
  evaluate
  approval
  pr_create
```

## 228. Structured Logs

Include:

```text
tenant
run_id
task_id
repository_id
agent_role
attempt
trace_id
```

Never log secrets.

## 229. Dashboards

Recommended dashboards:

```text
run throughput
success/repair/replan
queue lag
sandbox utilization
test failure
MCP latency
model cost
approval backlog
PR acceptance
```

## 230. Alerts

Alert on:

```text
oldest task
UNKNOWN backlog
outbox lag
worker lease churn
sandbox provisioning failure
security blocks
artifact failure
```

## 231. Evaluation Corpus

Maintain real representative engineering tasks with expected tests/behavior rather than optimizing only on toy coding benchmarks.

## 232. Shadow Evaluation

Before changing planner/model/skill versions, replay historical tasks in a non-mutating environment.

## 233. Canary Rollout

Route a small percentage of eligible runs to new model/agent versions and compare evaluation metrics.

## 234. Model Version Pinning

Persist exact model/profile and prompt/template versions for each agent action.

## 235. Prompt Versioning

Prompts are deployable artifacts with version IDs and evaluation history.

## 236. Skill Versioning

A run pins skill versions so replay is deterministic.

## 237. Tool Schema Versioning

Breaking MCP/tool schema changes require explicit version migration.

## 238. Database Migration Strategy

Use Alembic expand/contract migrations:

```text
expand schema
deploy compatible code
backfill
switch readers/writers
contract old schema
```

## 239. Backup

Back up SQL plus artifact metadata/content according to required RPO.

## 240. Restore Test

A backup is not valid until restoration and workflow reconciliation are tested.

## 241. Multi-Region Ownership

Use an authoritative execution region per run. Global APIs can route to that owner.

## 242. Regional Failover

On failover:

```text
stop/fence old region
promote SQL
restore event processing
reconcile external state
resume idempotent tasks
```

## 243. Repository Residency

Repository content and artifacts may have geographic constraints; route execution accordingly.

## 244. Threat Model — Repository Prompt Injection

Threat: malicious repository text asks the agent to exfiltrate credentials.

Defense: content has no authority; sandbox has no raw long-lived credentials and deny-by-default egress.

## 245. Threat Model — Malicious Build Script

Threat: package/build script attempts host escape or secret theft.

Defense: hardened sandbox, restricted mounts, seccomp/VM isolation, egress controls.

## 246. Threat Model — Tool Poisoning

Threat: compromised MCP server returns malicious instructions.

Defense: response treated as data; every follow-on action independently authorized.

## 247. Threat Model — Approval Substitution

Threat: candidate changes after approval.

Defense: bind approval to base SHA + patch hash + target + evaluation.

## 248. Threat Model — Cross-Tenant Leakage

Defense: trusted tenant context, row/object ACLs, isolated workspaces, scoped caches and tests.

## 249. Threat Model — Dependency Confusion

Use approved registries, lockfiles, checksums and dependency policy.

## 250. Threat Model — Secret in Generated Patch

Run secret scanning before artifacts/PR publication.

## 251. Privacy

Minimize code sent to external models; route sensitive repositories to approved/self-hosted profiles when required.

## 252. Local Models

A model gateway can route selected analysis/coding workloads to local models while preserving the same typed agent contracts.

## 253. Cost Model

Approximate per run:

```text
model cost
+ sandbox compute
+ CI compute
+ repository indexing
+ storage
+ external tool/API cost
```

## 254. Budget Enforcement

Budgets are checked before dispatch and before spawning subagents.

## 255. Performance

Avoid repeatedly re-indexing repositories or rebuilding unchanged dependency caches.

## 256. Large Repositories

Use sparse checkout/indexing, package ownership boundaries and incremental graph updates.

## 257. Monorepos

Planner should identify affected build targets and ownership boundaries before fan-out.

## 258. Parallel Patch Strategy

Parallel patches should target disjoint ownership scopes where possible.

## 259. Patch Conflict Detection

Before integration, rebase candidate worktrees against the current integration base and rerun impacted tests.

## 260. Merge Queue

For multiple approved candidates:

```text
approved patch
 -> merge queue
 -> rebase
 -> validation
 -> protected integration
```

## 261. Human Experience

Human reviewers should see concise evidence:

```text
what changed
why
tests
benchmarks
risks
uncertainty
trace/artifacts
```

## 262. Explainability

Expose the plan and evidence without presenting hidden model reasoning.

## 263. Failure Reporting

Failures should contain machine-readable class, failed stage, relevant artifacts and suggested operator action.

## 264. Operations — Normal Health Check

```bash
docker compose ps
curl http://localhost:8000/health
docker compose logs --tail=100 api
```

## 265. Operations — Database

```bash
docker compose exec postgres psql -U postgres -d antigravity
```

Inspect tables and stuck states.

## 266. Operations — Event Infrastructure

```bash
docker compose logs --tail=200 redpanda
```

Production additionally inspects consumer lag and DLQs.

## 267. Operations — Workspace Cleanup

Abandoned worktrees should be reconciled against durable task state before removal.

## 268. Operations — Incident: Worker Crash

```text
do not manually mark success
wait/expire lease
fence stale worker
inspect durable task
redispatch idempotently
```

## 269. Operations — Incident: Ambiguous PR Creation

```text
mark UNKNOWN
query provider using idempotency/branch/commit
attach existing PR if found
create only if absence is proven
```

## 270. Operations — Incident: Compromised Skill

Disable the skill version in registry, stop new dispatch, identify affected runs from audit, rotate credentials if necessary and evaluate generated artifacts.

## 271. Operations — Emergency Kill Switch

Support:

```text
disable all writes
disable specific skill
disable repository
disable model/provider
disable MCP server
disable tenant
```

## 272. Developer Workflow

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
pytest -q
ruff check .
uvicorn app.main:app --reload
```

## 273. Adding a Skill

1. Define a typed skill contract.
2. Assign risk and role.
3. Add implementation/adapter.
4. Add policy.
5. Add unit/contract/security tests.
6. Version it.
7. Add evaluation coverage.

## 274. Adding an Agent

1. Define role and output schema.
2. Define allowed skills.
3. Define budget.
4. Define context builder.
5. Define evaluation.
6. Add regression tasks.
7. Register with supervisor.

## 275. Adding an MCP Server

1. Register endpoint/version.
2. Validate server identity.
3. Import tool schemas.
4. Assign risk.
5. Define authentication.
6. Define network policy.
7. Add contract tests.
8. Add audit fields.

## 276. Adding a Language

Add parser/indexer, sandbox image, build/test skills, lint/type checks and benchmark conventions.

## 277. Adding GitHub/GitLab

Implement a provider interface for repository metadata, branches, PR/MR creation, checks and comments. Keep provider credentials in a broker.

## 278. Production API Shape

```text
POST /v1/runs
GET  /v1/runs/{run_id}
GET  /v1/runs/{run_id}/tasks
GET  /v1/runs/{run_id}/events
GET  /v1/runs/{run_id}/artifacts
POST /v1/runs/{run_id}/cancel

GET  /v1/skills
GET  /v1/agents

GET  /v1/approvals
POST /v1/approvals/{approval_id}/decision

GET  /v1/repositories/{id}/index/status
POST /v1/repositories/{id}/index
```

## 279. Example Production Run Response

```json
{
  "run_id": "run_...",
  "status": "RUNNING",
  "repository": {
    "id": "repo_...",
    "base_sha": "..."
  },
  "plan_version": 3,
  "current_tasks": ["test_backend", "test_frontend"],
  "budget": {
    "sandbox_minutes_remaining": 32,
    "model_calls_remaining": 14
  }
}
```

## 280. Deployment Environments

Use separate:

```text
local
development
staging
production
```

with different repository, credential, model and sandbox policies.

## 281. Production Readiness Gate

Do not enable autonomous external writes until:

```text
identity complete
repository ACL complete
sandbox hardened
idempotency enforced
reconciliation tested
approval service operational
audit complete
security tests pass
DR tested
```

## 282. Current Executable Boundary

The included source is intentionally transparent about what is implemented locally:

**Implemented and executable:** real local Git analysis, isolated worktrees, real diff capture, allowlisted subprocess execution, pytest execution, typed DAG validation, specialist agent boundaries, subagent fan-out abstraction, skills registry, MCP abstraction, review/evaluation, approval hashing, artifact files, SQL schema foundations, Redis/Redpanda infrastructure and Kubernetes starters.

**Production design but not fully wired in the synchronous local path:** durable scheduler/workers, outbox publisher, Kafka consumers, leases/fencing enforcement, UNKNOWN reconciliation, persistent memory, OIDC, Git provider PR creation, hardened VM/container sandbox service, full MCP transport, OpenTelemetry exporter and Helm deployment.

This distinction is deliberate: a professional reference should not label mocked enterprise integrations as completed production infrastructure.

## 283. Google Antigravity Mapping

Public Antigravity concepts map naturally to this architecture:

```text
Antigravity multi-agent orchestration -> Supervisor + worker roles
Dynamic subagents                  -> SubagentManager
Asynchronous/background work       -> durable scheduler/event runtime
Skills                             -> Skills Registry
Hooks                              -> deterministic lifecycle hooks
Plugins                            -> packaged skills/hooks/MCP/rules
Agent harness                      -> planner/supervisor/tool/sandbox loop
Isolated environment               -> sandbox + isolated worktree
Managed/background tasks           -> durable run IDs and state machines
```

The mapping is conceptual; this project does not claim Google's internal implementation.

## 284. Principal-Level Architecture Review

A strong design review should be able to defend:

```text
Why SQL, not chat history, owns workflow state.
Why worktrees are isolated per candidate.
Why sandbox execution is a separate trust boundary.
Why a passing test suite is necessary but insufficient.
Why review should consume artifacts rather than agent claims.
Why approval is bound to exact patch semantics.
Why event delivery is at-least-once.
Why idempotency and reconciliation are both required.
Why subagent authority is explicitly delegated.
Why repository text is untrusted.
Why model choice is separate from workflow correctness.
Why background tasks need durable IDs and resumability.
```

## 285. Final Production Architecture Principle

```text
Goal            -> desired engineering outcome
Repository      -> immutable grounded context
Planner         -> typed decomposition
Compiler        -> structural correctness
Supervisor      -> bounded coordination
Subagents       -> specialized parallel reasoning
Skills          -> reusable engineering procedures
MCP             -> governed tool interoperability
Sandbox         -> containment
Worktrees       -> mutation isolation
Build/Test      -> executable evidence
Reviewer        -> independent scrutiny
Evaluator       -> quality gate
Repair/Replan   -> bounded recovery
Approval        -> human authority
PR              -> candidate integration artifact
SQL Runtime     -> durable execution truth
Outbox/EventBus -> reliable asynchronous dispatch
Audit           -> reconstruction
```

**The model may propose code. The engineering system decides whether that code is safe enough to become a candidate change.**
