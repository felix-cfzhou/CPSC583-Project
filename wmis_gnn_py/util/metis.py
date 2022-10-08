import pathlib

import networkx as nx


def yield_metis_filenames(graph_dir):
    path = pathlib.Path(graph_dir)
    for filename in sorted(path.glob("*.graph")):
        yield filename


def metis_to_nx(filename: str):
    G = nx.Graph()

    with open(filename, "r") as f:
        for line_num, line in enumerate(f):
            if line_num == 0:
                n_vertices, n_edges, graph_type = map(int, line.split(" "))

                assert n_vertices >= 0
                assert n_edges >= 0
                assert graph_type == 10

                continue

            if line[0] == "%":
                continue

            node_weight, *neighbors = map(int, line.split(" "))

            assert node_weight > 0

            G.add_node(line_num, weight=node_weight)

            for v in neighbors:
                assert 1 <= v <= n_vertices
                G.add_edge(line_num, v)

        assert G.size() == n_edges

    return G


def _write_line(f, line):
    f.write(line)
    f.write("\n")


def nx_to_metis(G: nx.Graph, filename):
    with open(filename, "w") as f:
        _write_line(f, " ".join([str(G.order()), str(G.size()), str(10)]))

        for v in range(1, G.order() + 1):
            adj = ["1"]
            if G.has_node(v):
                adj = [str(G.nodes[v].get("weight", 1))]
                for w in sorted(G.neighbors(v)):
                    adj.append(str(w))

            _write_line(f, " ".join(adj))


def nx_to_solution(G: nx.Graph, filename):
    solution = nx.get_node_attributes(G, "solution")

    with open(filename, "w") as f:
        for v in range(1, G.order()+1):
            _write_line(f, str(solution[v]))
