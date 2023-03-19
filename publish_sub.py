import time
import zmq

context = zmq.Context()
socket = context.socket(zmq.PUB)
socket.bind("tcp://*:5555")

# Publish 100 messages
for i in range(50):
    message = f"Message {i}"
    start_time = time.time()
    socket.send(message.encode())
    latency = time.time() - start_time
    print(f"Message {message} published with latency {latency:.6f} seconds")
    time.sleep(1)
