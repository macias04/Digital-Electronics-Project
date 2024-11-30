# Project: Smart Plant Monitoring System with ESP32

## Introduction
Measurement/Control/Visualization of the environment for tropical plants :
The goal of the project would be to create a system that measures key environmental parameters (such as temperature, humidity, light levels, soil moisture) for tropical plants.
This system should also allow the user to control or adjust environmental conditions and visualize the data.

This project was developed by Gerson Hauwanga, Adrián Macias and Mario Loizaga. The aim is to create a smart environmental monitoring system using an ESP32, sensors for temperature, humidity, light, and soil moisture, along with an integrated web server for real-time data visualization.

The system measures and displays sensor values on an OLED screen and transmits this data through a web interface. It also includes LED control based on detected light levels and a buzzer alert for critical soil moisture conditions.

We have developed the project using Thonny, a programming environment that allows us to interact directly with microdevices like the ESP32.
By programming in MicroPython, we can create, delete, modify, automate, control, and improve device functions to build a final project that meets our exact requirements.
To achieve this, it is essential to have a solid understanding of MicroPython and the ability to write efficient code that aligns with our objectives.
Additionally, a foundational knowledge of timers, displays, and synchronous/asynchronous communication is beneficial for comprehending the operation of microcontrollers and sensors.
Subsequently, we will create or utilize the files outlined later and upload them to the ESP32 to enable the use of these modules when executed from the main program.

## Main Features
I2C communication:
I2C, which stands for Inter-Integrated Circuit, is a simple, low-speed serial communication protocol commonly used for short-distance communication between integrated circuits on a single printed circuit board.
It's particularly popular in embedded systems due to its simplicity and low cost.
I2C (Inter-Integrated Circuit, I2C, IIC, [eye-squared-C]) is two-wire, synchronous,bi-directional, half-duplex, short-distance, intra-board, serial bus communication
SCL (one-directional Serial Clock), SDA (bi-directional Serial Data) signals
One Master, one or more Slave devices
Communication protocol consists of: Start condition, Address frame, Data frame, Stop condition.

(Add image of the I2C communication) 

Photoresistor:
A photoresistor, also known as a Light-Dependent Resistor (LDR) or photoconductor, is an electronic component whose electrical resistance varies depending on the amount of light that falls on it.
In simpler terms, the more light it receives, the lower its resistance becomes.
How does it work?
When light hits the semiconductor material of a photoresistor, photons (particles of light) provide energy to electrons, allowing them to move more freely. 
This increased movement of electrons reduces the overall resistance of the material.


Soil moisture:
Soil moisture refers to the amount of water present in the soil. It's a critical factor for life on Earth, influencing:
Plant growth: Water is essential for plants to absorb nutrients and perform photosynthesis.
Biogeochemical cycles: Soil moisture plays a crucial role in the water, carbon, and other element cycles.
Soil stability: Moisture affects soil structure and its ability to resist erosion.
Climate: Evaporation of water from the soil influences atmospheric humidity and precipitation.

Display:
LCD (Liquid Crystal Display) is an electronic device which is used for display any ASCII text. There are many different screen sizes e.g. 16x1, 16x2, 16x4, 20x4, 40x4 characters and each character is made of 5x8 matrix pixel dots.
LCD displays have different LED back-light in yellow-green, white and blue color. LCD modules are mostly available in COB (Chip-On-Board) type.
With this method, the controller IC chip or driver (here: HD44780) is directly mounted on the backside of the LCD module itself.

Web page:
A threading library provides a way to manage multiple threads of execution within a single process.
In the context of web development, threading allows you to handle multiple tasks concurrently, improving the responsiveness of your application.
Then we developed a web page for showing data after reading it. We did it focused on the purpose of controlling data faster and automatically.
Also we can see if any value is lower or higher inmediatly and react to that.

(add image of the web page)


