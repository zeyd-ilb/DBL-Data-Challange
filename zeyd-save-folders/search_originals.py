from pymongo import MongoClient
import time
import logging


# Configure logging settings
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s', filename='search_originals.log', filemode='w')

# MongoDB connection details
mongo_host = 'localhost'
mongo_port = 27017
database_name = 'DBL'
collection_name = 'cleaned'

start = time.time()
def find_and_remove_redundant_retweeted_ids(input_file):
    # Connect to MongoDB
    client = MongoClient(mongo_host, mongo_port)
    db = client[database_name]
    collection = db[collection_name]

    unique_ids = set()
    
    # Read the file and collect unique IDs
    with open(input_file, 'r') as file:
        for line in file:
            id = line.strip()
            unique_ids.add(id)

    # Check if each retweeted_status.id exists as an id in other documents
    quarantine_ids = []
    counter = 0

    for retweeted_id in unique_ids:
        counter = counter + 1
        print(f"doing {counter}th out of ??")
        # Check if there is a document with id matching retweeted_id (searching for original tweet)
        matching_doc = collection.find_one({"id":  int(retweeted_id)})
        
        #if there is no original tweet
        if not matching_doc:
            quarantine_ids.append(retweeted_id)
            logging.info(f"This id added to the list: {retweeted_id} ")
    
    return quarantine_ids,

if __name__ == "__main__":
    input_file = 'ids.txt'
    matching_ids = find_and_remove_redundant_retweeted_ids(input_file)
        
    # Write IDs to a text file
    with open('quarantine_ids.txt', 'w') as file:
        print("writing quarantine ids to text file : ")
        for doc in matching_ids:
            file.write(str(doc + '\n'))
    
    end = time.time()
    print(f"it took : {end-start} seconds")
    print(len(matching_ids)) 
