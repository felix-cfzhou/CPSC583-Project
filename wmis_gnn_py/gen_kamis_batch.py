import argparse
import fnmatch
import glob
import itertools
import os
import pathlib

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
    parser.add_argument("--kamis", type=existing_file, required=True)
    parser.add_argument("--time_limit", type=positive_integer, required=True)
    parser.add_argument("--output_dir", type=existing_directory, required=True)

    return parser


if __name__ == "__main__":
    parser = make_parser()
    args = parser.parse_args()

    for graph_filename in itertools.chain.from_iterable(
        yield_metis_filenames(graph_dir) for graph_dir in args.graph_dirs
    ):
        output_filename = args.output_dir / graph_filename.with_suffix(".ind").name
        cmd_str = f"module load GCC; {args.kamis.resolve()} {graph_filename.resolve()} --time_limit={args.time_limit} --output={output_filename.resolve()}"
        print(cmd_str)
