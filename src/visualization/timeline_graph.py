import networkx as nx
import matplotlib.pyplot as plt

def draw_timeline(timeline):
    G = nx.DiGraph()

    for i in range(len(timeline) - 1):
        G.add_edge(timeline[i]["event"], timeline[i+1]["event"])

    plt.figure(figsize=(10, 4))
    nx.draw(G, with_labels=True, node_size=2000, font_size=8)
    plt.show()
