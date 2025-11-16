from machine import Pin
from utime import sleep

pin1 = Pin("LED", Pin.OUT)
pin = Pin(15, Pin.OUT)

print("LED starts flashing...")
while True:
    try:
        pin1.toggle()
        pin.toggle()
        sleep(1) # sleep 1sec
    except KeyboardInterrupt:
        break
pin1.off()
pin.off()
print("Finished.")
