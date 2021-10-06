import time 



class Testing:
    def __init__(self):
        
        self.stop=None

    def timer(self):
        self.stop=False
        time.sleep(20)
        self.stop=True

