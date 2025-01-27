from neo4j import GraphDatabase
from typing import Dict, Any, List, Optional
import logging
from datetime import datetime


class ChemicalGraph:
    def __init__(self, uri: str, user: str, password: str):
        self._driver = GraphDatabase.driver(uri, auth=(user, password))
        self._verify_connection()
        self._setup_constraints()

    def _verify_connection(self):
        try:
            with self._driver.session() as session:
                session.run("MATCH (n) RETURN count(n) AS count").single()
        except Exception as e:
            logging.error(f"Failed to connect to Neo4j: {e}")
            raise

    def _setup_constraints(self):
        """Setup necessary constraints for the database"""
        with self._driver.session() as session:
            # Ensure unique formulas
            session.run("""
                CREATE CONSTRAINT compound_formula IF NOT EXISTS
                FOR (c:Compound) REQUIRE c.formula IS UNIQUE
            """)

    def close(self):
        self._driver.close()

    def get_compounds(self, filters: Dict[str, Any] = None) -> List[Dict]:
        with self._driver.session() as session:
            query = "MATCH (c:Compound) WHERE 1=1"
            params = {}

            if filters:
                if 'search' in filters:
                    query += """ AND (c.formula CONTAINS $search 
                                OR toLower(c.properties.name) CONTAINS toLower($search))"""
                    params['search'] = filters['search']
                
            query += " RETURN c"
            result = session.run(query, params).data()
            return [record['c'] for record in result]

    def get_compound(self, formula: str) -> Optional[Dict]:
        with self._driver.session() as session:
            result = session.run(
                "MATCH (c:Compound {formula: $formula}) RETURN c",
                formula=formula
            ).single()
            return result['c'] if result else None

    def get_compound_suggestions(self, prefix: str, limit: int) -> List[Dict]:
        with self._driver.session() as session:
            result = session.run("""
                MATCH (c:Compound)
                WHERE c.formula STARTS WITH $prefix 
                   OR toLower(c.properties.name) STARTS WITH toLower($prefix)
                RETURN c
                LIMIT $limit
            """, prefix=prefix, limit=limit).data()
            return [record['c'] for record in result]

    def add_compound(self, formula: str, properties: Dict[str, Any] = None) -> Dict:
        with self._driver.session() as session:
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
            return result[0] if result else None

    def add_reaction(self,
                     reactant: str,
                     product: str,
                     conditions: Dict[str, Any]) -> Dict:
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
                ).data()
            )
            return result[0] if result else None

    def find_paths(self, start_compound: str, end_compound: str, max_depth: int = 5) -> List[Dict]:
        with self._driver.session() as session:
            query = """
                MATCH path = (start:Compound {formula: $start})
                    -[reactions:REACTS_TO*..%d]->
                    (end:Compound {formula: $end})
                WHERE ALL(r IN relationships(path) WHERE 1=1
            """ % max_depth

            params = {"start": start_compound, "end": end_compound}

            query += """)
                WITH path,
                    [n IN nodes(path) | n] as compounds,
                    [r IN relationships(path) | properties(r)] as reactions,
                    [r IN relationships(path) | r.reagent] as reagents,
                    length(path) AS path_length
                RETURN {
                    compounds: compounds,
                    reactions: reactions,
                    reagents: reagents,
                    total_steps: path_length
                } as pathInfo
                ORDER BY path_length
            """

            result = session.run(query, params).data()
            return [record['pathInfo'] for record in result]
