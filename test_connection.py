# CHEMPATH/test_connection.py
from neo4j import GraphDatabase
import os
from dotenv import load_dotenv

load_dotenv()

uri = os.getenv("NEO4J_URI")
user = os.getenv("NEO4J_USER")
password = os.getenv("NEO4J_PASSWORD")

print(f"Connecting to {uri} as {user}...")

driver = GraphDatabase.driver(uri, auth=(user, password))

def test_connection():
    with driver.session() as session:
        result = session.run("MATCH (n) RETURN count(n) AS count")
        print(f"Connected successfully! Node count: {result.single()['count']}")

if __name__ == "__main__":
    try:
        test_connection()
    except Exception as e:
        print(f"Connection failed: {e}")
    finally:
        driver.close()