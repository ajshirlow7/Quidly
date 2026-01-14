export type Retailer = {
  name: string;
  logo?: string;
  shippingEstimate: string;
  price: number;
  url: string;
  updatedAt: string;
};

export type TechItem = {
  id: string;
  name: string;
  category: string;
  baseSpecs: string;
  retailers: Retailer[];
};

export const techCatalog: TechItem[] = [
  {
    id: "ps5-slim",
    name: "PlayStation 5 Slim",
    category: "Console",
    baseSpecs: "Disc · 1 TB SSD",
    retailers: [
      {
        name: "PlayStation Direct UK",
        shippingEstimate: "Free delivery in 1-2 days",
        price: 479,
        url: "https://direct.playstation.com/en-gb/buy-consoles/playstation5-console-1-tb",
        updatedAt: "Just now"
      },
      {
        name: "Currys",
        shippingEstimate: "Next-day delivery",
        price: 469,
        url: "https://www.currys.co.uk/products/sony-playstation-5-model-group-slim-10258393.html",
        updatedAt: "7 min ago"
      },
      {
        name: "Amazon UK",
        shippingEstimate: "Prime · arrives tomorrow",
        price: 459,
        url: "https://www.amazon.co.uk/gp/product/B0CL52TWK1",
        updatedAt: "2 min ago"
      },
      {
        name: "GAME",
        shippingEstimate: "Collect in store today",
        price: 465,
        url: "https://www.game.co.uk/playstation/consoles/ps5/disc-edition",
        updatedAt: "15 min ago"
      }
    ]
  },
  {
    id: "xbox-series-x",
    name: "Xbox Series X",
    category: "Console",
    baseSpecs: "1 TB NVMe",
    retailers: [
      {
        name: "Microsoft Store UK",
        shippingEstimate: "Ships tomorrow",
        price: 479,
        url: "https://www.microsoft.com/en-gb/d/xbox-series-x/8wj714n3rbtl",
        updatedAt: "5 min ago"
      },
      {
        name: "Very",
        shippingEstimate: "Tracked delivery in 2 days",
        price: 459,
        url: "https://www.very.co.uk/microsoft-xbox-series-x-1tb-console/1600598967.prd",
        updatedAt: "12 min ago"
      },
      {
        name: "Argos",
        shippingEstimate: "Same-day collection",
        price: 469,
        url: "https://www.argos.co.uk/product/7085969",
        updatedAt: "18 min ago"
      }
    ]
  },
  {
    id: "switch-oled",
    name: "Nintendo Switch OLED",
    category: "Console",
    baseSpecs: "Neon · 64 GB",
    retailers: [
      {
        name: "Nintendo Store UK",
        shippingEstimate: "Ships in 3 days",
        price: 309,
        url: "https://store.nintendo.co.uk/en-gb/nintendo-switch-oled-model-neon-blue-neon-red/9997015.html",
        updatedAt: "10 min ago"
      },
      {
        name: "Amazon UK",
        shippingEstimate: "Prime · arrives tomorrow",
        price: 299,
        url: "https://www.amazon.co.uk/gp/product/B098RL6J8S",
        updatedAt: "Just now"
      },
      {
        name: "Smyths Toys",
        shippingEstimate: "Pickup later today",
        price: 305,
        url: "https://www.smythstoys.com/uk/en-gb/video-games-and-consoles/nintendo-switch/nintendo-switch-consoles/nintendo-switch-oled-model-neon-blue-neon-red/p/199508",
        updatedAt: "6 min ago"
      }
    ]
  },
  {
    id: "steam-deck-oled",
    name: "Steam Deck OLED",
    category: "Console",
    baseSpecs: "1 TB · Wi-Fi 6E",
    retailers: [
      {
        name: "Steam Store UK",
        shippingEstimate: "Ships in 4 days",
        price: 569,
        url: "https://store.steampowered.com/steamdeck",
        updatedAt: "3 min ago"
      },
      {
        name: "Currys",
        shippingEstimate: "Collect tomorrow",
        price: 559,
        url: "https://www.currys.co.uk/products/valve-steam-deck-oled-1-tb-handheld-gaming-pc-10254784.html",
        updatedAt: "20 min ago"
      },
      {
        name: "Scan UK",
        shippingEstimate: "Tracked delivery in 2 days",
        price: 565,
        url: "https://www.scan.co.uk/products/valve-steam-deck-oled-1tb-handheld-gaming-pc",
        updatedAt: "11 min ago"
      }
    ]
  }
];
