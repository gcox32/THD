
# load in classifier with pickle
import pickle

filename = 'models/tweetclassifier.sav'
model = pickle.load(open(filename, 'rb'))
