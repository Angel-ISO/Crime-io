from pymongo import MongoClient

MONGO_URI = "mongodb+srv://zaid_2003:zaid_1907@cluster1.03jozqw.mongodb.net/"

client = MongoClient(MONGO_URI)


DB_NAME = "Crime" 
COLLECTION_NAME = "Train"

client = MongoClient(MONGO_URI)
db = client[DB_NAME]
collection = db[COLLECTION_NAME]

conn = collection
