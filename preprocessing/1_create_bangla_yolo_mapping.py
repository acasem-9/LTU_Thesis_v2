"""
This script reads txt label files containing character annotations, counts the occurrence of each unique Bangla character,
generates a mapping of Bangla characters to YOLO class identifiers based on their frequency, and saves this mapping to a CSV file.
The mapping is done based on the appearence of the objects. 
"""
import os
import pandas as pd
import re
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from config_local import WORD_SEPARATED_DIR

def remove_quotes(path):
    return re.sub(r'^[\'\"]|[\'\"]$', '', path)

def count_characters_in_file(file_path):
    try:
        df = pd.read_csv(file_path, sep=' ', header=None, names=['Line', 'Word', 'Char', 'Character', '-', 'Coordinates'], encoding='utf-8')
        characters = df['Character'].tolist()
        return characters
    except Exception as e:
        print(f"Error processing file {file_path}: {e}")
        return []

def count_unique_characters_parallel(input_path):
    files = [os.path.join(input_path, f) for f in os.listdir(input_path) if f.endswith('.txt')]
    all_characters = []

    with ThreadPoolExecutor(max_workers=10) as executor:
        futures = [executor.submit(count_characters_in_file, file_path) for file_path in files]
        for future in as_completed(futures):
            all_characters.extend(future.result())

    return pd.Series(all_characters).value_counts()

def main():
    user_confirmation = input("Do you want to proceed with data refinement? (y/n): ")
    if user_confirmation.lower() != 'y':
        print("Operation cancelled by the user.")
        sys.exit(1)
        
    input_path = os.path.join(WORD_SEPARATED_DIR, 'labels')
    print('Processing...')
    char_counts = count_unique_characters_parallel(input_path)
    print(char_counts)

    mapping_df = pd.DataFrame({
        'bangla_character': char_counts.index,
        'count': char_counts.values
    }).reset_index().rename(columns={'index': 'yolo_class'})
    mapping_df['character_class'] = ''

    parent_dir = os.path.abspath(os.path.join(input_path, os.pardir))
    csv_path = os.path.join(parent_dir, 'bangla_yolo_class_mapping.csv')
    mapping_df.to_csv(csv_path, index=False)
    print(f"Mapping CSV saved to {csv_path}")

if __name__ == "__main__":
    main()
