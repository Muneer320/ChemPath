from neo4j import GraphDatabase
from typing import Dict, Any
import logging

class ChemicalGraph:
    def __init__(self, uri: str, user: str, password: str):
        self._driver = GraphDatabase.driver(uri, auth=(user, password))
        self._verify_connection()
        
    def _verify_connection(self):
        try:
            with self._driver.session() as session:
                session.run("MATCH (n) RETURN count(n) AS count")
        except Exception as e:
            logging.error(f"Failed to connect to Neo4j: {e}")
            raise

    def close(self):
        self._driver.close()

    def add_compound(self, formula: str, properties: Dict[str, Any]):
        with self._driver.session() as session:
            result = session.execute_write(
                lambda tx: tx.run(
                    """
                    MERGE (c:Compound {formula: $formula})
                    SET c += $properties
                    RETURN c
                    """,
                    formula=formula,
                    properties=properties
                )
            )
            return result.single()

    def add_reaction(self, 
                    reactant: str, 
                    product: str, 
                    conditions: Dict[str, Any]):
        with self._driver.session() as session:
            result = session.execute_write(
                lambda tx: tx.run(
                    """
                    MATCH (r:Compound {formula: $reactant})
                    MATCH (p:Compound {formula: $product})
                    MERGE (r)-[rel:REACTS_TO]->(p)
                    SET rel += $conditions
                    RETURN rel
                    """,
                    reactant=reactant,
                    product=product,
                    conditions=conditions
                )
            )
            return result.single()