# Controller

The Controller script is part of the Air Factories 2.0 project, it should be used with the pi camera in order to interact with the Ethereum SmartContract, IPFS and Hyperledger  for storing information about a print process.

---

## Prerequisites

First of all check your python3 version with:

```bash
python3 --version
```

It should be 3.9.x or newer. 

### OctoPrint

In order to install OctoPrint first you have to setup Python dependencies.

```bash
sudo apt update
sudo apt install python3-pip python3-dev python3-setuptools python3-venv git libyaml-dev build-essential
mkdir OctoPrint && cd OctoPrint
pip install pip --upgrade
pip install octoprint
```

#### Automatic start up

Download the init script files from OctoPrint's repository, move them to their respective folders and make the init script executable:

```bash
wget https://github.com/OctoPrint/OctoPrint/raw/master/scripts/octoprint.service && sudo mv octoprint.service /etc/systemd/system/octoprint.service
```

make sure you have the correct path in `etc/systemd/system/octoprint.service`, it should point to the binary of octoprint. 

This is an example of octoprint.service

```
[Unit]
Description=The snappy web interface for your 3D printer
After=network-online.target
Wants=network-online.target

[Service]
Environment="LC_ALL=C.UTF-8"
Environment="LANG=C.UTF-8"
Type=exec
User=pi
ExecStart=/home/pi/.local/bin/octoprint

[Install]
WantedBy=multi-user.target
```

Now add the script to the autostart with 

```bash
sudo systemctl enable octoprint.service
```

If you have to start|stop|restart OctoPrint deamon:

```bash
sudo service octoprint {start|stop|restart}
```

#### Camera Module

First of all check if your camera is correctly mounted in your raspberry with:

```bash
vcgencmd get_camera
```

If everything is setted up correctly you should see the following response:

```
supported=1 detected=1
```

Now you have to enable your pi camera from raspi-config

```bash
sudo raspi-config
```

You should see a screen like the following, and you have to select "Interface Options"

