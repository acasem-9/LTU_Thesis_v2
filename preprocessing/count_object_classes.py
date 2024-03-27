"""
This script reads through all the .txt files in a user-specified 'labels' folder
and counts the occurrences of each object class. The script sorts and prints the counts 
of each object class to the terminal. It also produces a bar plot to visualize the 
distribution of object classes across all files.

"""

import os
import matplotlib.pyplot as plt
import sys 
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

def count_classes(labels_path):
    class_count = {} 

    for txt_file in os.listdir(labels_path):
        if txt_file.endswith(".txt"):
            with open(os.path.join(labels_path, txt_file), "r") as f:
                lines = f.readlines()
                for line in lines:
                    class_id = int(line.split(" ")[0])  # Extract the class ID (first element before space)
                    class_count[class_id] = class_count.get(class_id, 0) + 1 

    sorted_count = dict(sorted(class_count.items()))
    
    return sorted_count

if __name__ == "__main__":
    labels_path = input("Enter the path to the labels directory: ").replace('"', '')

    sorted_count = count_classes(labels_path)
    print("Counts of each object class:")
    for class_id, count in sorted_count.items():
        print(f"Class {class_id}: {count}")

    plt.bar(sorted_count.keys(), sorted_count.values(), color='blue')
    plt.xlabel('Object Class')
    plt.ylabel('Count')
    plt.yscale('log')
    plt.title(f'Object Class Distribution in {labels_path}')
    plt.show()
