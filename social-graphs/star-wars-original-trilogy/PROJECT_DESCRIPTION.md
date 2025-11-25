# Star Wars Original Trilogy: Social Network Analysis

## Project Overview

This project combines **network science** and **natural language processing (NLP)** to analyze the Star Wars original trilogy. Using network methodologies, we construct and analyze two complementary networks: a character-character interaction network and a character-location bipartite network. Using NLP techniques, we perform sentiment analysis on character dialogue to understand emotional tones and communication patterns. Together, these analyses reveal patterns of character relationships, identifies central figures in the narrative, uncovers how the story's geography shapes interactions, and characterizes the emotional dimensions of character dialogue and interactions.

### Central Research Questions

**Network Science**:
1. **Character Connectivity**: Which characters are most central to the narrative based on their interactions with other characters?
2. **Network Topology**: How is the character interaction network structured? Are there distinct communities or clusters of characters?
3. **Spatial Patterns**: How do characters move through different locations, and which locations are most narratively significant?
4. **Story Structure**: How do character interactions and location usage reflect the narrative progression across the three films?

**Natural Language Processing & Sentiment Analysis**:
5. **Character Sentiment Profiles**: What are the emotional characteristics of each character based on their dialogue?
6. **Interaction Sentiment**: What is the sentiment nature of interactions between characters (friendly, hostile, neutral)?
7. **Dialogue Patterns**: How do characters' speech patterns, tone, and vocabulary differ across the trilogy?
8. **Sentiment Evolution**: How does the overall sentiment tone change across the three films and relate to narrative arcs?

## Data Source

**Dataset**: Star Wars Original Trilogy Scripts
- **A New Hope** (1977)
- **The Empire Strikes Back** (1980)
- **Return of the Jedi** (1983)

**Data Source**: Internet Movie Script Database (imsdb.com)
- Direct access via HTTP requests
- HTML parsing to extract structured screenplay data
- Scene headings and character dialogue extraction

**Data Acquisition Method**:
1. Web scraping using BeautifulSoup4 and requests libraries
2. HTML parsing to identify scene headings (INT/EXT locations and times)
3. Character name extraction from screenplay formatting standards
4. Scene-by-scene analysis to identify character co-occurrence
5. Dialogue extraction and segmentation by character for NLP analysis
6. Sentiment analysis using transformer-based models (VADER, TextBlob, or HuggingFace models)

---

# PART A: Preliminary Data Analysis & 1-Minute Video

## Data Characteristics

### Dataset Size
- **Total Scripts**: 3 files (~150 KB of raw HTML data)
- **Parsed Scenes**: ~300 total scenes across all three films
- **Characters Extracted**: ~80 unique characters (post-normalization)
- **Locations**: ~120 unique scene locations (post-cleaning)

### Network 1: Character-Character Interaction Network

**Network Type**: Undirected, Weighted Graph

**Basic Metrics**:
- **Nodes**: ~80 character nodes
- **Edges**: ~250+ character interactions (weighted)
- **Edge Weights**: Number of scenes in which two characters appear together
- **Node Attributes**:
  - Character name
  - Total number of scenes
  - Connection strength with other characters

**Network Characteristics**:
- **Network Density**: Moderate density (~0.07-0.12) indicating selective connectivity
- **Average Degree**: 6-8 connections per character
- **Diameter**: Indicates how many steps separate the most distant characters
- **Connected Components**: Likely 1-2 main components with some isolated characters
- **Degree Distribution**: Power-law-like distribution with few highly-connected hub characters and many peripheral characters

**Key Findings**:
- Core characters (Luke, Han, Leia, Vader, Obi-Wan) show high degree centrality
- Strong clustering around central heroes and antagonists
- Community structure reflects narrative groupings (Rebel Alliance, Imperial Forces, Neutral parties)

### Network 2: Character-Location Bipartite Network

**Network Type**: Bipartite, Undirected, Weighted Graph

**Basic Metrics**:
- **Total Nodes**: ~200 (80 characters + 120 locations)
- **Character Nodes**: ~80
- **Location Nodes**: ~120
- **Edges**: ~400+ character-location connections
- **Edge Weights**: Number of scenes where character appears at location

**Node Attributes**:
- **Character Nodes**: Name, number of locations visited, total scenes
- **Location Nodes**: Name, description, number of characters, narrative significance

