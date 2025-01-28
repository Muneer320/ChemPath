"""ChemPath read-only API for a small, validated teaching graph."""

from contextlib import asynccontextmanager
from datetime import datetime, UTC
import os

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware

from src.database.graph_manager import ChemicalGraph

load_dotenv()


@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.graph = ChemicalGraph()
    yield


app = FastAPI(title="ChemPath teaching graph", version="1.0.0", lifespan=lifespan)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[origin.strip() for origin in os.getenv("ALLOWED_ORIGINS", "http://localhost:5173,http://127.0.0.1:5173").split(",") if origin.strip()],
    allow_methods=["GET"],
    allow_headers=["Content-Type"],
)


@app.get("/")
def root():
    return {"service": "ChemPath", "docs": "/docs", "health": "/health"}


@app.get("/health")
def health():
    graph = app.state.graph
    return {"status": "healthy", "compounds": len(graph.compounds), "reactions": len(graph.reactions), "timestamp": datetime.now(UTC).isoformat()}


@app.get("/compounds/")
def get_compounds(search: str | None = None):
    return app.state.graph.get_compounds(search)


@app.get("/compounds/suggestions/")
def get_suggestions(prefix: str = Query(min_length=1), limit: int = Query(default=10, ge=1, le=50)):
    return app.state.graph.get_compound_suggestions(prefix, limit)


@app.get("/compounds/{identifier}")
def get_compound(identifier: str):
    compound = app.state.graph.get_compound(identifier)
    if compound is None:
        raise HTTPException(status_code=404, detail="Compound not found")
    return compound


@app.get("/paths/")
def find_paths(start: str, end: str, max_steps: int = Query(default=5, ge=1, le=6)):
    try:
        paths = app.state.graph.find_paths(start, end, max_steps)
    except KeyError:
        raise HTTPException(status_code=404, detail="Unknown start or end compound")
    if not paths:
        raise HTTPException(status_code=404, detail="No path in this teaching subset")
    return paths
