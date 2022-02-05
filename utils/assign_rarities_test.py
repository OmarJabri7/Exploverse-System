import os
import json
import random
from tqdm import tqdm
import numpy as np

rarities = {}
traits_dir = "imgs/layers/"
for traits in os.listdir(traits_dir):
    if "." not in traits:
        rarities[traits.lower()] = {}
        for trait in os.listdir(traits_dir + traits):
            trait_name = trait.split(".")[0]
            print(trait_name)
            rarities[traits.lower()][trait_name.lower()] = np.random.randint(1, 20)

with open("imgs/layers/rarity.json", "w") as outfile:
    json.dump(rarities, outfile)
