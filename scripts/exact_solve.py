if __name__ == "__main__":
  for graph in range(1, 201):
    task = f"module load GCC; /home/cz397/project/CPSC583-Project/KaMIS/deploy/online_mis /home/cz397/project/CPSC583-Project/pace2019_track1_vc_exact_all/vc-exact_{graph:03}.graph --time_limit=36000 --output=/home/cz397/project/CPSC583-Project/exact_solve/vc-exact_{graph:03}.ind"
    print(task)
