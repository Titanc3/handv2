"""
This ESP32 MicroPython code was developed by newbiely.com
This ESP32 MicroPython code is made available for public use without any restriction
For comprehensive instructions and wiring diagrams, please visit:
https://newbiely.com/tutorials/esp32-micropython/esp32-micropython-oled-128x64
"""

from machine import I2C, Pin
from DIYables_MicroPython_OLED import OLED_SSD1306_I2C
import bitmaps


# Initialize I2C
i2c = I2C(0, scl=Pin(9), sda=Pin(8), freq=400000)  # Adjust ESP32 pins according to your setup

# Initialize the OLED display
oled = OLED_SSD1306_I2C(128, 64, i2c)

# Clear the display
oled.clear_display()
oled.display()

oled.set_text_size(1)

# Print a message to the display

devNum = 3
text = f"{devNum:02}"+"/16|"
integer_value = 123
float_value = 45.67

oled.set_cursor(0, 0)
oled.println(text)
oled.set_cursor(0, 8)
oled.println("-----*")
oled.set_cursor(0, 25)
oled.println(str(integer_value))  # Print integer and move to the next line
oled.set_cursor(0, 50)
oled.println("{:.2f}".format(float_value))  # Print formatted float and move to the next line
oled.display()  # Ensure you update the display after writing to it

