const mqtt = require('mqtt')
const client = mqtt.connect('mqtt://localhost')

client.on('connect', function () {
    client.subscribe('sensors/#', function (err) {
      if (!err) {
        console.log('Connected to MQTT broker and subscribed to sensors/#')
      }
    })
  })
  
  let count = 0
  let start_time = 0
  client.on('message', function (topic, message) {
    if (count == 1){
        start_time = new Date().getTime()
    }
    count++
    if (count === 1000) {
      let end_time = new Date().getTime()
      let elapsed_time = (end_time - start_time) / 1000
      let delivery_rate = count / elapsed_time
      console.log(`Message delivery rate: ${delivery_rate} messages/second`)
      console.log("Time passed from  the first to last message is: " + `${(end_time-start_time)/1000}`)
      console.log(`Received messages count: ${count}`)
    }
  })
