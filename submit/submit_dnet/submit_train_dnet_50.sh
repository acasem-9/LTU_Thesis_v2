#!/bin/bash

# Job time (hh:mm:ss):
#SBATCH -t 03:00:00

# Project specification:
#SBATCH -A lu2023-2-80

# GPU access:
#SBATCH -p gpua100

# Naming of job:
#SBATCH -J train_dnet_50

# Job output:
#SBATCH -o train_dnet_50_%j.out
#SBATCH -e train_dnet_50_%j.err

# Job notification:
#SBATCH --mail-user=ca4360sa-s@student.lu.se
#SBATCH --mail-type=ALL

# No restart if node failure:
#SBATCH --no-requeue

#Get output 
#cat $0

# Staring process: 
echo "Starting processing work"

# Load modules required:
#echo "loading anaconda3"
#module load Anaconda3
#source config_conda.sh
#ml GCC/11.3.0
#ml OpenMPI/4.1.4
#ml cuDNN/8.4.1.50-CUDA-11.7.0

# Set up conda environment:
#echo "setting up conda env"
#conda activate LTU_Thesis_YOLOv8_231227_T1512

# Change directory:
echo "Changing directory"
cd ../../dnet

# Run the work tasks:
echo "Start work"
python train_dnet_50.py

echo "Finished processing."
