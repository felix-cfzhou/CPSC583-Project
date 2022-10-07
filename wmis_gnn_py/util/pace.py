import pathlib

import networkx as nx


def yield_pace_filenames(graph_dir):
  path = pathlib.Path(graph_dir)
  for filename in sorted(path.glob("*.gr")):
    yield filename

def pace_to_nx(filename: str):
  G = nx.Graph()
  H = nx.MultiGraph()

  with open (filename, 'r') as f:
    for line_num, line in enumerate(f):
      if line_num == 0:
        p, td, n_vertices, n_edges = line.split(' ')
        n_vertices, n_edges = int(n_vertices), int(n_edges)

        assert p == 'p'
        assert td == 'td'
        assert n_vertices >= 0
        assert n_edges >= 0

        continue

      if line[0] == 'c':
        continue

      u, v = line.split(' ')
      u, v = int(u), int(v)

      assert 1 <= u <= n_vertices
      assert 1 <= v <= n_vertices

      G.add_edge(u, v)
      H.add_edge(u, v)

    assert H.size() == n_edges

  return G, H
