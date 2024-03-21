import os
import pandas as pd
from PIL import Image
import re

def remove_quotes(path):
    return re.sub(r'^[\'\"]|[\'\"]$', '', path)

def prompt_for_paths():
    labels_path = remove_quotes(input("Enter the path to the folder (labels) containing the label .txt files: "))
    images_path = remove_quotes(input("Enter the path to the folder (images) containing the images: "))
    mapping_path = remove_quotes(input("Enter the path to the csv file 'bangla_yolo_class_mapping.csv': "))

    return labels_path, images_path, mapping_path

def get_image_dimensions(image_path):
    with Image.open(image_path) as img:
        return img.width, img.height

def convert_annotations_to_yolo(labels_path, images_path, class_mapping):
    for txt_file in os.listdir(labels_path):
        if txt_file.endswith('.txt'):
            base_filename = os.path.splitext(txt_file)[0]
            image_filename = base_filename + '.tif' 
            image_path = os.path.join(images_path, image_filename)
            if not os.path.exists(image_path):
                print(f"Image file {image_filename} not found. Skipping...")
                continue

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

def main():
    labels_path, images_path, mapping_path = prompt_for_paths()
    class_mapping = pd.read_csv(mapping_path, encoding='utf-8')
    print('running ...')
    convert_annotations_to_yolo(labels_path, images_path, class_mapping)

if __name__ == "__main__":
    main()
