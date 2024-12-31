from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Dict, Any, List
import os
from dotenv import load_dotenv
from src.database.graph_manager import ChemicalGraph

load_dotenv()

app = FastAPI(title="ChemPath API", version="0.1")
graph = ChemicalGraph(
    os.getenv("NEO4J_URI"),
    os.getenv("NEO4J_USER"),
    os.getenv("NEO4J_PASSWORD")
)

class CompoundCreate(BaseModel):
    formula: str
    properties: Dict[str, Any]

class ReactionCreate(BaseModel):
    reactant: str
    product: str
    conditions: Dict[str, Any]

@app.post("/compounds/")
async def create_compound(compound: CompoundCreate):
    try:
        result = graph.add_compound(compound.formula, compound.properties)
        return {"status": "success", "data": result}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/reactions/")
async def create_reaction(reaction: ReactionCreate):
    try:
        result = graph.add_reaction(
            reaction.reactant, 
            reaction.product, 
            reaction.conditions
        )
        return {"status": "success", "data": result}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))