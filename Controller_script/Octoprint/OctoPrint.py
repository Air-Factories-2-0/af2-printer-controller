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


import octorest
import time
import requests, shutil, time

class Octoprint:
    def __init__(self, url, user, api, auto):
        self.__url= url
        self.__user= user
        self.__client= None
        self.__api_key= api
        self.__local_folder ="/home/pi/.octoprint/uploads/"
        self.__snapshotURL = "http://localhost:9080/?action=snapshot"
        self.__snapshotTemp = "Temp/snap.png"
        self.__automatic = auto
        self.__waitResume = False
        self.__printing_order = False
        self.connect()
   
    
    def get_printing_order(self):
        return self.__printing_order

    def set_printing_order(self,value):
        self.__printing_order = value

    def get_wait_resume(self):
        return self.__waitResume

    def set_wait_resume(self,value):
        self.__waitResume = value

    def set_automatic(self,value):
        self.__automatic = value

    def get_automatic(self):
        return self.__automatic 

    def get_tmp_folder(self):
        return self.__tmp_folder

    def connect(self):
        try :
            self.__client=octorest.OctoRest(url=self.__url,apikey=self.__api_key)
            self.connect_printer(autoconnect=True)
            print("Connected to Octoprint and to printer")
            return self.__client
        except ConnectionError as ex:
            time.sleep(5)

    def isPrinting(self):
        status = self.getStatus()
        return status["printing"] or status["paused"] or status["pausing"]
        

    def getStatus(self):
        printing_status=self.__client.printer(exclude="temperature,sd")
        return printing_status["state"]["flags"]


    def isSliced(self,gconame):
        return self.__client.files_info(location="local", filename= gconame)
    
    def get_GCO_path(self,gconame):
        return self.__local_folder+gconame

    def upload_STL(self,path):
        self.__client.upload(path,location='local',select=False,print=False,userdata=None,path=None)
  
    def slice_STL(self,stlfile):
        self.__client.slice(stlfile,slicer="curalegacy")

    def print_GCO(self,gconame):
        self.__client.select("local/"+gconame,print=True)
        
   
    def connect_printer(self, autoconnect, profile = None):
        self.__client.connect(autoconnect = autoconnect, printer_profile= profile)

    def delete_model(self, name):
        self.__client.delete("local/"+name+".stl")
        self.__client.delete("local/"+name+".gco")

    #!Command
    def stop_and_home(self):
        self.__client.pause()
        
    def resume(self):
        self.__client.resume()

    def cancel(self):
        if self.isPrinting():
            self.__client.cancel()

    #! Profiles
    def getProfiles(self):
        return self.__client.printer_profiles()

    def postProfile(self, profile_data):
        return self.__client.add_printer_profile(profile_data)

    def deleteProfile(self, profile):
        return self.__client.delete_printer_profile(profile)

   #! Slicer Profiles
    def getSlicerProfiles(self):
        return self.__client.slicers()

    def postSlicerProfile(self, profile_data):
        return self.__client.add_slicer_profile(profile_data)

    def deleteSlicerProfile(self, profile):
        return self.__client.delete_slicer_profile(profile)

    #! Printing Layer
    def get_layer_printing(self):
        return self.get_layer_info()["current"]

    def get_layer_info(self):
        return self.__client.get_printing_layer()["layer"]

    def test(self):
        return self.__client.get_printing_layer()

    def get_layer_total(self):
        return self.get_layer_info()["total"]

    def takeSnap(self):
        response = requests.get(self.__snapshotURL, stream=True)
        with open(self.__snapshotTemp, 'wb') as out_file:
            shutil.copyfileobj(response.raw, out_file)
        return self.__snapshotTemp

if __name__=="__main__":
    config={
    "octo_address":"http://localhost:5000",
    "octo_key":"12E22ACF2B5C4F818517A26870864F93",
    "octo_user":"pi",
    }
    octoprint = Octoprint(url=config["octo_address"], user=config["octo_user"], api=config["octo_key"])
    

