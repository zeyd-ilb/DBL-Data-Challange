import os
import json
import time
import logging


# Configure logging settings
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s', filename='cleaning.log', filemode='w')

# Initialize counters for various conditions
truncated_counter = 0
null_counter = 0
empty_array_counter = 0
deleted_counter = 0
retweet_counter = 0
deleted_field_counter = 0

# Record the start time for performance measurement
start = time.time()

# Temporary storage for transferring data
transfer = {"full_text": None, "entities": None}

# Initialize line and file name tracking variables
line_number = 0
file_name = None

""" Checks if a field is null or an empty array and deletes it if true.
    Since the key value is deleted we have to change the skipp status to True
    so the other functions will not be executed for this key 
"""
def check_null(full_key,data,key):
    skipp = None
    global null_counter
    global empty_array_counter

    if data[key] is None: 
        del data[key]
        skipp = True 
        null_counter = null_counter + 1
        #logging.info(f"Deleted key {full_key} because it was null")
    elif (isinstance(data[key], list) and len(data[key]) == 0):
        del data[key]
        skipp = True
        empty_array_counter = empty_array_counter + 1
        #logging.info(f"Deleted key {full_key} because it was empty array")
    return data,key, skipp

""" Checks if the tweet is a retweet or corrupted (referred as deleted in the raw data).
    gbd is an abbreviation for "Gonna Be Deleted" which basically means the data will 
    be deleted if it is True.
"""
def check_retweets_and_deletes(full_key, gbd):
    global retweet_counter
    global deleted_counter
    if full_key == "retweeted_status":
        gbd = True
        #logging.info(f"Found retweet status at line {line_number}")
        retweet_counter = retweet_counter + 1
    elif  full_key == "delete":
        gbd = True
        #logging.info(f"Found deleted status at line {line_number}")
        deleted_counter = deleted_counter + 1
    return gbd

""" Checks if the tweet is truncated."""
def check_truncated(full_key,data,key,tr):
    global truncated_counter 
    if full_key == "truncated" and data[key] == True:
        tr = True
        truncated_counter = truncated_counter + 1
        #logging.info(f"Found truncated status at key {full_key}")
    return data,key, tr

""" Records text and entities fields for transfer to original tweet structure.
    If access is True then the function is called to copy the fields to dictionary "transfer".
    If access is False then the function is returning transfer. This part is called when we 
    want to transfer the fields from extended_tweet to the surface level fields as "text", "entities" and "extended_entities"
"""
def record_text(data,key,access):
    global transfer
    if access:
        transfer['full_text'] = data['full_text']
        transfer['entities'] = data['entities']
        if "extended_entities" in data:
            transfer['extended_entities'] = data['extended_entities']
            #logging.info(f"Recorded extended entities for key extended_entities in line {line_number}")
        #logging.info(f"Recorded text and entities for key {key} in line {line_number}")
    else:
        return transfer

"""
Transfers data from extended_tweet structure to the original tweet structure.
The parameter original takes the original data itself
"""
def tranfer_from_extended_to_original(original):
    transfers = record_text(data='',key='',access=False)
    original['text'] = transfers['full_text']

    for k in transfers.keys():
        if k != "full_text" and k != "display_text_range":
            original[k] = transfers[k]
    
    # Remove extended tweet after transfer is complete 
    if "extended_tweet" in original:
        del original['extended_tweet']
        logging.info(f"Transferred data from extended_tweet to original")
    return original

"""
Recursively deletes specified fields and handles retweets, deletions, and truncation.
Kind of a main part where all the other functions are used. It enables to iterate through
each field one by one and call the functions to check retweets, truncated or redundant field.
"""
def delete_fields(data, fields_to_delete,keys_to_delete, rt, trunc, parent_key='' ):
    gbd = None
    skip = None
    global deleted_field_counter 
    if isinstance(data, dict):
        for key in list(data.keys()):
            # Build the full key path including parent keys if present
            full_key = f"{parent_key}.{key}" if parent_key else key

            gbd = check_retweets_and_deletes(full_key, gbd)
            
            #To not run the rest of the code, if the data is retweet or corrupted 
            if gbd:
                logging.info(f"The line number {line_number} will be deleted from file {file_name} ")
                return gbd , trunc
            
            data,key,trunc = check_truncated(full_key,data,key,trunc)
            data,key,skip = check_null(full_key, data,key)

            if not skip:
                if (full_key in fields_to_delete or key in keys_to_delete):
                    del data[key] #the key was redundant so removed
                    deleted_field_counter = deleted_field_counter + 1
                    #logging.info(f"Deleted key {full_key}")

                elif trunc and (full_key in is_it_full_text):
                    record_text(data,key,True)

                else:
                        # Recursively call delete_fields with the updated key path
                        delete_fields(data[key], fields_to_delete,keys_to_delete,rt, trunc, full_key)

    elif isinstance(data, list):
        for item in data:
            # Recursively call delete_fields for each item in the list
            delete_fields(item, fields_to_delete, keys_to_delete,rt,trunc, parent_key)
    return gbd, trunc

""" Processes all JSON files in the specified folder."""
def process_json_files(folder_path, fields_to_delete):
    # Get list of JSON files in the folder
    json_files = [f for f in os.listdir(folder_path) if f.endswith('.json')]
    file_number = 0
    for json_file in json_files:
        file_path = os.path.join(folder_path, json_file)
        modified_lines = []
        file_number = file_number + 1
        print(f"dealing with file number: {file_number}/567" )
        
        #used in logging
        global file_name
        file_name = json_file 

        logging.info(f"Processing file: {json_file}")
        with open(file_path,"r+") as f:
            global line_number
            line_number = 0
            # Read each line from the file and process JSON data
            for line in f:
                line_number += 1
                if "Exceeded connection limit for user" not in line:
                    retweeted = False
                    truncated = False
                    try:
                        original_data = json.loads(line)
                        gon_be_deleted, truncated = delete_fields(original_data, fields_to_delete,keys_to_delete,retweeted, truncated)
                        if truncated and not gon_be_deleted:
                            original_data = tranfer_from_extended_to_original(original_data)
                        if not gon_be_deleted: 
                            modified_lines.append(json.dumps(original_data) + '\n')
                    except:
                        logging.error(f"ERROR occured at file: {json_file} in line {line_number}")
                               
        with open(file_path,'w+') as f:        
           f.writelines(modified_lines) #write only the clean data back to the same file 

if __name__ == "__main__":
    folder_path = "C:\\Users\\20223070\\Downloads\\deneme data\\yan"  # Path to the folder containing JSON files
    is_it_full_text = ["extended_tweet.full_text"]
    fields_to_delete = ["created_at"]  # List of fields to delete
    keys_to_delete = ["indices","display_text_range","media_url","media_url_https","display_url","expanded_url","id_str","in_reply_to_status_id_str",
                      "in_reply_to_user_id_str","quoted_status_id_str", "display_text_range","default_profile_image","profile_background_image_url",
                      "profile_image_url"]
    
    process_json_files(folder_path, fields_to_delete)
    
    end = time.time()
    # Log the results and processing time
    logging.info(f"deleted fields counter is : {deleted_field_counter}")
    logging.info(f"empty array counter is : {empty_array_counter}")
    logging.info(f"null counter is : {null_counter}")
    logging.info(f"retweeted counter is : {retweet_counter}")
    logging.info(f"truncated counter is : {truncated_counter}")
    logging.info(f"deleted (corrupted) tweets counter is : {deleted_counter}")
    logging.info(f"Processing completed in {end - start} seconds")
    print(end - start)
