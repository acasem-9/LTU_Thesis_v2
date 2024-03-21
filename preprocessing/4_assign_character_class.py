import bangla_config as bc
import pandas as pd
import re

def remove_quotes(path):
    return re.sub(r'^[\'\"]|[\'\"]$', '', path)

def get_character_class(character):
    unicode_codes = [ord(char) for char in character]
    
    for code in unicode_codes:
        if not (code in bc.BANGLA_CONSONANTS or code in bc.BANGLA_IND_VOWELS or code in bc.BANGLA_DIGITS):
            return 'd' 
    return 'c' 

def update_character_classes(csv_path):
    mapping_df = pd.read_csv(csv_path, encoding='utf-8')
    mapping_df['character_class'] = mapping_df['bangla_character'].apply(get_character_class)
    mapping_df.to_csv(csv_path, index=False, encoding='utf-8')
    print(f"Updated CSV saved to {csv_path}")

def main():
    csv_path = input("Enter the path to your 'bangla_yolo_class_mapping.csv' file: ")

    update_character_classes(remove_quotes(csv_path))

if __name__ == "__main__":
    main()