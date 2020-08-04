import json
import ast

file_loc = 'tweets.json'

with open(file_loc, 'r') as f:
    data = json.load(f)

f.close()

data.pop('EOF')

print(len(data))
