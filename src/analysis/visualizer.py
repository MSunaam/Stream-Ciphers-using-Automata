import networkx as nx
import matplotlib.pyplot as plt
from src.analysis.statistics import A51Statistics


class A51Visualizer:
    def __init__(self, statistics: A51Statistics):
        self.statistics = statistics

    def generate_graph(self, max_nodes: int = 100) -> nx.DiGraph:
        G = nx.DiGraph()
        transitions = self.statistics.state_transitions()
        frequency = self.statistics.get_frequency()

        # Add nodes and edges
        for from_state, to_states in transitions.items():
            if G.number_of_nodes() >= max_nodes:
                break
            from_state_weight = frequency.get(from_state, 1)  # Default weight is 1
            G.add_node(from_state, weight=from_state_weight)
            for to_state in to_states:
                to_state_weight = frequency.get(to_state, 1)  # Default weight is 1
                G.add_node(to_state, weight=to_state_weight)  # Ensure the node exists
                G.add_edge(from_state, to_state)

        return G

    def visualize_graph(self, G: nx.DiGraph, output_file: str = 'a51_state_transition.png'):
        plt.figure(figsize=(12, 8))
        pos = nx.spring_layout(G)
        node_sizes = [G.nodes[node]['weight'] * 10 for node in G.nodes()]
        nx.draw(G, pos, with_labels=True, node_size=node_sizes, node_color='lightblue', 
                font_size=8, arrows=True)
        plt.title("A5/1 State Transition Graph")
        plt.axis('off')
        plt.tight_layout()
        plt.savefig(output_file, dpi=300, bbox_inches="tight")
        plt.close()
