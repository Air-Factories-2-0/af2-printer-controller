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

import ipfshttpclient, os, glob


class IPFS: 
    address = "/ip4/192.168.1.54/tcp/5001"

    def __init__(self, address = address):
        self.__stl_dir = "STL_Download"
        self.__img_dir = "Image_Download"
        self.__address = address
        self.connect()

    def connect(self): 
        try:
            self.__connection=ipfshttpclient.connect(self.__address)
            print("Connected to ipfs")
            return self.__connection
        except:
            print("Error while connecting to ipfs")
            return False

    def disconnect(self):
        print("Closing connection")
        if self.__connection:
            self.__ipfs.close()

    def upload(self,data):
        data_hash=self.__connection.add(data)
        print("data loaded on ipfs succesfully\n")
        print ("L'hash del dato è :"+data_hash['Hash']+'\n')
        return data_hash['Hash']
    

    def download(self,hash,ext):
        '''
        Download a file from IPFS giving the hash and save it with the specified extension
        @param hash: hash of the file on IPFS
        @param ext: extension of the file 
        
        @return return the path in which the file is saved
        '''
        self.__connection.get(hash, self.__stl_dir)
        path = str(os.path.abspath(f'{self.__stl_dir}/{hash}'))
        newName = path+ext
        os.rename(path, newName)
        return path
   
    def deleteDownloaded(self,name):
        os.remove(f'{self.__stl_dir}/{name}.stl')
        
    def get_stl_dir(self):
        return self.__stl_dir
