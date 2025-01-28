from fastapi import FastAPI, HTTPException, Query, status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import Dict, Any, List, Optional
import os
from dotenv import load_dotenv
from datetime import datetime
import logging
from src.database.graph_manager import ChemicalGraph

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

app = FastAPI(
    title="ChemPath API",
    description="Chemical Reaction Pathway Finder for Students",
    version="0.1.0",
    root_path=""
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Will adjust this in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global graph instance
graph = None

@app.on_event("startup")
async def startup_event():
    global graph
    logger.info("Starting up ChemPath API")
    
    required_vars = ["NEO4J_URI", "NEO4J_USER", "NEO4J_PASSWORD"]
    missing_vars = [var for var in required_vars if not os.getenv(var)]
    
    if missing_vars:
        logger.error(f"Missing required environment variables: {', '.join(missing_vars)}")
        raise RuntimeError(f"Missing required environment variables: {', '.join(missing_vars)}")
    
    try:
        # Initialize graph with connection retry logic
        graph = ChemicalGraph(
            os.getenv("NEO4J_URI"),
            os.getenv("NEO4J_USER"),
            os.getenv("NEO4J_PASSWORD")
        )
        logger.info("Successfully initialized ChemPath API")
    except Exception as e:
        logger.error(f"Failed to initialize graph database: {str(e)}")
        raise

@app.on_event("shutdown")
async def shutdown_event():
    global graph
    if graph:
        graph.close()
        logger.info("Closed Neo4j connection")


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

@app.get("/")
async def root():
    return {
        "status": "running",
        "service": "ChemPath API",
        "time": datetime.utcnow().isoformat()
    }

@app.get("/health")
async def health_check():
    """API health check endpoint"""
    if not graph:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Database connection not initialized"
        )
    
    try:
        # Try to execute a simple query to verify database connection
        with graph._driver.session() as session:
            result = session.run("RETURN 1 as num").single()
            if result and result["num"] == 1:
                return {
                    "status": "healthy",
                    "database": "connected",
                    "timestamp": datetime.utcnow().isoformat()
                }
    except Exception as e:
        logger.error(f"Health check failed: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=f"Database connection error: {str(e)}"
        )


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


# Run the API with Uvicorn: `uvicorn src.api.main:app --reload`
