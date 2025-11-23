# Save as mpu6050.py
from machine import I2C

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