"""
    A class to control a buzzer using PWM on a microcontroller.

    Attributes:
        buzzer (machine.PWM): The PWM object for the buzzer.

    Methods:
        sound_buzzer(x):
            Turns the buzzer on (x=1) or off (x=0).

    Example:
        buzzer = Buzzer(pin=15)
        buzzer.sound_buzzer(1)  # Turn on the buzzer
        buzzer.sound_buzzer(0)  # Turn off the buzzer
"""

import machine


class Buzzer:

    def __init__(self, pin):
        self.buzzer = machine.PWM(machine.Pin(pin))
        self.buzzer.freq(800)  # Set a frequency for the PWM signal

    def sound_buzzer(self, x):
        if x == 1:
            self.buzzer.duty_u16(32768)  # Set duty cycle to 50% (range 0-65535)
        else:
            self.buzzer.duty_u16(0)  # Stop the buzzer
