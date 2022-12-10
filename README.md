# Weighted Maximum Independent Set Heuristics with Graph Neural Networks

## Usage
In general, we expect graphs in the [METIS format](https://people.sc.fsu.edu/~jburkardt/data/metis_graph/metis_graph.html).

See the following for generating Erdos-Reyni and Watts-Strogatz graphs
```
scripts/gen_erdos_reyni_small.sh
scripts/gen_watts_strogatz.sh
```
If we wish to work with the [PACE 2019 Vertex Cover Dataset](https://pacechallenge.org/2019/vc/vc_exact/),
it must be downloaded, uncompressed, and converted to the METIS format.
There is a utility function for doing so.

See the following for (non-exhaustive) examples for model training.
Weights are saved to an indicated directory.
```
scripts/train_baseline_er_small.sh
scripts/train_wmvc_er_small.sh
```

See the following for examples of running the heuristic
```
scripts/er_small_baseline.txt
scripts/er_small_output.txt
```
We can also run the greedy heuristic and local search algorithms as in below
```
scripts/er_small_greedy.txt
scripts/local_search_er_small.txt
```
Note that to run the local search algorithm, a compiled binary for [KaMIS](https://github.com/KarlsruheMIS/KaMIS) is required.


## Directories
- metrics: csv files for heuristic performance on all graphs
- models: compressed weights per architecture-dataset pair, saved every few epochs
- notebooks: Jupyter notebooks for analysis and output figures
- scripts: scripts used for preprocessing / generating data, training models, and running heuristics / baselines
- wmis_gnn_py: python utility functions with commandline interfaces

See [here](https://github.com/felix-cfzhou/CPSC583-Project/blob/main/wmis_gnn_py/README.md) for more explanation of python files.
