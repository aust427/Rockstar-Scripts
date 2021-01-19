#!/bin/bash
#SBATCH -J TNG50-4-DM-CT
#SBATCH -N1 --ntasks-per-node=30
#SBATCH --exclusive
#SBATCH --time=160:00:00
#SBATCH -o OUTPUT.o%j
#SBATCH -e OUTPUT.e%j


perl /home/agabrielpillai/consistent-trees/do_merger_tree.pl /mnt/sdceph/users/agabrielpillai/TNG50/L35n270TNG_DM/output/rockstar/outputs/merger_tree.cfg

