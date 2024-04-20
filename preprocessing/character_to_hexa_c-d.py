"""
This script is for manual inspection of classification. 
Note that the terminal isn't able to correctly represent via utf-8, 
thus the use of unicode code as output. 
"""
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import legacy.config_bangla as bc

# cons_eg = 'ঠ' # 'ভ' 
# character =  'প্ল্যা' #'ভ'

# d-net conjuncts: র্প প্র ত্র ক্র প্য প্যা
# 'ি' 
character = 'র'# 'রো' ভরুর

# Converting character to hexadecimal unicode code points
unicode_hex = [format(ord(char), '04X').upper() for char in character]
print("Hexadecimal Notation:", ' '.join(unicode_hex))

# Converting hexadecimal to decimal notation
unicode_decimal = [format(int(code, 16), '04d') for code in unicode_hex]
print("Decimal Notation (formatted):", ' '.join(unicode_decimal))

for uh in unicode_hex:
    if uh in bc.CONSONANTS:
        print(f"'{uh}' is a consonant (c-net).")

    elif uh in bc.IND_VOWELS:
        print(f"'{uh}' is an independent vowel (c-net).")

    elif uh in bc.DIGITS:
        print(f"'{uh}' is a digit (c-net).")

    elif uh in bc.DEP_VOWELS:
        print(f"'{uh}' is an dependent vowel (d-net).")

    elif uh in bc.VIRAMA:
        print(f"'{uh}' (virama) joiner (unassigned).")

    else:
        print(f"'{uh}' is not identified.")

print(f'Length for --> consonants: {len(bc.CONSONANTS)} | ind. vowels: {len(bc.IND_VOWELS)} | digits:  {len(bc.DIGITS)} ')

