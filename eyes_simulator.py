from machine import Pin, I2C
import ssd1306
import time
import random


i2c = I2C(0, scl=Pin(22), sda=Pin(21))      # set up the 2-wire connection
oled = ssd1306.SSD1306_I2C(128, 64, i2c)    # the screen is 128 x 64 pixels

     
def draw_open(offset=0):
    oled.fill(0)
    oled.fill_rect(19+offset, 14, 30, 36, 1)
    oled.fill_rect(79+offset, 14, 30, 36, 1)
    oled.show()

def draw_closed():
    oled.fill(0)
    oled.fill_rect(19, 30, 30, 4, 1)
    oled.fill_rect(79, 30, 30, 4, 1)
    oled.show()

def blink():
    draw_closed()
    time.sleep(0.15)
    draw_open()
    time.sleep(0.15)


def look_around():
    direction=random.choice([10, -10])
    draw_open(direction)
    time.sleep(1)
    draw_open()

draw_open()
while True:
    sec=random.uniform(1.5, 4)
    time.sleep(sec)
    blink()
    if random.random()<0.3:
       blink()
    if random.random()<0.2:
       look_around()
 





