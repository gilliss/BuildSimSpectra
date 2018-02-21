#!/bin/bash -l

#SBATCH -t 24:00:00
#SBATCH --ntasks=1
#SBATCH -A majorana
#SBATCH -J mjr-chos
#SBATCH -p shared-chos 
#SBATCH --mail-type=FAIL
#SBATCH --mail-user=gilliss@unc.edu
#SBATCH -D /global/u2/g/gilliss/BuildSpectra_Output

python Macro_ConfigData_Example.py
