#!/bin/bash
#SBATCH --output dsq-pace_weighted_1-%A_%4a-%N.out
#SBATCH --array 0-9999%2000
#SBATCH --job-name dsq-pace_weighted_1
#SBATCH --cpus-per-task=1 --mem-per-cpu=16G -t 7:00:00 --mail-type ALL

# DO NOT EDIT LINE BELOW
/gpfs/loomis/apps/avx/software/dSQ/1.05/dSQBatch.py --job-file /gpfs/gibbs/project/karbasi/cz397/CPSC583-Project/scripts/pace_weighted_1.txt --status-dir /gpfs/gibbs/project/karbasi/cz397/CPSC583-Project/out/dsq-pace_weighted_1-2022-10-09/

