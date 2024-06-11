from pymongo import MongoClient

# Connect to MongoDB
client = MongoClient('mongodb://localhost:27017/')
db = client['DBL']
collection = db['cleaned_v3']

# Remove duplicates using MongoDB aggregation pipeline
pipeline = [
    {"$group": {"_id": "$id", "count": {"$sum": 1}}},
    {"$match": {"count": {"$gt": 1}}}
]

print("gecti")
duplicates = list(collection.aggregate(pipeline))
print("gecti")

with open("duplicates_on_cleaned.txt", 'w') as file:
    for doc in duplicates:
        duplicate_ids = doc["_id"]
        #print(duplicate_ids)
        file.write(f"{duplicate_ids}\n")
