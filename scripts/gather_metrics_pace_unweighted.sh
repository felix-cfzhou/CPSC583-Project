#!/bin/bash

#SBATCH --output gather_metrics_pace_unweighted.out
#SBATCH --job-name=gather_metrics_pace_unweighted
#SBATCH --cpus-per-task=1 --mem-per-cpu=4G -t 8:00:00 --mail-type ALL

module purge
module load miniconda
module load Gurobi

conda activate graph

python3 /gpfs/gibbs/project/karbasi/cz397/CPSC583-Project/wmis_gnn_py/gather_metrics.py \
  --graph_dir=/gpfs/gibbs/project/karbasi/cz397/CPSC583-Project/data/pace_unweighted \
  --opt_dir=/gpfs/gibbs/project/karbasi/cz397/CPSC583-Project/data/pace_unweighted/label \
  --heuristic_dir=/gpfs/gibbs/project/karbasi/cz397/CPSC583-Project/data/pace_unweighted/output \
  --baseline_dir=/gpfs/gibbs/project/karbasi/cz397/CPSC583-Project/data/pace_unweighted/baseline \
  --local_search_dir=/gpfs/gibbs/project/karbasi/cz397/CPSC583-Project/data/pace_unweighted/kamis_local_search \
  --greedy_dir=/gpfs/gibbs/project/karbasi/cz397/CPSC583-Project/data/pace_unweighted/greedy \
  --sample=0 \
  --output_dir=/gpfs/gibbs/project/karbasi/cz397/CPSC583-Project/metrics/ \
  --output_name=pace_unweighted_metrics.csv
