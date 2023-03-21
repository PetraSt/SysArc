import time
import zmq

context = zmq.Context()
socket = context.socket(zmq.PUB)
socket.bind("tcp://*:5555")
# danger: the publish subscribe is nto connected on time and some messeges can be lost without a delay
time.sleep(2)
# Publish 100 messages
for i in range(1000):
    message = f"Message {i}"
    #start_time = time.time()
    socket.send(message.encode())
    #latency = time.time() - start_time
    #print(f"Message {message} published with latency {latency:.6f} seconds")
    time.sleep(0.1)


#time for 1000 messeges is 108.435