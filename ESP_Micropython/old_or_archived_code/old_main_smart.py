from machine import Pin, SoftSPI
import time
from bme680 import BME680_SPI
import json
import asyncio
import network


def gas_resistance_to_iaq(r_gas_ohm):
    """
    Convert gas resistance in Ohms to an IAQ index.

    Parameters:
        r_gas_ohm (int): Gas resistance in Ohms.

    Returns:
        int: IAQ index (50-500).
    """
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
        'GAS': bme.gas,
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

def control_leds(sensor_data):
    # Turn on/off LEDs based on sensor data

    if sensor_data['HUMIDITY'] > 20:
        led_humidity.on()
        print(sensor_data)
    else:
        led_humidity.off()

    if sensor_data['IAQ_INFO'] in ["Excellent", "Good", "Moderate"]:
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

