"""
This script is designed to refine the classification of a dataset that has been 
previously separated into characters and diacritics (yolo notation). It processes 
the label files within each separated directory and removes any entries that do 
not match the intended classification for that directory. After running, the separated 
data directories will contain label files that are strictly relevant to their respective
classifications.
"""

import pandas as pd
import os
import sys
from concurrent.futures import ProcessPoolExecutor
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from config_local import SEPARATED_C_DATA_DIR, SEPARATED_D_DATA_DIR, BANGLA_YOLO_CLASS_MAPPING

def load_class_mapping():
    # Load the YOLO class mapping from the CSV file and return it as a dictionary.
    class_mapping_df = pd.read_csv(BANGLA_YOLO_CLASS_MAPPING)
    return dict(zip(class_mapping_df.yolo_class, class_mapping_df.character_class))

def refine_single_label(file_path, desired_class, class_mapping):
    # Refine a single label file to include only entries matching the desired class.
    with open(file_path, 'r') as file:
        lines = file.readlines()

    # Filter out undesired classes and write back to file
    new_lines = [line for line in lines if class_mapping[int(line.split()[0])] == desired_class]
    with open(file_path, 'w') as file:
        file.writelines(new_lines)

def refine_labels_parallel(directory, desired_class, class_mapping):
    # Use ProcessPoolExecutor to parallelize the refinement of label files
    label_dir = os.path.join(directory, 'labels')
    file_paths = [os.path.join(label_dir, f) for f in os.listdir(label_dir) if f.endswith('.txt')]
    
    # Define a partial function to encapsulate additional arguments
    from functools import partial
    refine_func = partial(refine_single_label, desired_class=desired_class, class_mapping=class_mapping)
    
    with ProcessPoolExecutor() as executor:
        executor.map(refine_func, file_paths)

def main():
    user_confirmation = input("Do you want to proceed with data refinement? (y/n): ")
    if user_confirmation.lower() != 'y':
        print("Operation cancelled by the user.")
        sys.exit(1)
    
    class_mapping = load_class_mapping()

    # Refine character data to remove diacritics
    print("Refining character data...")
    refine_labels_parallel(SEPARATED_C_DATA_DIR, 'c', class_mapping)

    # Refine diacritic data to remove characters
    print("Refining diacritic data...")
    refine_labels_parallel(SEPARATED_D_DATA_DIR, 'd', class_mapping)

    print("Data refinement completed.")

if __name__ == "__main__":
    main()
