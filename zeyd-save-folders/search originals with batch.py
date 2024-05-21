from pymongo import MongoClient
import logging

# Replace these with your actual MongoDB connection details
mongo_host = 'localhost'
mongo_port = 27017
database_name = 'DBL'
collection_name = 'trial2'

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s', filename='originals.log', filemode='w')

def find_original_tweets(collection, unique_ids, batch_size=10):
    quarantine_ids = []
    counter = 0

    # Process IDs in batches
    for i in range(0, len(unique_ids), batch_size):
        batch = unique_ids[i:i + batch_size]
        print(f"Processing batch {i // batch_size + 1} out of {len(unique_ids) // batch_size + 1}")
        
        # Query for all IDs in the current batch
        batch_query = {"id": {"$in": [int(id) for id in batch]}}
        matching_docs = collection.find(batch_query)
        
        # Create a set of IDs that have matching documents
        found_ids = {doc['id'] for doc in matching_docs}
        
        # Determine which IDs are not in the found_ids set
        for retweeted_id in batch:
            counter += 1
            if int(retweeted_id) not in found_ids:
                quarantine_ids.append(retweeted_id)
                logging.info(f"This id added to the list: {retweeted_id}")

    return quarantine_ids

if __name__ == "__main__":
    # Connect to MongoDB
    client = MongoClient(mongo_host, mongo_port)
    db = client[database_name]
    collection = db[collection_name]

    unique_ids = []
    
    # Read the file and collect unique IDs
    with open("unique_ids.txt", 'r') as file:
        for line in file:
            id = line.strip()
            unique_ids.append(id)
    # Find and log quarantine IDs
    quarantine_ids = find_original_tweets(collection, unique_ids)
    print(f"Quarantine IDs: {quarantine_ids}")
