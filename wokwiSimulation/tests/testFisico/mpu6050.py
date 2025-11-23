# Save as mpu6050.py
from machine import I2C
import math

class MPU6050:
    def __init__(self, i2c, addr=0x68):
        self.i2c = i2c
        self.addr = addr
        # Wake up sensor
        self.i2c.writeto_mem(self.addr, 0x6B, bytes([0]))
    
    def read_raw_data(self, reg):
        high = self.i2c.readfrom_mem(self.addr, reg, 1)[0]
        low = self.i2c.readfrom_mem(self.addr, reg+1, 1)[0]
        value = (high << 8) | low
        if value > 32768:
            value -= 65536
        return value
    
    def get_accel(self):
        ax = self.read_raw_data(0x3B)
        ay = self.read_raw_data(0x3D)
        az = self.read_raw_data(0x3F)
        return ax, ay, az
    
    def get_gyro(self):
        gx = self.read_raw_data(0x43)
        gy = self.read_raw_data(0x45)
        gz = self.read_raw_data(0x47)
        return gx, gy, gz