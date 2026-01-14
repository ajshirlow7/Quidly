import { useEffect, useMemo, useState } from "react";
import ItemSelector from "./components/ItemSelector";
import RetailerGrid from "./components/RetailerGrid";
import { techCatalog, type TechItem } from "./data/items";
import { fetchRemoteCatalog } from "./lib/remoteCatalog";

const App = () => {
  const [catalog, setCatalog] = useState<TechItem[]>(techCatalog);
  const [query, setQuery] = useState("");
  const [selectedId, setSelectedId] = useState(techCatalog[0]?.id ?? "");
  const [isUsingFallback, setIsUsingFallback] = useState(true);
  const [feedMessage, setFeedMessage] = useState("Syncing live console prices...");

  useEffect(() => {
    const controller = new AbortController();
    const load = async () => {
      try {
        const remoteCatalog = await fetchRemoteCatalog(controller.signal);
        if (remoteCatalog.length) {
          setCatalog(remoteCatalog);
          setIsUsingFallback(false);
          setFeedMessage("Streaming live retailer data");
        }
      } catch (error) {
        console.warn("Falling back to static catalog", error);
        setIsUsingFallback(true);
        setFeedMessage("Live feed unavailable — showing cached prices");
      }
    };
    load();
    return () => controller.abort();
  }, []);

  useEffect(() => {
    if (!catalog.length) {
      return;
    }
    setSelectedId((current) => (catalog.some((item) => item.id === current) ? current : catalog[0].id));
  }, [catalog]);

  const filtered = useMemo(() => {
    const normalized = query.trim().toLowerCase();
    if (!normalized) {
      return catalog;
    }
    return catalog.filter((item) => {
      const haystack = `${item.name} ${item.category} ${item.baseSpecs}`.toLowerCase();
      return haystack.includes(normalized);
    });
  }, [catalog, query]);

  const visibleId = filtered.some((item) => item.id === selectedId) ? selectedId : filtered[0]?.id ?? "";
  const activeItem = filtered.find((item) => item.id === visibleId);

  return (
    <div className="app-shell">
      <section className="hero">
        <p>Quidly • UK Price Radar</p>
        <h1>Pick a device, get the best deal</h1>
        <p>
          The launch focuses on flagship consoles sourced solely from trusted United Kingdom retailers, with pound sterling prices
          and fulfillment context tailored to local shoppers.
        </p>
        <span className={`data-badge ${isUsingFallback ? "fallback" : "live"}`}>{feedMessage}</span>
      </section>

      <ItemSelector
        items={filtered}
        selectedId={visibleId}
        onSelect={setSelectedId}
        query={query}
        onQueryChange={setQuery}
      />

      <div className="panel results-card">
        <div className="results-header">
          <div>
            <p>Currently tracking</p>
            <h2>{activeItem ? `${activeItem.name} · ${activeItem.baseSpecs}` : "No matching items"}</h2>
          </div>
          {activeItem ? <span>{activeItem.category}</span> : null}
        </div>

        {activeItem ? <RetailerGrid retailers={activeItem.retailers} /> : <p className="empty-state">No products match this search.</p>}
      </div>
    </div>
  );
};

export default App;
