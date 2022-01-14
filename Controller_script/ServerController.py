# coding=utf-8
############################################################################################
##
# Copyright (C) 2021-2022 Michele Arena, Antonio Pipitone, Attilio Azzarelli 
##
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
##
# http://www.apache.org/licenses/LICENSE-2.0
##
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
##
############################################################################################ 


from flask import Flask, request, jsonify, Response
from Controller import Controller, IPFS, Hyperledger, Octoprint
import json, threading

controller = Controller(
    Octoprint = Octoprint(),
    IPFS = IPFS(),
    Hyperledger = Hyperledger()
)
app=Flask(__name__)


@app.route('/start', methods = ["POST"])
def slice():
  try:
    #! If I'm already printing stop the call
    if controller.getOcto().isPrinting():
      return Response(json.dumps({"status":"Bad Request","Error" : "Already Printing"}), 400, mimetype="application/json")
    
    #! Get the STL hash from the body request
    stl_hash=request.get_json().get('stl_hash',None)
    if not stl_hash:#! L'hash è settato nel body? Se no errore
      return Response(json.dumps({"status":"Bad Request", "Error": "Missing stl_hash key"}), 400, mimetype="application/json" )

     #! Get the STL hash from the body request
    pieces=request.get_json().get('pieces',None)
    if not stl_hash:#! L'hash è settato nel body? Se no errore
      return Response(json.dumps({"status":"Bad Request", "Error": "Invalid number of pieces to print"}), 400, mimetype="application/json" )
    
    #! Creating the response 
    #! The response will contain the status and acknowledge about the stl_hash sended
    x = threading.Thread(target=controller.start, kwargs=({"hash":stl_hash, "pieces":pieces}))
    x.start()      
    return Response(json.dumps({"status":"start printing","stl_hash" : stl_hash}), 200, mimetype="application/json")
    
  except Exception as e: #! If something should go wrong an error will be returned
    return Response(json.dumps({"status":"Internal Server Error", "Error": str(e)}), 500, mimetype="application/json" )

@app.route("/profile", methods = ["POST, DELETE, GET"])
def profile():
  pass

if __name__=='__main__':
    app.run(host='0.0.0.0', port=9000, debug=True)
