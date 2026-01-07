import networkx as nx
import matplotlib.pyplot as plt
import os

def draw_timeline(timeline, output_file=None):
    """Visualize timeline as a directed acyclic graph.
    
    Args:
        timeline: List of timeline entries with 'event' key
        output_file: Optional file path to save graph (PNG/PDF)
    """
    if not timeline or len(timeline) < 2:
        print("Timeline has fewer than 2 events; skipping visualization")
        return
    
    G = nx.DiGraph()
    
    # Truncate long event names for readability
    for i in range(len(timeline) - 1):
        src = timeline[i]["event"][:50] + "..." if len(timeline[i]["event"]) > 50 else timeline[i]["event"]
        dst = timeline[i+1]["event"][:50] + "..." if len(timeline[i+1]["event"]) > 50 else timeline[i+1]["event"]
        G.add_edge(src, dst)
    
    plt.figure(figsize=(14, 6))
    pos = nx.spring_layout(G, k=2, iterations=50)
    nx.draw_networkx_nodes(G, pos, node_size=1500, node_color="lightblue")
    nx.draw_networkx_edges(G, pos, edge_color="gray", arrows=True)
    nx.draw_networkx_labels(G, pos, font_size=7, font_weight="bold")
    plt.axis("off")
    plt.tight_layout()
    
    if output_file:
        plt.savefig(output_file, dpi=150, bbox_inches="tight")
        print(f"Timeline saved to {output_file}")
    else:
        plt.show()
