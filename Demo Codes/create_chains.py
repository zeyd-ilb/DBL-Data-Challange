from pymongo import MongoClient
from collections import defaultdict

# Connect to MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client['DBL']
collection = db['all_chains'] #all_chains is duplicate of all_results_2

# Fetch the document
"""
#The initial/original pipeline
pipeline = [
    {"$match": {"results":{"$ne":[]}
                }},
    {"$project": {"results": 1}},
]
"""
#Pipeline to run if the initial pipeline got error after running. This one will save some time
pipeline = [
    {"$match": {"chains":{"$exists":0}, "results":{"$ne":[]}
                }},
    {"$project": {"results": 1}},
]
doc = collection.aggregate(pipeline)

cod = list(doc)

# Create a dictionary to store chains by section
all_chains = defaultdict(list)

# Helper function to create chains
def create_chains(tweet, current_chain, results, chains):
    current_chain.append(tweet)
    tweet_id = str(tweet['id'])

    has_replies = False
    for reply in results:
        reply_to_id = str(reply['in_reply_to_status_id'])
        if reply_to_id == tweet_id:
            has_replies = True
            new_chain = current_chain.copy()
            create_chains(reply, new_chain, results, chains)
                
    if not has_replies:
        chains.append(current_chain)

# Process each section in 'cod'
for section_index, section in enumerate(cod):
    print("handling document : " , section_index)
    results = section["results"]
    
    # Create a dictionary to map each tweet by its id for the current section
    tweets_by_id = {}
    root_tweets = list() 
    for tweet in results:
        tweet_id = str(tweet['id'])
        tweets_by_id[tweet_id] = tweet
        if tweet["depth"] == 0:
            root_tweets.append(tweet)

    # Create a dictionary to store chains for the current section
    chains = []
    
    # Find the root tweet for the current section
    for tw in root_tweets:
        create_chains(tw, [], results, chains)
        all_chains[section_index] = chains
        collection.update_one(
                {"_id": section["_id"]},
                {"$set": {"chains": chains}}
        )
"""
# Write the chains to a text file
with open("chains.txt", "w") as file:
    for section_index, chains in all_chains.items():
        file.write(f"Section {section_index}:\n")
        for chain_id, chain in enumerate(chains):  # Adjusted this line to use enumerate since chains is a list
            file.write(f"  Chain {chain_id}:\n")
            for tweet in chain:
                file.write(f"    - {tweet}\n")
"""
