import os
import pandas as pd
from PIL import Image
import re
import concurrent.futures

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


def process_single_file(txt_file, coordinates_path, labels_path, images_path, pages_path):
    padding = 10
    page_id = os.path.splitext(txt_file)[0]
    df = pd.read_csv(os.path.join(coordinates_path, txt_file), sep=' ', names=['Line', 'Word', 'Char', 'Character', '-', 'Coordinates'], encoding='utf-8')

    df['x1'] = df['Coordinates'].apply(lambda x: int(x.split(',')[0]))
    df['y1'] = df['Coordinates'].apply(lambda x: int(x.split(',')[1]))
    df['x2'] = df['Coordinates'].apply(lambda x: int(x.split(',')[0]) + int(x.split(',')[2]))
    df['y2'] = df['Coordinates'].apply(lambda x: int(x.split(',')[1]) + int(x.split(',')[3]))
    
    for word, group in df.groupby('Word'):
        min_x = group['x1'].min() - padding
        max_x = group['x2'].max() + padding
        min_y = group['y1'].min() - padding
        max_y = group['y2'].max() + padding
        
        # Crop image based on calculated coordinates
        image_path = os.path.join(pages_path, f"{page_id}.tif")
        with Image.open(image_path) as img:
            cropped_img = img.crop((min_x, min_y, max_x, max_y))
            cropped_img.save(os.path.join(images_path, f"{page_id}_{word}.tif"))
        
        # Adjust and save coordinates for each cropped image
        adjusted_coords = group.copy()
        adjusted_coords['x1'] -= min_x
        adjusted_coords['y1'] -= min_y
        adjusted_coords['x2'] -= min_x
        adjusted_coords['y2'] -= min_y
        with open(os.path.join(labels_path, f"{page_id}_{word}.txt"), 'w', encoding='utf-8') as file:
            for _, row in adjusted_coords.iterrows():
                line = f"{row['Line']} {row['Word']} {row['Char']} {row['Character']} - {row['x1']},{row['y1']},{row['x2'] - row['x1']},{row['y2'] - row['y1']}\n"
                file.write(line)

def main():
    output_path = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'data/raw/word_separated'))
    pages_path, coordinates_path = prompt_for_paths()
    labels_path, images_path = create_output_structure(output_path)

    txt_files = [f for f in os.listdir(coordinates_path) if f.endswith('.txt')]
    args = [(f, coordinates_path, labels_path, images_path, pages_path) for f in txt_files]
    
    print('running ... ')

    with concurrent.futures.ProcessPoolExecutor() as executor:
        futures = [executor.submit(process_single_file, *arg) for arg in args]
        for future in concurrent.futures.as_completed(futures):
            try:
                result = future.result()
            except Exception as e:
                print(f"Exception occurred: {e}")

if __name__ == "__main__":
    main()
