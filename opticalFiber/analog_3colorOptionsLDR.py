from machine import Pin, ADC, PWM
import utime
import urandom


ADC_PIN = 26             # LDR photoresistor → GP26/ADC0
LED_PINS = (10, 11, 12)  # red, green, blue

# ========== CHANGE THIS TO SELECT PATTERN (1-8) ==========
PATTERN_MODE = 8
# 1: Chase Burst (original)
# 2: Intensity Bar Graph
# 3: Color Fade/Pulse
# 4: Wave Pattern
# 5: Random Sparkle
# 6: Build-Up Pattern
# 7: Morse/Rhythm Pattern
# 8: Breathing Effect (PWM)
# ==========================================================

# Adjust these after watching the printed readings
# For LDR: Higher values = more light, Lower values = less light
LEVEL_ONE = 30000    # Dim light
LEVEL_TWO = 45000    # Medium light
LEVEL_THREE = 55000  # Bright light

COOLDOWN_MS = 120
CHASE_DELAY_MS = 140

ldr = ADC(Pin(ADC_PIN))
leds = [Pin(pin, Pin.OUT) for pin in LED_PINS]

if PATTERN_MODE == 8:
    pwm_leds = [PWM(Pin(pin)) for pin in LED_PINS]  # For breathing effect
    for pwm in pwm_leds:
        pwm.freq(1000)
else:
    pwm_leds = []

_last = 0


def all_off():
    if PATTERN_MODE == 8:
        for pwm in pwm_leds:
            pwm.duty_u16(0)
    else:
        for led in leds:
            led.off()


# ========== PATTERN 1: Chase Burst (Original) ==========
def chase_once(delay_ms):
    for led in leds:
        led.on()
        utime.sleep_ms(delay_ms)
        led.off()

