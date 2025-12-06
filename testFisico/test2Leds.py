import machine
import time
import neopixel

# --- Configuration ---
LED_PIN = 22        # GPIO pin connected to DIN of first LED
NUM_LEDS = 2      # Number of WS2812B LEDs

# Create neopixel object
np = neopixel.NeoPixel(machine.Pin(LED_PIN), NUM_LEDS)

# --- Helper: Set all LEDs at once ---
def set_all(r, g, b):
    for i in range(NUM_LEDS):
        np[i] = (r, g, b)
    np.write()

# --- Test pattern: each LED a different color ---
colors = [
    (255,   0, 255),  # LED 4 - Magenta
    (255,   0,   0),  # LED 0 - Red
    (  0, 255,   0),  # LED 1 - Green
    (  0,   0, 255),  # LED 2 - Blue
    (255, 255,   0),  # LED 3 - Yellow
    # (255,   0, 255),  # LED 4 - Magenta
    (  0, 255, 255),  # LED 5 - Cyan
    (255, 100,   0),  # LED 6 - Orange
    (180,   0, 255),  # LED 7 - Purple
    (255, 255, 255),  # LED 8 - White
    (180,   0, 255),  # LED 9 - Dim gray
]

# Keep LEDs on forever (or press reset)
while True:
    time.sleep(1)
    try:
        for i in range(10):
            np[0] = colors[i]
            np[1] = colors[i]
            print("color = ", i)
            np.write()
            time.sleep(1)
    except KeyboardInterrupt:
        break

np[0] = (0,0,0)
np[1] = (0,0,0)
np.write()
