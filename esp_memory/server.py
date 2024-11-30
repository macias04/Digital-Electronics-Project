"""
This module implements a simple web server for an ESP32 microcontroller that serves sensor data 
for an indoor gardening application. It connects to a specified Wi-Fi network and listens for 
incoming client connections. The server responds to requests for sensor data in JSON format 
and serves an HTML page with a chart displaying the data.

MIT License: This module is open source and can be freely used, modified, and distributed.

Classes:
    - Server: Manages Wi-Fi connection and serves sensor data over HTTP.

Usage:
    1. Set the SSID and PASSWORD variables with the Wi-Fi credentials.
    2. Create an instance of the Server class with the sensor data.
    3. The server will automatically connect to Wi-Fi and start listening for requests.

Example:
    sensor_data = {
        'temp': 25,
        'humid': 60,
        'light': 300,
        'soil': 40
    }
    server = Server(sensor_data)
"""



import network
import socket
import time

SSID = ''
PASSWORD = ''

class Server:
    
    def __init__(self, sensor_data):
        self.sensor_data = sensor_data 
        self.sock = socket.socket()
        self.cl = None 
        self.addr = socket.getaddrinfo('0.0.0.0', 80)[0][4]
        self.ip_address = self.connect_wifi()
        self.web_server()
    

    def connect_wifi(self):
        """
    Connects the ESP32 to a specified Wi-Fi network.

    This method activates the WLAN interface, connects to the Wi-Fi using the provided SSID and password,
    and waits for the connection to be established. It retrieves and stores the assigned IP address in
    `self.ip_address`, which is also printed to the console.

    Returns:
        str: The IP address assigned to the ESP32 after a successful connection.

    Example:
        Ensure that SSID and PASSWORD are defined with the correct Wi-Fi credentials before calling this method.
    """

        wlan = network.WLAN(network.STA_IF)
        wlan.active(False)  
        time.sleep(1)       
        wlan.active(True)   
        wlan.connect(SSID, PASSWORD)

        
        while not wlan.isconnected():
            print("Connecting to WiFi...")
            time.sleep(1)

        print("Connected to WiFi")
        self.ip_address = wlan.ifconfig()[0]  
        print("IP Address:", self.ip_address)
        return self.ip_address

    def web_server(self):
        """
    Starts a simple web server that listens for incoming client connections and serves sensor data.

    This method binds the server socket to the specified address and listens for incoming connections.
    When a client connects, it accepts the connection and processes the incoming request. If the request
    is for sensor data (i.e., a GET request to "/data"), it responds with a JSON object containing the
    current temperature, humidity, light, and soil moisture values. For any other request, it serves
    an HTML page that includes a chart displaying the sensor data.

    The server runs indefinitely, handling one client connection at a time. It prints connection details
    and the received request to the console for debugging purposes.

    Attributes:
        self.sock (socket.socket): The socket object used for the server.
        self.addr (tuple): The address (host, port) to which the server is bound.
        self.sensor_data (dict): A dictionary containing sensor readings with keys 'temp', 'humid',
                                 'light', and 'soil'.

    Exceptions:
        Catches and prints any exceptions that occur during the server operation. Ensures that the
        client socket and server socket are closed properly in case of an error or when the server stops.

    Example:
        To use this method, ensure that the server socket is initialized and the sensor_data attribute
        is populated with the latest sensor readings before calling this method.
    """
        try:
            self.sock.bind(self.addr)
            self.sock.listen(5)
            print('Listening on', self.addr)

            while True:
                self.cl, self.addr = self.sock.accept()
                print('Client connected from', self.addr)
                request = self.cl.recv(1024).decode('utf-8')
                print(f"Request: {request}")

                
                temperature = self.sensor_data['temp']
                humidity = self.sensor_data['humid']
                light = self.sensor_data['light']
                soil_moisture_val = self.sensor_data['soil']

                if "GET /data" in request:
                    response = f"""HTTP/1.0 200 OK\r\nContent-Type: application/json\r\n\r\n{{
                        "temperature": {temperature},
                        "humidity": {humidity},
                        "light": {light},
                        "soil_moisture": {soil_moisture_val}
                    }}"""
                else:
                    response = """HTTP/1.0 200 OK\r\nContent-Type: text/html\r\n\r\n
                    <!DOCTYPE html>
                    <html>
                    <head>
                        <title>ESP32 Sensor Data</title>
                        <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
                    </head>
                    <body>
                        <h1>Sensor Data</h1>
                        <canvas id="myChart" width="400" height="200"></canvas>
                        <script>
                            async function fetchData() {
                                const response = await fetch('/data');
                                const data = await response.json();
                                return data;
                            }

                            async function updateChart(chart) {
                                const data = await fetchData();
                                chart.data.datasets[0].data = [
                                    data.temperature,
                                    data.humidity,
                                    data.light,
                                    data.soil_moisture
                                ];
                                chart.update();
                            }

                            const ctx = document.getElementById('myChart').getContext('2d');
                            const myChart = new Chart(ctx, {
                                type: 'bar',
                                data: {
                                    labels: ['Temperature', 'Humidity', 'Light', 'Soil Moisture'],
                                    datasets: [{
                                        label: 'Sensor Values',
                                        data: [0, 0, 0, 0],
                                        backgroundColor: [
                                            'rgba(255, 99, 132, 0.2)',
                                            'rgba(54, 162, 235, 0.2)',
                                            'rgba(255, 206, 86, 0.2)',
                                            'rgba(75, 192, 192, 0.2)'
                                        ],
                                        borderColor: [
                                            'rgba(255, 99, 132, 1)',
                                            'rgba(54, 162, 235, 1)',
                                            'rgba(255, 206, 86, 1)',
                                            'rgba(75, 192, 192, 1)'
                                        ],
                                        borderWidth: 2
                                    }]
                                },
                                options: {
                                    scales: {
                                        y: {
                                            beginAtZero: true
                                        }
                                    }
                                }
                            });

                            setInterval(() => updateChart(myChart), 5000);
                        </script>
                    </body>
                    </html>"""
                
                self.cl.send(response.encode('utf-8'))
                self.cl.close()

        except Exception as e:
            print(f"Error in web server: {e}")
        finally:
            if self.cl:
                self.cl.close()
            self.sock.close()
