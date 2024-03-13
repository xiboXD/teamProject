import pymongo

class DataEntry:
    def __init__(self, id, description, submitter, create_date, status, result_link, comments):
        self.id = id
        self.description = description
        self.submitter = submitter
        self.create_date = create_date
        self.status = status
        self.result_link = result_link
        self.comments = comments

def get_db():
    client = pymongo.MongoClient("mongodb://localhost:27017/")
    db = client["experimentPlatform"]
    return db

def get_collection(db, collection_name):
    _collection = db[collection_name]
    return _collection

def insert(collection, data):
    res = collection.insert_one(data)
    _id = res.inserted_id
    print(_id)

def query(collection):
    res = []
    for x in collection.find({}, {"submitter": "aaaa"}):
        res.append(x)
    print(res)