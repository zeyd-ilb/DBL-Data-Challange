import nltk
import pandas as pd
import requests
import json
from nltk.sentiment.vader import SentimentIntensityAnalyzer

nltk.download("vader_lexicon")

# Initialize sentiment analyzer
sent_analyzer = SentimentIntensityAnalyzer()

# Test the sentiment analyzer
sentence = "I like having meetings with my team"
print(sent_analyzer.polarity_scores(sentence))

# Define the data URL
data_url = 'https://raw.githubusercontent.com/zeyd-ilb/DBL-Data-Challange/Demo Codes/Sentiment-Analysis/airlines-1565119387407.json'

# Fetch the JSON data
response = requests.get(data_url)
if response.status_code == 200:
    # Split the response text into lines and parse each line as JSON
    json_lines = response.text.splitlines()
    texts = []
    sentiments = []
    for line in json_lines:
        if line.strip():  # Ensure the line is not empty
            json_obj = json.loads(line)
            if 'text' in json_obj:
                text = json_obj['text']
                # Analyze sentiment
                sentiment_score = sent_analyzer.polarity_scores(text)
                # Append text and sentiment score to lists
                texts.append(text)
                sentiments.append(sentiment_score)
    
    # Create a DataFrame with the extracted text data and sentiment scores
    sentiment_data = pd.DataFrame(texts, columns=['text'])
    # Add sentiment scores as new columns
    sentiment_data['compound'] = [score['compound'] for score in sentiments]
    sentiment_data['positive'] = [score['pos'] for score in sentiments]
    sentiment_data['negative'] = [score['neg'] for score in sentiments]
    sentiment_data['neutral'] = [score['neu'] for score in sentiments]
    
    # Display the first 10 rows
    print(sentiment_data.head(10))
else:
    print(f"Failed to fetch data. HTTP Status code: {response.status_code}")

