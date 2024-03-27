"""
Remove lines that is not if interest and txt/tif pairs that have become empty. 
"""

import os
import re
import pandas as pd
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from config_local import BANGLA_YOLO_CLASS_MAPPING, BANGLA_CONFIG_JSON
import json

def remove_quotes(path):
    """Remove leading and trailing quotes from a path string."""
    return re.sub(r'^[\'\"]|[\'\"]$', '', path)

def filter_label_files(data_type_dir, constraints, constraints_conjunct):
    """Filter label files within a specified directory based on given constraints."""
    df = pd.read_csv(BANGLA_YOLO_CLASS_MAPPING, encoding='utf-8')
    removed_files = []  # Keep track of files marked for removal

    for sub_dir in ['train', 'validation', 'test']:
        label_dir = os.path.join(data_type_dir, sub_dir, 'labels')
        print(f'In subdir {sub_dir}')
        for label_file in os.listdir(label_dir):
            file_path = os.path.join(label_dir, label_file)
            with open(file_path, 'r') as f:
                lines = f.readlines()
            new_lines = []
            for line in lines:
                yolo_class = int(line.split()[0])
                character = df[df['yolo_class'] == yolo_class]['bangla_character'].iloc[0]
                bangla_class = [format(ord(char), '04X').upper() for char in character]
                #print(f'bangla_class: {bangla_class}')
                if len(bangla_class) == 1: 
                    bangla_char = bangla_class[0]
                    if bangla_char in constraints: 
                        new_lines.append(line)
                        #print (f'Matched: {bangla_char} to constraint')

                # elif len(bangla_class) == 2:
                #     if bangla_class[0] in constraints:
                #         line.split()[0] = ban
                #     elif bangla_class[1] in constraints: 
                #         pass

                #     else: 
                        
                #         new_lines.append(line) 


                elif bangla_class in constraints_conjunct:

                     
                    new_lines.append(line) 
                    #print (f'Matched: {bangla_class} to constraints')

                # if bangla_class in constraints or any(bangla_class in conj for conj in constraints_conjunct):
                #     new_lines.append(line)

            if new_lines:
                with open(file_path, 'w') as f:
                    f.writelines(new_lines)
            else:
                removed_files.append(file_path)  # Add to the list of removed files

    # Display Summary
    if removed_files:
        print(f"Identified {len(removed_files)} label files for potential removal from {data_type_dir}:")
        for file in removed_files[:5]:  # Show top 5
            print(f"  {file}")
        if len(removed_files) > 5:
            print(f"... and {len(removed_files) - 5} more files.")

        # Confirmation
        if input("Do you want to proceed with label file removal? (y/n): ").lower() == 'y':
            for file_path in removed_files:
                os.remove(file_path)
            print("Label files successfully removed.")
            return True
        else: 
            print("No labeled files where removed.")
            return False


def remove_orphaned_images(data_type_dir):
    """Remove images with no corresponding label file."""
    for sub_dir in ['train','validation', 'test']:
        image_dir = os.path.join(data_type_dir, sub_dir ,'images')
        label_dir = os.path.join(data_type_dir, sub_dir ,'labels')
        for image_file in os.listdir(image_dir):
            base_name = os.path.splitext(image_file)[0]
            label_file = f"{base_name}.txt"
            if not os.path.exists(os.path.join(label_dir, label_file)):
                os.remove(os.path.join(image_dir, image_file))  # Remove orphaned image
                print(os.path.join(image_dir, image_file))

def load_bangla():
    """Load a JSON file and return its content as Python data structures."""
    with open(BANGLA_CONFIG_JSON, 'r', encoding='utf-8') as file:
        data = json.load(file)
    return data

def process_data(base_folder):
    """Process c_data and d_data folders based on constraints and remove orphaned images."""
    bc = load_bangla() 
    for data_type in ['c_data', 'd_data']:
        if data_type == 'c_data': 
            constraints = bc['C_NET_2019_CONSTRAINT'] 
            constraints_conjunct = bc['C_NET_2019_CONSTRAINT_CONJUNT']
            
        else: 
            constraints = bc['D_NET_2019_CONSTRAINT']
            constraints_conjunct = bc['D_NET_2019_CONSTRAINT_CONJUNT'] + bc['DEP_VOWELS_CONSONANTS']

        data_type_dir = os.path.join(base_folder, data_type)
        print(f"Processing {data_type}...")
        if filter_label_files(data_type_dir, constraints, constraints_conjunct):
            remove_orphaned_images(data_type_dir)
        

    print("Processing completed.")

def main():
    base_folder = remove_quotes(input("Enter the path to the dataset folder: "))
    process_data(base_folder)
    print('Dataset filtering based on constraints has been completed.')

if __name__ == "__main__":
    main()
