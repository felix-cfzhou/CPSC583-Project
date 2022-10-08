import argparse
import pathlib

from util.metis import metis_to_nx, nx_to_solution
from util.gurobi_wmis import wmis_ilp

from util.parser import positive_integer, existing_directory, existing_file


def make_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "metis_path",
        type=existing_file,
    )
    parser.add_argument("--output_dir", type=existing_directory, required=True)

    return parser


if __name__ == "__main__":
    parser = make_parser()
    args = parser.parse_args()

    G = metis_to_nx(args.metis_path.resolve())
    wmis_ilp(G)

    output_path = args.output_dir / args.metis_path.with_suffix(".ind").name

    nx_to_solution(G, output_path.resolve())