![](https://github.com/AntonioPipitone/af2-printer-controller/blob/master/Img/1.png)

At this point you will see the following screen, select "Legacy Camera" and enable it:

![](/Users/antoniopipitone/Desktop/Schermata%202022-01-18%20alle%2015.58.32.png)

<img title="" src="file:///Users/antoniopipitone/Desktop/Schermata%202022-01-18%20alle%2015.58.41.png" alt="" width="372" data-align="center">



Eventually reboot your Raspberry.

##### Check Pi Camera

To test if the pi camera is actually working use the following command.

```bash
raspistill -o Desktop/image.jpg
```

It should save a photo taken with the pi camera named image.jpg.

#### Integrate Pi Camera with OctoPrint

First of all install all the dependancies with the following command:

```bash
cd ~
sudo apt install subversion libjpeg62-turbo-dev imagemagick ffmpeg libv4l-dev cmake
git clone https://github.com/jacksonliam/mjpg-streamer.git
cd mjpg-streamer/mjpg-streamer-experimental
export LD_LIBRARY_PATH=.
make
```

At the end of the compilation process you should be able to run ./mjpg_streamer in order to start a webcamera server.

Test it with the following command: 

```bash
./mjpg_streamer -i "./input_uvc.so -y" -o "./output_http.so" 
```

#### Webcam Server Automatic Startup

Download the file webcamDeamon form the repository and modify the following line adding the port in which you want the webcam server to be exposed

webcamDeamon is taken by community.octoprint.org

```bash
    LD_LIBRARY_PATH=. ./mjpg_streamer -o "output_http.so -w ./www -p 8090" -i "$input"
```

In this case we are using port 8090 `-p 8090`

Set the file as executable with:

```bash
chmod +x ./webcamDaemon
```

Then create the a file in /etc/systemd/system/ named webcamd.service

```bash
sudo nano /etc/systemd/system/webcamd.service
```

Add the following lines:

```
[Unit]
Description=Camera streamer for OctoPrint
After=network-online.target OctoPrint.service
Wants=network-online.target

[Service]
Type=simple
User=pi
ExecStart=/home/pi/scripts/webcamDaemon

[Install]
WantedBy=multi-user.target
```

Now to the system should read the new service file created.

Then we can enable the service so it should automatically start on the next boot

```bash
sudo systemctl daemon-reload
sudo systemctl enable webcamd
```

#### OctoPrint Timelapse

Go to the User Interface of OctoPrint, it should be in `http://localhost:5000/`.

In this page go to settings:

![](/Users/antoniopipitone/Desktop/Schermata%202022-01-18%20alle%2016.51.01.png)

First click on Webcam & Timelapse (1) and set Stream URL(2) to your webcam server address specify the action `stream`

```
#Example
http://192.168.1.171:8090/?action=stream
```

![](/Users/antoniopipitone/Desktop/Schermata%202022-01-18%20alle%2017.25.35.png)

Clicking on Test you should see a live video of your webcam.

- ###### Disable Auto Rendering
  
  In our case we do not want to create a rendered timelapse of our printing process we just need the timelapse functionality in order to take a snapshot each N layers printed.
  
  The number of layers is specified by the UI.
  
  Go to `/home/pi/.local/lib/python3.9/site-packages/octoprint` and open the file `timelapse.py` and change set the default argument `do_create_movie=False` in the `stop_timelapse` function.

##### CuraEngine Slicer

Go to the setting panel of OctoPrint and click on Plugin Manager, search for CuraEngine Legacy (1.1.2) and install the plugin.

![](/Users/antoniopipitone/Desktop/Schermata%202022-01-18%20alle%2017.43.06.png)

Now you can add .STL File on OctoPrint and make a slicing. 
But you have to load your slicing profile.

### IPFS

In order to install IPFS on an ARM device we need different installer than the one that is  provided by IPFS. We used ipfs-rpi from mitchallen

```bash
git clone https://github.com/mitchallen/ipfs-rpi.git
```

To run the installation simply open the folder and run the install file

```bash
cd ipfs-rpi/
./install
```

To check if IPFS is working run the following command:

```bash
ipfs swarm peers
```

You should see a list of peers on the screen.

### Truffle & Ganache

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



#### Controller Script Dependancies

Install all the python dependancies that are needed in order to run the ServerController script:

```bash
pip install octorest, ipfshttpclient==0.8.0a2, web3, flask, requests
```



#### Octoprint API Key

In order to communicate with OctoPrint you have to modify the ServerController script adding your API KEY created via OctoPrint.

To create an API KEY go to the User Interface of OctoPrint and open the Setting pannel as we saw before

Then click on Application Keys

![](/Users/antoniopipitone/Desktop/Schermata%202022-01-18%20alle%2016.51.59.png)

To create a new API Key select an user, give an Application Identifier and click on Generate

![](/Users/antoniopipitone/Desktop/Schermata%202022-01-18%20alle%2016.52.47.png)

Now go into the ServerController script and use the generated API KEY as the argument `api` in the OctoPrint constructor.

```py
controller = Controller(
    SmartContract = SmartContract_AF2()
    Octoprint = Octoprint(api="Your KEY", user="pi", url="http://localhost:5000"),
    IPFS = IPFS(),
    Hyperledger = Hyperledger()
)
```

You can specify as well the user and the url of OctoPrint.

---

## Usage

To start the server use the following command 

```bash
python3 ServerController.py
```

It will automatically connect to OctoPrint and IPFS and will print the url in which the server is avaiable.

These are API you can use:

---

| API    | METHODS | BODY                    |
| ------ |:-------:|:----------------------- |
| /start | [POST]  | { "stl_hash" : "hash "} |

#### /start Description

From an .STL hash on IPFS create the GCODE and start printing it. 

The controller send the snapshot taken at each N layers printed to the Hyperledger ChainCode to valide the printing process, and contact the SmartContract on Ethereum just to say the start timestamp and the end timestamp

---

| API              | METHODS             | BODY                           |
| ---------------- | ------------------- | ------------------------------ |
| /profile/printer | [GET, POST, DELETE] | {"profile": "profile in JSON"} |

#### /profile GET - Description

Return all the printer profile stored in OctoPrint

#### /profile POST - Description

Add a new printer profile in Octoprint

#### /profile DELETE - Description

Delete a printer profile in Octoprint

---


