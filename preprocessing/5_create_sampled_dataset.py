
'''
This script performs a custom sampling procedure to create a new dataset for YOLO object detection training.
The new dataset aims to have a user-defined minimum number of observations for each object class.

Last updated 2024-02-21 by Carl
'''
import os
import random
import shutil
from collections import defaultdict
import re

def read_txt_file(file_path):
    with open(file_path, 'r') as f:
        return [int(line.split()[0]) for line in f.readlines()]

def remove_quotes(path):
    return re.sub(r'^[\'\"]|[\'\"]$', '', path)

def main():
    # Step 1: User input for minimum number of observations per class
    min_obs = int(input("Enter the minimum number of observations per object class: "))
    
    # Step 2: Initialize 'contains' dictionary
    contains = defaultdict(list)

    # Step 3: Populate 'contains' dictionary
    label_dir = remove_quotes(input("Enter the path to the folder (labels) containing the label .txt files: "))
    for txt_file in os.listdir(label_dir):
        classes_in_file = read_txt_file(os.path.join(label_dir, txt_file))
        for cls in set(classes_in_file):
            contains[cls].append(txt_file)
    
    # Step 3.5: Sort 'contains' by the length of each list
    contains = dict(sorted(contains.items(), key=lambda item: len(item[1])))

    # Step 4: Initialize 'samples' list
    samples = []
    
    # Step 5: Sampling Loop
    for cls, txt_files in contains.items():
        existing_count = sum(1 for f in samples if f in txt_files)
        min_required = max(0, min_obs - existing_count)
        
        # Over-sample or Under-sample
        if len(txt_files) > min_required:
            sampled_files = random.sample(txt_files, min_required)
        else:
            sampled_files = txt_files + random.choices(txt_files, k=min_required-len(txt_files))
        
        samples.extend(sampled_files)
    
    # Step 6: Count and print object class counts
    counts = defaultdict(int)
    for f in samples:
        classes_in_file = read_txt_file(os.path.join(label_dir, f))
        for cls in classes_in_file:
            counts[cls] += 1

    counts = dict(sorted(counts.items(), key=lambda item: item[1]))
    print("Counts per object class:", counts)
    print(f"Number of object classes: {len(contains)}")
    
    # Step 7: User Confirmation
    user_input = input("Do you want to create the dataset based on this sample? (y/n): ")
    if user_input.lower() == 'y':
        # Create new dataset folder
        classes = len(contains)
        
        output_path = remove_quotes(input("Enter the path to the output folder: "))
        output_path = os.path.join(output_path, f"training_dataset-{classes}classes-{min_obs}min_obs")
        
        if os.path.exists(output_path):
            print(f"Folder {output_path} already exists. Please remove it manually and tun the script again.")
            return
        os.makedirs(os.path.join(output_path, 'images'))
        os.makedirs(os.path.join(output_path, 'labels'))
        
        # Copy files to new dataset
        for f in set(samples):
            copy_count = samples.count(f)
            for i in range(copy_count):
                suffix = f"_{i}" if i > 0 else ""
                shutil.copy(os.path.join(label_dir, f), os.path.join(output_path, 'labels', f"{f[:-4]}{suffix}.txt"))
                shutil.copy(os.path.join(label_dir.replace('labels', 'images'), f"{f[:-4]}.jpg"), 
                            os.path.join(output_path, 'images', f"{f[:-4]}{suffix}.jpg"))
        
        print(f"Dataset created at {output_path}")
        
if __name__ == "__main__":
    main()