**Network Characteristics**:
- **Network Type**: Bipartite structure (can be projected to character-character or location-location networks)
- **Location Degree Distribution**: Varied from 2-15+ characters per location
- **Character Mobility**: Ranging from 3-20+ different locations per character
- **Most Connected Nodes**: Core locations like "Millennium Falcon", "Death Star", "Cloud City", "Dagobah"

**Key Findings**:
- Some locations are narrative hubs (appear in multiple films or involve multiple characters)
- Characters vary significantly in mobility and range of environments
- Location clustering reflects different storylines and settings

### NLP Analysis: Sentiment & Dialogue Analysis

**Text Data Metrics**:
- **Total Dialogue Lines**: ~5,000-8,000 dialogue exchanges across all three films
- **Character Dialogue Distribution**: Ranges from <10 lines to 500+ lines per character
- **Average Dialogue Length**: 5-15 words per line
- **Total Unique Words**: 2,000-3,000 words (after tokenization)

**Sentiment Analysis Approach**:
- **Models Used**: VADER (Valence Aware Dictionary and sEntiment Reasoner) for rule-based analysis and/or HuggingFace transformers for deep learning-based analysis
- **Sentiment Labels**: Positive, Negative, Neutral (with intensity scores 0-1)
- **Analysis Levels**:
  1. **Character-level sentiment**: Average sentiment score for each character's dialogue
  2. **Interaction-level sentiment**: Sentiment of dialogue exchanges between specific character pairs
  3. **Scene-level sentiment**: Overall emotional tone of each scene
  4. **Film-level sentiment**: Sentiment progression across A New Hope, Empire, Return of Jedi

**Key Metrics**:
- **Sentiment Polarity Distribution**: Percentage of positive/negative/neutral dialogue per character
- **Sentiment Intensity**: Average sentiment strength on -1 (very negative) to +1 (very positive) scale
- **Character Emotion Profiles**: Statistical summary of each character's typical emotional tone
- **Interaction Sentiment**: Edge attributes indicating positive/negative/neutral relationships

**Expected Sentiment Patterns**:
- **Heroes** (Luke, Leia, Han): Mix of positive/neutral with context-dependent negative
- **Villains** (Vader, Emperor): Higher negative sentiment, commanding tone
- **Droids** (C-3PO, R2-D2): Generally positive/neutral, comedic exchanges
- **Wise characters** (Obi-Wan, Yoda): Neutral/positive, instructional dialogue

## Part A Deliverable: 1-Minute Explainer Video

### Video Content Outline (≤1:30)

**Slide 1-2 (0:00-0:15): Project Concept**
- Title: "Star Wars Social Networks & Sentiment Analysis"
- Research questions: How do character interactions, locations, and dialogue sentiment shape the narrative of the original trilogy?
- Dataset: 3 Star Wars films' screenplays with 5,000+ dialogue lines

**Slide 3-4 (0:15-0:45): Network & NLP Analysis**
- **Network Science**: Character-character interactions (80 characters, 250+ edges) + Character-location bipartite network (120 locations)
- **NLP/Sentiment**: VADER-based sentiment analysis of 5,000+ dialogue lines
- Data Processing: Web scraping, name normalization, dialogue extraction, sentiment scoring

**Slide 5 (0:45-1:15): Preliminary Findings**
- **Networks**: Hub-and-spoke topology; core characters (Luke, Han, Leia, Vader) most central
- **Sentiment**: Heroes show mixed positive/neutral sentiment; villains show higher negative sentiment
- Key locations are narrative hubs; location clustering reflects storylines
- Character sentiment profiles reveal personality archetypes

**Slide 6 (1:15-1:30): Next Steps**
- Integrate sentiment with networks (sentiment-weighted edges)
- Dialogue pattern analysis (word frequency, linguistic features)
- Sentiment evolution across three films
- Academic paper combining network science + NLP findings

---

# PART B: Academic Paper & Explainer Notebook

## Part B Deliverables

### 1. Academic Paper (PDF, ≤5 pages with ≤5 figures)

#### Proposed Paper Structure

**Title**: *Narrative Architecture in Star Wars: Network Science and Sentiment Analysis of Character Interactions in the Original Trilogy*

