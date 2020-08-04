import os
from dotenv import load_dotenv
from pathlib import Path
import tweepy
import jsonpickle
import json

# retrieve twitter api credentials
env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)

APIKEY = os.getenv('APIKEY')
SECRET = os.getenv('SECRETKEY')

# establish api connection
auth = tweepy.AppAuthHandler(APIKEY, SECRET)

api = tweepy.API(auth, 
                wait_on_rate_limit=True, 
                wait_on_rate_limit_notify=True, 
                # parser=tweepy.parsers.JSONParser()
                )

if not api:
    print("Can't authenticate :(")
    raise SystemExit(-1)
else:
    print('Success!')

# search
searchQuery = '#homedepot'
maxTweets = 20000
tweetsPerQry = 100
fName = 'tweets.json'

# if results from specific ID onwards are required, set since_id to that ID
# otherwise, default to no lower limit, and go back as far as the API allows
since_id = None

# if results only below a specific ID are, set max_id to that ID
# otherwise default to no upper limit, start from the most recent tweet matching the search query
max_id = 0

tweetCount = 0
print(f'Downloading max {maxTweets} tweets')
with open(fName, 'w') as f:
    end = False
    f.write('{\n')
    i = 1
    while tweetCount < maxTweets:
        try:
            if (max_id <= 0):
                if not since_id:
                    new_tweets = api.search(q = searchQuery, count = tweetsPerQry)
                else:
                    new_tweets = api.search(q = searchQuery, count = tweetsPerQry, since_id = since_id)
            else:
                if not since_id:
                    new_tweets = api.search(q = searchQuery, count = tweetsPerQry, max_id = (max_id - 1))
                else:
                    new_tweets = api.search(q = searchQuery, count = tweetsPerQry, max_id = (max_id - 1), since_id = since_id)
            if not new_tweets:
                print('No more tweets found')
                end = True

            if not end:
                for idx, tweet in enumerate(new_tweets):
                    f.write('"' + str(i)+'":')
                    json.dump(tweet._json, f)
                    i += 1
                    f.write(',\n')
            else:
                f.write('"EOF":"True"\n')
                f.write('}') # end of file
                break

            tweetCount += len(new_tweets)
            print(f'Downloaded {tweetCount} tweets')
            
            max_id = new_tweets[-1].id

        except tweepy.TweepError as e:
            # just exit if any error
            print('Error: '+str(e))
            break

print(f'Downloaded {tweetCount} tweets; saved to {fName}')

