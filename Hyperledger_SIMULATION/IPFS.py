import ipfshttpclient
import os
import glob


class IPFS: 

    def __init__(self):
        self.__stl_dir = "STL_Download"
        self.__img_dir = "Image_Download"
        self.__connection=None

    def connect(self, addr): 
        try:
            self.__connection=ipfshttpclient.connect(addr)
            print("Connected to ipfs")
            return self.__connection
        except Exception as e:
            print("Error while connecting to ipfs")
            print(e)
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
        self.__connection.get(hash, self.__stl_dir)
        path=str(os.path.abspath(self.__stl_dir+"/"+hash))
        newName = path+ext
        os.rename(path, newName)
        return path

    def get_stl_dir(self):
        return self.__stl_dir

'''
if __name__ == "__main__":
    
    print("Creo oggetto IPFS")
    ipfs = IPFS()
    print("Cerco di connettermi")
    ipfs.connect()
    print("Connessione riuscita\nCerco di caricare un file")
    hash_data=ipfs.upload("/home/pi/af2-printer-controller/Controller_script/Octoprint/STL/CalibrationCube.stl")
    print("Upload Effettuato correttamente\nProvo a fare il download")
    print(ipfs.download(hash_data))
'''


