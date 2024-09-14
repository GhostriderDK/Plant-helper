# Soil Moisture Monitor

This Python project is designed to monitor soil moisture levels using a soil moisture sensor connected to an ADC pin on an ESP32 dev kit. It also includes temperature and humidity monitoring using a DHT11 sensor.

The project consists of four main scripts:
- `app.py`: Implements a Flask web application to visualize the soil moisture, temperature, and humidity data.
- `get_data.py`: Contains functions to read data from the soil moisture sensor and the DHT11 sensor.
- `log_data.py`: Handles logging of sensor data to a CSV file.
- `main.py`: The main script that integrates all functionalities, including reading sensor data, logging it, and updating the LED status.

The LEDs are controlled as follows:
- **Red LED**: Turns on when the moisture level is below 30%, indicating dry soil.
- **Green LED**: Turns on when the moisture level is between 30% and 80%, indicating moist soil.
- **Blue LED**: Turns on when the moisture level is above 80%, indicating wet soil.

The script runs in an infinite loop, continuously reading the moisture level and updating the LED status. The loop can be interrupted with a `KeyboardInterrupt`, at which point all LEDs are turned off and the script ends.

## Dependencies
- `machine` module from MicroPython: Provides classes for interfacing with the hardware peripherals available on the microcontroller.
- `time` module: Provides functions for working with time, including delays.
- `os` module: Provides functions for interacting with the operating system, used for file operations.
- `flask` module: Provides the web framework for the web application.
- `paho-mqtt` module: Provides MQTT capabilities for sending data to a remote server.

## Hardware setup (pin numbers can be changed if you want to use other pins)
- ESP32 dev kit
- Red LED connected to pin 4
- Green LED connected to pin 16
- Blue LED connected to pin 17
- Soil moisture sensor connected to ADC pin 35

## Features
- MQTT capability to send soil moisture, temperature, and humidity data to a remote server.
- Flask web application with a SQL database to visualize the data received through MQTT.
- LED control logic to include moisture thresholds.
- Flask web application with visualization of the logged data.

## New Features
- Added an overview site to give a important info fast without having to look on the graph.
- - includes current rounded percentage of moisture in the soil, timestamp for last watering and the current level: wet, moist or dry. with a coloured circle to make it clearer
- - Watering autodetection and timestamp keeping, so even if the last watering isn't within the scanned dataset pulled from the database it will still be displayed in the overview


## Future Enhancements in order of implementation priority
- Add a list of the last waterings in format [(plant) watered (timestamp) from (lower percentage) -> (upper percentage)], on the right side of overview
- Add support for remote notifications via email or SMS when soil moisture levels are critical.
- Implement a calibration routine for the soil moisture sensor to improve accuracy.
- Add a battery power option with low-power optimizations for the ESP32.
- Add support for additional sensor types and data logging formats.
- Implement user authentication for the web application.

## Additional Dependencies
- `sqlite3` module: Provides a lightweight disk-based database that doesn’t require a separate server process and allows access to the database using a nonstandard variant of the SQL query language.