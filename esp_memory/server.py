import network
import socket
import time

SSID = 'IWN'
PASSWORD = 'c3z35gyy'

class Server:
    
    def __init__(self, sensor_data):
        self.sensor_data = sensor_data  # Store a reference to the sensor data
        self.sock = socket.socket()
        self.cl = None
        self.addr = socket.getaddrinfo('0.0.0.0', 80)[0][4]
        self.ip_address = self.connect_wifi()
        self.web_server()

    def connect_wifi(self):
        wlan = network.WLAN(network.STA_IF)
        wlan.active(False)  # Disable the Wi-Fi interface
        time.sleep(1)       # Wait a moment
        wlan.active(True)   # Re-enable the Wi-Fi interface
        wlan.connect(SSID, PASSWORD)

        # Wait for connection
        while not wlan.isconnected():
            print("Connecting to WiFi...")
            time.sleep(1)

        print("Connected to WiFi")
        self.ip_address = wlan.ifconfig()[0]  # Get the IP address
        print("IP Address:", self.ip_address)
        return self.ip_address

    def web_server(self):
        try:
            self.sock.bind(self.addr)
            self.sock.listen(5)
            print('Listening on', self.addr)

            while True:
                self.cl, self.addr = self.sock.accept()
                print('Client connected from', self.addr)
                request = self.cl.recv(1024).decode('utf-8')
                print(f"Request: {request}")

                # Use the sensor data directly from the reference
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





