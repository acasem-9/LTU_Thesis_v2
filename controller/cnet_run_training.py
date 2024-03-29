import os
import sys 
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import subprocess
from datetime import datetime
import config_local as config_local
import config_networks as config_networks

def time_now():
    return datetime.now().strftime('%Y-%m-%d %H:%M:%S')

def main(network, model, dataset, num_classes, obj_per_class, epochs, batch): 
    
    output_folder_name = f'{network}_{model}_c{num_classes}_o{obj_per_class}_e{epochs}_b{batch}'
    train_script_path = os.path.join(config_local.CNET, f'train_{network}.py')
    output_folder_path = os.path.join(config_local.CNET, 'cnet_models', f'{output_folder_name}')

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

    main(config_networks.NETWORK, config_networks.MODEL, config_networks.DATASET, config_networks.NUM_CLASSES, config_networks.OBJ_PER_CLASS, config_networks.EPOCHS, config_networks.BATCH)


