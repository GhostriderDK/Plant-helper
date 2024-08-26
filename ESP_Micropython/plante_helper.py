from mqtt_as import MQTTClient, config
from machine import Pin, ADC
import time
import json
import asyncio

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

min_moisture=0
max_moisture=4095

soil.atten(ADC.ATTN_11DB)       #Full range: 3.3v
soil.width(ADC.WIDTH_12BIT)     #range 0 to 4095

red_treshold = 30
green_treshold = 80

# Wifi config
config['server'] = '52.236.38.161'  # Change to suit
config['ssid'] = 'iot'
config['wifi_pw'] = 'gruppe06'

#other config
info = None

# test leds at startup
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
        await client.subscribe('plant_topic', 1)  # renew subscriptions


async def main(client):
    try:
        await client.connect()
    except:
        print('Error')
        reboot_esp()

    for coroutine in (up, messages):
        asyncio.create_task(coroutine(client))

    while True:
        await asyncio.sleep(5)
        try:
            soil.read()
            time.sleep(2)
            m = (max_moisture-soil.read())*100/(max_moisture-min_moisture)
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

            message = {"soil_moisture": m, 
                       "timestamp": time.time(), 
                       "level": info}
            
            json_message = json.dumps(message)
            print("Published soil moisture: ", json_message)
            await client.publish('plant_topic', str(json_message), qos = 1)
            time.sleep(5)
        except KeyboardInterrupt:
            red_led.off()
            green_led.off()
            blue_led.off()
            break
        await asyncio.sleep(5)


# while True:
#     try:
#         soil.read()
#         time.sleep(2)
#         m = (max_moisture-soil.read())*100/(max_moisture-min_moisture)
#         print(m)
#         if red_treshold > m:
#             red_led.on()
#             green_led.off()
#             blue_led.off()
#         elif green_treshold > m and m > red_treshold:
#             red_led.off()
#             green_led.on()
#             blue_led.off()
#         else:
#             red_led.off()
#             green_led.off()
#             blue_led.on()
#         time.sleep(5)
#     except KeyboardInterrupt:
#         red_led.off()
#         green_led.off()
#         blue_led.off()
#         break

config["queue_len"] = 1  # Use event interface with default queue size
MQTTClient.DEBUG = True  # Optional: print diagnostic messages
client = MQTTClient(config)
try:
    asyncio.run(main(client))
finally:
    client.close()  # Prevent LmacRxBlk:1 errors




