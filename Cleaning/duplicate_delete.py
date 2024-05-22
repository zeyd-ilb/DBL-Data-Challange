from pymongo import MongoClient
import logging


# Configure logging settings
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s', filename='remove_duplicates.log', filemode='w')

# Read the duplicate IDs from the text file
def read_duplicate_ids(file_path):
    with open(file_path, 'r') as file:
        return [line.strip() for line in file]

# Connect to MongoDB
client = MongoClient('mongodb://localhost:27017/')
db = client['DBL']
collection = db['cleaned_v2']

# Path to the file containing duplicate IDs
duplicate_ids_file = 'duplicates.txt'

# Get the list of duplicate IDs
duplicate_ids = read_duplicate_ids(duplicate_ids_file)

# Remove duplicates from MongoDB
for dup_id in duplicate_ids:
    # print("dup id is: ", dup_id)
    # Find all documents with this duplicate ID
    # print("\n looking for this id: " , dup_id)
    pipeline = [
        {"$project":{"id" : 1 , "_id" : 1 }},
        {"$match": {"id": int(dup_id)}}
    ]

    docs = list(collection.aggregate(pipeline))

    # Keep one document and remove the rest
    if len(docs) > 1:
        # Sort documents if necessary to keep a specific one, e.g., by creation date
        docs_to_delete = docs[1:]  # Keeping the first document and deleting the rest
        
        for doc in docs_to_delete:
            # print("BU _ID SILINECEK", doc["_id"])
            logging.info(f"This object_id gonna be deleted {doc['_id']} for this id : {doc['id']}")
            collection.delete_one({"_id": doc["_id"]})
    elif len(docs)==1:
        for i in docs:
            # print("There aren't more than doc one for this id",i["id"])
            logging.info(f"There aren't more than 1 doc one for this id {i['id']}")
    else:
            # print("No result for ",dup_id)
            logging.info(f"No result for {dup_id}")

print("Duplicate documents removed.")

