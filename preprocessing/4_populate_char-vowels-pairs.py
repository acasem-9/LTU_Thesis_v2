'''
The scripts appends the dependent vowels (defined as pair of a consonant and a dependent vowel)
identified in the bangla_yolo_class_mapping.csv till DEP_VOWELS_CONSONANTS in the config_bangla.json
'''
import csv
import json
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import config_local as lc

def load_configuration(json_filepath):
    """Load the JSON configuration file."""
    with open(json_filepath, 'r', encoding='utf-8') as json_file:
        return json.load(json_file)

def save_configuration(config, json_filepath):
    """Save the updated configuration back to the JSON file."""
    with open(json_filepath, 'w', encoding='utf-8') as json_file:
        json.dump(config, json_file, ensure_ascii=False, indent=4)

def char_to_unicode_hex(character):
    """Convert characters to Unicode hexadecimal notation."""
    #uni_hex = ''.join(format(ord(c), '04X').upper() for c in char)
    return [format(ord(char), '04X').upper() for char in character]

def process_csv_and_update_config(csv_filepath, config):
    if "DEP_VOWELS_CONSONANTS" not in config:
        config["DEP_VOWELS_CONSONANTS"] = []

    with open(csv_filepath, 'r', encoding='utf-8') as csv_file:
        reader = csv.DictReader(csv_file)
        for row in reader:
            char_hex_list = char_to_unicode_hex(row['bangla_character'])
            # Process characters only if they form a pair (consonant + vowel)
            if len(char_hex_list) == 2:
                if (char_hex_list[0] in config["CONSONANTS"] and char_hex_list[1] in config["DEP_VOWELS"]) or \
                   (char_hex_list[1] in config["CONSONANTS"] and char_hex_list[0] in config["DEP_VOWELS"]):
                    config["DEP_VOWELS_CONSONANTS"].append(char_hex_list)
                    print(f"Identified valid combination added to DEP_VOWELS_CONSONANTS: {char_hex_list}")


def main():
    user_confirmation = input("Do you want to proceed? (y/n): ")
    if user_confirmation.lower() != 'y':
        print("Operation cancelled by the user.")
        sys.exit(1)
   
    config = load_configuration(lc.BANGLA_CONFIG_JSON)

    # Initialize the list for storing combinations if it doesn't already exist
    if "DEP_VOWELS_CONSTANTS" not in config:
        config["DEP_VOWELS_CONSTANTS"] = []

    process_csv_and_update_config(lc.BANGLA_YOLO_CLASS_MAPPING, config)
    save_configuration(config, lc.BANGLA_CONFIG_JSON)
    print("Updated JSON configuration saved with identified combinations.")

if __name__ == "__main__":
    main()
