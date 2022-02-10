from flask import Flask, request, jsonify
from IPFS import IPFS

ipfs = IPFS()
ipfs.connect("/ip4/192.168.1.170/tcp/5001")
app = Flask(__name__)


@app.route("/", methods = ["POST"])
def test():
    body = request.json
    hash_img = body.get("hash",None) if body else None

    if hash_img:
        ipfs.download(hash=hash_img, ext=".png")
        print(hash_img)
        return jsonify(
            {
                "received" : True,
                "hash":hash_img    
            }), 200
    return jsonify({"error":"Bad request"}), 400 