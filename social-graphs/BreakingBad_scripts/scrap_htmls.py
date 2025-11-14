from bs4 import BeautifulSoup
import json
import os
import re
from collections import defaultdict
import networkx as nx
import matplotlib.pyplot as plt

# Path to html files
html_files_path = '/home/juanma/Downloads/BreakingBad_subtitles/Breaking_bad_scripts'

def extract_scene_characters(scene_description):
    """Extract character names from scene descriptions"""
    words = scene_description.split()
    potential_names = []
    
    # Expanded list of known Breaking Bad characters
    known_characters = [
        'Walt', 'Walter', 'Jesse', 'Mike', 'Skyler', 'Hank', 
        'Marie', 'Saul', 'Gus', 'Jr', 'Flynn', 'Todd',
        'Badger', 'Skinny', 'Pete', 'Combo', 'Jane',
        'Lydia', 'Tuco', 'Bogdan', 'Ted', 'Gomez',
        'Andrea', 'Brock', 'Holly', 'Huell', 'Kuby'
    ]
    
    for word in words:
        clean_word = word.strip('*,.:;()[]')
        if clean_word in known_characters:
            potential_names.append(clean_word)
    
    return list(set(potential_names))

def normalize_character_name(name):
    """Normalize character names to a standard form"""
    name = name.upper().strip()
    
    # Handle common variations
    name_mappings = {
        'WALTER': 'WALT',
        'FLYNN': 'JR',
        'WALTER JR': 'JR',
        'SKINNY PETE': 'PETE',
    }
    
    return name_mappings.get(name, name)

def parse_script(html_content):
    """Parse the HTML to extract character interactions from Genius scripts"""
    soup = BeautifulSoup(html_content, 'html.parser')
    
    # Find the lyrics container (where the script content is)
    content = soup.find('div', {'data-lyrics-container': 'true'})
    
    if not content:
        # Try alternative selectors
        content = soup.find('div', class_=re.compile(r'Lyrics__Container'))
    
    if not content:
        print("Warning: Could not find script content in HTML")
        return []
    
    scenes = []
    current_scene_chars = set()
    
    # Get all text, preserving structure
    for element in content.descendants:
        if element.name == 'br':
            continue
            
        if isinstance(element, str):
            line = element.strip()
            
            if not line:
                continue
            
            # Check if it's a scene description (starts and ends with *)
            if line.startswith('*') and line.endswith('*'):
                # Save previous scene if it has multiple characters
                if len(current_scene_chars) >= 2:
                    scenes.append(list(current_scene_chars))
                
                # Start new scene
                scene_desc = line.strip('*')
                current_scene_chars = set(extract_scene_characters(scene_desc))
            
            # Check for character dialogue (NAME: dialogue)
            elif ':' in line and not line.startswith('http'):
                parts = line.split(':', 1)
                char_name = parts[0].strip()
                
                # Valid character name heuristics:
                # - All caps or title case
                # - Not too long (< 20 chars)
                # - Mostly alphabetic
                if (char_name and 
                    len(char_name) < 20 and 
                    (char_name.isupper() or char_name.istitle()) and
                    sum(c.isalpha() for c in char_name) / len(char_name) > 0.6):
                    
                    normalized_name = normalize_character_name(char_name)
                    current_scene_chars.add(normalized_name)
    
    # Don't forget the last scene
    if len(current_scene_chars) >= 2:
        scenes.append(list(current_scene_chars))
    
    return scenes

def build_character_network(all_scenes):
    """Build a network of character interactions"""
    character_connections = defaultdict(lambda: defaultdict(int))
    
    for scene in all_scenes:
        # For each pair of characters in the scene, add a connection
        for i, char1 in enumerate(scene):
            for char2 in scene[i+1:]:
                # Normalize names
                c1 = normalize_character_name(char1)
                c2 = normalize_character_name(char2)
                
                # Add bidirectional connection
                character_connections[c1][c2] += 1
                character_connections[c2][c1] += 1
    
    return character_connections

def save_to_json(character_connections, filename='character_network.json'):
    """Save the character network to JSON"""
    # Convert defaultdict to regular dict for JSON serialization
    network = {}
    for char, connections in character_connections.items():
        network[char] = dict(connections)
    
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(network, f, indent=2)
    
    print(f"Saved network to {filename}")
    return network