### Classes and Methods
- **`leds_controller.py`**
-Module where we defined the method set_color
```pyhton
import machine, neopixel
n = 12 
p = 5  
np = neopixel.NeoPixel(machine.Pin(p), n) 
def set_color(r, g, b, n): 
  for i in range(n):
    np[i] = (r, g, b)
  np.write()
```
  -**`set_color(r, g, b, n)`**: Changes the color of the NeoPixel LEDs.
  
- **`main.py`**
```pyhton
import time
import threading
from machine import I2C, Pin, ADC 
from sh1106 import SH1106_I2C
import sys
from led_light import Light
from server import Server
# from web_page import Server
from display import Display
from soil_moisture import SoilMoisture
# from buzzer import Buzzer

# Initialization of sensors
i2c = I2C(0, scl=Pin(22), sda=Pin(21), freq=400_000)
photoresistor = ADC(Pin(36))
photoresistor.atten(ADC.ATTN_11DB)
soil_moisture = SoilMoisture(35)
# buzz = Buzzer(23)
# soil_moisture.zero_adc()  # Call this to zero the ADC


# Initialization of the OLED display
display = Display(i2c, 50)

# DHT12
SENSOR_ADDR = 0x5c  # Change according to the sensor

# Scan I2C devices
print("Stop execution `Ctrl+C`.")
print("Looking for I2C... ", end="")
addrs = i2c.scan()

if SENSOR_ADDR in addrs:
    print(f"{hex(SENSOR_ADDR)} is detected")
else:
    print("[ERROR] Sensor not detected. Check connections.")
    raise Exception("Sensor I2C not found.")

# Shared data structure for sensor readings
sensor_data = {
    'temp': 0,
    'humid': 0,
    'light': 0,
    'soil': 0
}



ip = '192.168.189.208' 

def run_server():
    server = Server(sensor_data)  # Pass the reference to sensor_data
    ip = server.ip_address
    while True:
        time.sleep(1)  # Keep the server running

    return ip
# Start the server in a separate thread
server_thread = threading.Thread(target=run_server)
server_thread.daemon = True  # This allows the thread to exit when the main program exits
server_thread.start()


try:
    while True:
        # Clear display
        display.clear_display()

        # Get sensors data
        try:
            temp_humi_data = i2c.readfrom_mem(SENSOR_ADDR, 0, 4)
            humi_val = temp_humi_data[0] + temp_humi_data[1]
            temp_val = temp_humi_data[2] + temp_humi_data[3]
            value_moisture = soil_moisture.update_soil_value()
            print(f"Main Soil >>> ---- {type(value_moisture)}")
            s_moisture = value_moisture/1800 * 100
            print(s_moisture)
            '''
            if value_moisture < 32500:
                buzz.sound_buzzer(1)
            else:
                buzz.sound_buzzer(0)
            '''
            temperature = f"{temp_val:.1f}C"
            humidity = f"{humi_val:.1f} %"
            soil_moi_val = f'{s_moisture} %'
            
        except Exception as e:
            print(f"Error reading the sensor: {e}")

        # Reading ambient light
        lux_val = photoresistor.read()
        lux_percentage = lux_val / 4100 * 100 
        luz = f"{lux_percentage:.1f} %"
        light = Light(lux_val)
        light.light_control()
        
        # Show data on the display
        display.write_text(f"Digi Mola", 0, 0)
        display.write_text(f"Temperature: {temperature}", 0, 10)
        display.write_text(f"Humidity: {humidity}", 0, 20)
        display.write_text(f"Light: {luz}", 0, 30)
        display.write_text(f"Soil: {soil_moi_val}", 0, 40)
        display.write_text(f"{ip}", 0, 50)


        # Update the display
        display.show_display()
        
        # Update shared sensor data
        sensor_data['temp'] = float(temp_val)
        sensor_data['humid'] = float(humi_val)
        sensor_data['light'] = float(round(lux_percentage, 2))
        sensor_data['soil'] = float(s_moisture)
        
        time.sleep(1)

except KeyboardInterrupt:
    print("Program stopped. Exiting...")

    # clean up the display
    display.clear_display()
    display.show_display()

    # Stop program execution
    sys.exit(0)
```
-Configures sensors for temperature, humidity, light, and soil moisture.
-Starts the web server and updates the OLED screen with collected data.
-Implements light control using a photoresistor.
-Runs the server in a separate thread for real-time data updates.

