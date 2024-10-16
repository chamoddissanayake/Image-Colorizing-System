from flask import Flask, request, send_from_directory, jsonify
import numpy as np
import cv2
from cv2 import dnn
import os
import time
import uuid
from flask_cors import CORS

app = Flask(__name__)
CORS(app) 

# Folder to store uploaded images
UPLOAD_FOLDER = './uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/uploads/<path:filename>', methods=['GET'])
def serve_image_upload(filename):
    # Use send_from_directory to serve the image file
    return send_from_directory(UPLOAD_FOLDER, filename)

# Create the uploads folder if it doesn't exist
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)




# Folder to store uploaded images
OUTPUT_FOLDER = './output'
app.config['OUTPUT_FOLDER'] = OUTPUT_FOLDER

@app.route('/output/<path:filename>', methods=['GET'])
def serve_image_output(filename):
    # Use send_from_directory to serve the image file
    return send_from_directory(OUTPUT_FOLDER, filename, as_attachment=True)

# Create the output folder if it doesn't exist
if not os.path.exists(OUTPUT_FOLDER):
    os.makedirs(OUTPUT_FOLDER)
    
# Helper function to get file extension
def get_file_extension(filename):
    return os.path.splitext(filename)[1]
    



@app.route('/upload', methods=['POST'])
def upload_file():
    if 'image' not in request.files:
        return jsonify({"error": "No file part"}), 400

    file = request.files['image']

    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    # Get the file extension from the original file
    file_extension = get_file_extension(file.filename)
    
    # Refactor the file name to the current epoch time with original extension
    epoch_time = int(time.time())
    filename = f"{epoch_time}{file_extension}"
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(file_path)

    return jsonify({"image_path": file_path}), 200



# Model file paths
proto_file = 'colorization_deploy_v2.prototxt'
model_file = 'colorization_release_v2.caffemodel'
hull_pts = 'pts_in_hull.npy'

# Load the model and cluster centers
net = dnn.readNetFromCaffe(proto_file, model_file)
kernel = np.load(hull_pts)

# Add cluster centers to the model as 1x1 convolutions
class8 = net.getLayerId("class8_ab")
conv8 = net.getLayerId("conv8_313_rh")
pts = kernel.transpose().reshape(2, 313, 1, 1)
net.getLayer(class8).blobs = [pts.astype("float32")]
net.getLayer(conv8).blobs = [np.full([1, 313], 2.606, dtype="float32")]

def colorize_image(img_path):
    # Read and preprocess the image
    img = cv2.imread(img_path)
    scaled = img.astype("float32") / 255.0
    lab_img = cv2.cvtColor(scaled, cv2.COLOR_BGR2LAB)

    # Resize image for the network
    resized = cv2.resize(lab_img, (224, 224))
    L = cv2.split(resized)[0]
    L -= 50

    # Predict 'ab' channels
    net.setInput(cv2.dnn.blobFromImage(L))
    ab_channel = net.forward()[0, :, :, :].transpose((1, 2, 0))
    ab_channel = cv2.resize(ab_channel, (img.shape[1], img.shape[0]))

    # Take the L channel from the original image
    L = cv2.split(lab_img)[0]

    # Concatenate L with predicted ab channels
    colorized = np.concatenate([L[:, :, np.newaxis], ab_channel], axis=2)

    # Convert the LAB image back to BGR
    colorized = cv2.cvtColor(colorized, cv2.COLOR_LAB2BGR)
    colorized = np.clip(colorized, 0, 1)
    colorized = (255 * colorized).astype("uint8")

    return colorized

@app.route('/colorize', methods=['POST'])
def colorize():
    data = request.get_json()
    img_path = data.get('image_path')

    if not os.path.exists(img_path):
        return jsonify({"error": "Image path does not exist"}), 400

    # Colorize the image
    colorized_image = colorize_image(img_path)

    # Generate a unique filename for the output image
    output_filename = f"colorized_{uuid.uuid4().hex}.jpg"
    output_path = os.path.join("output", output_filename)

    # Save the colorized image
    os.makedirs("output", exist_ok=True)
    cv2.imwrite(output_path, colorized_image)

    # Return the path of the saved colorized image
    return jsonify({"colorized_image_path": output_path})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5009)
