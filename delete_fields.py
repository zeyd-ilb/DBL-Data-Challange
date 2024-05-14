import os
import json
import time

# start = time.time()

def check_retweets(full_key,data,key,rt):
    if full_key == "retweeted_status":
        rt = True
    elif rt and full_key == "is_quote_status":
        if data[key] == False:
            gbd = True
            # print('data will be deleted')
    return data,key, rt,gbd

def check_truncated(full_key,data,key):
    if full_key == "truncated" and data[key] == True:
        del data['text']
    return data,key

def delete_fields(data, fields_to_delete, rt, parent_key='' ):
    gbd = None 
    if isinstance(data, dict):
        for key in list(data.keys()):
            # Build the full key path including parent keys if present
            full_key = f"{parent_key}.{key}" if parent_key else key
            
            data,key,rt, gbd = check_retweets(full_key,data,key,rt)
            data,key = check_truncated(full_key,data,key)

            if full_key in fields_to_delete:
                del data[key]
            else:
                # Recursively call delete_fields with the updated key path
                delete_fields(data[key], fields_to_delete,rt, full_key)
    elif isinstance(data, list):
        for item in data:
            # Recursively call delete_fields for each item in the list
            delete_fields(item, fields_to_delete, rt, parent_key)
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
                original_data = json.loads(line)
                gon_be_deleted = delete_fields(original_data, fields_to_delete,retweeted)
                if gon_be_deleted:
                    deleted_lines.append(json.dumps(original_data) + '\n')
                else: 
                    modified_lines.append(json.dumps(original_data) + '\n')
        with open(file_path,'w+') as f:        
           f.writelines(modified_lines)

if __name__ == "__main__":
    folder_path = "C:\\Users\\20223070\\Downloads\\deneme data\\yan"  # Path to the folder containing JSON files
    fields_to_delete = ["id_str"]  # List of fields to delete
    process_json_files(folder_path, fields_to_delete)
    # end = time.time()
    # print(end - start)