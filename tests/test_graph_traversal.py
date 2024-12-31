import os
import pytest
from dotenv import load_dotenv
from src.database.graph_manager import ChemicalGraph
from src.database.data_ingestion import ALCOHOLS_OXIDATION, ingest_data

# Load environment variables
load_dotenv()

@pytest.fixture
def graph():
    """Fixture to create and populate test database"""
    # Initialize graph connection
    graph = ChemicalGraph(
        os.getenv("NEO4J_URI"),
        os.getenv("NEO4J_USER"),
        os.getenv("NEO4J_PASSWORD")
    )
    
    # Ingest test data
    print("Ingesting test data...")  # Add this line
    ingest_data([ALCOHOLS_OXIDATION], clear_existing=False)
    
    # Verify data ingestion  # Add these lines
    with graph._driver.session() as session:
        count = session.run("MATCH (n) RETURN count(n) as count").single()["count"]
        print(f"Number of nodes in database: {count}")
    
    yield graph
    
    # Cleanup
    graph.close()

def test_single_step_path(graph):
    """Test finding a direct reaction path between two compounds"""
    # Test ethanol to acetaldehyde path
    paths = graph.find_all_paths("CH3CH2OH", "CH3CHO")
    assert len(paths) > 0, "Should find at least one path"
    
    # Verify path properties
    path = paths[0]
    assert path['path_length'] == 1, "Should be a direct path"
    assert 'K2Cr2O7/H+' in str(path['reagents']) or 'CuO' in str(path['reagents']), \
        "Should use expected reagents"

def test_multi_step_path(graph):
    """Test finding a path that requires multiple reactions"""
    # Test ethanol to acetic acid path
    paths = graph.find_all_paths("CH3CH2OH", "CH3COOH")
    assert len(paths) > 0, "Should find at least one path"
    
    # Verify path properties
    path = paths[0]
    assert path['path_length'] == 2, "Should be a two-step path"
    assert 'oxidation' in str(path), "Should be an oxidation pathway"

def test_multiple_paths(graph):
    """Test finding multiple possible paths between compounds"""
    # Test ethanol to acetaldehyde (should have multiple oxidation routes)
    paths = graph.find_all_paths("CH3CH2OH", "CH3CHO")
    assert len(paths) > 1, "Should find multiple paths"
    
    # Verify different reagents are used
    reagents = set()
    for path in paths:
        reagents.update(path['reagents'])
    assert len(reagents) > 1, "Should find paths with different reagents"

def test_nonexistent_path(graph):
    """Test behavior when no path exists"""
    # Test path between unconnected compounds
    paths = graph.find_all_paths("CH3OH", "CH3COOH")
    assert len(paths) == 0, "Should not find a path between unconnected compounds"

def test_path_with_specific_conditions(graph):
    """Test finding paths with specific reaction conditions"""
    with graph._driver.session() as session:
        result = session.run("""
            MATCH path = (start:Compound {formula: $start})-[r:REACTS_TO*]->(end:Compound {formula: $end})
            WHERE ALL(rel IN r WHERE rel.temperature = 'heat')
            RETURN path
        """, start="CH3CH2OH", end="CH3COOH").data()
        
        assert len(result) > 0, "Should find paths using heated reactions"

def test_cycle_detection(graph):
    """Test that the system can handle cycles in reaction paths"""
    # First create a cycle by adding a reverse reaction
    graph.add_reaction(
        "CH3CHO",
        "CH3CH2OH",
        {
            "reagent": "NaBH4",
            "temperature": "room temperature",
            "type": "reduction"
        }
    )
    
    # Now test path finding with cycles
    paths = graph.find_all_paths("CH3CH2OH", "CH3CH2OH", max_depth=3)
    assert len(paths) > 0, "Should find cyclic paths"
    
    # Verify at least one cycle exists
    cycle_exists = False
    for path in paths:
        if path['path_length'] > 1:  # Length > 1 indicates a cycle
            cycle_exists = True
            break
    assert cycle_exists, "Should detect at least one reaction cycle"

def test_shortest_path(graph):
    """Test finding the shortest path between compounds"""
    # Add a longer alternative path
    graph.add_reaction(
        "CH3CH2OH",
        "CH2O",
        {"reagent": "KMnO4", "type": "oxidation"}
    )
    graph.add_reaction(
        "CH2O",
        "CH3COOH",
        {"reagent": "O2", "type": "oxidation"}
    )
    
    paths = graph.find_all_paths("CH3CH2OH", "CH3COOH")
    assert paths[0]['path_length'] <= paths[-1]['path_length'], \
        "Paths should be ordered by length"

if __name__ == "__main__":
    pytest.main([__file__])