def pattern_chase_burst(level):
    if level == 1:
        chase_once(CHASE_DELAY_MS)
    elif level == 2:
        for _ in range(2):
            chase_once(CHASE_DELAY_MS // 2)
    else:
        for _ in range(2):
            for led in leds:
                led.on()
            utime.sleep_ms(60)
            all_off()
            chase_once(CHASE_DELAY_MS // 3)


# ========== PATTERN 2: Intensity Bar Graph ==========
def pattern_bar_graph(level):
    all_off()
    if level == 1:
        leds[0].on()  # Red only
        utime.sleep_ms(300)
    elif level == 2:
        leds[0].on()  # Red + Green
        leds[1].on()
        utime.sleep_ms(300)
    else:
        for led in leds:  # All LEDs
            led.on()
        utime.sleep_ms(300)


# ========== PATTERN 3: Color Fade/Pulse ==========
def pattern_pulse(level):
    repeats = 1 if level == 1 else (2 if level == 2 else 4)
    delay = 100 if level == 1 else (50 if level == 2 else 25)
    
    active_leds = leds[:level]
    for _ in range(repeats):
        for led in active_leds:
            led.on()
        utime.sleep_ms(delay)
        for led in active_leds:
            led.off()
        utime.sleep_ms(delay)


# ========== PATTERN 4: Wave Pattern ==========
def pattern_wave(level):
    if level == 1:
        # Single wave left-to-right
        for led in leds:
            led.on()
            utime.sleep_ms(80)
            led.off()
    elif level == 2:
        # Bounce wave
        for led in leds:
            led.on()
            utime.sleep_ms(50)
            led.off()
        for led in reversed(leds):
            led.on()
            utime.sleep_ms(50)
            led.off()
    else:
        # Rapid bidirectional
        for _ in range(2):
            for led in leds:
                led.on()
                utime.sleep_ms(30)
                led.off()
            for led in reversed(leds):
                led.on()
                utime.sleep_ms(30)
                led.off()


# ========== PATTERN 5: Random Sparkle ==========
def pattern_sparkle(level):
    flashes = 3 if level == 1 else (6 if level == 2 else 12)
    delay = 100 if level == 1 else (50 if level == 2 else 25)
    
    for _ in range(flashes):
        all_off()
        if level == 1:
            leds[urandom.randint(0, 2)].on()
        elif level == 2:
            leds[urandom.randint(0, 2)].on()
            leds[urandom.randint(0, 2)].on()
        else:
            for led in leds:
                if urandom.randint(0, 1):
                    led.on()
        utime.sleep_ms(delay)
    all_off()


# ========== PATTERN 6: Build-Up Pattern ==========
def pattern_buildup(level):
    if level == 1:
        leds[0].on()
        utime.sleep_ms(150)
        leds[0].off()
    elif level == 2:
        leds[0].on()
        utime.sleep_ms(100)
        leds[1].on()
        utime.sleep_ms(100)
        all_off()
    else:
        for i, led in enumerate(leds):
            led.on()
            utime.sleep_ms(60)
        utime.sleep_ms(100)
        all_off()
        for led in leds:
            led.on()
        utime.sleep_ms(100)


# ========== PATTERN 7: Morse/Rhythm Pattern ==========
def pattern_morse(level):
    short = 80
    long = 200
    gap = 100
    
    if level == 1:
        # Two short blinks
        for _ in range(2):
            leds[0].on()
            utime.sleep_ms(short)
            leds[0].off()
            utime.sleep_ms(gap)
    elif level == 2:
        # Short-long pattern
        leds[1].on()
        utime.sleep_ms(short)
        leds[1].off()
        utime.sleep_ms(gap)
        leds[1].on()
        utime.sleep_ms(long)
        leds[1].off()
    else:
        # SOS: ... --- ...
        for _ in range(3):
            for led in leds:
                led.on()
            utime.sleep_ms(short)
            all_off()
            utime.sleep_ms(gap)
        for _ in range(3):
            for led in leds:
                led.on()
            utime.sleep_ms(long)
            all_off()
            utime.sleep_ms(gap)
        for _ in range(3):
            for led in leds:
                led.on()
            utime.sleep_ms(short)
            all_off()
            utime.sleep_ms(gap)


# ========== PATTERN 8: Breathing Effect (PWM) ==========
def pattern_breathing(level):
    all_off()
    steps = 20 if level == 1 else (15 if level == 2 else 10)
    delay = 30 if level == 1 else (20 if level == 2 else 10)
    cycles = 1 if level == 1 else (2 if level == 2 else 3)
    
    active_pwms = pwm_leds[:level]
    
    for _ in range(cycles):
        # Fade in
        for i in range(steps):
            duty = int((i / steps) * 65535)
            for pwm in active_pwms:
                pwm.duty_u16(duty)
            utime.sleep_ms(delay)
        # Fade out
        for i in range(steps, 0, -1):
            duty = int((i / steps) * 65535)
            for pwm in active_pwms:
                pwm.duty_u16(duty)
            utime.sleep_ms(delay)
    
    all_off()


# ========== Pattern Dispatcher ==========
def run_pattern(level):
    if PATTERN_MODE == 1:
        pattern_chase_burst(level)
    elif PATTERN_MODE == 2:
        pattern_bar_graph(level)
    elif PATTERN_MODE == 3:
        pattern_pulse(level)
    elif PATTERN_MODE == 4:
        pattern_wave(level)
    elif PATTERN_MODE == 5:
        pattern_sparkle(level)
    elif PATTERN_MODE == 6:
        pattern_buildup(level)
    elif PATTERN_MODE == 7:
        pattern_morse(level)
    elif PATTERN_MODE == 8:
        pattern_breathing(level)
        # pass
    else:
        print("Invalid pattern mode!")


print(f"LDR light sensor ready - Pattern Mode {PATTERN_MODE}")


while True:
    reading = ldr.read_u16()
    # print("Light level:", reading)

    level = 0
    if reading > LEVEL_THREE:
        level = 3
    elif reading > LEVEL_TWO:
        level = 2
    elif reading > LEVEL_ONE:
        level = 1

    t = utime.ticks_ms()
    if level and utime.ticks_diff(t, _last) > COOLDOWN_MS:
        _last = t
        print("Pattern", PATTERN_MODE, "- Level", level, " - value", reading, "triggered at", t)
        run_pattern(level)
        all_off()

    utime.sleep_ms(40)