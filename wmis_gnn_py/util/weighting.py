import networkx as nx
import numpy as np


def inject_node_weights(
    G: nx.Graph, max_weight: int, random_state: np.random.RandomState
):
    node_weights = {v: random_state.randint(1, max_weight + 1) for v in G.nodes}
    nx.set_node_attributes(G, node_weights, name="weight")
