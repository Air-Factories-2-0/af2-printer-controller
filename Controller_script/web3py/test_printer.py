import json
import web3
from web3 import Web3

url="http://127.0.0.1:7545"
web3_istance=Web3(Web3.HTTPProvider(url))
contract_address="0xc95F10fc75445EE84E5B99c2E7276d7f7A23b87A"
web3_istance.eth.defaultAccount = web3_istance.eth.accounts[1]
#print(web3_istance.eth.defaultAccount)

#We need to get the abi data from the json file in order to call an istance of the smart contract
with open("/home/mike/Scrivania/Controller/Controller_script/web3py/build/contracts/designVoting.json") as f:

    json_data=json.load(f)
    abi=json_data["abi"]
contract_istance=web3_istance.eth.contract(address=contract_address,abi=abi)
account="0xd4DeBBbbC664a97D82786C9486d7350d837ED6D5"



#Registering new player to the smart contract

messageHash=web3_istance.sha3(text=account)
sig = web3_istance.eth.sign(account,messageHash)
messageHash=web3_istance.toHex(messageHash)

contract_istance.functions.addPlayer(messageHash,sig).transact()
res=contract_istance.functions.getPlayerDetails(account).call()
print(res)

#Registering the associated printer

#printer=web3_istance.eth.accounts[1]
printer="0x41b304E62CC7DbEB2A65Cd326Fa45F0EFd581B59"
make=b'printer'
name=b'prova'
contract_istance.functions.addPrinter(printer,make,name,2,2,2,2,24,12,False,False).transact()
#Get the details
#####################

res=contract_istance.functions.getUserPrinters(account).call()
print(res)

