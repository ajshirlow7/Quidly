from __future__ import annotations

from datetime import datetime

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from .schemas import ConsoleCollection, ConsolePrice, RefreshResponse
from .services.price_service import price_service
from .services.refresh import register_background_tasks
from .store import store

app = FastAPI(title="Quidly Pricing API", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

register_background_tasks(app)


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok", "timestamp": datetime.utcnow().isoformat()}


@app.get("/consoles", response_model=ConsoleCollection)
async def list_consoles() -> ConsoleCollection:
    consoles = store.list_consoles()
    if not consoles:
        await price_service.refresh_all()
        consoles = store.list_consoles()
    return ConsoleCollection(consoles=consoles, refreshed_at=datetime.utcnow())


@app.get("/consoles/{console_id}", response_model=ConsolePrice)
async def get_console(console_id: str) -> ConsolePrice:
    console = store.get_console(console_id)
    if not console:
        raise HTTPException(status_code=404, detail="Console not found")
    return console


@app.post("/refresh", response_model=RefreshResponse)
async def trigger_refresh() -> RefreshResponse:
    refreshed, failed = await price_service.refresh_all()
    return RefreshResponse(refreshed=refreshed, failed=failed, completed_at=datetime.utcnow())
