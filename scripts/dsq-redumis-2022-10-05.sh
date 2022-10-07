#!/bin/bash
#SBATCH --array 0-199%2000
#SBATCH --output dsq-redumis-%A_%3a-%N.out
#SBATCH --job-name dsq-redumis
#SBATCH --cpus-per-task=4 --mem-per-cpu=1G -t 12:00:00 --mail-type ALL

# DO NOT EDIT LINE BELOW
/gpfs/loomis/apps/avx/software/dSQ/1.05/dSQBatch.py --job-file /gpfs/gibbs/project/karbasi/cz397/CPSC583-Project/scripts/redumis.txt --status-dir /gpfs/gibbs/project/karbasi/cz397/CPSC583-Project/scripts

