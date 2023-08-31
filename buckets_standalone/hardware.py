"""
Hardware declarations for the timer project. 
Used to easily change pin connections without changing the primary code.
"""
import board

from busio import I2C, UART
from rotaryio import IncrementalEncoder
from digitalio import DigitalInOut, Pull, DriveMode
from neopixel import NeoPixel
from adafruit_debouncer import Button
from lcd import LCD
from i2c_pcf8574_interface import I2CPCF8574Interface

# I2C display assignments
lcd_i2c = I2C(board.GP1, board.GP0)
pcf_interface = None
# PCF8574 address can be two potential values
for addr in [0x27, 0x3F]:
    try:
        pcf_interface = I2CPCF8574Interface(lcd_i2c, addr)
    except ValueError:
        continue
    else:
        break
DISPLAY = LCD(pcf_interface, num_rows=2, num_cols=16)

# UART audio output
AUDIO = UART(board.GP4, board.GP5, baudrate=9600)

# Initialize RGB and inputs
iopins = (
    board.GP26_A0,  # RGB data pin
    board.GP8,  # Encoder pin 1
    board.GP7,  # Encoder pin 2
    board.GP6,  # Encoder button
    board.GP17,  # Red button
    board.GP14,  # Blue button
    board.GP16,  # Red LED
    board.GP15,  # Blue LED
)

# RGB strip setup
led_count = 58
RGB_LED = NeoPixel(iopins[0], led_count, brightness=0.1, auto_write=False)

# Encoder rotary setup
ENCODER = IncrementalEncoder(iopins[1], iopins[2])

# Setup button DIO objects
ENC, RED, BLUE = (DigitalInOut(pin) for pin in iopins[3:6])
for button in [ENC, RED, BLUE]:
    button.switch_to_input(Pull.UP)

# Create debouncer objects from DIO buttons
hold_duration = 1000  # ms
ENCB, REDB, BLUEB = (
    Button(ENC, long_duration_ms=2500),
    Button(RED, long_duration_ms=hold_duration),
    Button(BLUE, long_duration_ms=hold_duration),
)

# Team button LED setup
RED_LED, BLUE_LED = (DigitalInOut(pin) for pin in iopins[6:8])
for led in [RED_LED, BLUE_LED]:
    led.switch_to_output(False, DriveMode.PUSH_PULL)
