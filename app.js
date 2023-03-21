const express = require('express');
const request = require('request');
const app = express();

app.get('/', (req, res) => {
  res.send('Hello World!');
});

app.get('/temperature', (req, res) => {
  // Make a GET request to the Python script running on the IoT device
  const start_time = new Date().getTime()
  let count = 0
  for (let i = 0; i < 1000; i++) {
    request('http://0.0.0.0:5000/temperature', (error, response, body) => {
      if (error) {
        console.error(error);
        res.status(500).send('Error retrieving temperature measurement');
        return;
      } else {
        count++
        //let temperature = parseFloat(body);
        //res.send(`Current temperature measurement: ${temperature}`);
        if (count == 1000){
          const end_time = new Date().getTime()
          const elapsed_time = ((end_time - start_time) / 1000)
          const delivery_rate = count / elapsed_time
          console.log(`Message delivery rate: ${delivery_rate} messages/second`)
          console.log("Time passed from first message to last in: " + `${elapsed_time}`)
          console.log(`Received messages count: ${count}`)
          res.send("Time passed from first message to last in: " + `${elapsed_time}`);
          return;
        }
      }
    });
  }
});

app.listen(3000, () => {
  console.log('Server listening on port 3000');
});
