import { ChangeEvent } from "react";
import type { TechItem } from "../data/items";

type Props = {
  items: TechItem[];
  selectedId: string;
  onSelect: (id: string) => void;
  query: string;
  onQueryChange: (value: string) => void;
};

const ItemSelector = ({ items, selectedId, onSelect, query, onQueryChange }: Props) => {
  const handleSelect = (event: ChangeEvent<HTMLSelectElement>) => {
    onSelect(event.target.value);
  };

  const handleQuery = (event: ChangeEvent<HTMLInputElement>) => {
    onQueryChange(event.target.value);
  };

  return (
    <div className="panel selector">
      <div>
        <label htmlFor="search">Find a product</label>
        <input
          id="search"
          type="search"
          placeholder="Search PlayStation, Xbox, Switch..."
          value={query}
          onChange={handleQuery}
        />
      </div>
      <div>
        <label htmlFor="item">Or choose from the list</label>
        <select id="item" value={selectedId} onChange={handleSelect}>
          {items.map((item) => (
            <option key={item.id} value={item.id}>
              {item.name} · {item.category}
            </option>
          ))}
        </select>
      </div>
    </div>
  );
};

export default ItemSelector;
