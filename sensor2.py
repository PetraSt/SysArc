import paho.mqtt.client as mqtt
import random

client = mqtt.Client()
client.connect("localhost", 1883, 60)
for x in range(10000):
    client.publish("sensors/energy", str(random.random()*100))
client.disconnect()
