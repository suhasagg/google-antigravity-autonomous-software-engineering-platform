# Runbook

```bash
cp .env.example .env
docker compose up --build -d
curl http://localhost:8000/health
pytest -q
```

For actual engineering runs, use host mode or mount an authorized Git checkout into the API container.
