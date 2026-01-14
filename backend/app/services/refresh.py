from __future__ import annotations

import asyncio
import logging
from datetime import datetime

from fastapi import FastAPI

from ..config import settings
from .price_service import price_service

logger = logging.getLogger(__name__)


class RefreshLoop:
    def __init__(self) -> None:
        self._task: asyncio.Task | None = None
        self._stop_event = asyncio.Event()

    async def start(self) -> None:
        if self._task and not self._task.done():
            return
        self._stop_event.clear()
        self._task = asyncio.create_task(self._run())

    async def stop(self) -> None:
        if self._task:
            self._stop_event.set()
            await self._task
            self._task = None

    async def _run(self) -> None:
        while not self._stop_event.is_set():
            try:
                refreshed, failed = await price_service.refresh_all()
                logger.info(
                    "Price refresh completed", extra={"refreshed": refreshed, "failed": failed, "at": datetime.utcnow().isoformat()}
                )
            except Exception as exc:  # pylint: disable=broad-except
                logger.exception("Price refresh failed: %s", exc)
            finally:
                try:
                    await asyncio.wait_for(self._stop_event.wait(), timeout=settings.price_refresh_seconds)
                except asyncio.TimeoutError:
                    continue


refresh_loop = RefreshLoop()


def register_background_tasks(app: FastAPI) -> None:
    @app.on_event("startup")
    async def _startup() -> None:  # noqa: WPS430
        await refresh_loop.start()

    @app.on_event("shutdown")
    async def _shutdown() -> None:  # noqa: WPS430
        await refresh_loop.stop()
