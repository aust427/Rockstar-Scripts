#!/bin/bash
#SBATCH -J TNG100-3-DM-rockstar 
#SBATCH -N1 --ntasks-per-node=43
#SBATCH --exclusive
#SBATCH --time=160:00:00
#SBATCH -o OUTPUT.o%j
#SBATCH -e OUTPUT.e%j

module load gcc
module load lib/hdf5/1.8.19
module load openmpi
module load lib/fftw2/2.1.5-openmpi1
module load lib/gsl

#Remove outputs from previous runs
# rm -f test_output.dat

/home/agabrielpillai/rockstar/rockstar/rockstar	-c /home/agabrielpillai/rockstar/parallel/IllustrisTNG/parallel_L75n455TNG_DM.cfg &> server.dat & 

perl -e 'sleep 1 while (!(-e "/simons/scratch/agabrielpillai/IllustrisTNG/L75n455TNG_DM/output/rockstar/auto-rockstar.cfg"))'


mpirun /home/agabrielpillai/rockstar/rockstar/rockstar -c /simons/scratch/agabrielpillai/IllustrisTNG/L75n455TNG_DM/output/rockstar/auto-rockstar.cfg >> test_output.dat 2>&1 

sleep 10

mpirun /home/agabrielpillai/rockstar/rockstar/rockstar -c /simons/scratch/agabrielpillai/IllustrisTNG/L75n455TNG_DM/output/rockstar/auto-rockstar.cfg >> test_output.dat 2>&1 

#Finish
