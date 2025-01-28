from neo4j import GraphDatabase
from neo4j.exceptions import ServiceUnavailable, ConfigurationError
import time
import logging
from typing import Optional, Dict, Any, List

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ChemicalGraph:
    def __init__(self, uri: str, user: str, password: str, max_retries: int = 5, retry_delay: int = 5):
        self._uri = uri
        self._user = user
        self._password = password
        self._driver = None
        self._max_retries = max_retries
        self._retry_delay = retry_delay
        self._connect()

    def _connect(self) -> None:
        """Establish connection to Neo4j with retry logic"""
        retries = 0
        last_exception = None

        while retries < self._max_retries:
            try:
                logger.info(f"Attempting to connect to Neo4j (Attempt {retries + 1}/{self._max_retries})")
                if not self._uri:
                    raise ConfigurationError("Neo4j URI is not set")
                
                self._driver = GraphDatabase.driver(
                    self._uri, 
                    auth=(self._user, self._password),
                    max_connection_lifetime=3600,  # 1 hour
                    max_connection_pool_size=50,
                    connection_acquisition_timeout=60  # 1 minute timeout
                )
                # Verify connection
                self._driver.verify_connectivity()
                logger.info("Successfully connected to Neo4j")
                return
            except Exception as e:
                last_exception = e
                logger.error(f"Failed to connect to Neo4j: {str(e)}")
                retries += 1
                if retries < self._max_retries:
                    logger.info(f"Retrying in {self._retry_delay} seconds...")
                    time.sleep(self._retry_delay)

        # If we get here, all retries failed
        logger.error("Max retries reached. Could not connect to Neo4j")
        raise last_exception

    def close(self):
        """Close the driver connection"""
        if self._driver:
            self._driver.close()

    def _verify_connection(self):
        try:
            with self._driver.session() as session:
                session.run("MATCH (n) RETURN count(n) AS count").single()
        except Exception as e:
            logging.error(f"Failed to connect to Neo4j: {e}")
            raise

    def _setup_constraints(self):
        """Setup necessary constraints for the database"""
        try:
            with self._driver.session() as session:
                # Ensure unique formulas
                session.run("""
                    CREATE CONSTRAINT compound_formula IF NOT EXISTS
                    FOR (c:Compound) REQUIRE c.formula IS UNIQUE
                """)
        except Exception as e:
            logger.error(f"Error setting constraints: {str(e)}")
            raise

    def get_compounds(self, filters: Dict[str, Any] = None) -> List[Dict]:
        try:
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
        except Exception as e:
            logger.error(f"Error getting compounds: {str(e)}")
            raise

    def get_compound(self, formula: str) -> Optional[Dict]:
        try:
            with self._driver.session() as session:
                result = session.run(
                    "MATCH (c:Compound {formula: $formula}) RETURN c",
                    formula=formula
                ).single()
                return result['c'] if result else None
        except Exception as e:
            logger.error(f"Error getting compounds: {str(e)}")
            raise

    def get_compound_suggestions(self, prefix: str, limit: int) -> List[Dict]:
        try:
            with self._driver.session() as session:
                result = session.run("""
                    MATCH (c:Compound)
                    WHERE c.formula STARTS WITH $prefix 
                    OR toLower(c.properties.name) STARTS WITH toLower($prefix)
                    RETURN c
                    LIMIT $limit
                """, prefix=prefix, limit=limit).data()
                return [record['c'] for record in result]
        except Exception as e:
            logger.error(f"Error getting compounds: {str(e)}")
            raise

    def add_compound(self, formula: str, properties: Dict[str, Any] = None) -> Dict:
        try:
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
        except Exception as e:
            logger.error(f"Error adding compounds: {str(e)}")
            raise

    def add_reaction(self,
                     reactant: str,
                     product: str,
                     conditions: Dict[str, Any]) -> Dict:
        try:
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
        except Exception as e:
            logger.error(f"Error adding reaction: {str(e)}")
            raise

    def find_paths(self, start_compound: str, end_compound: str, max_depth: int = 5) -> List[Dict]:
        try:
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
        except Exception as e:
            logger.error(f"Error finding path: {str(e)}")
            raise