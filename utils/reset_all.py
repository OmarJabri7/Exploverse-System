import os

def reset_fn():

    imgs_dir = "results/"
    metadata_dir = "metadata/"

    with open("counter.txt", "w") as f:
        f.write("0")
    for imgs in os.listdir(imgs_dir):
        os.remove(imgs_dir + imgs)

    for metadata in os.listdir(metadata_dir):
        os.remove(metadata_dir + metadata)

# reset()