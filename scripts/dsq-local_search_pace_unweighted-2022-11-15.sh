#!/bin/bash
#SBATCH --output dsq-local_search_pace_unweighted-%A_%3a-%N.out
#SBATCH --array 0-199%2000
#SBATCH --job-name dsq-local_search_pace_unweighted
#SBATCH --cpus-per-task=1 --mem-per-cpu=2G -t 1:00:00 --mail-type ALL

# DO NOT EDIT LINE BELOW
/gpfs/loomis/apps/avx/software/dSQ/1.05/dSQBatch.py --job-file /gpfs/gibbs/project/karbasi/cz397/CPSC583-Project/scripts/local_search_pace_unweighted.txt --status-dir /home/cz397/project/CPSC583-Project/out/local_search_pace_unweighted

