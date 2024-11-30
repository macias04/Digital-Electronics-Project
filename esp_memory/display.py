"""
This class uses inheritance from sh1106 module to draw text oled display. 
For simplicity we took important functions that we needed
For more information check that module out
"""

from sh1106 import SH1106_I2C as sh

class Display(sh):
    def __init__(self, i2c, contrast):
        super().__init__(i2c)  
        self.contrast(contrast)

    def clear_display(self, value=0):
        self.fill(value) 
    
    def show_display(self):
        self.show() 
    
    def write_text(self, text, start, row):
        self.text(text, start, row)  
