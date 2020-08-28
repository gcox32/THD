import os
import numpy as np
import pandas as pd
import nltk
from src.functions import check_nltk_downloads, lemmatize_sentence

check_nltk_downloads()

from nltk.corpus import twitter_samples
from nltk.tag import pos_tag

pos_tweets = twitter_samples.strings('positive_tweets.json') #5k tweets
neg_tweets = twitter_samples.strings('negative_tweets.json') #5k tweets
text = twitter_samples.strings('tweets.20150430-223406.json') #20k tweets

tweet_tokens = twitter_samples.tokenized('positive_tweets.json')

df = pd.read_csv('tweetsdf.csv')

from nltk.tokenize import TweetTokenizer
tweet_tokenizer = TweetTokenizer(preserve_case=False, strip_handles=True, reduce_len=True)

print(tweet_tokenizer.tokenize(df['text'][0]))