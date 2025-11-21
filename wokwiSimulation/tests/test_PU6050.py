from machine import I2C, Pin
from mpu6050 import MPU6050
import time

# Configure I2C on GP4 (SDA) and GP5 (SCL)
i2c = I2C(0, scl=Pin(21), sda=Pin(20), freq=400000)

sensor = MPU6050(i2c)

while True:
    ax, ay, az = sensor.get_accel()
    gx, gy, gz = sensor.get_gyro()
    print("Accel:", ax, ay, az)
    print("Gyro :", gx, gy, gz)
    time.sleep(0.5)