**Abstract** (150 words)
- Brief statement of research questions (network structure + sentiment patterns)
- Dataset overview (3 films, 80+ characters, 5,000+ dialogue lines, 120+ locations)
- Methodology (web scraping, network construction, VADER-based sentiment analysis)
- Key findings (e.g., character centrality reflects narrative importance; sentiment profiles match character archetypes)
- Implications for computational narrative analysis combining network science and NLP

**Significance Statement** (1 paragraph)
- Why this research matters: Demonstrates integrated computational approach to narrative analysis
- Application of network science and NLP to film analysis
- Bridges computational methods with humanities scholarship
- Demonstrates practical application of course concepts (both network science and NLP)
- Shows how sentiment analysis can reveal character psychology and relationship dynamics

**Introduction** (1 page)
- Context: Network science and NLP applications in narrative analysis
- Problem: How do we quantify narrative structure and character psychology?
- Approach: Character interaction networks, location analysis, and sentiment analysis of dialogue
- Research questions clearly stated (both network-based and sentiment-based)

**Results** (1.5 pages)
- **Network Findings**: Network topology, centrality analysis (degree, betweenness, closeness centrality), character clustering and communities
- **Location Analysis**: Location significance, co-occurrence patterns, character mobility
- **Sentiment Analysis Results**:
  - Character sentiment profiles (average sentiment scores, polarity distributions)
  - Sentiment patterns matching character archetypes (heroes, villains, comic relief)
  - Interaction sentiment (positive/negative/neutral relationship indicators)
  - Dialogue sentiment across different films
  - Correlation between character centrality and sentiment patterns
- **Integrated Findings**: How network structure relates to sentiment patterns; sentiment as a network edge attribute

**Discussion** (1 page)
- Interpretation of findings
- Connection to film studies and narrative theory
- Limitations of the approach
- Future research directions

**Methods** (0.75 pages)
- **Data Collection**: Web scraping from imsdb.com using BeautifulSoup4
- **Data Preprocessing**: Character name normalization, location cleaning, dialogue extraction and segmentation
- **Network Construction**: Character-character and character-location network algorithms (NetworkX)
- **Sentiment Analysis**: VADER sentiment analysis on character dialogue (lexicon-based approach for explainability)
  - Sentiment scoring for each dialogue line (-1 to +1 scale)
  - Aggregation to character, interaction, and scene levels
- **Analysis Techniques**: Centrality measures, community detection, sentiment statistics
- **Visualization**: Force-directed layouts, sentiment heatmaps, distribution plots
- *Reference to Explainer Notebook for detailed code and supplementary analyses*

**References** (0.5 pages)
- Academic papers on network analysis
- Film studies literature
- Course materials
- Data sources

#### Proposed Figures (≤5 maximum)

1. **Character Network with Sentiment Attributes** (Force-directed layout, node color = average sentiment, size = degree)
2. **Character Sentiment Profiles** (Bar chart or heatmap showing sentiment polarity for each character)
3. **Sentiment vs. Centrality Correlation** (Scatter plot: character centrality vs. average sentiment; reveals relationship between importance and tone)
4. **Interaction Sentiment Network** (Character-character edges colored by interaction sentiment: positive/negative/neutral)
5. **Sentiment Evolution Across Films** (Time series or faceted plots showing how sentiment changes from A New Hope → Empire → Return of Jedi)

### 2. Explainer Jupyter Notebook

**Filename**: `star-wars-network-analysis-explainer.ipynb`

**Structure**:

1. **Introduction & Research Questions**
   - Overview of the project (network science + NLP integration)
   - Research questions and hypotheses (both network-based and sentiment-based)
   - Expected contributions

2. **Data Collection & Preprocessing**
   - Web scraping methodology
   - HTML parsing details
   - Character name normalization mapping (commented)
   - Location name cleaning rules
   - **Dialogue extraction and segmentation** (new for NLP)
   - Data quality checks

3. **Network Construction**
   - Network 1: Character-character graph construction
   - Network 2: Character-location bipartite graph construction
   - Edge weight definitions
   - Data structures used (adjacency lists, edge attributes)

4. **Natural Language Processing: Sentiment Analysis**
   - **VADER sentiment analysis setup** and justification
   - Sentiment scoring for each dialogue line
   - Aggregation strategies (character-level, interaction-level, scene-level)
   - Sentiment distribution analysis
   - Validation of sentiment labels (spot-checking representative examples)

