import pymongo
import json

# MongoDB connection information
mongo_uri = "mongodb://logcaptain:pascalloljungle23@192.168.1.30:27017/"
database_name = "ForwardDB"
collection_name = "ForwardCollection"

# JSON file path
json_file_path = "C:\\Users\\bob\\Desktop\\report.json" 

# Connect to MongoDB
client = pymongo.MongoClient(mongo_uri)
db = client[database_name]
collection = db[collection_name]

# Read the JSON file
with open(json_file_path, 'r') as json_file:
    data = json.load(json_file)

# Insert data into MongoDB
collection.insert_one(data)

# Close the MongoDB connection
client.close()

print("Data imported successfully.")
