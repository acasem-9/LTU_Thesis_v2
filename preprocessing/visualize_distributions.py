
import os
import pandas as pd
import matplotlib.pyplot as plt

def aggregate_yolo_classes(data_folder):
    """Aggregate YOLO class occurrences from label files."""
    data_structure = {'train': [], 'validation': [], 'test': []}
    
    for phase in ['train', 'validation', 'test']:
        phase_folder = os.path.join(data_folder, phase, 'labels')
        for label_file in os.listdir(phase_folder):
            with open(os.path.join(phase_folder, label_file), 'r') as file:
                classes = [int(line.split()[0]) for line in file.readlines()]
                data_structure[phase].extend(classes)
    
    return data_structure

def plot_class_distributions(c_data, d_data, class_names):
    """Plot YOLO class distributions for c_data and d_data."""
    fig, axs = plt.subplots(2, 1, figsize=(10, 8), sharex=True)
    
    # Assuming 'class_names' is a list of class names ordered by YOLO class ID
    x = range(len(class_names))
    
    for idx, (data, title) in enumerate(zip([c_data, d_data], ['c_data', 'd_data'])):
        df = pd.DataFrame(data)
        df_counts = df.apply(pd.Series.value_counts).fillna(0)
        df_counts = df_counts.reindex(index=x, fill_value=0)  # Ensure all classes are represented
        
        df_counts.plot(kind='bar', stacked=True, ax=axs[idx], alpha=0.5, title=title)
    
    axs[1].set_xticks(x)
    axs[1].set_xticklabels(class_names, rotation=45, ha='right')
    
    plt.tight_layout()
    plt.show()

# Paths to your data folders
c_data_folder = 'dataset_folder/c_data'
d_data_folder = 'dataset_folder/d_data'

# Aggregate YOLO class data
c_data_classes = aggregate_yolo_classes(c_data_folder)
d_data_classes = aggregate_yolo_classes(d_data_folder)

# Define your class names based on YOLO class IDs
class_names = ['Class 1', 'Class 2', 'Class 3']  # Update this list based on your actual class names

# Plotting
plot_class_distributions(c_data_classes, d_data_classes, class_names)
