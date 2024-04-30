"""
This script converts Bangla character annotations into the YOLO format from the Bois State Handwritten Bangla Dataset annotation style. 
It prompts the user for paths to folders containing label files and images, along with the path to a CSV file mapping 
Bangla characters to YOLO class IDs. For each annotation, it calculates the center coordinates, width, and height relative 
to the image dimensions, and associates each character with its corresponding YOLO class ID. The script then saves these 
YOLO-formatted annotations, replacing the original label files.
"""

import os
import pandas as pd
from PIL import Image
import re
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from config_local import WORD_SEPARATED_DIR, BANGLA_YOLO_CLASS_MAPPING

def remove_quotes(path):
    return re.sub(r'^[\'\"]|[\'\"]$', '', path)

def get_image_dimensions(image_path):
    with Image.open(image_path) as img:
        return img.width, img.height

def process_file(txt_file, labels_path, images_path, class_mapping):
    base_filename = os.path.splitext(txt_file)[0]
    image_filename = base_filename + '.tif' 
    image_path = os.path.join(images_path, image_filename)
    if not os.path.exists(image_path):
        print(f"Image file {image_filename} not found. Skipping...")
        return

    image_width, image_height = get_image_dimensions(image_path)
    txt_file_path = os.path.join(labels_path, txt_file)
    df = pd.read_csv(txt_file_path, sep=' ', header=None, names=['Line', 'Word', 'Char', 'Character', '-', 'Coordinates'], encoding='utf-8')
    yolo_annotations = []

    for _, row in df.iterrows():
        character = row['Character']
        coords = [int(x) for x in row['Coordinates'].split(',')]
        x_center = (coords[0] + coords[2] / 2) / image_width
        y_center = (coords[1] + coords[3] / 2) / image_height
        width = coords[2] / image_width
        height = coords[3] / image_height
        class_id = class_mapping.loc[class_mapping['bangla_character'] == character, 'yolo_class'].values[0]
        yolo_annotations.append(f"{class_id} {x_center} {y_center} {width} {height}")

    # Save YOLO annotations to new .txt file, replacing the old one
    with open(txt_file_path, 'w', encoding='utf-8') as f:
        for annotation in yolo_annotations:
            f.write("%s\n" % annotation)

def convert_annotations_to_yolo_parallel(labels_path, images_path, class_mapping):
    txt_files = [f for f in os.listdir(labels_path) if f.endswith('.txt')]
    with ThreadPoolExecutor() as executor:
        futures = [executor.submit(process_file, txt_file, labels_path, images_path, class_mapping) for txt_file in txt_files]
        for future in as_completed(futures):
            future.result()

def main():
    labels_path = os.path.join(WORD_SEPARATED_DIR, 'labels')
    images_path = os.path.join(WORD_SEPARATED_DIR, 'images')
    mapping_path = BANGLA_YOLO_CLASS_MAPPING
    class_mapping = pd.read_csv(mapping_path, encoding='utf-8')
    print('Processing...')
    convert_annotations_to_yolo_parallel(labels_path, images_path, class_mapping)
    print('Done processing.')

if __name__ == "__main__":
    main()
