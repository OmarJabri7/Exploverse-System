from PIL import Image
import os
import json
import random
from tqdm import tqdm
import numpy as np
from utils.combine_layers import comb_layers
import uuid
import logging
import threading
import time
import tempfile
import os
import json
import subprocess
from utils.update_metadata import update_metadata_files

thread_q = []
IMG_URI = "ipfs://UPDATE/"


def store_data(f):
    def wrapper(*args):
        thread_q.append(f(*args))

    return wrapper


def generate_weights(main, trait, json_file):
    with open(json_file) as f:
        rarities = json.load(f)
        rarity = rarities[main.lower()][trait.lower()]
        weight = 1 / rarity
        return weight


def get_layer(img_dir, rarity_file):
    img_list = []
    main = img_dir.split("/")[2]
    assoc_weights = []
    for img in os.listdir(img_dir):
        img_name = img.split(".")[0]
        assoc_weights.append(generate_weights(main, img_name, rarity_file))
        img_list.append(img)
    return img_list, tuple(assoc_weights)


def get_img_info(img_name, traits, img_uri):
    attributes = []
    meta_data = dict()
    meta_data["name"] = "Diver#" + img_name
    meta_data["description"] = "Explorer"
    meta_data["image"] = img_uri + img_name + ".jpeg"
    for key, val in traits.items():
        with open("imgs/layers/rarity.json") as f:
            rarity = json.load(f)
        trait = {}
        trait["trait_type"] = key
        trait["value"] = val.split("/")[3].split(".")[0].lower()
        attributes.append(trait)
    meta_data["attributes"] = attributes
    return meta_data


@store_data
def generate_nfts(idx):
    main_dir = "imgs/layers/"
    rarity_file = "imgs/layers/rarity.json"
    nft_contents = dict()
    json_urls = []
    unique_ids = []
    tier = ""
    for traits in os.listdir(main_dir):
        if "." not in traits:
            img_list, weight_list = get_layer(
                main_dir + traits + "/", rarity_file)
            trait = random.choices(img_list, weights=weight_list)  # chooses
            img_name = trait[0].split(".")[0]
            nft_contents[traits] = (
                main_dir + str(traits) + "/" + trait[0].replace("€", "")
            )
            trait_type = nft_contents[traits].split("/")[3]
            if "main_body" in trait_type:
                if "silver" in trait_type:
                    tier = "silver"
                elif "gold" in trait_type:
                    tier = "gold"
                elif "bronze" in trait_type:
                    tier = "bronze"
    if tier != "":
        for key, val in nft_contents.items():
            trait_type = val.split("/")[3]
            if "silver" in trait_type:
                nft_contents[key] = val.replace("silver", tier)
            elif "gold" in trait_type:
                nft_contents[key] = val.replace("gold", tier)
            elif "bronze" in trait_type:
                nft_contents[key] = val.replace("bronze", tier)
    img = comb_layers(nft_contents)
    img_dir = "results/"
    img_name = f"{idx}"
    extension = ".jpeg"
    img.save(f"{img_dir + img_name + extension}")  # , quality=90)
    if not os.path.exists("metadata/" + img_name + ".json"):
        meta_data = get_img_info(img_name, nft_contents, IMG_URI)
        with open(f"metadata/{img_name}.json", "w") as outfile:
            json.dump(meta_data, outfile)
    return "", ""


def run_gen(requests=1):
    idx = ""
    with open("counter.txt", "r") as f:
        idx = f.read()
    idx = int(idx)
    start_time = time.time()
    format = "%(asctime)s: %(message)s"
    logging.basicConfig(format=format, level=logging.INFO, datefmt="%H:%M:%S")
    threads = list()
    for index in range(requests):
        logging.info("Main    : create and start thread %d.", index)
        x = threading.Thread(target=generate_nfts, args=(idx,))
        idx += 1
        threads.append(x)
        x.start()

    for index, thread in tqdm(enumerate(threads)):
        logging.info("Main    : before joining thread %d.", index)
        thread.join()
        logging.info("Main    : thread %d done", index)

    thread_data = thread_q
    print("--- %s seconds ---" % (time.time() - start_time))

    with open("counter.txt", "w") as f:
        f.write(str(idx))
    if os.path.exists("results/.DS_Store"):
        os.remove("results/.DS_Store")
    if os.path.exists("metadata/.DS_Store"):
        os.remove("metadata/.DS_Store")

    res_1 = os.popen('pinatapinner/pinatapinner results/ imgs_presale').read()

    res_1_json = json.loads(res_1)

    imgs_hash = res_1_json["IpfsHash"]

    update_metadata_files(imgs_hash)

    _ = os.popen('pinatapinner/pinatapinner metadata/ metadata_presale').read()

    with open("../Exploverse-Mint-App/public/config/config.json", "r") as jsonFile:
        data = json.load(jsonFile)

    data["MAX_SUPPLY"] = str(requests)

    with open("../Exploverse-Mint-App/public/config/config.json", "w") as jsonFile:
        json.dump(data, jsonFile)

    img_paths = []
    path = "results/"

    for img in os.listdir(path):
        if "DS" not in img:
            img_paths.append(path + img)

    img_json = dict()
    img_json["paths"] = img_paths

    with open("img_paths.json", "w") as f:
        json.dump(img_json, f)

    return thread_data


if __name__ == "__main__":

    requests = 10

    run_gen(requests)
