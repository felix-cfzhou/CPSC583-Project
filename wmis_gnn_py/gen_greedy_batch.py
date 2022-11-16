import argparse
import itertools
import pathlib

import numpy as np

from util.parser import existing_directory, existing_file
from util.metis import yield_metis_filenames


def make_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "graph_dirs",
        nargs="+",
        type=existing_directory,
        help="Directories to graphs in metis format. File names should end with .graph",
    )
    parser.add_argument("--greedy", type=existing_file, required=True)
    parser.add_argument("--output_dir", type=existing_directory, required=True)
    parser.add_argument("--random_state", type=int, required=True)

    return parser


if __name__ == "__main__":
    parser = make_parser()
    args = parser.parse_args()

    random_state = np.random.RandomState(args.random_state)

    for graph_path in itertools.chain.from_iterable(
        yield_metis_filenames(graph_dir) for graph_dir in args.graph_dirs
    ):
        cmd_str = (
            f"module purge; "
            f"module load miniconda; module load Gurobi; conda activate graph; "
            f"python3 {args.greedy.resolve()} "
            f"--graph={graph_path.resolve()} "
            f"--random_state={random_state.randint(low=0, high=1000000)} "
            f"--output_dir={args.output_dir.resolve()} "
            f"--output_name={graph_path.with_suffix('.ind').name}"
        )
        print(cmd_str)
