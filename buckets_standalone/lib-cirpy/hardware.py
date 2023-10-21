"""
Hardware declarations for the timer project.
Used to easily change pin connections without changing the primary code.
"""
import board
from busio import I2C, UART
from digitalio import DigitalInOut, Pull, DriveMode
from rotaryio import IncrementalEncoder
from neopixel import NeoPixel  # type: ignore
from adafruit_debouncer import Button  # type: ignore
from lcd_i2c8574_m import I2cLcd


class DisplayWrapper:
    """Wrapper for I2C LCD display"""

    def __init__(
        self,
        sda_pin=board.GP0,
        scl_pin=board.GP1,
        lcd_addresses=[0x27, 0x3F],
        rows=2,
        cols=16,
    ):
        self.i2c = I2C(scl_pin, sda_pin)
        self.display = None
        self.lcd_addresses = lcd_addresses
        self.dimensions = (cols, rows)
        self.init_lcd()

    def init_lcd(self):
        while self.i2c.try_lock():
            for addr in self.lcd_addresses:
                try:
                    self.display = I2cLcd(self.i2c, addr, self.dimensions)
                except Exception:
                    continue
                else:
                    return

    def write(self, text):
        if self.display is not None:
            self.display.write(text)

    def clear(self):
        if self.display is not None:
            self.display.clear()


DISPLAY = DisplayWrapper(board.GP0, board.GP1, rows=2, cols=16)

# UART audio output
AUDIO_OUT = UART(board.GP4, board.GP5, baudrate=9600)

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
RGB_LED = NeoPixel(iopins[0], led_count, brightness=1, auto_write=False)  # type: ignore

# Encoder rotary setup
ENCODER = IncrementalEncoder(iopins[1], iopins[2])

# Setup button DIO objects
ENC, RED, BLUE = (DigitalInOut(pin) for pin in iopins[3:6])
for button in [ENC, RED, BLUE]:
    button.switch_to_input(Pull.UP)

# Create debouncer objects from DIO buttons
hold_ms = 2000
ENCB, REDB, BLUEB = (
    Button(ENC, long_duration_ms=hold_ms),
    Button(RED, long_duration_ms=hold_ms),
    Button(BLUE, long_duration_ms=hold_ms),
)

# Team button LED setup
RED_LED, BLUE_LED = (DigitalInOut(pin) for pin in iopins[6:8])
for led in [RED_LED, BLUE_LED]:
    led.switch_to_output(False, DriveMode.PUSH_PULL)
