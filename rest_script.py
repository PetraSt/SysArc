import requests
import json

sensor_id = 'sensor_1'

for i in range(1000):
    value = 20 + i/10
    data = {
        'sensor_id': sensor_id,
        'value': value
    }
    headers = {
        'Content-type': 'application/json'
    }
    response = requests.post('http://localhost:3000/data', data=json.dumps(data), headers=headers)