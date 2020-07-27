dmadict = {
    'MW': ['North Dakota', 'South Dakota', 'Nebraska', 'Kansas', 'Minnesota', 'Iowa', 'Missouri',
            'Wisconsin', 'Illinois', 'Indiana', 'Michigan', 'Ohio'],
    'NE': ['Pennsylvania', 'New York', 'Maryland', 'Delaware', 'New Jersey', 'Connecticut', 'Rhode Island',
            'Massachusetts', 'Vermont', 'New Hampshire', 'Maine'],
    'SE': ['West Virginia', 'Kentucky','Virginia', 'Tennessee','North Carolina', 'Arkansas', 'Louisiana',
            'Mississippi', 'Alabama', 'Georgia', 'South Carolina', 'Florida', 'Oklahoma', 'Texas'],
    'W': ['Alaska', 'Washington', 'Oregon', 'California', 'Nevada', 'Hawaii', 'Idaho', 'Utah',
            'Arizona', 'New Mexico', 'Colorado', 'Wyoming', 'Montana'],
    'Territories': ['Guam', 'Puero Rico', 'Virgin Islands']
}

import pandas as pd
from tqdm import tqdm

df = pd.read_csv('fulldata.csv')

for i in tqdm(range(df.shape[0])):
    for key, value in dmadict.items():
        if df.loc[i, 'State'] in value:
            df.loc[i, 'DMA'] = key

df.to_csv('fulldata.csv', index = False)