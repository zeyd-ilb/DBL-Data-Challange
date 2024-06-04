import pymongo
from transformers import AutoModelForSequenceClassification, AutoTokenizer
from scipy.special import softmax
import torch
import time

# Initialize the sentiment analysis model
MODEL_NAME = "cardiffnlp/twitter-roberta-base-sentiment-latest"
tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
model = AutoModelForSequenceClassification.from_pretrained(MODEL_NAME)
model.eval()

def calculate_compound_score(scores, config):
    label_to_weight = {
        'positive': 1,
        'neutral': 0,
        'negative': -1
    }
    compound_score = 0

    for i in range(scores.shape[0]):
        label = config.id2label[i]
        weight = label_to_weight[label]
        compound_score += scores[i] * weight
    return compound_score

def analyze_sentiment(text):
    try:
        inputs = tokenizer(text, return_tensors='pt', truncation=True, max_length=514)
        outputs = model(**inputs)
        scores = outputs.logits.detach().numpy()
        scores = softmax(scores, axis=1)
        return calculate_compound_score(scores[0], model.config)
    except IndexError as e:
        print(f"Error processing text: {text[:50]}... - {e}")
        return None

def update_sentiment_scores_batch(db_uri, db_name, collection_name, batch_size=100):
    finished_documents = 0
    start_time = time.time()

    client = pymongo.MongoClient(db_uri)
    db = client[db_name]
    collection = db[collection_name]

    total_documents = collection.count_documents({})
    processed_documents = 0

    while processed_documents < total_documents:
        cursor = collection.find().skip(processed_documents).limit(batch_size)

        for doc in cursor:
            text = doc.get("text")
            if text:
                compound_score = analyze_sentiment(text)
                if compound_score is not None:
                    collection.update_one({"_id": doc["_id"]}, {"$set": {"compound_score": compound_score}})
                    print(f"Updated document {doc['_id']} with compound score {compound_score}")
                    finished_documents += 1
                    average_time_min = (time.time() - start_time) / 60
                    docs_per_min = finished_documents / average_time_min
                    print(f"Processed {finished_documents} documents at {docs_per_min:.2f} docs per minute")
        processed_documents += batch_size

if __name__ == "__main__":
    db_uri = "mongodb://localhost:27017/"
    db_name = "DBL_cleaned"
    collection_name = "v1"
    update_sentiment_scores_batch(db_uri, db_name, collection_name)
