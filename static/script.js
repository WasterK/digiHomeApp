// JavaScript code to fetch and update temperature
function updateTemperature() {
    fetch('/get_temperature')
        .then(response => response.json())
        .then(data => {
            const temperatureElement = document.getElementById('bedroom-temp');
            const humidityElement = document.getElementById('bedroom-humidity');
            
            // Round temperature and humidity values to 2 decimal places
            const roundedTemperature = Math.round(data.temperature * 100) / 100;
            const roundedHumidity = Math.round(data.humidity * 100) / 100;
            
            temperatureElement.textContent = roundedTemperature;
            humidityElement.textContent = roundedHumidity;
        })
        .catch(error => {
            console.error('Error fetching temperature & humidity: ', error);
        });
}

// Update temperature initially and every 5 seconds
updateTemperature();
setInterval(updateTemperature, 60000); // Update every 5 seconds

// Add event listener for the refresh button
const refreshButton = document.getElementById('refresh-button');
refreshButton.addEventListener('click', () => {
    updateTemperature();
});

document.addEventListener('DOMContentLoaded', function () {
    const addRoomButton = document.getElementById('add-room-button');
    const roomContainer = document.getElementById('room-container');

    addRoomButton.addEventListener('click', function () {
        // Create a new sensor div for the room
        const newSensor = document.createElement('div');
        newSensor.classList.add('sensor');

        // Create room-specific elements
        const roomName = prompt('Enter room name:');
        const roomTitle = document.createElement('h2');
        roomTitle.textContent = roomName;

        const roomTemp = document.createElement('p');
        roomTemp.innerHTML = `Temperature: <span id="${roomName.toLowerCase()}-temp">-- °C</span>`;

        const roomHumidity = document.createElement('p');
        roomHumidity.innerHTML = `Humidity: <span id="${roomName.toLowerCase()}-humidity">-- %</span>`;

        // Append elements to the new sensor div
        newSensor.appendChild(roomTitle);
        newSensor.appendChild(roomTemp);
        newSensor.appendChild(roomHumidity);

        // Append the new sensor div to the room container
        roomContainer.appendChild(newSensor);
    });

    // Add code to refresh data for the new rooms here
});