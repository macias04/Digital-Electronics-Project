# Complete project details at https://RandomNerdTutorials.com
# trying out

import machine, neopixel

leds_number = 12 #numero de leds que vamos a encender
pin = 5  # el pin gpio que esta conectado

neopixel_ = neopixel.NeoPixel(machine.Pin(pin), leds_number) 

def set_color(r, g, b, n):  
  for i in range(n):
    neopixel_[i] = (r, g, b)
  neopixel_.write()
