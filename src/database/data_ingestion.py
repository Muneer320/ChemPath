import os
from dotenv import load_dotenv
from typing import Dict, List, Any
from src.database.graph_manager import ChemicalGraph


# Load environment variables
load_dotenv()

# ===================== DATA DEFINITIONS =====================

ALCOHOLS_OXIDATION = {
    "compounds": [
        {"formula": "CH3OH", "name": "Methanol",
         "molecular_weight": 32.04, "class": "alcohol"},
        {"formula": "CH2O", "name": "Formaldehyde"},
        {"formula": "HCOOH", "name": "Formic Acid"},
        {"formula": "CH3CH2OH", "name": "Ethanol",
         "molecular_weight": 46.07, "class": "alcohol"},
        {"formula": "CH3CH2CH2OH", "name": "Propanol",
         "molecular_weight": 60.10, "class": "alcohol"},
        {"formula": "CH3CHO", "name": "Acetaldehyde"},
        {"formula": "CH3COOH", "name": "Acetic Acid"},
        {"formula": "C6H5OH", "name": "Phenol",
         "molecular_weight": 94.11, "class": "alcohol"},
    ],
    "reactions": [
        {
            "reactant": "CH3OH",
            "product": "CH2O",
            "conditions": {
                "reagent": "K2Cr2O7/H+",
                "temperature": "heat",
                "type": "oxidation"
            }
        },
        {
            "reactant": "CH2O",
            "product": "HCOOH",
            "conditions": {
                "reagent": "K2Cr2O7/H+",
                "temperature": "heat",
                "type": "oxidation"
            }
        },
        {
            "reactant": "CH3CH2OH",
            "product": "CH3CHO",
            "conditions": {
                "reagent": "K2Cr2O7/H+",
                "temperature": "heat",
                "type": "oxidation",
                "mechanism": "primary alcohol oxidation"
            }
        },
        {
            "reactant": "CH3CH2OH",
            "product": "CH3COOH",
            "conditions": {
                "reagent": "KMnO4/H+",
                "temperature": "heat",
                "type": "oxidation",
                "mechanism": "complete alcohol oxidation"
            }
        },
        # Multiple pathways for ethanol oxidation
        {
            "reactant": "CH3CH2OH",
            "product": "CH3CHO",
            "conditions": {
                "reagent": "K2Cr2O7/H+",
                "temperature": "heat",
                "type": "oxidation"
            }
        },
        {
            "reactant": "CH3CH2OH",
            "product": "CH3CHO",
            "conditions": {
                "reagent": "CuO",
                "temperature": "300°C",
                "type": "oxidation"
            }
        },
        {
            "reactant": "CH3CHO",
            "product": "CH3COOH",
            "conditions": {
                "reagent": "K2Cr2O7/H+",
                "temperature": "heat",
                "type": "oxidation"
            }
        }
    ]
}

ALKENE_ADDITIONS = {
    "compounds": [
        {"formula": "CH3CH2OH", "name": "Ethanol"},
        {"formula": "CH3CH2Cl", "name": "Chloroethane"},
        {"formula": "CH3CH2Br", "name": "Bromoethane"},
        {"formula": "CH2CH2", "name": "Ethene",
         "molecular_weight": 28.05, "class": "alkene"},
        {"formula": "CH3CHCH2", "name": "Propene",
         "molecular_weight": 42.08, "class": "alkene"},
        {"formula": "CH3CH2CHCH2", "name": "Butene",
            "molecular_weight": 56.11, "class": "alkene"}
    ],
    "reactions": [
        {
            "reactant": "CH2CH2",
            "product": "CH3CH2OH",
            "conditions": {
                "reagent": "H2O/H+",
                "temperature": "room temperature",
                "type": "addition"
            }
        },
        {
            "reactant": "CH2CH2",
            "product": "CH3CH2Cl",
            "conditions": {
                "reagent": "HCl",
                "temperature": "room temperature",
                "type": "addition"
            }
        },
        {
            "reactant": "CH2CH2",
            "product": "CH3CH2Br",
            "conditions": {
                "reagent": "HBr",
                "temperature": "room temperature",
                "type": "addition"
            }
        },
        {
            "reactant": "CH3CHCH2",
            "product": "CH3CCH",
            "conditions": {
                "reagent": "Br2/KOH",
                "temperature": "heat",
                "type": "elimination",
                "mechanism": "dehydrohalogenation"
            }
        },

    ]
}

