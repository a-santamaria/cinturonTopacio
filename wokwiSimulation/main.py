from machine import Pin, I2C
from neopixel import NeoPixel
from mpu6050 import MPU6050
import time
import math
import urandom

# ---------- Setup ----------
i2c = I2C(0, scl=Pin(11), sda=Pin(10), freq=400000)
sensor = MPU6050(i2c)

NUM_LEDS = 10
np = NeoPixel(Pin(22), NUM_LEDS)

# Breathing parameters
base_brightness = 40
max_brightness = 150
breath_speed = 0.05

# Step detection
step_threshold = 13000
last_step_time = 0
step_delay = 0.4  # seconds
step_echo_length = 3  # LEDs in pulse

# Rainbow offset for twist
offset = 0

# ---------- Helper Functions ----------
def scale(val, in_min, in_max, out_min, out_max):
    return (val - in_min) * (out_max - out_min) // max((in_max - in_min), 1) + out_min

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

# Step pulse tracking
pulse_leds = [0] * NUM_LEDS  # brightness factor for step echo

# ---------- Main Loop ----------
while True:
    t = time.ticks_ms() / 1000

    # --- Breathing effect ---
    ax, ay, az = sensor.get_accel()
    magnitude = math.sqrt(ax**2 + ay**2 + az**2)
    brightness = scale(magnitude, 0, 20000, base_brightness, max_brightness)
    brightness = min(max(brightness, base_brightness), max_brightness)
    breath_factor = (math.sin(2 * math.pi * breath_speed * t) + 1) / 2
    base_led_brightness = int(brightness * breath_factor)

    # --- Gyro rainbow shift ---
    gx, gy, gz = sensor.get_gyro()
    offset += gz // 50
    offset = offset % 256

    # --- Step detection ---
    now = time.time()
    if magnitude > step_threshold and now - last_step_time > step_delay:
        last_step_time = now
        # Trigger step pulse: illuminate first few LEDs
        for i in range(step_echo_length):
            if i < NUM_LEDS:
                pulse_leds[i] = 255  # max pulse brightness

    # --- Update LEDs ---
    for i in range(NUM_LEDS):
        # Rainbow color
        idx = (i * 256 // NUM_LEDS + offset) % 256
        r, g, b = wheel(idx)

        # Combine breathing
        r = r * base_led_brightness // 255
        g = g * base_led_brightness // 255
        b = b * base_led_brightness // 255

        # Add step pulse
        pulse = pulse_leds[i]
        r = min(r + pulse, 255)
        g = min(g + pulse, 255)
        b = min(b + pulse, 255)

        # Organic flicker
        flicker = urandom.getrandbits(4)  # small 0-15 random
        r = min(r + flicker, 255)
        g = min(g + flicker, 255)
        b = min(b + flicker, 255)

        np[i] = (r, g, b)

        # Decay pulse for next iteration
        if pulse_leds[i] > 0:
            pulse_leds[i] = max(pulse_leds[i] - 25, 0)

    np.write()
    time.sleep(0.05)
