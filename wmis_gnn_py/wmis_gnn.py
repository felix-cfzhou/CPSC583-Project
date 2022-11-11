import time

import networkx as nx
import torch

from util.subgraph import get_unsolved_view, is_independent
from util.pyg_interface import nx_to_tensor
from util.greedy import greedy_wmis
from util.gurobi_wmis import wmis_lp


def wmis_gnn(G: nx.Graph, model, batch_size: int, time_limit: int):
    t_0 = time.time()

    nx.set_node_attributes(G, 0.5, name="solution")
    H = get_unsolved_view(G)

    it = 0
    t = time.time()
    while H.order() > 0 and t - t_0 <= time_limit:
        it += 1
        print(f"Beginning iteration {it:05} after {t-t_0:.2f} seconds")

        wmis_lp(H)
        H = get_unsolved_view(H)

        if H.order() == 0:
            break

        data = nx_to_tensor(H)
        with torch.no_grad():
            prob = torch.exp(model(data.x, data.edge_index)[:, 1])
        prob_dict = {data.id[idx]: prob[idx] for idx in range(len(data.id))}
        nx.set_node_attributes(H, prob_dict, name="solution")

        greedy_wmis(H, limit=batch_size)
        H = get_unsolved_view(H)

        t = time.time()

    greedy_wmis(H, limit=-1)
    assert is_independent(G)

    t = time.time()
    print(f"Done after iteration {it:05} after {t-t_0:.2f} seconds")
