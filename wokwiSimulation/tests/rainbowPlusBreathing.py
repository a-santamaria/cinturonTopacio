from machine import Pin, I2C
from neopixel import NeoPixel
from mpu6050 import MPU6050
import time
import math

# ---------- Setup ----------
i2c = I2C(0, scl=Pin(5), sda=Pin(4), freq=400000)
sensor = MPU6050(i2c)

NUM_LEDS = 10
np = NeoPixel(Pin(22), NUM_LEDS)

# Breathing parameters
base_brightness = 30
max_brightness = 150
breath_speed = 0.05  # controls breathing sine wave speed

# ---------- Helper Functions ----------
def scale(val, in_min, in_max, out_min, out_max):
    return (val - in_min) * (out_max - out_min) // max((in_max - in_min), 1) + out_min

# Rainbow color wheel
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

# Track color offset for rainbow shift
offset = 0

# ---------- Main Loop ----------
while True:
    t = time.ticks_ms() / 1000  # seconds

    # --- Breathing based on accelerometer magnitude ---
    ax, ay, az = sensor.get_accel()
    magnitude = math.sqrt(ax**2 + ay**2 + az**2)
    brightness = scale(magnitude, 0, 20000, base_brightness, max_brightness)
    brightness = min(max(brightness, base_brightness), max_brightness)
    breath_factor = (math.sin(2 * math.pi * breath_speed * t) + 1) / 2
    led_brightness = int(brightness * breath_factor)

    # --- Gyro-based rainbow shift ---
    gx, gy, gz = sensor.get_gyro()
    offset += gz // 50  # adjust sensitivity of twist effect
    offset = offset % 256

    # --- Update LEDs ---
    for i in range(NUM_LEDS):
        idx = (i * 256 // NUM_LEDS + offset) % 256
        r, g, b = wheel(idx)
        # Apply breathing brightness to rainbow
        np[i] = (r * led_brightness // 255, g * led_brightness // 255, b * led_brightness // 255)

    np.write()
    time.sleep(0.05)
