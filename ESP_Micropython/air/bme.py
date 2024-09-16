from mqtt_as import MQTTClient, config
import time
from bme680 import BME680_SPI
from machine import Pin
import json
import asyncio
import network
import machine


# WiFi config
config['server'] = '##############'  # Change to mqtt server ip
config['ssid'] = '###########' # Change to wifi ssid
config['wifi_pw'] = '#############' # Change to wifi password

# BME680 sensor config
def initialize_bme():
    cs = Pin(5, Pin.OUT, value=1)
    spi = machine.SoftSPI(baudrate=400000, sck=Pin(18), mosi=Pin(19), miso=Pin(23))
    bme = BME680_SPI(spi, cs)
    return bme

bme = initialize_bme()


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
            message =  {
                'TEMP': bme.temperature,
                'HUMIDITY': bme.humidity,
                'PRESSURE': bme.pressure,
                'GAS': bme.gas,
                'ALTITUDE': bme.altitude}
            
            json_message = json.dumps(message)
            print("Published soil moisture: ", json_message)
            if mqtt_connected:
                await client.publish('air/bathroom/json', str(json_message), qos=1)
            time.sleep(60)
        except KeyboardInterrupt:
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

