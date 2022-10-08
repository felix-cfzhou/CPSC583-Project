#!/bin/bash

#SBATCH --output gen_erdos_reyni_small.out
#SBATCH --job-name=gen_erdos_reyni_small
#SBATCH --cpus-per-task=1 --mem-per-cpu=2G -t 1:00:00 --mail-type ALL

module load SciPy-bundle
module load networkx

python3 /home/cz397/project/CPSC583-Project/wmis_gnn_py/gen_erdos_reyni.py --n_graphs=1000 --n_vertices=200 --p_edge=0.1 --random_seed=20 --output_dir=/home/cz397/project/CPSC583-Project/data/erdos_reyni_small
