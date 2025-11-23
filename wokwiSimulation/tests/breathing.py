from machine import Pin, I2C
from neopixel import NeoPixel
from mpu6050 import MPU6050
import time
import math

# ---------- Setup ----------
# I2C for MPU6050
i2c = I2C(0, scl=Pin(11), sda=Pin(10), freq=400000)
sensor = MPU6050(i2c)

# Neopixels on GP22
NUM_LEDS = 10
np = NeoPixel(Pin(22), NUM_LEDS)

# Breathing parameters
base_brightness = 20    # minimum brightness
max_brightness = 150    # maximum brightness
breath_speed = 0.05     # speed of smooth breathing

# Helper to scale values
def scale(val, in_min, in_max, out_min, out_max):
    return (val - in_min) * (out_max - out_min) // (in_max - in_min) + out_min

# ---------- Main Loop ----------
while True:
    # Read accelerometer magnitude (motion intensity)
    ax, ay, az = sensor.get_accel()
    magnitude = math.sqrt(ax**2 + ay**2 + az**2)

    # Scale magnitude to brightness
    # Typical accel range ~ -17000 to +17000 in simulation; adjust if needed
    brightness = scale(magnitude, 0, 20000, base_brightness, max_brightness)
    brightness = min(max(brightness, base_brightness), max_brightness)

    # Create smooth breathing effect using sine wave
    t = time.ticks_ms() / 1000  # seconds
    factor = (math.sin(2 * math.pi * breath_speed * t) + 1) / 2  # 0..1

    # Final brightness per LED
    led_brightness = int(brightness * factor)

    # Set LEDs to a soft blue color with breathing brightness
    for i in range(NUM_LEDS):
        np[i] = (0, 0, led_brightness)

    np.write()
    time.sleep(0.05)
