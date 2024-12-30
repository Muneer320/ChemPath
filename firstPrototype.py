from collections import deque


# Define a simple graph structure using dictionaries
reactions_graph = {
    "CH3OH": {  # Methanol
        "HCHO": "Oxidation with K2Cr2O7/H+",
        "CH3Cl": "Treatment with SOCl2"
    },
    "CH3CH2OH": {  # Ethanol
        "CH3CHO": "Oxidation with K2Cr2O7/H+",
        "CH3CH2Br": "Treatment with HBr",
        "CH2=CH2": "Conc. H2SO4, 443K"
    },
    "CH3CHO": {  # Acetaldehyde
        "CH3COOH": "Oxidation with K2Cr2O7/H+",
        "CH3CH2OH": "Reduction with NaBH4",
        "CH3CH(OH)CN": "Addition of HCN"
    },
    "CH3COOH": {  # Acetic acid
        "CH3COCl": "Treatment with SOCl2",
        "CH3CONH2": "NH3, heat",
        "CH3COOCH3": "CH3OH, H2SO4"
    },
    "CH3COCl": {  # Acetyl chloride
        "CH3CONH2": "NH3",
        "CH3COOCH3": "CH3OH"
    },
    "CH2=CH2": {  # Ethene
        "CH3CH2OH": "H2O, H3PO4, 300°C",
        # "CH3CH2OH": ["H2O, H3PO4, 300°C", "H2O/H2SO4"]  # To Ethanol (hydration) [We can make a list of possible reactions]
        "CH2Br-CH2Br": "Br2/CCl4"
    },
    "CH3CH2Br": {  # Bromoethane
        "CH3CH2OH": "NaOH (aq), heat",
        "CH2=CH2": "Alc. KOH, heat",
        "CH3CH2NH2": "NH3/alc"
    },
    "CH3CH2NH2": {  # Ethylamine
        "CH3CH2OH": "NaNO2/HCl, heat",
        "CH3CH2N2Cl": "NaNO2/HCl, 273-278K"
    },
    "HCHO": {  # Formaldehyde
        "HCOOH": "Oxidation with K2Cr2O7/H+",
        "CH3OH": "Reduction with NaBH4"
    },
    "CH3CH(OH)CN": {  # Cyanohydrin
        "CH3COOH": "H3O+, heat"
    },
    "CH3CONH2": {  # Acetamide
        "CH3COOH": "H3O+, heat",
        "CH3NH2": "Br2/NaOH"
    },
    "CH3COOCH3": {  # Methyl acetate
        "CH3COOH": "H3O+, heat",
        "CH3OH": "NaOH, heat"
    }
}

# Add additional compound information
compounds_info = {
    "CH3OH": {
        "name": "Methanol",
        "type": "alcohol",
        "molecular_weight": 32.04
    },
    "CH3CH2OH": {
        "name": "Ethanol",
        "type": "alcohol",
        "molecular_weight": 46.07
    },
    "CH3CHO": {
        "name": "Acetaldehyde",
        "type": "aldehyde",
        "molecular_weight": 44.05
    },
    "HCHO": {
        "name": "Formaldehyde",
        "type": "aldehyde",
        "molecular_weight": 30.03
    },
    "CH3COOH": {
        "name": "Acetic acid",
        "type": "carboxylic acid",
        "molecular_weight": 60.05
    }
    # We can add more as needed...
}

