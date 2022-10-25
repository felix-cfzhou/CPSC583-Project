import pathlib

import networkx as nx
import torch_geometric as pyg
import torch

from metis import metis_to_nx, solution_to_nx, yield_solution_filenames


def nx_to_tensor(G: nx.Graph):
    id_attr = {v: v for v in G.nodes}
    nx.set_node_attributes(G, id_attr, "id")
    
    deg_attr = dict(G.degree)
    nx.set_node_attributes(G, deg_attr, "deg")
    
    hood_weight = {v: sum(G.nodes[w]["weight"] for w in G.neighbors(v)) for v in G.nodes}
    nx.set_node_attributes(G, hood_weight, "hood_weight")
    
    weight = nx.get_node_attributes(G, "weight")
    nx.set_node_attributes(G, weight, "weight_copy")

    data = pyg.utils.convert.from_networkx(G, group_node_attrs=["weight_copy", "hood_weight", "deg"])
    data.x = data.x / (2 * G.order())
    
    return data


def tensor_to_nx(data):
    G = pyg.utils.convert.to_networkx(data, node_attrs=["weight", "id", "solution"], to_undirected=True)
    id_map = nx.get_node_attributes(G, "id")
    nx.relabel_nodes(G, id_map, copy=False)
    
    return G


class WMISDataset(pyg.data.Dataset):
    def __init__(self, root, transform=None, pre_transform=None, pre_filter=None):
        super().__init__(root, transform, pre_transform, pre_filter)

        self.root_path = pathlib.Path(root)
        self.graph_paths = []
        self.label_paths = []
        for label_path in yield_solution_filenames(self.root_path / "label/"):
            if label_path.suffix != ".ind":
                continue

            graph_path = self.root_path / label_path.with_suffix(".graph").name
            if not graph_path.is_file():
                continue

            self.graph_paths.append(graph_path)
            self.label_paths.append(label_path)

    def len(self):
        return len(self.label_paths)

    def get(self, idx):
        G = metis_to_nx(self.graph_paths[idx])
        solution_to_nx(G, self.label_paths[idx])
        data = nx_to_tensor(G)
        
        return data