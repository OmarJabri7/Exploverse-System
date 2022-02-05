from PIL import Image
import os
import json
import numpy as np
import collections


def comb_layers(nft_contents):
    img_dir = "imgs/layers/"

    with open("imgs/layers/ordering.json") as f:
        orders = json.load(f)

    layers_ordered = dict()
    for key, value in nft_contents.items():
        val = value.split("/")[3].split(".")[0]
        order = orders[key.lower()]
        if val in orders:
            order = orders[val.lower()]
        layers_ordered[order] = value
    layers_ordered = collections.OrderedDict(sorted(layers_ordered.items()))
    base = np.zeros([1700, 1700, 3], dtype=np.uint8)
    base = Image.fromarray(base, "RGB").convert("RGBA")
    for key, val in layers_ordered.items():
        if "none" in val:
            next_layer = base
        else:
            next_layer = Image.open(val).convert("RGBA")
        base = Image.alpha_composite(base, next_layer)
    base = base.convert("RGB")
    return base
