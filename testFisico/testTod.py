from machine import I2C, Pin
#from BMI160 import BMI160
import time
import math
import neopixel

BMI160_ADDR = 0x68

class BMI160:
    def __init__(self, i2c, addr=0x68):
        self.i2c = i2c
        self.addr = addr

        # Power on accelerometer + gyro (normal mode)
        self.i2c.writeto_mem(addr, 0x7E, bytes([0x11]))  # accel normal
        time.sleep(0.05)
        self.i2c.writeto_mem(addr, 0x7E, bytes([0x15]))  # gyro normal
        time.sleep(0.05)

    def read16(self, reg):
        data = self.i2c.readfrom_mem(self.addr, reg, 2)
        return int.from_bytes(data, "little")

    def get_accel(self):
        ax = self.read16(0x12)
        ay = self.read16(0x14)
        az = self.read16(0x16)
        return ax, ay, az

    def get_gyro(self):
        gx = self.read16(0x0C)
        gy = self.read16(0x0E)
        gz = self.read16(0x10)
        return gx, gy, gz

    def get_temperature(self):
        return self.read16(0x20)


# ---- Example use ----
i2c = I2C(1, scl=Pin(11), sda=Pin(10), freq=400000)

sensor = BMI160(i2c)

NUM_LEDS = 2
np = neopixel.NeoPixel(Pin(22), NUM_LEDS)

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
    # gx, gy, gz = sensor.get_gyro()
    ax, ay, az = sensor.get_accel()
    gx, gy, gz = sensor.get_gyro()
    t = sensor.get_temperature()

    print("Accel:", ax, ay, az)
    print("Gyro :", gx, gy, gz)
    print("Temp :", t)
    print("-----")

    # Scale rotation to offset change (adjust sensitivity)
    offset += gz // 50  # integer division to slow down rotation effect
    offset = offset % 256

    
    time.sleep(0.1)

    # Update LEDs with rainbow along the strip
    for i in range(NUM_LEDS):
        idx = (i * 256 // NUM_LEDS + offset) % 256
        np[i] = wheel(idx)
    
    np.write()
    time.sleep(0.05)


# while True:
    # ax, ay, az = sensor.get_accel()
    # gx, gy, gz = sensor.get_gyro()
    # t = sensor.get_temperature()

    # print("Accel:", ax, ay, az)
    # print("Gyro :", gx, gy, gz)
    # print("Temp :", t)
    # print("-----")
    # time.sleep(0.1)