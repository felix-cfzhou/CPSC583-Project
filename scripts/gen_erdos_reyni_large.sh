#!/bin/bash

#SBATCH --output gen_erdos_reyni_large.out
#SBATCH --job-name=gen_erdos_reyni_large
#SBATCH --cpus-per-task=1 --mem-per-cpu=16G -t 12:00:00 --mail-type ALL

module load SciPy-bundle
module load networkx

python3 /home/cz397/project/CPSC583-Project/wmis_gnn_py/gen_erdos_reyni.py --n_graphs=20000 --n_vertices=50000 --p_edge=0.001 --random_seed=5000 --output_dir=/home/cz397/project/CPSC583-Project/data/erdos_reyni_large
