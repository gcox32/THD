import json
import pandas as pd
import nltk
from collections import Counter
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator
import random
import matplotlib.pyplot as plt

# load in json data
file_loc = 'tweets.json'
with open(file_loc, 'r') as f:
    data = json.load(f)
f.close()
data.pop('EOF')

# retrieve tweet text and date
text_list = []
date_list = []

for k in data.keys():
    date = data[k]['created_at']
    text = data[k]['text']
    date_list.append(date)
    text_list.append(text)

df = pd.DataFrame({'created_at':date_list, 
                    'text':text_list, 
                    'sentiment':0.0, 
                    'subjectivity':0.0,
                    'polarity':0.0,})

stopwords = nltk.corpus.stopwords.words('english')

# IMPORTANT: add search text specific language to filter out (variations on search terms that are unhelpful)
stopwords = stopwords + ['homedepot','@homedepot','amp;','home depot','depot',]

RE_stopwords = r'\b(?:{})\b'.format('|'.join(stopwords))
replacements = [r'\u2026',r'\#',r'\|',r'\&',r'\-',r'\.',r'\,',r'\'',r'\@','amp;',RE_stopwords]
subs = ['']*len(replacements)
words = (df.text
           .str.lower()
           .replace(replacements, subs, regex=True)
           .str.cat(sep=' ')
           .split()
)

# generate df out of Counter
topwords = pd.DataFrame(Counter(words).most_common(25),
                        columns=['word', 'frequency'])

# generate and display word cloud
wordcloud = WordCloud(max_font_size=60, max_words=100, width=480, height=380,colormap="brg",
                      background_color="white").generate(' '.join(topwords['word']))

plt.imshow(wordcloud, interpolation='bilinear')
plt.axis("off")
plt.figure(figsize=[10,10])
plt.show()