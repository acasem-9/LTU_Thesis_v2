import os
import glob
from pathlib import Path
import numpy as np
import cv2
#from yolov8 import Yolov8
from ultralytics import YOLO


# Function to load the model
def load_model(weights_path):
    model = YOLO(weights=weights_path, device='cuda')
    return model

# Process images and save detections
def process_images(model, images_path, detections_path):
    image_files = glob.glob(os.path.join(images_path, '*.tif'))
    for image_path in image_files:
        img = cv2.imread(image_path)  # Load image with OpenCV
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)  # Convert to RGB
        results = model.predict(img_rgb, conf_thres=0.7)  # Apply model
        # Save results to corresponding text file in detections folder
        fname = os.path.splitext(os.path.basename(image_path))[0] + '.txt'
        file_path = os.path.join(detections_path, fname)
        with open(file_path, 'w') as f:
            for *xyxy, conf, cls in results.xyxy[0]:
                # Convert from tensor to numpy array and then to list
                box_data = xyxy.cpu().numpy().tolist()
                line = f"{int(cls)} {' '.join(f'{x:.2f}' for x in box_data)} {conf:.2f}\n"
                f.write(line)

def main():
    # User input for paths
    project_folder = input("Enter the path to the project folder (e.g., '20240405_T2112'): ").strip('"')
    test_data_folder = input("Enter the path to the test data folder (e.g., 'c_data/test'): ").strip('"')

    # Prepare directories
    base_path = Path(project_folder)
    test_output_folder = base_path.parent / (base_path.name + '_test')
    detections_folder = test_output_folder / 'detections'
    weights_path = base_path / 'weights' / 'best.pt'
    
    # Create directories if they do not exist
    test_output_folder.mkdir(parents=True, exist_ok=True)
    detections_folder.mkdir(parents=True, exist_ok=True)
    
    # Load model
    model = load_model(weights_path)
    
    # Path to images
    images_path = Path(test_data_folder) / 'images'
    
    # Process images
    process_images(model, images_path, detections_folder)

    print(f"All images processed. Detections are saved in {detections_folder}.")

if __name__ == "__main__":
    main()
