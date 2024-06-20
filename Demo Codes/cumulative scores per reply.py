from pymongo import MongoClient
import csv
import re
import time

# Connect to the MongoDB client
client = MongoClient('mongodb://localhost:27017/')

# Access the database and collections
db = client['Chains']
collection = db['chains_British_Airways_v3']
compound_scores_collection = db['compound_scores_3m']

pipeline = [
    {
        '$project': {
            'results': 0
        }
    },
    {
        '$match': {
            'root_user_id':{"$nin":[18332190]}
        }
    },
     {
        '$match': {
            'chains': {
                '$elemMatch': {
                    '$elemMatch': {
                        'in_reply_to_user_id': {
                            '$in': [
                                18332190
                            ]
                        }
                    }
                }
            }
        }
    }, 
    # {
    #     '$match': {
    #         '$expr': {
    #             "$and":[
    #             {'$gt': [{'$size': '$chains'}, 0]},
    #             {"$lt": [{ "$size": "$chains" }, 10]}
    #             ]
    #         }
    #     }
    # }, 
    # {
    #     '$limit': 10000
    # }
]

# Fetch the documents
documents = list(collection.aggregate(pipeline))

def update_score(cumulative,item_id):
    cumulative += compound_scores.get(item_id,0)
    return cumulative

    
def extract_numbers_from_brackets(line):
    # Extract the numbers inside the brackets
    matches = re.findall(r'\[(.*?)\]', line)
    extracted_data = []
    for match in matches:
        numbers = match.split(',')
        extracted_data.append(numbers)
    return extracted_data

def txt_to_csv(input_file, output_file):
    with open(input_file, 'r') as txt_file:
        lines = txt_file.readlines()
    
    all_data = []
    for line in lines:
        extracted_data = extract_numbers_from_brackets(line)
        all_data.extend(extracted_data)
    
    # Determine the maximum number of columns
    max_columns = max(len(row) for row in all_data)

    with open(output_file, 'w', newline='') as csv_file:
        csv_writer = csv.writer(csv_file)
        
        for row in all_data:
            # Extend row with empty strings if it has less columns than max_columns
            row.extend([''] * (max_columns - len(row)))
            csv_writer.writerow(row)


def fix_txt(input,output):
    print("in fix_txt")
    # Read the data from the text file
    with open(input, 'r') as file:
        data = file.read()

    # Convert the string representation of the list into an actual list
    data_list = eval(data)

    # Filter out sublists that have more than one number
    filtered_list = [sublist for sublist in data_list if len(sublist) > 0 ]
    filtered_list = [sublist for sublist in filtered_list if len(sublist) < 6 ]

    # Optionally, save the filtered list back to a file
    with open(output, 'w') as file1:
        file1.write(str(filtered_list))

# Fetch compound scores and store them in a dictionary for quick access
cumulative_scores_total = list()

compound_scores = {}
for docc in compound_scores_collection.aggregate([{"$project":{"_id":0,"id":1,"compound_score":1}}]):
    compound_scores[str(docc['id'])] = docc['compound_score']

# Process each document
for doc in documents:
    cumulative_score = 0
    root_tweet = str(doc["id"])

    item_number = 0
    chains = doc['chains']
    if compound_scores.get(root_tweet,0) < -0.3:
        # Process each chains
        for chain in chains:
            cumulative_scores = []
            cumulative_score = update_score(cumulative_score,root_tweet)
            item_number = item_number + 1
            # Process each tweet
            for item in chain:
                user_id = str(item["user"]['id'])
                item_id = str(item['id'])
                # Check if it is a reply from the airline
                if user_id == "18332190":  
                    # Reset cumulative_score for the next segment
                    if item_number != 0:
                        cumulative_score = cumulative_score/item_number
                        cumulative_scores.append(cumulative_score)
                        item_number = 0
                        cumulative_score = 0

                else:
                    item_number = item_number + 1
                    # Sum the scores from compound_scores
                    cumulative_score = update_score(cumulative_score,item_id)
                item['cumulative_score'] = cumulative_score  # Store the cumulative score
                
            # Chain is finished, add the scores of the tweets (if exist) after the last airline reply 
            if item_number > 0:
                    cumulative_score = cumulative_score/item_number
                    cumulative_scores.append(cumulative_score)
                    cumulative_score =0
                    item_number = 0
            cumulative_scores_total.append(cumulative_scores)
            

# Write the chains to a text file
input_file_1 = 'chains_scores_v1.txt'  # Replace with your input text file name
output_file_1 = 'fixed_scores_v1.txt'  # Replace with your input text file name
with open(input_file_1, "w") as file:
    file.write(f"{cumulative_scores_total}\n")
'''
fix_txt(input_file_1,output_file_1)

input_file_2 = output_file_1
output_file_2 = 'output_file_2.csv'  # Replace with your desired output CSV file name
txt_to_csv(input_file_2, output_file_2)
print(f"Conversion complete. {output_file_2} has been created.")

'''
