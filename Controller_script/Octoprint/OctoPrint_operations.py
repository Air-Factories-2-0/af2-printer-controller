# coding=utf-8
############################################################################################
##
# Copyright (C) 2021-2022 Michele Arena
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


class Octoprint_Op:
    def __init__(self):
        self.__url="http://localhost:5000"
        self.__user='mike'
        self.__client=None
        self.__api_key="4BA88DDCBB2649C5B2B879F1ABDA447C"



    def OctoSlice(self,stlfile):
        self.__client.slice(stlfile,slicer="curalegacy")
    

    def OctoUpload(self,path):

        self.__client.upload(path,location='local',select=False,print=False,userdata=None,path=None)

    
    def OctoConnect(self):
    
    
    
        try :
            self.__client=octorest.OctoRest(url=self.__url,apikey=self.__api_key)
            return self.__client
        except ConnectionError as ex:
            time.sleep(5)
            # print(ex)


    def Octo_do_Print(self,gconame):

        self.__client.select("local/"+gconame,print=True)
        
    
    def Print_status(self):
        
        printing_status=self.__cient.printer(exclude="temperature,sd")
        printing_status=printing_status["state"]["flags"]["printing"]
        return printing_status
