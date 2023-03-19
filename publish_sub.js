const zmq = require('zeromq')
const subscriber = zmq.socket('sub')

subscriber.connect('tcp://localhost:5555')
subscriber.subscribe('')

let count = 0
let start_time = new Date().getTime()

subscriber.on('message', function(message) {
  count = count + 1
  console.log(message)
  console.log(`Received message ${count} with size ${message.byteLength} bytes`)
  if (count === 50) {
    let end_time = new Date().getTime()
    let elapsed_time = (end_time - start_time) / 1000
    let delivery_rate = count / elapsed_time
    console.log(`Message delivery rate: ${delivery_rate} messages/second`)
    console.log("Time passed: " + `${(end_time-start_time)/1000}`)
    subscriber.close()
  }
})
