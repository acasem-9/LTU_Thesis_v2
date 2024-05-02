"""
SKIP THIS STEP IF ORIGINAL DATASET IS TO BE USED!!! 

This script generates a new dataset from a base dataset, ensuring a user-
specified minimum number of observations per object class for the training set. 
It also copies validation and test sets to the new dataset structure. 

Tip: Take into account the comming split into e.g., 80-10-10 --> #obs per cls
     to get the 'right' num. of obs. in train folder. 
"""
import os
import shutil
import random
import re
from collections import defaultdict
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from config_local import SEPARATED_C_DATA_DIR, SEPARATED_D_DATA_DIR

def remove_quotes(path):
    return re.sub(r'^[\'\"]|[\'\"]$', '', path)

def read_txt_file(file_path):
    with open(file_path, 'r') as f:
        return [int(line.split()[0]) for line in f.readlines()]

def sample_folder(data_type_dir, min_obs, output_data_type_dir):
    print('Calculating sample distribution...')
    contains = defaultdict(list)
    label_dir = os.path.join(data_type_dir, 'labels')
    for txt_file in os.listdir(label_dir):
        classes_in_file = read_txt_file(os.path.join(label_dir, txt_file))
        for cls in set(classes_in_file):
            contains[cls].append(txt_file)
    
    contains = dict(sorted(contains.items(), key=lambda item: len(item[1])))
    samples = []
    
    # Sampling
    for cls, txt_files in contains.items():
        existing_count = sum(1 for f in samples if f in txt_files)
        min_required = max(0, min_obs - existing_count)
        
        # Over-sample or under-sample
        if len(txt_files) > min_required:
            sampled_files = random.sample(txt_files, min_required)
        else:
            sampled_files = txt_files + random.choices(txt_files, k=min_required-len(txt_files))
        
        samples.extend(sampled_files)
    
    # Count and print object class counts
    counts = defaultdict(int)
    for f in samples:
        classes_in_file = read_txt_file(os.path.join(label_dir, f))
        for cls in classes_in_file:
            counts[cls] += 1

    counts = dict(sorted(counts.items(), key=lambda item: item[1]))
    print("Counts per object class:", counts)
    print(f"Number of object classes: {len(contains)}")
    
    user_input = input(f"Do you want to create the {data_type_dir.split('/')[-1]} dataset based on this sample? (y/n): ")
    if user_input.lower() == 'y':
        os.makedirs(os.path.join(output_data_type_dir, 'images'))
        os.makedirs(os.path.join(output_data_type_dir, 'labels'))
        print('Creating new dataset...')
        # Copy files to new dataset
        for f in set(samples):
            copy_count = samples.count(f)
            for i in range(copy_count):
                suffix = f"_{i}" if i > 0 else ""
                shutil.copy(os.path.join(label_dir, f), os.path.join(output_data_type_dir, 'labels', f"{f[:-4]}{suffix}.txt"))
                shutil.copy(os.path.join(label_dir.replace('labels', 'images'), f"{f[:-4]}.tif"), 
                            os.path.join(output_data_type_dir, 'images', f"{f[:-4]}{suffix}.tif"))
        
        print(f"Dataset created at {output_data_type_dir}")

# def create_new_dataset_for_separated_folders(base_folders, min_obs):
#     for base_folder in base_folders:
#         base_name = base_folder.strip(os.path.sep).split(os.path.sep)[-1]
#         print(f'Processing {base_name}...')
#         new_dataset_suffix = f"_{min_obs}"
#         new_dataset_name = f"{base_name}{new_dataset_suffix}"
#         output_path = os.path.join(os.path.dirname(base_folder), new_dataset_name)
        
#         if os.path.exists(output_path):
#             user_confirm = input(f"{output_path} exists. Overwrite? (y/n): ")
#             if user_confirm.lower() != 'y':
#                 print("Operation cancelled.")
#                 continue
        
#         shutil.rmtree(output_path, ignore_errors=True)
#         os.makedirs(output_path)
        
#         data_type_dir = base_folder
#         output_data_type_dir = output_path  # Directly use the constructed path
        
#         os.makedirs(output_data_type_dir, exist_ok=True)
        
#         # Sample and process the train folder
#         sample_folder(data_type_dir, min_obs, output_data_type_dir)
        
#         print(f"New dataset created at {output_path}")


def main():
    user_confirmation = input("Do you want to proceed with the script? (y/n): ")
    if user_confirmation.lower() != 'y':
        print("Operation cancelled by the user.")
        return

    min_obs = int(input("Enter the minimum number of observations per object class: "))
    raw_data_path = input("Enter the path to the raw/base dataset to make the over/under sampling from: ").strip('"')
    output_path = input("Enter the output path (parent folder) for the new sampled dataset: ").strip('"')
    #create_new_dataset_for_separated_folders([SEPARATED_C_DATA_DIR, SEPARATED_D_DATA_DIR], min_obs)
    sample_folder(raw_data_path, min_obs, output_path)


if __name__ == "__main__":
    main()
