from machine import Pin
import neopixel
import time
import random

led = neopixel.NeoPixel(Pin(48), 1)   # 1 RGB LED on pin 48

def LED_on():
    led[0]=(0, 0, 40)
    led.write()
    
    
def LED_off():
    led[0]=(0, 0, 0) #only stores it
    led.write()  #actually sends the color to the led
    
def blink():
    LED_off()
    time.sleep(0.15)
    LED_on()
    time.sleep(0.15)
    
LED_on()

try:
    while True:
        time.sleep(random.uniform(1.5, 4))
        blink()
        if random.random() < 0.3:
            blink()
finally:
    LED_off()