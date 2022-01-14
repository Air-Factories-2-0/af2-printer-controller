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
