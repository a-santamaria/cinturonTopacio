from machine import Pin, ADC
import utime


THRESHOLD = 2100      # tune based on readings
DEBOUNCE_MS = 150

# pins
# VIB_PIN = 16        # DO from module
ADC_PIN = 26        # AO from module → GP26/ADC0
LED_PIN = "LED"     # use onboard LED
LED_EXT_PIN = 10    # external LED pin

led = Pin(LED_PIN, Pin.OUT)
led_ext = Pin(LED_EXT_PIN, Pin.OUT)
vib_adc = ADC(ADC_PIN)

_last = 0

def fire_pattern():
    led.on()
    led_ext.on()
    utime.sleep_ms(80)
    led.off()
    led_ext.off()

print("start program!!")

while True:
    reading = vib_adc.read_u16()
    print("VIB analog:", reading)

    t = utime.ticks_ms()
    if reading > THRESHOLD and utime.ticks_diff(t, _last) > DEBOUNCE_MS:
        _last = t
        print("Vibration detected at", t, "value:", reading)
        fire_pattern()

    utime.sleep_ms(50)