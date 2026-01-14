import { ExternalLink, Truck } from "lucide-react";
import type { Retailer } from "../data/items";

type Props = {
  retailers: Retailer[];
};

const currency = new Intl.NumberFormat("en-GB", {
  style: "currency",
  currency: "GBP"
});

const RetailerGrid = ({ retailers }: Props) => {
  if (!retailers.length) {
    return <p className="empty-state">No live offers yet. Try a different item.</p>;
  }

  return (
    <div className="price-grid">
      {retailers.map((retailer) => (
        <article className="price-card" key={retailer.name}>
          <header>
            <h3>{retailer.name}</h3>
            <span>{retailer.updatedAt}</span>
          </header>
          <p className="price">{currency.format(retailer.price)}</p>
          <p>
            <Truck size={16} style={{ marginRight: "0.3rem", verticalAlign: "text-bottom" }} />
            {retailer.shippingEstimate}
          </p>
          <a className="cta" href={retailer.url} target="_blank" rel="noreferrer">
            See offer <ExternalLink size={16} />
          </a>
        </article>
      ))}
    </div>
  );
};

export default RetailerGrid;
