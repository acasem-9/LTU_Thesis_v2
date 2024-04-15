import csv
import glob
import os
from pathlib import Path

def load_class_to_bangla_mapping(csv_path):
    mapping = {}
    with open(csv_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            mapping[int(row['yolo_class'])] = row['bangla_character']
    print(mapping)
    return mapping

def process_label_files(labels_path, mapping):
    image_to_word = []
    label_files = glob.glob(os.path.join(labels_path, '*.txt'))
    for file_path in label_files:
        word = ''
        with open(file_path, 'r') as file:
            for line in file:
                parts = line.strip().split()
                class_index = int(parts[0])
                word += mapping[class_index]
        image_name = Path(file_path).stem + '.tif'
        image_to_word.append(f"{image_name} {word}")
    return image_to_word

def main():
    # User input for paths
    labels_folder = input("Enter the path to the labels folder: ").strip('"')
    csv_mapping_path = input("Enter the path to the Bangla YOLO class mapping CSV (note that hex should be included): ").strip('"')

    # Load YOLO to Bangla character mapping
    class_to_bangla_mapping = load_class_to_bangla_mapping(csv_mapping_path)

    # Process label files to form image to word mappings
    mappings = process_label_files(labels_folder, class_to_bangla_mapping)

    # Save the results
    output_file_path = Path(labels_folder).parent / "image_to_word_mapping.txt"
    with open(output_file_path, 'w', encoding='utf-8') as output_file:
        for mapping in mappings:
            output_file.write(mapping + '\n')

    print(f"Image-to-word mappings saved in {output_file_path}")

if __name__ == "__main__":


    
    main()
