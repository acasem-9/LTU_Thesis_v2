import os
import matplotlib.pyplot as plt


"""
This script reads through all the .txt files in a user-specified 'labels' folder
and counts the occurrences of each object class. The script sorts and prints the counts 
of each object class to the terminal. It also produces a bar plot to visualize the 
distribution of object classes across all files.

Last modified 2024-02-21 by Carl 
"""


def count_classes(labels_path):
    class_count = {}  # Dictionary to store the count of each object class

    # Loop through each txt file in the labels folder
    for txt_file in os.listdir(labels_path):
        if txt_file.endswith(".txt"):
            with open(os.path.join(labels_path, txt_file), "r") as f:
                lines = f.readlines()
                for line in lines:
                    class_id = int(line.split(" ")[0])  # Extract the class ID (first element before space)
                    class_count[class_id] = class_count.get(class_id, 0) + 1  # Increment the count of the class ID

    # Sort the dictionary by class ID
    sorted_count = dict(sorted(class_count.items()))
    
    return sorted_count

if __name__ == "__main__":
    # Get labels directory from user and remove quotes if any
    labels_path = input("Please enter the path to the labels directory: ").replace('"', '')

    # Count occurrences of each object class
    sorted_count = count_classes(labels_path)
    
    # Print the counts
    print("Counts of each object class:")
    for class_id, count in sorted_count.items():
        print(f"Class {class_id}: {count}")

    # Generate bar plot for the counts
    plt.bar(sorted_count.keys(), sorted_count.values(), color='blue')
    plt.xlabel('Object Class')
    plt.ylabel('Count')
    plt.yscale('log')
    plt.title(f'Object Class Distribution in {labels_path}')
    plt.show()
