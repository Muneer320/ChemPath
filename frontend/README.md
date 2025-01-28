# ChemPath frontend

This Vite app is part of the [ChemPath teaching demo](../README.md). Run the API and frontend together with `docker compose up --build` from the repository root, then visit http://localhost:5173.

For local development, run `npm ci`, then `npm run dev`; the development server proxies `/api` to http://127.0.0.1:8000. Run `npm run build` and `npm test` to check the app. The frontend was imported from the former `Muneer320/chempath-frontend` repository and adapted to the read-only API.
