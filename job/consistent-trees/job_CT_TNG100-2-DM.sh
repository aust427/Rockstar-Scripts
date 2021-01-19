#!/bin/bash
#SBATCH -J TNG100-2-DM-ct
#SBATCH -N1 --ntasks-per-node=20
#SBATCH --exclusive
#SBATCH --time=160:00:00
#SBATCH -o OUTPUT.o%j
#SBATCH -e OUTPUT.e%j

perl /home/agabrielpillai/consistent-trees/do_merger_tree.pl /mnt/sdceph/users/agabrielpillai/IllustrisTNG/L75n910TNG_DM/output/rockstar/outputs/merger_tree.cfg


