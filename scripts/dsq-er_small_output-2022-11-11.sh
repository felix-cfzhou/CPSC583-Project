#!/bin/bash
#SBATCH --output dsq-er_small_output-%A_%3a-%N.out
#SBATCH --array 0-999%2000
#SBATCH --job-name dsq-er_small_output
#SBATCH --cpus-per-task=1 --mem-per-cpu=1G -t 1:00:00 --mail-type ALL

# DO NOT EDIT LINE BELOW
/gpfs/loomis/apps/avx/software/dSQ/1.05/dSQBatch.py --job-file /gpfs/gibbs/project/karbasi/cz397/CPSC583-Project/scripts/er_small_output.txt --status-dir /home/cz397/project/CPSC583-Project/out/er_small_output

