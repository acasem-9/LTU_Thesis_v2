"""
The script splits the separated Bangla script datasets (characters and diacritics) 
into training, validation and testing subsets based on a user-specified ratio for
the number of pages. 
"""
import os
import shutil
import sys
from concurrent.futures import ThreadPoolExecutor
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
        response = input(f"The directory {directory} already exists. Do you want to overwrite it? (y/n): ").lower()
        return response == 'y'
    return True

def create_directories(base_path):
    sub_dirs = ['train/images', 'train/labels', 'validation/images', 'validation/labels', 'test/images', 'test/labels']
    for sub_dir in sub_dirs:
        dir_path = os.path.join(base_path, sub_dir)
        if os.path.exists(dir_path):
            shutil.rmtree(dir_path)
        os.makedirs(dir_path)

def get_page_number(filename):
    return filename.split('_')[0]

def split_data_based_on_pages(files, split_ratios):
    unique_pages = sorted(set(get_page_number(file) for file in files))
    train_end = int(len(unique_pages) * (split_ratios[0] / 100))
    validation_end = train_end + int(len(unique_pages) * (split_ratios[1] / 100))

    train_pages = set(unique_pages[:train_end])
    validation_pages = set(unique_pages[train_end:validation_end])
    test_pages = set(unique_pages[validation_end:])

    return train_pages, validation_pages, test_pages

def distribute_files_to_folders(source_dir, target_dir, pages_split, file_type):
    def copy_file(file):
        if not file.endswith('.txt') and not file.endswith('.tif'):  # Only process .txt and .tif files
            return
        page_num = get_page_number(file)
        if page_num in pages_split['train']:
            subdir = 'train'
        elif page_num in pages_split['validation']:
            subdir = 'validation'
        else:
            subdir = 'test'
        shutil.copy2(os.path.join(source_dir, file), os.path.join(target_dir, subdir, file_type, file))
    
    # Set up ThreadPoolExecutor to parallelize file copying
    with ThreadPoolExecutor() as executor:
        executor.map(copy_file, os.listdir(source_dir))

def process_data(class_dir, split_ratios, source_images_dir, source_labels_dir):
    label_files = [f for f in os.listdir(source_labels_dir) if f.endswith('.txt')]
    train_pages, validation_pages, test_pages = split_data_based_on_pages(label_files, split_ratios)
    
    print(f'Number of pages to train folder: {len(train_pages)}')
    print(f'Number of pages to validation folder: {len(validation_pages)}')
    print(f'Number of pages to test folder: {len(test_pages)}\n')

    # print(f'Pages to train folder: {train_pages}\n')
    # print(f'Pages to validation folder: {validation_pages}\n')
    # print(f'Pages to test folder: {test_pages}\n')

    pages_split = {
        'train': train_pages,
        'validation': validation_pages,
        'test': test_pages
    }
    
    distribute_files_to_folders(source_labels_dir, class_dir, pages_split, 'labels')
    distribute_files_to_folders(source_images_dir, class_dir, pages_split, 'images')

def main():
    user_confirmation = input("Do you want to proceed? (y/n): ")
    if user_confirmation.lower() != 'y':
        print("Operation cancelled by the user.")
        sys.exit(1)
        
    split_ratios = prompt_for_split()
    base_dataset_dir = os.path.join(DATA_DIR, f"base_dataset_{split_ratios[0]}-{split_ratios[1]}-{split_ratios[2]}-page")

    if confirm_overwrite(base_dataset_dir):
        separated_c = input("Enter the path to the separated_c_data to use: ").strip('"')
        separated_d = input("Enter the path to the separated_d_data to use: ").strip('"')

        for class_type, source_dir in zip(['c_data', 'd_data'], [separated_c, separated_d]):
            target_dir = os.path.join(base_dataset_dir, class_type)
            create_directories(target_dir)

            print(f'\nProcessing {class_type}...')
            source_images_dir = os.path.join(source_dir, 'images')
            source_labels_dir = os.path.join(source_dir, 'labels')
            process_data(target_dir, split_ratios, source_images_dir, source_labels_dir)
            print(f"Processed {class_type} data.")
    else:
        print("Operation cancelled by the user.")

    print("Dataset splitting completed.")

if __name__ == "__main__":
    main()
