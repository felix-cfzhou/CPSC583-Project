#!/bin/bash
#SBATCH --array 0-73%2000
#SBATCH --output dsq-weighted_branch_reduce_large-%A_%2a-%N.out
#SBATCH --job-name dsq-weighted_branch_reduce_large
#SBATCH --cpus-per-task=1 --mem-per-cpu=128G -t 12:00:00 --mail-type ALL

# DO NOT EDIT LINE BELOW
/gpfs/loomis/apps/avx/software/dSQ/1.05/dSQBatch.py --job-file /gpfs/gibbs/project/karbasi/cz397/CPSC583-Project/scripts/weighted_branch_reduce_large.txt --status-dir /gpfs/gibbs/project/karbasi/cz397/CPSC583-Project/scripts

