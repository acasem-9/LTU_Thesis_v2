
"""
This script prompts the user for the path to the 'bangla_yolo_class_mapping.csv' file,
analyzes it to report on character class occurrences ('c' for consonants, independent vowels, and digits; 'd' for others),
aggregated counts for each class, and the total count of characters. 

Last modified 2024-02-21 by Carl 
"""

import pandas as pd
import re

def remove_quotes(path):
    return re.sub(r'^[\'\"]|[\'\"]$', '', path)

def analyze_character_classes(csv_path):
    mapping_df = pd.read_csv(csv_path, encoding='utf-8')
    
    # Print occurrences of each character class
    occurrences = mapping_df['character_class'].value_counts()
    print("\nOccurrences of each character class:")
    print(occurrences)
    
    # Aggregate and print the total count for each character class
    aggregated_counts = mapping_df.groupby('character_class')['count'].sum()
    print("\nAggregated count for each character class:")
    print(aggregated_counts)

    # Print total count of characters
    total_count = mapping_df['count'].sum()
    print(f"\nTotal count of characters: {total_count}")

    # Calculate and print the average count for 'c' and 'd'
    average_counts = mapping_df.groupby('character_class')['count'].mean()
    print("\nAverage count for each character class:")
    print(average_counts)

def main():
    csv_path = input("Enter the path to your 'bangla_yolo_class_mapping.csv' file: ")
    analyze_character_classes(remove_quotes(csv_path))

if __name__ == "__main__":
    main()
