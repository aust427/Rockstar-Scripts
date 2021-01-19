#!/bin/bash
#SBATCH -J TNG300-1-DM-CT
#SBATCH -N1 --ntasks-per-node=30
#SBATCH --exclusive
#SBATCH --time=160:00:00
#SBATCH -o OUTPUT.o%j
#SBATCH -e OUTPUT.e%j

perl /home/agabrielpillai/consistent-trees/do_merger_tree.pl /mnt/sdceph/users/agabrielpillai/IllustrisTNG/L205n2500TNG_DM/output/rockstar/outputs/merger_tree.cfg

