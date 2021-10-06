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