ALKYNE = {
    "compounds": [
        {"formula": "CHCH", "name": "Ethyne",
         "molecular_weight": 26.04, "class": "alkyne"},
        {"formula": "CH3CCH", "name": "Propyne",
         "molecular_weight": 40.06, "class": "alkyne"}
    ],
    "reactions": [
        {
            "reactant": "CHCH",
            "product": "CH2CH2",
            "conditions": {
                "reagent": "H2/Pd",
                "temperature": "room temperature",
                "type": "reduction",
                "mechanism": "catalytic hydrogenation"
            }
        }
    ]
}

ALDEHYDE_KETONE = {
    "compounds": [
        {"formula": "HCHO", "name": "Formaldehyde",
         "molecular_weight": 30.03, "class": "aldehyde"},
        {"formula": "CH3CHO", "name": "Acetaldehyde",
         "molecular_weight": 44.05, "class": "aldehyde"},
        {"formula": "C6H5CHO", "name": "Benzaldehyde",
         "molecular_weight": 106.12, "class": "aldehyde"},
        {"formula": "CH3COCH3", "name": "Acetone",
         "molecular_weight": 58.08, "class": "ketone"},
        {"formula": "CH3COCH2CH3", "name": "Butanone",
         "molecular_weight": 72.11, "class": "ketone"}
    ],
    "reactions": [
        {
            "reactant": "CH3CHO",
            "product": "CH3COOH",
            "conditions": {
                "reagent": "K2Cr2O7/H+",
                "temperature": "heat",
                "type": "oxidation",
                "mechanism": "aldehyde oxidation"
            }
        },
        {
            "reactant": "CH3CHO",
            "product": "CH3CH2OH",
            "conditions": {
                "reagent": "NaBH4",
                "temperature": "room temperature",
                "type": "reduction",
                "mechanism": "hydride reduction"
            }
        },
        {
            "reactant": "CH3COCH3",
            "product": "CH3CH(OH)CH3",
            "conditions": {
                "reagent": "LiAlH4",
                "temperature": "room temperature",
                "type": "reduction",
                "mechanism": "hydride reduction"
            }
        }
    ]
}

CARBOXYLIC_ACID = {
    "compounds": [
        {"formula": "HCOOH", "name": "Formic acid",
         "molecular_weight": 46.03, "class": "carboxylic_acid"},
        {"formula": "CH3COOH", "name": "Acetic acid",
         "molecular_weight": 60.05, "class": "carboxylic_acid"},
        {"formula": "C6H5COOH", "name": "Benzoic acid",
         "molecular_weight": 122.12, "class": "carboxylic_acid"}
    ],
    "reactions": []
}

ALKYL_HALIDES = {
    "compounds": [
        {"formula": "CH3Cl", "name": "Chloromethane",
         "molecular_weight": 50.49, "class": "alkyl_halide"},
        {"formula": "CH3CH2Br", "name": "Bromoethane",
         "molecular_weight": 108.97, "class": "alkyl_halide"},
        {"formula": "CH3I", "name": "Iodomethane",
         "molecular_weight": 141.94, "class": "alkyl_halide"}
    ],
    "reactions": [
        {
            "reactant": "CH3CH2OH",
            "product": "CH3CH2Cl",
            "conditions": {
                "reagent": "SOCl2",
                "temperature": "heat",
                "type": "substitution",
                "mechanism": "nucleophilic substitution"
            }
        }
    ]
}

AMINES = {
    "compounds": [
        {"formula": "CH3NH2", "name": "Methylamine",
         "molecular_weight": 31.06, "class": "amine"},
        {"formula": "C6H5NH2", "name": "Aniline",
         "molecular_weight": 93.13, "class": "amine"}
    ],
    "reactions": [
        {
            "reactant": "CH3Cl",
            "product": "CH3NH2",
            "conditions": {
                "reagent": "NH3",
                "temperature": "heat",
                "type": "substitution",
                "mechanism": "nucleophilic substitution"
            }
        },
    ]
}

