from transformers import pipeline
from transformers import AutoModelForSequenceClassification, AutoTokenizer
from scipy.special import softmax

# Define broad categories and their sub-categories
broad_categories = {
    "Luggage Issues": {
        "Missing Luggage": "We're sorry to hear about your missing luggage. Please contact our support team with your flight details.",
        "Damaged Luggage": "We regret the damage to your luggage. Please file a claim through our online form."
    },
    "Flight Issues": {
        "Flight Prices": "For inquiries about flight prices, visit our website or contact our sales team.",
        "Refunds": "For refund requests, please visit our refunds page and submit your details.",
        "Flight Booking Issues": "If you're experiencing issues with flight booking, please contact our support team for assistance.",
        "Flight Delay": "We apologize for the delay. Please check the flight status on our app for real-time updates.",
        "Unexpected Flight Length": "We apologize for any inconveniences caused by the unexpected flight length and will take in your feedback for consideration. We hope to make your future journeys more comfortable.",
        "Cancelled Flight": "We're sorry your flight was cancelled. Please contact our support team for rebooking options.",
        "Possessions left on the plane": "If you've left something on the plane, please fill out the lost and found form on our website.",
        "In-Flight Services": "Thank you for your feedback on our in-flight amenities. We strive to improve our services.",
        "Flight Attendant Complaints": "We're sorry to hear about your experience. Please provide more details to our customer service."
    },
    "Service Issues": {
        "Wheelchair Issue": "For special assistance requests, please contact our special services department.",
        "Elderly Issue": "For special assistance requests, please contact our special services department.",
        "Customer Service Issue": "We apologize for any inconvenience caused by our customer service. Please provide more details.",
        "Airport Issues": "For issues at the airport, please report them to the airport management or contact our support."
    },
    "Unclassified": {
        "Unclassified": "Thank you for reaching out. Please provide more details so we can assist you better."
    }
}

# Load the zero-shot classification pipeline
classifier = pipeline("zero-shot-classification", model="facebook/bart-large-mnli")

# Initialize the sentiment analysis model
MODEL_NAME = "cardiffnlp/twitter-roberta-base-sentiment-latest"
tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
model = AutoModelForSequenceClassification.from_pretrained(MODEL_NAME)
model.eval()

# Calculate RoBERTa compound score
def calculate_compound_score(scores, config):
    label_to_weight = {
        'positive': 1,
        'neutral': 0,
        'negative': -1}
    compound_score = 0
    for i in range(scores.shape[0]):
        label = config.id2label[i]
        weight = label_to_weight[label]
        compound_score += scores[i] * weight
    print(compound_score)
    return compound_score

# Run the sentiment analysis using RoBERTa
def analyze_sentiment(tweet):
    try:
        inputs = tokenizer(tweet, return_tensors='pt', truncation=True, max_length=514)
        outputs = model(**inputs)
        scores = outputs.logits.detach().numpy()
        scores = softmax(scores, axis=1)
        return calculate_compound_score(scores[0], model.config)
    except IndexError as e:
        print(f"Error processing text: {tweet[:50]}... - {e}")
        return None

def classify_tweet(tweet):
    # First classify into broad category
    broad_result = classifier(tweet, candidate_labels=list(broad_categories.keys()))
    broad_category = broad_result['labels'][0]
    broad_confidence = broad_result['scores'][0]
    
    # Now classify into specific sub-category within the chosen broad category
    sub_categories = broad_categories[broad_category]
    sub_result = classifier(tweet, candidate_labels=list(sub_categories.keys()))
    sub_category = sub_result['labels'][0]
    sub_confidence = sub_result['scores'][0]
    
    response = sub_categories[sub_category]
    
    return broad_category, broad_confidence, sub_category, sub_confidence, response

# Main part of the code, asks for a user input and returns the category and response to the tweet
def main():
    while True:
        print("Enter a tweet:")
        tweet = input()
        if analyze_sentiment(tweet) <= -0.3:
            broad_category, broad_confidence, sub_category, sub_confidence, response = classify_tweet(tweet)
            print(f"Broad Category: {broad_category} (Confidence: {broad_confidence:.2f})")
            print(f"Specific Category: {sub_category} (Confidence: {sub_confidence:.2f})")
            print(f"Response: {response}")
            print()
        else:
            print("This tweet is not a complaint!")
            print()

if __name__ == "__main__":
    main()
