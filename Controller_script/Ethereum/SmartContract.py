from web3 import Web3
from datetime import datetime
from Ethereum.Utils import setConfig, loadConfig, hash_to_bytes32, getContractAddress
import glob, json, random, string


class Contract:
    def __init__(self, config):
        self.web3 = Web3(Web3.HTTPProvider(config["ethereum_node_address"]))
        self.public_address = config.get("printer_account_address",None)
        self.psw = config.get("printer_account_password",None)
        self.len_psw=32
        
        #! Load all Contracts in ABIs except Migrations
        self.contracts={}
        for path in glob.glob("./Ethereum/ABIs/*.json"):
            if (file_name:=path.split("/")[3].split(".")[0])!="Migrations":
                self.contracts[file_name]=self.web3.eth.contract(address=getContractAddress(path), abi=json.load(open(path))["abi"])
        
    def createWallet(self, config):
        '''Create a new Account and returns it with the private key'''
        self.psw = ''.join(random.choice(string.ascii_letters) for _ in range(self.len_psw))
        self.public_address = self.web3.geth.personal.new_account(self.psw)
        
        setConfig(config, "printer_account_address", self.public_address)
        setConfig(config, "printer_account_password", self.psw)
                
        return self.public_address

    def getPrintingInfo(self, orderID):
        return self.contracts["PrintingProcess"].functions.get_printing_process(orderID.encode("utf-8"), self.public_address).call()
        
    def startPrinting(self, orderID, designHash, piece):
        timestamp = int(round(datetime.now().timestamp()))
        _, designHash = hash_to_bytes32(designHash)
        return self.contracts["PrintingProcess"].functions.start_printing(orderID.encode("utf-8"), self.public_address, designHash, piece, timestamp)
    
    def endPrinting(self, orderID , piece, status):
        timestamp = int(round(datetime.now().timestamp()))
        return self.contracts["PrintingProcess"].functions.end_printing(orderID.encode("utf-8"), self.public_address, piece, timestamp, status)
    
    def getBalance(self):
        return self.web3.eth.get_balance(self.public_address)
    
    def startTransaction(self, tx):
        gas = self.estimateGas(tx)
        if self.getBalance()<gas:
            return False

        self.web3.geth.personal.unlock_account(self.public_address, self.psw,300)
        tx.transact({'from': self.public_address, 'gas':gas})
        self.web3.geth.personal.lock_account(self.public_address)
    
    def estimateGas(self, tx):
        return tx.estimateGas()
    
    def estimateGasComunication(self, orderID, designHash, npieces):
        piece = 0
        cost = self.estimateGas(self.startPrinting(orderID, designHash, piece))
        tot = cost*2
        return tot, tot*npieces



if __name__ == "__main__":
    AirFactories2 = Contract(config)
    print("Printer Wei:" + str(AirFactories2.getBalance()))

    design="QmZ1iQZcQthftfj45Mtx6SYT6PRkF7kZH8Y3pV9pBimpUY"
    orderID="prova"

    print(AirFactories2.getPrintingInfo(orderID))



