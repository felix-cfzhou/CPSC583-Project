#!/bin/bash

#SBATCH --output gather_metrics_pace_weighted.out
#SBATCH --job-name=gather_metrics_pace_weighted
#SBATCH --cpus-per-task=1 --mem-per-cpu=4G -t 17:00:00 --mail-type ALL

module purge
module load miniconda
module load Gurobi

conda activate graph

python3 /gpfs/gibbs/project/karbasi/cz397/CPSC583-Project/wmis_gnn_py/gather_metrics.py \
  --graph_dir=/gpfs/gibbs/project/karbasi/cz397/CPSC583-Project/data/pace_weighted \
  --opt_dir=/gpfs/gibbs/project/karbasi/cz397/CPSC583-Project/data/pace_weighted/label \
  --heuristic_dir=/gpfs/gibbs/project/karbasi/cz397/CPSC583-Project/data/pace_weighted/output \
  --baseline_dir=/gpfs/gibbs/project/karbasi/cz397/CPSC583-Project/data/pace_weighted/baseline \
  --local_search_dir=/gpfs/gibbs/project/karbasi/cz397/CPSC583-Project/data/pace_weighted/kamis_local_search \
  --greedy_dir=/gpfs/gibbs/project/karbasi/cz397/CPSC583-Project/data/pace_weighted/greedy \
  --sample=0 \
  --output_dir=/gpfs/gibbs/project/karbasi/cz397/CPSC583-Project/metrics/ \
  --output_name=pace_weighted_metrics.csv
