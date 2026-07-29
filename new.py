from machine import I2C, Pin
from DIYables_MicroPython_OLED import OLED_SSD1306_I2C
from bitmaps import clear, show, draw_bg
import utime

i2c = I2C(0, scl=Pin(9), sda=Pin(8), freq=400000)  # Adjust ESP32 pins according to your setup

oled = OLED_SSD1306_I2C(128, 64, i2c)

oled.clear_display()

oled.set_text_size(1)

# Print a message to the display

devNum = 15
state = 2
adcData = "1:.43:.2:.7:.23:.9"
t1 = f"{devNum+1:02}"+"/16" # text1
t2 = "machine error"
t3 = ":D"
integer_value = 123
float_value = 45.67

def draw():
    clear()
    draw_bg(devNum, adcData, state, t1, t2, t3)
    show()

draw()
