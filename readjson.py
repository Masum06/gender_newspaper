import json

with open('output/result.json') as json_data:
    d = json.load(json_data)
    print(len(d))
json_data.close()