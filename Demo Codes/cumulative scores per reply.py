from pymongo import MongoClient

# Connect to the MongoDB client
client = MongoClient('mongodb://localhost:27017/')

# Access the database and collections
db = client['Chains']
collection = db['chains_British_Airways']
compound_scores_collection = db['compound_scores_1']

pipeline = [
    {
        '$project': {
            'results': 0
        }
    }, {
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
    }, {
        '$match': {
            '$expr': {
                "$and":[
                {'$gt': [{'$size': '$chains'}, 1]},
                {"$lt": [{ "$size": "$chains" }, 10]}
                ]
            }
        }
    }, {
        '$limit': 1000
    }
]

# Fetch the documents
documents = list(collection.aggregate(pipeline))

def update_score(cumulative,item_id):
    cumulative += compound_scores.get(item_id,0)
    return cumulative

# Fetch compound scores and store them in a dictionary for quick access
cumulative_scores_total = list()

compound_scores = {}
for doc in compound_scores_collection.aggregate([{"$project":{"_id":0,"id":1,"compound_score":1}}]):
    compound_scores[str(doc['id'])] = doc['compound_score']


# Process each document
for doc in documents:
    
    cumulative_score = 0
    root_tweet = str(doc["id"])

    item_number = 0
    chains = doc['chains']
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
            
print("Total is:",cumulative_scores_total)

# Write the chains to a text file
with open("chains_scores.txt", "w") as file:
    file.write(f"{cumulative_scores_total}\n")