#!/bin/bash

#SBATCH --output gen_watts_strogatz.out
#SBATCH --job-name=gen_watts_strogatz
#SBATCH --cpus-per-task=1 --mem-per-cpu=2G -t 1:00:00 --mail-type ALL

module load SciPy-bundle
module load networkx

python3 /home/cz397/project/CPSC583-Project/wmis_gnn_py/gen_watts_strogatz.py --n_graphs=10000 --n_vertices=1000 --k_neighbors=5 --p_edge=0.9 --random_seed=5000 --output_dir=/home/cz397/project/CPSC583-Project/data/watts_strogatz/
