from pymongo import MongoClient
import time
import logging

# Configure logging settings
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s', filename='search_originals.log', filemode='w')

# MongoDB connection details
mongo_host = 'localhost'
mongo_port = 27017
database_name = 'DBL'
collection_name = 'trial2'

start = time.time()
def find_and_remove_redundant_retweeted_ids():
    # Connect to MongoDB
    client = MongoClient(mongo_host, mongo_port)
    db = client[database_name]
    collection = db[collection_name]

    # Fetch all documents that contain the "retweeted_status" field
    pipeline = [
        {"$match": {"retweeted_status.id": {"$exists": True}}},
        {"$project": {"retweeted_status.id": 1, "id": 1, "_id":0}}
    ]
    retweeted_docs = collection.aggregate(pipeline)

    counter = 0
    # Write IDs to a text file
    with open('ids.txt', 'w') as file:
        for doc in retweeted_docs:
            counter = counter + 1
            print(counter)
            print("anan is : ", doc['retweeted_status']['id'])
            file.write(str(doc["retweeted_status"]["id"])+ '\n')

    
if __name__ == "__main__":
    find_and_remove_redundant_retweeted_ids()
    end = time.time()
    logging.info(f"it took : {end-start} seconds to finish the first part")
    print(f"it took : {end-start} seconds")
