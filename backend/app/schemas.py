from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, HttpUrl


class RetailerQuote(BaseModel):
    retailer_id: str
    retailer_name: str
    console_id: str
    console_name: str
    url: HttpUrl
    price: float
    currency: str
    shipping_estimate: Optional[str]
    last_checked: datetime
    status: str
    notes: Optional[str] = None


class ConsolePrice(BaseModel):
    console_id: str
    console_name: str
    base_specs: str
    retailers: List[RetailerQuote]
    cheapest_price: Optional[float]
    cheapest_retailer: Optional[str]


class ConsoleCollection(BaseModel):
    consoles: List[ConsolePrice]
    refreshed_at: datetime


class RefreshResponse(BaseModel):
    refreshed: int
    failed: int
    completed_at: datetime
