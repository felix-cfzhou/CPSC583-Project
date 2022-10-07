#!/bin/bash

#SBATCH --output gen_erdos_reyni_mid.out
#SBATCH --job-name=gen_erdos_reyni_mid
#SBATCH --cpus-per-task=1 --mem-per-cpu=8G -t 6:00:00 --mail-type ALL

module load SciPy-bundle
module load networkx

python3 /home/cz397/project/CPSC583-Project/wmis_gnn_py/gen_erdos_reyni.py --n_graphs=5000 --n_vertices=1000 --p_edge=0.1 --random_seed=100 --output_dir=/home/cz397/project/CPSC583-Project/data/erdos_reyni_mid
