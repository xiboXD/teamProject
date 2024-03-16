import redis
from rq import Queue
from rq.job import Job
from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin
from pymongo import MongoClient
import time
import os

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
@app.route('/experiments/start-task', methods=['POST'])
def start_task():
    # Extract necessary info from request
    config_file = request.json.get('configFile')
    traits_file = request.json.get('traitsFile')
    js_file = request.json.get('createPromptFile')
    submitter_name = request.json.get('submitterName')
    experiment_details = request.json.get('experimentDetails')
    experiment_id = request.json.get('experimentId')
    sampleNum = request.json.get('noOfSamples')
    submittedDate = int(time.time())

    # Print the request body
    app.logger.info('Received request body:')
    app.logger.info(f'config_file: {config_file}')
    app.logger.info(f'traits_file: {traits_file}')
    app.logger.info(f'js_file: {js_file}')
    app.logger.info(f'sampleNum: {sampleNum}')
    app.logger.info(f'submittedDate: {submittedDate}')

    # Enqueue the job
    job = q.enqueue(generate_images, config_file, traits_file, js_file, sampleNum, submitter_name, experiment_details, experiment_id, submittedDate)

    return jsonify({"job_id": job.get_id()}), 202

# Define route for getting job status
@app.route('/experiments/job/<job_id>', methods=['GET'])
def get_job_status(job_id):
    job = Job.fetch(job_id, connection=redis_conn)

    if job.is_finished:
        return jsonify({"status": "finished", "result": job.result}), 200
    elif job.is_failed:
        return jsonify({"status": "failed"}), 200
    else:
        return jsonify({"status": "in progress"}), 202

@app.route('/experiments/result/<experiment_id>', methods=['GET'])
def get_result_from_mongo(experiment_id):
    # Get the collection
    collection = db[f'experiment_{experiment_id}']
    
    # Query all data from the collection
    results = list(collection.find({}))
    
    # Convert ObjectId to string for JSON serialization
    for result in results:
        result['_id'] = str(result['_id'])
    
    numberOfResult = len(results)
    # Initialize formatted results list
    formatted_results = []
    
    result = collection.find_one(sort=[("_id", -1)])
    # Format each result
    if result:
        formatted_result = {
            "experimentId": experiment_id,
            "submitterName": result.get("submitter", ""),
            "noOfSamples": numberOfResult,
            "experimentDetails": result.get("description", ""),
            "status": result.get("status", ""),
            "submittedDate": result.get("create_date", ""),
            "traitsFile": result.get("traitsFile", ""),
            "configFile": result.get("configFile", ""),
            "createPromptFile": result.get("createPromptFile", ""),
            "result": []
        }
        
        for result in results:
            formatted_entry = {
                "_id": str(result["_id"]),
                "create_date": result.get("create_date", ""),
                "prompt": result.get("prompt", ""),
                "imageResult": result.get("imageResult", ""),
                "revised_prompt": result.get("revised_prompt", ""),
                "traits": result.get("traits", ""),
                "status": result.get("status", "")
            }
            formatted_result["result"].append(formatted_entry)
        
        formatted_results.append(formatted_result)  # Append formatted result to the list
    
    return jsonify(formatted_results), 200

@app.route('/experiments/get-list', methods=['GET'])
def get_list_from_mongo():
    # Get all collection names
    collection_names = db.list_collection_names()
    
    # Initialize result list
    results = []
    
    # Iterate over collection names
    for name in collection_names:
        if name.startswith('experiment_'):
            # Extract experiment ID
            experiment_id = name.split('_')[1]
            
            # Get the collection
            collection = db[name]
            
            # Get the first document (if exists)
            first_document = collection.find_one(sort=[("_id", -1)])
            
            if first_document:  # Check if document exists
                # Extract experiment details, submitter name, submitted date, and status
                experiment_details = first_document.get('description', '')
                submitter_name = first_document.get('submitter', '')
                submitted_date = first_document.get('create_date', '')
                status = first_document.get('status', '')
                
                # Create dictionary with experiment info
                experiment_info = {
                    'experimentId': experiment_id,
                    'experimentDetails': experiment_details,
                    'submitterName': submitter_name,
                    'submittedDate': submitted_date,
                    'status': status
                }
                
                # Add experiment info to results list
                results.append(experiment_info)
    
    return jsonify(results), 200

if __name__ == '__main__':
    app.run(debug=True, port=2323) 
