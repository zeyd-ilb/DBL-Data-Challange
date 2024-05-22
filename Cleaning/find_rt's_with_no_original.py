from pymongo import MongoClient
import time
import logging

# Configure logging settings
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s', filename='get_all_ids_from_cleaned_collection.log', filemode='w')

# MongoDB connection details
mongo_host = 'localhost'
mongo_port = 27017
database_name = 'DBL'
collection_name = 'cleaned'

start = time.time()

def get_ids_to_text(file_name):
    # Connect to MongoDB
    client = MongoClient(mongo_host, mongo_port)
    db = client[database_name]
    collection = db[collection_name]

    # pipeline to find all ids of reweeted tweets    : {"$match": {"retweeted_status.id": {"$exists": True}}},{"$project": {"retweeted_status":1, "id": 1, "_id":0}} # run this on pre-presentation 1 cleaned data
    # pipeline to find all ids of non-retweet tweets :{"$match": {}},{"$project": {"id": 1, "_id":0}}  # run this on uncleaned data 
        
    # Fetch all documents that contain the "retweeted_status" field
    pipeline = [
        {"$match": {}},
        {"$project": {"id": 1, "_id":0}}
    ]
    retweeted_docs = collection.aggregate(pipeline)

    counter = 0
    # Write IDs to a text file
    with open(file_name, 'w') as file:
        for doc in retweeted_docs:
            counter = counter + 1
            file.write(str(doc["id"])+ '\n')

def remove_duplicates(input_file, output_file):
    unique_ids = set()
    
    # Read the file and collect unique IDs
    with open(input_file, 'r') as file:
        for line in file:
            id = line.strip()
            unique_ids.add(id)

    # Write the unique IDs to a new file
    with open(output_file, 'w') as file:
        for id in unique_ids:
            file.write(id + '\n')

def sort_ids(input_file, output_file):
    # Read the IDs from the file
    with open(input_file, 'r') as f:
        ids = f.readlines()

    # Remove any extra whitespace/newline characters
    ids = [id.strip() for id in ids]

    # Sort the IDs
    ids.sort(key=int)  # Sorting numerically

    # Write the sorted IDs back to a file
    with open(output_file, 'w') as f:
        for id in ids:
            f.write(f"{id}\n")

def read_ids_from_file(file_path):
    with open(file_path, 'r') as file:
        #return [line.strip() for line in file]         # this line is used except "remove_ids" function
        return set([line.strip() for line in file])

def write_ids_to_file(file_path, ids):
    with open(file_path, 'w') as file:
        for id in ids:
            file.write(f"{id}\n")

def find_common_ids(file1_path, file2_path):
    ids_file1 = read_ids_from_file(file1_path)
    ids_file2 = read_ids_from_file(file2_path)
    common_ids = []
    i, j = 0, 0

    while i < len(ids_file1) and j < len(ids_file2):
        id1 = int(ids_file1[i])
        id2 = int(ids_file2[j])

        if id1 == id2:
            common_ids.append(id1)
            i += 1
            j += 1
        elif id1 < id2:
            i += 1
        else:
            j += 1

    return common_ids

def find_uncommon_ids(all_ids_file, ids_to_delete_file, output_file):
    # Read all IDs from the files
    all_ids = read_ids_from_file(all_ids_file)
    ids_to_delete = read_ids_from_file(ids_to_delete_file)

    # Remove the IDs that need to be deleted
    remaining_ids = all_ids - ids_to_delete

    # Write the remaining IDs to the output file
    write_ids_to_file(output_file, remaining_ids)

    
if __name__ == "__main__":
    #!!!! CONFIGURE FILE NAMES  
    #!!!! you need to run the code to get all non-retweet ids and to get retweeted_status.ids  
    #!!!! collection names and pipelines should be configured according to what is trying to extracted from the db
    #! read_ids_from_file needs to be changed before using find_uncommon_ids details are in the function
    
    file_name_1= "all_ids_from_cleaned_collection.txt" 
    file_name_1_output = "all_ids_removed_duplicate.txt" 
    file_name_2_output = "sorted_all_ids.txt" 

    get_ids_to_text(file_name_1)
    remove_duplicates(file_name_1, file_name_1_output)
    sort_ids(file_name_1_output,file_name_2_output)

    file1_path = 'sorted_all_ids.txt'
    file2_path = 'sorted_ids.txt'
    common_ids_file_path = 'common_ids.txt'

    common_ids = find_common_ids(file1_path, file2_path)
    write_ids_to_file(common_ids_file_path, common_ids)
    print(f"Found {len(common_ids)} common IDs.")

    # File paths
    all_rt_ids_file = 'sorted_ids.txt'
    ids_to_delete_file = 'common_ids.txt'
    output_file = 'uncommon_ids.txt'

    # Remove the IDs
    find_uncommon_ids(all_rt_ids_file, ids_to_delete_file, output_file)

    end = time.time()
    logging.info(f"it took : {end-start} seconds to finish the first part")
    print(f"it took : {end-start} seconds")
