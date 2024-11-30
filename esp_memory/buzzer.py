import machine
class Buzzer:
    def __init__(self,pin):
        self.buzzer = machine.PWM(machine.Pin(pin))

    def sound_buzzer(self, x):
        self.buzzer.value(x)  # 1 ==> Sounds, 0 ==> Stops
        self.buzzer.duty_u16(50)