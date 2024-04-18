"""
The script splits the separated Bangla script datasets (characters and diacritics) 
into training, validation and testing subsets based on a user-specified ratio for
the number of image/lable pairs. 
"""

import os
import shutil
import random
from concurrent.futures import ProcessPoolExecutor
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from config_local import DATA_DIR

def prompt_for_split():
    while True:
        split_input = input("Enter the train-validation-test split ratio (e.g., '70-15-15'): ")
        try:
            train, validation, test = map(int, split_input.split('-'))
            if train + validation + test == 100:
                return train, validation, test
            else:
                print("The sum of the split ratio must equal 100.")
        except ValueError:
            print("Invalid format. Please enter the ratio in the format 'xx-yy-zz'.")

def confirm_overwrite(directory):
    if os.path.exists(directory):
        response = input(f"The directory {directory} already exists. Do you want to overwrite it? (yes/no): ").lower()
        return response == 'yes'
    return True

def create_directories(base_path):
    sub_dirs = ['train/images', 'train/labels', 'validation/images', 'validation/labels', 'test/images', 'test/labels']
    for sub_dir in sub_dirs:
        dir_path = os.path.join(base_path, sub_dir)
        if os.path.exists(dir_path):
            shutil.rmtree(dir_path)
        os.makedirs(dir_path)

def copy_file(source, destination):
    shutil.copy2(source, destination)

def process_data(class_dir, split_ratios, source_images_dir, source_labels_dir):
    label_files = [f for f in os.listdir(source_labels_dir) if f.endswith('.txt')]
    random.shuffle(label_files)

    train_split, validation_split = split_ratios[0], split_ratios[0] + split_ratios[1]
    train_end = int(len(label_files) * (train_split / 100))
    validation_end = int(len(label_files) * (validation_split / 100))

    train_files = label_files[:train_end]
    validation_files = label_files[train_end:validation_end]
    test_files = label_files[validation_end:]

    with ProcessPoolExecutor() as executor:
        tasks = []
        for file_set, subdir in [(train_files, 'train'), (validation_files, 'validation'), (test_files, 'test')]:
            images_subdir = os.path.join(class_dir, subdir, 'images')
            labels_subdir = os.path.join(class_dir, subdir, 'labels')
            for file in file_set:
                img_source = os.path.join(source_images_dir, file.replace('.txt', '.tif'))
                img_destination = os.path.join(images_subdir, file.replace('.txt', '.tif'))
                label_source = os.path.join(source_labels_dir, file)
                label_destination = os.path.join(labels_subdir, file)

                tasks.append(executor.submit(copy_file, img_source, img_destination))
                tasks.append(executor.submit(copy_file, label_source, label_destination))

        for task in tasks:
            task.result()

def main():
    user_confirmation = input("Do you want to proceed? (y/n): ")
    if user_confirmation.lower() != 'y':
        print("Operation cancelled by the user.")
        sys.exit(1)
    
    split_ratios = prompt_for_split()
    base_dataset_dir = os.path.join(DATA_DIR, f"dataset_{split_ratios[0]}-{split_ratios[1]}-{split_ratios[2]}")

    if confirm_overwrite(base_dataset_dir):
        separated_c = input("Enter the path to the separated_c_data to use: ").strip('"')
        separated_d = input("Enter the path to the separated_d_data to use: ").strip('"')

        for class_type, source_dir in zip(['c_data', 'd_data'], [separated_c, separated_d]):
            target_dir = os.path.join(base_dataset_dir, class_type)
            create_directories(target_dir)

            source_images_dir = os.path.join(source_dir, 'images')
            source_labels_dir = os.path.join(source_dir, 'labels')
            process_data(target_dir, split_ratios, source_images_dir, source_labels_dir)
            print(f"Processed {class_type} data.")
    else:
        print("Operation cancelled by the user.")

    print("Dataset splitting completed.")

if __name__ == "__main__":
    main()