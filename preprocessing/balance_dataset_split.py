"""
This script removes a specified number of .tif/.txt file pairs randomly from
'images' and 'labels' subfolders within a given directory.
    
 """

import os
import random
from glob import glob

def delete_random_file_pairs(num_files, path):

    # Paths to the images and labels subfolders
    images_path = os.path.join(path, 'images')
    labels_path = os.path.join(path, 'labels')
    
    # Check if the directories exist
    if not os.path.exists(images_path) or not os.path.exists(labels_path):
        print("The specified path does not contain 'images' or 'labels' subfolders.")
        return
    
    # Get list of image and label files
    image_files = glob(os.path.join(images_path, '*.tif'))
    label_files = [os.path.join(labels_path, os.path.basename(f).replace('.tif', '.txt')) for f in image_files]
    
    # Ensure both tif and txt files exist
    paired_files = [(img, lbl) for img, lbl in zip(image_files, label_files) if os.path.exists(lbl)]
    
    # Check if the number of files requested to delete is available
    if len(paired_files) < num_files:
        print(f"Not enough file pairs to remove. Only {len(paired_files)} pairs available.")
        return
    
    # Randomly select file pairs to delete
    to_delete = random.sample(paired_files, num_files)
    
    # Delete the files
    for img, lbl in to_delete:
        os.remove(img)
        os.remove(lbl)
        print(f"Removed {img} and {lbl}")
    
    print(f"Successfully removed {num_files} file pairs.")

if __name__ == "__main__":
    num = int(input("Enter the number of tif/txt file pairs to remove: "))
    directory = input("Enter the path to the folder (train/val/test): ").strip('"')
    delete_random_file_pairs(num, directory)
