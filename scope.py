from wifi import WIFI
import socket
from ST7735 import TFT
from sysfont import sysfont
from machine import SPI,Pin,PWM
import time
import utime
import math
from music import MUSIC

fs = 4000

speaker = MUSIC(0)
speaker.play_digital(2000,4)
speaker.play_digital(-1,1)

pwm = PWM(Pin(1))
pwm.duty_u16(32768)
pwm.freq(10)
pwm1 = PWM(Pin(2))
pwm1.duty_u16(32768)
pwm1.freq(100)
adc = machine.ADC(0)

spi = SPI(1, baudrate=20000000, polarity=0, phase=0,sck=Pin(10), mosi=Pin(11), miso=None)
tft=TFT(spi,16,17,18)
tft.initr()
tft.rgb(True)

#wifi = WIFI("Duke's Hub", "rkp12345")
#wifi_config = wifi.connect()
#tft.fill(TFT.BLACK)
#tft.text((0,0), f"LOCAL IP :: {wifi_config[0]}", TFT.WHITE, sysfont, 1)
marker_1 = int((70/100)*tft.size()[0])
marker = []
marker.append(0)
tft.fill(TFT.BLACK)

tft.rect((0,26), (tft.size()[0],88), TFT.GRAY)

def handle_display(buffer,marker):
    tft.text((2,tft.size()[1]-12), f"MARKER 1 = {marker[0]*3.3:05.3f}V", TFT.PURPLE, sysfont, 1)
    for i in range(tft.size()[0]-2):
        tft.line((i+1,27), (i+1,112), TFT.NAVY)
        if i == marker_1+4:
            tft.text((marker_1,buffer[marker_1][1]-8), "1", TFT.PURPLE, sysfont, 1)
        tft.line(buffer[i],buffer[i+1],TFT.GREEN)

def handle_adc(fs):
    while True:
        t1 = time.ticks_us()
        buffer = []
        for i in range(tft.size()[0]):
            data_adc = adc.read_u16()/65535
            if i == marker_1:
                marker[0] = data_adc
            buffer.append((i,36+int(tft.size()[1]*0.60*(1-data_adc))))
        t2 = time.ticks_us()
        loop_time = ((t2 - t1)/1e6)
        fs = tft.size()[0] / loop_time
        tft.text((1,1), f"FS = {fs:08.3f} Hz", TFT.GREEN, sysfont, 1)
        tft.text((1,11), f"SW_TIME = {1/fs} s", TFT.GREEN, sysfont, 1)
        speaker.play_digital(int(marker[0]*tft.size()[1]+800),0)
        handle_display(buffer,marker)

handle_adc(fs)





