"""
    A class to read soil moisture levels using an ADC (Analog-to-Digital Converter).

    This class initializes the ADC on a specified GPIO pin to measure the soil moisture level.
    It provides a method to read and return the ADC value, which corresponds to the moisture level.

    Attributes:
        soil_adc (ADC): The ADC object used to read soil moisture values.

    Methods:
        update_soil_value():
            Reads the current soil moisture level and returns the ADC value.

    Example:
        soil_sensor = SoilMoisture(pin_number=34)  # Replace with the actual pin number
        moisture_value = soil_sensor.update_soil_value()  # Get the current soil moisture value
"""

from machine import ADC, Pin
import time

class SoilMoisture:    
    def __init__(self, pin_number):
        self.soil_adc = ADC(Pin(pin_number)) 
        self.soil_adc.atten(ADC.ATTN_11DB)
        
    def update_soil_value(self):
        adc_soil_value = self.soil_adc.read()  
        print("ADC Value is -----> %d" % adc_soil_value) #for testing purposes
        return adc_soil_value


