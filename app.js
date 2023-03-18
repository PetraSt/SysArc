const express = require('express')
const mqtt = require('mqtt')

const app = express()
const client = mqtt.connect('mqtt://localhost')

client.on('connect', function () {
  client.subscribe('sensors/#', function (err) {
    if (!err) {
      console.log('Connected to MQTT broker and subscribed to sensors/#')
    }
  })
})

let start = "";
let stop = "";
client.on('message', function (topic, message) {
  if (topic.includes("start")){
    start = Date.now();
    console.log('Time starts now:' + `${start}`);
  } else if (topic.includes("stop")) {
    stop = Date.now();
    console.log('Time stops now: ' + `${stop}`);
    console.log('Time elapsed in miliseconds: ' + `${stop-start}`);
    console.log('Time elapsed in seonds: ' + `${(stop-start)/1000}`);
  } else {
    console.log(topic + ': ' + message.toString())
  }
})

app.get('/', (req, res) => {
  res.send("Time passed: " + `${(stop-start)/1000}`);
})

app.listen(3000, () => {
  console.log('Express server listening on port 3000')
})