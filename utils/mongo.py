import pymongo

class DataEntry:
    def __init__(self, description, submitter, create_date, status, imageResults):
        self.description = description
        self.submitter = submitter
        self.create_date = create_date
        self.status = status
        self.result_link = imageResults

def get_db():
    client = pymongo.MongoClient("mongodb://localhost:27017/")
    db = client["experimentPlatform"]
    return db

def get_collection(db, collection_name):
    _collection = db[collection_name]
    return _collection

def insert(collection, data):
    res = collection.insert_one(data)
    print(res)
    _id = res.inserted_id
    print(_id)

def query(collection):
    res = []
    for x in collection.find({}, {"submitter": "xibo"}):
        res.append(x)
    print(res)