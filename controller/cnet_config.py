import os 

######### Change the below to reflect the settings for the current train instance: #######

NETWORK = 'cnet' # 'cnet' or 'dnet'
MODEL = 'yolo8l' # Check that the correct weights (.pt) exists in the 'pretrained' folder. 
DATASET = 'xxx.yaml' # 
NUM_CLASSES = '331'
OBJ_PER_CLASS = '100'
EPOCHS = '500' 
BATCH = '32'

##########################################################################################