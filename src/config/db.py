from pymongo import MongoClient

MONGO_URI = ""

client = MongoClient(MONGO_URI)


DB_NAME = "Crime" 
COLLECTION_NAME = "Train"

client = MongoClient(MONGO_URI)
db = client[DB_NAME]
collection = db[COLLECTION_NAME]

conn = collection
