#!/bin/bash
#SBATCH --array 0-199%2000
#SBATCH --output dsq-exact_solve-%A_%3a-%N.out
#SBATCH --job-name dsq-exact_solve
#SBATCH --cpus-per-task=16 --mem-per-cpu=18G -t 12:00:00 --mail-type ALL

# DO NOT EDIT LINE BELOW
/gpfs/loomis/apps/avx/software/dSQ/1.05/dSQBatch.py --job-file /gpfs/gibbs/project/karbasi/cz397/CPSC583-Project/scripts/exact_solve.txt --status-dir /gpfs/gibbs/project/karbasi/cz397/CPSC583-Project/

