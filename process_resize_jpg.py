import pydicom
import numpy as np
import cv2
import os
from pathlib import Path
from pydicom.pixel_data_handlers.util import apply_voi_lut

RESIZE_TO = (512, 512)

# specify the output directory
OUTPUT_DIR = 'resized_images' 

# specify the input directory containing the DICOM files
input_dir = 'sample_files'

def dicom_file_to_array(path):
    dicom = pydicom.dcmread(path)
    data = dicom.pixel_array
    data = apply_voi_lut(dicom.pixel_array, dicom)

    data = (data - data.min()) / (data.max() - data.min())

    if dicom.PhotometricInterpretation == "MONOCHROME1":
        data = 1 - data

    data = cv2.resize(data, RESIZE_TO)
    data = (data * 255).astype(np.uint8)

    # get the filename without extension
    filename = os.path.basename(path).split('.')[0]

    # create the output folder if it doesn't exist
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)

    # save the resized image to the output folder
    output_path = os.path.join(OUTPUT_DIR, f'{filename}.jpg')
    cv2.imwrite(output_path, data)

def process_dicom_files(root_dir):
    for root, dirs, files in os.walk(root_dir):
        for file in files:
            if file.endswith('.dcm'):
                file_path = os.path.join(root, file)
                dicom_file_to_array(file_path)

# process each DICOM file in the input directory
process_dicom_files(input_dir)