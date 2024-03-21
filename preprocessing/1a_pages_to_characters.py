import os
import pandas as pd
from PIL import Image
import re

def remove_quotes(path):
    return re.sub(r'^[\'\"]|[\'\"]$', '', path)

def prompt_for_paths():
    pages_path = remove_quotes(input("Enter the path to the 'pages' (tif) folder: "))
    coordinates_path = remove_quotes(input("Enter the path to the 'pages_character_coordinates' (txt) folder: "))
    return pages_path, coordinates_path  

def create_output_structure(output_path):
    labels_path = os.path.join(output_path, 'labels')
    images_path = os.path.join(output_path, 'images')
    os.makedirs(labels_path, exist_ok=True)
    os.makedirs(images_path, exist_ok=True)
    return labels_path, images_path

def process_text_files(coordinates_path, labels_path, images_path, pages_path):
    padding = 0 # Padding of character image
    for txt_file in os.listdir(coordinates_path):
        if txt_file.endswith('.txt'):
            page_id = os.path.splitext(txt_file)[0]
            df = pd.read_csv(os.path.join(coordinates_path, txt_file), sep=' ', names=['Line', 'Word', 'Char', 'Character', '-', 'Coordinates'])
            df['x1'] = df['Coordinates'].apply(lambda x: int(x.split(',')[0]))
            df['y1'] = df['Coordinates'].apply(lambda x: int(x.split(',')[1]))
            df['x2'] = df['Coordinates'].apply(lambda x: int(x.split(',')[0]) + int(x.split(',')[2]))
            df['y2'] = df['Coordinates'].apply(lambda x: int(x.split(',')[1]) + int(x.split(',')[3]))
            
            # Process each character
            for _, row in df.iterrows():
                char_id = f"{row['Word']}_{row['Char']}"
                crop_and_adjust_character(page_id, char_id, row, pages_path, images_path, labels_path, padding)

def crop_and_adjust_character(page_id, char_id, row, pages_path, images_path, labels_path, padding):

    min_x, max_x = row['x1'] - padding, row['x2'] + padding
    min_y, max_y = row['y1'] - padding, row['y2'] + padding
    image_path = os.path.join(pages_path, f"{page_id}.tif")
    with Image.open(image_path) as img:
        cropped_img = img.crop((min_x, min_y, max_x, max_y))
        cropped_img.save(os.path.join(images_path, f"{page_id}_{char_id}.tif"))
    
    adjusted_x1, adjusted_y1 = 0, 0 
    adjusted_x2, adjusted_y2 = (max_x - min_x) - 2*padding, (max_y - min_y) - 2*padding
    with open(os.path.join(labels_path, f"{page_id}_{char_id}.txt"), 'w', encoding='utf-8') as file:
        line = f"{row['Line']} {row['Word']} {row['Char']} {row['Character']} - {adjusted_x1},{adjusted_y1},{adjusted_x2},{adjusted_y2}\n"
        file.write(line)

def main():
    output_path = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'data/temp_characters'))
    pages_path, coordinates_path = prompt_for_paths()
    labels_path, images_path = create_output_structure(output_path)
    process_text_files(coordinates_path, labels_path, images_path, pages_path)

if __name__ == "__main__":
    main()
