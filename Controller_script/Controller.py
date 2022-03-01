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


from Octoprint.OctoPrint import Octoprint
from IPFS.IPFS import IPFS
from Hyperledger.Hyperledger import Hyperledger, body
from Ethereum.SmartContract import Contract

import time, glob, os, json

class PrintInfo:
    def __init__(self):
        pass

class Controller:
    def __init__(self,Octoprint,IPFS, Hyperledger, Contract_AF2):
        self.__octo = Octoprint
        self.__ipfs = IPFS
        self.__hyper = Hyperledger
        self.__contract = Contract_AF2
        self._body = None
        self._wait = 5
        self._percentage = 5

    #! Getter
    def getOcto(self):
        return self.__octo

    def getIPFS(self):
        return self.__ipfs
    
    def getHyper(self):
        return self.__hyper
    #!-----------------------

    
    def sliceSTL(self, hash):
        #!Download The STL from IPFS
        path=self.__ipfs.download(hash,".stl")
        name= path[::-1].split("/")[0][::-1] 

        #!Upload the STL into Octoprint
        self.__octo.upload_STL(path+".stl")

        #!Create the GCODE from the STL
        self.__octo.slice_STL(name+".stl")

        #!Wait untile the GCODE is Created
        if not self.waitSlicing(1, name+".gco"): return False      #! Wait max 1 minute: return False
        
        #!Upload the GCODE on IPFS        
        self._body["gcode"] = self.__ipfs.upload(self.__octo.get_GCO_path(name+".gco"))
        return name


    def waitSlicing(self, n_minute, gconame): #! Wait the slicing for n minute
        maxTries = n_minute * 60
        while(True): 
            try:
                print("Waiting for File")
                data = self.__octo.isSliced(gconame)
                if data: return data
                time.sleep(self._wait)
            except:
                maxTries-=1
                if maxTries == 0:
                    break
                time.sleep(self._wait)
        print("File Not Found")



    def printFail(self,name):
        print("ERRORE")
        self.endPrinting(1)
        self.__octo.set_printing_order(False)
        self.__octo.set_wait_resume(False)



    def clean(self, name):
        self.__ipfs.deleteDownloaded(name)
        self.__octo.cancel()
        self.__octo.delete_model(name)
        self._body = body 


    def startPrinting(self):
        try:
            self.__contract.startTransaction(self.__contract.startPrinting(self._body["orderID"], self._body["design"], self._body["piece"]))
        except:
            pass

    def endPrinting(self,status):
        self.__contract.startTransaction(self.__contract.endPrinting(self._body["orderID"], self._body["piece"], status))


    def dataCollecting(self, name):
        try:
            print("Start collecting")
            currentLayer=0
            totalLayer=0
            step = 0
            checked = set()
            while(self.__octo.isPrinting()):
                time.sleep(self._wait)
                layer_info = self.__octo.get_layer_info()
                currentLayer = layer_info["current"]
                totalLayer = layer_info["total"]
                if currentLayer =="-" or totalLayer== "-":
                    time.sleep(self._wait)
                    print("waiting for layer info")
                    continue

                if step == 0:
                    step = (int(totalLayer) * self._percentage)//100
                    print("Step: ",step)
                else:
                    print("check layer: ", currentLayer, "-", int(currentLayer)%step)
                    if(int(currentLayer)%step==0 and int(currentLayer) not in checked):
                        print("Layer: ", currentLayer)
                        checked.add(int(currentLayer))
                        print("pausing")
                        self.__octo.stop_and_home()
                        time.sleep(self._wait)
                        #!Wait until paused
                        while(not self.__octo.getStatus()["paused"]):
                            time.sleep(self._wait)
            
                        #!Take a pic
                        file = self.__octo.takeSnap()
                        self._body["snapshot"] = self.__ipfs.upload(file)
                        self._body["layer"] = currentLayer

                        
                        #!Send hash to hyperledger
                        self.send_snap_to_Hyperledger()

                        
                        os.remove(file)
                        print("resume")
                        self.__octo.resume()
                time.sleep(self._wait//2)

            
        except Exception as e:
            print(e)
            self.printFail(name)

    def send_snap_to_Hyperledger(self):
        while True:
            check = self.__hyper.send_hash(self._body)
            if check["received"] and check["hash"] == self._body["snapshot"]: break
            time.sleep(self._wait)

    def start(self,orderID, hash,user, pieces):
        self._body = body #!Fresh copy of a template body
        self._body["orderID"] = orderID
        self._body["design"] = hash #!Setting the desing
        self._body["printer"] = self.__contract.public_address
        self._body["player"] = user

        self.__octo.set_printing_order(True)
        self.__octo.set_wait_resume(False)


        name=self.sliceSTL(hash)
        gconame = name+".gco"

        for piece in range(int(pieces)):

            while(self.__octo.get_wait_resume()):
                print("waiting resume")
                time.sleep(self._wait)

            self._body["piece"] = piece+1                 #! Piece currently printing
            print("Printing piece: ",self._body["piece"])
            print("Eth startPrinting")
            self.startPrinting()                  #! 3.0 Contact the Contract to say that the printing is starting
            
            self.__octo.print_GCO(gconame)        #! 3.1 Start printing
            time.sleep(self._wait*2)
            self.dataCollecting(name)       #! 4.0 Start data collection

            print("Eth endPrinting")
            self.endPrinting(2)                    #! 4.1 Contact the Contract to say that the printing is finished
            

            print("END")
            if(not self.__octo.get_automatic()):
                self.__octo.set_wait_resume(True)

            time.sleep(60)
        
        self.clean(name)                      #! Clean env
        self.__octo.set_printing_order(False)
        self.__octo.set_wait_resume(False)




