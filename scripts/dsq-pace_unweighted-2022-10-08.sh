#!/bin/bash
#SBATCH --output dsq-pace_unweighted-%A_%3a-%N.out
#SBATCH --array 0-199%2000
#SBATCH --job-name dsq-pace_unweighted
#SBATCH --cpus-per-task=1 --mem-per-cpu=16 -t 7:00:00 --mail-type ALL

# DO NOT EDIT LINE BELOW
/gpfs/loomis/apps/avx/software/dSQ/1.05/dSQBatch.py --job-file /gpfs/gibbs/project/karbasi/cz397/CPSC583-Project/scripts/pace_unweighted.txt --status-dir /gpfs/gibbs/project/karbasi/cz397/CPSC583-Project/out/dsq-pace_unweighted-2022-10-08/

