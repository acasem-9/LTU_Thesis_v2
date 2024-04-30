"""
This script classifies each Bangla character as either a consonant ('c') or a digit ('d'). 
It reads the mapping file specified by the user, applies the classification based on 
predefined Unicode ranges in 'config_bangla.json', and updates the CSV file with the new 
'character_class' column.
"""

import re
import os
import sys 
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import pandas as pd
import json 
import config_local as lc

def load_configuration(json_filepath):
    """Load the JSON configuration file."""
    with open(json_filepath, 'r', encoding='utf-8') as json_file:
        return json.load(json_file)

def remove_quotes(path):
    return re.sub(r'^[\'\"]|[\'\"]$', '', path)

def get_character_class(character):
    bc = load_configuration(lc.BANGLA_CONFIG_JSON)
    unicode_hex = [format(ord(char), '04X') for char in character]
    if len(unicode_hex) == 1:
        hex_code = unicode_hex[0]
        if hex_code in bc['CONSONANTS'] or hex_code in bc['IND_VOWELS'] or hex_code in bc['DIGITS'] or hex_code in bc['C_NET_ADDITIONAL']:
            return 'c'  
        else:
            return 'd'
    else:
        # Check for conjuncts
        if unicode_hex in bc['CNET_CONJUNCTS']:
            return 'c'
        else:
            return 'd'

def update_character_classes(csv_path):
    mapping_df = pd.read_csv(csv_path, encoding='utf-8')
    mapping_df['character_class'] = mapping_df['bangla_character'].apply(get_character_class)
    mapping_df.to_csv(csv_path, index=False, encoding='utf-8')
    print(f"Updated CSV saved to {csv_path}")

def main():
    user_confirmation = input("Do you want to proceed? (y/n): ")
    if user_confirmation.lower() != 'y':
        print("Operation cancelled by the user.")
        sys.exit(1)
    
    #csv_path = input("Enter the path to your 'bangla_yolo_class_mapping.csv' file: ")
    csv_path = lc.BANGLA_YOLO_CLASS_MAPPING
    update_character_classes(remove_quotes(csv_path))

if __name__ == "__main__":
    main()