ETHERS = {
    "compounds": [
        {"formula": "CH3OCH3", "name": "Dimethyl ether",
         "molecular_weight": 46.07, "class": "ether"},
        {"formula": "CH3CH2OCH2CH3", "name": "Diethyl ether",
         "molecular_weight": 74.12, "class": "ether"}
    ],
    "reactions": [
        {
            "reactant": "CH3OH",
            "product": "CH3OCH3",
            "conditions": {
                "reagent": "H2SO4",
                "temperature": "140°C",
                "type": "dehydration",
                "mechanism": "acid-catalyzed dehydration"
            }
        },
    ]
}

ESTER = {
    "compounds": [
        {"formula": "CH3COOCH3", "name": "Methyl acetate",
         "molecular_weight": 74.08, "class": "ester"},
        {"formula": "CH3COOCH2CH3", "name": "Ethyl acetate",
         "molecular_weight": 88.11, "class": "ester"}
    ],
    "reactions": [{
        "reactant": "CH3COOH",
        "product": "CH3COOCH3",
        "conditions": {
            "reagent": "CH3OH/H+",
            "temperature": "heat",
            "type": "condensation",
            "mechanism": "fischer esterification"
        }
    },
    ]
}

MISC = {
    "compounds": [

    ],
    "reactions": [
        {
            "reactant": "C6H5NH2",
            "product": "C6H5OH",
            "conditions": {
                "reagent": "NaNO2/HCl, H2O",
                "temperature": "0-5°C",
                "type": "diazotization-hydrolysis",
                "mechanism": "sandmeyer type reaction"
            }
        }
    ]
}


# Add more reaction sets as needed...


# Collection of all data sets
REACTION_SETS = [
    ALCOHOLS_OXIDATION,
    ALKENE_ADDITIONS,
    ALKYNE,
    ALDEHYDE_KETONE,
    CARBOXYLIC_ACID,
    ALKYL_HALIDES,
    AMINES,
    ETHERS,
    ESTER,
    MISC
    # Add more sets here...
]


def ingest_data(reaction_sets: List[Dict[str, Any]], clear_existing: bool = False) -> None:
    """
    Ingest chemical data into Neo4j database.

    Args:
        reaction_sets: List of dictionaries containing compounds and reactions
        clear_existing: If True, clears all existing data before ingestion
    """
    # Initialize graph connection
    graph = ChemicalGraph(
        os.getenv("NEO4J_URI"),
        os.getenv("NEO4J_USER"),
        os.getenv("NEO4J_PASSWORD")
    )

    try:
        # Clear existing data if requested
        if clear_existing:
            with graph._driver.session() as session:
                session.run("MATCH (n) DETACH DELETE n")
                print("Cleared existing data")

        # Process each reaction set
        for reaction_set in reaction_sets:
            # Add compounds
            print("\nAdding compounds...")
            for compound in reaction_set["compounds"]:
                result = graph.add_compound(compound["formula"], compound)
                print(f"Added compound: {compound['formula']}")

            # Add reactions
            print("\nAdding reactions...")
            for reaction in reaction_set["reactions"]:
                result = graph.add_reaction(
                    reaction["reactant"],
                    reaction["product"],
                    reaction["conditions"]
                )
                print(f"Added reaction: {reaction['reactant']} -> {reaction['product']} "
                      f"using {reaction['conditions']['reagent']}")

    except Exception as e:
        print(f"Error during data ingestion: {e}")
        raise
    finally:
        graph.close()


def verify_ingestion():
    """Verify that data was properly ingested by running some test queries."""
    graph = ChemicalGraph(
        os.getenv("NEO4J_URI"),
        os.getenv("NEO4J_USER"),
        os.getenv("NEO4J_PASSWORD")
    )

    try:
        with graph._driver.session() as session:
            # Count nodes and relationships
            node_count = session.run(
                "MATCH (n) RETURN count(n) as count").single()["count"]
            rel_count = session.run(
                "MATCH ()-[r]->() RETURN count(r) as count").single()["count"]

            print(f"\nVerification Results:")
            print(f"Total compounds: {node_count}")
            print(f"Total reactions: {rel_count}")

    finally:
        graph.close()


if __name__ == "__main__":
    # Example usage
    print("Starting data ingestion...")
    ingest_data(REACTION_SETS, clear_existing=False)
    verify_ingestion()

# Run this script from root as : "uv run python -m src.database.data_ingestion"