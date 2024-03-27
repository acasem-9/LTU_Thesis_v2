import os
import pandas as pd
from collections import defaultdict
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import config_local as lc
import json

def generate_new_mapping_csv(data_type_dir, constraints, conjuncts, data_type):
    """
    Generate a new CSV file with updated YOLO class mappings based on the specified constraints.
    """
    new_mapping = []
    yolo_class_counter = 0

    # Process individual characters
    for hex_code in constraints:
        char = chr(int(hex_code, 16))
        new_mapping.append([yolo_class_counter, char, '', 'c' if data_type_dir.endswith('c_data') else 'd'])
        yolo_class_counter += 1

    # Process conjuncts
    for conj in conjuncts:
        # Join conjunct characters for CSV entry
        conj_char = ''.join([chr(int(c, 16)) for c in conj])
        new_mapping.append([yolo_class_counter, conj_char, '', 'c' if data_type_dir.endswith('c_data') else 'd'])
        yolo_class_counter += 1

    # Save the new mapping to a CSV file
    new_mapping_df = pd.DataFrame(new_mapping, columns=['yolo_class', 'bangla_character', 'count', 'character_class'])
    new_csv_path = os.path.join(data_type_dir, f'bangla_yolo_class_mapping_{data_type}.csv')
    new_mapping_df.to_csv(new_csv_path, index=False, encoding='utf-8')

    return new_mapping_df

def update_label_files(data_type_dir, new_mapping_df, data_type):
    """
    Update all label files in the dataset to reflect new YOLO class assignments.
    """
    old_mapping_df = pd.read_csv(lc.BANGLA_YOLO_CLASS_MAPPING, encoding='utf-8')
    char_counts = defaultdict(int)
    for sub_dir in ['train', 'validation', 'test']:
        label_dir = os.path.join(data_type_dir, sub_dir, 'labels')
        for label_file in os.listdir(label_dir):
            file_path = os.path.join(label_dir, label_file)
            with open(file_path, 'r') as file:
                lines = file.readlines()
                # print(file_path)
                # print(f'# LINES: {len(lines)}\n')
            # Update lines with new YOLO class assignments
            updated_lines = []
            for line in lines:
            # try:
                parts = line.strip().split()
                old_yolo_class = int(parts[0])
                #print(f'HERE IS THE LINE: {line}\n')
                bangla_character = old_mapping_df[old_mapping_df['yolo_class'] == old_yolo_class]['bangla_character'].iloc[0]

                if new_mapping_df['bangla_character'].isin([bangla_character]).any(): 

                    #bangla_character = new_mapping_df.loc[new_mapping_df['yolo_class'] == old_yolo_class, 'bangla_character'].iloc[0]
                    new_yolo_class = new_mapping_df.loc[new_mapping_df['bangla_character'] == bangla_character, 'yolo_class'].iloc[0]
                    updated_lines.append(f"{new_yolo_class} {' '.join(parts[1:])}\n")
                    char_counts[bangla_character] += 1

                else:
                    bangla_char_comp = [char for char in bangla_character]
                    for comp in bangla_char_comp:
                        if new_mapping_df['bangla_character'].isin([comp]).any():
                            #print(f'processing {comp} from {bangla_char_comp}, and line: {line} from file {file_path}')
                            new_yolo_class = new_mapping_df.loc[new_mapping_df['bangla_character'] == comp, 'yolo_class'].iloc[0]
                            updated_lines.append(f"{new_yolo_class} {' '.join(parts[1:])}\n")
                            char_counts[comp] += 1
                            
                    

            # except IndexError as e:
            #     print(line)
            #     user_confirmation = input("Do you want to proceed? (y/n): ")
            #     if user_confirmation.lower() != 'y':
            #         print("Operation cancelled by the user.")
            #         sys.exit(1)

            # Rewrite the file with updated lines
            with open(file_path, 'w') as file:
                file.writelines(updated_lines)

    # Update counts in new mapping dataframe
    for char, count in char_counts.items():
        new_mapping_df.loc[new_mapping_df['bangla_character'] == char, 'count'] = count

    # Save the updated new mapping to the CSV file again
    new_csv_path = os.path.join(data_type_dir, f'bangla_yolo_class_mapping_{data_type}.csv')
    new_mapping_df.to_csv(new_csv_path, index=False, encoding='utf-8')

def load_bangla(file):
    """Load a JSON file and return its content as Python data structures."""
    with open(file, 'r', encoding='utf-8') as file:
        data = json.load(file)
    return data

def process_data(base_folder):
    """Process c_data and d_data folders to generate new mappings and update label files."""
    bc = load_bangla(lc.BANGLA_CONFIG_JSON)
    for data_type in ['c_data', 'd_data']:
        data_type_dir = os.path.join(base_folder, data_type)
        print(f"Processing {data_type}...")

        if data_type == 'c_data':
            constraints = bc['C_NET_2019_CONSTRAINT']
            constraints_conjunct = bc['C_NET_2019_CONSTRAINT_CONJUNT']

        else:
            constraints = bc['D_NET_2019_CONSTRAINT']
            constraints_conjunct = bc['D_NET_2019_CONSTRAINT_CONJUNT'] #+ bc['DEP_VOWELS_CONSONANTS'] #Add this line for 'all' characters (not limied to the 2019 selection)

        new_mapping_df = generate_new_mapping_csv(data_type_dir, constraints, constraints_conjunct, data_type)
        update_label_files(data_type_dir, new_mapping_df, data_type)


    print("Dataset processing and updating completed.")

def main():
    base_folder = input("Enter the path to the base dataset folder: ").strip('\'\"')

    process_data(base_folder)

if __name__ == "__main__":
    main()
