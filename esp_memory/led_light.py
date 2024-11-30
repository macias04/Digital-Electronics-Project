"""
    This module control LED lighting based on the amount of ambient light detected.

    It adjusts the number of LEDs and their colors based on the provided light amount.
    It uses the `leds_controller` module to set the LED colors.

    Attributes:
        light_amount (int): The amount of light detected, used to determine LED settings.
        leds_num (int): The number of LEDs to be activated based on the light amount.

    Methods:
        light_control():
            Adjusts the number of LEDs and their colors based on the light amount.

    Example:
        light_sensor = Light(light_amount=100)
        light_sensor.light_control()  # Adjusts LEDs based on the light amount
"""

import leds_controller as leds 
class LedLight:
    def __init__(self, light_amount):
        self.light_amount = light_amount
        self.leds_num = 0

    def  light_control(self):
        if self.light_amount < 41:
            self.leds_num=12
            leds.set_color(0,0,230, self.leds_num) 
        elif self.light_amount < 819:
            self.leds_num=10
            leds.set_color(0,0,130, self.leds_num)
        elif self.light_amount < 2048:
            self.leds_num=8
            leds.set_color(0,0,50, self.leds_num)
        elif self.light_amount < 3277:
            self.leds_num=5
            leds.set_color(0,0,50, self.leds_num)
        else:
            self.leds_num=2
            leds.set_color(0,0,50, self.leds_num)
  