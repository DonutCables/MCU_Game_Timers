import board

from busio import I2C, UART
from rotaryio import IncrementalEncoder
from digitalio import DigitalInOut, Pull, DriveMode
from neopixel import NeoPixel
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
        print("LCD is not", hex(addr))
        continue
    else:
        print("LCD is", hex(addr))
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

led_count = 58
RGB_LED = NeoPixel(iopins[0], led_count, brightness=1, auto_write=False)

ENCODER = IncrementalEncoder(iopins[1], iopins[2])

ENC, RED, BLUE, RED_LED, BLUE_LED = (DigitalInOut(pin) for pin in iopins[3:])
for button in [ENC, RED, BLUE]:
    button.switch_to_input(Pull.UP)
for led in [RED_LED, BLUE_LED]:
    led.switch_to_output(False, DriveMode.PUSH_PULL)
