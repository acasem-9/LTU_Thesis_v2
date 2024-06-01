"""
This script performs object detection on a set of images. It reads images in TIFF format,
applies the model to detect objects, and saves the detection results as text files. Optionally, 
if specified by the user, the script also saves images annotated with bounding boxes that 
represent detected objects.
"""

import os
import glob
from pathlib import Path
import cv2
from ultralytics import YOLO
from PIL import Image

def load_model(weights_path):
    model = YOLO(weights_path)
    model.to('cuda')
    return model

# Process images and save detections
def process_images(model, images_path, detection_labels_path, detection_images_path, save_image, conf_level):
    image_files = glob.glob(os.path.join(images_path, '*.tif'))
    for image_path in image_files:
        img = cv2.imread(image_path)  # Load image with OpenCV
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)  # Convert to RGB
        results = model.predict(source=img_rgb, conf=conf_level, device='0')  # Apply model

        # Save results to corresponding text file in (and tif) detections folder
        txt_fname = os.path.splitext(os.path.basename(image_path))[0] + '.txt'
        img_fname = os.path.splitext(os.path.basename(image_path))[0] +'.tif'
        print(f'img_fname: {img_fname}')
        txt_file_path = os.path.join(detection_labels_path, txt_fname)
        tif_file_path = os.path.join(detection_images_path, img_fname)
        with open(txt_file_path, 'w') as f:
            for r in results:
                box_data = r.boxes.data
                print(box_data)
                for *b, conf, cls in box_data:
                    line = f'{int(cls)} {b[0]} {b[1]} {b[2]} {b[3]} {conf}\n'
                    f.write(line)
                if save_image == 'yes':
                    im_array = r.plot(conf=False)  # plot a BGR numpy array of predictions
                    im = Image.fromarray(im_array[..., ::-1])  # RGB PIL image
                    im.save(tif_file_path)


def main():
    # User input for paths
    project_folder = input("Enter the path to the project folder for c-net or d-net (e.g., '20240405_T2112'): ").strip('"')
    test_data_folder = input("Enter the path to the test data folder (e.g., 'c_data/test'): ").strip('"')
    save_images = input("Do you want to create images with bounding boxes plotted? (yes/no): ").lower().strip()
    conf_level = float(input("Enter the confidence level for the detections to keep (e.g., 0.4): ").strip('"'))

    # Prepare directories
    base_path = Path(project_folder)
    test_output_folder = base_path.parent / (base_path.name + '_test' + f'_conf={conf_level}')
    detection_folder = test_output_folder / 'detections'
    detection_labels_folder = detection_folder / 'labels'
    detection_images_folder = detection_folder / 'images'

    weights_path = base_path / 'weights' / 'best.pt'

    # Create directories if they do not exist
    test_output_folder.mkdir(parents=True, exist_ok=True)
    detection_folder.mkdir(parents=True, exist_ok=True)
    detection_labels_folder.mkdir(parents=True, exist_ok=True)
    if save_images == 'yes': detection_images_folder.mkdir(parents=True, exist_ok=True)

    # Load model
    model = load_model(weights_path)

    # Path to images
    images_path = Path(test_data_folder) / 'images'

    # Process images
    process_images(model, images_path, detection_labels_folder,detection_images_folder, save_images, conf_level)

    print(f"All images processed. Detections are saved in {detection_labels_folder}.")

if __name__ == "__main__":
    main()
