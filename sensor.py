import paho.mqtt.client as mqtt
import random

client = mqtt.Client()
client.connect("localhost", 1883, 60)
client.publish("sensors/start", "")
for x in range(10000):
    client.publish("sensors/temperature", str(random.random()*100))
    client.publish("sensors/humidity", str(random.random()*100))
    client.publish("sensors/energy", str(random.random()*100))
    client.publish("sensors/water", str(random.random()*100))
    client.publish("sensors/gas", str(random.random()*100))
client.publish("sensors/stop", "")
client.disconnect()
