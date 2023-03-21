# SysArc

MQTT
pip install paho-mqtt

and also download 
https://mosquitto.org/download/

and run the command 
net start mosquitto

with the windows terminal as admin in teh folder 
c:\Program Files\mosquitto

to find the port the mosquito server is running run the following command
netstat -a (default port should be 1883)

EXAMPLE

TCP    127.0.0.1:1883         LAPTOP-JD70FA7V:0      LISTENING

ZEROMQ vs MQTT
Tested for 1000 messages. In MQTT uncomment the time.sleep() so the mesurements are fair.
MQTT Run:
mqtt_client.js
mqtt_script.py
ZEROMQ:
publish_sub.js
publish_sub.py

MQTT vs REST
Tested for 1000 messages. In MQTT comment out the time.sleep() so the measure is fair.
MQTT Run:
mqtt_client.js
mqtt_script.py
REST Run:
app.js
rest_script.py
Go to browser: localhost:3000/temperature to see the results



