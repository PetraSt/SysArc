const express = require('express')
const bodyParser = require('body-parser')

const app = express()

app.use(bodyParser.json())

let startTime
let count = 0

app.post('/data', (req, res) => {
  // do something with the data, e.g. store it in a database
  count++
  if (count === 1) {
    startTime = Date.now()
  } else if (count === 1000) {
    const endTime = Date.now()
    const totalTime = (endTime - startTime) / 1000
    console.log(`Received 1000 messages in ${totalTime} s`)
    console.log(`Message delivery rate: ${delivery_rate} messages/second`)
  }
  res.status(200).send('Data received')
})

app.listen(3000, () => {
  console.log('Server started on port 3000')
})