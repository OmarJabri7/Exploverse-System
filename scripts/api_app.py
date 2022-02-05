from flask import Flask, render_template, request, redirect, url_for
from utils.random_gen import run_gen
from utils.reset_all import reset_fn
import threading
from utils.contract_interaction import deploy_contract_fn, hide_fn, reveal_fn, set_base_uri_fn, withdraw_fn

app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        if("mint" in request.form):
            nft_nbr = request.form["nfts_range"]
            return redirect(url_for("mint_explorer", nft_nbr=nft_nbr))
        elif("deploy" in request.form):
            return redirect(url_for("deploy_contract"))
        elif("withdraw" in request.form):
            return redirect(url_for("withdraw"))
        elif('reset' in request.form):
            return redirect(url_for("reset"))
        elif('set_base_uri' in request.form):
            base_uri = request.form["base_uri"]
            return redirect(url_for("set_base_uri", base_uri=base_uri))
        elif('reveal' in request.form):
            request.form["reveal"]
            return redirect(url_for("reveal"))
        elif('hide' in request.form):
            request.form["hide"]
            return redirect(url_for("hide"))

    return render_template("index.html")


@app.route("/reveal", methods=["GET", "POST"])
def reveal():
    reveal_fn()
    return render_template("index.html")


@app.route("/mint_explorer/<nft_nbr>", methods=["GET", "POST"])
def mint_explorer(nft_nbr):
    with open("../contract_address.txt", "r") as f:
        contract_addr = f.read()
    minting_thread = threading.Thread(
        target=run_gen, name="Minting", args=[int(nft_nbr)]
    )
    minting_thread.start()
    return f"Check wallet for minted NFTs of {nft_nbr}"


@app.route("/deploy_contract", methods=["GET", "POST"])
def deploy_contract():
    contract_addr = deploy_contract_fn()
    return render_template("index.html")


@app.route("/withdraw", methods=["GET", "POST"])
def withdraw():
    withdraw_fn()
    return render_template("index.html")


@app.route("/set_base_uri/<base_uri>", methods=["GET", "POST"])
def set_base_uri(base_uri):
    set_base_uri_fn(base_uri)
    return render_template("index.html")


@app.route("/reset", methods=["GET", "POST"])
def reset():
    reset_fn()
    return render_template("index.html")


@app.route("/hide", methods=["GET", "POST"])
def hide():
    hide_fn()
    return render_template("index.html")


def main():
    app.run()


if __name__ == "__main__":
    main()
