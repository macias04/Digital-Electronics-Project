# Complete project details at https://RandomNerdTutorials.com

import machine, neopixel

n = 12 #numero de leds que vamos a encender
p = 5  # el pin gpio que esta conectado

np = neopixel.NeoPixel(machine.Pin(p), n) 

def set_color(r, g, b, n):  # podemos ponerlos de los colores que queramos o mezclarolos
  for i in range(n):
    np[i] = (r, g, b)
  np.write()
