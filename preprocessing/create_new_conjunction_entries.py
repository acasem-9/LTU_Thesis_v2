import csv

def unicode_hex_list(character):
    """Converts a string of characters into a list of hexadecimal unicode code points."""
    return [format(ord(char), '04X') for char in character]

def process_csv(file_path):
    """Reads the CSV file and converts each row of conjuncts into the desired output format."""
    results = []
    try:
        with open(file_path, encoding='utf-8') as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                if row:  # Ensuring the row is not empty
                    hex_codes = []
                    for character in row:
                        hex_codes.extend(unicode_hex_list(character))
                    #print(hex_codes) 
                    results.append(hex_codes)
    except FileNotFoundError:
        print(f"The file {file_path} does not exist.")
    except Exception as e:
        print(f"An error occurred: {e}")
    return results

def main():
    file_path = input("Enter the path to the CSV file containing the conjuncts: ").strip('"')
    hexa_representations = process_csv(file_path)
    
    if hexa_representations:
        print("Hexadecimal representations of conjuncts:")
        for hex_list in hexa_representations:
            formatted_hex_list = '",\n            "'.join(hex_list)
            print(f'        [\n            "{formatted_hex_list}"\n        ],')

if __name__ == "__main__":
    main()
