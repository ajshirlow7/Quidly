from dataclasses import dataclass, field
from typing import List, Optional


@dataclass(slots=True)
class RetailerTarget:
    retailer_id: str
    retailer_name: str
    url: str
    currency: str = "GBP"
    shipping_copy: Optional[str] = None
    price_selector: Optional[str] = None
    price_attribute: Optional[str] = None
    json_ld_hint: Optional[str] = None
    requires_session: bool = False
    notes: Optional[str] = None


@dataclass(slots=True)
class ConsoleDefinition:
    console_id: str
    console_name: str
    base_specs: str
    retailers: List[RetailerTarget] = field(default_factory=list)


CONSOLE_CATALOG: List[ConsoleDefinition] = [
    ConsoleDefinition(
        console_id="ps5-slim",
        console_name="PlayStation 5 Slim",
        base_specs="Disc · 1 TB SSD",
        retailers=[
            RetailerTarget(
                retailer_id="ps-direct",
                retailer_name="PlayStation Direct UK",
                url="https://direct.playstation.com/en-gb/buy-consoles/playstation5-console-1-tb",
                shipping_copy="Free delivery in 1-2 days",
                json_ld_hint="Product",
                notes="Requires PSN session for basket actions; HTML fetcher reads public price block."
            ),
            RetailerTarget(
                retailer_id="currys",
                retailer_name="Currys",
                url="https://www.currys.co.uk/products/sony-playstation-5-model-group-slim-10258393.html",
                shipping_copy="Next-day delivery",
                price_selector="span[data-product-price]",
            ),
            RetailerTarget(
                retailer_id="amazon-uk",
                retailer_name="Amazon UK",
                url="https://www.amazon.co.uk/gp/product/B0CL52TWK1",
                shipping_copy="Prime · arrives tomorrow",
                requires_session=True,
                notes="Switch to PA-API or ASIN affiliate feeds for reliability."
            ),
            RetailerTarget(
                retailer_id="game-uk",
                retailer_name="GAME",
                url="https://www.game.co.uk/playstation/consoles/ps5/disc-edition",
                shipping_copy="Collect in store today",
                price_selector="div.price .value"
            )
        ]
    ),
    ConsoleDefinition(
        console_id="xbox-series-x",
        console_name="Xbox Series X",
        base_specs="1 TB NVMe",
        retailers=[
            RetailerTarget(
                retailer_id="microsoft-store",
                retailer_name="Microsoft Store UK",
                url="https://www.microsoft.com/en-gb/d/xbox-series-x/8wj714n3rbtl",
                shipping_copy="Ships tomorrow",
                price_selector="span[data-bi-name='price']"
            ),
            RetailerTarget(
                retailer_id="very",
                retailer_name="Very",
                url="https://www.very.co.uk/microsoft-xbox-series-x-1tb-console/1600598967.prd",
                shipping_copy="Tracked delivery in 2 days",
                price_selector="span[itemprop='price']"
            ),
            RetailerTarget(
                retailer_id="argos",
                retailer_name="Argos",
                url="https://www.argos.co.uk/product/7085969",
                shipping_copy="Same-day collection",
                price_selector="span[data-e2e='product-price']"
            )
        ]
    ),
    ConsoleDefinition(
        console_id="switch-oled",
        console_name="Nintendo Switch OLED",
        base_specs="Neon · 64 GB",
        retailers=[
            RetailerTarget(
                retailer_id="nintendo-store",
                retailer_name="Nintendo Store UK",
                url="https://store.nintendo.co.uk/en-gb/nintendo-switch-oled-model-neon-blue-neon-red/9997015.html",
                shipping_copy="Ships in 3 days",
                json_ld_hint="Product"
            ),
            RetailerTarget(
                retailer_id="amazon-switch",
                retailer_name="Amazon UK",
                url="https://www.amazon.co.uk/gp/product/B098RL6J8S",
                shipping_copy="Prime · arrives tomorrow",
                requires_session=True,
                notes="Leverage ASIN feeds for consistent data."
            ),
            RetailerTarget(
                retailer_id="smyths",
                retailer_name="Smyths Toys",
                url="https://www.smythstoys.com/uk/en-gb/video-games-and-consoles/nintendo-switch/nintendo-switch-consoles/nintendo-switch-oled-model-neon-blue-neon-red/p/199508",
                shipping_copy="Pickup later today",
                price_selector="span[itemprop='price']"
            )
        ]
    ),
    ConsoleDefinition(
        console_id="steam-deck-oled",
        console_name="Steam Deck OLED",
        base_specs="1 TB · Wi-Fi 6E",
        retailers=[
            RetailerTarget(
                retailer_id="steam",
                retailer_name="Steam Store UK",
                url="https://store.steampowered.com/steamdeck",
                shipping_copy="Ships in 4 days",
                json_ld_hint="Product"
            ),
            RetailerTarget(
                retailer_id="currys-steam",
                retailer_name="Currys",
                url="https://www.currys.co.uk/products/valve-steam-deck-oled-1-tb-handheld-gaming-pc-10254784.html",
                shipping_copy="Collect tomorrow",
                price_selector="span[data-product-price]"
            ),
            RetailerTarget(
                retailer_id="scan",
                retailer_name="Scan UK",
                url="https://www.scan.co.uk/products/valve-steam-deck-oled-1tb-handheld-gaming-pc",
                shipping_copy="Tracked delivery in 2 days",
                price_selector="span.price"
            )
        ]
    )
]
