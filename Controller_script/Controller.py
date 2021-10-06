import ipfshttpclient
import socket 
import os
import hashlib
import json
import glob
import datetime
from Octoprint.OctoPrint_operations import Octoprint_Op
from test_for_print.test_for_print import Testing
from web3py.contract_printing import smart_contract

class Controller:
    def __init__(self):
        self.__octo=None
        self.testing=None
        self.__host = ''
        self.__port=12345
        self.__dirStl=None
        self.__stop=False
        self.__connection=None
        self.__ipfs=None
        self.__res="None"
        self.__octo=None
        self.__smCntrt=None
        self.__stl_hash=None
        self.__data_hash="None"
        self.__ipfs_path=str(os.path.abspath("ipfs_files/data_file.txt"))
        self.__stl=None



    #THE HASH OF THE STL FILE LOADED ON IPFS SHOULD BE GIVEN BY THE SMART CONTRACT
    #
    #
    def stl_download(self,hash):
        self.__stl_hash=hash
        self.__ipfs=self.ipfs_connect()
        self.__ipfs.get(hash,"stl_dir")
        self.__dirStl=str(os.path.abspath("stl_dir/"+hash))
        files=glob.glob(self.__dirStl+"/*")
        #files=[x for x in os.listdir("/stl_dir")]
        file_path=max(files,key=os.path.getctime)
        spliting=os.path.split(file_path)
        self.__stl=spliting[1]
        self.start_print(file_path)

    
    
    def start_print(self,file_path):
        self.__octo=Octoprint_Op()
        print("Connetto  a Octoprint ...")
        self.__octo.OctoConnect()
        print("OK")
        self.__octo.OctoUpload(file_path)
        print("Eseguo lo slicing del file")
        self.__octo.OctoSlice(self.__stl)
        print("Slicing del file completato")
        
        
        
        #self.testing.timer()
        #self.start()
        #self.testing=Testing()
   
    def get_stl_name(self):
        return self.__stl



    def start(self):
        #TO BE ENABLE IF NOT USING THE OCTOPRINT METHOD
        #
        #
        #self.__ipfs=self.ipfs_connect()
        
        #Enable to test the smart Contract
        self.__smCntrt=smart_contract()
        self.__smCntrt.smart_contract_init()
        #
        #
        self.__smCntrt.printBegin(self.__stl_hash)
        self.__connection=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print("Collego")
        #self.get_connection()
        self.__connection.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.__connection.bind((self.__host,self.__port))
        print("In ascolto")
        self.__connection.listen(1)

        start_time = datetime.datetime.now()
        endtime=start_time+datetime.timedelta(seconds=10)

        while not self.__stop:
        
            (conn,addr)=self.__connection.accept()
            print('Connected by', addr)
            
            while True:
               
                try:
                    
                    if endtime<datetime.datetime.now():
                        print("End of printing")
                        
                        self.__res=self.load_data(f.name)
                        self.__smCntrt.printEnd(self.__res)
                        f.truncate(0)
                        f.close()
                        #info=self.__smCntrt.get_printing_result()
                        #print("Data of printing saved on the smart contract: "+ info)
                        self.__stop=True
                        break

                    f=open(self.__ipfs_path,"a+")
                    data=conn.recv(4096)
                    data_recived=data.decode()
                    
                   
                    if not data: break
                    data_recived=data_recived+ "\n data hash :"+self.__data_hash
                    self.__data_hash=hashlib.md5(json.dumps(data_recived).encode("utf-8")).hexdigest()
                    print(data_recived)
                    print("\n\n")
                    data_recived=data_recived+"\n\n"
                    f.write(data_recived)
                    
                    if(f.tell()>4000):
                            f.write("\n hash_file : "+str(self.__res))
                            self.__res=self.load_data(f.name)
                            print("The Final size is ",f.tell(),"bytes")
                            f.truncate(0)
                            f.close()
                        
                    
                    
                  
                except:
                   f.truncate(0) 
                   f.close()
                   self.stop()
                   print("Error occured")
                   break
                
    def stop(self):

        print("Closing connection")
        if self.__connection:
            
            self.stop=True
            self.__ipfs.close()
            self.__connection.close()
    
    #Test if it works      
    def get_connection(self):
            connection=None
            try:
                connection=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                connection.bind((self.host,self.port))
                return connection
            except:
                print("Error during connection")
            
    
    def ipfs_connect(self):
        client=None
        try:
            client=ipfshttpclient.connect()
            print("Connected to ipfs")
            return client
        except:
            print("Error while connecting to ipfs")
            
    def load_data(self,data):
        data_hash=self.__ipfs.add(data)
        print("data loaded on ipfs succesfully\n")
        print ("L'hash del dato è :"+data_hash['Hash']+'\n')
        return data_hash['Hash']
    
    





       

#controller= Controller()
#controller.start()
