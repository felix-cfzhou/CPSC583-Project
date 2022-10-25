import pathlib

import networkx as nx
import torch_geometric as pyg
import torch
from torch_geometric.utils import add_remaining_self_loops
from torch_scatter import scatter_add

from metis import metis_to_nx, solution_to_nx, yield_solution_filenames


def _norm(edge_index, num_nodes, edge_weight=None, improved=False, dtype=None):
    if edge_weight is None:
        edge_weight = torch.ones(
            (edge_index.size(1),), dtype=dtype, device=edge_index.device
        )

    fill_value = 1.0 if not improved else 2.0
    edge_index, edge_weight = add_remaining_self_loops(
        edge_index, edge_weight, fill_value, num_nodes
    )

    row, col = edge_index
    deg = scatter_add(edge_weight, row, dim=0, dim_size=num_nodes)
    deg_inv_sqrt = deg.pow(-0.5)
    deg_inv_sqrt[deg_inv_sqrt == float("inf")] = 0

    return edge_index, deg_inv_sqrt[row] * edge_weight * deg_inv_sqrt[col]


def compute_identity(edge_index, n, k):
    _id, value = _norm(edge_index, n)
    adj_sparse = torch.sparse.FloatTensor(_id, value, torch.Size([n, n]))
    adj_power = adj_sparse.to_dense()
    diag_all = [torch.diag(adj_power)]
    for i in range(1, k):
        adj_power = adj_sparse @ adj_power
        diag_all.append(torch.diag(adj_power))
    diag_all = torch.stack(diag_all, dim=1)
    return diag_all


def nx_to_tensor(G: nx.Graph):
    id_attr = {v: v for v in G.nodes}
    nx.set_node_attributes(G, id_attr, "id")

    deg_attr = dict(G.degree)
    nx.set_node_attributes(G, deg_attr, "deg")

    hood_weight = {
        v: sum(G.nodes[w]["weight"] for w in G.neighbors(v)) for v in G.nodes
    }
    nx.set_node_attributes(G, hood_weight, "hood_weight")

    weight = nx.get_node_attributes(G, "weight")
    nx.set_node_attributes(G, weight, "weight_copy")

    # eigenvector_centrality = nx.eigenvector_centrality(G)
    # nx.set_node_attributes(G, eigenvector_centrality, "eigenvector_centrality")

    data = pyg.utils.convert.from_networkx(
        G, group_node_attrs=["weight_copy", "hood_weight", "deg"]
    )
    data.x = data.x / (2 * G.order())

    # graph_identity = compute_identity(data.edge_index, G.order(), 8)
    # data.x = torch.cat([data.x, data.eigenvector_centrality.reshape((-1, 1)), graph_identity], dim=1)

    return data


def tensor_to_nx(data):
    G = pyg.utils.convert.to_networkx(
        data, node_attrs=["weight", "id", "solution"], to_undirected=True
    )
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
