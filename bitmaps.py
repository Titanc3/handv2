
from machine import I2C, Pin
from DIYables_MicroPython_OLED import OLED_SSD1306_I2C
import utime
from math import floor

i2c = I2C(0, scl=Pin(9), sda=Pin(8), freq=400000)

# Initialize the OLED display
oled = OLED_SSD1306_I2C(128, 64, i2c)

# Clear the display
oled.clear_display()
oled.display()

MKC_bmp = [
0x88, 0xD8, 0xA8, 0x88, 0x00, 0x88, 0x90, 0xF0, 0x88, 0x00, 0xF8, 0x80, 0x80, 0xF8

]

mag_bmp = [
0x38, 0x00,
0x44, 0x00,
0x82, 0x00,
0x82, 0x00,
0x82, 0x00,
0x44, 0x00,
0x3B, 0x00,
0x03, 0x80,
0x01, 0xC0,
0x00, 0xC0,
]

chain_bmp = [
0x03, 0x80,
0x04, 0x40,
0x08, 0x40,
0x10, 0x40,
0x16, 0x80,
0x5A, 0x00,
0x82, 0x00,
0x84, 0x00,
0x88, 0x00,
0x70, 0x00
]

grid_bmp = [
0x92, 0x40,
0x00, 0x00,
0x00, 0x00,
0x92, 0x40,
0x00, 0x00,
0x00, 0x00,
0x92, 0x40,
0x00, 0x00,
0x00, 0x00,
0x92, 0x40
]

devNum_bmp = [
0x40,
0xA0,
0x40
]

def draw_bg(dev_num, adcData, state):
    oled.clear_display()
    oled.draw_bitmap(3, 3, grid_bmp, 10, 10, 1)
    oled.draw_bitmap(122, 1, MKC_bmp, 5, 14, 1)
    oled.draw_rect(34, 0, 2, 63, 1) # main divider
    draw_devNum(dev_num)
    draw_flexion(adcData)
    if state == 1: #states 0-2: not_connected, searching, connected
        oled.draw_bitmap(19, 3, mag_bmp, 10, 10, 1)
    else if state == 2:
        oled.draw_bitmap(19, 3, chain_bmp, 10, 10, 1)
    oled.display()


def draw_devNum(index):
    x = index%4*3+2
    y = floor(index/4)*3+2
    oled.draw_bitmap(x, y, devNum_bmp, 3, 3, 1)
    oled.display()
    utime.sleep(.001)

def draw_flexion(dataList):
    l=dataList.split(":")
    
    for x in range (0, 4):
        oled.draw_rect((x*2+121), int(47-float(l[x])*47)+16, 1, 48, 1)

