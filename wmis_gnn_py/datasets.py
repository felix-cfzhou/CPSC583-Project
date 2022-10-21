import pathlib

import networkx as nx
import torch_geometric as pyg
import torch

from util.metis import metis_to_nx, solution_to_nx, yield_solution_filenames


class SmallER(pyg.data.Dataset):
    def __init__(self, root, transform=None, pre_transform=None, pre_filter=None):
        super().__init__(root, transform, pre_transform, pre_filter)

        self.root_path = pathlib.Path(root)
        self.graph_paths = []
        self.label_paths = []
        for label_path in yield_solution_filenames(self.root_path / "label/"):
            graph_path = self.root_path / label_path.with_suffix(".graph").name

            self.graph_paths.append(graph_path)
            self.label_paths.append(label_path)

    def len(self):
        return len(self.label_paths)

    def get(self, idx):
        G = metis_to_nx(self.graph_paths[idx])
        solution_to_nx(G, self.label_paths[idx])
        id_attr = {v: v for v in G.nodes}
        nx.set_node_attributes(G, id_attr, "id")

        data = pyg.utils.convert.from_networkx(G, group_node_attrs=["weight"])
        data.x = data.x.type(torch.FloatTensor)
        data.solution = data.solution.type(torch.FloatTensor).reshape((-1, 1))
        return data
