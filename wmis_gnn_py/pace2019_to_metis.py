import argparse
import itertools
import pathlib
import sys

from util.pace import pace_to_nx, yield_pace_filenames
from util.metis import nx_to_metis
from util.parser import positive_integer, existing_directory, existing_file


def make_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "graph_dirs",
        nargs="+",
        type=existing_directory,
        help="Directories to graphs in pace format. File names should end with .gr",
    )
    parser.add_argument("--output_dir", type=existing_directory, required=True)

    return parser


if __name__ == "__main__":
    parser = make_parser()
    args = parser.parse_args()

    for graph_filename in itertools.chain.from_iterable(
        yield_pace_filenames(graph_dir) for graph_dir in args.graph_dirs
    ):
        path = pathlib.Path(graph_filename)
        assert path.is_file()

        G, _ = pace_to_nx(path.resolve())

        out_filename = args.output_dir / path.with_suffix(".graph").name
        print(out_filename.resolve())
        nx_to_metis(G, out_filename.resolve())
