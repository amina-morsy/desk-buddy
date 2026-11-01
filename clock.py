import network
import time
import secrets
import ntptime

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

while True:
    t=local_time()
    print(f"{t[3]:02d}:{t[4]:02d}:{t[5]:02d}")
    time.sleep(1)
    