import fitsio
import os
import numpy as np
from flask import jsonify

def process_file(file_path):
    try:
        file_name = os.path.basename(file_path)
        subtract_background(file_path)
        
        return jsonify({'message': 'File uploaded and Processed successfully', 'filename': file_name})

    except FileNotFoundError:
        print("File not found")
    except Exception as e:
        print("An error occurred:", e)

def subtract_background(file_path):

    file_name = os.path.basename(file_path)

    # Read the image data
    with fitsio.FITS(file_path) as fits:
        image_data = fits[0].read()

    # Estimate the background
    # This is a simple median estimate, you might need a more sophisticated approach depending on your data
    background = np.median(image_data)

    # Subtract the background
    image_data_subtracted = image_data - background

    # Write the new FITS file with the background subtracted
    fitsio.write( os.path.join("SubtractBackground", file_name), image_data_subtracted, clobber=True)