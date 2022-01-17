import json
import os

def WriteToJsonFile(key, value):
    jsonFile = "config.json"
    if (os.path.getsize(jsonFile) == 0):
        data = {key:value}
        with open(jsonFile, 'w') as json_file:
            json.dump(data, json_file)
        return

    with open(jsonFile) as json_file:
        json_decoded = json.load(json_file)

    json_decoded[key] = value

    with open(jsonFile, 'w') as json_file:
        json.dump(json_decoded, json_file)