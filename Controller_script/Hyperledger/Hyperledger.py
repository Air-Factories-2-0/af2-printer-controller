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



import requests
import json

body = {
    "orderID":"",
    "printer":"",     #!Printer Address
    "design":"",      #!hashDesign 1
    "gcode":"",       #!Carica gcode su IPFS 2
    "snapshot":"",    #!Carica snapshot su IPFS
    "piece":0,        #!Numero del pezzo
    "player":"" ,      #!Address player  
    "layer":""  
}

class Hyperledger:

    
    def __init__(self, address):
        self.__address = address
        self.__post_api = "/asset"

    def send_hash(self, data):
        if data == None: raise Exception
        r = requests.post(self.__address+self.__post_api, json =data)
        r = json.loads(r.content.decode("utf-8"))
        return r

