"""
This script is designed to separate a dataset of Bangla script images into two distinct categories: characters and diacritics. 
It reads the dataset from a specified directory, classifies each image based on the accompanying label files and a predefined class mapping, 
and then copies the images and labels into separate directories for diacritics and characters the opposing character classes are removed. 
"""

import os
import sys 
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import shutil
import pandas as pd
from concurrent.futures import ProcessPoolExecutor
from config_local import SEPARATED_C_DATA_DIR, SEPARATED_D_DATA_DIR, WORD_SEPARATED_DIR, BANGLA_YOLO_CLASS_MAPPING

def prepare_folders():
    # Prepares the directory structure for separated data, creating or clearing folders as necessary.
    print('Preparing folders... ')
    for dir_path in [SEPARATED_C_DATA_DIR, SEPARATED_D_DATA_DIR]:
        for sub_folder in ['labels', 'images']:
            path = os.path.join(dir_path, sub_folder)
            if not os.path.exists(path):
                os.makedirs(path)
            else:
                shutil.rmtree(path)  # Remove existing content
                os.makedirs(path)

def classify_and_copy(file_info):
    # Classifies and copies files to the appropriate directory based on their classification.

    file_name, classes = file_info

    # Determine destination based on classes
    destinations = []
    if 'd' in classes:
        destinations.append(SEPARATED_D_DATA_DIR)
    if 'c' in classes:
        destinations.append(SEPARATED_C_DATA_DIR)

    # Copy files to the appropriate destination
    for dest in destinations:
        for folder_type in ['images', 'labels']:
            src_file = f"{file_name}.{('txt' if folder_type == 'labels' else 'tif')}"
            src = os.path.join(WORD_SEPARATED_DIR, folder_type, src_file)
            dst = os.path.join(dest, folder_type, src_file)
            shutil.copy(src, dst)

def main():
    user_confirmation = input("Do you want to proceed? (y/n): ")
    if user_confirmation.lower() != 'y':
        print("Operation cancelled by the user.")
        sys.exit(1)

    prepare_folders()

    # Load class mappings
    class_mapping = pd.read_csv(BANGLA_YOLO_CLASS_MAPPING, encoding='utf-8')
    file_class_mapping = {}  # A dictionary to hold file classification
    print('Processing...')
    # Populate file_class_mapping based on the CSV
    for _, row in class_mapping.iterrows():
        yolo_class, _, _, character_class = row
        # Assume yolo_class corresponds to the file naming
        if int(yolo_class) in file_class_mapping:
            file_class_mapping[int(yolo_class)].add(character_class)
        else:
            file_class_mapping[int(yolo_class)] = {character_class}

    # Prepare the list of files to process
    label_files = [f for f in os.listdir(os.path.join(WORD_SEPARATED_DIR, 'labels')) if f.endswith('.txt')]
    to_process = []
    for label_file in label_files:
        file_name = label_file.split('.')[0]
        try:
            with open(os.path.join(WORD_SEPARATED_DIR, 'labels', label_file), 'r') as file:
                labels = {line.split()[0] for line in file.readlines()}
                classes = set()
                for label in labels:
                    classes.update(file_class_mapping.get(int(label), set()))
                to_process.append((file_name, classes))
        except Exception as e:
            print(f"Error processing file {label_file}: {e}")

    # Use ProcessPoolExecutor to parallelize the copying process
    with ProcessPoolExecutor() as executor:
        list(executor.map(classify_and_copy, to_process))

    print("Data separation completed.")

if __name__ == "__main__":
    main()
