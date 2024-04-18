"""
Create the yaml files for yolo based on the 'bangla_yolo_class_mapping_c_data_hex.csv'. 
"""
import pandas as pd
import yaml
import os

def create_data_yaml():
    csv_path = input("Enter the path to your 'bangla_yolo_class_mapping_hex.csv' file: ").strip('"')
    csv_path_out = input("Enter the output path for the x_data.yaml' file: ").strip('"')
    print(csv_path_out)

    base_name = os.path.basename(csv_path).rsplit('_')
    base_name = "_".join(base_name[4:6])
    yaml_file_name = f"{base_name}.yaml"
    yaml_path = os.path.join(csv_path_out, yaml_file_name)
    print(yaml_path)
    df = pd.read_csv(csv_path, encoding='utf-8')
    names = {row['yolo_class']: row['unicode_hex'] for index, row in df.iterrows()}

    data_yaml_content = {
        'path': f'../datasets/{base_name}',
        'train': '../datasets/train/images',
        'val': '../datasets/validation/images',
        'test': '../datasets/test/images',
        'names': names,
        'nc': len(names), 
        
    }


    with open(yaml_path, 'w') as file:
        yaml.dump(data_yaml_content, file, default_flow_style=False, sort_keys=False)

    print(f"Data YAML file saved to {yaml_path}")

create_data_yaml()
