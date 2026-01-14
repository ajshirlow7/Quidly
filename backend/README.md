# Quidly Pricing Backend

FastAPI-based microservice that polls UK retailer listings, normalises prices, and serves the React app via a JSON API.

## Key capabilities

- Modular fetchers: each retailer implements `RetailerFetcher` so you can swap between authenticated APIs, HTML scrapers, or partner feeds.
- Background refresh: a configurable worker polls every `PRICE_REFRESH_SECONDS` and stores the latest quotes in-memory (ready for you to swap to Redis/Postgres).
- HTTP API: `GET /consoles` returns all current offers, `GET /consoles/{id}` drills into a single console, and `POST /refresh` triggers an on-demand crawl.
- Operational visibility: `/health` exposes heartbeat info, while structured logging makes it easy to send events to Application Insights or CloudWatch.

## Quick start

```bash
cd backend
python -m venv .venv
. .venv/Scripts/activate  # PowerShell: .venv\Scripts\Activate.ps1
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Environment variables (optional, loaded via `.env` if present):

| Variable | Default | Description |
| --- | --- | --- |
| `PRICE_REFRESH_SECONDS` | `900` | Interval between automatic refresh cycles (in seconds). |
| `MAX_CONCURRENT_REQUESTS` | `4` | Upper bound for simultaneous retailer fetches. |
| `HTTP_TIMEOUT_SECONDS` | `12` | Timeout per outbound retailer request. |
| `SCRAPER_USER_AGENT` | `QuidlyBot/0.1 (+https://quidly.local/pricing)` | Identifies your crawler; set this to something contactable. |
| `ENABLE_JSON_LD_FALLBACK` | `true` | When true, the HTML fetcher parses JSON-LD offer metadata if CSS selectors fail. |

> ⚠️ **Legal + ethical reminder**: respect each retailer's terms of service and robots.txt, implement polite rate limits, and prefer official affiliate/API feeds whenever available.

## Project layout

```
backend/
  app/
    config.py          # Settings + environment handling
    data.py            # Console + retailer metadata
    main.py            # FastAPI entrypoint
    schemas.py         # Pydantic response/request models
    store.py           # In-memory cache of the latest quotes
    retailers/
      base.py          # Fetcher contract + helpers
      html.py          # Generic HTML/JSON-LD scraper implementation
    services/
      price_service.py # Orchestrates fetchers and persistence
      refresh.py       # Background scheduler wiring
```

## Extending fetchers

1. Add retailer metadata in `app/data.py` (CSS selectors, shipping text, etc.).
2. Implement a fetcher in `app/retailers/*.py` if the HTML helper is insufficient (e.g., when OAuth or signed requests are required).
3. Register the fetcher in `FETCHER_REGISTRY` (see `price_service.py`).
4. Run `POST /refresh` (or restart the worker) to pull live data.

## Frontend integration

The React app can read real-time prices by pointing `VITE_API_URL` at this service (defaults to `http://localhost:8000`). You can keep the static mock catalog as a fallback if the backend is offline.
