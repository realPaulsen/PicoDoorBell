####################################################################################
# MIT License
#
# Copyright (c) 2022 Maurício C. P. Pessoa
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
####################################################################################

# A simple example that:
# - Connects to a WiFi Network defined by "ssid" and "password"
# - Performs a GET request (loads a webpage)
# - Queries the current time from a server

import network   # handles connecting to WiFi
import urequests # handles making and servicing network requests
import time
import machine
from secrets import secrets


# Load login data from different file for safety reasons
ssid = secrets['ssid']
pw = secrets['pw']
botToken = secrets['botToken']
chatId = secrets['telegramDmUid']
startupText = 'Klingelficker aktiviert'
text = 'Ding Dong!!! Mund auf!!'

wlan = network.WLAN(network.STA_IF)
wlan.active(True)
led = machine.Pin('LED', machine.Pin.OUT)
doorBellInput = machine.Pin(0, machine.Pin.IN, machine.Pin.PULL_DOWN)
pressed = 1


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
            send_message(startupText)
            break
        else:
            print('WiFi is disconnected. Trying to connect.')
            led.off()
            wlan.connect(ssid, pw)
            time.sleep(3)

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
    if (doorBellInput.value() == pressed):
        print('Door bell pressed!')
        return True
    return False


def main_loop():
    led.on()
    time.sleep(1)
    led.off()

    while True:
        if is_bell_pressed():
            send_message(text)
            time.sleep(4)
        time.sleep(0.1)





# Connect to network
connect_to_wifi()

main_loop()

