from flask import Flask
from flask import request
from Controller import Controller

controller=Controller()
app=Flask(__name__)

@app.route('/slice')

def slice():

    stl_name=request.args.get('hash')
    controller.stl_download(stl_name)
    stl=controller.get_stl_name()

   
    return '''<h1>The stl file {} has been sliced</h1>
    <h3>hash:{}</h3>'''.format(stl,stl_name)
    
@app.route('/start')

def start():
  controller.start()
  return '''<h3>The print process has ended</h1>'''



if __name__=='__main__':
    app.run(host='127.0.0.1', port=8000)



 
''' 
app = Flask(__name__)
@app.route("/")
def hello():
  return "Hello World!"

if __name__ == "__main__":
  app.run()
  '''