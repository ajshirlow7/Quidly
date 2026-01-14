from __future__ import annotations

import asyncio
import logging
from collections import defaultdict
from datetime import datetime
from typing import Dict, List, Tuple, Type

from ..config import settings
from ..data import CONSOLE_CATALOG, ConsoleDefinition, RetailerTarget
from ..schemas import ConsolePrice, RetailerQuote
from ..store import store
from ..retailers.base import RetailerFetcher
from ..retailers.html import HtmlRetailerFetcher

logger = logging.getLogger(__name__)

FETCHER_REGISTRY: Dict[str, Type[RetailerFetcher]] = {}
DEFAULT_FETCHER: Type[RetailerFetcher] = HtmlRetailerFetcher


class PriceService:
    def __init__(self) -> None:
        self._semaphore = asyncio.Semaphore(settings.max_concurrent_requests)

    async def refresh_all(self) -> Tuple[int, int]:
        tasks = []
        for console in CONSOLE_CATALOG:
            for target in console.retailers:
                tasks.append(self._fetch_with_lock(console, target))

        results = await asyncio.gather(*tasks, return_exceptions=True)

        grouped: Dict[str, List[RetailerQuote]] = defaultdict(list)
        refreshed = 0
        failed = 0

        for result in results:
            if isinstance(result, RetailerQuote):
                grouped[result.console_id].append(result)
            else:
                failed += 1

        for console in CONSOLE_CATALOG:
            quotes = grouped.get(console.console_id, [])
            if not quotes:
                continue
            quotes.sort(key=lambda quote: quote.price)
            store.replace_console(
                ConsolePrice(
                    console_id=console.console_id,
                    console_name=console.console_name,
                    base_specs=console.base_specs,
                    retailers=quotes,
                    cheapest_price=quotes[0].price if quotes else None,
                    cheapest_retailer=quotes[0].retailer_name if quotes else None,
                )
            )
            refreshed += 1

        return refreshed, failed

    async def _fetch_with_lock(self, console: ConsoleDefinition, target: RetailerTarget):
        if target.requires_session:
            logger.warning("Skipping %s for %s: requires authenticated feed", target.retailer_name, console.console_name)
            raise RuntimeError("requires authenticated session or API key")

        async with self._semaphore:
            fetcher_cls = FETCHER_REGISTRY.get(target.retailer_id, DEFAULT_FETCHER)
            fetcher = fetcher_cls(target, console)
            try:
                quote = await fetcher.fetch()
                if not quote:
                    raise RuntimeError(f"Unable to parse price for {target.retailer_name}")
                return quote
            finally:
                if hasattr(fetcher, "close"):
                    await getattr(fetcher, "close")()


price_service = PriceService()
