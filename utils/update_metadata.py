import os
import json

def update_metadata_files(IMG_URI):

    path = "metadata/"

    for metadata_json in os.listdir(path):
        with open(path + metadata_json, "r") as f:
            data = json.load(f)
            data["image"] = data["image"].replace("UPDATE", IMG_URI)
        with open(path + metadata_json, 'w', encoding='utf-8') as updated_json:
            json.dump(data, updated_json)