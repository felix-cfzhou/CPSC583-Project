#!/bin/bash
#SBATCH --output dsq-pace_unweighted_greedy-%A_%3a-%N.out
#SBATCH --array 0-199%2000
#SBATCH --job-name dsq-pace_unweighted_greedy
#SBATCH --cpus-per-task=1 --mem-per-cpu=4G -t 1:00:00 --mail-type ALL

# DO NOT EDIT LINE BELOW
/gpfs/loomis/apps/avx/software/dSQ/1.05/dSQBatch.py --job-file /gpfs/gibbs/project/karbasi/cz397/CPSC583-Project/scripts/pace_unweighted_greedy.txt --status-dir /home/cz397/project/CPSC583-Project/out/pace_unweighted_greedy

