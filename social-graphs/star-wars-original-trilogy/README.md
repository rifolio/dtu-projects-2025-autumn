# Star Wars Original Trilogy - Social Network Analysis

This project analyzes the social networks present in the Star Wars original trilogy scripts using NetworkX and creates two distinct network visualizations.

## Project Structure

```
star-wars-original-trilogy/
├── star-wars-scrape.ipynb              # Phase 1: Data scraping and preprocessing
├── star-wars-network-analysis.ipynb    # Phase 2: Network creation and visualization
├── data/                               # Output directory for JSON data files
│   ├── character_connections.json      # Character-character connections
│   └── location_characters.json        # Character-location mappings
├── figures/                            # Output directory for network visualizations
│   ├── character_network.png
│   └── bipartite_network.png
├── networks/                           # Output directory for exported network files
│   ├── character_network.gml
│   ├── bipartite_network.gml
│   └── network_statistics.json
└── README.md                           # This file
```

## Notebooks

### 1. star-wars-scrape.ipynb

**Purpose**: Scrapes Star Wars scripts from imsdb.com, extracts character and location data, and generates JSON files.

**Key Features**:
- Fetches all 3 original trilogy scripts from imsdb.com
- Parses HTML to extract:
  - Scene headings (locations)
  - Character names appearing in each scene
- Character name normalization (handles variations like "LUKE", "Luke", "Luke Skywalker" → "Luke Skywalker")
- Location name cleaning (removes INT/EXT prefixes, standardizes formatting)
- Detects which characters appear together in scenes
- Generates two JSON output files

**Output Files**:
- `data/character_connections.json`: Bidirectional character connections with scene counts
- `data/location_characters.json`: Mapping of locations to characters present there

**Required Packages**:
- requests
- beautifulsoup4
- json (built-in)
- pathlib (built-in)
- collections (built-in)

### 2. star-wars-network-analysis.ipynb

**Purpose**: Creates and visualizes two networks from the scraped data.

**Networks Created**:

1. **Character-Character Network**
   - Nodes: Characters from the Star Wars scripts
   - Edges: Connections between characters who share scenes
   - Edge weights: Number of scenes the two characters share
   - Type: Undirected weighted graph
   - Visualization: Force-directed layout (NetworkX spring_layout)

2. **Character-Location Bipartite Network**
   - Nodes: Characters and locations
   - Character nodes (blue): Main Star Wars characters
   - Location nodes (red): Scenes/locations where action takes place
   - Edges: Connections from characters to locations they appear in
   - Edge weights: Number of times a character appears at a location
   - Type: Undirected bipartite weighted graph
   - Visualization: Force-directed layout

**Key Analyses**:
- Network density and connectivity metrics
- Degree distribution (most connected characters)
- Shortest path analysis
- Location popularity (most visited places)
- Character mobility (characters in most locations)
- Network statistics exported to JSON

**Required Packages**:
- networkx
- matplotlib
- numpy
- json (built-in)
- pathlib (built-in)

## How to Run

### Prerequisites

Make sure you have the conda environment "sg" with all required packages installed:

```bash
conda activate sg
pip install requests beautifulsoup4 networkx matplotlib numpy
```

### Execution Steps

1. **Run the scraping notebook first**:
   ```bash
   jupyter execute star-wars-scrape.ipynb --kernel=sg
   ```
   This will create the JSON data files in the `data/` directory.

2. **Run the network analysis notebook**:
   ```bash
   jupyter execute star-wars-network-analysis.ipynb --kernel=sg
   ```
   This will generate visualizations in `figures/` and network files in `networks/`.

Alternatively, you can open both notebooks in Jupyter Lab/Notebook and run them cell by cell:
```bash
jupyter lab star-wars-scrape.ipynb
jupyter lab star-wars-network-analysis.ipynb
```

## Data Files Generated

### character_connections.json
```json
{
  "Character Name": {
    "Other Character 1": 15,
    "Other Character 2": 8,
    ...
  },
  ...
}
```
- Keys: Character names (canonicalized)
- Values: Dictionary of other characters and the number of scenes they share

### location_characters.json
```json
{
  "Location Name": ["Character 1", "Character 2", ...],
  ...
}
```
- Keys: Cleaned location names
- Values: List of characters appearing at that location

## Network Statistics

The analysis generates network statistics including:
- Number of nodes and edges
- Network density
- Connected components
- Average degree
- Most connected characters
- Most visited locations
- Character mobility patterns

## Character Name Normalization

The scraper includes a comprehensive mapping of character name variations:
- "LUKE", "Luke", "Luke Skywalker" → "Luke Skywalker"
- "HAN", "Han Solo" → "Han Solo"
- "VADER", "Darth Vader" → "Darth Vader"
- And many more variations

Unknown characters are kept with cleaned formatting (title case).

## Location Name Cleaning

Scene headings are cleaned to remove:
- INT/EXT prefixes
- Time of day indicators (DAY, NIGHT, CONTINUOUS)
- Parenthetical details (MOVING, etc.)
- Extra whitespace

Example: `INT. LUKE'S HOUSE - LIVING ROOM - DAY` → `Luke's House - Living Room`

## Force-Directed Layout Configuration

Both networks use NetworkX's `spring_layout` with these parameters:
- `k=2` for character network (or `k=1.5` for bipartite)
- `iterations=50` for convergence
- `seed=42` for reproducible results
- `weight='weight'` to respect edge weights

This creates naturally clustered visualizations where frequently-connected characters appear close together.

## Output Visualizations

- **character_network.png**: Shows character relationships with node size representing connection count
- **bipartite_network.png**: Shows characters and their locations with node coloring for distinction

## Next Steps

Potential extensions:
- Analyze network communities/clusters
- Calculate centrality measures (betweenness, closeness, etc.)
- Temporal analysis across the three movies
- Community detection algorithms
- Character importance ranking
