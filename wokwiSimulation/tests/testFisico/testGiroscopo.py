from machine import I2C, Pin
#from mpu6050 import MPU6050
import time
import math

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

    def accel(self):
        ax = self.read16(0x12)
        ay = self.read16(0x14)
        az = self.read16(0x16)
        return ax, ay, az

    def gyro(self):
        gx = self.read16(0x0C)
        gy = self.read16(0x0E)
        gz = self.read16(0x10)
        return gx, gy, gz

    def temperature(self):
        return self.read16(0x20)


# ---- Example use ----
i2c = I2C(1, scl=Pin(11), sda=Pin(10), freq=400000)

sensor = BMI160(i2c)

while True:
    ax, ay, az = sensor.accel()
    gx, gy, gz = sensor.gyro()
    t = sensor.temperature()

    print("Accel:", ax, ay, az)
    print("Gyro :", gx, gy, gz)
    print("Temp :", t)
    print("-----")
    time.sleep(0.1)