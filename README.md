# 🧪 ChemPath: Your Molecular GPS
*Because getting lost in organic chemistry is so last semester*

## Problem Statement
High school students preparing for JEE and NEET exams spend countless hours memorizing chemical conversion pathways. Current solutions are either:
- PhD-level tools (way too complex)
- Paywalled resources (goodbye pocket money, and still too complex)
- Random YouTube tutorials (a lot of time waste & 50% chance of getting rickrolled)

## My Solution
ChemPath: A student-friendly tool that shows you how to get from compound A to compound B, using only reactions you actually need to know. Like Maps, but for molecules!

### Key Features
- Step-by-step reaction pathways
- Multiple route options
- Focuses on high school curriculum
- Uses familiar reactions only
- Visual reaction maps
- Free access (because I'm nice)

## Technical Implementation

### Data Collection
1. Create compound database (my estimates: ~500-1000 compounds) from:
   - ~~NCERT textbooks~~
   - ~~JEE previous papers~~
   - ~~NEET question banks~~
   - Scrape some sites for molecules.
   - `r/jeeneetards` doubts and other subs
   - That one chemistry teacher's favorite reactions

### Architecture
- Graph-based system:
  - Nodes: Chemical compounds
  - Edges: Reaction mechanisms
  - Algorithm: A* search (or something similar/faster)

### Development Phases
1. Data Collection & Cleaning
2. Graph Database Setup
3. Pathfinding Algorithm Implementation
4. User Interface Development
5. Testing (lots of it, we don't want accidental TNT recipes)

## Example Workflow: Converting Ethanol to Ethanoic Acid

### User Interface (we can work on web or app bsed UI later)
```
Input:
Starting Compound: CH3CH2OH (Ethanol)
Target Compound: CH3COOH (Ethanoic Acid)
```

### System Processing
1. Graph Search Initiation:
   - Identifies ethanol node
   - Locates ethanoic acid node
   - Begins A* pathfinding

2. Found Pathways:
   ```
   Path 1 (Oxidation Route):
   CH3CH2OH → CH3CHO → CH3COOH
   Steps:
   1. Oxidation with K2Cr2O7/H+
   2. Oxidation with K2Cr2O7/H+ (continued)

   Path 2 (Alternative Route):
   CH3CH2OH → CH3CH2Br → CH3COOH
   Steps:
   1. Treatment with HBr
   2. Nucleophilic substitution with KOH
   3. Oxidation
   ```

### Output Display
```
Recommended Path: Path 1 (Shortest route)
Step-by-step Procedure:
1. Add K2Cr2O7 and H2SO4 to ethanol
2. Heat under reflux at 60°C
3. Distill to obtain acetaldehyde
4. Further oxidation with K2Cr2O7/H+
5. Heat under reflux
6. Collect ethanoic acid

Reaction Conditions:
- Temperature: 60°C
- Catalyst: H2SO4
- Oxidizing Agent: K2Cr2O7
```

## Market Potential
- Primary Users: JEE/NEET aspirants
- Secondary Users: Chemistry teachers (who can finally stop drawing the same reactions 50 times)
- Tertiary Users: Students who just want to pass their exams

## Challenges
- Dataset creation (our biggest hurdle)
- Data cleaning (because messy data is messier than a failed lab experiment)
- Ensuring educational relevance
- Keeping it simple (unlike your organic chemistry textbook)

## Resources Required
- Web scraping tools
- Database management system
- Graph algorithm implementation
- Development team
- Coffee (lots of it)

## Next Steps
1. Dataset compilation initiation
2. Proof of concept development
3. Basic algorithm testing
4. UI mockup creation
5. Initial user testing with students

## Conclusion
ChemPath has the potential to become an invaluable tool for chemistry students. It's like having a chemistry teacher in your pocket, minus the bad jokes (we'll add better ones).

---
*Note: No molecules were harmed in the making of this proposal*

*P.S. : If this was uncomfortable to read then you are not alone, blame Claude for writing it, and I don't have energy to rewrite it.*
