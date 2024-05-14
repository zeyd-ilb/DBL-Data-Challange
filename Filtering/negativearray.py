#Creating an array with negative words
with open('negative-words.txt', 'r') as file:
    # Initialize an empty list to store negative words
    negative_words = []
    
    # Read each line in the file
    for line in file:
        # Strip whitespace and newline characters from the line
        word = line.strip()
        
        # Add the word to the list of negative words
        negative_words.append(word)


import re

# Assuming you have the negative_words array populated with negative words

# Construct regex pattern from negative words array
regex_pattern = "|".join(map(re.escape, negative_words))

# Construct MongoDB query
mongo_query = {
    "text": {
        "$regex": regex_pattern,
        "$options": "i"  # Case-insensitive search
    }
}

# Print the MongoDB query to copy+paste in MongoDB Compass
print(mongo_query)