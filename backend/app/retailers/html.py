from __future__ import annotations

import json
import re
from typing import Optional

import httpx
from bs4 import BeautifulSoup
from tenacity import retry, stop_after_attempt, wait_fixed

from ..config import settings
from ..data import ConsoleDefinition, RetailerTarget
from ..schemas import RetailerQuote
from .base import RetailerFetcher

PRICE_PATTERN = re.compile(r"([0-9]+[\.,]?[0-9]{0,2})")


class HtmlRetailerFetcher(RetailerFetcher):
    slug = "html"

    def __init__(self, target: RetailerTarget, console: ConsoleDefinition) -> None:
        super().__init__(target, console)
        self._client = httpx.AsyncClient(timeout=settings.http_timeout_seconds, headers={"user-agent": self.user_agent})

    async def close(self) -> None:
        await self._client.aclose()

    @retry(stop=stop_after_attempt(3), wait=wait_fixed(1.5))
    async def _get(self, url: str) -> httpx.Response:
        response = await self._client.get(url, follow_redirects=True)
        response.raise_for_status()
        return response

    async def fetch(self) -> Optional[RetailerQuote]:
        response = await self._get(self.target.url)
        soup = BeautifulSoup(response.text, "html.parser")

        price_text: Optional[str] = None
        if self.target.price_selector:
            node = soup.select_one(self.target.price_selector)
            if node:
                if self.target.price_attribute and node.has_attr(self.target.price_attribute):
                    price_text = str(node[self.target.price_attribute])
                else:
                    price_text = node.get_text(strip=True)

        if not price_text and settings.enable_json_ld_fallback:
            price_text = self._parse_json_ld(soup)

        if not price_text:
            return None

        price_value = self._normalise_price(price_text)
        if price_value is None:
            return None

        return self.build_quote(price=price_value)

    def _parse_json_ld(self, soup: BeautifulSoup) -> Optional[str]:
        scripts = soup.find_all("script", attrs={"type": "application/ld+json"})
        for script in scripts:
            try:
                data = json.loads(script.string or "{}")
            except json.JSONDecodeError:
                continue

            if isinstance(data, list):
                for entry in data:
                    value = self._extract_price_from_ld(entry)
                    if value:
                        return value
            else:
                value = self._extract_price_from_ld(data)
                if value:
                    return value
        return None

    def _extract_price_from_ld(self, data: dict) -> Optional[str]:
        if self.target.json_ld_hint and data.get("@type") != self.target.json_ld_hint:
            return None

        offers = data.get("offers")
        if isinstance(offers, dict):
            price = offers.get("price") or offers.get("priceSpecification", {}).get("price")
            if price:
                return str(price)
        if isinstance(offers, list):
            for offer in offers:
                price = offer.get("price")
                if price:
                    return str(price)
        if "price" in data:
            return str(data["price"])
        return None

    def _normalise_price(self, text: str) -> Optional[float]:
        match = PRICE_PATTERN.search(text.replace(",", ""))
        if not match:
            return None
        try:
            return float(match.group(1))
        except ValueError:
            return None
