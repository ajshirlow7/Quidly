import { techCatalog } from "../src/data/items";

const USER_AGENT = "QuidlyLinkChecker/1.0 (+https://quidly.local)";
const TIMEOUT_MS = 10000;

type CheckResult = {
  item: string;
  retailer: string;
  url: string;
  status?: number;
  ok: boolean;
  finalUrl?: string;
  error?: string;
};

async function verifyUrl(itemName: string, retailerName: string, url: string): Promise<CheckResult> {
  const controller = new AbortController();
  const timer = setTimeout(() => controller.abort(), TIMEOUT_MS);

  try {
    const response = await fetch(url, {
      method: "GET",
      redirect: "follow",
      headers: {
        "user-agent": USER_AGENT,
        "accept-language": "en-GB,en;q=0.9"
      },
      signal: controller.signal
    });

    clearTimeout(timer);

    const ok = response.status >= 200 && response.status < 400;
    return {
      item: itemName,
      retailer: retailerName,
      url,
      status: response.status,
      finalUrl: response.url,
      ok,
      error: ok ? undefined : `Unexpected status ${response.status}`
    };
  } catch (error) {
    return {
      item: itemName,
      retailer: retailerName,
      url,
      ok: false,
      error: error instanceof Error ? error.message : "Unknown error"
    };
  }
}

(async () => {
  const results: CheckResult[] = [];

  for (const item of techCatalog) {
    for (const retailer of item.retailers) {
      const result = await verifyUrl(item.name, retailer.name, retailer.url);
      results.push(result);
      const statusText = result.status ? `${result.status}` : "ERR";
      const finalPart = result.finalUrl && result.finalUrl !== result.url ? ` → ${result.finalUrl}` : "";
      if (result.ok) {
        console.log(`✔︎ ${item.name} | ${retailer.name} | ${statusText}${finalPart}`);
      } else {
        console.error(`✖ ${item.name} | ${retailer.name} | ${statusText} | ${result.error ?? "Unknown failure"}${finalPart}`);
      }
    }
  }

  const failures = results.filter((result) => !result.ok);
  if (failures.length) {
    console.error(`\n${failures.length} retailer link(s) failed validation.`);
    process.exitCode = 1;
  } else {
    console.log("\nAll retailer links responded successfully.");
  }
})();
