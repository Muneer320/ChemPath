from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import Dict, Any, List, Optional
import os
from dotenv import load_dotenv
from datetime import datetime
from src.database.graph_manager import ChemicalGraph


# Load environment variables
load_dotenv()

app = FastAPI(
    title="ChemPath API",
    description="Chemical Reaction Pathway Finder for Students",
    version="0.1.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust this in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create graph instance
graph = ChemicalGraph(
    os.getenv("NEO4J_URI"),
    os.getenv("NEO4J_USER"),
    os.getenv("NEO4J_PASSWORD")
)


# Models

class CompoundCreate(BaseModel):
    formula: str
    name: Optional[str] = None
    molecular_weight: Optional[float] = None
    state: Optional[str] = None
    class_: Optional[str] = Field(None, alias="class")


class ReactionConditions(BaseModel):
    reagent: str
    temperature: Optional[float] = None
    pressure: Optional[float] = None
    mechanism: Optional[str] = None
    description: Optional[str] = None


class ReactionCreate(BaseModel):
    reactant: str
    product: str
    conditions: ReactionConditions


# Endpoints

@app.get("/health")
async def health_check():
    """API health check endpoint"""
    return {"status": "healthy", "timestamp": datetime.utcnow().isoformat()}


@app.get("/compounds/", response_model=List[Dict[str, Any]])
async def get_compounds(
    search: Optional[str] = None
):
    """Get all compounds with optional filtering."""
    try:
        filters = {}
        if search:
            filters["search"] = search

        compounds = graph.get_compounds(filters)
        return compounds
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.get("/compounds/{formula}", response_model=Dict[str, Any])
async def get_compound(formula: str):
    """Get detailed information about a specific compound"""
    try:
        compound = graph.get_compound(formula)
        if not compound:
            raise HTTPException(status_code=404, detail="Compound not found")
        return compound
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.get("/compounds/suggestions/", response_model=List[Dict[str, Any]])
async def get_compound_suggestions(
    prefix: str = Query(..., min_length=1),
    limit: int = Query(default=10, le=50)
):
    """Get compound suggestions for autocomplete"""
    try:
        suggestions = graph.get_compound_suggestions(prefix, limit)
        return suggestions
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.get("/paths/", response_model=List[Dict[str, Any]])
async def find_paths(
    start: str,
    end: str,
    max_steps: int = Query(default=5, le=10)
):
    """Find possible reaction paths between two compounds."""
    try:
        paths = graph.find_paths(start, end, max_steps)
        if not paths:
            raise HTTPException(
                status_code=404, detail="No valid paths found between compounds")
        return paths
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.post("/compounds/", response_model=Dict[str, Any])
async def create_compound(compound: CompoundCreate):
    """Create a new compound."""
    try:
        result = graph.add_compound(
            compound.formula,  # Mandatory
            {k: v for k, v in compound.dict().items() if v is not None}
        )
        return result.get("c")
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.post("/reactions/", response_model=str)
async def create_reaction(reaction: ReactionCreate):
    """Create a new reaction between compounds."""
    try:
        result = graph.add_reaction(
            reaction.reactant,
            reaction.product,
            reaction.conditions.dict()
        )
        return "Reaction created successfully"
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


# Shutdown event


@app.on_event("shutdown")
def shutdown_event():
    graph.close()


# Run the API with Uvicorn: `uvicorn src.api.main:app --reload`
