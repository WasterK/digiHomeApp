from flask import Flask, render_template, jsonify, request_started, request
import requests
from DB.db_access import DatabaseAccess
import json

app = Flask(__name__)

# Initial bedroom temperature value
bedroom_temperature = "--"

@app.route('/')
def index():
    return render_template('index.html', bedroom_temperature=bedroom_temperature)

@app.route('/upload_logs', methods=['POST'])
def upload_logs():
    try:
        # Get data from the POST request
        data = request.get_json()

        deviceID = data.get('deviceID')

        # Extract log_data and additional_info from the received data
        db = DatabaseAccess()
        db.upload_logs(dict(data))

        # Send a response back to the client
        response = {
            'status': 'success',
            'message': 'Logs received successfully',
            "deviceID": str(deviceID)
        }
        return jsonify(response)

    except Exception as e:
        # Handle any exceptions that may occur during processing
        response = {
            'status': 'error',
            'message': f'Error processing logs: {str(e)}'
        }
        return jsonify(response), 500 


@app.route('/get_temperature', methods=['GET'])
def get_temperature():
    global bedroom_temperature
    db = DatabaseAccess() 
    db.upload_logs({"log1": "test msg 1", "log2": "test msg 2", "deviceID": "ENGR012002"})
    # Make a GET request to your ESP32 to get the bedroom temperature
    esp32_url = 'http://192.168.187.238/getBedroomTemp'  # Replace with your ESP32's IP address
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
            db.store_temp_humidity(data)
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