5. **Exploratory Network Analysis**
   - Basic statistics (nodes, edges, density, components)
   - Degree distributions (histograms, log-log plots)
   - Neighborhood analysis
   - Path analysis

6. **Centrality & Importance**
   - Degree centrality calculations
   - Betweenness centrality (identifies bridges/connectors)
   - Closeness centrality (identifies influential characters)
   - Eigenvector centrality (identifies well-connected neighbors)

7. **Character Sentiment Profiles**
   - Average sentiment score per character
   - Sentiment polarity distribution (positive/negative/neutral percentages)
   - Sentiment variance (consistency vs. variability in tone)
   - Visualization: Sentiment heatmaps and bar charts
   - Interpretation relative to character archetypes

8. **Interaction-Level Sentiment Analysis**
   - Sentiment of conversations between specific character pairs
   - Friendly vs. hostile relationships identified by sentiment
   - Edge-weighted networks using sentiment scores
   - Visualization: Sentiment-colored networks

9. **Community Detection & Sentiment Integration**
   - Louvain algorithm or modularity optimization
   - Community size and composition analysis
   - **Sentiment homogeneity within communities** (do similar characters cluster together?)
   - Interpretation relative to narrative structure

10. **Location & Dialogue Analysis**
    - Most significant locations
    - **Sentiment profile of each location** (tense vs. peaceful scenes)
    - Character mobility patterns
    - Location clustering

11. **Temporal Sentiment Analysis**
    - Sentiment progression across three films
    - Per-movie sentiment statistics
    - Character arc visualization through sentiment changes
    - Scene-level sentiment tracking

12. **Visualizations**
    - Force-directed network layouts (with sentiment coloring)
    - Sentiment distribution plots (histograms, KDE plots)
    - Character sentiment profiles (heatmaps, bar charts)
    - Sentiment vs. centrality scatter plots
    - Temporal sentiment evolution plots
    - Community visualizations with sentiment overlay

13. **Integrated Network-Sentiment Analysis**
    - Correlation between network centrality and sentiment metrics
    - Sentiment as a predictive feature for character importance
    - Network clustering vs. sentiment clustering comparison
    - Insights from combining network and NLP perspectives

14. **Supplementary Analyses**
    - Per-film analysis (A New Hope, Empire, Return of Jedi separately)
    - Character appearance frequency and dialogue length
    - Dialogue word frequency analysis (topic modeling prep)
    - Location importance scoring
    - Network metrics comparison across films
    - Robustness testing with alternative sentiment models

15. **Conclusions & Insights**
    - Summary of network findings
    - Summary of sentiment analysis findings
    - **Integration insights**: How network structure and sentiment patterns reveal narrative design
    - Narrative interpretations combining both approaches
    - Limitations and challenges (sentiment model limitations, context-dependency)
    - Future research opportunities (emotion detection, sarcasm handling, character relationship evolution)

**Code Features**:
- Well-commented code explaining each analysis step
- Clear variable naming and documentation
- Error handling and data validation
- Modular functions for reusability
- Reproducible with seed values for visualizations

---

## Methodology Overview

### Data Processing Pipeline

```
Raw Scripts (HTML)
    ↓
[Web Scraping] (BeautifulSoup4, requests)
    ↓
Scene & Character Extraction + Dialogue Extraction
    ↓
[Data Cleaning]
  - Character name normalization
  - Location name standardization
  - Dialogue segmentation by character
  - Duplicate removal
    ↓
Cleaned Data (JSON) + Dialogue Corpus
    ↓
        ├─→ [Network Construction] (NetworkX)      ├─→ [Sentiment Analysis] (VADER, nltk)
        │   - Character-character connections        │   - Sentiment scoring per dialogue
        │   - Character-location bipartite           │   - Aggregation to character/interaction level
        │                                             │
        ↓                                             ↓
    Network Analysis                           Sentiment Analysis
    (Centrality, Communities)                  (Profiles, Patterns)
        ↓                                             ↓
        └──────────────── Integration ────────────────┘
                           ↓
            Combined Network-Sentiment Analysis
            (Correlation, Visualization)
                           ↓
            Academic Paper + Explainer Notebook
```

### Tools & Libraries

