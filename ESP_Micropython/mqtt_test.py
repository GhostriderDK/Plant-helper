from mqtt_as import MQTTClient, config
import network
import uasyncio as asyncio

# WiFi config
config['server'] = '0.0.0.0'  # Change to your PC's local IP address
config['ssid'] = 'Fly by requested'
config['wifi_pw'] = 'P@tern!sFull'

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
    try:
        print("Connecting to MQTT broker...")
        await client.connect()
        print("Connected to MQTT broker")
    except Exception as e:
        print(f"Error connecting to MQTT broker: {e}")
        reboot_esp()

config["queue_len"] = 1  # Use event interface with default queue size
MQTTClient.DEBUG = True  # Optional: print diagnostic messages
client = MQTTClient(config)

try:
    asyncio.run(main(client))
finally:
    client.close()  # Prevent LmacRxBlk:1 errors