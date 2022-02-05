from brownie import accounts, config, network
from brownie import Explorer
import json


def set_base_uri_fn(base_uri="ipfs://"):
    prefix = "ipfs://"
    dev_acc = accounts.add(config["wallets"]["from_key"])
    explorer = Explorer[len(Explorer) - 1]
    explorer.setBaseURI(prefix + base_uri + "/", {"from": dev_acc})


def reveal_fn():
    dev_acc = accounts.add(config["wallets"]["from_key"])
    explorer = Explorer[len(Explorer) - 1]
    explorer.reveal({"from": dev_acc})


def hide_fn():
    dev_acc = accounts.add(config["wallets"]["from_key"])
    explorer = Explorer[len(Explorer) - 1]
    explorer.hide({"from": dev_acc})


def withdraw_fn():
    dev_acc = accounts.add(config["wallets"]["from_key"])
    explorer = Explorer[len(Explorer) - 1]
    explorer.withdraw({"from": dev_acc})


def set_cost(cost_eth):
    dev_acc = accounts.add(config["wallets"]["from_key"])
    print(f"Account: {dev_acc}")
    print(dev_acc.address)
    print(f"BALANCE: {dev_acc.balance()}")
    print(network.show_active())
    publish_src = False
    explorer = Explorer[len(Explorer) - 1]
    cost_wei = cost_eth*10**18
    explorer.setCost(cost_wei, {"from": dev_acc})
    new_cost = explorer.getCost()

    supply = explorer.totalSupply()

    with open("../Exploverse-Mint-App/public/config/config.json", "r") as jsonFile:
        data = json.load(jsonFile)

    data["DISPLAY_COST"] = str(new_cost/10**18)
    data["INIT_SUPPLY"] = supply

    with open("../Exploverse-Mint-App/public/config/config.json", "w") as jsonFile:
        json.dump(data, jsonFile)

    return explorer


def deploy_contract_fn():
    dev_acc = accounts.add(config["wallets"]["from_key"])
    print(f"Account: {dev_acc}")
    print(dev_acc.address)
    print(f"BALANCE: {dev_acc.balance()}")
    print(network.show_active())
    publish_src = False
    explorer = Explorer.deploy(
        "Explorer",
        "EXP",
        "ipfs://QmeqzaQ2tWDRY6dobNxFbntHXAjZQbwaM66euWKYC346X1/",
        "ipfs://QmZ5SJhjtLkx7y67KkQSs7ixSy9abUbBHcYdSyT3dMMEWd/hidden.json",
        {"from": dev_acc},
        publish_source=publish_src,
    )
    with open("contract_address.txt", "w") as f:
        params = explorer.address
        f.write(params)

    with open("../Exploverse-Mint-App/public/config/config.json", "r") as jsonFile:
        data = json.load(jsonFile)

    data["CONTRACT_ADDRESS"] = str(explorer.address)

    ethscan = f"https://rinkeby.etherscan.io/address/{explorer.address}"

    data["SCAN_LINK"] = ethscan

    with open("../Exploverse-Mint-App/public/config/config.json", "w") as jsonFile:
        json.dump(data, jsonFile)

    return explorer


def main():
    set_cost(0.15)  # TEST ONLY
