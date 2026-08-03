from machine import I2C, Pin
from DIYables_MicroPython_OLED import OLED_SSD1306_I2C
import utime
from math import floor, ceil

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

bat = [
0x7f, 0xf0, 
0x80, 0x08, 
0x80, 0x0c, 
0x80, 0x0c, 
0x80, 0x0c, 
0x80, 0x08, 
0x7f, 0xf0
]
def draw_battery(percent):
    for x in range(0, 5):
        if percent-((x+1)*20) >= 0: # draw full bars
            oled.draw_line(102+(x*2), 4, 102+(x*2), 2, 1)
        else: # do partial bar
            a = percent%20
            if a == 0: # no need for partial bar
                break
            oled.draw_line(102+(x*2), 4, 102+(x*2), 4-floor(a/6.7), 1)
            break

def draw_bg(dev_num, adcData, state, text1, text2, data, batPercent, currentDeviceIcon):
    oled.draw_bitmap(19, 3, grid_bmp, 10, 10, 1)
    oled.draw_bitmap(122, 1, MKC_bmp, 5, 14, 1)
    oled.draw_bitmap(0, 16, currentDeviceIcon, 32, 48, 1)
    oled.draw_bitmap(100, 0, bat, 14, 7, 1)
    draw_devNum(dev_num)
    draw_flexion(adcData)
    draw_battery(batPercent)
    
    
    oled.draw_rect(33, 16, 2, 70, 1) # main divider
    
    oled.set_cursor(36, 0)
    oled.println(text1.replace("\n", "\n      ")) # fix text looping to the beginning of the display
    oled.set_cursor(36, 8)
    oled.println(text2.replace("\n", "\n      "))
    oled.set_cursor(42, 16)
    oled.println(data.replace("\n", "\n       "))
    

    if state == 1: #states 0-2: not_connected, searching, connected
        oled.draw_bitmap(3, 3, mag_bmp, 10, 10, 1)
    elif state == 2:
        oled.draw_bitmap(3, 3, chain_bmp, 10, 10, 1)

def clear():
    oled.clear_display()
    
def show():
    oled.display()
    utime.sleep(1)

def draw_devNum(index):
    x = index%4*3+18
    y = floor(index/4)*3+2
    oled.draw_bitmap(x, y, devNum_bmp, 3, 3, 1)
    oled.display()

def draw_flexion(dataList):
    l=dataList.split(":")
    
    for x in range (0, 4):
        oled.draw_rect((x*2+121), int(47-float(l[x])*47)+16, 1, 48, 1)

