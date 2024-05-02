'''
The script sorts all txt files in a given labels folder to appear based on their 
x-position rather than ordered after object class. This enables further scripts 
to construct the word mapping based on detected characters. 
'''

import os
import glob

def sort_detections_by_x(filepath):
    with open(filepath, 'r') as file:
        detections = file.readlines()

    # Parse each line to extract the starting x-coordinate and sort by this value
    sorted_detections = sorted(detections, key=lambda x: float(x.split()[1]))

    # Write the sorted detections back to the file
    with open(filepath, 'w') as file:
        file.writelines(sorted_detections)

def main():
    labels_folder = input("Enter the path to the 'detections/labels' folder: ").strip('"')

    # Iterate over each text file in the directory and sort its detections
    label_files = glob.glob(os.path.join(labels_folder, '*.txt'))
    print('Processing...')
    for file_path in label_files:
        sort_detections_by_x(file_path)

    print(f"All label files have been sorted based on x-coordinates in {labels_folder}.")

if __name__ == "__main__":
    main()
