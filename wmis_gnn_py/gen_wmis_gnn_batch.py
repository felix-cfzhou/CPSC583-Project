import argparse
import fnmatch
import glob
import itertools
import os
import pathlib

import pandas as pd

from util.parser import positive_integer, existing_directory, existing_file
from util.metis import yield_metis_filenames


def make_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "graph_dirs",
        nargs="+",
        type=existing_directory,
        help="Directories to graphs in metis format. File names should end with .graph",
    )
    parser.add_argument("--wmis_gnn", type=existing_file, required=True)
    parser.add_argument("--time_limit", type=positive_integer, required=True)
    parser.add_argument("--output_dir", type=existing_directory, required=True)
    parser.add_argument("--model_dir", type=existing_directory, required=True)
    parser.add_argument("--model_base", type=str, required=True)
    parser.add_argument("--batch_size", type=positive_integer, required=True)
    parser.add_argument("--hidden_dim", type=positive_integer, required=True)

    return parser


if __name__ == "__main__":
    parser = make_parser()
    args = parser.parse_args()

    model_csv_path = args.model_dir / f"{args.model_base}.csv"
    assert model_csv_path.is_file()

    df_metrics = pd.read_csv(model_csv_path.resolve())
    best_epoch = df_metrics["eval_acc_1"].idxmax() + 1
    model_path = args.model_dir / f"{args.model_base}_epoch{best_epoch:05}.pt"
    assert model_path.is_file()

    for graph_path in itertools.chain.from_iterable(
        yield_metis_filenames(graph_dir) for graph_dir in args.graph_dirs
    ):
        cmd_str = (
            f"module purge; "
            f"module load miniconda; module load Gurobi; conda activate graph; "
            f"python3 {args.wmis_gnn.resolve()} --graph={graph_path.resolve()} "
            f"--model={model_path.resolve()} --output_dir={args.output_dir.resolve()} "
            f'--output_name={graph_path.with_suffix(".ind").name} '
            f"--batch_size={args.batch_size} --time_limit={args.time_limit} "
            f"--hidden_dim={args.hidden_dim}"
        )
        print(cmd_str)
