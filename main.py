import time
import threading
from machine import I2C, Pin, ADC 
from sh1106 import SH1106_I2C
import sys
from buzzer import Buzzer
from led_light import LedLight
from server import Server
from display import Display
from soil_moisture import SoilMoisture


# Initialization of sensors
i2c = I2C(0, scl=Pin(22), sda=Pin(21), freq=400_000)
photoresistor = ADC(Pin(36))
photoresistor.atten(ADC.ATTN_11DB)
soil_moisture = SoilMoisture(35)
buzz = Buzzer(23)




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


sensor_data = {
    'temp': 0,
    'humid': 0,
    'light': 0,
    'soil': 0
}
ip = None


def run_server():
    global ip
    server = Server(sensor_data)  
    ip = server.ip_address
    while True:
        time.sleep(1)  

    return ip


# Start the server in a separate thread
server_thread = threading.Thread(target=run_server)
server_thread.daemon = True  # This allows the thread to exit when the main program exits
server_thread.start()

try:
    while True:

        display.clear_display()


        try:
            temp_humi_data = i2c.readfrom_mem(SENSOR_ADDR, 0, 4)
            humi_val = temp_humi_data[0] + temp_humi_data[1]
            temp_val = temp_humi_data[2] + temp_humi_data[3]

            light_val = photoresistor.read()
            light_percentage = light_val / 4100 * 100 
            led_light = LedLight(light_val)
            led_light.light_control()

            value_moisture = soil_moisture.update_soil_value()
            print(f"Main Soil >>> ---- {type(value_moisture)}")
            s_moisture = value_moisture/1800 * 100
            print(s_moisture)
            
            
            if value_moisture < 32500:
                buzz.sound_buzzer(1)
            else:
                buzz.sound_buzzer(0)
            
            temperature = f"{temp_val:.1f}C"
            humidity = f"{humi_val:.1f} %"
            light_string = f"{light_percentage:.1f} %"
            soil_moi_val = f'{s_moisture} %'
            
        except Exception as e:
            print(f"Error reading the sensor: {e}")

        

        display.write_text(f"Digi Mola", 0, 0)
        display.write_text(f"Temperature: {temperature}", 0, 10)
        display.write_text(f"Humidity: {humidity}", 0, 20)
        display.write_text(f"Light: {light_string}", 0, 30)
        display.write_text(f"Soil: {soil_moi_val}", 0, 40)
        display.write_text(f"{ip}", 0, 50)



        display.show_display()
        

        sensor_data['temp'] = float(temp_val)
        sensor_data['humid'] = float(humi_val)
        sensor_data['light'] = float(round(light_percentage, 2))
        sensor_data['soil'] = float(s_moisture)
        
        time.sleep(1)

except KeyboardInterrupt:
    print("Program stopped. Exiting...")
    server_thread.stop()
    

    display.clear_display()
    display.show_display()

    sys.exit(0)
