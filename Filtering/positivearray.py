#Creating an array with positive words
with open('positive-words.txt', 'r') as file:
    # Initialize an empty list to store positive words
    positive_words = []
    
    # Read each line in the file
    for line in file:
        # Strip whitespace and newline characters from the line
        word = line.strip()
        
        # Add the word to the list of positive words
        positive_words.append(word)


import re

# Assuming you have the positive_words array populated with positive words

# Construct regex pattern from positive words array
regex_pattern = "|".join(map(re.escape, positive_words))

# Construct MongoDB query
mongo_query = {
    "text": {
        "$regex": regex_pattern,
        "$options": "i"  # Case-insensitive search
    }
}

# Print the MongoDB query to copy+paste in MongoDB Compass
print(mongo_query)
