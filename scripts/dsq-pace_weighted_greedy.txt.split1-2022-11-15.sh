#!/bin/bash
#SBATCH --output dsq-pace_weighted_greedy.txt-%A_%4a-%N.out
#SBATCH --array 0-9844%2000
#SBATCH --job-name dsq-pace_weighted_greedy.txt
#SBATCH --cpus-per-task=1 --mem-per-cpu=4G -t 1:00:00 --mail-type ALL

# DO NOT EDIT LINE BELOW
/gpfs/loomis/apps/avx/software/dSQ/1.05/dSQBatch.py --job-file /gpfs/gibbs/project/karbasi/cz397/CPSC583-Project/scripts/pace_weighted_greedy.txt.split1 --status-dir /home/cz397/project/CPSC583-Project/out/pace_weighted_greedy

