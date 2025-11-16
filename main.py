from machine import Pin, sleep

led = Pin("LED", Pin.OUT)

while True:
    led.toggle()
    sleep(500)