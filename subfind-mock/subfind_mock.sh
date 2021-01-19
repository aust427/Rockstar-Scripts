#!/bin/bash
#SBATCH --nodes=1
#SBATCH -J rockstar-mock-subfind
#SBATCH --exclusive
#SBATCH --time=108:00:00
#SBATCH --mail-user=a.gabrielpillai@gmail.com
#SBATCH --mail-type=ALL
#SBATCH -o OUTPUT.o%j
#SBATCH -e OUTPUT.e%j


module load gcc
module load python3
module load lib/hdf5

NFILES=72
BOXLENGTH=35
NPARTICLES=2160

SIM=TNG50/L"$BOXLENGTH"n"$NPARTICLES"TNG_DM

BINARY_DIR=/mnt/sdceph/users/agabrielpillai/$SIM/output/binary
HDF5_DIR=/mnt/sdceph/users/agabrielpillai/$SIM/postprocessing/rockstar

echo $SIM

for i in {75..99}
do 
	echo "$i" 
	python3 /home/agabrielpillai/scripts/subfind-mock/create_hdf5.py $NFILES $NPARTICLES $BINARY_DIR $HDF5_DIR $i
done

