import nltk
import os

def check_nltk_downloads(basepath = '/Users/administrator/nltk_data/'):

    print('Checking for nltk resources...')

    dir_loc = os.listdir(basepath + 'corpora/')

    if 'twitter_samples.zip' not in dir_loc:
        print('Downloading training data from nltk.corpora')
        nltk.download('twitter_samples')
    if 'wordnet.zip' not in dir_loc:
        print('Downloading wordnet from nltk.corpora')
        nltk.download('wordnet')
    if 'stopwords.zip' not in dir_loc:
        print('Downloading stopwords from nltk.corpora')
        nltk.download('averaged_perceptron_tagger')

    dir_loc = os.listdir(basepath + 'tokenizers/')

    if 'punkt.zip' not in dir_loc:
        print('Downloading tokenizer from nltk.tokenizers')
        nltk.download('punkt')

    print('All nltk resources detected.')

from nltk.stem.wordnet import WordNetLemmatizer

def lemmatize_sentence(tokens):
    """takes tokens and returns root words"""
    lemmatizer = WordNetLemmatizer()
    lemmatized_sentence = []
    for word, tag in pos_tag(tokens):
        if tag.startswith('NN'):
            pos = 'n'
        elif tag.startswith('VB'):
            pos = 'v'
        else:
            pos = 'a'
        lemmatized_sentence.append(lemmatizer.lemmatize(word, pos))
    return lemmatized_sentence

import re, string

def remove_noise(tweet_tokens, stop_words = ()):
    pass