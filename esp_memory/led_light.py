import leds_controller as leds 
class Light:
    def __init__(self, value):
        self.value = value

    def  light_control(self):
        if self.value < 41:
            n=12
            leds.set_color(0,0,230,n) #mete solo color azul y a una intensidad de 230
        elif self.value < 819:
            n=10
            leds.set_color(0,0,130,n)
        elif self.value < 2048:
            n=8
            leds.set_color(0,0,50,n)
        elif self.value < 3277:
            n=5
            leds.set_color(0,0,50,n)
        else:
            n=2
            leds.set_color(0,0,50,n)
  