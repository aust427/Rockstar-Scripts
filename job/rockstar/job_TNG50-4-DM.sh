#!/bin/bash

#SBATCH --mail-user=agabrielpillai@flatironinstitute.org
#SBATCH --mail-type=ALL
#SBATCH -J TNG50-4-DM-rockstar 
#SBATCH -N1 --ntasks-per-node=40
#SBATCH --exclusive
#SBATCH --time=160:00:00
#SBATCH -o OUTPUT.o%j
#SBATCH -e OUTPUT.e%j

module load gcc
module load lib/hdf5/1.8.21
module load openmpi
module load lib/fftw2/2.1.5-openmpi1
module load lib/gsl

#Remove outputs from previous runs
# rm -f test_output.dat

/home/agabrielpillai/rockstar/rockstar/rockstar	-c /home/agabrielpillai/rockstar/parallel/TNG50/parallel_L35n270TNG_DM.cfg &> server.dat & 

perl -e 'sleep 1 while (!(-e "/mnt/sdceph/users/agabrielpillai/TNG50/L35n270TNG_DM/output/rockstar/auto-rockstar.cfg"))'


mpirun /home/agabrielpillai/rockstar/rockstar/rockstar -c /mnt/sdceph/users/agabrielpillai/TNG50/L35n270TNG_DM/output/rockstar/auto-rockstar.cfg >> test_output.dat 2>&1 

sleep 10

mpirun /home/agabrielpillai/rockstar/rockstar/rockstar -c /mnt/sdceph/users/agabrielpillai/TNG50/L35n270TNG_DM/output/rockstar/auto-rockstar.cfg >> test_output.dat 2>&1 

#Finish
