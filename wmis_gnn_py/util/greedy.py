import operator

import networkx as nx


def greedy_wmis(G: nx.Graph, limit=-1):
    solution = list(nx.get_node_attributes(G, "solution").items())
    if len(solution) == 0:
        return

    solution.sort(reverse=True, key=operator.itemgetter(1))

    # ensure all vertices in the view are not solved yet
    # assert solution[0][1] < 1.0

    if limit < 0:
        limit = len(solution)
    for idx, (v, x) in enumerate(solution):
        if idx == limit:
            break
        elif G.nodes[v]["solution"] == 0.0:
            continue

        G.nodes[v]["solution"] = 1.0
        for w in G.neighbors(v):
            G.nodes[w]["solution"] = 0.0
