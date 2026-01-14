from __future__ import annotations

import abc
from datetime import datetime
from typing import Optional

from ..config import settings
from ..data import ConsoleDefinition, RetailerTarget
from ..schemas import RetailerQuote


class RetailerFetcher(abc.ABC):
    slug: str

    def __init__(self, target: RetailerTarget, console: ConsoleDefinition) -> None:
        self.target = target
        self.console = console

    @abc.abstractmethod
    async def fetch(self) -> Optional[RetailerQuote]:
        """Return the latest quote or None if the retailer could not be parsed."""

    def build_quote(
        self,
        *,
        price: float,
        notes: Optional[str] = None,
        status: str = "ok",
    ) -> RetailerQuote:
        return RetailerQuote(
            retailer_id=self.target.retailer_id,
            retailer_name=self.target.retailer_name,
            console_id=self.console.console_id,
            console_name=self.console.console_name,
            url=self.target.url,
            price=price,
            currency=self.target.currency,
            shipping_estimate=self.target.shipping_copy,
            last_checked=datetime.utcnow(),
            status=status,
            notes=notes or self.target.notes,
        )

    @property
    def user_agent(self) -> str:
        return settings.scraper_user_agent
