from machine import Pin, ADC
import utime


ADC_PIN = 26             # AO from module → GP26/ADC0
LED_PINS = (10, 11, 12)  # red, green, blue

# Adjust these after watching the printed readings
LEVEL_ONE = 8000
LEVEL_TWO = 18000
LEVEL_THREE = 32000

COOLDOWN_MS = 120
CHASE_DELAY_MS = 140

vib_adc = ADC(ADC_PIN)
leds = [Pin(pin, Pin.OUT) for pin in LED_PINS]

_last = 0


def all_off():
    for led in leds:
        led.off()


def chase_once(delay_ms):
    for led in leds:
        print("chase_once led=", led, " value=", led.value())
        led.on()
        print("chase_once led=", led, " value=", led.value())
        utime.sleep_ms(delay_ms)
        led.off()
        print("chase_once led=", led, " value=", led.value())


def chase_burst(level):
    if level == 1:
        chase_once(CHASE_DELAY_MS)
    elif level == 2:
        for _ in range(2):
            chase_once(CHASE_DELAY_MS // 2)
    else:
        for _ in range(2):
            for led in leds:
                led.on()
            utime.sleep_ms(60)
            all_off()
            chase_once(CHASE_DELAY_MS // 3)


print("Analog chase burst ready!")

while True:
    reading = vib_adc.read_u16()
    # print("VIB analog:", reading)

    level = 0
    if reading > LEVEL_THREE:
        level = 3
    elif reading > LEVEL_TWO:
        level = 2
    elif reading > LEVEL_ONE:
        level = 1

    t = utime.ticks_ms()
    if level and utime.ticks_diff(t, _last) > COOLDOWN_MS:
        _last = t
        print("Chase level", level, "triggered at", t)
        chase_burst(level)
        all_off()

    utime.sleep_ms(40)