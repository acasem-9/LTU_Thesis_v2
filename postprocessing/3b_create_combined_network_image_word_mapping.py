'''
This script processes YOLO label files that classify detections into Bangla characters. It combines detections
from separate label sets (c-data and d-data), each potentially classified under different mappings (for consonants and dependent characters).

'''
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
    return mapping

def read_and_sort_detections(file_path, mapping):
    detections = []
    with open(file_path, 'r') as file:
        for line in file:
            parts = line.strip().split()
            class_index = int(parts[0])
            x_center = float(parts[1])
            detections.append((x_center, mapping[class_index]))
    return sorted(detections, key=lambda x: x[0])

def combine_detections_old(c_labels_path, d_labels_path, c_mapping, d_mapping):
    image_to_word = {}
    c_label_files = glob.glob(os.path.join(c_labels_path, '*.txt'))
    d_label_files = glob.glob(os.path.join(d_labels_path, '*.txt'))

    for c_file_path in c_label_files:
        image_name = Path(c_file_path).stem
        c_detections = read_and_sort_detections(c_file_path, c_mapping)
        d_file_path = os.path.join(d_labels_path, f"{image_name}.txt")
        d_detections = read_and_sort_detections(d_file_path, d_mapping) if os.path.exists(d_file_path) else []
        
        combined_detections = sorted(c_detections + d_detections, key=lambda x: x[0])
        image_to_word[image_name] = ''.join([det[1] for det in combined_detections])

    return image_to_word

def combine_detections(c_labels_path, d_labels_path, c_mapping, d_mapping):
    image_to_word = {}
    # Collect all unique image names from both c-labels and d-labels
    c_label_files = glob.glob(os.path.join(c_labels_path, '*.txt'))
    d_label_files = glob.glob(os.path.join(d_labels_path, '*.txt'))
    all_image_names = set(Path(file).stem for file in c_label_files).union(Path(file).stem for file in d_label_files)

    for image_name in all_image_names:
        c_file_path = os.path.join(c_labels_path, f"{image_name}.txt")
        d_file_path = os.path.join(d_labels_path, f"{image_name}.txt")
        
        c_detections = read_and_sort_detections(c_file_path, c_mapping) if os.path.exists(c_file_path) else []
        d_detections = read_and_sort_detections(d_file_path, d_mapping) if os.path.exists(d_file_path) else []
        
        combined_detections = sorted(c_detections + d_detections, key=lambda x: x[0])
        image_to_word[image_name] = ''.join([det[1] for det in combined_detections])

    return image_to_word


def main():
    c_labels_folder = input("Enter the path to the c-labels folder: ").strip('"')
    d_labels_folder = input("Enter the path to the d-labels folder: ").strip('"')
    c_csv_mapping_path = input("Enter the path to the Bangla YOLO class mapping CSV for c-data: ").strip('"')
    d_csv_mapping_path = input("Enter the path to the Bangla YOLO class mapping CSV for d-data: ").strip('"')
    output_path = input("Enter the path to the output file: ").strip('"')
    combination_type = input("Enter the type of combination ('detection' or 'test'): ").strip().lower()
    
    # Load mappings
    c_mapping = load_class_to_bangla_mapping(c_csv_mapping_path)
    d_mapping = load_class_to_bangla_mapping(d_csv_mapping_path)
    
    # Process label files to form image to word mappings
    mappings = combine_detections(c_labels_folder, d_labels_folder, c_mapping, d_mapping)
    
    # Save the results
    output_file_suffix = '_detection' if combination_type == 'detection' else '_test'
    output_file = f"{output_path}/{output_file_suffix}.txt"
    with open(output_file, 'w', encoding='utf-8') as file:
        for image_name, word in mappings.items():
            file.write(f"{image_name}.tif {word}\n")

    print(f"Image-to-word mappings saved in {output_file}")

if __name__ == "__main__":
    main()
