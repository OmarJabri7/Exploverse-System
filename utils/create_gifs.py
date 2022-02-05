# import imageio
# import os
# images = []
# for filename in os.listdir("results/"):
#     images.append(imageio.imread("results/" + filename))
# imageio.mimsave('web_app/public/config/images/explorer.gif', images)

import glob
from PIL import Image

# filepaths
fp_in = "imgs_4_gif/*.jpeg"
fp_out = "web_app/public/config/images/explorer.gif"

# https://pillow.readthedocs.io/en/stable/handbook/image-file-formats.html#gif
img, *imgs = [Image.open(f) for f in sorted(glob.glob(fp_in))]

# print([Image.open(f) for f in sorted(glob.glob(fp_in))])
img.save(fp=fp_out, format='GIF', append_images=imgs,
         save_all=True, duration=500, loop=0)