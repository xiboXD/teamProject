import redis
from rq import Queue
from rq.job import Job
from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin
from pymongo import MongoClient
import time
import os
from utils.generation import *
import os
from datetime import datetime
from flask import request, jsonify, current_app as app
from utils.generation import generate_one_sample
import base64

# Import your task module
from tasks import *

mongo_url = os.environ.get("MONGO_URL", "mongodb://localhost:27017/")
redis_host = os.environ.get("REDIS_HOST", "localhost")
redis_port = int(os.environ.get("REDIS_PORT", "6379"))

# Create Flask application
app = Flask(__name__)
CORS(app)
# Create Redis connection and task queue
redis_conn = redis.Redis(host=redis_host, port=redis_port)
q = Queue(connection=redis_conn)

client = MongoClient(mongo_url)
db = client['experimentPlatform']

# Define route for starting a task


@app.route('/image/create', methods=['POST'])
def start_task():
    prompt = request.json.get('prompt')

    # Print the request body
    app.logger.info('Received request body:')
    app.logger.info(f'prompt: {prompt}')

    # Enqueue the job
    base64Image, _ = generate_one_sample(prompt)

    # Save image to images folder with timestamp as filename
    timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    image_filename = f"{timestamp}.png"
    image_path = os.path.join(app.root_path, 'images', image_filename)
    with open(image_path, 'wb') as f:
        f.write(base64.b64decode(base64Image))  # Convert Base64 string to bytes and write to file

    return jsonify({"image": base64Image}), 200

@app.route('/experiments/get-images', methods=['GET'])
def get_images_base64_from_folder():
    # Get list of filenames in the images folder
    images_folder = os.path.join(app.root_path, 'images')
    image_files = os.listdir(images_folder)
    
    # Filter out any non-image files if necessary
    image_files = [filename for filename in image_files if filename.lower().endswith(('.png', '.jpg', '.jpeg'))]
    
    # Read each image file, encode it as base64, and store in a list
    image_base64_list = []
    for filename in image_files:
        image_path = os.path.join(images_folder, filename)
        with open(image_path, 'rb') as f:
            image_data = f.read()
            image_base64 = base64.b64encode(image_data).decode('utf-8')
            image_base64_list.append(image_base64)
    
    return jsonify(image_base64_list), 200

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5050) 
