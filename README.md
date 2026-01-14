# Quidly Tech Price Radar

A Vite + React + TypeScript single-page app for comparing flagship tech prices across major United Kingdom retailers, with
launch coverage centred on modern consoles priced in GBP.

## Getting started

1. **Install dependencies**
   ```bash
   npm install
   ```
2. **Run the dev server**
   ```bash
   npm run dev
   ```
3. **Build for production**
   ```bash
   npm run build
   npm run preview
   ```

4. **Validate retailer links**
   ```bash
   npm run check:links
   ```
   Runs a lightweight fetch against every retailer URL in the mock catalog so you can catch broken or redirected listings early.

## Live pricing backend (optional but recommended)

1. Bootstrap the Python API (FastAPI + httpx) inside `backend/`:
   ```bash
   cd backend
   python -m venv .venv
   . .venv/Scripts/activate  # PowerShell: .venv\Scripts\Activate.ps1
   pip install -r requirements.txt
   uvicorn app.main:app --reload
   ```
2. Point the frontend at the API by setting `VITE_API_URL` (defaults to `http://localhost:8000`). Create a `.env` file at the repo root if you need to override it:
   ```bash
   VITE_API_URL=http://localhost:8000
   ```
3. The app automatically prefers live data; if the backend is offline it falls back to the bundled mock catalog.

See [backend/README.md](backend/README.md) for fetcher architecture, environment variables, and extension guidance.

## Project structure

- `src/data/items.ts` — mock catalog of UK retailers with GBP pricing for launch consoles.
- `src/components` — `ItemSelector` and `RetailerGrid` present the search UI and price grid.
- `src/App.tsx` — orchestrates filtering, selection, and renders the experience.
- `src/styles.css` — global styles, gradients, and component-specific styling.
- `backend/` — FastAPI service that polls retailers, caches the latest prices, and exposes them over HTTP.

Feel free to expand the catalog, wire up live APIs, or layer in auth/search analytics as you evolve the product.
