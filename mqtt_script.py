import paho.mqtt.client as mqtt
import random
import time

client = mqtt.Client()
client.connect("localhost", 1883, 60)
#time.sleep(2)
for x in range(250):
    client.publish("sensors/temperature", str(random.random()*100))
    #time.sleep(0.1)
    client.publish("sensors/humidity", str(random.random()*100))
    #time.sleep(0.1)
    client.publish("sensors/water", str(random.random()*100))
    #time.sleep(0.1)
    client.publish("sensors/gas", str(random.random()*100))
    #time.sleep(0.1)
client.disconnect()

#mqtt with zeromq
#time for 1000 messeges is 108.385

#mqtt with rest_script
#Time passed from  the first to last message is: 0.048