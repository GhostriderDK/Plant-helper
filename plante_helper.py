from machine import Pin, ADC
import time

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
while True:
    try:
        soil.read()
        time.sleep(2)
        m = (max_moisture-soil.read())*100/(max_moisture-min_moisture)
        print(m)
        if red_treshold > m:
            red_led.on()
            green_led.off()
            blue_led.off()
        elif green_treshold > m and m > red_treshold:
            red_led.off()
            green_led.on()
            blue_led.off()
        else:
            red_led.off()
            green_led.off()
            blue_led.on()
        time.sleep(5)
    except KeyboardInterrupt:
        red_led.off()
        green_led.off()
        blue_led.off()
        break




