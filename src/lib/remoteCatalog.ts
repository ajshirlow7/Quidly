import type { TechItem } from "../data/items";

export type ApiRetailer = {
  retailer_id: string;
  retailer_name: string;
  url: string;
  price: number;
  currency: string;
  shipping_estimate?: string | null;
  last_checked: string;
  status: string;
};

export type ApiConsole = {
  console_id: string;
  console_name: string;
  base_specs: string;
  retailers: ApiRetailer[];
};

export type ApiResponse = {
  consoles: ApiConsole[];
  refreshed_at: string;
};

const API_URL = import.meta.env.VITE_API_URL ?? "http://localhost:8000";

const formatter = new Intl.RelativeTimeFormat("en", { numeric: "auto" });

function formatRelativeTime(timestamp: string): string {
  const updated = new Date(timestamp);
  const now = new Date();
  const diffMs = updated.getTime() - now.getTime();
  const diffMinutes = Math.round(diffMs / 60000);
  if (Math.abs(diffMinutes) < 60) {
    return formatter.format(diffMinutes, "minute");
  }
  const diffHours = Math.round(diffMinutes / 60);
  return formatter.format(diffHours, "hour");
}

function mapConsole(apiConsole: ApiConsole): TechItem {
  return {
    id: apiConsole.console_id,
    name: apiConsole.console_name,
    category: "Console",
    baseSpecs: apiConsole.base_specs,
    retailers: apiConsole.retailers.map((retailer) => ({
      name: retailer.retailer_name,
      shippingEstimate: retailer.shipping_estimate ?? "",
      price: retailer.price,
      url: retailer.url,
      updatedAt: formatRelativeTime(retailer.last_checked)
    }))
  };
}

export async function fetchRemoteCatalog(signal?: AbortSignal): Promise<TechItem[]> {
  const response = await fetch(`${API_URL.replace(/\/$/, "")}/consoles`, { signal });
  if (!response.ok) {
    throw new Error(`Failed to load consoles: ${response.status}`);
  }
  const payload = (await response.json()) as ApiResponse;
  return payload.consoles.map(mapConsole);
}
