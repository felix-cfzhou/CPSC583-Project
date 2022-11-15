#!/bin/bash

#SBATCH --output train_baseline_ws.out
#SBATCH --job-name=train_baseline_ws
#SBATCH --partition=gpu --gpus=1 --cpus-per-task=1 --mem-per-cpu=4G -t 2-00:00:00 --mail-type ALL

module purge
module load miniconda
module load Gurobi

conda activate graph

python /gpfs/gibbs/project/karbasi/cz397/CPSC583-Project/wmis_gnn_py/train_baseline.py --data_dir=/gpfs/gibbs/project/karbasi/cz397/CPSC583-Project/data/watts_strogatz --output_dir=/gpfs/gibbs/project/karbasi/cz397/CPSC583-Project/models/baseline_ws/ --output_name="baseline_ws.pt" --eval_size=0.2 --batch_size=256 --num_epochs=300 --class1_weight=0.5 --hidden_dim=32 --learning_rate=1e-2 --momentum=0.9 --max_dataset_len=10000 --max_node_num=1000
