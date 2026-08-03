from machine import I2C, Pin, RTC # programmed by mark:D  (for esp32-c3 SuperMini)
from DIYables_MicroPython_OLED import OLED_SSD1306_I2C
from bitmaps import clear, show, draw_bg
import utime
from lsm6ds3 import LSM6DS3, NORMAL_MODE_104HZ

import network
import espnow
from machine import Pin, ADC, sleep, PWM

fingerEn = Pin(2, Pin.OUT) ##ADC SETUP##    low to enable finger flexers
joystickEn = Pin(21, Pin.OUT)
fingerEn.value(1)
joystickEn.value(1)
a = ADC(3) # pinky finger                     joystick x
b = ADC(4) # ring finger                      joystick y
c = ADC(1) # middle finger                    joystick button
d = ADC(0) # index finger                     
a.atten(ADC.ATTN_11DB)
b.atten(ADC.ATTN_11DB)
c.atten(ADC.ATTN_11DB)
d.atten(ADC.ATTN_11DB)

rtc = RTC() # time setup

sta = network.WLAN(network.WLAN.IF_STA)  ##NETWORK SETUP##
sta.active(True)
sta.disconnect()     
espn = espnow.ESPNow()
espn.active(True)
pList = [b'0v\xf5\xa6Mh'] ####################################add peers here, MAC address of peers' wifi interface [0-16 peers])#########################################################
pNames = ["led array"] #######################################add peer names here########################################################################################################
for _ in range (0, 16):
    pList.append(b'00\x00\x0000') #ensure list is filled to prevent out-of-index err
    pNames.append("N/A")
devNum = 0 # index to use when connecting to peers

i2c = I2C(0, scl=Pin(9), sda=Pin(8), freq=400000)  ##DISPLAY SETUP##
oled = OLED_SSD1306_I2C(128, 64, i2c)
oled.clear_display()
oled.set_text_size(1)
# Print a message to the display

sensor = LSM6DS3(i2c, mode=NORMAL_MODE_104HZ)


state = 0
adcData = "1:.43:.2:.7:.23:.9"
time = rtc.datetime()
print(time)
battery = 14
t1 = f" {time[4]%12:02}:{time[5]:02} {battery:02}%"
t2 = f"{devNum+1:02} " + pNames[devNum]
t3 = ":D\ng"
devIcon = [0x00, 0x00, 0x00, 0x00, 
0x00, 0x00, 0x00, 0x00, 
0x00, 0x00, 0x00, 0x00, 
0x00, 0x00, 0x00, 0x00, 
0x00, 0x00, 0x00, 0x00, 
0x02, 0x00, 0x00, 0x00, 
0x06, 0x00, 0x40, 0x00, 
0x04, 0x00, 0x40, 0x00, 
0x04, 0x00, 0x40, 0x00, 
0x04, 0x00, 0x40, 0x00, 
0x04, 0x00, 0x40, 0x00, 
0x04, 0x00, 0x20, 0x00, 
0x04, 0x00, 0x20, 0x00, 
0x04, 0x00, 0x20, 0x00, 
0x04, 0x00, 0x20, 0x00, 
0x06, 0x00, 0x20, 0x00, 
0x00, 0x00, 0x00, 0x00, 
0x00, 0x00, 0x00, 0x00, 
0x00, 0x00, 0x00, 0x00, 
0x00, 0x00, 0x00, 0x00, 
0x00, 0x00, 0x00, 0x00, 
0x00, 0x00, 0x00, 0x00, 
0x00, 0x00, 0x00, 0x00, 
0x00, 0x00, 0x00, 0x00, 
0x00, 0x00, 0x00, 0x00, 
0x00, 0x00, 0x00, 0x00, 
0x02, 0x00, 0x00, 0x00, 
0x02, 0x00, 0x00, 0x00, 
0x02, 0x00, 0x60, 0x00, 
0x02, 0x00, 0x40, 0x00, 
0x01, 0x00, 0x80, 0x00, 
0x01, 0x01, 0x00, 0x00, 
0x01, 0x01, 0x00, 0x00, 
0x00, 0x81, 0x00, 0x00, 
0x00, 0x82, 0x00, 0x00, 
0x00, 0x4c, 0x00, 0x00, 
0x00, 0x30, 0x00, 0x00, 
0x00, 0x00, 0x00, 0x00, 
0x00, 0x00, 0x04, 0x00, 
0x00, 0x00, 0x45, 0x00, 
0x00, 0x00, 0x4c, 0x00, 
0x00, 0x00, 0x74, 0x80, 
0x00, 0x00, 0x44, 0x80, 
0x00, 0x00, 0x44, 0x80, 
0x00, 0x00, 0x00, 0x00, 
0x00, 0x00, 0x00, 0x00, 
0x00, 0x00, 0x00, 0x00, 
0x00, 0x00, 0x00, 0x00]

handAdj = [3500, 3500, 3500, 3500] #############################################################ADJUST THRESHOLDS HERE#####################################################################
joystickAdj = [3500, 3500, 3500, 3500]


def clamp(n, minn, maxn): # generic func
    return max(min(maxn, n), minn)

def poll(): # polls hand then joystick
        fingerEn.value(0)
        joystickEn.value(1)
        A1 = clamp(a.read()/handAdj[0], 0, 1) # convert to % flex
        B1 = clamp(b.read()/handAdj[1], 0, 1)
        C1 = clamp(c.read()/handAdj[2], 0, 1)
        D1 = clamp(d.read()/handAdj[3], 0, 1)
        fingerEn.value(1)
        joystickEn.value(0)
        A2 = clamp(a.read()/joystickAdj[0], 0, 1) # convert to % flex=
        B2 = clamp(b.read()/joystickAdj[1], 0, 1)
        C2 = clamp(c.read()/joystickAdj[2], 0, 1)
        D2 = clamp(d.read()/joystickAdj[3], 0, 1)
        fingerEn.value(1)
        joystickEn.value(1)
        return [[A1, B1, C1, D1], [A2, B2, C2, D2]]

def draw():
    t1 = f" {time[4]%12:02}:{time[5]:02} {battery:02}%"
    t2 = f"{devNum+1:02} " + pNames[devNum]
    clear()
    draw_bg(devNum, adcData, state, t1, t2, t3, battery, devIcon)
    show()

def toggle_connect(): # this pauses the poll->send cycle
    global state
    if state == 0:
        espn.add_peer(pList[devNum])
        espn.send("send icon pls :D")
        state = 1
        draw()
        exitnum = 0
        host, msg = espn.recv(3000)
        if msg:             # msg == None if timeout in recv()
            if host == pList[devNum]:
                state = 3
                devIcon = msg
        state -= 1 # sneaky way to ensure state 0 or 2 based on connection
    else:
        espn.del_peer(pL[pIndex])



def send(): # sends data to oled then espnow
    if state == 2:
        espn.send(pL[pI], f"{a}:{b}:{c}:{d}")

print(poll())
draw()
toggle_connect()
draw()

ax, ay, az, gx, gy, gz = sensor.get_readings()
print("Accelerometer\nX:{}, Y:{}, Z:{}\nGyro\nX:{}, Y:{}, Z{}\n\n ".format(ax, ay, az, gx, gy, gz))

for x in range(0, 16):
    devNum = x
    t1 = f" {time[4]%12:02}:{time[5]:02} {battery:02}%"
    draw()
