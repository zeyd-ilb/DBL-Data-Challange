import os
import subprocess
import json

def preprocess_json_file(folder_path):
    # Open the JSON file for reading
    cleaned_files = []
    json_files = [f for f in os.listdir(folder_path) if f.endswith('.json')]
    for json_file in json_files:
        file_path = os.path.join(folder_path, json_file)
        cleaned_counter = True  
        with open(file_path, "r+") as file:
            print("file " , file_path , " is OPENED")
            lines = file.readlines()
            file.seek(0)
            for line in lines:
                if "Exceeded connection limit for user" not in line:
                    file.write(line)
                else:
                    if cleaned_counter:
                        cleaned_files.append(json_file)
                        print("FILE: ", json_file, " CLEANED FROM BS")
                        cleaned_counter = False
            file.truncate()    
    return cleaned_files

def import_json_files(folder_path, db_uri, collection_name):
    # Get list of JSON files in the folder
    json_files = [f for f in os.listdir(folder_path) if f.endswith('.json')]
    failed_files = []

 # Iterate through each JSON file and import into MongoDB
    for json_file in json_files:
        file_path = os.path.join(folder_path, json_file)
        print(f"Importing {json_file}...")
        try:
            subprocess.run([
                'mongoimport',
                '--uri', db_uri,
                '--collection', collection_name,
                '--file', file_path,
            ], check=True)
            print(f"Successfully imported {json_file}.")
        except subprocess.CalledProcessError as e:
            failed_files.append(json_file)
            print(f"Failed to import {json_file}: {e}")
    return failed_files

if __name__ == "__main__":
    folder_path = "C:\\Users\\20223070\Downloads\\deneme data\\orta"  # Path to the folder containing JSON files
    db_uri = "mongodb://localhost:27017/DBL"  # MongoDB URI
    collection_name = "Trial01"  
    #a = preprocess_json_file(folder_path)
    #print(a)
    #b = import_json_files(folder_path, db_uri, collection_name)
    #print(b)