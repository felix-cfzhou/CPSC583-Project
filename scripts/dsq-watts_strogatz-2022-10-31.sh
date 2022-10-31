#!/bin/bash
#SBATCH --output dsq-watts_strogatz-%A_%4a-%N.out
#SBATCH --array 0-9999%2000
#SBATCH --job-name dsq-watts_strogatz
#SBATCH --cpus-per-task=1 --mem-per-cpu=16G -t 7:00:00 --mail-type ALL

# DO NOT EDIT LINE BELOW
/gpfs/loomis/apps/avx/software/dSQ/1.05/dSQBatch.py --job-file /gpfs/gibbs/project/karbasi/cz397/CPSC583-Project/scripts/watts_strogatz.txt --status-dir /gpfs/gibbs/project/karbasi/cz397/CPSC583-Project/scripts

