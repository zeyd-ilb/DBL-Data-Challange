from pymongo import MongoClient, ASCENDING
from pymongo import DeleteOne
import logging

# Configure logging settings
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s', filename='remove_duplicates_2.log', filemode='w')

# Read the duplicate IDs from the text file
def read_duplicate_ids(file_path):
    with open(file_path, 'r') as file:
        return [line.strip() for line in file]

# Connect to MongoDB
client = MongoClient('mongodb://localhost:27017/')
db = client['DBL']
collection = db['cleaned_v3']

# Ensure index on 'id' field for faster querying
collection.create_index([("id", ASCENDING)])

# Path to the file containing duplicate IDs
duplicate_ids_file = 'duplicates_on_cleaned.txt'

# Get the list of duplicate IDs
duplicate_ids = read_duplicate_ids(duplicate_ids_file)

# Batch size for processing duplicate IDs
batch_size = 100

# Process duplicates in batches
for i in range(0, len(duplicate_ids), batch_size):
    batch_ids = duplicate_ids[i:i+batch_size]

    # Query for documents in the current batch of duplicate IDs
    pipeline = [
        {"$match": {"id": {"$in": [int(dup_id) for dup_id in batch_ids]}}},
        {"$project": {"id": 1, "_id": 1}},
        {"$group": {"_id": "$id", "docs": {"$push": {"_id": "$_id"}}}},
        {"$match": {"docs.1": {"$exists": True}}}  # Only keep groups with more than one document
    ]

    groups = list(collection.aggregate(pipeline))

    # Prepare bulk operations
    bulk_operations = []
    for group in groups:
        docs_to_delete = group["docs"][1:]  # Keeping the first document and deleting the rest

        for doc in docs_to_delete:
            logging.info(f"This object_id gonna be deleted {doc['_id']} for this id : {group['_id']}")
            bulk_operations.append(DeleteOne({"_id": doc["_id"]}))

    # Execute bulk operations
    if bulk_operations:
        collection.bulk_write(bulk_operations)

print("Duplicate documents removed.")
