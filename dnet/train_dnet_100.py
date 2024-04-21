from ultralytics import YOLO
import time
import json
import os
import yaml

class TrainingTimer:
    def __init__(self, project_path, name):
        self.start_time = time.time()
        self.total_training_time = 0
        self.project_path = project_path
        self.time_file = os.path.join(project_path, name, 'training_time.json')

    def load_previous_time(self):
        if os.path.exists(self.time_file):
            with open(self.time_file, 'r') as f:
                self.total_training_time = json.load(f)
            print(f"Previous training time: {self.total_training_time} seconds")

    def update_training_time(self):
        end_time = time.time()
        self.total_training_time += end_time - self.start_time
        print(f"Total training time: {self.total_training_time} seconds")
        with open(self.time_file, 'w') as f:
            json.dump(self.total_training_time, f)
        self.start_time = time.time()

def update_yaml_path(yaml_file, path, train, val, test):
    with open(yaml_file, 'r') as file:
        yaml_content = yaml.safe_load(file)
    
    yaml_content['path'] = path
    yaml_content['train'] = train
    yaml_content['val'] = val
    yaml_content['test'] = test
    
    with open(yaml_file, 'w') as file:
        yaml.dump(yaml_content, file, default_flow_style=False, sort_keys=False)
    
    print(f"Updated the 'path' in {yaml_file}")

def train_eval_model(data, yolo_weights, project, name, epochs, batch, patience, device, exist_ok,
                     hsv_h, hsv_s, hsv_v, degrees, translate, scale, shear, perspective, flipud, fliplr, 
                     bgr, mosaic, mixup, copy_paste, auto_augment, erasing):
    model = YOLO(yolo_weights) #YOLO(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'pretrained', f'{yolo_weights}'))
    timer = TrainingTimer(project, name)
    timer.load_previous_time()

    result = model.train(
        data=data,
        project=project,
        name=name,
        epochs=epochs,
        batch=batch,
        patience=patience,
        device=device,
        exist_ok=exist_ok,
        hsv_h=hsv_h,
        hsv_s=hsv_s,
        hsv_v=hsv_v,
        degrees=degrees,
        translate=translate,
        scale=scale,
        shear=shear,
        perspective=perspective,
        flipud=flipud,
        fliplr=fliplr,
        bgr=bgr,
        mosaic=mosaic,
        mixup=mixup,
        copy_paste=copy_paste,
        auto_augment=auto_augment,
        erasing=erasing,
    )

    # Export the model to ONNX format
    success = model.export(format='onnx')
    timer.update_training_time()
    #return result

def main():
    ### INPUT #####################################################################################################
    # Model parameters
    data_yaml = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'dnet_dataset_80-10-10-page_100', 'd_data.yaml'))
    project=os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'dnet_dataset_80-10-10-page_100','yolov8x'))#'./yolov8m'
    name='20240421_T1320_100'
    yolo_weights =  os.path.join(os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')), 'yolov8x.pt')
    #os.path.join(os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')), 'pretrained', 'yolov8m.pt')
    epochs=250
    batch=16
    patience=15
    device=0
    exist_ok=False
    # Augmentation
    hsv_h = 0.015
    hsv_s = 0.7
    hsv_v = 0.4
    degrees = 5.0
    translate = 0.1
    scale = 0.5
    shear = 5.0
    perspective = 0.0
    flipud = 0.0
    fliplr = 0.0
    bgr = 0.0
    mosaic = 1.0
    mixup = 0.0
    copy_paste = 0.0
    auto_augment = 'randaugment'
    erasing = 0.4

    # Yaml path 
    dataset_path = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'data', 'dataset_80-10-10-page_100/d_data'))
    train_path = os.path.abspath(os.path.join(dataset_path, 'train/images'))
    val_path = os.path.abspath(os.path.join(dataset_path, 'validation/images'))
    test_path = os.path.abspath(os.path.join(dataset_path, 'test/images'))
    
    ### RUN #######################################################################################################
        # Populate x_data.yaml
    update_yaml_path(data_yaml, dataset_path, train_path, val_path, test_path)

    # Train & Evaluatin 
    train_eval_model(data=data_yaml,
                     yolo_weights= yolo_weights,     # pre-trained weights or untrained weights
                     project=project,                # project (output)
                     name=name,
                     epochs=epochs,                  
                     batch=batch,                    
                     patience=patience,              # number of epochs with no improvement
                     device=device,                   # gpu to use
                     exist_ok=exist_ok,
                     hsv_h=hsv_h,
                     hsv_s=hsv_s,
                     hsv_v=hsv_v,
                     degrees=degrees,
                     translate=translate,
                     scale=scale,
                     shear=shear,
                     perspective=perspective,
                     flipud=flipud,
                     fliplr=fliplr,
                     bgr=bgr,
                     mosaic=mosaic,
                     mixup=mixup,
                     copy_paste=copy_paste,
                     auto_augment=auto_augment,
                     erasing=erasing
                    )

if __name__ == "__main__":
    main()