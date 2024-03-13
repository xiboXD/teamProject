# tasks.py
import json
import execjs
import random
import pymongo
from utils.constants import *
from utils.mongo_new import *
from utils.generation import *


class Sampler:
    def __init__(self, traits):
        self.traits = traits

    def sample(self, n):
        output = []
        for i in range(n):
            trait_args = []
            for trait_type, values in self.traits.items():
                trait_args.append({'traitType': trait_type, 'value': random.choice(values)})
            output.append(trait_args)
        return output

def get_db(db_name):
    client = pymongo.MongoClient("mongodb://localhost:27017/")
    return client[db_name]


def get_collection(db_name):
    db = get_db(db_name)
    return db[COLLECTION_NAME]


def create_collection_if_not_exists(collection_name, db_name="experimentPlatform"):
    db = get_db(db_name)

    if collection_name not in db.list_collection_names():
        db.create_collection(collection_name)

    # Access the collection
    coll = db[collection_name]

    # Step 4: Create Index
    # This creates an index on the 'prompt' field
    coll.create_index([('prompt', 1)])  # 1 for ascending order

def get_samples(traits_file, sampleNum):
    sampler = Sampler(traits_file)
    samples = sampler.sample(sampleNum)
    return samples

def generate_images(config_file, traits_file, js_file, sampleNum):
    # Your long-running task logic here
    samples = get_samples(traits_file, sampleNum)
    with open(js_file, 'r') as js_file:
        js_code = js_file.read()
        print(js_code)

    # Load config and trait arguments from JSON files
    with open(config_file, 'r') as f:
        config = json.load(f)

    # Create an ExecJS context
    ctx = execjs.compile(js_code)
    prompts = []
    for sample in samples:
        prompt = ctx.call('createPrompt', config, sample)
        prompts.append(prompt)
    
    base64images = []
    for prompt in prompts:
        base64image = generate_one_sample(prompt)
        base64images.append(base64image)
    return base64images


    
