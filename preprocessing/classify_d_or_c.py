import bangla_config as bc
import pandas as pd

cons_eg = 'ঠ' # 'ভ' 

character =  'প্ল্যা' #'ভ'


unicode_code = [ord(char) for char in character]

print(unicode_code) 
      
for uc in unicode_code: 
    if uc in bc.BANGLA_CONSONANTS:
        print(f"'{uc}' is a consonant (c)")

    elif uc in bc.BANGLA_IND_VOWELS:
        print(f"'{uc}' is an independent vowel (c)")

    elif uc in bc.BANGLA_DIGITS:
        print(f"'{uc}' is a digit (c)")

    else:
        print(f"'{uc}' is a 'diacritic' (d)")