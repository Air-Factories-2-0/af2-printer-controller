from flask import Flask #!solo ServerController
from Ethereum.SmartContract import Contract
from Ethereum.Utils import loadConfig


#! Da aggiungere al ServerController
app = Flask(__name__)
config= loadConfig()
AirFactories2 = Contract(config)

@app.route('/printer/createKey',methods=["POST"])
def createKey():
    if addr := config.get("printer_public_address", None):
        return ({"printer_public_address":addr},201)
    pub_address = AirFactories2.createWallet(config)
    return ({"printer_public_address":pub_address},200)


if __name__ == "__main__":
    app.run(host = "0.0.0.0", port = 12345, debug=True)
    