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
from nltk.tag import pos_tag
import re, string

def remove_noise(tweet_tokens, stop_words = ()):
    
    cleaned_tokens = []
    for token, tag in pos_tag(tweet_tokens):
        token = re.sub('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+#]|[!*\(\),]|'\
                       '(?:%[0-9a-fA-F][0-9a-fA-F]))+','', token)
        token = re.sub("(@[A-Za-z0-9_]+)","",token)

        if tag.startswith('NN'):
            pos = 'n'
        elif tag.startswith('VB'):
            pos = 'v'
        else:
            pos = 'a'
        
        # lemmatize tokens
        lemmatizer = WordNetLemmatizer()
        token = lemmatizer.lemmatize(token, pos)

        if len(token) > 0 and token not in string.punctuation and token.lower() not in stop_words:
            cleaned_tokens.append(token.lower())
    
    return cleaned_tokens

def get_all_words(cleand_tokens_list):
    for tokens in cleand_tokens_list:
        for token in tokens:
            yield token

def get_tweets_for_model(cleaned_tokens_list):
    for tweet_tokens in cleaned_tokens_list:
        yield dict([token, True] for token in tweet_tokens)

from nltk.tokenize import word_tokenize
def pipeline(tweet):
    tokens = word_tokenize(tweet)
    cleaned_tokens = remove_noise(tweet)
    cleaned_inputs = dict([token, True] for token in cleaned_tokens)
    return cleaned_inputs

from nltk.sentiment.util import mark_negation, extract_unigram_feats
from nltk.sentiment import SentimentAnalyzer
from nltk.classify import NaiveBayesClassifier
from nltk.sentiment.vader import SentimentIntensityAnalyzer
def addfeatures(cleaned_tokens_list):
    sentim_analyzer = SentimentAnalyzer()
    all_words_neg = sentim_analyzer.all_words([mark_negation(token_list) for token_list in cleaned_tokens_list])
    unigram_feats = sentim_analyzer.unigram_word_feats(all_words_neg, min_freq=4)
    sentim_analyzer.add_feat_extractor(extract_unigram_feats, unigrams=unigram_feats)
