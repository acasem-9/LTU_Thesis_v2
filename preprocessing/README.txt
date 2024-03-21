Step 1: Choose between pages_to_characters.py or pages_to_words.py for the initial cropping and annotation generation based on the project's needs. 
This step prepares the images and annotations for further processing.

Step 2: Run create_bangla_yolo_mapping.py to generate a mapping between Bangla characters or words and YOLO class IDs. 
This step is crucial for linking the dataset's annotations to the format required by YOLO models.

Step 3: Execute convert_annotations_to_yolo.py to transform your annotations into the YOLO format, 
making the dataset ready for use with YOLO object detection models.

Step 4: Run assign_character_class.py 