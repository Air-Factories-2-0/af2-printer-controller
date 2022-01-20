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


class Octoprint:
    def __init__(self):
        self.__url="http://localhost:5000"
        self.__user='pi'
        self.__client=None
        self.__api_key="E62464E105CE4560A864A000706220EC"
        self.__tmp_folder="/home/pi/.octoprint/timelapse/tmp/"
        self.connect()
   
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
        printing_status=self.__client.printer(exclude="temperature,sd")
        printing_status=printing_status["state"]["flags"]["printing"]
        return printing_status

    def isSliced(self,gconame):
        return self.__client.files_info(location="local", filename= gconame)

    def upload_STL(self,path):
        self.__client.upload(path,location='local',select=False,print=False,userdata=None,path=None)
  
    def slice_STL(self,stlfile):
        self.__client.slice(stlfile,slicer="curalegacy")

    def print_GCO(self,gconame):
        self.__client.select("local/"+gconame,print=True)
        
    def stop_print(self):
        if self.isPrinting():
            self.__client.cancel()
            
    def timelapse_start(self):
        self.__client.change_timelapse_config("zchange")

    def delete_images(self,gconame):
        self.__client.delete_unrendered_timelapse(gconame)

    def connect_printer(self, autoconnect, profile = None):
        self.__client.connect(autoconnect = autoconnect, printer_profile= profile)

    def delete_model(self, name):
        self.__client.delete("local/"+name+".stl")
        self.__client.delete("local/"+name+".gco")
