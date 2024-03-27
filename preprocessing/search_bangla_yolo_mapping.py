import pandas as pd
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from config_local import BANGLA_YOLO_CLASS_MAPPING

csv_file_path = BANGLA_YOLO_CLASS_MAPPING

# The Bangla character you're searching for
x =  'বা' #  র্প প্র ত্র ক্র প্য প্যা # 'ং' 

def search_character_in_csv(character, csv_path):
    try:
        # Load the CSV file into a DataFrame
        df = pd.read_csv(csv_path)
        
        # Search for the character in the 'bangla_character' column
        results = df[df['bangla_character'] == character]
        
        if not results.empty:
            # If the character is found, get the hexadecimal representation for each composing character
            unicode_hex = [format(ord(char), '04X').upper() for char in character]
            hex_representation = ' '.join([f'U+{hex_code}' for hex_code in unicode_hex])
            return True, results['yolo_class'].values[0], unicode_hex
        else:
            # If the character is not found, return False
            return False, None, None
    except Exception as e:
        print(f"Error reading the CSV file: {e}")
        return False, None, None

# Search for the character and print the result
exists, yolo_class, hex_representation = search_character_in_csv(x, csv_file_path)
if exists:
    print(f"Character '{x}' exists with yolo_class {yolo_class} and hexadecimal representation {hex_representation}.")
else:
    print(f"Character '{x}' does not exist.")