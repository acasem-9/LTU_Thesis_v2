#!/bin/bash

# Job time (hh:mm:ss):
#SBATCH -t 00:05:00

# Project specification:
#SBATCH -A lu2023-2-80

# GPU access:
#SBATCH -p gpua100

# Naming of job:
#SBATCH -J bengali_gpu_test

# Job output:
#SBATCH -o bengali_gpu_test_%j.out
#SBATCH -e bengali_gpu_test_%j.err

# Job notification:
#SBATCH --mail-user=carl.sandelius.4360@student.lu.se
#SBATCH --mail-type=END

# High Prio. Test jobs (remove for full run): 
#SBATCH --qos=test

# No restart if node failure:
#SBATCH --no-requeue

# Staring process: 
echo "Starting processing work"

# Loding GPU drivers: 
echo "Loading modules..."
ml cuDNN/8.4.1.50-CUDA-11.7.0

# Load conda env
# Assume that the login node have instanciated the right env before calling compute node. 

# Change directory:
echo "Changing directory..."
cd ../../scripts

# Run the work tasks:
echo "List of conda packages.."
python --version
conda list

echo "Test GPU..."
python test_gpu.py

echo "Finished processing."
