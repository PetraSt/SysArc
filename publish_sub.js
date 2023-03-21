const zmq = require('zeromq')
const subscriber = zmq.socket('sub')

subscriber.connect('tcp://localhost:5555')
subscriber.subscribe('')

let count = 0
let start_time = 0

subscriber.on('message', function(message) {
  count++
  if (count == 1) {
    start_time = new Date().getTime()
  }
  if (count === 1000) {
    let end_time = new Date().getTime()
    let elapsed_time = ((end_time - start_time) / 1000)
    let delivery_rate = count / elapsed_time
    console.log(`Message delivery rate: ${delivery_rate} messages/second`)
    console.log("Time passed from first message to last in: " + `${elapsed_time}`)
    console.log(`Received messages count: ${count}`)
    subscriber.close()
  }
})
