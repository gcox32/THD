import pandas as pd
from urllib.request import urlopen
from bs4 import BeautifulSoup
from datetime import date
from tqdm import tqdm

base = 'https://www.homedepot.com'
storedir = base + '/StoreFinder/storeDirectory'

html = urlopen(storedir)
soup = BeautifulSoup(html, features='lxml')
results = soup.find_all('a', attrs={'class':'stateList__link'})

# remove the repeats
count = round(len(results)/2)
results = results[:count]

statelist = []
urllist = []

for i in results: 
    # convert to string and grab state name
    state = str(i).split('>')[1][:-3]
    statelist.append(state)
    
    # grab state-specific url
    end = str(i).split(' ')[2][6:11]
    end = base + end
    urllist.append(end)

citylist = []
cityurllist = []
longstatelist = []
ziplist = []
storenumlist = []

for state, i in zip(statelist, tqdm(range(len(urllist)))):
    # grab city name and city link
    stateurl = urllist[i]
    try:
        html = urlopen(stateurl)
        soup = BeautifulSoup(html, features='lxml')
        results = soup.find_all('a', attrs={'class':'u__default-link'})
        
        for j in results:
            city = str(j).split('>')[1][:-3]
            # we only want store fronts, not 'San Antonio Rentals' or 'Modesto Home Services'
            if 'Services' in city or 'Rental' in city:
                pass
            else:
                citylist.append(city)

                # parse and create url
                cityurl = str(j).split('"')[3]
                cityurl = base + cityurl
                cityurllist.append(cityurl)

                # parse zipcode
                zipcode = cityurl.split('/')[-2]
                ziplist.append(zipcode)

                # parse store number
                storenum = cityurl.split('/')[-1]
                storenumlist.append(storenum)

                longstatelist.append(state)
    except:
        pass

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

citydf = pd.DataFrame({'State':longstatelist, 
                        'City':citylist, 
                        'Zipcode':ziplist, 
                        'Store Number':storenumlist,
                        'URL':cityurllist,
                        })

for i in tqdm(range(citydf.shape[0])):
    for key, value in dmadict.items():
        if citydf.loc[i, 'State'] in value:
            citydf['DMA'] = key

citydf.to_csv('storeurls.csv', index=False)
