from mqtt_as import MQTTClient, config
from machine import Pin, ADC
import time
import json
import asyncio
import network

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

red_treshold = 50
green_treshold = 75

# WiFi config
config['server'] = '########'  # Change to mqtt server ip
config['ssid'] = '#########' # Change to wifi ssid
config['wifi_pw'] = '#######' # Change to wifi password

# Other config
info = None

# Test LEDs at startup
red_led.on()
time.sleep(1)
red_led.off()
time.sleep(1)
green_led.on()
time.sleep(1)
green_led.off()
time.sleep(1)
blue_led.on()
time.sleep(1)
blue_led.off()
time.sleep(1)

def reboot_esp():
    print("Rebooting!\n\n")
    import machine
    machine.reset()

async def up(client):  # Respond to connectivity being (re)established
    while True:
        await client.up.wait()  # Wait on an Event
        client.up.clear()
        await client.subscribe('plant_topic', 1)  # Renew subscriptions

async def connect_wifi():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(config['ssid'], config['wifi_pw'])
    max_attempts = 10
    attempt = 0
    while not wlan.isconnected() and attempt < max_attempts:
        print(f"Connecting to WiFi... Attempt {attempt + 1}")
        await asyncio.sleep(1)
        attempt += 1
    if wlan.isconnected():
        print("Connected to WiFi")
    else:
        print("Failed to connect to WiFi")
        reboot_esp()

async def main(client):
    await connect_wifi()
    mqtt_connected = False
    try:
        print("Connecting to MQTT broker...")
        await client.connect()
        print("Connected to MQTT broker")
        mqtt_connected = True
    except Exception as e:
        print(f"Error connecting to MQTT broker: {e}")

    if mqtt_connected:
        asyncio.create_task(up(client))

    while True:
        await asyncio.sleep(5)
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
                "soil": m,
                "timestamp": time.time(),
                "level": info
            }
            
            json_message = json.dumps(message)
            print("Published soil moisture: ", json_message)
            if mqtt_connected:
                await client.publish('plant/peperomia/json', str(json_message), qos=1)
            time.sleep(600)
        except KeyboardInterrupt:
            red_led.off()
            green_led.off()
            blue_led.off()
            break
        except Exception as e:
            print(f"Error in main loop: {e}")
        await asyncio.sleep(5)

config["queue_len"] = 1  # Use event interface with default queue size
MQTTClient.DEBUG = True  # Optional: print diagnostic messages
client = MQTTClient(config)
try:
    asyncio.run(main(client))
finally:
    client.close()  # Prevent LmacRxBlk:1 errors
