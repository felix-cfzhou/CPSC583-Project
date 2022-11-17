#!/bin/bash
#SBATCH --output dsq-ws_baseline-%A_%4a-%N.out
#SBATCH --array 0-9999%2000
#SBATCH --job-name dsq-ws_baseline
#SBATCH --cpus-per-task=1 --mem-per-cpu=4G -t 1:00:00 --mail-type ALL

# DO NOT EDIT LINE BELOW
/gpfs/loomis/apps/avx/software/dSQ/1.05/dSQBatch.py --job-file /gpfs/gibbs/project/karbasi/cz397/CPSC583-Project/scripts/ws_baseline.txt --status-dir /home/cz397/project/CPSC583-Project/out/ws_baseline

