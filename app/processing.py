import networkx as nx
import pandas as pd
import community.community_louvain as community_louvain
import matplotlib.pyplot as plt
import io
from io import BytesIO
from typing import Dict, Any


def load_graph_data(filepath: str) -> nx.Graph:
    """
    Loads graph data from a CSV file.

    Args:
        filepath: Path to the CSV file.

    Returns:
        A NetworkX graph object.

    Raises:
        FileNotFoundError: If the file does not exist.
        ValueError: If required columns are missing.
    """
    try:
        # Load a subset of data to ensure speed
        # Using departure_id and return_id as per Databike.csv structure
        df = pd.read_csv(filepath, nrows=1000)

        required_columns = ['departure_id', 'return_id']
        if not all(col in df.columns for col in required_columns):
            raise ValueError(f"CSV must contain columns: {required_columns}")

        G = nx.from_pandas_edgelist(df, source='departure_id', target='return_id')
        return G
    except FileNotFoundError:
        raise
    except Exception as e:
        raise ValueError(f"Error loading graph data: {str(e)}")


def detect_communities(G: nx.Graph) -> Dict[str, Any]:
    """
    Detects communities in the graph using the Louvain algorithm.

    Args:
        G: A NetworkX graph object.

    Returns:
        A dictionary containing modularity score, number of communities, and total nodes.
    """
    if not G or len(G.nodes) == 0:
        return {
            "modularity_score": 0.0,
            "total_communities_detected": 0,
            "total_nodes": 0
        }

    # This is the Louvain algorithm (Fast optimization)
    partition = community_louvain.best_partition(G)

    # Calculate modularity (A metric for quality)
    modularity = community_louvain.modularity(partition, G)

    # Count communities
    num_communities = len(set(partition.values()))

    return {
        "modularity_score": modularity,
        "total_communities_detected": num_communities,
        "total_nodes": len(G.nodes)
    }


def generate_graph_image(G: nx.Graph) -> BytesIO:
    """
    Generates a visualization of the graph with community colors and labels.

    Args:
        G: A NetworkX graph object.

    Returns:
        A BytesIO object containing the image data.
    """
    plt.figure(figsize=(16, 12))
    pos = nx.spring_layout(G, k=0.5, iterations=50, seed=42)

    # Detect communities for coloring
    partition = community_louvain.best_partition(G)
    
    # Create a color map for communities
    import matplotlib.cm as cm
    import numpy as np
    num_communities = len(set(partition.values()))
    colors = [partition[node] for node in G.nodes()]
    
    # Draw edges first (in background)
    nx.draw_networkx_edges(G, pos, alpha=0.1, width=0.5)
    
    # Draw nodes with community colors
    nx.draw_networkx_nodes(G, pos, 
                          node_size=100,
                          node_color=colors,
                          cmap=cm.tab20,
                          alpha=0.8,
                          edgecolors='black',
                          linewidths=0.5)

    # Calculate center positions for each community and add labels
    community_centers = {}
    for node, comm_id in partition.items():
        if comm_id not in community_centers:
            community_centers[comm_id] = {'x': [], 'y': []}
        community_centers[comm_id]['x'].append(pos[node][0])
        community_centers[comm_id]['y'].append(pos[node][1])
    
    # Draw community labels at the center of each cluster
    for comm_id, coords in community_centers.items():
        center_x = np.mean(coords['x'])
        center_y = np.mean(coords['y'])
        plt.text(center_x, center_y, f'C{comm_id}', 
                fontsize=14, fontweight='bold',
                ha='center', va='center',
                bbox=dict(boxstyle='round,pad=0.5', facecolor='white', 
                         edgecolor='black', alpha=0.8))

    plt.title(f"Bike Sharing Network - {num_communities} Communities Detected", 
              fontsize=18, fontweight='bold', pad=20)
    
    # Add legend
    plt.text(0.02, 0.98, f'Total Nodes: {len(G.nodes)}\nTotal Communities: {num_communities}',
             transform=plt.gca().transAxes,
             fontsize=11,
             verticalalignment='top',
             bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))
    
    plt.axis('off')
    plt.tight_layout()

    img_buf = io.BytesIO()
    plt.savefig(img_buf, format='png', dpi=150, bbox_inches='tight')
    plt.close()
    img_buf.seek(0)

    return img_buf

