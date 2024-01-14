import os
import subprocess
from datetime import datetime
import config_path as config_path
import cnet_config as cnet_config

def time_now():
    return datetime.now().strftime('%Y-%m-%d %H:%M:%S')

def main(network, model, dataset, num_classes, obj_per_class, epochs, batch): 
    
    output_folder_name = f'{network}_{model}_c{num_classes}_o{obj_per_class}_e{epochs}_b{batch}'
    train_script_path = os.path.join(config_path.CNET, f'train_{network}.py')
    output_folder_path = os.path.join(config_path.CNET, 'cnet_models', f'{output_folder_name}')

    if not os.path.exists(output_folder_path):
        os.makedirs(output_folder_path)
        print(f'Started processing: {output_folder_name} at {time_now()}')
        subprocess.run(['python', train_script_path, '--output', output_folder_path, '--network', network, 
                        '--model', model, '--dataset', dataset, '--num_classes', num_classes, '--obj_per_class', obj_per_class,
                         '--epochs', epochs, '--batch', batch ])  
        print(f'Finished processing: {output_folder_name} at {time_now()}')

    else :
        print(f"Aborted! --> Move (or delete) folder at: {output_folder_path} to allow new run.")
   
if __name__ == "__main__":

    main(cnet_config.NETWORK, cnet_config.MODEL, cnet_config.DATASET, cnet_config.NUM_CLASSES, cnet_config.OBJ_PER_CLASS, cnet_config.EPOCHS, cnet_config.BATCH)


