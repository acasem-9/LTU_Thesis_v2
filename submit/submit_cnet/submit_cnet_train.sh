#!/bin/bash

# Job time (hh:mm:ss):
#SBATCH -t 00:05:00

# Project specification:
#SBATCH -A lu2023-2-80

# GPU access:
#SBATCH -p gpua100

# Naming of job:
#SBATCH -J cnet_train

# Job output:
#SBATCH -o cnet_train_%j.out
#SBATCH -e cnet_train_%j.err

# Job notification:
#SBATCH --mail-user=carl.sandelius.4360@student.lu.se
#SBATCH --mail-type=END

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
cd ../../scripts

# Run the work tasks:
echo "Start work"
python cnet_run_training.py

echo "Finished processing."
