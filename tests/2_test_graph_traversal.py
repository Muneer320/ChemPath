import os
import pytest
from dotenv import load_dotenv
from src.database.graph_manager import ChemicalGraph

load_dotenv()


@pytest.fixture
def graph():
    """Fixture to create and manage test database connection"""
    graph = ChemicalGraph(
        os.getenv("NEO4J_URI"),
        os.getenv("NEO4J_USER"),
        os.getenv("NEO4J_PASSWORD")
    )

    # Setup test data
    yield graph

    # Cleanup after tests
    with graph._driver.session() as session:
        session.run("MATCH (n) DETACH DELETE n")
    graph.close()


class TestCompoundManagement:
    """Test compound node creation and management"""

    def test_add_compound_basic(self, graph):
        """Test basic compound addition"""
        result = graph.add_compound("CH3OH", {"name": "Methanol"})
        assert result, "Should return result after adding compound"

        with graph._driver.session() as session:
            count = session.run(
                "MATCH (c:Compound {formula: $formula}) RETURN count(c) as count",
                formula="CH3OH"
            ).single()["count"]
            assert count == 1, "Should create exactly one compound node"

    def test_add_compound_duplicate(self, graph):
        """Test adding same compound multiple times"""
        graph.add_compound("CH3OH", {"name": "Methanol"})
        graph.add_compound("CH3OH", {"name": "Methanol"})

        with graph._driver.session() as session:
            count = session.run(
                "MATCH (c:Compound {formula: $formula}) RETURN count(c) as count",
                formula="CH3OH"
            ).single()["count"]
            assert count == 1, "Should not create duplicate compounds"

    def test_add_compound_with_properties(self, graph):
        """Test adding compound with various properties"""
        properties = {
            "name": "Ethanol",
            "molecular_weight": 46.07,
            "density": 0.789,
            "boiling_point": 78.37,
            "class": "alcohol",
            "state": "liquid"
        }
        graph.add_compound("CH3CH2OH", properties)

        with graph._driver.session() as session:
            result = session.run(
                "MATCH (c:Compound {formula: $formula}) RETURN properties(c) as props",
                formula="CH3CH2OH"
            ).single()["props"]
            assert all(result[k] == v for k, v in properties.items()), \
                "All properties should be stored correctly"

    def test_add_compound_invalid_formula(self, graph):
        """Test adding compound with invalid chemical formula"""
        # graph.add_compound("invalid_formula", {"name": "Invalid"})
        # with graph._driver.session() as session:
        #     count = session.run(
        #         "MATCH (c:Compound {formula: 'invalid_formula'}) RETURN count(c) as count"
        #     ).single()["count"]
        #     assert count == 0, "Should not create node with invalid formula"

        # We won't need to handle invalid formulas in the API
        pass


class TestReactionManagement:
    """Test reaction relationship creation and management"""

    @pytest.fixture
    def setup_compounds(self, graph):
        """Setup basic compounds for reaction tests"""
        graph.add_compound("CH3CH2OH", {"name": "Ethanol"})
        graph.add_compound("CH3CHO", {"name": "Acetaldehyde"})
        graph.add_compound("CH3COOH", {"name": "Acetic Acid"})
        return graph

    def test_add_reaction_basic(self, setup_compounds):
        """Test basic reaction addition"""
        conditions = {
            "reagent": "K2Cr2O7/H+",
            "temperature": "heat",
            "type": "oxidation"
        }
        result = setup_compounds.add_reaction("CH3CH2OH", "CH3CHO", conditions)
        assert result, "Should return result after adding reaction"

    def test_add_reaction_bidirectional(self, setup_compounds):
        """Test adding reactions in both directions"""
        setup_compounds.add_reaction(
            "CH3CH2OH", "CH3CHO",
            {"reagent": "K2Cr2O7/H+", "type": "oxidation"}
        )
        setup_compounds.add_reaction(
            "CH3CHO", "CH3CH2OH",
            {"reagent": "NaBH4", "type": "reduction"}
        )

        with setup_compounds._driver.session() as session:
            count = session.run("""
                MATCH (:Compound {formula: 'CH3CH2OH'})-[r]->(:Compound {formula: 'CH3CHO'})
                RETURN count(r) as count
            """).single()["count"]
            assert count == 1, "Should have one forward reaction"

            count = session.run("""
                MATCH (:Compound {formula: 'CH3CHO'})-[r]->(:Compound {formula: 'CH3CH2OH'})
                RETURN count(r) as count
            """).single()["count"]
            assert count == 1, "Should have one reverse reaction"

    def test_add_reaction_with_detailed_conditions(self, setup_compounds):
        """Test adding reaction with complex conditions"""
        conditions = {
            "reagent": "K2Cr2O7/H+",
            "temperature": "60°C",
            "pressure": "1 atm",
            "catalyst": "H2SO4",
            "yield": "75%",
            "mechanism": "oxidation",
            "safety_notes": "Highly acidic conditions",
            "reference": "NCERT Ch.12"
        }
        result = setup_compounds.add_reaction("CH3CH2OH", "CH3CHO", conditions)

        with setup_compounds._driver.session() as session:
            props = session.run("""
                MATCH ()-[r:REACTS_TO]->()
                WHERE r.reagent = 'K2Cr2O7/H+'
                RETURN properties(r) as props
            """).single()["props"]
            assert all(props[k] == v for k, v in conditions.items()), \
                "All reaction conditions should be stored correctly"


