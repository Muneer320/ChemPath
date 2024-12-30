# ChemPath
**A Chemical Reaction Pathway Finder for Students**

## Project Overview
ChemPath is an educational tool designed to help high school students (particularly JEE/NEET aspirants) find step-by-step pathways between chemical compounds. The tool focuses on reactions and compounds relevant to their curriculum, making it more accessible than existing professional-grade solutions.

## Current Status
- Project Stage: Initial Development
- Last Updated: December 30, 2024
- Implementation Started: Basic architecture and database design

## Core Features (Planned)
1. **Reaction Pathway Finding**
   - Input: Starting compound and target compound
   - Output: Step-by-step reaction pathway(s)
   - Multiple pathway suggestions

2. **Educational Focus**
   - Limited to high school level reactions
   - Clear, step-by-step instructions
   - Reaction conditions and mechanisms
   - Safety information

## Technical Architecture

### Backend
- **Framework**: FastAPI
- **Database**: Neo4j (Graph Database)
- **Language**: Python 3.9+

### Current Directory Structure
```plaintext
ChemPath/
├── data/
├── docker/
|   ├── docker-compose.yml
|   └── Dockerfile
├── docs/
├── src/
|   ├── api/
|   |   └── main.py
|   └── database/
|       └── graph_manager.py
├── tests/
├── .env
├── .gitignore
├── firstPrototype.py
├── Project Documentation.md
├── README.md
├── relate.project.json
├── requirements.txt
└── test_connection.py
```

### Database Schema
Currently implemented as a graph structure:
- **Nodes**: Chemical compounds
- **Edges**: Reaction pathways
- **Properties**:
  - Compounds: formula, name, molecular weight, etc.
  - Reactions: conditions, temperature, reagents, etc.

## Implementation Progress

### Completed
1. Initial project structure
2. Basic Neo4j database setup
3. Basic GraphManager class implementation
4. Initial API endpoints

### In Progress
1. Chemical formula validation
2. Reaction pathfinding algorithms
3. Basic data collection

### Pending
1. User interface implementation
2. Reaction condition details
3. Path optimization
4. Testing suite
5. Documentation
6. Deployment setup

## Data Sources
Planning to collect data from:
- NCERT textbooks
- JEE previous papers
- NEET question banks
- Scrape some sites for molecules.
- `r/jeeneetards` doubts and other subs
- Standard organic chemistry reactions

## Reaction Examples (Sample Data)
```python
reactions_graph = {
    "CH3CH2OH": {  # Ethanol
        "CH3CHO": "Oxidation with K2Cr2O7/H+",
        "CH3CH2Br": "Treatment with HBr"
    },
    "CH3CHO": {  # Acetaldehyde
        "CH3COOH": "Oxidation with K2Cr2O7/H+"
    }
    # More to be added...
}
```

## Current Challenges
1. **Data Collection**
   - Need to build comprehensive reaction database
   - Ensure data accuracy

2. **Algorithm Optimization**
   - Efficient path finding
   - Handling multiple possible pathways

3. **Validation**
   - Chemical formula validation
   - Reaction feasibility checking
   - Safety constraints

## Next Steps
1. **Immediate Tasks**
   - Complete basic database population
   - Implement pathfinding algorithm
   - Add formula validation

2. **Short-term Goals**
   - Create test suite
   - Add more reactions
   - Implement basic UI

3. **Long-term Goals**
   - Mobile app development
   - Integration with educational platforms
   - Advanced features (3D structures, mechanism visualization)

## Development Setup Guide

### Prerequisites
- Python 3.9+
- Neo4j Desktop
- Docker (optional)

### Environment Setup
```bash
# Create virtual environment
uv venv chemPath
source chemPath\Scripts\activate  # If you're fancy: chemPath/bin/activate

# Install dependencies
uv pip install -r requirements.txt
```

### Configuration
Create `.env` file with:
```plaintext
NEO4J_URI=neo4j://localhost:7687
NEO4J_USER=neo4j
NEO4J_PASSWORD=your_password
API_PORT=8000
```

### Running the Project
```bash
# Start Neo4j
# Start the API
uvicorn src.api.main:app --reload
```

## API Endpoints (Planned)

### Basic Endpoints
1. `/find-path/`
   - POST request
   - Finds reaction pathway between compounds

2. `/compound/{formula}`
   - GET request
   - Returns compound information

3. `/suggest-compounds/{partial}`
   - GET request
   - Autocomplete suggestions

## Testing
- Unit tests for each component
- Integration tests for API endpoints
- Chemical validation tests

## Deployment
- Docker containers for consistency
- CI/CD pipeline (to be implemented)
- Scalability considerations

## Future Enhancements
1. Mobile application
2. Reaction mechanism visualization
3. Integration with molecular visualization tools
4. User accounts and progress tracking
5. Integration with educational platforms

## Notes
- Focus on educational use
- Maintain simplicity in interface
- Ensure accuracy of chemical data
- Regular updates to reaction database

---
*Documentation will be updated as project progresses*