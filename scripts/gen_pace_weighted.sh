#!/bin/bash

#SBATCH --output gen_pace_weighted.out
#SBATCH --job-name=gen_pace_weighted
#SBATCH --cpus-per-task=1 --mem-per-cpu=16G -t 6:00:00 --mail-type ALL

module purge
module load SciPy-bundle
module load networkx

python3 /home/cz397/project/CPSC583-Project/wmis_gnn_py/pace2019_to_metis.py /home/cz397/project/CPSC583-Project/data/pace2019_track1_vc_exact_all/ --samples_per_graph=50 --random_state=2019 --output_dir=/home/cz397/project/CPSC583-Project/data/pace_weighted/
