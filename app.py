import redis
from rq import Queue
from rq.job import Job
from flask import Flask, request, jsonify  

# Import your task module
from tasks import *

# Create Flask application
app = Flask(__name__)

# Create Redis connection and task queue
redis_conn = redis.Redis()
q = Queue(connection=redis_conn)

# Define route for starting a task
@app.route('/start-task', methods=['POST'])
def start_task():
    # Extract necessary info from request
    config_file = request.json.get('configFile')
    traits_file = request.json.get('traitsFile')
    js_file = request.json.get('createPromptFile')
    submitter_name = request.json.get('submitterName')
    experiment_details = request.json.get('experimentDetails')
    experiment_id = request.json.get('experimentId')
    sampleNum = request.json.get('noOfSamples')

    # Print the request body
    app.logger.info('Received request body:')
    app.logger.info(f'config_file: {config_file}')
    app.logger.info(f'traits_file: {traits_file}')
    app.logger.info(f'js_file: {js_file}')
    app.logger.info(f'sampleNum: {sampleNum}')

    # Enqueue the job
    job = q.enqueue(generate_images, config_file, traits_file, js_file, sampleNum)

    return jsonify({"job_id": job.get_id()}), 202

# Define route for getting job status
@app.route('/job/<job_id>', methods=['GET'])
def get_job_status(job_id):
    job = Job.fetch(job_id, connection=redis_conn)

    if job.is_finished:
        return jsonify({"status": "finished", "result": job.result}), 200
    elif job.is_failed:
        return jsonify({"status": "failed"}), 200
    else:
        return jsonify({"status": "in progress"}), 202


if __name__ == '__main__':
    app.run(debug=True, port=2323) 
