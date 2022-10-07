import argparse
import itertools
import pathlib
import sys

import numpy as np

from util.pace import pace_to_nx, yield_pace_filenames
from util.metis import nx_to_metis
from util.parser import positive_integer, existing_directory, existing_file
from util.weighting import inject_node_weights


def make_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "graph_dirs",
        nargs="+",
        type=existing_directory,
        help="Directories to graphs in pace format. File names should end with .gr",
    )
    parser.add_argument(
        "--samples_per_graph",
        type=positive_integer,
        required=True,
        help="Number of samples to generate per graph. Each sample injects some random vertex weights to the graph.",
    )
    parser.add_argument(
        "--max_vertex_weight",
        type=int,
        default=0,
        help="A random weight between 1 and max_vertex_weight is assigned to each vertex. A value less than 1 indicates the max_vertex_weight=2*|V|.",
    )
    parser.add_argument("--random_state", type=int, required=True)
    parser.add_argument("--output_dir", type=existing_directory, required=True)

    return parser


if __name__ == "__main__":
    parser = make_parser()
    args = parser.parse_args()

    random_state = np.random.RandomState(args.random_state)

    for graph_filename in itertools.chain.from_iterable(
        yield_pace_filenames(graph_dir) for graph_dir in args.graph_dirs
    ):
        path = pathlib.Path(graph_filename)
        assert path.is_file()

        G, _ = pace_to_nx(path.resolve())
        max_weight = (
            args.max_vertex_weight if args.max_vertex_weight > 0 else 2 * G.order()
        )

        for sample_idx in range(args.samples_per_graph):
            if max_weight > 1:
                out_filename = (
                    args.output_dir
                    / f"{path.stem}-maxw{max_weight}-seed{args.random_state}_{sample_idx}.graph"
                )
                inject_node_weights(G, max_weight=max_weight, random_state=random_state)
            else:
                out_filename = args.output_dir / f"{path.stem}.graph"

            print(out_filename.resolve())
            nx_to_metis(G, out_filename.resolve())
