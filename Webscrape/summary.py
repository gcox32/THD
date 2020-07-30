import pandas as pd
import numpy as np
import requests
import re
import json
import os
from dotenv import load_dotenv

load_dotenv(dotenv_path='.env')
key = os.getenv('API_KEY')

df = pd.read_csv('fulldata.csv')

# # weatherapi.com/docs/
# # Call limit of 20000 API calls/month
# base = 'http://api.weatherapi.com/v1/'
# zipcode = '29910'
# year, month, day = '2020', '07', '28'
# response = requests.get(base + f'history.json?key={key}&q={zipcode}&dt={year}-{month}-{day}')
# data = response.json()
# print(data['forecast']['forecastday'][0]['day'])

print(df.describe())
