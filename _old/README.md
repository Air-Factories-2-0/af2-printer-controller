# Controller

The Controller script is part of the Air factories project, it should be used with the arancino module and interact with a smart contract
for storing information about a print process.
This is a in development component that at the moment can be only used for testing purposes.
 
 
# Prerequisites

Install the truffle suite, from the terminal type

```npm install -g truffle```
 
 For running the Controller is necessary to have and run an image of IPFS and Ganache, so they need to be downloaded from the official sites.
 
 Once the images are downloaded open the terminal and make them executable by typing
 
``` $ chomd +x ipfs..```
 
```$ chmod +x ganache...```
 
 After the images are made executable it is possible to run them.
 
 Load the smart contract on the ganache blockchain by typing on the terminal where the path is the smart contract directory
 
 ```truffle migrate ```
  
  When the smart contract is loaded on the blockchain take the address and update the smart contract address on the Controller section dedicated to web3.
  
  Modify the test-printer script by changing the user address and the printer address with one of the many given by ganache and execute the script to add a user
  and his printer to the smart contract
  
   ```python3 test_printer.py```
 
 Install all the necessary python library used by the Controller, this are <strong><em>octorest</em></strong>, <strong><em>flask</em></strong>, <strong><em>web3py</em></strong> and <strong><em>py-ipfs-http-client</em></strong>; in the terminal type
 
 ```$ pip install octorest```
 
 ```$ pip install ipfshttpclient```
 
 ```$ pip install web3```
 
```$ pip install flask```

You need to have Octoprint installed locally to be able to interact with it and set up the port on the Controller section dedicated to octoprint
 
 # Usage 
 
 First create a simple script that load a directory containing an stl file on IPFS, after that launch the <strong><em>Controller-request</em></strong> script
 this will start a local server waiting for any request at localhost port <strong><em>8000</em></strong>.
 
 On the address-bar from your browser type the following
 
 ```localhost:8000/slice?hash=<the hash of the directory loaded on IPFS>```
 
 This will load the stl file on octoprint and execute the slicing operation; to begin a print operation just type
 
  ```localhost:8000/start```
  
  Once the printing operation is completed  the server will wait for other requests

 
 
 

 
