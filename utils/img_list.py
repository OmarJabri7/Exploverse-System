import os
import json

img_paths = []
path = "results/"

for img in os.listdir(path):
    if "DS" not in img:
        img_paths.append(path + img)

img_json = dict()
img_json["paths"] = img_paths

with open("img_paths.json", "w") as f:
    json.dump(img_json, f)