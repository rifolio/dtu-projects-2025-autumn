import requests
from bs4 import BeautifulSoup
import json
import re
import time
from collections import defaultdict
import networkx as nx
import matplotlib.pyplot as plt

# Your list of URLs with metadata
episodes = [
    # Season 1
    {'url': 'https://genius.com/Breaking-bad-pilot-script-annotated', 'season': 1, 'name': 'Pilot'},
    {'url': 'https://genius.com/Breaking-bad-cats-in-the-bag-script-annotated', 'season': 1, 'name': 'Cats in the Bag'},
    {'url': 'https://genius.com/Breaking-bad-crazy-handful-of-nothin-script-annotated', 'season': 1, 'name': 'Crazy Handful of Nothin'},
    # Season 2
    {'url': 'https://genius.com/Breaking-bad-seven-thirty-seven-script-annotated', 'season': 2, 'name': 'Seven Thirty Seven'},
    {'url': 'https://genius.com/Breaking-bad-over-script-annotated', 'season': 2, 'name': 'Over'},
    # Season 3
    {'url': 'https://genius.com/Breaking-bad-fly-annotated', 'season': 3, 'name': 'Fly'},
    {'url': 'https://genius.com/Breaking-bad-half-measures-annotated', 'season': 3, 'name': 'Half Measures'},
    {'url': 'https://genius.com/Breaking-bad-full-measure-annotated', 'season': 3, 'name': 'Full Measure'},
    # Season 4
    {'url': 'https://genius.com/Breaking-bad-cornered-script-annotated', 'season': 4, 'name': 'Cornered'},
    {'url': 'https://genius.com/Breaking-bad-crawl-space-annotated', 'season': 4, 'name': 'Crawl Space'},
    {'url': 'https://genius.com/Breaking-bad-end-times-annotated', 'season': 4, 'name': 'End Times'},
    # Season 5
    {'url': 'https://genius.com/Breaking-bad-say-my-name-script-annotated', 'season': 5, 'name': 'Say My Name'},
    {'url': 'https://genius.com/Breaking-bad-felina-script-annotated', 'season': 5, 'name': 'Felina'},
    {'url': 'https://genius.com/Breaking-bad-granite-state-script-annotated', 'season': 5, 'name': 'Granite State'},
    {'url': 'https://genius.com/Breaking-bad-ozymandias-script-annotated', 'season': 5, 'name': 'Ozymandias'},
    {'url': 'https://genius.com/Breaking-bad-tohajiilee-script-annotated', 'season': 5, 'name': 'Tohajiilee'},
    {'url': 'https://genius.com/Breaking-bad-blood-money-script-annotated', 'season': 5, 'name': 'Blood Money'}
]

def download_page(episode_data):
    """Download a single page and save as HTML with proper naming"""
    url = episode_data['url']
    season = episode_data['season']
    name = episode_data['name']
    
    # Create filename: S01E01_Pilot.html
    filename = f"S{season:02d}_{name.replace(' ', '_')}.html"
    
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(response.text)
        
        print(f"Downloaded: {filename}")
        return filename, True
    except Exception as e:
        print(f"Error downloading {url}: {e}")
        return filename, False

def extract_scene_characters(scene_description):
    """Extract character names from scene descriptions"""
    # Look for names in the scene description (typically capitalized)
    # This is a simple heuristic - you may need to adjust based on actual format
    words = scene_description.split()
    potential_names = []
    
    # Common character names to look for
    known_characters = [
        'Walt', 'Walter', 'Jesse', 'Mike', 'Skyler', 'Hank', 
        'Marie', 'Saul', 'Gus', 'Jr', 'Flynn', 'Todd'
    ]
    
    for word in words:
        clean_word = word.strip('*,.:;')
        if clean_word in known_characters:
            potential_names.append(clean_word)
    
    return list(set(potential_names))

