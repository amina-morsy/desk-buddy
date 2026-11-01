import network
import time
import secrets
import ntptime
from machine import Pin
import neopixel
import random

led=neopixel.NeoPixel(Pin(48), 1)

def LED_on():
    t = local_time()
    led[0] = colour_for_hour(t[3])
    led.write()

def LED_off():
    led[0]=(0, 0, 0)
    led.write()
    
def blink():
    LED_off()
    time.sleep(0.15)
    LED_on()
    time.sleep(0.15)

def colour_for_hour(hour):
    if 7<= hour <=11:
        return (40, 30, 0) #yellow
    elif 12 <= hour <=17: 
        return (30, 30, 30) #white
    elif 18<= hour <=22:
        return (40, 15, 0) #orange
    else:
        return (5, 0, 8) #dim purple
    


wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect(secrets.WIFI_NAME, secrets.WIFI_PASSWORD)

print("Connecting", end="")
for i in range(40):                  # try for up to 20 seconds
    if wlan.isconnected():
        break
    print(".", end="")
    time.sleep(0.5)

if wlan.isconnected():
    print("\nConnected! IP address:", wlan.ifconfig()[0])
else:
    print("\nCould not connect. Check the name and password.")
    
ntptime.settime()
TZ_OFFSET =1

def local_time():
    return time.localtime(time.time()+TZ_OFFSET*3600)

LED_on()
try:
    while True:
        time.sleep(random.uniform(1.5, 4))
        blink()
        if random.random() < 0.3:
            blink()
finally:
    LED_off()
    