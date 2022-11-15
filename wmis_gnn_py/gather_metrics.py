import argparse
import pathlib

import numpy as np
import pandas as pd
from tqdm import tqdm

from util.metis import yield_metis_filenames, metis_to_nx, solution_to_nx
from util.parser import existing_directory


def make_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument("--graph_dir", type=existing_directory, required=True)
    parser.add_argument("--opt_dir", type=existing_directory, required=True)
    parser.add_argument("--heuristic_dir", type=existing_directory, required=True)
    parser.add_argument("--baseline_dir", type=existing_directory, required=True)
    parser.add_argument("--local_search_dir", type=existing_directory, required=True)
    parser.add_argument("--sample", type=int, required=True)
    parser.add_argument("--output_dir", type=existing_directory, required=True)
    parser.add_argument("--output_name", type=str, required=True)

    return parser


def compute_metrics(
    graph_dir, opt_dir, heuristic_dir, baseline_dir, local_search_dir, size=0
):
    graph_paths = list(pathlib.Path(path) for path in yield_metis_filenames(graph_dir))
    rows = []
    if size > 0:
        graph_paths = np.random.choice(graph_paths, size=size, replace=False)

    for graph_path in tqdm(graph_paths):
        # print(graph_path.name)
        heuristic_solution_path = heuristic_dir / graph_path.with_suffix(".ind").name
        opt_solution_path = opt_dir / graph_path.with_suffix(".ind").name
        baseline_solution_path = baseline_dir / graph_path.with_suffix(".ind").name
        local_search_solution_path = (
            local_search_dir / graph_path.with_suffix(".ind").name
        )

        G = metis_to_nx(graph_path.resolve())

        opt_weight = None
        if opt_solution_path.is_file():
            solution_to_nx(G, opt_solution_path.resolve())
            opt_weight = sum(
                G.nodes[v]["weight"] for v in G.nodes if G.nodes[v]["solution"] == 1
            )

        heuristic_weight = None
        if heuristic_solution_path.is_file():
            solution_to_nx(G, heuristic_solution_path.resolve())
            heuristic_weight = sum(
                G.nodes[v]["weight"] for v in G.nodes if G.nodes[v]["solution"] == 1
            )

        baseline_weight = None
        if baseline_solution_path.is_file():
            solution_to_nx(G, baseline_solution_path.resolve())
            baseline_weight = sum(
                G.nodes[v]["weight"] for v in G.nodes if G.nodes[v]["solution"] == 1
            )

        local_search_weight = None
        if local_search_solution_path.is_file():
            solution_to_nx(G, local_search_solution_path.resolve())
            local_search_weight = sum(
                G.nodes[v]["weight"] for v in G.nodes if G.nodes[v]["solution"] == 1
            )

        rows.append(
            pd.Series(
                {
                    "name": graph_path.name,
                    "opt_weight": opt_weight,
                    "heuristic_weight": heuristic_weight,
                    "baseline_weight": baseline_weight,
                    "local_search_weight": local_search_weight,
                }
            )
        )

    return rows


if __name__ == "__main__":
    parser = make_parser()
    args = parser.parse_args()

    rows = compute_metrics(
        args.graph_dir,
        args.opt_dir,
        args.heuristic_dir,
        args.baseline_dir,
        args.local_search_dir,
        size=args.sample,
    )
    df = pd.DataFrame(rows)

    output_path = args.output_dir / args.output_name
    df.to_csv(output_path.resolve())
