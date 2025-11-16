from machine import Pin, ADC
import utime

# pins
VIB_PIN = 21        # DO from module
ADC_PIN = 26        # AO from module → GP26/ADC0
LED_PIN = "LED"     # use onboard LED
LED_EXT_PIN = 15    # external LED pin

led = Pin(LED_PIN, Pin.OUT)
led_ext = Pin(LED_EXT_PIN, Pin.OUT)
# vib = Pin(16, Pin.IN, Pin.PULL_UP)  # PULL_UP for active LOW
vib = Pin(VIB_PIN, Pin.IN, Pin.PULL_DOWN)   # idle low, pulses high on vibration
# vib = Pin(VIB_PIN, Pin.IN)  # adjust for your wiring

def edge_logger(pin):
    value = pin.value()
    edge = "RISING" if value else "FALLING"
    print("Edge:", edge, "value:", value, "time:", utime.ticks_ms())

vib.irq(handler=edge_logger, trigger=Pin.IRQ_RISING | Pin.IRQ_FALLING)

while True:
    utime.sleep(1)