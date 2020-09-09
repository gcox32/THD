import os, random
import numpy as np
from src.functions import check_nltk_downloads, remove_noise, get_all_words, get_tweets_for_model

check_nltk_downloads()

from nltk.corpus import twitter_samples, stopwords
stop_words = stopwords.words('english')

from nltk import classify, NaiveBayesClassifier
from nltk.tag import pos_tag
from nltk.tokenize import word_tokenize

if __name__ == "__main__":
    
    print('Loading in data...')
    pos_tokens = twitter_samples.tokenized('positive_tweets.json') #5k tweets
    neg_tokens = twitter_samples.tokenized('negative_tweets.json') #5k tweets
    neutral_tokens = twitter_samples.tokenized('tweets.20150430-223406.json') #20k tweets

    positive_cleaned_tokens_list = []
    negative_cleaned_tokens_list = []
    neutral_cleaned_tokens_list = []

    # remove noise and incorporate normalization and lemmatization
    print('Cleaning data...')
    for tokens in pos_tokens:
        positive_cleaned_tokens_list.append(remove_noise(tokens, stop_words=stop_words))
    for tokens in neg_tokens:
        negative_cleaned_tokens_list.append(remove_noise(tokens, stop_words = stop_words))
    for tokens in neutral_tokens:
        neutral_cleaned_tokens_list.append(remove_noise(tokens, stop_words = stop_words))

    # convert tweets from list of cleaned tokens to dictionary with token:True as key:value
    print('Converting tweets to tokens...')
    pos_tokens_for_model = get_tweets_for_model(positive_cleaned_tokens_list)
    neg_tokens_for_model = get_tweets_for_model(negative_cleaned_tokens_list)

    pos_dataset = [(tweet_dict, "Positive")
                    for tweet_dict in pos_tokens_for_model]
    neg_dataset = [(tweet_dict, "Negative")
                    for tweet_dict in neg_tokens_for_model]

    dataset = pos_dataset + neg_dataset

    random.shuffle(dataset)

    # establish training and testing data (70/30)
    train_data = dataset[:7000]
    test_data = dataset[7000:]

    # simple classifier
    print('Training data...')
    classifier = NaiveBayesClassifier.train(train_data)

    acc = classify.accuracy(classifier, test_data)
    acc = round(acc, 5)

    print(f'Accuracy: {acc}')
    print(classifier.show_most_informative_features(10))


    custom_tweet = "Robinhood is down, yet again. Unreal."

    custom_tokens = remove_noise(word_tokenize(custom_tweet))
    print('-'*10, 'Test Model','-'*10)
    print('Test tweet:',custom_tweet)
    print(classifier.classify(dict([token, True] for token in custom_tokens)))

    # save model for later use with pickle
    import pickle

    filename = 'models/tweetclassifier.sav'
    pickle.dump(classifier, 
                open(filename, 'wb'))