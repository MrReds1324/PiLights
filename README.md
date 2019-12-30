# PiLights

Clone the repository onto the raspberry pi as well as whatever computer you want to use to control the lights

## **Running the Server**

Activate the SPI bus on raspberry pi through
```sudo raspi-config```

Requires bottle and adafruit-ws2801 which can be installed with
```sudo pip3 install adafruit-ws2801``` and ```sudo pip3 install bottle```

Make sure you edit PiLightsServer to have the correct LED count.

Then run the python script with ```python3 <PATH TO DIR>/PiLightsServer.py```

Recommended that you create a .desktop file in the auto start to automcatically start the server on reboot

This can be done with creating a .desktop file in /home/pi/.config/autostart which will look similar to

```
[Desktop Entry]
Type=Application
Name=PiLightServer
Exec=/usr/bin/python3 <PATH TO DIR>/PiLightsServer.py
Terminal=true
Hidden=false
```

## Running the UI

Requires PyAutoGui and PyQt5 which can be installed with ```pip install PyQutoGui``` and ```pip install PyQt5```

Start the server and it will give you the IP to connect to. Edit the config file in the same location as PiLightsClient to have your proper screen resolution, IP, and LED count. The default wait is optional.

Then simply run PiLightsClient.py if you wish to see output to the console (will be responses from the server) or PiLightsClient.pyw if you only want the GUI.
