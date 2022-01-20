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


import json
from toolz.itertoolz import first
from web3 import Web3
import calendar;
import time;
import os
import base58


class smart_contract:

    def __init__(self):

        self.__host="http://127.0.0.1:7545"
        self.__web3=Web3(Web3.HTTPProvider(self.__host))
        self.__smcAddress="0x4bE1AFA9706854f38c09C92B131C0C65D1b9Df5a"
        #self.account="0xeCb10d26b1A7094152d7A7871c03a0f3A02C0202"
        self.__printer="0x47051D53C0bFdDcE76264a928c21EF6095AA9eca"
        self.__abi=""
        self.__abiPath=str(os.path.abspath(("web3py/build/contracts/designVoting.json")))
        self.__contract=None
        self.__firstbyte=None


    def smart_contract_init(self):
        self.__web3.eth.defaultAccount = self.__web3.eth.accounts[1]  
        print(self.__printer)
        with open(self.__abiPath)as f:
            
            json_data=json.load(f)
            self.__abi=json_data["abi"]
        
        self.__contract=self.__web3.eth.contract(address=self.__smcAddress,abi=self.__abi)
    
    def printBegin(self,design):
        design_bytes32=self.hash_to_bytes32(design)

        tstmp=calendar.timegm(time.gmtime())
        self.__contract.functions.printingBegin(self.__printer,tstmp,design_bytes32).transact()
    
    def printEnd(self,hash_file):
        ipfs_bytes32=self.hash_to_bytes32(hash_file)
        tstmp=calendar.timegm(time.gmtime())
        self.__contract.functions.end_of_printing(self.__printer,tstmp,ipfs_bytes32)
    
        
    
    def get_printing_result(self):
        
        res=self.__contract.functions.get_printingProcess(self.__printer).call()
        return res
    
    

    def hash_to_bytes32(self,hash_val):
        
        b58val=base58.b58decode(hash_val)
        #salvo i 2 bytes
        self.__firstbyte=b58val[0:2]
        b58val=b58val[2:]
        res=b58val.hex()
        return res


    

    def bytes32_to_hash(self,first,bytes32Hash):

        begin=list(first)
        byteshash=list(bytes32Hash)
        res=begin+byteshash
        res=bytes(res)
        res=base58.b58encode(res)
        return res.decode()
