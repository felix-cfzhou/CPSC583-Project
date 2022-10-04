import sys

import networkx as nx

def file_to_nx(filename: str):
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


def write_line(f, line):
  f.write(line)
  f.write('\n')

def nx_Graph_to_metis(G: nx.Graph, filename):
  with open(filename, 'w') as f:
    write_line(f, ' '.join([str(G.order()), str(G.size()), str(10)]))

    for v in range(1, G.order()+1):
      adj = ['1']
      if G.has_node(v):
        adj.extend(str(w) for w in sorted(G.neighbors(v)))

      write_line(f, ' '.join(adj))


if __name__ == "__main__":
  filenames = sys.argv[1:]
  for filename in filenames:
    G, _ = file_to_nx(filename)

    components = filename.split('.')
    components[-1] = 'graph'
    out_filename = '.'.join(components)
    print(out_filename)
    nx_Graph_to_metis(G, '.'.join(components))

