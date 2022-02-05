from psd_tools import PSDImage
from PIL import Image

img_dir = "bronze"

from psd_tools import PSDImage
import os

psd = PSDImage.open(f"imgs/{img_dir}.psd")
for group in psd:
    if group.kind == "group":
        for layer in group:
            layer_image = layer.composite()
            name = layer.name.split("/")[0]
            if not os.path.exists(f"imgs/layers/{group.name}"):
                os.makedirs(f"imgs/layers/{group.name}")
            layer_image.save("imgs/layers/%s/%s.png" % (group.name, name))
