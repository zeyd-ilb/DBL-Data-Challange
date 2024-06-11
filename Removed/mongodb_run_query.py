from pymongo import MongoClient
from collections import Counter
from bson import ObjectId

# Replace these with your actual MongoDB connection details
mongo_host = 'localhost'
mongo_port = 27017
database_name = 'DBL'
collection_name = 'trial2'

def get_language_counts():
    # Connect to MongoDB
    client = MongoClient(mongo_host, mongo_port)
    db = client[database_name]
    collection = db[collection_name]

    # Aggregate language counts
    language_counts = collection.aggregate([
        {"$group": {"_id": "$lang", "count": {"$sum": 1}}}
    ])

    # Convert to dictionary
    lang_count_dict = {doc['_id']: doc['count'] for doc in language_counts}

    return lang_count_dict

def run_query(query):
    # Connect to MongoDB
    client = MongoClient(mongo_host, mongo_port)
    db = client[database_name]
    collection = db[collection_name]

    # Run the query
    print(query)
    results = collection.find(query)
    # Count the number of tweets for each user
    user_tweet_counts = {}
    for result in results:
        user_id = result['user']['id']
        if user_id in user_tweet_counts:
            user_tweet_counts[user_id] += 1
        else:
            user_tweet_counts[user_id] = 1

    # Print the results
    print("User Tweet Counts:")
    for user_id, count in user_tweet_counts.items():
        print(f"User ID: {user_id}, Tweet Count: {count}")

def find_mentiones(query):
    # Connect to MongoDB
    client = MongoClient(mongo_host, mongo_port)
    db = client[database_name]
    collection = db[collection_name]

    # Run the query
    results = collection.aggregate(query)
    print(results)
    # Print the results
    print("Tweet counts per user:")
    for result in results:
        user_id = result['_id']['user_id']
        username = result['_id']['username']
        tweet_count = result['tweet_count']
        print(f"User ID: {user_id}, Username: {username}, Tweet Count: {tweet_count}")

if __name__ == "__main__":
    # Example query: Find all documents where the 'lang' is 'en'
    #query = {"lang": "en"}
    #run_query(query)

     # Define the users and their corresponding user IDs
    users = {
        "KLM": 56377143,
        "AirFrance": 106062176,
        "British_Airways": 18332190,
        "AmericanAir": 22536055,
        "Lufthansa": 124476322,
        "AirBerlin": 26223583,
        "AirBerlin assist": 2182373406,
        "easyJet": 38676903,
        "RyanAir": 1542862735,
        "SingaporeAir": 253340062,
        "Qantas": 218730857,
        "EtihadAirways": 45621423,
        "VirginAtlantic": 20626359
    }
    # Define the list of user IDs
    # user_ids = list(users.keys())
    user_ids = [56377143, 106062176, 18332190, 22536055, 124476322, 26223583, 2182373406, 38676903, 1542862735, 253340062, 218730857, 45621423, 20626359]

    # Construct the query
    query = {
        "in_reply_to_user_id": {"$in": user_ids}
    }

    # Aggregate to group tweets per user
    pipeline = [
        {"$match": query},
        {"$group": {
            "_id": {
                "user_id": "$in_reply_to_user_id",
                "username": "$in_reply_to_screen_name"
            },
            "tweet_count": {"$sum": 1}
        }}
    ]
    find_mentiones(pipeline)

"""
    # Run query for each user
    for username, user_id in users.items():
        query = {"user.id": user_id,"in_reply_to_status_id":{"$eq":None}}
        print(f"\nRunning query for {username}:")
        run_query(query)
"""
    # Get and print language counts
    #language_counts = get_language_counts()
    #print("Language counts:")
    #for lang, count in language_counts.items():
        #print(f"{lang}: {count}")
