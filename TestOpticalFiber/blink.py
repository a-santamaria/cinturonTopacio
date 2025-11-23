from machine import Pin
from utime import sleep

pin1 = Pin("LED", Pin.OUT)
pin = Pin(10, Pin.OUT)
pin11 = Pin(11, Pin.OUT)
pin12 = Pin(12, Pin.OUT)
print("LED starts flashing...")
while True:
    try:
        pin1.toggle()
        pin.toggle()
        pin11.toggle()
        pin12.toggle()
        sleep(1) # sleep 1sec
    except KeyboardInterrupt:
        break
pin1.off()
pin.off()
pin11.off()
pin12.off()
print("Finished.")
