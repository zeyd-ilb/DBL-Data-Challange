import os
import json
import time

# start = time.time()
a = {
    "full_text": None,
    "display_text_range": None,
    "entities": None
}
def check_null(full_key,data,key):
    skipp = None
    if data[key] is None:
        del data[key]
        skipp = True
    return data,key, skipp

def check_retweets(full_key, data, key, rt, gbd):
    if full_key == "retweeted_status":
        rt = True
    elif rt and full_key == "is_quote_status":
        if data[key] == False:
            gbd = True
    return data,key, rt,gbd

def check_truncated(full_key,data,key,tr):
    if full_key == "truncated" and data[key] == True:
        tr = True
        # if 'text' in data:
        #     del data['text']
    return data,key, tr

def record_text(data,key,pull_push):
    global a
    if pull_push:
        a['full_text'] = data['full_text']
        a['entities'] = data['entities']
        a['display_text_range'] = data['display_text_range']
    else:
        return a

def tranfer_from_extended_to_original(original):
    transfers = record_text(data='',key='',pull_push=False)
    original['text'] = transfers['full_text']
    for k in transfers.keys():
        if k != "full_text" and k in original:
            original[k] = transfers[k]
    return original

def delete_fields(data, fields_to_delete, rt, trunc, parent_key='' ):
    gbd = None
    skip = None
    if isinstance(data, dict):
        for key in list(data.keys()):
            # Build the full key path including parent keys if present
            full_key = f"{parent_key}.{key}" if parent_key else key

            data,key,rt, gbd = check_retweets(full_key, data, key, rt, gbd)
            data,key, trunc = check_truncated(full_key,data,key,trunc)
            data,key,skip = check_null(full_key, data,key)
            
            if full_key in fields_to_delete:
                print("this one has been deleted" , key)

                del data[key]
            elif trunc and (full_key in fields_to_transfer):
                record_text(data,key,True)

            else:
                if not skip:
                    # Recursively call delete_fields with the updated key path
                    delete_fields(data[key], fields_to_delete,rt, trunc, full_key)

    elif isinstance(data, list):
        for item in data:
            # Recursively call delete_fields for each item in the list
            delete_fields(item, fields_to_delete, rt,trunc, parent_key)
    return gbd


def process_json_files(folder_path, fields_to_delete):
    # Get list of JSON files in the folder
    json_files = [f for f in os.listdir(folder_path) if f.endswith('.json')]
    for json_file in json_files:
        file_path = os.path.join(folder_path, json_file)
        modified_lines = []
        deleted_lines = []

        with open(file_path,"r+") as f:
            # Read each line from the file and process JSON data
            for line in f:
                retweeted = False
                truncated = False
                original_data = json.loads(line)
                gon_be_deleted = delete_fields(original_data, fields_to_delete,retweeted, truncated)
                original_data = tranfer_from_extended_to_original(original_data)

                if gon_be_deleted:
                    deleted_lines.append(json.dumps(original_data) + '\n')
                else: 
                    modified_lines.append(json.dumps(original_data) + '\n')
        with open(file_path,'w+') as f:        
           f.writelines(modified_lines)

if __name__ == "__main__":
    folder_path = "C:\\Users\\20223070\\Downloads\\deneme data\\yan"  # Path to the folder containing JSON files
    fields_to_transfer = ["extended_tweet.full_text"]
    fields_to_delete = ["id_str"]  # List of fields to delete
    process_json_files(folder_path, fields_to_delete)
    # end = time.time()
    # print(end - start)
