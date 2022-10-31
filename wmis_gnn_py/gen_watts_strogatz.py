import argparse
import itertools
import pathlib

from util.parser import probability, positive_integer, existing_directory
from util.weighting import inject_node_weights
from util.metis import nx_to_metis

import networkx as nx
import numpy as np


def make_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument("--n_graphs", type=positive_integer, required=True)
    parser.add_argument("--n_vertices", type=positive_integer, required=True)
    parser.add_argument("--k_neighbors", type=positive_integer, required=True)
    parser.add_argument("--p_edge", type=probability, required=True)
    parser.add_argument("--random_seed", type=int, required=True)
    parser.add_argument("--output_dir", type=existing_directory, required=True)
    parser.add_argument("--max_vertex_weight", type=int, default=0)

    return parser


if __name__ == "__main__":
    parser = make_parser()
    args = parser.parse_args()

    random_state = np.random.RandomState(args.random_seed)

    max_weight = (
        args.max_vertex_weight if args.max_vertex_weight > 0 else 2 * args.n_vertices
    )

    for graph_idx in range(args.n_graphs):
        G = nx.watts_strogatz_graph(
            args.n_vertices, args.k_neighbors, args.p_edge, seed=random_state
        )
        G = nx.convert_node_labels_to_integers(G, first_label=1)
        inject_node_weights(G, max_weight=max_weight, random_state=random_state)

        output_path = (
            args.output_dir
            / f"watts-strogatz-n{args.n_vertices}-k{args.k_neighbors}-p{args.p_edge}-maxw{max_weight}-seed{args.random_seed}_{graph_idx:05}.graph"
        )
        print(output_path.resolve())
        nx_to_metis(G, output_path.resolve())
