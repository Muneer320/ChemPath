---
title: ChemPath
emoji: 🧪
colorFrom: blue
colorTo: green
sdk: docker
pinned: false
license: mit
---

# ChemPath

ChemPath is a local teaching demo for exploring organic chemistry conversions. It includes a React interface and a read-only FastAPI service. The checked-in dataset has **21 compounds and 23 reaction variants**. You can search compounds, select a start and target compound, and compare up to ten loop-free routes of at most six steps.

The route order uses a simple `teaching_cost` score. It does **not** calculate reaction yield, safety, feasibility, or an optimal lab synthesis. This is an incomplete example dataset derived from the original prototype, not a verified NCERT reaction catalog. Check reactions and conditions against a textbook or instructor before relying on them. [NCERT chemistry textbooks](https://ncert.nic.in/textbook.php) are a reference for further study.

## Run the demo

Install Docker and run:

```sh
docker compose up --build
```

Open http://localhost:5173. Try **Ethene** → **Ethanoic acid** in Path Finder; select different Path buttons to compare routes. The compounds page searches by name, formula, and aliases. The API is at http://localhost:8000/docs and its health check at http://localhost:8000/health. Stop the containers with `docker compose down`.

For development without Docker, install Python 3.13 and Node 22. In one terminal run `python -m pip install -r requirements-dev.txt` then `uvicorn main:app --reload`. In another, run `cd frontend`, `npm ci`, and `npm run dev`. Run `python -m unittest discover -s tests -v`, `npm run build`, and `npm test` for checks.

The dataset is in [`data/reactions.json`](data/reactions.json). The app loads and validates it at startup; it has no write API or external database. The graph ranks distinct reagent variants separately. To extend the demo, add compounds and reactions there, including stable IDs and `teaching_cost` values from 1 to 3, and add a source and chemistry review before claiming curricular coverage.

The interface originated in [`Muneer320/chempath-frontend`](https://github.com/Muneer320/chempath-frontend), which is retained as a separate historical archive. This repository contains the integrated runnable version. No public deployment is currently advertised.

## Project notes

The prototype explored representing compounds as graph nodes and reactions as directed edges, then searching for stepwise conversions. The current architecture replaces the former external database with a small checked-in JSON graph, serves read-only endpoints through FastAPI, and uses a React interface to browse compounds and routes. The original hosted deployment and database are no longer maintained; this repository is preserved as a runnable local learning archive.

Revisiting the prototype exposed several useful design lessons: formulas are display text rather than reliable identifiers, multiple reagents can connect the same pair of compounds, and route search must exclude cycles and cap its depth. A useful chemistry product would also need a much larger, individually sourced and reviewed reaction dataset. These examples are intentionally limited to support a working demonstration without suggesting that the prototype reached that goal.

MIT license; see [LICENSE](LICENSE).
