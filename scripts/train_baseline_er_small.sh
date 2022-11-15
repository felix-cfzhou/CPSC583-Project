#!/bin/bash

#SBATCH --output train_baseline_er_small.out
#SBATCH --job-name=train_baseline_er_small
#SBATCH --partition=gpu --gpus=1 --cpus-per-task=1 --mem-per-cpu=4G -t 8:00:00 --mail-type ALL

module purge
module load miniconda
module load Gurobi

conda activate graph

python /gpfs/gibbs/project/karbasi/cz397/CPSC583-Project/wmis_gnn_py/train_baseline.py --data_dir=/gpfs/gibbs/project/karbasi/cz397/CPSC583-Project/data/erdos_reyni_small --output_dir=/gpfs/gibbs/project/karbasi/cz397/CPSC583-Project/models/baseline_er_small/ --output_name="baseline_er_small.pt" --eval_size=0.2 --batch_size=256 --num_epochs=300 --class1_weight=0.5 --hidden_dim=32 --learning_rate=1e-2 --momentum=0.9 --max_dataset_len=10000 --max_node_num=10000
