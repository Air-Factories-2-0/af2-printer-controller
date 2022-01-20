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
from Hyperledger.Hyperledger import Hyperledger

import time, glob, os, json


class Controller:
    def __init__(self,Octoprint,IPFS, Hyperledger):
        self.__octo = Octoprint
        self.__ipfs = IPFS
        self.__hyper = Hyperledger

    #! Getter
    def getOcto(self):
        return self.__octo

    def getIPFS(self):
        return self.__ipfs
    
    def getHyper(self):
        return self.__hyper
    
    def slice(self, hash):
        path=self.__ipfs.download(hash,".stl")
        name= path[::-1].split("/")[0][::-1] 
        self.__octo.upload_STL(path+".stl")
        self.__octo.slice_STL(name+".stl")
        return name

    def waitSlicing(self, n_minute, gconame): #! Wait the slicing for n minute
        maxTries = n_minute * 60
        while(True): 
            try:
                data = self.__octo.isSliced(gconame)
                if data: break
                time.sleep(1)
            except:
                maxTries-=1
                if maxTries == 0:
                    break
                print("File not Found")
                time.sleep(1)

    def printFail(self):
        self.__octo.stop_print()

    def deleteDownloaded(self, name):
        self.__ipfs.deleteDownloaded(name)
        self.__octo.delete_model(name)

    def dataCollecting(self, name):
        try:
            print("Start collecting")
            files_sended = {}
            while(self.__octo.isPrinting()):
                print("Searching data")
                path = self.__octo.get_tmp_folder()+name+"*"
                files = glob.glob(path)

                for file in files:
                    if files_sended.get(file,None)==None:
                        hash_img = files_sended[file]=self.__ipfs.upload(file)

                        #!Send hash to hyperledger
                        while True:
                            check = self.__hyper.send_hash(hash_img)
                            if check["received"] and check["hash"] == hash_img: break
                            time.sleep(1)

                        os.remove(file)         #!Remove sended image
                time.sleep(1)
        except Exception:
            self.printFail()

    def start(self, hash, pieces):
        if self.__octo.isPrinting():
            return False
        name = self.slice(hash)
        gconame = name +".gco"
        self.waitSlicing(1, gconame)          #! Wait max 1 minute

        self.__octo.delete_images(name)       #! 1. Clean folder timelapse
        self.__octo.timelapse_start()         #! 2. Enable timelapse
        self.__octo.print_GCO(gconame)        #! 3. Start printing

        self.dataCollecting(name)             #! 4. Start data collection
        self.__octo.delete_images(name)       #! 5. Eventually clean the folder timelapse
        
        self.deleteDownloaded(name)
        print("END PRINT")


if __name__=="__main__":
    controller = Controller(
        Octoprint = Octoprint(),
        IPFS = IPFS(),
        Hyperledger = Hyperledger()
    )
    controller.deleteDownloaded("QmNgpqVt1NPsqMnoef8ijNBgtHDhyK9ZQiJCWCYPQDJD3T")

 