def parse_script(html_content):
    """Parse the HTML to extract character interactions"""
    soup = BeautifulSoup(html_content, 'html.parser')
    
    # Find the main content area (adjust selector based on actual page structure)
    # This is a generic approach - you'll need to inspect the actual HTML
    content = soup.find('div', class_='lyrics') or soup.find('div', class_='Lyrics__Container')
    
    if not content:
        return []
    
    scenes = []
    current_scene_chars = []
    
    # Split by scene descriptions (text in italics or asterisks)
    text = content.get_text()
    lines = text.split('\n')
    
    for line in lines:
        line = line.strip()
        if not line:
            continue
            
        # Check if it's a scene description (starts with *)
        if line.startswith('*') and line.endswith('*'):
            scene_desc = line.strip('*')
            current_scene_chars = extract_scene_characters(scene_desc)
            if len(current_scene_chars) >= 2:
                scenes.append(current_scene_chars)
        
        # Also check for character dialogue (typically NAME: dialogue)
        elif ':' in line:
            parts = line.split(':', 1)
            char_name = parts[0].strip().upper()
            # Add to current scene if it's a valid character name
            if char_name and len(char_name) < 20 and char_name.isalpha():
                if char_name not in current_scene_chars:
                    current_scene_chars.append(char_name)
    
    return scenes

def build_character_network(all_scenes):
    """Build a network of character interactions"""
    character_connections = defaultdict(lambda: defaultdict(int))
    
    for scene in all_scenes:
        # For each pair of characters in the scene, add a connection
        for i, char1 in enumerate(scene):
            for char2 in scene[i+1:]:
                # Normalize names
                c1 = char1.upper()
                c2 = char2.upper()
                
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

def create_graph(character_connections, output_file='character_network.png'):
    """Create and visualize the character network graph"""
    G = nx.Graph()
    
    # Add edges with weights
    for char1, connections in character_connections.items():
        for char2, weight in connections.items():
            if char1 < char2:  # Avoid duplicate edges
                G.add_edge(char1, char2, weight=weight)
    
    # Create visualization
    plt.figure(figsize=(15, 10))
    pos = nx.spring_layout(G, k=2, iterations=50)
    
    # Draw nodes
    nx.draw_networkx_nodes(G, pos, node_size=1000, node_color='lightblue', alpha=0.9)
    
    # Draw edges with varying thickness based on weight
    edges = G.edges()
    weights = [G[u][v]['weight'] for u, v in edges]
    max_weight = max(weights) if weights else 1
    
    for (u, v), weight in zip(edges, weights):
        nx.draw_networkx_edges(G, pos, [(u, v)], 
                              width=weight/max_weight * 5,
                              alpha=0.6)
    
    # Draw labels
    nx.draw_networkx_labels(G, pos, font_size=10, font_weight='bold')
    
    plt.axis('off')
    plt.tight_layout()
    plt.savefig(output_file, dpi=300, bbox_inches='tight')
    print(f"Graph saved to {output_file}")
    
    return G

def main():
    """Main execution function"""
    
    # Step 1: Download pages
    print("Step 1: Downloading pages...")
    downloaded_files = []
    for episode_data in episodes:
        filename, success = download_page(episode_data)
        if success:
            downloaded_files.append(filename)
        time.sleep(1)  # Be respectful with requests
    
    # # Step 2: Parse all downloaded pages
    # print("\nStep 2: Parsing scripts...")
    # all_scenes = []
    
    # for filename in downloaded_files:
    #     try:
    #         with open(filename, 'r', encoding='utf-8') as f:
    #             html_content = f.read()
    #             scenes = parse_script(html_content)
    #             all_scenes.extend(scenes)
    #             print(f"Parsed {filename}: {len(scenes)} scenes found")
    #     except FileNotFoundError:
    #         print(f"File {filename} not found, skipping...")
    
    # # Step 3: Build character network
    # print("\nStep 3: Building character network...")
    # character_connections = build_character_network(all_scenes)
    
    # # Step 4: Save to JSON
    # print("\nStep 4: Saving to JSON...")
    # save_to_json(character_connections)
    
    # # Step 5: Create graph visualization
    # print("\nStep 5: Creating graph visualization...")
    # G = create_graph(character_connections)
    
    # # Print some statistics
    # print("\n=== Network Statistics ===")
    # print(f"Total characters: {len(character_connections)}")
    # print(f"Total connections: {G.number_of_edges()}")
    # print(f"\nTop 10 most connected characters:")
    
    # centrality = nx.degree_centrality(G)
    # sorted_chars = sorted(centrality.items(), key=lambda x: x[1], reverse=True)[:10]
    # for char, score in sorted_chars:
    #     print(f"  {char}: {score:.3f}")

if __name__ == "__main__":
    main()