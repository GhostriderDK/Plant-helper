# Soil Moisture Monitor

This Python script is designed to monitor soil moisture levels using a soil moisture sensor connected to an ADC pin on an ESP32 dev kit. 

The script uses three LEDs (red, green, and blue) to indicate the moisture level. The moisture level is calculated as a percentage of the maximum possible reading from the ADC.

The LEDs are controlled as follows:
- Red LED: Turns on when the moisture level is below 30% indicating dry soil.
- Green LED: Turns on when the moisture level is between 30% and 80% indicating moist soil.
- Blue LED: Turns on when the moisture level is above 80% indicating wet soil.

The script runs in an infinite loop, continuously reading the moisture level and updating the LED status. The loop can be interrupted with a KeyboardInterrupt, at which point all LEDs are turned off and the script ends.

In the future, this project will be extended to include a Flask web application with a SQL database. The web application will display the soil moisture data, providing a user-friendly interface for monitoring the soil conditions.

## Dependencies
- machine module from MicroPython: Provides classes for interfacing with the hardware peripherals available on the microcontroller.
- time module: Provides functions for working with time, including delays.

## Hardware setup (pin numbers can be changed if want to use other pins)
- ESP32 dev kit
- Red LED connected to pin 4.
- Green LED connected to pin 16.
- Blue LED connected to pin 17.
- Soil moisture sensor connected to ADC pin 35.