# A simple example that:
# - Connects to a WiFi Network defined by "ssid" and "password"
# - Performs a GET request (loads a webpage)
# - Queries the current time from a server

import network   # handles connecting to WiFi
import urequests # handles making and servicing network requests
import time
import machine
from secrets import secrets

# secrets
ssid = secrets['ssid']
pw = secrets['pw']
botToken = secrets['botToken']
chatId = secrets['telegramDmUid']
# hardware constants
pin_bell = 0
pin_led = 'LED'
time_cooldown_message = 4
time_cooldown_wifi_retry = 3
time_loopstep = 0.1 # Update resolution of the pin_bell
time_cooldown_alive = 30
# other
startupText = 'Klingelficker aktiviert'
text = '🔔'
last_blink = time.time()


# other vars
wlan = network.WLAN(network.STA_IF)
wlan.active(True)
led = machine.Pin(pin_led, machine.Pin.OUT)
doorBellInput = machine.Pin(pin_bell, machine.Pin.IN, machine.Pin.PULL_DOWN)


def send_message(message:str):
    try:
        if not is_wifi_connected():
            connect_to_wifi()
        urequests.get(f"https://api.telegram.org/bot{botToken}/sendMessage?chat_id={chatId}&text="+message)
    except OSError as e:
        print(e)
        led.off()
        wlan.disconnect()
        # Grace period.
        time.sleep(10)
        led.on()
        pass

def connect_to_wifi():
    while True:
        if (is_wifi_connected()):
            blink_onboard_led(3)
            led.on()
            status = wlan.ifconfig()
            print('ip = ' + status[0])
            #send_message(startupText)
            break
        else:
            print('WiFi is disconnected. Trying to connect.')
            led.off()
            wlan.connect(ssid, pw)
            time.sleep(time_cooldown_wifi_retry)

def is_wifi_connected():
    wlan_status = wlan.status()
    if wlan_status != 3:
        return False
    else:
        return True

def blink_onboard_led(num_blinks):
    for i in range(num_blinks):
        led.on()
        time.sleep(.2)
        led.off()
        time.sleep(.2)

def is_bell_pressed():
    if (doorBellInput.value() == 1):
        print(f'{text} [Door bell pressed!]')
        return True
    return False


# Connect to network
connect_to_wifi()

led.on()
time.sleep(1)
led.off()

while True:
    if is_bell_pressed():
        led.on()
        send_message(text) # send Telegrammessage
        time.sleep(time_cooldown_message) # cooldown
        led.off()

    if (time.time() - last_blink > time_cooldown_alive): # show led to signal that it's alive
        led.on()
        time.sleep(time_loopstep)
        led.off()
        last_blink = time.time()
    else:
        time.sleep(time_loopstep)
