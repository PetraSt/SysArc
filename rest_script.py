from flask import Flask

app = Flask(__name__)

@app.route('/temperature')
def temperature():
    # Code to measure temperature and return the result
    return '25.6'  # Example temperature measurement

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

#Time passed from first message to last in: 1.75