#!/bin/bash

#SBATCH --output train_wmvc2_pace_weighted.out
#SBATCH --job-name=train_wmvc2_pace_weighted
#SBATCH --partition=gpu --gpus=1 --cpus-per-task=1 --mem-per-cpu=32G -t 1-20:00:00 --mail-type ALL

module purge
module load miniconda
module load Gurobi

conda activate graph

python /gpfs/gibbs/project/karbasi/cz397/CPSC583-Project/wmis_gnn_py/train_gnn.py --data_dir=/gpfs/gibbs/project/karbasi/cz397/CPSC583-Project/data/pace_weighted --output_dir=/gpfs/gibbs/project/karbasi/cz397/CPSC583-Project/models/wmvc_pace_weighted/ --output_name="wmvc_pace_weighted.pt" --eval_size=0.2 --batch_size=4 --num_epochs=300 --class1_weight=0.8 --hidden_layers=32 --learning_rate=1e-2 --momentum=0.9