def create_graph(character_connections, output_file='character_network.png'):
    """Create and visualize the character network graph"""
    G = nx.Graph()
    
    # Add edges with weights
    for char1, connections in character_connections.items():
        for char2, weight in connections.items():
            if char1 < char2:  # Avoid duplicate edges
                G.add_edge(char1, char2, weight=weight)
    
    # Create visualization
    plt.figure(figsize=(16, 12))
    
    # Use spring layout with more iterations for better spacing
    pos = nx.spring_layout(G, k=3, iterations=100, seed=42)
    
    # Calculate node sizes based on degree
    degrees = dict(G.degree())
    node_sizes = [degrees[node] * 100 + 300 for node in G.nodes()]
    
    # Draw nodes with size based on connections
    nx.draw_networkx_nodes(G, pos, 
                          node_size=node_sizes, 
                          node_color='lightblue', 
                          alpha=0.9,
                          edgecolors='navy',
                          linewidths=2)
    
    # Draw edges with varying thickness based on weight
    edges = G.edges()
    weights = [G[u][v]['weight'] for u, v in edges]
    max_weight = max(weights) if weights else 1
    
    # Normalize weights for visualization
    edge_widths = [max(0.5, (weight / max_weight) * 8) for weight in weights]
    
    nx.draw_networkx_edges(G, pos, 
                          width=edge_widths,
                          alpha=0.5,
                          edge_color='gray')
    
    # Draw labels
    nx.draw_networkx_labels(G, pos, 
                           font_size=9, 
                           font_weight='bold',
                           font_family='sans-serif')
    
    plt.axis('off')
    plt.title('Breaking Bad Character Interaction Network', 
              fontsize=16, 
              fontweight='bold',
              pad=20)
    plt.tight_layout()
    plt.savefig(output_file, dpi=300, bbox_inches='tight', facecolor='white')
    print(f"Graph saved to {output_file}")
    
    return G

def main():
    """Main execution function"""
    
    print("Breaking Bad Character Network Analysis")
    print("=" * 50)
    
    # Get all HTML files from the directory
    html_files = [f for f in os.listdir(html_files_path) if f.endswith('.html')]
    html_files.sort()  # Sort for consistent processing
    
    if not html_files:
        print(f"Error: No HTML files found in {html_files_path}")
        return
    
    print(f"\nFound {len(html_files)} HTML files")
    
    # Parse all HTML files
    print("\nParsing scripts...")
    all_scenes = []
    
    for filename in html_files:
        filepath = os.path.join(html_files_path, filename)
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                html_content = f.read()
                scenes = parse_script(html_content)
                all_scenes.extend(scenes)
                print(f"  {filename}: {len(scenes)} scenes found")
        except Exception as e:
            print(f"  Error parsing {filename}: {e}")
    
    print(f"\nTotal scenes extracted: {len(all_scenes)}")
    
    if not all_scenes:
        print("Error: No scenes were extracted. Check the HTML structure.")
        return
    
    # Build character network
    print("\nBuilding character network...")
    character_connections = build_character_network(all_scenes)
    
    # Save to JSON
    print("\nSaving to JSON...")
    save_to_json(character_connections)
    
    # Create graph visualization
    print("\nCreating graph visualization...")
    G = create_graph(character_connections)
    
    # Print statistics
    print("\n" + "=" * 50)
    print("NETWORK STATISTICS")
    print("=" * 50)
    print(f"Total characters: {len(character_connections)}")
    print(f"Total connections: {G.number_of_edges()}")
    print(f"Average connections per character: {2 * G.number_of_edges() / len(G.nodes()):.2f}")
    
    print("\nTop 10 most connected characters:")
    centrality = nx.degree_centrality(G)
    sorted_chars = sorted(centrality.items(), key=lambda x: x[1], reverse=True)[:10]
    for i, (char, score) in enumerate(sorted_chars, 1):
        degree = dict(G.degree())[char]
        print(f"  {i:2d}. {char:15s} - {degree} connections (centrality: {score:.3f})")
    
    # Additional network metrics
    print("\nNetwork Metrics:")
    try:
        print(f"  Density: {nx.density(G):.3f}")
        print(f"  Average clustering coefficient: {nx.average_clustering(G):.3f}")
        if nx.is_connected(G):
            print(f"  Average shortest path length: {nx.average_shortest_path_length(G):.3f}")
        else:
            print(f"  Network is disconnected ({nx.number_connected_components(G)} components)")
    except:
        pass
    
    print("\n" + "=" * 50)
    print("Analysis complete!")

if __name__ == "__main__":
    main()