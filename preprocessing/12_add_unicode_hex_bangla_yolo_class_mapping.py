"""
This script processes a CSV file containing Bangla characters by adding a new column that 
converts each character into its Unicode hexadecimal notation. The script reads an existing CSV file, 
applies the conversion, and saves the result to a new CSV file with '_hex' appended to the original filename.
"""

import pandas as pd
import os

def char_to_unicode_hex(char):
    """Convert a character to its Unicode hexadecimal notation."""
    return ' '.join(format(ord(c), '04X') for c in char)

def process_csv_add_unicode_hex(input_csv_path):
    """Reads an input CSV, adds a unicode_hex column, and saves to a new CSV file."""
    # Load the CSV file into a DataFrame
    df = pd.read_csv(input_csv_path, encoding='utf-8')
    
    # Apply the conversion function to the 'bangla_character' column and create a new column
    df['unicode_hex'] = df['bangla_character'].apply(char_to_unicode_hex)
    
    # Generate the output file path
    base, ext = os.path.splitext(input_csv_path)
    output_csv_path = f"{base}_hex{ext}"
    
    # Save the updated DataFrame to a new CSV file
    df.to_csv(output_csv_path, index=False, encoding='utf-8')
    print(f"Processed file saved as '{output_csv_path}'.")

def main():
    input_csv_path = input("Enter the path to your bangla_yolo_class_mapping.csv file: ").strip('"')

    # Check if the input file exists
    if not os.path.isfile(input_csv_path):
        print("The file does not exist. Please check the path and try again.")
        return

    # Process the file
    process_csv_add_unicode_hex(input_csv_path)

if __name__ == "__main__":
    main()
