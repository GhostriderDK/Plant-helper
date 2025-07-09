from mqtt_as import MQTTClient, config
from machine import Pin, ADC, SoftSPI, PWM
from bme680 import BME680_SPI
import time
import json
import asyncio
import network

# Initialize LEDs with PWM
led_humidity = PWM(Pin(27), freq=1000)
led_gas = PWM(Pin(14), freq=1000)

# Set LED brightness to 5%
def set_led_brightness(led, brightness_percent):
    duty_cycle = int((brightness_percent / 100) * 1023)
    led.duty(duty_cycle)

set_led_brightness(led_humidity, 5)
set_led_brightness(led_gas, 5)

# WiFi config
config['server'] = '77.33.140.232'  # Change to mqtt server ip
config['ssid'] = 'AirTies_Air4960_VCHY' # Change to wifi ssid
config['wifi_pw'] = 'pdcfcp9983' # Change to wifi password

# Other config
info = None

def reboot_esp():
    print("Rebooting!\n\n")
    import machine
    machine.reset()

def initialize_bme():
    cs = Pin(5, Pin.OUT, value=1)
    spi = SoftSPI(baudrate=400000, sck=Pin(18), mosi=Pin(19), miso=Pin(23))
    for _ in range(3):  # Retry 3 times
        try:
            bme = BME680_SPI(spi, cs)
            print("BME680 initialized")
            return bme
        except RuntimeError as e:
            print(f"Initialization failed: {e}")
            time.sleep(1)
    raise RuntimeError("Failed to initialize BME680 after 3 attempts")

bme = initialize_bme()

def gas_resistance_to_iaq(r_gas_ohm):
    r_gas_kohm = r_gas_ohm / 1000  # Convert Ohms to kilo-ohms for threshold comparison

    if r_gas_kohm > 200:
        return 50    # Excellent
    elif 100 < r_gas_kohm <= 200:
        return 75    # Good
    elif 50 < r_gas_kohm <= 100:
        return 150   # Moderate
    elif 20 < r_gas_kohm <= 50:
        return 200   # Poor
    elif 10 < r_gas_kohm <= 20:
        return 300   # Bad
    else:
        return 500    # Hazardous

def battery_percentage():
    adc = ADC(Pin(35))
    adc.atten(ADC.ATTN_11DB)
    adc.width(ADC.WIDTH_12BIT)
    adc_value = adc.read()
    return adc_value / 4095 * 100

def read_sensor():
    data = {
        'TEMP': bme.temperature,
        'HUMIDITY': bme.humidity,
        'PRESSURE': bme.pressure,
        'GAS': bme.gas,
        'ALTITUDE': bme.altitude,
        'BATTERY': battery_percentage(),
        'IAQ': gas_resistance_to_iaq(bme.gas)
    }
    data['IAQ_INFO'] = (
        "Excellent" if data['IAQ'] == 50 else
        "Good" if data['IAQ'] == 75 else
        "Moderate" if data['IAQ'] == 150 else
        "Poor" if data['IAQ'] == 200 else
        "Bad" if data['IAQ'] == 300 else
        "Hazardous"
    )
    return data

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
            sensor_data = read_sensor()
            json_message = json.dumps(sensor_data)
            print("Published air quality data: ", json_message)
            if mqtt_connected:
                await client.publish('air_quality/roam/json', str(json_message), qos=1)
            await asyncio.sleep(5)  # Sleep for 60 seconds
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

