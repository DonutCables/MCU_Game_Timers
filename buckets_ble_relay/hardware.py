"""
Hardware declarations for the timer project.
Used to easily change pin connections without changing the primary code.
"""

import neopixel
from rotary_irq_rp2 import RotaryIRQ
from machine import Pin, I2C, UART
from adafruit_debouncer import Button
from lcd_i2c8574_m import I2cLcd

# I2C display assignments
lcd_i2c = I2C(0, sda=Pin(0), scl=Pin(1))
DISPLAY = None
# PCF8574 address can be two potential values
for addr in [0x27, 0x3F]:
    try:
        DISPLAY = I2cLcd(lcd_i2c, addr, (2, 16))
    except ValueError:
        continue
    else:
        break
"""LCD commands include .putstr and .clear"""

# UART audio output
AUDIO_OUT = UART(1, tx=Pin(4), rx=Pin(5), baudrate=9600)

# Initialize RGB and inputs
iopins = (
    Pin(26, Pin.OUT),  # RGB data pin
    8,    # Encoder pin 1
    7,    # Encoder pin 2
    6,    # Encoder button
    17,   # Red button
    14,   # Blue button
    16,  # Red LED
    15,  # Blue LED
)

# RGB strip setup
led_count = 58
RGB_LED = neopixel.NeoPixel(iopins[0], led_count)

# Encoder rotary setup
ENCODER = RotaryIRQ(pin_num_clk=8, pin_num_dt=7)

# Setup button DIO objects
ENC, RED, BLUE = (Pin(pin, Pin.IN, Pin.PULL_UP) for pin in iopins[3:6])

# Team button LED setup
RED_LED, BLUE_LED = (Pin(pin, Pin.OUT) for pin in iopins[6:8])

# Constants for button debounce and hold duration
HOLD_DURATION_MS = 1000

# Create debouncer objects from DIO buttons
ENCB = Button(ENC, long_duration_ms=HOLD_DURATION_MS)
REDB = Button(RED, long_duration_ms=HOLD_DURATION_MS)
BLUEB = Button(BLUE, long_duration_ms=HOLD_DURATION_MS)
