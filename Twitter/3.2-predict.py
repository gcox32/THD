import pandas as pd
from nltk.tokenize import word_tokenize
from tqdm import tqdm
from src.functions import pipeline

# load in classifier with pickle
import pickle

filename = 'models/tweetclassifier.sav'
model = pickle.load(open(filename, 'rb'))

# test classifier with single tweet
singletest = False
if singletest:
    tweet = 'i am very unhappy.'
    test = pipeline(tweet)
    sentiment = model.classify(test)
    print(sentiment)
    raise SystemExit

# test on tweetsdf
dfloc = 'data/tweetsdf.csv'

df = pd.read_csv(dfloc)

sentiment_list = []
for tweet in tqdm(df['text']):
    tokenized = pipeline(tweet)
    sentiment = model.classify(tokenized)
    sentiment_list.append(sentiment)

df['sentiment'] = sentiment_list

df['polarity'] = [1 if i == 'Positive' else -1 for i in df.sentiment]

print(df.describe())