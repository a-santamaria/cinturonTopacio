import machine
import time
import neopixel

# --- Configuration ---
LED_PIN = 22        # GPIO pin connected to DIN of first LED
NUM_LEDS = 11        # Number of WS2812B LEDs
BRIGHTNESS = 0.05    # 0.0 (off) to 1.0 (full brightness)

# Create neopixel object
np = neopixel.NeoPixel(machine.Pin(LED_PIN), NUM_LEDS)

# --- Helper: Set all LEDs at once ---
def set_all(r, g, b):
    for i in range(NUM_LEDS):
        np[i] = (r, g, b)
    np.write()


def scale_color(color):
    """Scale an (r, g, b) tuple by the global brightness factor."""
    return tuple(int(component * BRIGHTNESS) for component in color)

# --- Test pattern: each LED a different color ---
colors = [
    scale_color((255,   0,   0)),  # LED 0 - Red
    scale_color((  0, 255,   0)),  # LED 1 - Green
    scale_color((  0,   0, 255)),  # LED 2 - Blue
    scale_color((255, 255,   0)),  # LED 3 - Yellow
    scale_color((255,   0, 255)),  # LED 4 - Magenta
    scale_color((  0, 255, 255)),  # LED 5 - Cyan
    scale_color((255, 100,   0)),  # LED 6 - Orange
    scale_color((180,   0, 255)),  # LED 7 - Purple
    scale_color((255, 255, 255)),  # LED 8 - White
    scale_color((180,   0, 255)),  # LED 9 - Dim gray
]

# Keep LEDs on forever (or press reset)
while True:
    time.sleep(1)
    try:
        for i in range(10):
            for j in range(NUM_LEDS):
                np[j] = colors[i]
                print("color = ", i)
            np.write()
            time.sleep(1)
    except KeyboardInterrupt:
        break

for j in range(NUM_LEDS):
    np[j] = (0,0,0)

np.write()
