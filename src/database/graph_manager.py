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
                session.run("MATCH (n) RETURN count(n) AS count").single()
        except Exception as e:
            logging.error(f"Failed to connect to Neo4j: {e}")
            raise

    def close(self):
        self._driver.close()

    def add_compound(self, formula: str, properties: Dict[str, Any] = None):
        with self._driver.session() as session:
            # Ensure we at least have a formula
            if not properties:
                properties = {}
                
            result = session.execute_write(
                lambda tx: tx.run(
                    """
                    MERGE (c:Compound {formula: $formula})
                    SET c += $properties
                    RETURN c
                    """,
                    formula=formula,
                    properties=properties
                ).data()
            )
            return result


    def add_reaction(self, 
                    reactant: str, 
                    product: str, 
                    conditions: Dict[str, Any],
                    reaction_id: str = None):
        with self._driver.session() as session:
            if not reaction_id:
                reagent = conditions.get('reagent', 'unknown')
                reaction_id = f"{reactant}->{product}_{reagent}"

            result = session.execute_write(
                lambda tx: tx.run(
                    """
                    MATCH (r:Compound {formula: $reactant})
                    MATCH (p:Compound {formula: $product})
                    MERGE (r)-[rel:REACTS_TO {reaction_id: $reaction_id}]->(p)
                    SET rel += $conditions
                    RETURN rel
                    """,
                    reactant=reactant,
                    product=product,
                    conditions=conditions,
                    reaction_id=reaction_id
                ).data()
            )
            return result

    def find_all_paths(self, start_compound: str, end_compound: str, max_depth: int = 5):
        with self._driver.session() as session:
            result = session.execute_read(
                lambda tx: tx.run(
                    f"""
                    MATCH path = (start:Compound {{formula: $start}})-[reactions:REACTS_TO*..{max_depth}]->(end:Compound {{formula: $end}})
                    WITH path,
                         [r IN relationships(path) | r.reagent] AS reagents,
                         [r IN relationships(path) | properties(r)] AS reactionProperties,
                         length(path) AS path_length
                    RETURN path, reagents, reactionProperties, path_length
                    ORDER BY path_length
                    """,
                    start=start_compound,
                    end=end_compound
                ).data()
            )
            return result