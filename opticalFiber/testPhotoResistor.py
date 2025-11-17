from machine import ADC, Pin
import time

# Create ADC object on GP26 (ADC0)
ldr = ADC(Pin(26))

while True:
    value = ldr.read_u16()   # Range: 0–65535
    print("LDR:", value)
    time.sleep(0.1)