# Add reaction conditions
reaction_conditions = {
    "Oxidation with K2Cr2O7/H+": {
        "temperature": "60°C",
        "catalyst": "H2SO4",
        "oxidizing_agent": "K2Cr2O7",
        "conditions": "Heat under reflux",
        "precautions": "Handle dichromate with care",
        "color_change": "Orange to green solution",
        "time": "30-45 minutes"
    },
    
    "Treatment with SOCl2": {
        "temperature": "Room temperature",
        "reagent": "SOCl2",
        "conditions": "Anhydrous conditions",
        "by_product": "SO2, HCl gases",
        "precautions": "Perform in fume hood",
        "solvent": "Anhydrous ether or benzene",
        "time": "15-20 minutes"
    },
    
    "Conc. H2SO4, 443K": {
        "temperature": "443K (170°C)",
        "catalyst": "Conc. H2SO4",
        "conditions": "Heat",
        "mechanism": "E1 elimination",
        "yield": "~70-80%",
        "side_products": "Small amounts of ether",
        "time": "Varies with scale"
    },
    
    "Reduction with NaBH4": {
        "temperature": "0-25°C",
        "reducing_agent": "NaBH4",
        "solvent": "Methanol or ethanol",
        "work_up": "Quench with water",
        "precautions": "Control temperature",
        "time": "1-2 hours",
        "yield": "90-95%"
    },
    
    "Treatment with HBr": {
        "temperature": "25-30°C",
        "reagent": "48% HBr",
        "mechanism": "SN2 substitution",
        "catalyst": "Conc. H2SO4",
        "time": "2-3 hours",
        "work_up": "Extract with ether",
        "yield": "75-85%"
    },
    
    "Alc. KOH, heat": {
        "temperature": "80-90°C",
        "base": "KOH pellets",
        "solvent": "Ethanol",
        "mechanism": "E2 elimination",
        "time": "1-2 hours",
        "work_up": "Pour into water",
        "yield": "85-90%"
    },
    
    "NaNO2/HCl, 273-278K": {
        "temperature": "0-5°C",
        "reagents": ["NaNO2", "HCl"],
        "conditions": "Ice bath",
        "precautions": "Maintain temperature strictly",
        "mechanism": "Diazotization",
        "time": "20-30 minutes",
        "work_up": "Keep cold"
    },
    
    "Br2/CCl4": {
        "temperature": "Room temperature",
        "reagent": "Bromine",
        "solvent": "Carbon tetrachloride",
        "mechanism": "Addition",
        "color_change": "Brown to colorless",
        "time": "10-15 minutes",
        "yield": "90-95%"
    },
    
    "H2O/H2SO4": {
        "temperature": "80-90°C",
        "catalyst": "H2SO4",
        "conditions": "Heat, pressure",
        "mechanism": "Electrophilic addition",
        "time": "Several hours",
        "yield": "60-70%",
        "side_products": "Possible polymers"
    },
    
    "NH3, heat": {
        "temperature": "100-120°C",
        "reagent": "Ammonia gas",
        "conditions": "Sealed tube",
        "pressure": "2-3 atm",
        "time": "3-4 hours",
        "yield": "70-80%",
        "work_up": "Cool, filter"
    },
    
    "CH3OH, H2SO4": {
        "temperature": "60-70°C",
        "catalyst": "Conc. H2SO4",
        "conditions": "Reflux",
        "mechanism": "Nucleophilic acyl substitution",
        "time": "2-3 hours",
        "yield": "75-85%",
        "equilibrium": "Use excess alcohol"
    },
    
    "NaOH (aq), heat": {
        "temperature": "80-90°C",
        "base": "40% NaOH",
        "conditions": "Reflux",
        "mechanism": "SN2 substitution",
        "time": "1-2 hours",
        "work_up": "Extract product",
        "yield": "80-85%"
    },
    
    "H3O+, heat": {
        "temperature": "90-100°C",
        "acid": "Dilute HCl or H2SO4",
        "conditions": "Reflux",
        "mechanism": "Hydrolysis",
        "time": "2-4 hours",
        "work_up": "Cool, extract",
        "pH_control": "Important"
    },
    
    "Br2/NaOH": {
        "temperature": "60-70°C",
        "reagents": ["Bromine", "NaOH"],
        "mechanism": "Hofmann degradation",
        "conditions": "Basic medium",
        "time": "1-2 hours",
        "work_up": "Acidify, extract",
        "yield": "60-70%"
    },
    
    "Addition of HCN": {
        "temperature": "10-15°C",
        "reagents": ["HCN or KCN", "Dilute HCl"],
        "catalyst": "Small amount of base",
        "mechanism": "Nucleophilic addition",
        "precautions": "Handle HCN with extreme care",
        "time": "30-45 minutes",
        "pH_control": "Critical"
    },
    
    "H2O, H3PO4, 300°C": {
        "temperature": "300°C",
        "catalyst": "H3PO4",
        "pressure": "High pressure",
        "mechanism": "Hydration",
        "time": "Continuous process",
        "yield": "70-75%",
        "industrial_scale": "Yes"
    },
    
    "NH3/alc": {
        "temperature": "120-130°C",
        "reagent": "Alcoholic ammonia",
        "pressure": "In sealed tube",
        "mechanism": "SN2 substitution",
        "time": "4-5 hours",
        "yield": "65-75%",
        "work_up": "Evaporate solvent"
    }
    # Add more as needed...
}


# Currently using a simple BFS, we upgrade to better/faster algorithms later
def find_path(graph, start, end):
    # Returns path and reactions if found, None if no path exists
    if start not in graph:
        return None

    queue = deque([[start]])
    visited = {start}

    while queue:
        path = queue.popleft()
        compound = path[-1]

        if compound == end:
            # Extract reactions for this path
            reactions = []
            for i in range(len(path)-1):
                reactions.append(graph[path[i]][path[i+1]])
            return path, reactions

        for next_compound in graph.get(compound, {}):
            if next_compound not in visited:
                visited.add(next_compound)
                queue.append(path + [next_compound])

    return None



# Basic CLI interface [We can improve this later]
def main():
    print("\nChemPath - Find your reaction pathway!")

    while True:
        # Example: CH3CH2OH ---→ CH3CONH2
        
        start = input("Enter starting compound (or 'quit' to exit): ").strip()
        if start.lower() == 'quit':
            break

        end = input("Enter target compound: ").strip()

        result = find_path(reactions_graph, start, end)

        # You can use reaction_conditions and compounds_info to display more information and with better formatting
        if result:
            path, reactions = result

            print("\n\t", start, "---→", end)

            print("\nPath found!")
            for i in range(len(path)-1):
                print(f"{i+1}. {path[i]} -→ {path[i+1]}")
                print(f"  Reaction: {reactions[i]}")
                if reactions[i] in reaction_conditions:
                    for key, value in reaction_conditions[reactions[i]].items():
                        print(f"    {key.title()}: {value}")
        else:
            print("\nNo path found between these compounds.")

        print("\n")


if __name__ == "__main__":
    main()
