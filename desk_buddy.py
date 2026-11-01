import network
import time
from machine import Pin, I2C
import sh1106
import random
import ntptime
import secrets



wlan = network.WLAN(network.STA_IF)   # STA_IF, station mode, means the board joins an existing network
wlan.active(True)                     # turn Wi-Fi on
wlan.connect(secrets.WIFI_NAME, secrets.WIFI_PASSWORD)       # network name, password

print("Connecting", end="")
for i in range(40):
    if wlan.isconnected():
        break
    print(".", end="")
    time.sleep(0.5)

if wlan.isconnected():
    print("\nConnected! IP address:", wlan.ifconfig()[0])
else:
    print("\nCould not connect. Check the name and password.")

 
for attempt in range(5):
    try:
        ntptime.settime()
        break
    except OSError:
        time.sleep(1)            # NTP (“Network Time Protocol”) is how computers and phones set their clocks. The board asks a time server, which replies with the exact time.

#UTC is the world reference time, the server always answers in UTC

TZ_OFFSET = 1                # Rome is UTC+1 in winter (UTC+2 in summer)

def local_time():
    return time.localtime(time.time() + TZ_OFFSET * 3600) # time.localtime() turns a number of seconds into a tuple of (year, month, day, hour, minute, second, weekday, day_of_year)

t = local_time()
print("Time in Rome: {:02d}:{:02d}:{:02d}".format(t[3], t[4], t[5])) #{:02d} formats a number with 2 digits and a leading zero


i2c = I2C(0, scl=Pin(9), sda=Pin(8))      # set up the 2-wire connection
oled = sh1106.SH1106_I2C(128, 64, i2c)    # the screen is 128 x 64 pixels

     
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
    direction = random.choice([10, -10])
    draw_open(direction)
    if wait(1, "eyes"):
        draw_open()


def show_eyes():
    draw_open()
    blink()
    if random.random()<0.2:
        look_around()

def show_clock():
    oled.fill(0)
    t = local_time()
    oled.text(f"{t[3]:02d}:{t[4]:02d}:{t[5]:02d}", 32, 28)   # time
    oled.show()

def show_date():
    oled.fill(0)
    t=local_time()
    oled.text(f"{t[2]:02d}/{t[1]:02d}/{t[0]}", 24, 28)       
    oled.show()



button = Pin(0, Pin.IN, Pin.PULL_UP) #this time the pin is an input, so the board reads it instead of sending power out like with the LED.
#the board connects the pin internally to 3.3V through a weak resistor, so it reads 1 when nothing is pressed. Without it, an unconnected pin “floats” and gives random values
# Pin 0 is the board's BOOT button so we can switch modes without any extra parts
mode = "eyes"        # what the buddy is showing right now
last_press = 0       # when the button was last pressed (in milliseconds)

def on_press(pin):
    global mode, last_press #global mode, last_press: normally a function can’t change variables that live outside it, and this line gives it permission. Without it, on_press would create its own local mode and the main loop would never see the change.
    now = time.ticks_ms()
    if time.ticks_diff(now, last_press) > 300:     # ignore "presses on the button" within 0.3 s
        if mode == "eyes":
            mode = "clock"
        elif mode == "clock":
            mode = "date"
        else:
            mode = "eyes"

        last_press = now

button.irq(trigger=Pin.IRQ_FALLING, handler=on_press) #button.irq(...) sets up the interrupt: “whenever this pin changes, immediately run on_press”, even if the code is in the middle of a sleep.
#IRQ_FALLING means “when the value falls from 1 to 0”, which is the moment the button is pressed


#after you press the button, it only switches once the sleep finishes. This version sleeps in tiny steps and stops early if the mode changed:

def wait(seconds, current_mode):
    end = time.ticks_add(time.ticks_ms(), int(seconds * 1000))
    while time.ticks_diff(end, time.ticks_ms()) > 0:
        if mode != current_mode:     # button was pressed, so stop waiting
            return False
        time.sleep(0.05)
    return True                      # waited the full time




while True:
    if mode == "eyes":
        draw_open()
        if wait(random.uniform(1.5, 3), "eyes"):   # only blink if still in eyes mode
            show_eyes()
    elif mode =="clock":
        show_clock()
        wait(1, "clock")
    else:
        show_date()
        wait(1, "date")