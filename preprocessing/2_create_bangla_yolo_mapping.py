import os
import pandas as pd
import re

def remove_quotes(path):
    return re.sub(r'^[\'\"]|[\'\"]$', '', path)

def prompt_for_input_path():
    path = input("Enter the path to the folder containing the label .txt files (the 'labels' folder of interest): ")
    return remove_quotes(path)

def count_unique_characters(input_path):
    all_characters = []
    for txt_file in os.listdir(input_path):
        if txt_file.endswith('.txt'):
            file_path = os.path.join(input_path, txt_file)
            df = pd.read_csv(file_path, sep=' ', header=None, names=['Line', 'Word', 'Char', 'Character', '-', 'Coordinates'], encoding='utf-8')
            all_characters.extend(df['Character'].tolist())
    return pd.Series(all_characters).value_counts()

def create_mapping_dataframe(char_counts):
    mapping_df = pd.DataFrame({
        'bangla_character': char_counts.index,
        'count': char_counts.values
    })
    mapping_df.reset_index(inplace=True)
    mapping_df.rename(columns={'index': 'yolo_class'}, inplace=True)
    mapping_df['character_class'] = ''

    return mapping_df

def save_mapping_csv(mapping_df, input_path):
    parent_dir = os.path.abspath(os.path.join(input_path, os.pardir))
    csv_path = os.path.join(parent_dir, 'bangla_yolo_class_mapping.csv')
    mapping_df.to_csv(csv_path, index=False)
    print(f"Mapping CSV saved to {csv_path}")

def main():
    input_path = prompt_for_input_path()
    print('running...')
    char_counts = count_unique_characters(input_path)
    print(char_counts)
    mapping_df = create_mapping_dataframe(char_counts)
    save_mapping_csv(mapping_df, input_path)

if __name__ == "__main__":
    main()
