import os
import json
import time
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s', filename='yan_Deneme.log', filemode='w')

truncated_counter = 0
null_counter = 0
empty_array_counter = 0
deleted_counter = 0
retweet_counter = 0
deleted_field_counter = 0

start = time.time()
a = {
    "full_text": None,
    "display_text_range": None,
    "entities": None
}
line_number = 0
file_name = 0

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

def check_truncated(full_key,data,key,tr):
    global truncated_counter 
    if full_key == "truncated" and data[key] == True:
        tr = True
        truncated_counter = truncated_counter + 1
        #logging.info(f"Found truncated status at key {full_key}")
    return data,key, tr

def record_text(data,key,pull_push):
    global a
    if pull_push:
        a['full_text'] = data['full_text']
        a['entities'] = data['entities']
        if "extended_entities" in data:
            a['extended_entities'] = data['extended_entities']
            #logging.info(f"Recorded extended entities for key extended_entities in line {line_number}")
        #logging.info(f"Recorded text and entities for key {key} in line {line_number}")
    else:
        return a

def tranfer_from_extended_to_original(original):
    transfers = record_text(data='',key='',pull_push=False)
    original['text'] = transfers['full_text']

    for k in transfers.keys():
        if k != "full_text" and k != "display_text_range":
            original[k] = transfers[k]
    if "extended_tweet" in original:
        del original['extended_tweet']
        logging.info(f"Transferred data from extended_tweet to original")
    return original

def delete_fields(data, fields_to_delete,keys_to_delete, rt, trunc, parent_key='' ):
    gbd = None
    skip = None
    global deleted_field_counter 
    if isinstance(data, dict):
        for key in list(data.keys()):
            # Build the full key path including parent keys if present
            full_key = f"{parent_key}.{key}" if parent_key else key
            gbd = check_retweets_and_deletes(full_key, gbd)
            if gbd:
                logging.info(f"The line number {line_number} will be deleted from file {file_name} ")
                return gbd , trunc
            data,key, trunc = check_truncated(full_key,data,key,trunc)
            data,key,skip = check_null(full_key, data,key)

            if not skip:
                if (full_key in fields_to_delete or key in keys_to_delete):
                    del data[key]
                    deleted_field_counter = deleted_field_counter + 1
                    #logging.info(f"Deleted key {full_key}")

                elif trunc and (full_key in fields_to_transfer):
                    record_text(data,key,True)

                else:
                        # Recursively call delete_fields with the updated key path
                        delete_fields(data[key], fields_to_delete,keys_to_delete,rt, trunc, full_key)

    elif isinstance(data, list):
        for item in data:
            # Recursively call delete_fields for each item in the list
            delete_fields(item, fields_to_delete, keys_to_delete,rt,trunc, parent_key)
    return gbd, trunc


def process_json_files(folder_path, fields_to_delete):
    # Get list of JSON files in the folder
    json_files = [f for f in os.listdir(folder_path) if f.endswith('.json')]
    for json_file in json_files:
        file_path = os.path.join(folder_path, json_file)
        modified_lines = []

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
           f.writelines(modified_lines)

if __name__ == "__main__":
    folder_path = "C:\\Users\\20223070\\Downloads\\deneme data\\yan"  # Path to the folder containing JSON files
    fields_to_transfer = ["extended_tweet.full_text"]
    fields_to_delete = ["created_at"]  # List of fields to delete
    keys_to_delete = ["indices","display_text_range","media_url","media_url_https","display_url","expanded_url","id_str","in_reply_to_status_id_str",
                      "in_reply_to_user_id_str","quoted_status_id_str", "display_text_range","default_profile_image","profile_background_image_url",
                      "profile_image_url"]
    process_json_files(folder_path, fields_to_delete)
    end = time.time()
    logging.info(f"deleted fields counter is : {deleted_field_counter}")
    logging.info(f"empty array counter is : {empty_array_counter}")
    logging.info(f"null counter is : {null_counter}")
    logging.info(f"retweeted counter is : {retweet_counter}")
    logging.info(f"truncated counter is : {truncated_counter}")
    logging.info(f"retweeted counter is : {retweet_counter}")
    logging.info(f"Processing completed in {end - start} seconds")
    print(end - start)
