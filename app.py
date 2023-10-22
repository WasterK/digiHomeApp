from flask import Flask, render_template, jsonify, request_started
import requests
from DB.db_access import store_temp_humidity
import json

app = Flask(__name__)

# Initial bedroom temperature value
bedroom_temperature = "--"

@app.route('/')
def index():
    return render_template('index.html', bedroom_temperature=bedroom_temperature)

@app.route('/get_temperature', methods=['GET'])
def get_temperature():
    global bedroom_temperature

    # Make a GET request to your ESP32 to get the bedroom temperature
    esp32_url = 'http://192.168.1.2/getBedroomTemp'  # Replace with your ESP32's IP address
    response = requests.get(esp32_url)

    if response.status_code == 200:
        responseData = json.loads(response.text)  # Parse the JSON response
        temperature = responseData.get("temperature")
        humidity = responseData.get("humidity")
        
        if temperature is not None and humidity is not None:
            data = {
                "temperature": temperature,
                "humidity": humidity
            }
            store_temp_humidity(data)
        else:
            bedroom_temperature = 'Incomplete data from ESP32'
    elif response.status_code == 500:
        bedroom_temperature = 'Something went wrong'
        return jsonify({'temperature': bedroom_temperature})
    else:
        bedroom_temperature = 'Error fetching temperature'
        return jsonify({'temperature': bedroom_temperature})

    return jsonify(data)

if __name__ == '__main__':
    app.run(debug=True)
