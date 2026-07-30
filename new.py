from machine import I2C, Pin # programmed by mark:D  (for esp32-c3 SuperMini)
from DIYables_MicroPython_OLED import OLED_SSD1306_I2C
from bitmaps import clear, show, draw_bg
import utime

import network
import espnow
from machine import Pin, ADC, sleep, PWM

adcEn = Pin(2, Pin.OUT) ##ADC SETUP##     high to enable joystick, low to enable finger flexers
a = ADC(3) # pinky finger                     joystick x
b = ADC(4) # ring finger                      joystick y
c = ADC(1) # middle finger                    joystick button
d = ADC(0) # index finger                     
a.atten(ADC.ATTN_11DB)
b.atten(ADC.ATTN_11DB)
c.atten(ADC.ATTN_11DB)
d.atten(ADC.ATTN_11DB)

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

state = 0
adcData = "1:.43:.2:.7:.23:.9"
t1 = f"{devNum+1: 2} " + pNames[devNum]
t2 = ""
t3 = ":D"

handAdj = [3500, 3500, 3500, 3500] #############################################################ADJUST THRESHOLDS HERE#####################################################################
joystickAdj = [3500, 3500, 3500, 3500]

def clamp(n, minn, maxn): # generic func
    return max(min(maxn, n), minn)

def poll(): # polls hand then joystick
        adcEn.value(0)# hand poll
        A1 = clamp(a.read()/handAdj[0], 0, 1) # convert to % flex
        B1 = clamp(b.read()/handAdj[1], 0, 1)
        C1 = clamp(c.read()/handAdj[2], 0, 1)
        D1 = clamp(d.read()/handAdj[3], 0, 1)
        adcEn.value(1)# joystick poll
        A2 = clamp(a.read()/joystickAdj[0], 0, 1) # convert to % flex=
        B2 = clamp(b.read()/joystickAdj[1], 0, 1)
        C2 = clamp(c.read()/joystickAdj[2], 0, 1)
        D2 = clamp(d.read()/joystickAdj[3], 0, 1)
        return [[A1, B1, C1, D1], [A2, B2, C2, D2]]

def draw():
    clear()
    draw_bg(devNum, adcData, state, t1, t2, t3)
    show()

def toggle_connect(): # this pauses the poll->send cycle
    global state
    if state == 0:
        espn.add_peer(pList[devNum])
        state = 1
        draw()
        exitnum = 0
        host, msg = espn.recv(3000)
        if msg:             # msg == None if timeout in recv()
            if host == pList[devNum]:
                state = 3
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
