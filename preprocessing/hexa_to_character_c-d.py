import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import config_bangla as bc

def hex_to_char(unicode_hex_list):
    """Convert hexadecimal unicode code points back to characters."""
    chars = [chr(int(uh, 16)) for uh in unicode_hex_list]
    return ''.join(chars)

# Example usage
unicode_hex_list = ['09B8', '09C8'] # ['09B0', '09CB']  # This is the Unicode hex for 'রো'
character = hex_to_char(unicode_hex_list)
print("Character representation:", character)

# Classifying each hex code in the list based on the config_bangla categories
for uh in unicode_hex_list:
    if uh in bc.CONSONANTS:
        print(f"'{uh}' is a consonant (c-net).")
    elif uh in bc.IND_VOWELS:
        print(f"'{uh}' is an independent vowel (c-net).")
    elif uh in bc.DIGITS:
        print(f"'{uh}' is a digit (c-net).")
    elif uh in bc.DEP_VOWELS:
        print(f"'{uh}' is a dependent vowel (d-net).")
    elif uh in bc.VIRAMA:
        print(f"'{uh}' (virama) is a joiner (unassigned).")
    else:
        print(f"'{uh}' is not identified.")

