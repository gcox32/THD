import numpy as np
import pandas as pd
import requests
import re
import json
from tqdm import tqdm
import os

key = os.getenv('API_KEY')

base = 'http://api.weatherapi.com/v1/'

# weatherapi.com/docs/
# Call limit of 20000 API calls/month

df = pd.read_csv('storeurls.csv')

year, month, day = '2020', '07', '16'

for i in tqdm(range(df.shape[0])):
    zipcode = df.loc[i, 'Zipcode']
    response = requests.get(base + f'history.json?key={key}&q={zipcode}&dt={year}-{month}-{day}')
    data = response.json()

    # parse day from json
    try:
        day = data['forecast']['forecastday'][0]['day']

        df.loc[i, 'mintemp_f'] = day['mintemp_f']
        df.loc[i, 'maxtemp_f'] = day['maxtemp_f']
        df.loc[i, 'avgtemp_f'] = day['avgtemp_f']
        df.loc[i, 'totalprecip_in'] = day['totalprecip_in']
        df.loc[i, 'avghumidity'] = day['avghumidity']
        df.loc[i, 'condition'] = day['condition']['text']
        df.loc[i, 'icon'] = day['condition']['icon']
    except:
        # fill with NaN if no response from GET request
        df.loc[i, 'mintemp_f'] = np.nan
        df.loc[i, 'maxtemp_f'] = np.nan
        df.loc[i, 'avgtemp_f'] = np.nan
        df.loc[i, 'totalprecip_in'] = np.nan
        df.loc[i, 'avghumidity'] = np.nan
        df.loc[i, 'condition'] = np.nan
        df.loc[i, 'icon'] = np.nan

df.dropna(inplace = True)

df.to_csv('fulldata.csv')