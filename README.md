# LMS Data Pipeline & Analytics Dashboard

An ETL pipeline and analytics dashboard for a learning management system. Fetches data from external APIs, aggregates it in PostgreSQL, and visualizes insights in a React frontend.

## Features

- ETL pipeline: extract from external API, transform, load into PostgreSQL
- Incremental sync with idempotent upserts
- SQL analytics endpoints (GROUP BY, COUNT, AVG, CASE WHEN)
- React dashboard with Chart.js visualizations
- Grafana integration (optional)

## Tech stack

**Backend:** Python, FastAPI, PostgreSQL, SQLAlchemy  
**Frontend:** React, Chart.js, Vite  
**Data:** ETL scripts, aggregation queries  
**DevOps:** Docker, Docker Compose

## Quick start

```bash
cp .env.docker.example .env.docker.secret
docker compose up --build
```

## Project structure

- `backend/` — ETL + API
- `frontend/` — Dashboard UI
- `docker-compose.yml` — full stack