- **`server.py`**
-Module where we defined the WiFi connections and the server for the web page
```python
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
```
-Server class: Manages Wi-Fi connection and communication via a web server.
-Responds to HTTP requests, displaying real-time data on a dynamically updated webpage using **Chart.js**.
  
- **`display.py`**
```pyhton
from sh1106 import SH1106_I2C as sh

class Display(sh):
    def __init__(self, i2c, contrast):
        super().__init__(i2c)  
        self.contrast(contrast)

    def clear_display(self, val=0):
        self.fill(val) 
    
    def show_display(self):
        self.show() 
    
    def write_text(self, text, start, row):
        self.text(text, start, row)  
```
-Display class: Manages the OLED display using the SH1106 driver.
  - Methods:
  - clear_display(val=0): Clears the screen.
  - how_display(): Refreshes the screen to show new content.
  - write_text(text, start, row): Writes text at a specific position.

- **`buzzer.py`**  
  - Buzzer class: Controls a buzzer using PWM.
  - Method:
  - sound_buzzer(x): Activates the buzzer (1 for on, 0 for off).

- **`soil_moisture.py`**
```python
from machine import ADC, Pin
import time

class SoilMoisture:    
    def __init__(self, pin_number):
        self.soil_adc = ADC(Pin(pin_number))  # Initialize ADC on the specified pin
        self.soil_adc.atten(ADC.ATTN_11DB)
        
    def update_soil_value(self):
        adc_soil_value = self.soil_adc.read()  # Read the ADC value
        print("ADC Value is -----> %d" % adc_soil_value)
        return adc_soil_value
 ```
  - SoilMoisture class: Reads soil moisture levels.
  - Method:
  - update_soil_value(): Returns the current ADC value of soil moisture.

### External Modules
- **`neopixel`**: Controls the NeoPixel LEDs.
- **`machine`**: Interacts with ESP32 hardware.
- **`socket`**: Powers the web server.
- **`time`**: Manipulates the time
- **`sh1106`**: Shows text and images, Creates user interfaces and Draw graphics.                                           
                                
## Microdevices and Sensors

(add images of the sensors)

1. **ESP32**  
   - Acts as the main microcontroller.
   - Connects sensors and manages the web server.
   - ![](esp32pins.png)

2. **OLED Display (SH1106)**  
   - Displays real-time information.  
   - Connected via I2C (GPIO 21 and GPIO 22).
   - ![](oled.webp)

3. **Soil Moisture Sensor**  
   - Detects soil moisture levels.  
   - Connected to ESP32 ADC (GPIO 35).

4. **Photoresistor**  
   - Measures ambient light.  
   - Connected to analog pin 36.

5. **NeoPixel LEDs**  
   - Controlled from GPIO 5.

6. **Buzzer**  
   - Controlled from GPIO 23.

7. **Wi-Fi**  
   - SSID: `IWN`  
   - Password: `c3z35gyy`

### Connections

| Component              | ESP32 Pin                    |
|------------------------|------------------------------|
| OLED Display (I2C)     | GPIO 21 (SDA), GPIO 22 (SCL) |
| Photoresistor          | GPIO 36                      |
| Soil Moisture Sensor   | GPIO 35                      |
| NeoPixel LEDs          | GPIO 5                       |
| Buzzer                 | GPIO 23                      |

                                               
## Installation and Usage

1. **Clone this repository:**
   ```bash
   git clone https://github.com/MarioLOI/Digital-Electronics-Project
