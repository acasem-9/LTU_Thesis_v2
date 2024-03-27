""" 
The script adjust the validation and test folders to be consistent 
with the entries in the train folder. If not in train it gets removed. 
"""
import os

def read_classes_from_file(file_path):
    with open(file_path, 'r') as f:
        return {int(line.split()[0]) for line in f.readlines()}

def find_files_to_remove(label_dir, classes_in_train):
    to_remove = []
    for txt_file in os.listdir(label_dir):
        file_path = os.path.join(label_dir, txt_file)
        file_classes = read_classes_from_file(file_path)
        
        if file_classes.isdisjoint(classes_in_train):
            # If there's any class in file_classes not found in classes_in_train, mark for removal
            to_remove.append(file_path)
    # print(f'classes in train \n{classes_in_train}\n')
    # print(f'to remove: \n{file_classes}')
    return to_remove

def remove_files_and_confirm(to_remove, subset):
    print(f"Identified {len(to_remove)} files for potential removal from {subset}.")
    if len(to_remove) > 0:
        for file in to_remove[:5]:  # Show a sample of files to be removed
            print(f"  {file}")
        if len(to_remove) > 5:
            print(f"... and {len(to_remove) - 5} more files.")
        if input("Do you want to proceed with file removal? (y/n): ").lower() == 'y':
            for file_path in to_remove:
                os.remove(file_path)
                # Remove corresponding image file
                image_path = file_path.replace('.txt', '.tif').replace('/labels/', '/images/')
                if os.path.exists(image_path):
                    os.remove(image_path)
            print("Files successfully removed.")

def process_data_type(data_type_dir):
    classes_in_train = set()
    label_dir_train = os.path.join(data_type_dir, 'train', 'labels')
    for label_file in os.listdir(label_dir_train):
        classes_in_train.update(read_classes_from_file(os.path.join(label_dir_train, label_file)))
    for subset in ['validation', 'test']:
        label_dir = os.path.join(data_type_dir, subset, 'labels')
        to_remove = find_files_to_remove(label_dir, classes_in_train)
        remove_files_and_confirm(to_remove, subset)
    
    print(f'Classes in {os.path.basename(data_type_dir)}: {classes_in_train}')

def main(data_dir):
    for data_type in ['c_data', 'd_data']:
        print(f'Processing {data_type}...')
        data_type_dir = os.path.join(data_dir, data_type)
        process_data_type(data_type_dir)

if __name__ == "__main__":
    data_dir = input("Enter the path to the dataset: ").strip('"')
    main(data_dir)
