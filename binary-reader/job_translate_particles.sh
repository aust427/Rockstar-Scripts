#!/bin/bash
#SBATCH --nodes=1
#SBATCH -J bin-part
#SBATCH --exclusive
#SBATCH --time=148:00:00
#SBATCH --mail-user=a.gabrielpillai@gmail.com
#SBATCH --mail-type=ALL
#SBATCH -o OUTPUT.o%j
#SBATCH -e OUTPUT.e%j

SIM=L205n2500TNG_DM
NFILES=64

cd /mnt/sdceph/users/agabrielpillai/IllustrisTNG/$SIM/output/binary

echo "$SIM"

for i in {85..99}
do
	echo "$i" 
	./translate_particles "$i" 100 $NFILES
done