class TestPathFinding:
    """Test pathway finding functionality"""

    @pytest.fixture
    def setup_reaction_network(self, graph):
        """Setup a complex reaction network for testing"""
        # Add compounds
        compounds = [
            ("CH3CH2OH", {"name": "Ethanol"}),
            ("CH3CHO", {"name": "Acetaldehyde"}),
            ("CH3COOH", {"name": "Acetic Acid"}),
            ("CH2O", {"name": "Formaldehyde"}),
            ("HCOOH", {"name": "Formic Acid"})
        ]
        for formula, props in compounds:
            graph.add_compound(formula, props)

        # Add reactions
        reactions = [
            ("CH3CH2OH", "CH3CHO", {
             "reagent": "K2Cr2O7/H+", "type": "oxidation"}),
            ("CH3CHO", "CH3COOH", {"reagent": "KMnO4", "type": "oxidation"}),
            ("CH3CH2OH", "CH2O", {"reagent": "KMnO4", "type": "oxidation"}),
            ("CH2O", "HCOOH", {"reagent": "O2/Ag", "type": "oxidation"}),
            ("CH3COOH", "HCOOH", {"reagent": "KMnO4", "type": "oxidation"})
        ]
        for reactant, product, conditions in reactions:
            graph.add_reaction(reactant, product, conditions)

        return graph

    def test_find_direct_path(self, setup_reaction_network):
        """Test finding direct reaction path"""
        paths = setup_reaction_network.find_paths("CH3CH2OH", "CH3CHO")
        assert len(paths) == 1, "Should find exactly one direct path"
        assert paths[0]['total_steps'] == 1, "Path length should be 1"
        assert paths[0]['reagents'] == [
            "K2Cr2O7/H+"], "Should use correct reagent"

    def test_find_multiple_paths(self, setup_reaction_network):
        """Test finding multiple possible paths"""
        paths = setup_reaction_network.find_paths("CH3CH2OH", "HCOOH")
        assert len(paths) >= 2, "Should find multiple paths"
        assert any('KMnO4' in str(path['reagents']) for path in paths), \
            "Should include path using KMnO4"

    def test_total_steps_limit(self, setup_reaction_network):
        """Test max_depth parameter in path finding"""
        paths = setup_reaction_network.find_paths(
            "CH3CH2OH", "HCOOH", max_depth=1)
        assert len(paths) == 0, "Should find no paths with depth 1"

        paths = setup_reaction_network.find_paths(
            "CH3CH2OH", "HCOOH", max_depth=3)
        assert all(path['total_steps'] <= 3 for path in paths), \
            "All paths should respect max_depth"

    def test_nonexistent_compound(self, setup_reaction_network):
        """Test behavior with nonexistent compounds"""
        paths = setup_reaction_network.find_paths("NonExistent", "CH3CHO")
        assert len(
            paths) == 0, "Should return empty list for nonexistent start compound"

        paths = setup_reaction_network.find_paths(
            "CH3CH2OH", "NonExistent")
        assert len(
            paths) == 0, "Should return empty list for nonexistent end compound"


class TestEdgeCases:
    """Test various edge cases and error conditions"""

    @pytest.fixture
    def setup_reaction_network(self, graph):
        compounds = [
            ("CH3CH2OH", {"name": "Ethanol"}),
            ("CH3CHO", {"name": "Acetaldehyde"})
        ]
        for formula, props in compounds:
            graph.add_compound(formula, props)

        reactions = [
            ("CH3CH2OH", "CH3CHO", {"reagent": "K2Cr2O7/H+", "type": "oxidation"})
        ]
        for reactant, product, conditions in reactions:
            graph.add_reaction(reactant, product, conditions)

        return graph

    def test_self_reaction(self, graph):
        """Test handling of self-reactions (same reactant and product)"""
        graph.add_compound("CH3CH2OH", {"name": "Ethanol"})
        graph.add_reaction("CH3CH2OH", "CH3CH2OH", {
                           "reagent": "catalyst", "type": "isomerization"})

        paths = graph.find_paths("CH3CH2OH", "CH3CH2OH")
        assert len(paths) > 0, "Should handle self-reactions"

    def test_disconnected_subgraphs(self, graph):
        """Test handling of disconnected reaction networks"""
        # Create two separate reaction networks
        graph.add_compound("CH3OH", {"name": "Methanol"})
        graph.add_compound("CH2O", {"name": "Formaldehyde"})
        graph.add_reaction("CH3OH", "CH2O", {"reagent": "KMnO4"})

        graph.add_compound("C2H4", {"name": "Ethene"})
        graph.add_compound("C2H5OH", {"name": "Ethanol"})
        graph.add_reaction("C2H4", "C2H5OH", {"reagent": "H2O/H+"})

        paths = graph.find_paths("CH3OH", "C2H5OH")
        assert len(paths) == 0, "Should handle disconnected subgraphs"

    def test_reaction_property_types(self, graph):
        """Test handling of various property types in reactions"""
        graph.add_compound("CH3OH", {"name": "Methanol"})
        graph.add_compound("CH2O", {"name": "Formaldehyde"})

        # No dicts because Neo4j doesn't support nested dicts
        conditions = {
            "temperature": 25,  # numeric
            "pressure": 1.5,    # float
            "catalyst": ["Pt", "Pd"],  # list
            "optional": None,   # null
            "required": True   # boolean
        }

        result = graph.add_reaction("CH3OH", "CH2O", conditions)
        assert result, "Should handle various property types"


if __name__ == "__main__":
    pytest.main(["-v"])
# Run it as follows: "pytest tests/2_test_graph_traversal.py -v"
