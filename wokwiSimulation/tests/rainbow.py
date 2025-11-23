from machine import Pin, I2C
from neopixel import NeoPixel
from mpu6050 import MPU6050
import time

# ---------- Setup ----------
i2c = I2C(0, scl=Pin(11), sda=Pin(10), freq=400000)
sensor = MPU6050(i2c)

NUM_LEDS = 10
np = NeoPixel(Pin(22), NUM_LEDS)

# Rainbow helper
def wheel(pos):
    pos = pos % 256
    if pos < 85:
        return (pos * 3, 255 - pos * 3, 0)
    elif pos < 170:
        pos -= 85
        return (255 - pos * 3, 0, pos * 3)
    else:
        pos -= 170
        return (0, pos * 3, 255 - pos * 3)

# Track color offset
offset = 0

# ---------- Main Loop ----------
while True:
    # Read Z-axis gyro (rotation around vertical axis)
    gx, gy, gz = sensor.get_gyro()

    # Scale rotation to offset change (adjust sensitivity)
    offset += gz // 50  # integer division to slow down rotation effect
    offset = offset % 256

    # Update LEDs with rainbow along the strip
    for i in range(NUM_LEDS):
        idx = (i * 256 // NUM_LEDS + offset) % 256
        np[i] = wheel(idx)
    
    np.write()
    time.sleep(0.05)
