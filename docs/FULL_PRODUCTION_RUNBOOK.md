# Full Production Runbook

## Start local services
```bash
cp .env.example .env
docker compose up --build -d
docker compose ps
curl http://localhost:8000/health
```

## Validate
```bash
pytest -q
ruff check .
```

## Incident priorities
1. Stop unsafe dispatch.
2. Preserve PostgreSQL workflow truth.
3. Fence stale workers.
4. Preserve worktree/artifact evidence.
5. Reconcile ambiguous external effects.
6. Replay unpublished outbox events.
7. Resume only idempotent work.
