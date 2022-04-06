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
from Controller import Controller, IPFS, Hyperledger, Octoprint, Contract
from Ethereum.Utils import loadConfig, setConfig
import json, threading

    
config = loadConfig()
AirFactories2 = Contract(config)

controller = Controller(
    Octoprint = Octoprint(url=config["octo_address"], user=config["octo_user"], api=config["octo_key"], auto=config["printer_automatic"]),
    IPFS = IPFS(address=config["ipfs_address"]),
    Hyperledger = Hyperledger(address=config["hyperledger_address"]),
    Contract_AF2 = AirFactories2
)
app=Flask(__name__)


@app.route('/printer/start', methods = ["POST"])
def slice():
  try:
    #! If I'm already printing stop the call
    if controller.getOcto().isPrinting() or controller.getOcto().get_printing_order():
      return Response(json.dumps({"status":"Bad Request","Error" : "Already Printing"}), 400, mimetype="application/json")
    
    #! Get the STL hash from the body request
    stl_hash=request.get_json().get('stl_hash',None)
    if not stl_hash:#! L'hash è settato nel body? Se no errore
      return Response(json.dumps({"status":"Bad Request", "Error": "Missing stl_hash key"}), 400, mimetype="application/json" )
     
    #! Get the pieces from the body request
    pieces=request.get_json().get('pieces',None)
    if not pieces:
      return Response(json.dumps({"status":"Bad Request", "Error": "Invalid number of pieces to print"}), 400, mimetype="application/json" )
    
    orderID=request.get_json().get('orderID',None)
    if not orderID:
      return Response(json.dumps({"status":"Bad Request", "Error": "Missing order ID"}), 400, mimetype="application/json" )
    
    user_address=request.get_json().get('user_address',None)
    if not user_address:
      return Response(json.dumps({"status":"Bad Request", "Error": "Missing user address"}), 400, mimetype="application/json" )
    
    minBalance, maxBalance = AirFactories2.estimateGasComunication(orderID,stl_hash,pieces)
    if(AirFactories2.getBalance()<minBalance):
      return Response(json.dumps({"status":"Bad Request", "Error": f'You do not have enough gas to complete the operation, you need {minBalance} for 1 print or {maxBalance} for {pieces} prints'}), 400, mimetype="application/json" )

    #! Creating the response 
    #! The response will contain the status and acknowledge about the stl_hash sended
    x = threading.Thread(target=controller.start, kwargs=({"hash":stl_hash, "pieces":pieces, "orderID": orderID, "user":user_address}))
    x.start()      
    return Response(json.dumps({"status":"start printing","stl_hash" : stl_hash}), 200, mimetype="application/json")
    
  except Exception as e: #! If something should go wrong an error will be returned
    return Response(json.dumps({"status":"Internal Server Error", "Error": str(e)}), 500, mimetype="application/json" )

@app.route("/profile/printer", methods = ["GET", "POST", "DELETE"])
def profile():
  msg = None
  try:
    if request.method == "POST" or request.method=="DELETE":
      profile = request.get_json().get("profile",None)
      if profile is None:
        return Response(json.dumps({"status":"Bad Request", "Error":"You have to specify a profile"}), 400, mimetype="application/json" )
    
    if request.method == "GET":
      msg = controller.getOcto().getProfiles()

    elif request.method == "POST":
      controller.getOcto().postProfile(request.get_json())
      msg = "Profile Added"

    elif request.method == "DELETE":
      controller.getOcto().deleteProfile(profile)
      msg = "Profile Deleted"

    return Response(json.dumps({"msg":msg}), 200, mimetype="application/json" )
  except Exception as e:
    return Response(json.dumps({"status":"Internal Server Error", "Error": str(e)}), 500, mimetype="application/json" )




@app.route("/profile/slicer", methods = ["GET", "POST", "DELETE"])
def profileSlicer():
  msg = None
  try:
    if request.method == "POST" or request.method=="DELETE":
      profile = request.get_json().get("SlicerProfile",None)
      if profile is None:
        return Response(json.dumps({"status":"Bad Request", "Error":"You have to specify a profile"}), 400, mimetype="application/json" )
    
    if request.method == "GET":
      msg = controller.getOcto().getSlicerProfiles()

    elif request.method == "POST":
      controller.getOcto().postSlicerProfile(request.get_json())
      msg = "Profile Added"

    elif request.method == "DELETE":
      controller.getOcto().deleteSlicerProfile(profile)
      msg = "Profile Deleted"

    return Response(json.dumps({"msg":msg}), 200, mimetype="application/json" )
  except Exception as e:
    return Response(json.dumps({"status":"Internal Server Error", "Error": str(e)}), 500, mimetype="application/json" )


@app.route('/printer/createKey',methods=["POST"])
def createKey():
    if addr := config.get("printer_account_address", None):
        return ({"printer_account_address":addr},201)
    pub_address = AirFactories2.createWallet(config)
    return ({"printer_account_address":pub_address},200)


@app.route("/printer/resume", methods=["POST"])
def resume():
  if not controller.getOcto().get_printing_order():
    return Response(json.dumps({"status":"Bad Request","Error" : "Not order printing"}), 400, mimetype="application/json")

  if not controller.getOcto().get_wait_resume():
    return Response(json.dumps({"status":"Bad Request","Error" : "Not waiting for a resume"}), 400, mimetype="application/json")
  
  controller.getOcto().set_wait_resume(False)
  return ({"resume":True},200)

@app.route("/printer/automatic", methods=["POST"])
def automatic():
  if controller.getOcto().isPrinting() or controller.getOcto().get_printing_order():
    return Response(json.dumps({"status":"Bad Request","Error" : "Already Printing"}), 400, mimetype="application/json")
  
  auto=request.get_json().get('automatic',"")
  if auto == "":
    return Response(json.dumps({"status":"Bad Request", "Error": "Missing automatic field"}), 400, mimetype="application/json" )
  setConfig(config,"printer_automatic",auto)
  controller.getOcto().set_automatic(auto)
  return ({"printer_automatic":auto},200)


if __name__=='__main__':
    app.run(host='0.0.0.0', port=9000, debug=True)
  