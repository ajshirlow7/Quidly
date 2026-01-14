from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Dict, List

from .schemas import ConsolePrice, RetailerQuote


@dataclass
class StoredConsole:
    console: ConsolePrice
    updated_at: datetime


class PriceStore:
    def __init__(self) -> None:
        self._data: Dict[str, StoredConsole] = {}

    def replace_console(self, console: ConsolePrice) -> None:
        self._data[console.console_id] = StoredConsole(console=console, updated_at=datetime.utcnow())

    def get_console(self, console_id: str) -> ConsolePrice | None:
        stored = self._data.get(console_id)
        if stored:
            return stored.console
        return None

    def list_consoles(self) -> List[ConsolePrice]:
        return [stored.console for stored in self._data.values()]

    def reset(self) -> None:
        self._data.clear()


store = PriceStore()
