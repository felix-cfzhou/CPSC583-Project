import argparse
import pathlib

import networkx as nx
import numpy as np

from util.metis import metis_to_nx, nx_to_solution
from util.parser import existing_file, existing_directory
from util.greedy import greedy_wmis


def make_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument("--graph", type=existing_file, required=True)
    parser.add_argument("--random_state", type=int, required=True)
    parser.add_argument("--output_dir", type=existing_directory, required=True)
    parser.add_argument("--output_name", type=str, required=True)

    return parser


if __name__ == "__main__":
    parser = make_parser()
    args = parser.parse_args()

    G = metis_to_nx(args.graph.resolve())

    random_state = np.random.RandomState(args.random_state)
    random_solution = random_state.rand(G.order())
    nx.set_node_attributes(
        G, {v: random_solution[idx] for idx, v in enumerate(G.nodes)}, name="solution"
    )

    greedy_wmis(G)

    output_path = args.output_dir / args.output_name
    nx_to_solution(G, output_path.resolve())