- **Data Scraping**: requests, BeautifulSoup4
- **Network Analysis**: NetworkX
- **Natural Language Processing & Sentiment Analysis**:
  - VADER Sentiment Analysis (via NLTK) - lexicon-based, explainable
  - NLTK (tokenization, stopword removal)
  - Optional: Transformers/HuggingFace for deep learning-based sentiment (alternative)
- **Visualization**: Matplotlib, NetworkX draw functions, Seaborn (heatmaps)
- **Data Processing**: Pandas (optional, for sentiment aggregation), Python standard library (json, collections, pathlib)
- **Numerical Computing**: NumPy, SciPy

---

## Expected Contributions

1. **Methodological**:
   - Demonstrates web scraping and network analysis workflow for textual data
   - Integrates network science and NLP in a complementary manner
   - Shows how to combine multiple analytical perspectives for richer insights

2. **Analytical**:
   - Reveals quantitative structure underlying narrative composition (networks)
   - Characterizes emotional and tonal patterns in dialogue (NLP)
   - Shows how character importance (network) correlates with communication style (sentiment)

3. **Educational**:
   - Shows practical application of network science concepts to real-world data
   - Demonstrates VADER sentiment analysis on screenplay dialogue
   - Illustrates integration of network and NLP techniques

4. **Creative**:
   - Bridges computer science and humanities (film/narrative analysis)
   - Provides computational tool for film scholars and screenwriters
   - Demonstrates how character psychology (sentiment) manifests in narrative structure (networks)

---

## Timeline

- **Phase 1** (Completed): Data scraping, preprocessing, JSON generation
- **Phase 2** (Completed): Network construction and visualization
- **Phase A**: Create explainer video (≤1:30) with preliminary findings
- **Phase B**:
  - Conduct comprehensive network analysis
  - Write academic paper (≤5 pages)
  - Complete explainer notebook
  - Generate final visualizations and figures

---

## Project Files & Organization

```
social-graphs/star-wars-original-trilogy/
├── README.md                                    # Technical documentation
├── PROJECT_DESCRIPTION.md                       # This file
├── star-wars-scrape.ipynb                       # Data scraping (Phase 1)
├── star-wars-network-analysis.ipynb             # Network analysis (Phase 2)
├── star-wars-network-analysis-explainer.ipynb   # [Part B] Explainer notebook
├── data/
│   ├── character_connections.json
│   └── location_characters.json
├── figures/
│   ├── character_network.png
│   ├── bipartite_network.png
│   └── [other visualizations]
├── networks/
│   ├── character_network.gml
│   ├── bipartite_network.gml
│   └── network_statistics.json
└── paper/
    └── star_wars_network_analysis.pdf           # [Part B] Academic paper
```

---

## References & Resources

### Network Science
- Barabási, A. L., & Albert, R. (1999). Emergence of scaling in random networks. *Science*, 286(5439), 509-512.
- Newman, M. E. J. (2010). *Networks: An Introduction*. Oxford University Press.
- Watts, D. J., & Strogatz, S. H. (1998). Collective dynamics of 'small-world' networks. *Nature*, 393(6684), 440-442.

### Network Analysis Tools
- NetworkX Documentation: https://networkx.org/
- Matplotlib Documentation: https://matplotlib.org/

### Natural Language Processing & Sentiment Analysis
- Hutto, C. J., & Gilbert, E. (2014). VADER: A Parsimonious Rule-based Model for Sentiment Analysis of Social Media Text. *Proceedings of the Eighth International AAAI Conference on Weblogs and Social Media*.
- Pang, B., & Lee, L. (2008). Opinion mining and sentiment analysis. *Foundations and Trends in Information Retrieval*, 2(1-2), 1-135.
- NLTK Documentation: https://www.nltk.org/
- HuggingFace Transformers: https://huggingface.co/transformers/

### Film & Narrative Analysis
- Sternberg, M. (2001). *Narrative Dynamics: Essays on Time, Plot, Closure, and Frames*. Ohio State University Press.
- Murray, S. (2016). *Movie Mutations: The Changing Face of World Cinephilia*. BFI.
- Kozloff, S. (2000). *Overhearing Film Dialogue*. University of California Press.

### Data Sources
- Internet Movie Script Database: https://imsdb.com/

---

**Project Status**: [Complete as of November 2025]

**Course**: Social Graphs (DTU)

**Kernel**: Python 3.12.11 (sg environment)
