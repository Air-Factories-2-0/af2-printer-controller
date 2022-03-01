from flask import Flask, request, jsonify
from IPFS import IPFS

ipfs = IPFS()
app = Flask(__name__)


@app.route("/asset", methods = ["POST"])
def test():
    body = request.json
    print(body)
    hash_img = body.get("snapshot",None) if body else None

    if hash_img:
        ipfs.download(hash=hash_img, ext=".png")
        print(hash_img)
        return jsonify(
            {
                "received" : True,
                "hash":hash_img    
            }), 200
    return jsonify({"error":"Bad request"}), 400 