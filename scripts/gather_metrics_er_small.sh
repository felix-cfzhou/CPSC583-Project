#!/bin/bash

#SBATCH --output gather_metrics_er_small.out
#SBATCH --job-name=gather_metrics_small
#SBATCH --cpus-per-task=1 --mem-per-cpu=2G -t 1:00:00 --mail-type ALL

module purge
module load miniconda
module load Gurobi

conda activate graph

python3 /gpfs/gibbs/project/karbasi/cz397/CPSC583-Project/wmis_gnn_py/gather_metrics.py \
  --graph_dir=/gpfs/gibbs/project/karbasi/cz397/CPSC583-Project/data/erdos_reyni_small \
  --opt_dir=/gpfs/gibbs/project/karbasi/cz397/CPSC583-Project/data/erdos_reyni_small/label \
  --heuristic_dir=/gpfs/gibbs/project/karbasi/cz397/CPSC583-Project/data/erdos_reyni_small/output \
  --baseline_dir=/gpfs/gibbs/project/karbasi/cz397/CPSC583-Project/data/erdos_reyni_small/baseline \
  --local_search_dir=/gpfs/gibbs/project/karbasi/cz397/CPSC583-Project/data/erdos_reyni_small/kamis_local_search \
  --greedy_dir=/gpfs/gibbs/project/karbasi/cz397/CPSC583-Project/data/erdos_reyni_small/greedy \
  --sample=0 \
  --output_dir=/gpfs/gibbs/project/karbasi/cz397/CPSC583-Project/metrics/ \
  --output_name=erdos_reyni_small_metrics.csv
