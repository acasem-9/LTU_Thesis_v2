'''
This script converts bounding box coordinates in YOLO formatted annotation files between absolute and relative formats.
Users can specify whether to convert from absolute (pixel) coordinates to relative (proportional to image dimensions) coordinates,
or from relative to absolute. The script processes all text files in the specified 'labels' folder and uses corresponding
image files from the 'images' folder to determine image dimensions for accurate conversions.
'''

import os
import glob
import cv2
from pathlib import Path

def convert_coordinates(mode, bbox, img_width, img_height):
    if mode == 'to_relative':
        # Convert from absolute (pixels) to relative (fraction of dimension)
        x_center, y_center, width, height = bbox
        return [x_center / img_width, y_center / img_height, width / img_width, height / img_height]
    elif mode == 'to_absolute':
        # Convert from relative to absolute
        x_center, y_center, width, height = bbox
        return [float(x_center * img_width), float(y_center * img_height), float(width * img_width), float(height * img_height)]

def process_files(labels_path, images_path, mode):
    label_files = glob.glob(os.path.join(labels_path, '*.txt'))
    for label_file in label_files:
        image_file = os.path.join(images_path, Path(label_file).stem + '.tif')
        img = cv2.imread(image_file)
        img_height, img_width = img.shape[:2]

        with open(label_file, 'r') as file:
            lines = file.readlines()

        with open(label_file, 'w') as file:
            for line in lines:
                parts = line.strip().split()
                class_id = int(parts[0])
                bbox = list(map(float, parts[1:5]))
                converted_bbox = convert_coordinates(mode, bbox, img_width, img_height)
                new_line = f"{class_id} {' '.join(map(str, converted_bbox))} {' '.join(parts[5:])}\n"
                file.write(new_line)

def main():
    labels_folder = input("Enter the path to the 'labels' folder: ").strip('"')
    conversion_direction = input("Do you want to translate from 'absolute' to 'relative' (a-t-r) or 'relative' to 'absolute' (r-t-a)? ").strip().lower()
    mode = 'to_relative' if conversion_direction == 'a-t-r' else 'to_absolute'

    images_folder = Path(labels_folder).parent / 'images'

    process_files(labels_folder, images_folder, mode)
    print("Conversion completed successfully.")

if __name__ == "__main__":
    main()
