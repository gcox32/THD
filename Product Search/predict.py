import time
start_time = time.time()

import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestRegressor, BaggingRegressor
from nltk.stem.snowball import SnowballStemmer
from sklearn.model_selection import train_test_split
from tqdm import tqdm

stemmer = SnowballStemmer('english')

print('Loading in data...')

print('    train.csv')
df_train = pd.read_csv('input/train.csv', encoding = 'ISO-8859-1')
print('    attributes.csv')
df_attr = pd.read_csv('input/attributes.csv')
print('    product_descriptios.csv')
df_desc = pd.read_csv('input/product_descriptions.csv')

print('Data loaded.')

len_train = df_train.shape[0]

def str_stemmer(s):
    return ' '.join([stemmer.stem(word) for word in s.lower().split()])

def str_common_word(str1, str2):
    return sum(int(str2.find(word)>= 0) for word in str1.split())

print('Merging data...')
df_all = pd.merge(df_train, df_desc, how = 'left', on = 'product_uid')

print('Feature engineering...')
tqdm.pandas()

print('    search_term')
df_all['search_term'] = df_all['search_term'].progress_map(lambda x:str_stemmer(x))
print('    product_title')
df_all['product_title'] = df_all['product_title'].progress_map(lambda x:str_stemmer(x))
print('    product_description')
df_all['product_description'] = df_all['product_description'].progress_map(lambda x:str_stemmer(x))

print('    len_of_query')
df_all['len_of_query'] = df_all['search_term'].map(lambda x:len(x.split())).astype(np.int64)
print('    product_info')
df_all['product_info'] = df_all['search_term']+"\t"+df_all['product_title']+"\t"+df_all['product_description']
print('    word_in_title, word_in_description')
df_all['word_in_title'] = df_all['product_info'].map(lambda x:str_common_word(x.split('\t')[0],x.split('\t')[1]))
df_all['word_in_description'] = df_all['product_info'].map(lambda x:str_common_word(x.split('\t')[0],x.split('\t')[2]))

print('Dropping search_term, product_title, product_description, product_info...')
df_all = df_all.drop(['search_term','product_title','product_description','product_info','product_uid'],axis=1)

print('Dividing into training and testing data...')
target = 'relevance'
y = df_all[target].values
X = df_all.drop(['id', target], axis = 1).values
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.3, random_state = 15)

print('Instantiating Random Forest Regressor...')
rf = RandomForestRegressor(n_estimators=15, max_depth=6, random_state=15)
clf = BaggingRegressor(rf, n_estimators=45, max_samples=0.1, random_state=15)
clf.fit(X_train, y_train)

print('Making predictions...')
y_pred = clf.predict(X_test)

# get RMSE (kaggle success metric)
from sklearn.metrics import mean_squared_error
from math import sqrt

rmse = sqrt(mean_squared_error(y_test, y_pred))
print(f'RMSE for this model: {rmse}')

def prompt():
    print('Save these predictions? (Y/N)')
    answer = input('>> ')
    return answer[0].lower()

submission = 'submission.csv'

answer = None
while answer != 'y' and answer != 'n':
    answer = prompt()
    if answer == 'y':
        pd.DataFrame({"relevance": y_test, "pred_relevance": y_pred}).to_csv(path_or_buf=submission,index=False)
        print(f'Predictions saved as {submission}')
    elif answer == 'n':
        print('Ending script...')
    else:
        print('Respond Y or N')
        pass
        
print("--- Training & Testing: %s minutes ---" % ((time.time() - start_time)/60))


