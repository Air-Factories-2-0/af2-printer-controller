import sys
from web3 import Web3
from Ethereum.Utils import loadConfig

config = loadConfig()


if __name__=="__main__":
        eth =  sys.argv[1]
        web3 = Web3(Web3.HTTPProvider(config["host"]))
        
        web3.eth.send_transaction({
            'to': "0xb17d7f6726efeAa68351189f746e8B29Eecba292",
            'from': web3.eth.coinbase,
            'value': web3.toWei(eth, 'ether'),
            'gas': 21000,
            'maxFeePerGas': web3.toWei(250, 'gwei'),
            'maxPriorityFeePerGas': web3.toWei(2, 'gwei'),
        })