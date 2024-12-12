from machine import Pin, SoftSPI
import time
from bme680 import BME680_SPI
import json
import asyncio
import network


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


# Initialize LEDs
led_humidity = Pin(27, Pin.OUT)
led_gas = Pin(14, Pin.OUT)

def read_sensor():
    data = {
        'TEMP': bme.temperature,
        'HUMIDITY': bme.humidity,
        'PRESSURE': bme.pressure,
        'GAS': bme.gas,
        'ALTITUDE': bme.altitude}    
    return data

def control_leds(sensor_data):
    # Turn on/off LEDs based on sensor data

    if sensor_data['HUMIDITY'] > 50:
        led_humidity.on()
        print(sensor_data)
    else:
        led_humidity.off()

    if sensor_data['GAS'] > 1000:
        led_gas.on()
        print(sensor_data)
    else:
        led_gas.off()

def publish_data():
    # Publish sensor data to MQTT broker
    pass

while True:
    try:
        sensor_data = read_sensor()
        control_leds(sensor_data)
        time.sleep(1)

    except KeyboardInterrupt:
        break

