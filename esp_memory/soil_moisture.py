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


