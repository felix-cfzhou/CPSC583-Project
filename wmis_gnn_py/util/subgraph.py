import networkx as nx


def _is_unsolved_node(attributes):
    if "solution" not in attributes:
        return True

    return 0.0 < attributes["solution"] < 1.0


def get_unsolved_view(G: nx.Graph):
    unsolved_vertices = [v for v in G.nodes if _is_unsolved_node(G.nodes[v])]
    return G.subgraph(unsolved_vertices)


def is_independent(G: nx.Graph):
    for v, w in G.edges:
        if G.nodes[v]["solution"] + G.nodes[w]["solution"] > 1:
            return False

    return True
