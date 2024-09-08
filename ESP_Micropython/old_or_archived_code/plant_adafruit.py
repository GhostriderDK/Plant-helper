import umqtt_robust2 as mqtt
from machine import Pin, ADC
import time
import json
import network
import os
import sys

# LED config
red_led_pin = 4
red_led = Pin(red_led_pin, Pin.OUT)

green_led_pin = 16
green_led = Pin(green_led_pin, Pin.OUT)

blue_led_pin = 17
blue_led = Pin(blue_led_pin, Pin.OUT)

# Soil Moisture
soil = ADC(Pin(35))
m = 100

min_moisture = 0
max_moisture = 4095

soil.atten(ADC.ATTN_11DB)       # Full range: 3.3v
soil.width(ADC.WIDTH_12BIT)     # Range 0 to 4095

red_treshold = 30
green_treshold = 80

# WiFi connection information
try:
    from credentials import credentials
except ImportError:
    print("Credentials are kept in credentials.py, please add them there!")
    raise

WIFI_SSID = credentials["ssid"]
WIFI_PASSWORD = credentials["password"]

# Turn off the WiFi Access Point
ap_if = network.WLAN(network.AP_IF)
ap_if.active(False)

# Connect the device to the WiFi network
wifi = network.WLAN(network.STA_IF)
if wifi.isconnected():
    wifi.disconnect()  # Fix WiFi OS issue
wifi.active(True)

def do_connect():
    if not wifi.isconnected(): 
        print("Connecting to WiFi...")
        wifi.connect(WIFI_SSID, WIFI_PASSWORD)
        # Wait until the device is connected to the WiFi network
        MAX_ATTEMPTS = 20
        attempt_count = 0
        while not wifi.isconnected() and attempt_count < MAX_ATTEMPTS:
            attempt_count += 1
            time.sleep(1)

        if attempt_count == MAX_ATTEMPTS:
            print('Could not connect to WiFi')
            sys.exit()

do_connect()        

# MQTT setup
def sub_cb(topic, msg, retained, duplicate):
    print((topic, msg, retained, duplicate))
    m = msg.decode('utf-8')
    print("\n", m)

# Create a random MQTT client ID
random_num = int.from_bytes(os.urandom(3), 'little')
mqtt_client_id = bytes('client_' + str(random_num), 'utf-8')

# Adafruit IO MQTT broker information
ADAFRUIT_IO_URL = credentials["ADAFRUIT_IO_URL"]
ADAFRUIT_USERNAME = credentials["ADAFRUIT_USERNAME"]
ADAFRUIT_IO_KEY = credentials["ADAFRUIT_IO_KEY"]
ADAFRUIT_IO_FEEDNAME = credentials["ADAFRUIT_IO_FEEDNAME"]

# Set up the MQTT client
c = mqtt.MQTTClient(client_id=mqtt_client_id,
                    server=ADAFRUIT_IO_URL,
                    user=ADAFRUIT_USERNAME,
                    password=ADAFRUIT_IO_KEY,
                    ssl=False)
c.DEBUG = True
c.KEEP_QOS0 = False
c.NO_QUEUE_DUPS = True
c.MSG_QUEUE_MAX = 2

c.set_callback(sub_cb)

mqtt_feedname = '{:s}/feeds/{:s}'.format(ADAFRUIT_USERNAME, ADAFRUIT_IO_FEEDNAME)

if not c.connect(clean_session=False):
    print("Connecting to Adafruit IO with client ID:", random_num)
    c.subscribe(mqtt_feedname)

# Main loop
while True:
    c.check_msg()  # Check for new messages
    c.send_queue()  # Send any unsent messages
    try:
        soil.read()
        time.sleep(2)
        m = (max_moisture - soil.read()) * 100 / (max_moisture - min_moisture)
        print(m)
        if red_treshold > m:
            red_led.on()
            green_led.off()
            blue_led.off()
            info = "Dry"
        elif green_treshold > m and m > red_treshold:
            red_led.off()
            green_led.on()
            blue_led.off()
            info = "Moist"
        else:
            red_led.off()
            green_led.off()
            blue_led.on()
            info = "Wet"

        message = {
            "moisture": m,
            "timestamp": time.time(),
            "level": info
        }
        
        json_message = json.dumps(message)
        print("Published soil moisture: ", json_message)
        c.publish('plant/peperomia/json', str(json_message), qos=1)
        time.sleep(5)
    except KeyboardInterrupt:
        red_led.off()
        green_led.off()
        blue_led.off()
        break
    except Exception as e:
        print(f"Error in main loop: {e}")
    time.sleep(5)