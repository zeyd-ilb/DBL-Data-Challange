import torch
from transformers import pipeline, AutoModelForSequenceClassification, AutoTokenizer, AutoConfig
import numpy as np
from scipy.special import softmax


# Preprocess text (username and link placeholders)
def preprocess(text):
    new_text = []
    for t in text.split(" "):
        t = '@user' if t.startswith('@') and len(t) > 1 else t
        t = 'http' if t.startswith('http') else t
        new_text.append(t)
    return " ".join(new_text)


# Function to analyze sentiment of a list of sentences and calculate compound score
def analyze_sentiments(sentences):
    MODEL = "cardiffnlp/twitter-roberta-base-sentiment-latest"
    tokenizer = AutoTokenizer.from_pretrained(MODEL)
    config = AutoConfig.from_pretrained(MODEL)
    model = AutoModelForSequenceClassification.from_pretrained(MODEL)

    for text, tweet_id in sentences:
        processed_text = preprocess(text)
        encoded_input = tokenizer(processed_text, return_tensors='pt')
        output = model(**encoded_input)
        scores = output[0][0].detach().numpy()
        scores = softmax(scores)

        # Print labels and scores
        ranking = np.argsort(scores)
        ranking = ranking[::-1]
        print(f"Tweet ID: {tweet_id}")
        for i in range(scores.shape[0]):
            l = config.id2label[ranking[i]]
            s = scores[ranking[i]]
            print(f"{i + 1}) {l} {np.round(float(s), 4)}")

        # Calculate compound score
        compound_score = calculate_compound_score(scores, config)
        print(f"Compound Score: {compound_score}\n")


# Function to calculate compound score
def calculate_compound_score(scores, config):
    # Assuming config.id2label maps index to labels like {0: 'negative', 1: 'neutral', 2: 'positive'}
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


# Sample sentences to analyze
sentences = [
    (
    "@jimmy_c_10 @British_Airways What has happened to British Airways? It just doesn’t care about its customers anymore- customer service isn’t important to them anymore, what a shame!",
    "1131459491810222080"),
    ("British Airways love a flight change! 10 minutes this time 😂🤦🏽‍♀️ @British_Airways #BA https://t.co/2bv6zcqNy5",
     None),
    (
    "RT @GenovAeroporto: Londra è sempre più vicina. Puoi volare da Genova con Ryanair, British Airways e easyJet, scegliendo il volo più comodo…",
    "1131494814313267200"),
    (
    "British Airways..... Just had a call from customer relations...bad bad experience on the flight..and all they want to offer is avios ??. Awful food awful entertainment..bad service in Club #britishairways #vegetarianfood #FoodTravelChat #Emirates #virginatlantic #Travel #holiday",
    "1131500317999284224"),
    (
    "@hjaytweet Hi, yeah you can add the luggage on later online, as long as it is a British Airways flight and not operated by another oneworld carrier.  If it was with another carrier, you would have to pay for the baggage at the airport at a higher rate.  For the charges, (1/2) Marie",
    "1131508938011217920"),
    (
    "@RoyalFamily Very proud moment for British Airways and our colleagues at Waterside. We're honoured and privileged. Steph",
    "1131528824796196864"),
    (
    "Jo, Penelope and the British Airways crew on the BA573 were awesome this morning. @British_Airways #BA100 https://t.co/voJKIC2nDE",
    "1154475465287118848"),
    ("@British_Airways NEVER NEVER FLY BRITISH AIRWAYS AGAIN. It's a terrible experience with BA.",
     "1154374203795279872"),
    (
    "@CraigBeck @BritishAirwSUCK @British_Airways It's so sad, British Airways was a wonderful thing before Walsh and Cruz got involved.  Talk about destroying a brand..... Apart from the Managers (not that I ever talk to them ) I never hear a good word about the company now",
    None),
    ("@sonamakapoor @British_Airways British Airways is awful I fully agree!", "1136357877709516800"),
    (
    "RT @sejhsnawat: @domjoly @British_Airways British Airways are a disaster. They used to be good but it’s rubbish now.",
    None),
    (
    "@British_Airways I have always had good service with British Airways.. until today. Super disappointed with your staff and the flight cancellation. Reply to my DM please...",
    None),
    ("@British_Airways give me MY REFUND BRITISH AIRWAYS I NEED THAT MONEY TO FEED MY CHILDREN", None),
    (
    "@GOVUK @British_Airways why are British airways making it hard for customers to have a cash refund? Online form only for vouchers and phone lines disconnect you... 7 days in a row now. The CAA rules are clear. You must offer a full refund. Stop messing us about, make it easy!",
    None),
    (
    "Now been waiting 3 and a half months for a refund from British Airways. After being told several times it was being done they promised it would be today at the latest. As usual disappointment @British_Airways your service is appalling and the lies even worse",
    None),
    (
    "Thank you Tom at the check in desk on behalf of British Airways, awesome/speedy customer service. Just what you need before a trek to Singapore @LBIAirport @British_Airways @JadeJones11 #leedsbradfordairport #britishairways",
    None),
    (
    "RT @Imani_Barbarin: Wow...fuck you @British_Airways ... On top of everything else, British Airways’ refund portal is complete bullshit.…",
    None),
    (
    "RT @Atul__Tanna: Can someone from British Airways please reply. When I call up i keep getting disconnected! I just want a refund, shouldnt…",
    None),
    ("@Metal_Head_Mama @British_Airways Basically, british airways special assistance is pretty good tbh", None),
    (
    "@Metal_Head_Mama @British_Airways Apart from a one time mishap, British airways have been really good to me in regards to borrowing a chair (I do have my own wheelchair but havent flown with it yet) and also my autism. They do have a tendency to go direct to the gate and not let you buy food/stop off at all tho",
    None)
]

# Analyze sentiments of the sample sentences
analyze_sentiments(sentences)
