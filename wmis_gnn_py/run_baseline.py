import argparse
import pathlib

import torch

from arch.baseline import Baseline
from util.metis import metis_to_nx, nx_to_solution
from util.parser import positive_integer, existing_file, existing_directory
from wmis_gnn import wmis_gnn


def make_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument("--graph", type=existing_file, required=True)
    parser.add_argument("--model", type=existing_file, required=True)
    parser.add_argument("--output_dir", type=existing_directory, required=True)
    parser.add_argument("--output_name", type=str, required=True)
    parser.add_argument("--batch_size", type=positive_integer, required=True)
    parser.add_argument("--time_limit", type=positive_integer, required=True)
    parser.add_argument("--hidden_dim", type=positive_integer, required=True)

    return parser


if __name__ == "__main__":
    parser = make_parser()
    args = parser.parse_args()

    model = Baseline(7, args.hidden_dim, 2)
    model.load_state_dict(
        torch.load(args.model.resolve(), map_location=torch.device("cpu"))
    )

    G = metis_to_nx(args.graph.resolve())

    wmis_gnn(G, model, batch_size=args.batch_size, time_limit=args.time_limit)

    output_path = args.output_dir / args.output_name
    nx_to_solution(G, output_path.resolve())
