# Flask: Imports the Flask class, which is used to create the Flask application.
# request: Used to access incoming request data (like files and form data).
# jsonify: Helper function to convert Python dictionaries into JSON responses
from flask import Flask, request, jsonify
# Imports the os module, which provides a way of using operating system dependent functionality like file paths
import os
# Preprocessing service
import Preprocessing as process
# API Documentation
from flasgger import Swagger

# Creates an instance of the Flask application
app = Flask(__name__)
# Make Swagger version
swagger = Swagger(app)

# Configer swagger
app.config['SWAGGER'] = {
    'title': 'Microservice',
    'uiversion': 1
}

# Set the directory to store FITS files
fits_files_directory = 'FITS_Files'
# Ensure the directory exists
os.makedirs(fits_files_directory, exist_ok=True)

# Handle HTTP POST requests that are sent to the /upload URL


@app.route('/upload', methods=['POST'])
def upload_file():
    """
    File Upload API
    ---
    tags:
      - File Operations
    consumes:
      - multipart/form-data
    parameters:
      - in: formData
        name: file
        type: file
        required: true
        description: The file to upload.
    responses:
      200:
        description: File successfully uploaded
      400:
        description: Error message if the file was not uploaded correctly
    """

    # Retrieves the file from the form data sent with the request. The client should include a file with the key 'file
    file = request.files['file']
    # Extracts the filename of the uploaded file
    filename = file.filename
    # Constructs the file path where the file will be saved
    filepath = os.path.join(fits_files_directory, filename)
    # Saves the uploaded file to the specified location on the server
    file.save(filepath)

    # Return message indicating result of preprocessing
    return process.process_file(filepath)


# Run main app
if __name__ == '__main__':
    app.run(debug=True)
